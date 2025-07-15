# 策略 (strategy)

此仓库包含用于 [nb-runner](https://github.com/NeoMatrixAI/nb-runner) 仓库的策略模块和配置文件。

---

### 📁 结构

每个策略都组织在独立的文件夹中，包含以下内容：
- `strategy_name.py`：策略核心逻辑
- `strategy_name_config.py`：该策略的配置文件

示例：

```
strategy/{future/spot}
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

我们还提供现货和期货策略模块的创建和设置指南，即使是初学者也可以轻松上手。

- 📘 更多信息，请参阅以下每种交易类型的指南。
  - [现货策略指南](./strategy/spot/README_CHN.md)
  - [期货策略指南](./strategy/future/README_CHN.md)

> 逐步讲解 `strategy()` 函数的编写方法、输入/输出格式、所需结构、设置方法以及示例代码。

---

### ❓ 支持

如有问题或需要支持，请通过 [**NeoMatrix Discord**](https://discord.gg/Xn26Q42DXD) 联系我们。
