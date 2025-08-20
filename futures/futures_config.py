# ==========================
# Required System Settings
# ==========================
system_config = {
    "data_apikey": "a71eaf04-802f-40be-93c2-5bee2548f4db", # Input your Data Api Key
    "tz_str": "Asia/Seoul", # Time zone (pytz.all_timezones)
    "strategy_name": "multi_period_momentum", # User strategy file name
    "trading_hours": 1, # System run time
    "base_symbol": "BTCUSDT",
    "tradeType": "futures",
    "productType": "usdt-futures",
    "posMode": "hedge_mode", # 'hedge_mode', 'one_way_mode'
    "marginMode": "crossed", # 'crossed' or 'isolated'
    "marginCoin": "usdt",
    "orderType": "market",
    "timeframe": "1min",
    "total_allocation": 0.95, # Proportion of total assets to use
    "leverage": 3, # Leverage
    "new_data_window": 200, # Window value to fetch recent data every minute (should be the maximum value of the strategy parameter value)
    "weight_method": "custom", # Weight method(equal, split, custom)  "equal" : Full equal split
                                                                    # "split" : After splitting spot/futures in half(spot:0.5 , futures:0.5), equal ratio 
                                                                    # "custom" : User custom ratio
    "symbols": ['BTCUSDT', 'ETHUSDT', 'XRPUSDT'], # Trade list of symbols to use
    "custom_weights": { # Applies only when weight_mode is "custom"  
                        # Example
        'BTCUSDT': 0.5,
        'ETHUSDT': 0.3,
        'XRPUSDT': 0.2
    }
}

# ==========================
# Rebalancing Trade Parameters
# ==========================
rebalancing_config = {
    "rebalancing_interval_hours": 1/6, # Rebalancing cycle (hours)
}
