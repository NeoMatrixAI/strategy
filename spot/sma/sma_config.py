# ==========================
# Required System Settings
# ==========================

system_config = {
    "data_apikey": "Input your Data API key", # Input your Data API Key
    "strategy_name": "sma", # Strategy name
    "trading_hours": 336, # Time to execute auto-trading
    "quoteCoin": "USDT", # Quote coin
    "symbols": ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'SOLUSDT', 'DOGEUSDT', 'ADAUSDT', 'BCHUSDT', 'XLMUSDT', 'AVAXUSDT', 'LTCUSDT', 'DOTUSDT', 'APTUSDT', 'ICPUSDT', 'NEARUSDT', 'ETCUSDT', 'FETUSDT', 'ATOMUSDT', 'ALGOUSDT', 'STXUSDT', 'XTZUSDT'], # Symbol to trade
    "orderType": "market", # Set order type : "market" or "limit"
    "timeframe": "1min", # Set data frequency : "1min", "5min", "15min"
    "tradeType": "spot", # Set trading method : "spot" or "futures"
    "total_allocation": 0.90, # Percentage to allocate from total assets
    "new_data_window": 5, # For example, if timeframe is 1min, set how many data will be retrieved per minute to execute the strategy (you may need to adjust the maximum value depending on your strategy parameters).
    "batchMode": 'multiple', # Set batch mode : "single", "multiple"
    "sizeMode": 'size', # Set whether to define the size for each symbol as a ratio or as a count : "size", "ratio" 
}

# ==========================
# Strategy Parameter Settings
# ==========================

strategy_config = {
        "sma_short": 5,
        "sma_long": 20,
        "take_profit_ratio": 0.01,
        "stop_loss_ratio": 0.005
    }
