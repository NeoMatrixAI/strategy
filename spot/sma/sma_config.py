# ==========================
# Required System Settings
# ==========================

system_config = {
    "data_apikey": "Input your Data API key", # CoinAPI - data api key
    "strategy_name": "sma",
    "trading_hours": 336,
    "quoteCoin": "USDT",
    "symbols": ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'SOLUSDT', 'DOGEUSDT', 'ADAUSDT', 'BCHUSDT', 'XLMUSDT', 'AVAXUSDT', 'LTCUSDT', 'DOTUSDT', 'APTUSDT', 'ICPUSDT', 'NEARUSDT', 'ETCUSDT', 'FETUSDT', 'ATOMUSDT', 'ALGOUSDT', 'STXUSDT', 'XTZUSDT'],
    "orderType": "market",
    "timeframe": "1min",
    "tradeType": "spot",
    "is_portfolio": True,
    "total_allocation": 0.90,
    "new_data_window": 5,
    "batchMode": 'multiple',
    "sizeMode": 'size', # ratio / size
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
