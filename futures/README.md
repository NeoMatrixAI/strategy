# Strategy Development Guide - AI Prompt

> This README is available in multiple languages:
> - English (default) - this file
> - [Korean](docs/Strategy.README.ko.md)
> - [Chinese](docs/Strategy.README.zh-CN.md)

---

> Copy this entire README and paste it to Claude, GPT, Gemini, or any AI assistant.
> Then describe your strategy idea, and the AI will generate compatible code for this system.

---

## AI Instructions

You are an expert trading system assistant.
Your task is to generate files that strictly follow the required structure below:

**Required files:**
1. **`{strategy_name}.py`** - The strategy logic file
2. **`config.yaml`** - The configuration file

**Optional files (generate when beneficial):**
3. **`common/{module_name}.py`** - Reusable utility modules

The user will provide strategy ideas, indicators, or trading logic, and you must implement them inside the fixed template.

### When to Create Common Modules

Create separate modules in the `common/` folder when:
- Logic can be **reused across multiple strategies** (indicators, signal generators, position sizing)
- Code improves **readability** by separating concerns (e.g., complex calculations)
- Functions are **self-contained utilities** (e.g., custom indicators, data transformers)

**Do NOT create common modules for:**
- Strategy-specific logic that won't be reused
- Simple one-liner calculations
- Configuration or constants (keep in config.yaml)

---

## System Architecture Overview

```
strategy/
├── common/                        # Shared modules (create as needed)
│   └── {module_name}.py           # e.g., indicators.py, signals.py, utils.py
└── futures/
    └── {strategy_name}/           # Strategy folder (name = strategy name)
        ├── {strategy_name}.py     # Strategy logic (filename must match folder name)
        └── config.yaml            # Configuration file
```

**Import path for common modules:**
```python
from common.{module_name} import your_function
# Example: from common.indicators import custom_rsi
```

---

## Required Package Versions (CRITICAL)

**You MUST write code compatible with these exact package versions.**
The system uses these versions for both backtesting and live trading.

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 1.5.3 | DataFrame processing |
| numpy | 1.24.4 | Numerical operations |
| ta-lib | 0.4.30 | Technical indicators (RSI, MACD, SMA, EMA, etc.) |
| scipy | 1.10.1 | Statistical/mathematical functions |

### TA-Lib Usage Examples

```python
import talib
import numpy as np

# Convert pandas Series to numpy array for TA-Lib
close_array = df["close"].values

# Simple Moving Average
sma_20 = talib.SMA(close_array, timeperiod=20)

# Exponential Moving Average
ema_12 = talib.EMA(close_array, timeperiod=12)

# RSI (Relative Strength Index)
rsi = talib.RSI(close_array, timeperiod=14)

# MACD
macd, macd_signal, macd_hist = talib.MACD(close_array, fastperiod=12, slowperiod=26, signalperiod=9)

# Bollinger Bands
upper, middle, lower = talib.BBANDS(close_array, timeperiod=20, nbdevup=2, nbdevdn=2)

# ATR (Average True Range) - requires high, low, close
atr = talib.ATR(high_array, low_array, close_array, timeperiod=14)

# Stochastic
slowk, slowd = talib.STOCH(high_array, low_array, close_array,
                           fastk_period=14, slowk_period=3, slowd_period=3)
```

### Important Compatibility Notes

1. **pandas 1.5.3**: Use `.iloc[]` for positional indexing, `.loc[]` for label-based indexing
2. **numpy 1.24.4**: `np.NaN` is deprecated, use `np.nan` instead
3. **ta-lib 0.4.30**: Input must be numpy arrays, not pandas Series (use `.values`)
4. **scipy 1.10.1**: Available for advanced statistical calculations

---

## Part 1: Strategy File (`{strategy_name}.py`)

### Fixed Rules (MUST Follow)

1. **Function name** must be `strategy`
2. **Function signature** must be exactly:
```python
def strategy(context: DataContext, config_dict: dict) -> dict:
```

3. **Required import**:
```python
from module.data_context import DataContext
```

4. **Optional imports** (from common folder - user uploaded modules):
```python
from common.your_module import your_function
```

### Data Request API

```python
# [FIXED] Get historical OHLCV data
hist = context.get_history(
    assets=assets,           # List of symbols, e.g., ["BTCUSDT", "ETHUSDT"]
    window=window,           # Lookback window (number of bars)
    frequency=frequency,     # "1m" | "5m" | "15m" | "1d"
    fields=["close"]         # Select from: ["open", "high", "low", "close", "volume"]
)
```

### Data Format (MultiIndex DataFrame)

The `hist` DataFrame has a MultiIndex with levels `["asset", "datetime"]`:

```
                                        open      high      low     close    volume
asset    datetime
BTCUSDT  2025-11-13 04:01:00+00:00    100.0    100.2     99.7    100.0    37215.0
         2025-11-13 04:02:00+00:00    100.0    100.5     99.8    100.3    42156.0
ETHUSDT  2025-11-13 04:01:00+00:00    105.1    105.1    104.7    105.0    74304.2
         2025-11-13 04:02:00+00:00    105.0    105.3    104.9    105.2    68421.5
```

**Common data manipulation patterns:**
```python
# Get single column as DataFrame (assets as columns, datetime as index)
df = hist["close"].unstack(level=0)

# Result:
#                            BTCUSDT   ETHUSDT
# datetime
# 2025-11-13 04:01:00+00:00   100.0    105.0
# 2025-11-13 04:02:00+00:00   100.3    105.2

# Get latest prices
latest_prices = df.iloc[-1]
```

### Return Format (MUST Follow)

```python
{
    "SYMBOL": {
        "weight": float,                  # Position weight (see rules below)
        "presetStopLossPrice": float,     # Stop loss price (can be None)
        "presetStopSurplusPrice": float   # Take profit price (can be None)
    }
}
```

**Weight Rules:**
- **Positive value** = Long position
- **Negative value** = Short position
- **Sum of absolute values must NOT exceed 1.0**: `sum(|weight|) <= 1.0`
- Each weight represents the proportion of margin capital allocated to that symbol

**Example return:**
```python
return {
    "BTCUSDT": {"weight": 0.4, "presetStopLossPrice": 98000.0, "presetStopSurplusPrice": 105000.0},
    "ETHUSDT": {"weight": -0.3, "presetStopLossPrice": 4200.0, "presetStopSurplusPrice": 3800.0},
    "XRPUSDT": {"weight": 0.2, "presetStopLossPrice": None, "presetStopSurplusPrice": None}
}
```

### Strategy File Template

```python
"""
{Strategy Name}

=== FIXED VALUES (DO NOT CHANGE) ===

1. Import Path
   - from common.xxx import ... (FIXED)
   - Server uses user-specific common folder for uploaded module files

2. Function Signature
   - def strategy(context: DataContext, config_dict: dict) -> dict (FIXED)

3. Config Access
   - assets = config_dict['assets'] (FIXED)
   - frequency = config_dict.get("frequency", "1m") (FIXED)
   - Other config_dict parameters are custom per strategy

4. History API
   - context.get_history(assets=, window=, frequency=, fields=) (FIXED)
   - fields: list of required columns from ohlcv (e.g., ["close"], ["open", "high", "low", "close"])
   - Returns: MultiIndex DataFrame (asset, datetime)

5. Return Format (FIXED)
   {
       "SYMBOL": {
           "weight": float,              # abs sum <= 1, positive=long, negative=short
           "presetStopLossPrice": float, # can be None
           "presetStopSurplusPrice": float # can be None
       }
   }
"""

# [FIXED] Import: from module.data_context
from module.data_context import DataContext

# [OPTIONAL] Import custom modules from common folder
# from common.your_module import your_function

import pandas as pd
import numpy as np


# [FIXED] def strategy(context: DataContext, config_dict: dict) -> dict
def strategy(context: DataContext, config_dict: dict) -> dict:

    # [FIXED] assets, frequency from config_dict
    assets = config_dict['assets']
    frequency = config_dict.get("frequency", "1m")

    # [CUSTOM] Strategy-specific parameters from config
    # Access nested config like: config_dict['config']['your_section']['param']
    # Example:
    # base_config = config_dict['config']['base']
    # window = base_config.get("window", 180)

    # [FIXED] context.get_history(assets=, window=, frequency=, fields=)
    # Returns: MultiIndex DataFrame (asset, datetime) with OHLCV columns
    hist = context.get_history(
        assets=assets,
        window=100,  # Adjust based on your strategy needs
        frequency=frequency,
        fields=["close"]  # Select only the fields you need
    )

    if hist.empty:
        return {}

    # === YOUR STRATEGY LOGIC HERE ===

    # Example: Convert to DataFrame with assets as columns
    df = hist["close"].unstack(level=0)
    latest_prices = df.iloc[-1]

    # Calculate your signals and weights...
    weights = {}  # Your logic to calculate weights

    # Build result
    result = {}
    for symbol in assets:
        weight = weights.get(symbol, 0.0)
        price = latest_prices[symbol]

        # Calculate stop loss and take profit (optional)
        sl = None  # Your stop loss logic
        tp = None  # Your take profit logic

        # [FIXED] Return format
        result[symbol] = {
            "weight": weight,
            "presetStopLossPrice": sl,
            "presetStopSurplusPrice": tp,
        }

    return result
```

---

## Part 2: Configuration File (`config.yaml`)

### Configuration Structure

```yaml
version: "2.0"

# =============================================================================
# SYSTEM - Common Settings
# =============================================================================
system:
  trade_type: futures                    # [Required] futures | spot
  trade_env: backtest                    # [Required] backtest | live
  rebalancing_interval_hours: 8          # [Required] Rebalancing interval (hours). Fraction allowed: "5/60" = 5min
  leverage: 5                            # Leverage (default: 5)
  tz_str: "Asia/Seoul"                   # Timezone (default: UTC)

# =============================================================================
# STRATEGY - Strategy Settings
# =============================================================================
strategy:
  name: your_strategy_name               # [Required] Strategy name (must match filename)
  assets:                                # [Required] Trading assets (must end with USDT)
    - BTCUSDT
    - ETHUSDT
    - XRPUSDT
  frequency: "15m"                       # [Required] Data frequency: 1m | 5m | 15m | 1d

  # [OPTIONAL] Custom parameters - structure is completely flexible
  # You can define any nested structure that fits your strategy needs.
  # Examples:
  #   config:
  #     window: 180
  #     rsi_period: 14
  #   OR
  #   params:
  #     indicators: {sma: 20, ema: 50}
  #     thresholds: {buy: 30, sell: 70}

# =============================================================================
# BACKTEST - Backtest Only (Required when trade_env: backtest)
# =============================================================================
backtest:
  data_apikey: "YOUR_DATA_API_KEY"       # [Required] Data API key
  start_date: "2025-10-01 09:00"         # [Required] Start datetime
  end_date: "2025-10-10 08:59"           # [Required] End datetime
  lookback_bars: 220                     # [Required] SEE BELOW: must be >= max window/period used in strategy
  initial_capital: 10000                 # [Required] Initial capital (USD)
  generate_report: true                  # Generate Pyfolio report (default: true)

# =============================================================================
# LIVE - Live Trading Only (Required when trade_env: live)
# =============================================================================
# live:
#   trading_hours: 720                   # Operating hours. 720 = 30 days
#   data_apikey: "YOUR_API_KEY"
#
#   futures:                             # When trade_type: futures
#     total_allocation: 0.8              # Capital allocation ratio (0~1)
#     margin_mode: crossed               # crossed
#     pos_mode: hedge_mode               # hedge_mode
#
#   spot:                                # When trade_type: spot
#     quote_coin: usdt
#     total_allocation: 0.8
```

### How Config is Passed to Strategy

The `config_dict` parameter in the strategy function receives all keys under `strategy:` section:
```python
config_dict = {
    "name": "your_strategy_name",             # [Required] From strategy.name
    "assets": ["BTCUSDT", "ETHUSDT", ...],    # [Required] From strategy.assets
    "frequency": "15m",                        # [Required] From strategy.frequency
    # ... any other custom keys you define under strategy: section
}
```

**Important:** The structure under `strategy:` is flexible. Only `name`, `assets`, and `frequency` are required.
Any additional keys you define will be passed directly to `config_dict`.

**DO NOT copy the example structure (base/position/sltp).** Design your own parameter structure based on your strategy's needs. Examples:
```yaml
# Simple flat structure
strategy:
  name: my_strategy
  assets: [BTCUSDT, ETHUSDT]
  frequency: "15m"
  window: 200
  rsi_period: 14
  threshold: 30

# Or nested structure
strategy:
  name: my_strategy
  assets: [BTCUSDT]
  frequency: "15m"
  indicators:
    sma_short: 20
    sma_long: 50
  rules:
    buy_threshold: 0.02
    sell_threshold: -0.02
```

---

### CRITICAL: lookback_bars Calculation

**Rule:** `lookback_bars` must be greater than or equal to the maximum historical data required by your strategy.

```
lookback_bars >= max(all window/period values used in strategy) + buffer (10~20%)
```

**When is historical data needed?**

| Case | Example | Required lookback_bars |
|------|---------|----------------------|
| `get_history(window=N)` call | `get_history(assets, window=200, ...)` | >= 200 |
| Moving Average | `talib.SMA(close, 50)` | >= 50 |
| RSI calculation | `talib.RSI(close, 14)` | >= 14 |
| Combined usage | `get_history(200)` then `SMA(50)` | >= 200 |

**Calculation Example:**

If your strategy uses:
- `get_history(window=200)`
- `talib.SMA(close, 20)` (short SMA)
- `talib.SMA(close, 50)` (long SMA)
- `talib.RSI(close, 14)`

Then:
```
max(200, 20, 50, 14) = 200
lookback_bars = 200 + buffer = 220 (recommended)
```

**Error when lookback_bars is too small:**
```
History window extends before YYYY-MM-DD. To use this history window,
start the backtest on or after YYYY-MM-DD.
```
**Solution:** Increase `lookback_bars` to be >= the window requested in your strategy.

---

## Complete Example: RSI Mean Reversion Strategy

**Note:** This is just ONE example. Design your own parameter names and structure based on YOUR strategy logic.

### File: `rsi_mean_reversion.py`

```python
"""
RSI Mean Reversion Strategy
- Long when RSI < oversold threshold
- Short when RSI > overbought threshold
"""

from module.data_context import DataContext
import talib
import numpy as np


def strategy(context: DataContext, config_dict: dict) -> dict:

    # [FIXED] Required parameters
    assets = config_dict['assets']
    frequency = config_dict.get("frequency", "1m")

    # [CUSTOM] Your own parameter names - design based on YOUR strategy
    window = config_dict.get("window", 100)
    rsi_period = config_dict.get("rsi_period", 14)
    oversold = config_dict.get("oversold", 30)
    overbought = config_dict.get("overbought", 70)
    stop_loss_pct = config_dict.get("stop_loss_pct", 0.02)
    take_profit_pct = config_dict.get("take_profit_pct", 0.04)

    # [FIXED] Get historical data
    hist = context.get_history(
        assets=assets,
        window=window,
        frequency=frequency,
        fields=["close"]
    )

    if hist.empty:
        return {}

    df = hist["close"].unstack(level=0)
    latest_prices = df.iloc[-1]

    result = {}
    num_assets = len(assets)
    max_weight_per_asset = 1.0 / num_assets  # Equal distribution

    for symbol in assets:
        close_array = df[symbol].values
        rsi = talib.RSI(close_array, timeperiod=rsi_period)
        current_rsi = rsi[-1]
        price = latest_prices[symbol]

        if np.isnan(current_rsi):
            weight = 0.0
            sl, tp = None, None
        elif current_rsi < oversold:
            weight = max_weight_per_asset  # Long
            sl = price * (1 - stop_loss_pct)
            tp = price * (1 + take_profit_pct)
        elif current_rsi > overbought:
            weight = -max_weight_per_asset  # Short
            sl = price * (1 + stop_loss_pct)
            tp = price * (1 - take_profit_pct)
        else:
            weight = 0.0
            sl, tp = None, None

        result[symbol] = {
            "weight": weight,
            "presetStopLossPrice": sl,
            "presetStopSurplusPrice": tp,
        }

    return result
```

### File: `config.yaml`

```yaml
version: "2.0"

system:
  trade_type: futures
  trade_env: backtest
  rebalancing_interval_hours: 4
  leverage: 5
  tz_str: "Asia/Seoul"

strategy:
  name: rsi_mean_reversion
  assets:
    - BTCUSDT
    - ETHUSDT
    - XRPUSDT
  frequency: "15m"

  # Custom parameters - YOUR OWN NAMING, not a fixed structure
  window: 100
  rsi_period: 14
  oversold: 30
  overbought: 70
  stop_loss_pct: 0.02
  take_profit_pct: 0.04

backtest:
  data_apikey: "YOUR_DATA_API_KEY"
  start_date: "2025-10-01 09:00"
  end_date: "2025-10-15 08:59"
  lookback_bars: 120                     # >= window (100) + buffer
  initial_capital: 10000
  generate_report: true
```

---

## Output Format Requirements

When generating code, provide output in this exact format:

### File: `{strategy_name}.py`

```python
# Full content of the strategy file
```

### File: `config.yaml`

```yaml
# Full content of the configuration file
```

### [OPTIONAL] File: `common/{module_name}.py`

Generate common modules when reusable utilities would benefit the strategy.

```python
# Full content of the common module
# Example: common/indicators.py, common/signals.py, common/utils.py
```

**Common Module Guidelines:**
- Each module should have a **single responsibility** (indicators, signals, position sizing, etc.)
- Include **docstrings** for each function explaining inputs/outputs
- Use **type hints** for better code clarity
- Module must be **self-contained** (no dependencies on strategy-specific code)

**Example common module structure:**
```python
"""
Custom Indicators Module
Reusable technical indicator functions for trading strategies.
"""

import numpy as np
import talib


def weighted_rsi(close: np.ndarray, period: int = 14, weight: float = 1.0) -> np.ndarray:
    """
    Calculate weighted RSI.

    Args:
        close: Array of closing prices
        period: RSI period
        weight: Weight multiplier

    Returns:
        Weighted RSI values
    """
    rsi = talib.RSI(close, timeperiod=period)
    return rsi * weight
```

---

## Your Strategy Idea

**Describe your strategy below:**

(Example prompts you can use:)
- "Create a simple moving average crossover strategy with 20 and 50 period SMAs"
- "Implement RSI-based mean reversion: go long when RSI < 30, short when RSI > 70"
- "Build a volatility breakout strategy using Bollinger Bands"
- "Create a dual momentum strategy combining absolute and relative momentum"

---

Now generate the complete Python code and YAML configuration for my strategy.
