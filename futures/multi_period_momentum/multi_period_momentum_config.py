# ==========================
# Strategy Parameter Settings
# ==========================

hours = [1,2,3]
strategy_config = {
    "long_maximum_candidates": 4,
    "long_minimum_candidates": 2,
    "short_maximum_candidates": 4,
    "short_minimum_candidates": 2,
    "minutes": [int(i*60) for i in hours]
}
