# ==========================
# Required System Settings
# ==========================
import os

system_config = {
    "data_apikey": "a71eaf04-802f-40be-93c2-5bee2548f4db",
    "strategy_name": "multi_period_momentum", # User strategy file name
    "trading_hours": 1, # System run time
    "base_symbol": "BTCUSDT",
    "symbols": ['BTCUSDT', 'ETHUSDT'], # List of symbols to use
    "productType": "usdt-futures",
    "posMode": "hedge_mode", # one_way_mode , hedge_mode
    "marginMode": "crossed", # isolated
    "holdSide": "long", # long , short
    "marginCoin": "usdt",
    "orderType": "market",
    "timeframe": "1min",
    "tradeType": "futures",
    "is_portfolio": True,   
    "total_allocation": 0.95, # Proportion of total assets to use
    "leverage": 3, # Leverage
    "new_data_window": 72, # The window value for fetching the latest data (preferably the maximum value of the strategy parameter)
    "weight_method": "custom", # 가중치 메소드 - equal, split(long/short), custom
    "custom_weights": { # 예시
        'BTCUSDT': 0.5,
        'ETHUSDT': 0.5
    }
}

# ==========================
# Rebalancing Trade Parameters
# ==========================

rebalancing_config = {
    "rebalancing_interval_hours": 1/12, # Rebalancing cycle (hours)
    "minimum_candidates": 0
}


# ==========================
# Strategy Parameter Settings
# ==========================

hours = [1,2,3]
strategy_config = {
    "long_maximum_candidates": 1,
    "short_maximum_candidates": 1,
    "minutes": [int(i*60) for i in hours]
}
