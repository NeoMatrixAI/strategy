# ==========================
# Required System Settings
# ==========================

system_config = {
    "data_apikey": "~~~~~~~~~~~~~~~~~~~~~~~~~~~~", # Input your Data API Key
    "strategy_name": "coinbase50index", # Strategy name
    "trading_hours": 336, # Time to execute auto-trading
    "quoteCoin": "USDT", # Quote coin
    "orderType": "market", # Set order type : "market" or "limit"
    "timeframe": "1min", # Set data frequency : "1min", "5min", "15min"
    "tradeType": "spot", # Set trading method : "spot" or "futures"
    "total_allocation": 0.90, # Percentage to allocate from total assets
    "new_data_window": 5, # For example, if timeframe is 1min, set how many data will be retrieved per minute to execute the strategy (you may need to adjust the maximum value depending on your strategy parameters).
    "batchMode": 'multiple', # Set batch mode : "single", "multiple"
    "sizeMode": 'ratio', # Set whether to define the size for each symbol as a ratio or as a count : "size", "ratio" 
}


# ==========================
# Rebalancing Trade Parameters
# Don't delete this item even if you don't rebalancing system.
# ==========================

rebalancing_config = {
    "rebalancing_interval_hours": 1/12, # Rebalancing cycle (hours)
}