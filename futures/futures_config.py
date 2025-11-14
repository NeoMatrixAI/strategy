# ==========================
# Required System Settings
# ==========================
system_config = {
    "data_apikey": "Inert your data apikey",
    "tz_str": "Asia/Seoul",
    "timeframe": "1min",
    "orderType": "market",
    "productType": "usdt-futures",
    "posMode": "hedge_mode",
    "marginMode": "crossed",
    "marginCoin": "usdt",
    "leverage": 3,
    "trading_hours": 12,
    "total_allocation": 0.9
}


# ==========================
# Rebalancing Trade Parameters
# ==========================
rebalancing_config = {
    "rebalancing_interval_hours": 1, # Rebalancing cycle (hours)
}
