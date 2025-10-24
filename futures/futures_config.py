# ==========================
# Required System Settings
# ==========================
system_config = {
    "tz_str": "Asia/Seoul",
    "timeframe": "1min",
    "orderType": "market",
    "productType": "usdt-futures",
    "posMode": "hedge_mode",
    "marginMode": "crossed",
    "marginCoin": "usdt",
    "leverage": 5,
    "trading_hours": 12,
    "total_allocation": 0.5,
}


# ==========================
# Rebalancing Trade Parameters
# ==========================
rebalancing_config = {
    "rebalancing_interval_hours": 1, # Rebalancing cycle (hours)
}
