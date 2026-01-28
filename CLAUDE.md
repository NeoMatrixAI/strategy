# CLAUDE.md

This document provides essential context for Claude Code to understand and work effectively with this trading strategy repository.

---

### 📁 Structure

```
strategy/
├── common/                              # Reusable utility modules (custom modules)
│   ├── momentum_utils.py                # Momentum calculation utilities
│   └── sltp_utils.py                    # Stop-loss/Take-profit utilities
├── futures/                             # Futures trading strategies
│   ├── README.md                        # Futures strategy guide & AI prompt
│   └── multi_period_momentum/           # Example futures strategy
│       ├── multi_period_momentum.py
│       └── config.yaml
├── spot/                                # Spot trading strategies
│   ├── README.md                        # Spot strategy guide
│   └── sma/                             # Example spot strategy
│       ├── sma.py
│       └── sma_config.py
└── docs/                                # Documentation translations
    ├── README.ko.md                     # Korean
    └── README.zh-CN.md                  # Chinese
```

---

### 📦 Technology Stack

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 1.5.3 | DataFrame processing for OHLCV data |
| numpy | 1.24.4 | Numerical operations |
| ta-lib | 0.4.30 | Technical indicators (SMA, RSI, MACD, etc.) |
| scipy | 1.10.1 | Statistical functions |

**Compatibility Notes:**
- Use `np.nan` instead of deprecated `np.NaN`
- Use `.iloc[]` for positional indexing
- Convert pandas Series to numpy arrays for ta-lib: `close_array = df["close"].values`

---

### 🔧 Two Strategy Architectures

#### Modern (Futures) - Recommended

```python
from module.data_context import DataContext
from common.momentum_utils import calculate_momentum
from common.sltp_utils import compute_sltp

def strategy(context: DataContext, config_dict: dict) -> dict:
    assets = config_dict['assets']
    frequency = config_dict.get("frequency", "1m")

    hist = context.get_history(assets=assets, window=200, frequency=frequency, fields=["close"])

    return {
        "BTCUSDT": {
            "weight": 0.4,                      # positive=long, negative=short
            "presetStopLossPrice": 98000.0,     # can be None
            "presetStopSurplusPrice": 105000.0  # can be None
        }
    }
```

#### Legacy (Spot)

```python
import pandas as pd
import numpy as np

def strategy(df: pd.DataFrame, config_dict: dict) -> dict:
    strategy_config = config_dict.get('strategy_config')

    return {
        "BTCUSDT": {
            "size": "0.7",
            "presetStopLossPrice": "85000",
            "presetTakeProfitPrice": "95000"
        }
    }
```

---

### 📦 Import Convention (CRITICAL)

**Always use `from common.xxx import ...` pattern:**

```python
# [FIXED] Import path: always use 'from common.xxx'
from common.momentum_utils import calculate_momentum, normalize_weights
from common.sltp_utils import compute_sltp
```

The server maps user-uploaded modules to the `common/` folder. This import path is fixed and must not be changed.

---

### ⚖️ Weight Rules (CRITICAL)

- Positive weight = Long position
- Negative weight = Short position
- **Sum of absolute values must NOT exceed 1.0:** `sum(|weight|) <= 1.0`

```python
# Weight normalization example
abs_sum = sum(abs(w) for w in weights.values())
if abs_sum > 1:
    scale = 1.0 / abs_sum
    for k in weights:
        weights[k] *= scale
```

---

### 📄 Configuration Format (config.yaml)

```yaml
version: "2.0"

system:
  trade_type: futures                    # futures | spot
  trade_env: backtest                    # backtest | live
  rebalancing_interval_hours: 8
  leverage: 5

strategy:
  name: multi_period_momentum            # Must match .py filename
  assets: [BTCUSDT, ETHUSDT]
  frequency: "15m"                       # 1m | 5m | 15m | 1d

  config:                                # Custom nested structure
    base:
      window: 200
      lookback_hours: [1, 3, 6]
    position:
      long_ratio: 0.6
      short_ratio: 0.4
    sltp:
      stop_loss_pct: 0.1
      take_profit_pct: 0.1

backtest:
  lookback_bars: 200                     # Must be >= max window/period used
  initial_capital: 10000
  start_date: "2025-10-01 09:00"
  end_date: "2025-10-10 08:59"
```

---

### 📊 Data Context API

```python
hist = context.get_history(
    assets=['BTCUSDT', 'ETHUSDT'],
    window=200,
    frequency="15m",
    fields=["close"]  # or ["open", "high", "low", "close", "volume"]
)
# Returns: MultiIndex DataFrame (asset, datetime)

# Convert to DataFrame with assets as columns
df = hist["close"].unstack(level=0)
latest_prices = df.iloc[-1]
```

---

### 📝 Naming Conventions

1. **Strategy folder and file must match:** `folder_name/folder_name.py`
2. **Config file:** `config.yaml` (YAML) or `{strategy_name}_config.py` (Python)
3. **Common modules:** Descriptive names (`momentum_utils.py`, `sltp_utils.py`)

---

### 🔍 Common Patterns

**Check for empty data:**
```python
if hist.empty:
    return {}
```

**Handle NaN values:**
```python
if np.isnan(indicator[-1]):
    weight = 0.0
```

**Use type hints:**
```python
def calculate_momentum(df: pd.DataFrame, periods: list) -> dict:
```

---

### 📘 Key Files Reference

| File | Purpose |
|------|---------|
| `futures/README.md` | AI prompt for generating futures strategies |
| `spot/README.md` | Spot strategy implementation guide |
| `common/momentum_utils.py` | Shared momentum calculation utilities |
| `common/sltp_utils.py` | Shared SL/TP calculation utilities |

---

### 🔄 Documentation Sync Rule (CRITICAL)

**When modifying `README.md`, you MUST also update the translated versions:**
- Korean: `docs/README.ko.md`
- Chinese: `docs/README.zh-CN.md`

All three documentation files must stay in sync.
