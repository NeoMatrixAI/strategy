# ==========================
# Required System Settings
# ==========================
system_config = {
    "tz_str": "Asia/Seoul", 
    "orderType": "market",
    "base_symbol": "BTCUSDT",
    "productType": "usdt-futures",
    "posMode": "hedge_mode",
    "holdSide": "long",                   
    "marginMode": "crossed",
    "marginCoin": "usdt",
    "leverage": 5,
    "trading_hours": 6,
    "total_allocation": 0.4, 
}


# ==========================
# Rebalancing Trade Parameters
# ==========================
rebalancing_config = {
    "rebalancing_interval_hours": 1, # Rebalancing cycle (hours)
}
