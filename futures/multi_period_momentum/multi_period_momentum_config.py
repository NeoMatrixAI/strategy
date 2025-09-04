# ==========================
# Strategy Parameter Settings
# ==========================

hours = [1,2,3]
strategy_config = {
    "long_maximum_candidates": 2,
    "long_minimum_candidates": 0,
    "short_maximum_candidates": 1,
    "short_minimum_candidates": 0,
    "minutes": [int(i*60) for i in hours]
}
