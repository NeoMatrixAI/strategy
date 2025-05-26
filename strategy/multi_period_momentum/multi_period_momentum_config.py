# ==========================
# Required System Settings
# ==========================

system_config = {
    "data_apikey": "Input your Data API key", # CoinAPI - data api key
    "strategy_name": "multi_period_momentum", # User strategy file name
    "trading_hours": 336, # System run time
    "base_symbol": "BTCUSDT",
    "symbols": ['BTCUSDT', 'ETHUSDT', 'XRPUSDT'], # List of symbols to use
    "productType": "usdt-futures",
    "posMode": "hedge_mode", # one_way_mode , hedge_mode
    "marginMode": "crossed", # isolated
    "holdSide": "long", # long , short
    "marginCoin": "usdt",
    "orderType": "market",
    "timeframe": "1min",
    "tradeType": "future", # demo / future
    "is_portfolio": True,   
    "total_allocation": 0.80, # Proportion of total assets to use
    "leverage": 10, # Leverage
    "weight": 1/3, # Proportion per symbol, must be sum 1
    "new_data_window": 360, # The window value for fetching the latest data 
                            # (preferably the maximum value of the strategy parameter)
}

# ==========================
# Rebalancing Trade Parameters
# ==========================

rebalancing_config = {
    "rebalancing_interval_hours": 72, # Rebalancing cycle (hours)
    "minimum_candidates": 1
}


# ==========================
# Strategy Parameter Settings
# ==========================

hours = [1,3,6]
strategy_config = {
    "maximum_candidates": 1, # The number of items set must not exceed more than half
    "minutes": [int(i*60) for i in hours]
}
