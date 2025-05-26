import pandas as pd

def strategy(df, config_dict):
    """
    Calculates momentum over multiple time periods (in minutes) for each stock in the given price data.
    Returns the top and bottom ranked stocks based on their averaged momentum scores at the latest time point.

    Parameters:
    - df (pd.DataFrame): Price time series data with datetime index and stock symbols as columns.
    - config_dict (dict): User-defined settings dictionary, expected to contain:
        - 'strategy_config': {
            'minutes': list of integers representing time periods for momentum calculation,
            'maximum_candidates': integer specifying how many top/bottom stocks to select
          }

    Returns:
    - long_candidates (list): List of stock symbols with the highest momentum scores (buy candidates).
    - short_candidates (list): List of stock symbols with the lowest momentum scores (sell candidates).
    """

    # Get settings
    strategy_specific_config = config_dict.get('strategy_config')
    
    periods = strategy_specific_config.get("minutes")
    maximum_candidates = strategy_specific_config.get("maximum_candidates")

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    momentum = pd.DataFrame(index=df.index, columns=df.columns, dtype=float)
    M = len(periods)

    # Calculate momentum
    for col in df.columns:
        for t in range(max(periods), len(df)):
            summation = 0
            for h in periods:
                raw_return = df[col].iloc[t] / df[col].iloc[t - h] - 1
                adjusted_return = (1 + raw_return) ** (1 / h) - 1
                summation += adjusted_return
            momentum[col].iloc[t] = summation / M

    # Sort momentum scores by last point in time
    momentum_scores = momentum.iloc[-1]
    ranked_df = momentum_scores.sort_values(ascending=False)

    # Extract top/bottom N
    long_candidates = list(ranked_df.head(maximum_candidates).index)
    short_candidates = list(ranked_df.tail(maximum_candidates).index)

    return long_candidates, short_candidates
