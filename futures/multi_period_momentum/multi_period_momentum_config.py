# ==========================
# Strategy Parameter Settings
# ==========================

hours = [1,2,3]
strategy_config = {
    "assets": ["BTCUSDT", "ETHUSDT", "XRPUSDT"],
    "window": 180,
    "minutes": [int(i*60) for i in hours],
    "long_ratio": 0.7,
    "short_ratio": 0.3    
}
