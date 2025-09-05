# ==========================
# Required System Settings
# ==========================
system_config = {
    "data_apikey": "a71eaf04-802f-40be-93c2-5bee2548f4db", # Input your Data Api Key
    "tz_str": "Asia/Seoul", # Time zone (pytz.all_timezones)
    "tradeType": "futures",
    "strategy_name": "multi_period_momentum", # User strategy file name
    "trading_hours": 9, # Time to execute AutoTrade
    "timeframe": "1min",
    "orderType": "market",
    "total_allocation": 0.50, # Percentage to allocate from total assets
    "base_symbol": "BTCUSDT",
    "productType": "usdt-futures",
    "posMode": "hedge_mode", # 'hedge_mode', 'one_way_mode'
    "holdSide": "long", # 1. When 'marginMode' is 'crossed' --> 'holdSide' is not required.
                        # 2. When 'marginMode' is 'isolated' and 'posMode' is 'one_way_mode' --> 'holdSide' is not required.
                        # 3. When 'marginMode' is 'isolated' and 'posMode' is 'hedge_mode' --> 'holdSide' must be specified (long or short).
                          # 3-1. Exception: if both long and short leverages are set simultaneously in 'hedge mode', 'holdSide' is not required.
    "marginMode": "crossed", # 'crossed' or 'isolated'
    "marginCoin": "usdt",
    "leverage": 3, # Leverage
    "new_data_window": 4, # (hours) Window value to fetch recent data every minute (should be the maximum value of the strategy parameter value)
    "weight_method": "custom", # Weight method(equal, split, custom)  "equal" : Full equal split
                                                                    # "split" : After splitting long/short in half(spot:0.5 , futures:0.5), equal ratio 
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
    "rebalancing_interval_hours": 1/2, # Rebalancing cycle (hours)
}
