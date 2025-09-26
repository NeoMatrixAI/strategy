from module.data_context import DataContext
import pandas as pd

def strategy(context: DataContext, config_dict: dict) -> dict:
    """
    Momentum strategy with configurable long/short allocation.
    """
    # --- Load strategy-specific config ---
    strategy_params = config_dict.get("strategy_config", {})
    assets = strategy_params.get("assets", [])
    long_allocation_pct = strategy_params.get("long_allocation_pct", 0.7)
    short_allocation_pct = strategy_params.get("short_allocation_pct", 0.3)
    
    if long_allocation_pct + short_allocation_pct > 1.0:
        raise ValueError("Sum of long and short allocation percentages cannot exceed 1.0")

    window = strategy_params.get("window", 20)

    # --- Fetch historical data ---
    hist = context.get_history(
        assets=assets,
        window=window,
        frequency="1m",
        fields=["close"]
    )

    # Pivot to get DataFrame: index=datetime, columns=asset
    df = hist["close"].unstack(level=0)

    # --- Momentum calculation ---
    momentum_scores = {}
    for symbol in df.columns:
        series = df[symbol].dropna()
        if len(series) < window + 1:
            continue
        momentum = series.iloc[-1] / series.iloc[-window] - 1
        momentum_scores[symbol] = momentum

    if not momentum_scores:
        return {}

    # --- Split into long and short candidates ---
    longs = {s: m for s, m in momentum_scores.items() if m > 0}
    shorts = {s: abs(m) for s, m in momentum_scores.items() if m < 0}

    weights = {}

    # --- Allocate longs proportionally ---
    if longs:
        long_total = sum(longs.values())
        for s, m in longs.items():
            weights[s] = (m / long_total) * long_allocation_pct

    # --- Allocate shorts proportionally ---
    if shorts:
        short_total = sum(shorts.values())
        for s, m in shorts.items():
            weights[s] = -(m / short_total) * short_allocation_pct

    # --- Final check: ensure sum(|weights|) ≤ 1.0 ---
    total_abs = sum(abs(w) for w in weights.values())
    if total_abs > 1.0:
        for s in weights:
            weights[s] = weights[s] / total_abs

    return weights
