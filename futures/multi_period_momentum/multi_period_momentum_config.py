# ==========================
# Strategy Parameter Settings
# ==========================

hours = [1,2,3]  # momentum periods in hours
strategy_config = {
    "strategy_config": {
        "window": 180,
        "minutes": [int(i*60) for i in hours]
    },
    "position_config": {
        "long_ratio": 0.5,
        "short_ratio": 0.5
    },
    "sltp_config": {
        "stop_loss_pct": 0.05,
        "take_profit_pct": 0.05
    },
    "assets": ["BTCUSDT", "ETHUSDT", "XRPUSDT", "BCHUSDT", "LTCUSDT", "ADAUSDT"]
}