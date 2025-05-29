# strategy

> 📚 This README is available in multiple languages:  
> - 🇺🇸 English (default) — this file  
> - 🇰🇷 [한국어](./README_KOR.md) 🇰🇷  
> - 🇨🇳 [中文](./README_CHN.md) 🇨🇳  
---
This repository contains strategy modules and configuration files used by the [nb-runner](https://github.com/NeoMatrixAI/nb-runner) repository.

---

### 📁 Structure

Each strategy is organized in its own folder and includes:
- `strategy_name.py`: The core logic of the strategy
- `strategy_name_config.py`: The configuration file for that strategy

Example:

```
strategy/
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

We also provide a beginner-friendly guide on how to create your own strategy module and configuration.

> 📘 See: [strategy_guide.md](./strategy/README.md) – A step-by-step tutorial on writing a custom `strategy()` function,  
> including input/output formats, required structure, configuration tips, and example code.

---

### ❓ Support

For questions or support, please reach out via the [**NeoMatrix Discord**](https://discord.gg/n6tMdrse)
