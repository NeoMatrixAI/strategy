# Strategy Guide

> 📚 This README is available in multiple languages:  
> - 🇺🇸 English (default) — this file  
> - 🇰🇷 [한국어](./README_KOR.md) 🇰🇷  
> - 🇨🇳 [中文](./README_CHN.md) 🇨🇳
---

## 📘 How to Implement Your Own Strategy

This guide is designed for users who may not be familiar with coding. 
It provides a simple step-by-step explanation for building a custom strategy function. The example below is for reference, and users can develop their own logic by following the same structure.

---

## ✅ Required Structure (Fixed Rules)

- Function name must be `strategy`
- Function inputs: `df`, `config_dict`
- Function outputs: a dictionary where each key is a symbol (e.g., "BTCUSDT") and the value contains the trade information as follows:
```python
"symbol" : {
    "size": str(size),                     # Position size or ratio as a string
    "presetTakeProfitPrice": str(preset_take),   # Pre-set take profit price
    "executeTakeProfitPrice": str(execute_take), # Executed take profit price
    "presetStopLossPrice": str(preset_stop),     # Pre-set stop loss price
    "executeStopLossPrice": str(execute_stop)    # Executed stop loss price
}

```
- Configuration must be accessed like this:
```python
strategy_specific_config = config_dict.get('strategy_config')
```

Your strategy settings must be defined in a file (e.g., `strategy_config.py`) as follows:
```python
# strategy-config.py example
strategy_config = {
        "parameter_1": 10,
        "parameter_2": 30,
        "parameter_3": 0.5
        }
```

> ⚠️ The system will wrap this `strategy_config` into a `config_dict` and pass it to the strategy like this:

```python
result = strategy.strategy(df, {'strategy_config': config.strategy_config})
```

---

## 🧾 Structure of Input Data (`df`)

The `df` passed into the strategy function is a **time series price DataFrame**, with:

- **Index (rows)**: Timestamps (minute frequency)
- **Columns**: Asset symbols (e.g., BTCUSDT, ETHUSDT, etc.)
- **Values**: Closing prices at each timestamp (float)

Example layout:

| Time               | BTCUSDT | ETHUSDT | XRPUSDT | ... |
|--------------------|---------|---------|---------|-----|
| 2025-04-13 00:00:00| 84817.0 | 1655.26 | 2.1568  | ... |
| 2025-04-13 00:01:00| 84836.7 | 1655.39 | 2.1565  | ... |
| 2025-04-13 00:02:00| 84891.7 | 1656.20 | 2.1593  | ... |

> ✅ The strategy uses this DataFrame to select long and short candidates based on your logic.

---

## 🪄 Strategy Example: Simple SMA Strategy

```python
# strategy.py
import pandas as pd

import pandas as pd
import numpy as np

def strategy(df: pd.DataFrame, config_dict: dict) -> dict:
    """
    SMA strategy for test
    """

    # Get settings
    strategy_specific_config = config_dict.get('strategy_config')
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    sma_short_period = strategy_specific_config.get("sma_short")
    sma_long_period = strategy_specific_config.get("sma_long")
    take_profit_ratio = strategy_specific_config.get("take_profit_ratio")
    stop_loss_ratio = strategy_specific_config.get("stop_loss_ratio")

    result = {}
    symbols = df.columns
    df = df.copy()

    for symbol in symbols:
        close = df[symbol].astype(float)
        
        # Calculate SMA manually
        sma_short = close.rolling(window=sma_short_period).mean()
        sma_long = close.rolling(window=sma_long_period).mean()

        # Check for valid data
        if len(close) < max(sma_short_period, sma_long_period) + 1:
            continue
        if np.isnan(sma_short.iloc[-1]) or np.isnan(sma_long.iloc[-1]):
            continue

        prev_short = sma_short.iloc[-2]
        prev_long = sma_long.iloc[-2]
        curr_short = sma_short.iloc[-1]
        curr_long = sma_long.iloc[-1]
        price = close.iloc[-1]

        # Determine buy/sell signal
        signal = None
        if prev_short < prev_long and curr_short > curr_long:
            signal = 'buy'
        elif prev_short > prev_long and curr_short < curr_long:
            signal = 'sell'

        if signal:
            size = 1
            if signal == 'buy':
                entry_price = price
                preset_take = round(entry_price * (1 + take_profit_ratio), 4)
                execute_take = round(entry_price * (1 + take_profit_ratio * 0.9), 4)
                preset_stop = round(entry_price * (1 - stop_loss_ratio), 4)
                execute_stop = round(entry_price * (1 - stop_loss_ratio * 0.8), 4)
            else:  # sell
                entry_price = price
                preset_take = round(entry_price * (1 - take_profit_ratio), 4)
                execute_take = round(entry_price * (1 - take_profit_ratio * 0.9), 4)
                preset_stop = round(entry_price * (1 + stop_loss_ratio), 4)
                execute_stop = round(entry_price * (1 + stop_loss_ratio * 0.8), 4)

            result[symbol] = {
                "size": str(size),
                "presetTakeProfitPrice": str(preset_take),
                "executeTakeProfitPrice": str(execute_take),
                "presetStopLossPrice": str(preset_stop),
                "executeStopLossPrice": str(execute_stop)
            }

    return result
```

---

## 🧱 Strategy Verify Test Example

```python
# 1. strategy.py: Contains the strategy function above

# 2. strategy-config.py
strategy_config = {
        "sma_short": 30,
        "sma_long": 60,
        "take_profit_ratio": 0.02,
        "stop_loss_ratio": 0.01
    }

# 3. verify-strategy.ipynb
import strategy   # Your strategy file
import config     # Your config file

df = pd.read_csv('sample_data.csv')
results = strategy.strategy(df, {"strategy_config": config.strategy_config})
```

# ✅ Expected Output Format
```
{'BTCUSDT': {'size': '0.7',
  'presetTakeProfitPrice': None,
  'executeTakeProfitPrice': None,
  'presetStopLossPrice': None,
  'executeStopLossPrice': None},
 'ETHUSDT': {'size': '0.3',
  'presetTakeProfitPrice': None,
  'executeTakeProfitPrice': None,
  'presetStopLossPrice': None,
  'executeStopLossPrice': None}}
```

---

## ❓Tips

- The `df` is provided automatically by the system
- You must return results as **lists**
- For more complex strategies, you can build on the logic of this template


---

# 🛠 Sample config.py Template

Here’s a minimal example of what your `config.py` should look like:

```python
# config.py
# ==========================
# Required System Settings
# ==========================

system_config = {
    "data_apikey": "Input User Data Api Key", # CoinAPI - data api key
    "strategy_name": "multi_period_momentum", # User strategy file name
    "trading_hours": 72, # System run time
    "base_symbol": "BTCUSDT",
    "symbols": ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'BCHUSDT', 'LTCUSDT', 
                'ADAUSDT', 'ETCUSDT', 'TRXUSDT', 'DOTUSDT', 'DOGEUSDT', 
                'SOLUSDT', 'BNBUSDT', 'ICPUSDT', 'FILUSDT', 'XLMUSDT',
                'ONTUSDT', 'QTUMUSDT', 'NKNUSDT', 'AVAXUSDT', 'CELOUSDT',
                'WAXPUSDT', 'DYMUSDT', 'APTUSDT', 'FLOWUSDT', 'GTCUSDT',
                'SEIUSDT', 'ATOMUSDT', 'NEARUSDT', 'STXUSDT', 'MINAUSDT',
                'BSVUSDT', 'EGLDUSDT', 'RVNUSDT', 'ONEUSDT', 'NEOUSDT',
                'JUPUSDT', 'ZILUSDT', 'XTZUSDT', 'LUNCUSDT', 'CKBUSDT',
                'IOTAUSDT', 'THETAUSDT', 'ICXUSDT', 'ALGOUSDT', 'LSKUSDT', 
                'CFXUSDT', 'TONUSDT', 'MEMEUSDT', 'SXPUSDT', 'KASUSDT',
                'HBARUSDT', 'IOSTUSDT', 'BEAMUSDT', 'FETUSDT', 'XVGUSDT', 
                'SUIUSDT', 'VETUSDT', 'KSMUSDT', 'ARBUSDT', 'ARUSDT', 
                'RUNEUSDT', 'IOTXUSDT', 'TAIKOUSDT', 'COREUSDT', 'BBUSDT', 
                'COTIUSDT', 'NTRNUSDT'], # List of all currently available symbols: define only the symbols you need as values.
    "productType": "usdt-futures",
    "posMode": "hedge_mode", # one_way_mode , hedge_mode
    "marginMode": "crossed", # Margin mode: crossed (isolated requires holdSide in hedge_mode)
    "holdSide": "long",      # Position direction: long (used only in isolated + hedge_mode)   
    "marginCoin": "usdt",
    "orderType": "market",
    "timeframe": "1min",
    "tradeType": "future",
    "is_portfolio": True,   
    "total_allocation": 1.0, # Proportion of total assets to use
    "leverage": 10,          # Leverage
    "new_data_window": 60,   # The window value for fetching the latest data (preferably the maximum value of the strategy parameter)
    "weight_method": "custom", # equal(1/n), split(long: 0.5 --> 1/n | short: 0.5 --> 1/n), custom(custom_weights)
    "custom_weights": {        # Required if weight_method is custom
        "BTCUSDT" : "0.5",
        "ETHUSDT" : "0.3",
        "XRPUSDT" : "0.2"
    }    
}

# ==========================
# Rebalancing Trade Parameters
# ==========================

rebalancing_config = {
    "rebalancing_interval_hours": 3, # Rebalancing cycle (hours)
    "minimum_candidates": 0
}


# ==========================
# Strategy Parameter Settings
# ==========================

hours = 12
strategy_config = {
    "maximum_candidates": 5,
    "minutes": 60 * hours
}
```

✅ strategy_config is automatically passed to your strategy function by the system.
