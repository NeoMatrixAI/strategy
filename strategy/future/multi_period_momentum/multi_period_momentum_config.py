# ==========================
# Required System Settings
# ==========================
from dotenv import load_dotenv
import os

dotenv_path = os.path.abspath(os.path.join(__file__, "../../../../module/.env"))
load_dotenv(dotenv_path)
DATA_KEY = os.getenv("DATA_KEY")

system_config = {
    "data_apikey": DATA_KEY, # CoinAPI - data api key
    "strategy_name": "multi_period_momentum", # User strategy file name
    "trading_hours": 6, # System run time
    "base_symbol": "BTCUSDT",
    "symbols": ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'BCHUSDT', 'LTCUSDT', 'ADAUSDT', 'ETCUSDT', 'TRXUSDT', 'DOTUSDT', 'DOGEUSDT'], # List of symbols to use
    "productType": "usdt-futures",
    "posMode": "hedge_mode", # one_way_mode , hedge_mode
    "marginMode": "crossed", # isolated
    "holdSide": "long", # long , short
    "marginCoin": "usdt",
    "orderType": "market",
    "timeframe": "1min",
    "tradeType": "future",
    "is_portfolio": True,   
    "total_allocation": 0.95, # Proportion of total assets to use
    "leverage": 10, # Leverage
    "new_data_window": 72, # The window value for fetching the latest data (preferably the maximum value of the strategy parameter)
    "weight_method": "custom", # 가중치 메소드 - equal, split(long/short), custom
    "custom_weights": { # 예시
        'BTCUSDT': 0.5,
        'ETHUSDT': 0.2,
        'XRPUSDT': 0.1,
        'BCHUSDT': 0.04,
        'LTCUSDT': 0.04,
        'ADAUSDT': 0.03,
        'ETCUSDT': 0.03,
        'TRXUSDT': 0.03,
        'DOTUSDT': 0.02,
        'DOGEUSDT': 0.01
    }
}

# ==========================
# Rebalancing Trade Parameters
# ==========================

rebalancing_config = {
    "rebalancing_interval_hours": 3, # Rebalancing cycle (hours)
    "minimum_candidates": 0
}


# ==========================
# Strategy Parameter Settings
# ==========================

hours = [1,2,3]
strategy_config = {
    "long_maximum_candidates": 5,
    "short_maximum_candidates": 5,
    "minutes": [int(i*60) for i in hours]
}
