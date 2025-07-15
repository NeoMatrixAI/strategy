# Strategy

[![Discord](https://img.shields.io/badge/Discord-2319DC)](https://discord.com/invite/Xn26Q42DXD)[![NeoMatrix](https://img.shields.io/badge/Neomatrix.com-white)](https://discord.com/invite/Xn26Q42DXD)
---
[![English](https://img.shields.io/badge/docs-English-blue)](./README.md) [![한국어](https://img.shields.io/badge/docs-한국어-red)](./docs/README_ko.md)
[![简体中文](https://img.shields.io/badge/docs-简体中文-yellow)](./docs/README.zh-CN.md)
---
This repository contains strategy modules and configuration files used by the [nb-runner](https://github.com/NeoMatrixAI/nb-runner) repository.

---

### 📁 Structure

Each strategy is organized in its own folder and includes:
- `strategy_name.py`: The core logic of the strategy
- `strategy_name_config.py`: The configuration file for that strategy

Example:

```
strategy/{futures/spot}
└── momentum_v1/
    ├── momentum_v1.py
    └── momentum_v1_config.py
```

This repository contains the strategies and configuration files we have developed and regularly update.  
No executable notebooks or API modules are included here.

However, you are free to use your own custom strategies and configuration files in the `nb-runner` environment,  
not limited to the ones provided in this repository.

---

### 📦 How to Use

To use a strategy in this repository:
1. Clone or pull the latest version of this repository
2. Select the strategy you want to use
3. Load it into your local `nb-runner` environment
4. Use it via notebooks like `strategy_verify_test.ipynb`, `backtest.ipynb`, and `trade.ipynb`

Make sure you are also using the [nb-runner](https://github.com/NeoMatrixAI/nb-runner) repository, which contains the notebook runner and execution logic.

---

### 🧩 Want to Implement Your Own Strategy?

We also provide guides for creating spot and futures strategy modules and settings that even beginners can easily follow.

- 📘 For more information, please refer to the guides for each trading type below.
  - [Spot Strategy Guide](./spot/README.md)
  - [Futures Strategy Guide](./futures/README.md)

> The `strategy()` function writing method, input/output format, required structure, setup method, and example code are explained step by step.

---

### ❓ Support

For questions or support, please reach out via the [**NeoMatrix Discord**](https://discord.gg/Xn26Q42DXD)
