# strategy.py
import pandas as pd
import requests
import time
from datetime import datetime, timedelta

def fetch_latest_data(url, payload, lookback, wait_sec=5):
    """
    A function that repeatedly requests data until the latest candle appears.
    """
    while True:
        response = requests.get(url, params=payload)
        res = response.json()
        data = res.get("data", [])
        if not data:
            print("[Info] No data, please wait a moment and try again")
            time.sleep(wait_sec)
            continue

        df = pd.DataFrame(data)
        if len(df) < lookback + 1:
            print("[Info] Insufficient data, please wait a moment and try again")
            time.sleep(wait_sec)
            continue
        return df


def strategy(config_dict):
    # --- Input validation ---
    if not isinstance(config_dict, dict):
        raise TypeError("config_dict must be a dictionary.")

    # --- Load strategy-specific config ---
    strategy_specific_config = config_dict.get("strategy_config", {})
    long_allocation_pct = strategy_specific_config.get("long_allocation_pct", 0.7)
    short_allocation_pct = strategy_specific_config.get("short_allocation_pct", 0.3)
    lookback = strategy_specific_config.get("lookback", 10)
    data_apikey = "Input your Data Api Key"

    if long_allocation_pct + short_allocation_pct > 1.0:
        raise ValueError("Sum of long and short allocation percentages cannot exceed 1.0")

    # --- Symbol List ---
    symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]

    momentum_scores = {}

    # --- Calculate time range (based on UTC) ---
    now = datetime.utcnow()
    start_time = now - timedelta(minutes=lookback + 1)
    end_time = now

    start_str = start_time.strftime("%Y-%m-%d %H:%M")
    end_str = end_time.strftime("%Y-%m-%d %H:%M")

    # --- Get data by symbol ---
    root_url = 'https://crypto.fin.cloud.ainode.ai/'
    endpoint = f'{data_apikey}/get/candlestick/future/1min'
    url = root_url + endpoint
    
    for symbol in symbols:
        payload = {
            "exchange_nm": "bitget",
            "symbol": symbol,
            "startDate": start_str,
            "endDate": end_str
        }

        try:
            df = fetch_latest_data(url, payload, lookback, wait_sec=5)
            print(f"[OK] Get {symbol} data complete")

            # close Price standard
            series = df["close"].astype(float).dropna()
            momentum = series.iloc[-1] / series.iloc[-lookback] - 1
            momentum_scores[symbol] = momentum

        except Exception as e:
            print(f"[Error] Failed to get {symbol} data: {e}")
            continue

    if not momentum_scores:
        return {}

    # --- Long & Short classification ---
    longs = {s: m for s, m in momentum_scores.items() if m > 0}
    shorts = {s: abs(m) for s, m in momentum_scores.items() if m < 0}

    weights = {}

    # --- Long weight allocation ---
    if longs:
        long_total = sum(longs.values())
        for s, m in longs.items():
            weights[s] = (m / long_total) * long_allocation_pct

    # --- Short weight allocation ---
    if shorts:
        short_total = sum(shorts.values())
        for s, m in shorts.items():
            weights[s] = -(m / short_total) * short_allocation_pct

    # --- Final specific gravity ≤ 1.0 correction ---
    total_abs = sum(abs(w) for w in weights.values())
    if total_abs > 1.0:
        for s in weights:
            weights[s] = weights[s] / total_abs

    return weights
