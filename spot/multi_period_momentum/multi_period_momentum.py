"""
Multi-Period Momentum Strategy (Spot - Long Only)

=== FIXED VALUES (DO NOT CHANGE) ===

1. Import Path
   - from common.xxx import ... (FIXED)
   - Server uses user-specific common folder for uploaded module files

2. Function Signature
   - def strategy(context: DataContext, config_dict: dict) -> dict (FIXED)

3. Config Access
   - assets = config_dict['assets'] (FIXED)
   - frequency = config_dict.get("frequency", "1m") (FIXED)
   - Other config_dict parameters are custom per strategy

4. History API
   - context.get_history(assets=, window=, frequency=, fields=) (FIXED)
   - fields: list of required columns from ohlcv (e.g., ["close"], ["open", "high", "low", "close"])
   - Returns: MultiIndex DataFrame (asset, datetime)
     ```
                                         open    high     low   close    volume
    asset    datetime
    BTCUSDT  2025-11-13 04:01:00+00:00  100.0   100.2    99.7   100.0   37215.0
    ETHUSDT  2025-11-13 04:01:00+00:00  105.1   105.1   104.7   105.0   74304.2
     ```

5. Return Format (FIXED - SPOT)
   {
       "SYMBOL": {
           "weight": float,              # >= 0, long only, sum <= 1.0
           "presetTakeProfitPrice": float, # can be None
           "presetStopLossPrice": float    # can be None
       }
   }
"""

# [FIXED] Import: from common.xxx (server uses user-specific common folder)
from module.data_context import DataContext
from common.momentum_utils import calculate_momentum
from common.sltp_utils import compute_sltp

import pandas as pd


def parse_frequency_to_minutes(frequency: str) -> int:
    """
    Convert frequency string to minutes.
    Example: "1m" -> 1, "5m" -> 5, "15m" -> 15, "1h" -> 60, "1d" -> 1440
    """
    freq = frequency.lower().strip()
    if freq.endswith("m"):
        return int(freq[:-1])
    elif freq.endswith("h"):
        return int(freq[:-1]) * 60
    elif freq.endswith("d"):
        return int(freq[:-1]) * 1440
    else:
        return 1  # default 1 minute


def normalize_weights_long_only(momentum: dict, long_ratio: float) -> dict:
    """
    Normalize weights for spot trading (long only).
    Only assets with positive momentum receive allocation.
    Assets with zero or negative momentum get weight = 0.
    """
    longs = {k: v for k, v in momentum.items() if v > 0}
    weights = {}

    total_long = sum(longs.values())
    for k, v in longs.items():
        weights[k] = (v / total_long) * long_ratio if total_long != 0 else 0

    # Zero or negative momentum assets get 0 weight
    for k in momentum:
        if k not in weights:
            weights[k] = 0.0

    # Scale adjustment
    abs_sum = sum(abs(w) for w in weights.values())
    if abs_sum > 1:
        scale = 1.0 / abs_sum
        for k in weights:
            weights[k] *= scale

    return weights


# [FIXED] def strategy(context: DataContext, config_dict: dict) -> dict
def strategy(context: DataContext, config_dict: dict) -> dict:

    # [FIXED] assets, frequency
    assets = config_dict['assets']
    frequency = config_dict.get("frequency", "1m")

    # [CUSTOM] Strategy-specific parameters
    base_config = config_dict['config']['base']
    position_config = config_dict['config']['position']
    sltp_config = config_dict['config']['sltp']

    window = base_config.get("window", 180)

    # lookback_hours: Hours to use for momentum calculation (in hours)
    # Example: [1, 3, 6] -> Compare prices from 1 hour ago, 3 hours ago, 6 hours ago
    lookback_hours = base_config.get("lookback_hours", [1, 3, 6])

    # Spot: long only, no short_ratio
    long_ratio = position_config.get("long_ratio", 0.8)
    stop_loss_pct = sltp_config.get("stop_loss_pct", 0.02)
    take_profit_pct = sltp_config.get("take_profit_pct", 0.04)

    # Convert frequency to minutes and convert lookback_hours to number of bars
    bar_minutes = parse_frequency_to_minutes(frequency)
    # Hours -> Minutes -> Number of bars
    # Example: lookback_hours=[1,3,6], bar_minutes=15 -> periods=[4, 12, 24] bars
    periods = [int(h * 60 / bar_minutes) for h in lookback_hours]

    # [FIXED] context.get_history(assets=, window=, frequency=, fields=)
    # Returns: MultiIndex DataFrame (asset, datetime) with ohlcv columns
    hist = context.get_history(
        assets=assets,
        window=window,
        frequency=frequency,
        fields=["close"]
    )

    if hist.empty:
        return {}

    df = hist["close"].unstack(level=0)

    momentum = calculate_momentum(df, periods)
    weights = normalize_weights_long_only(momentum, long_ratio)

    latest_prices = df.iloc[-1]
    result = {}

    for symbol, weight in weights.items():
        price = latest_prices[symbol]

        if weight > 0:
            sl, tp = compute_sltp(price, weight, stop_loss_pct, take_profit_pct)
        else:
            sl, tp = None, None

        # [FIXED] Return format (SPOT): weight, presetTakeProfitPrice, presetStopLossPrice
        # weight: >= 0, long only, sum <= 1.0
        # sl/tp: can be None
        result[symbol] = {
            "weight": weight,
            "presetTakeProfitPrice": tp,
            "presetStopLossPrice": sl,
        }

    return result
