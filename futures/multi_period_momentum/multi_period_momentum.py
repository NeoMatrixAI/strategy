from module.data_context import DataContext
import pandas as pd

def strategy(context: DataContext, config_dict: dict) -> dict:
    """
    Multi-period momentum strategy with configurable long/short ratio.
    """
    # Load strategy-specific configuration
    strategy_params = config_dict.get("strategy_config", {})
    assets = strategy_params.get("assets", [])
    window = strategy_params.get("window", 180)
    periods = strategy_params.get("minutes", [1, 3, 5])
    long_ratio = strategy_params.get("long_ratio", 0.7)   # default 70%
    short_ratio = strategy_params.get("short_ratio", 0.3) # default 30%

    # Fetch historical price data
    hist = context.get_history(
        assets=assets,
        window=window,
        frequency="1m",
        fields=["close"]
    )

    # Pivot to get DataFrame: index=datetime, columns=asset
    df = hist["close"].unstack(level=0)

    # Initialize momentum DataFrame
    momentum = pd.DataFrame(index=df.index, columns=df.columns, dtype=float)

    # Calculate momentum for each symbol
    for col in df.columns:
        for t in range(max(periods), len(df)):
            summation = 0
            for h in periods:
                raw_return = df[col].iloc[t] / df[col].iloc[t - h] - 1
                adjusted_return = (1 + raw_return) ** (1 / h) - 1
                summation += adjusted_return
            momentum.at[df.index[t], col] = summation / len(periods)

    # Extract momentum scores at the last timestamp
    momentum_scores = momentum.iloc[-1]

    # Separate long and short
    long_scores = {k: v for k, v in momentum_scores.items() if v > 0}
    short_scores = {k: v for k, v in momentum_scores.items() if v < 0}

    # Normalize weights according to long_ratio and short_ratio
    total_long = sum(long_scores.values())
    total_short = -sum(short_scores.values())  # convert to positive for scaling

    weights = {}
    for k, v in long_scores.items():
        weights[k] = (v / total_long) * long_ratio if total_long != 0 else 0
    for k, v in short_scores.items():
        weights[k] = (v / total_short) * short_ratio if total_short != 0 else 0

    return weights
