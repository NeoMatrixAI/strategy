# 策略 (strategy)

此仓库包含用于 [nb-runner](https://github.com/NeoMatrixAI/nb-runner) 仓库的策略模块和配置文件。

---

### 📁 结构

每个策略都组织在独立的文件夹中，包含以下内容：
- `{strategy_name}.py`：策略核心逻辑（文件名必须与文件夹名一致）
- `config.yaml`：该策略的配置文件

示例：

```
strategy/
├── common/                              # 可复用的工具模块（自定义模块）
│   ├── momentum_utils.py                # 示例：动量计算工具
│   └── sltp_utils.py                    # 示例：止损/止盈工具
├── futures/
│   └── multi_period_momentum/
│       ├── multi_period_momentum.py     # 策略逻辑
│       └── config.yaml                  # 配置（系统、策略、回测/实盘设置）
└── spot/
    └── your_strategy/
        ├── your_strategy.py
        └── config.yaml
```

本仓库包含我们开发并定期更新的策略及配置文件。
不包含可执行的笔记本或API模块。

但是，在 `nb-runner` 环境中，您可以自由使用自己的自定义策略和配置文件，
不限于本仓库提供的内容。

---

### 📦 自定义模块 (common/ 文件夹)

`common/` 文件夹用于存储**可复用的工具模块**，这些模块可以在多个策略之间共享。

**重要:** 在自定义策略中，导入路径必须使用 `from common.xxx import ...` 格式，因为服务器会将用户上传的模块映射到 `common/` 文件夹。

#### 可用模块

| 模块 | 描述 |
|------|------|
| `momentum_utils.py` | 动量计算和权重归一化工具 |
| `sltp_utils.py` | 止损/止盈价格计算工具 |

#### 导入示例

```python
# [FIXED] 导入路径：始终使用 'from common.xxx'
from common.momentum_utils import calculate_momentum, normalize_weights
from common.sltp_utils import compute_sltp
```

#### 创建您自己的模块

1. 在 `common/` 文件夹中创建一个新的 `.py` 文件
2. 定义可复用的函数或类
3. 在策略中使用 `from common.your_module import your_function` 导入

**示例: custom_indicators.py**
```python
# common/custom_indicators.py
import pandas as pd

def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """计算相对强弱指数 (RSI)"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
```

**在策略中使用:**
```python
from common.custom_indicators import calculate_rsi

def strategy(context: DataContext, config_dict: dict) -> dict:
    # ... 获取历史数据 ...
    rsi = calculate_rsi(close_prices, period=14)
    # ... 策略逻辑 ...
```

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
  - [现货策略指南](../spot/README.md)
  - [期货策略指南](../futures/README.md)

> 逐步讲解 `strategy()` 函数的编写方法、输入/输出格式、所需结构、设置方法以及示例代码。

---

### 🤖 使用AI生成策略（推荐）

您可以使用Claude、GPT、Gemini等AI助手轻松创建策略。

**使用方法：**
1. 复制[期货策略指南](../futures/README.md)的全部内容
2. 粘贴到您的AI助手（Claude、GPT、Gemini等）
3. 用自然语言描述您的策略想法
4. AI将生成兼容的 `{strategy_name}.py` 和 `config.yaml` 文件

**提示示例：**
- "创建一个使用20日和50日移动平均线交叉的策略"
- "实现基于RSI的均值回归策略：RSI < 30时做多，RSI > 70时做空"
- "使用布林带构建波动率突破策略"

> AI提示指南包含生成生产级策略代码所需的所有模板、数据格式和示例。

---

### ❓ 支持

如有问题或需要支持，请通过 [**NeoMatrix Discord**](https://discord.gg/Xn26Q42DXD) 联系我们。
