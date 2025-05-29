# 策略 (strategy)

此仓库包含用于 [nb-runner](https://github.com/NeoMatrixAI/nb-runner) 仓库的策略模块和配置文件。

---

### 📁 结构

每个策略都组织在独立的文件夹中，包含以下内容：
- `strategy_name.py`：策略核心逻辑
- `strategy_name_config.py`：该策略的配置文件

示例：

```
strategy/
└── momentum_v1/
├── momentum_v1.py
└── momentum_v1_config.py
```


本仓库包含我们开发并定期更新的策略及配置文件。  
不包含可执行的笔记本或API模块。

但是，在 `nb-runner` 环境中，您可以自由使用自己的自定义策略和配置文件，  
不限于本仓库提供的内容。

---

### 📦 使用方法

使用本仓库策略步骤：
1. 克隆或拉取本仓库最新版本
2. 选择想使用的策略
3. 加载到本地 `nb-runner` 环境
4. 通过 `strategy_verify_test.ipynb`、`backtest.ipynb`、`trade.ipynb` 等笔记本使用

请确保同时使用包含执行逻辑的 [nb-runner](https://github.com/NeoMatrixAI/nb-runner) 仓库。

---

### 🧩 想自己实现策略？

我们也提供了适合初学者的策略模块和配置编写指南。

> 📘 详情请参见 [strategy_guide.md](./strategy/README.md) –  
> 分步教程，介绍如何编写自定义 `strategy()` 函数，  
> 包括输入/输出格式、必需结构、配置技巧及示例代码。

---

### ❓ 支持

如有问题或需要支持，请通过 [**NeoMatrix Discord**](https://discord.gg/n6tMdrse) 联系我们。
