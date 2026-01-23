"""
Test Strategy

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

5. Return Format (FIXED)
   {
       "SYMBOL": {
           "weight": float,              # abs sum <= 1, positive=long, negative=short
           "presetStopLossPrice": float, # can be None
           "presetStopSurplusPrice": float # can be None
       }
   }
"""

# [FIXED] Import: from common.xxx (server uses user-specific common folder)
from module.data_context import DataContext
from common.momentum_utils import calculate_momentum, normalize_weights
from common.sltp_utils import compute_sltp

import pandas as pd


def parse_frequency_to_minutes(frequency: str) -> int:
    """
    frequency 문자열을 분 단위로 변환
    예: "1m" -> 1, "5m" -> 5, "15m" -> 15, "1h" -> 60, "1d" -> 1440
    """
    freq = frequency.lower().strip()
    if freq.endswith("m"):
        return int(freq[:-1])
    elif freq.endswith("h"):
        return int(freq[:-1]) * 60
    elif freq.endswith("d"):
        return int(freq[:-1]) * 1440
    else:
        return 1  # default 1분


# [FIXED] def strategy(context: DataContext, config_dict: dict) -> dict
def strategy(context: DataContext, config_dict: dict) -> dict:

    # [FIXED] assets, frequency
    assets = config_dict['assets']
    frequency = config_dict.get("frequency", "1m")

    # [CUSTOM] Strategy-specific parameters
    base_config = config_dict['base']
    position_config = config_dict['position']
    sltp_config = config_dict['sltp']

    window = base_config.get("window", 180)

    # lookback_hours: 모멘텀 계산에 사용할 시간 (시간 단위)
    # 예: [1, 3, 6] -> 1시간 전, 3시간 전, 6시간 전 가격과 비교
    lookback_hours = base_config.get("lookback_hours", [1, 3, 6])

    long_ratio = position_config.get("long_ratio", 0.7)
    short_ratio = position_config.get("short_ratio", 0.3)
    stop_loss_pct = sltp_config.get("stop_loss_pct", 0.02)
    take_profit_pct = sltp_config.get("take_profit_pct", 0.04)

    # frequency를 분 단위로 변환하여 lookback_hours를 bar 수로 변환
    bar_minutes = parse_frequency_to_minutes(frequency)
    # 시간 -> 분 -> bar 수
    # 예: lookback_hours=[1,3,6], bar_minutes=15 -> periods=[4, 12, 24] bars
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
    weights = normalize_weights(momentum, long_ratio, short_ratio)

    latest_prices = df.iloc[-1]
    result = {}

    for symbol, weight in weights.items():
        price = latest_prices[symbol]
        sl, tp = compute_sltp(price, weight, stop_loss_pct, take_profit_pct)

        # [FIXED] Return format: weight, presetStopLossPrice, presetStopSurplusPrice
        # weight: abs sum <= 1, positive=long, negative=short
        # sl/tp: can be None
        result[symbol] = {
            "weight": weight,
            "presetStopLossPrice": sl,
            "presetStopSurplusPrice": tp,
        }

    return result
