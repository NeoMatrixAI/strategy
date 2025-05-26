import pandas as pd

def strategy(df, config_dict):
    """
    Refer to https://www.marketvector.com/indexes/digital-assets/coinbase-50
    """

    # Get settings
    strategy_specific_config = config_dict.get('strategy_config')
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    long_candidates = ['BTCUSDT','ETHUSDT','XRPUSDT','']
    short_candidates = []

    return long_candidates, short_candidates
