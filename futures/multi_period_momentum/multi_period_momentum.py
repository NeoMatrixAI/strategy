import pandas as pd

def strategy(df, config_dict):
    """
    A user strategy function that calculates momentum over multiple time periods (minutes) 
    and returns a ranking of the top and bottom stocks.

    Parameters:
    - df (pd.DataFrame): price time series data
    - config_dict (dict): User defined settings (parsed from JSON string)
      - Expected structure: 
        {
          'strategy_config': {
            'minutes': [...], 
            'long_minimum_candidates': ...,
            'long_maximum_candidates': ...,
            'short_minimum_candidates': ...,
            'short_maximum_candidates': ...
          }
        }

    Returns:
    - long_candidates (list): Top N Stocks (Buy Candidates)
    - short_candidates (list): Bottom N Stocks (Sell Candidates)
    """

    # Get settings
    strategy_specific_config = config_dict.get('strategy_config')
    
    ############################################################################
    # Users should define variables in this section to suit their strategy.
    # example
    # param_example_name = strategy_specific_config.get("param_example_name")
    periods = strategy_specific_config.get("minutes")
    long_minimum_candidates = strategy_specific_config.get("long_minimum_candidates", 1)
    long_maximum_candidates = strategy_specific_config.get("long_maximum_candidates", 1)
    short_minimum_candidates = strategy_specific_config.get("short_minimum_candidates", 1)
    short_maximum_candidates = strategy_specific_config.get("short_maximum_candidates", 1)
    ############################################################################

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

    # --- Long candidates ---
    long_candidates = ranked_df.head(long_maximum_candidates).index.tolist()

    # --- Short candidates (not overlapping with Long) ---
    short_candidates = ranked_df.tail(short_maximum_candidates).index.tolist()
    short_candidates = [s for s in short_candidates if s not in long_candidates]

    # --- Long minimum number guaranteed ---
    if len(long_candidates) < long_minimum_candidates:
        extra_needed = long_minimum_candidates - len(long_candidates)
        additional = [s for s in ranked_df.index if s not in long_candidates + short_candidates]
        long_candidates += additional[:extra_needed]

    # --- Short minimum number guaranteed ---
    if len(short_candidates) < short_minimum_candidates:
        extra_needed = short_minimum_candidates - len(short_candidates)
        additional = [s for s in ranked_df.index if s not in long_candidates + short_candidates]
        short_candidates += additional[-extra_needed:]

    return long_candidates, short_candidates
