# Strategy

[![Discord](https://img.shields.io/badge/Discord-2319DC)](https://discord.com/invite/Xn26Q42DXD)[![NeoMatrix](https://img.shields.io/badge/Neomatrix-white)](https://discord.com/invite/Xn26Q42DXD)
---
[![English](https://img.shields.io/badge/docs-English-blue)](./README.md) [![한국어](https://img.shields.io/badge/docs-한국어-red)](./docs/README.ko.md)
[![简体中文](https://img.shields.io/badge/docs-简体中文-yellow)](./docs/README.zh-CN.md)
---
This repository contains strategy modules and configuration files used by the [nb-runner](https://github.com/NeoMatrixAI/nb-runner) repository.

---

### 📁 Structure

Each strategy is organized in its own folder and includes:
- `{strategy_name}.py`: The core logic of the strategy (filename must match folder name)
- `config.yaml`: The configuration file for that strategy

Example:

```
strategy/
├── common/                              # Reusable utility modules (custom modules)
│   ├── momentum_utils.py                # Example: momentum calculation utilities
│   └── sltp_utils.py                    # Example: stop-loss/take-profit utilities
├── futures/
│   └── multi_period_momentum/
│       ├── multi_period_momentum.py     # Strategy logic
│       └── config.yaml                  # Configuration (system, strategy, backtest/live settings)
└── spot/
    └── your_strategy/
        ├── your_strategy.py
        └── config.yaml
```

This repository contains the strategies and configuration files we have developed and regularly update.
No executable notebooks or API modules are included here.

However, you are free to use your own custom strategies and configuration files in the `nb-runner` environment,
not limited to the ones provided in this repository.

---

### 📦 Custom Modules (common/ folder)

The `common/` folder is used to store **reusable utility modules** that can be shared across multiple strategies.

**Important:** In custom strategies, import paths must use `from common.xxx import ...` format, as the server maps user-uploaded modules to the `common/` folder.

#### Available Modules

| Module | Description |
|--------|-------------|
| `momentum_utils.py` | Momentum calculation and weight normalization utilities |
| `sltp_utils.py` | Stop-loss and take-profit price calculation utilities |

#### Import Example

```python
# [FIXED] Import path: always use 'from common.xxx'
from common.momentum_utils import calculate_momentum, normalize_weights
from common.sltp_utils import compute_sltp
```

#### Creating Your Own Module

1. Create a new `.py` file in the `common/` folder
2. Define reusable functions or classes
3. Import in your strategy using `from common.your_module import your_function`

**Example: custom_indicators.py**
```python
# common/custom_indicators.py
import pandas as pd

def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
```

**Usage in strategy:**
```python
from common.custom_indicators import calculate_rsi

def strategy(context: DataContext, config_dict: dict) -> dict:
    # ... get historical data ...
    rsi = calculate_rsi(close_prices, period=14)
    # ... strategy logic ...
```

---

### 📦 How to Use

To use a strategy in this repository:
1. Clone or pull the latest version of this repository
2. Select the strategy you want to use
3. Load it into your local `nb-runner` environment
4. Use it via notebooks like `download_{futures/spot}_sample.ipynb`, `{futures/spot}_strategy_verify.ipynb`, `{futures/spot}_backtest.ipynb`, and `{futures/spot}_trade.ipynb`

Make sure you are also using the [nb-runner](https://github.com/NeoMatrixAI/nb-runner) repository, which contains the notebook runner and execution logic.

---

### 🧩 Want to Implement Your Own Strategy?

We also provide guides for creating spot and futures strategy modules and settings that even beginners can easily follow.

- 📘 For more information, please refer to the guides for each trading type below.
  - [Spot Strategy Guide](./spot/README.md)
  - [Futures Strategy Guide](./futures/README.md)

> The `strategy()` function writing method, input/output format, required structure, setup method, and example code are explained step by step.

---

### 🤖 Generate Strategy with AI (Recommended)

You can easily create strategies using AI assistants like Claude, GPT, or Gemini.

**How to use:**
1. Copy the entire contents of the strategy guide for your trading type:
   - [Futures Strategy Guide](./futures/README.md) - for futures trading (long/short, leverage)
   - [Spot Strategy Guide](./spot/README.md) - for spot trading (long only, no leverage)
2. Paste it into your AI assistant (Claude, GPT, Gemini, etc.)
3. Describe your strategy idea in natural language
4. The AI will generate compatible `{strategy_name}.py` and `config.yaml` files

**Example prompts:**
- "Create a simple moving average crossover strategy with 20 and 50 period SMAs"
- "Implement RSI-based mean reversion: go long when RSI < 30, short when RSI > 70"
- "Build a volatility breakout strategy using Bollinger Bands"

> The AI Prompt guide includes all required templates, data formats, and examples to generate production-ready strategy code.

---

### ❓ Support

For questions or support, please reach out via the [**NeoMatrix Discord**](https://discord.gg/Xn26Q42DXD)
