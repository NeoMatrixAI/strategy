# ==========================
# Required System Settings
# ==========================

system_config = {
    "data_apikey": "a71eaf04-802f-40be-93c2-5bee2548f4db", # Input your Data API Key
    "tz_str": "Asia/Seoul", # Time zone (pytz.all_timezones)
    "tradeType": "spot",
    "strategy_name": "coinbase50index", # User strategy file name
    "trading_hours": 6, # Time to execute AutoTrade
    "timeframe": "1min",
    "orderType": "market",
    "total_allocation": 0.50, # Percentage to allocate from total assets
    "quoteCoin": "USDT",
    "new_data_window": 1, # (hours) Window value to fetch recent data every minute (should be the maximum value of the strategy parameter value)
    "batchMode": 'multiple', # Set batch mode : "single", "multiple"
    "sizeMode": 'ratio', # Set whether to define the size for each symbol as a ratio or as a count : "size", "ratio" 
    "symbols": ['BTCUSDT', 'ETHUSDT']    
}


# ==========================
# Rebalancing Trade Parameters
# ==========================

rebalancing_config = {
    "rebalancing_interval_hours": 1, # Rebalancing cycle (hours)
}