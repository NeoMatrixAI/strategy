import pandas as pd

def strategy(df, config_dict):
    """
    A user-defined strategy function that calculates momentum over multiple time periods
    and outputs portfolio weights for each symbol.

    Parameters:
    - df (pd.DataFrame): price time series data 
      (index: datetime, columns: symbols like BTCUSDT, ETHUSDT, ...)
    - config_dict (dict): user-defined settings (parsed from JSON string)
      {
        "strategy_config": {
          "minutes": [...],   # list of periods to calculate momentum
          ... other custom parameters ...
        }
      }

    Returns:
    - weights (dict): {symbol: weight}, where positive = long, negative = short
    """
    # Load strategy-specific configuration
    strategy_specific_config = config_dict.get("strategy_config", {})
    periods = strategy_specific_config.get("minutes", [1, 3, 5])

    # Validate input type
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

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

    # Convert scores to weights (no normalization, user-customized usage)
    weights = momentum_scores.to_dict()

    return weights
