# Strategy Guide
## 📘 How to Implement Your Own Strategy

This guide is designed for users who may not be familiar with coding. It provides a simple step-by-step explanation for building a custom strategy function. The example below is for reference, and users can develop their own logic by following the same structure.

---

## ✅ Required Structure (Fixed Rules)

- Function name must be `strategy`
- Function inputs: `df`, `config_dict`
- Function outputs: `long_candidates`, `short_candidates` (both must be lists)
- Configuration must be accessed like this:

```python
strategy_specific_config = config_dict.get('strategy_config')
```

Your strategy settings must be defined in a file (e.g., `config.py`) as follows:

```python
# config.py example
hours = 12  # Time intervals in hours

strategy_config = {
    "maximum_candidates": 5,  # Number of long/short selections
    "minutes": 60*hours  # Converted to minutes
}
```

> ⚠️ The system will wrap this `strategy_config` into a `config_dict` and pass it to the strategy like this:

```python
longs, shorts = strategy.strategy(df, {'strategy_config': config.strategy_config})
```

Users do **not** need to create `config_dict` manually—just call the strategy as shown.

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

## 🪄 Strategy Example: Simple Return-Based Strategy

```python
import pandas as pd

def strategy(df, config_dict):
    """
    A very simple strategy that compares the latest price
    to the price N minutes ago. It selects assets with the
    highest and lowest returns.
    """
    strategy_specific_config = config_dict.get('strategy_config')

    period = strategy_specific_config.get("minutes")[0]  # Use the first period only
    maximum_candidates = strategy_specific_config.get("maximum_candidates")

    returns = df.iloc[-1] / df.iloc[-period] - 1  # Calculate simple returns
    sorted_returns = returns.sort_values(ascending=False)

    long_candidates = list(sorted_returns.head(maximum_candidates).index)
    short_candidates = list(sorted_returns.tail(maximum_candidates).index)

    return long_candidates, short_candidates
```

---

## 🧱 Full Strategy Usage Structure (Including Config)

```python
# 1. config.py example
hours = 12  # Time intervals in hours

strategy_config = {
    "maximum_candidates": 5,  # Number of long/short selections
    "minutes": 60*hours  # Converted to minutes
}

# 2. strategy.py: Contains the strategy function above

# 3. How to run it (e.g., in main.py or Jupyter Notebook)
import strategy   # Your strategy file
import config     # Your config file

# df is the system-provided DataFrame of price data
df = get_price_data_somehow()
longs, shorts = strategy.strategy(df, {"strategy_config": config.strategy_config})

# Print result
print("📈 Long candidates:", longs)
print("📉 Short candidates:", shorts)
```

---

## ✅ Expected Output Format

```python
📈 Long candidates:
['BTCUSDT', 'ETHUSDT', 'XRPUSDT']

📉 Short candidates:
['SOLUSDT', 'AVAXUSDT', 'DOGEUSDT']
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

hours = 12

strategy_config = {
    "maximum_candidates": 5,   # Select top 5 assets
    "minutes": 60 * hours      # Look-back window: 12 hours
}

✅ strategy_config is automatically passed to your strategy function by the system.
