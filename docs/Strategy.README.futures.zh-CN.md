# 期货策略开发指南 - AI 提示

> **Trade Type: Futures**
>
> 本 README 提供多种语言版本：
> - [English](../futures/README.md)
> - [Korean](Strategy.README.futures.ko.md)
> - Chinese (简体中文) - 当前文件

---

> 将本 README 的全部内容复制并粘贴到 Claude、GPT、Gemini 或任何 AI 助手中。
> 然后描述您的策略想法，AI 将生成与本系统兼容的代码。

---

## AI 指令

您是一位专业的交易系统助手。
您的任务是生成严格遵循以下结构要求的文件：

**必需文件：**
1. **`{strategy_name}.py`** - 策略逻辑文件
2. **`config.yaml`** - 配置文件

**可选文件（在有益时生成）：**
3. **`common/{module_name}.py`** - 可复用的工具模块

用户将提供策略想法、指标或交易逻辑，您必须在固定模板中实现它们。

### 何时创建通用模块

在以下情况下，在 `common/` 文件夹中创建独立模块：
- 逻辑可以**在多个策略之间复用**（指标、信号生成器、仓位管理）
- 通过分离关注点来提高代码**可读性**（例如：复杂计算）
- 函数是**独立的工具函数**（例如：自定义指标、数据转换器）

**不要为以下情况创建通用模块：**
- 不会被复用的策略专属逻辑
- 简单的单行计算
- 配置或常量（保留在 config.yaml 中）

---

## 期货交易规则 (重要)

**本系统用于期货交易。必须遵守以下约束条件：**

1. **做多和做空** - 期货交易支持做多（正权重）和做空（负权重）仓位。
2. **杠杆** - 期货交易使用杠杆，在 `system.leverage` 中配置。
3. **权重规则** - 绝对值之和不得超过 1.0：`sum(|weight|) <= 1.0`。
4. **止盈字段** - 使用 `presetStopSurplusPrice`（不是现货使用的 `presetTakeProfitPrice`）。

---

## 系统架构概览

```
strategy/
├── common/                        # 共享模块（按需创建）
│   └── {module_name}.py           # 例如：indicators.py, signals.py, utils.py
└── futures/
    └── {strategy_name}/           # 策略文件夹（名称 = 策略名称）
        ├── {strategy_name}.py     # 策略逻辑（文件名必须与文件夹名一致）
        └── config.yaml            # 配置文件
```

**通用模块的导入路径：**
```python
from common.{module_name} import your_function
# 示例: from common.indicators import custom_rsi
```

---

## 必需的软件包版本 (重要)

**您必须编写与以下确切版本兼容的代码。**
系统在回测和实盘交易中均使用这些版本。

| 软件包 | 版本 | 用途 |
|---------|---------|---------|
| pandas | 1.5.3 | DataFrame 数据处理 |
| numpy | 1.24.4 | 数值运算 |
| ta-lib | 0.4.30 | 技术指标 (RSI, MACD, SMA, EMA 等) |
| scipy | 1.10.1 | 统计/数学函数 |

### TA-Lib 使用示例

```python
import talib
import numpy as np

# 将 pandas Series 转换为 numpy 数组以供 TA-Lib 使用
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

# ATR (Average True Range) - 需要 high, low, close
atr = talib.ATR(high_array, low_array, close_array, timeperiod=14)

# Stochastic
slowk, slowd = talib.STOCH(high_array, low_array, close_array,
                           fastk_period=14, slowk_period=3, slowd_period=3)
```

### 重要兼容性说明

1. **pandas 1.5.3**：使用 `.iloc[]` 进行位置索引，使用 `.loc[]` 进行标签索引
2. **numpy 1.24.4**：`np.NaN` 已弃用，请使用 `np.nan` 代替
3. **ta-lib 0.4.30**：输入必须是 numpy 数组，而非 pandas Series（使用 `.values`）
4. **scipy 1.10.1**：可用于高级统计计算

---

## 第一部分：策略文件 (`{strategy_name}.py`)

### 固定规则（必须遵守）

1. **函数名**必须为 `strategy`
2. **函数签名**必须完全一致：
```python
def strategy(context: DataContext, config_dict: dict) -> dict:
```

3. **必需的导入**：
```python
from module.data_context import DataContext
```

4. **可选导入**（从 common 文件夹 - 用户上传的模块）：
```python
from common.your_module import your_function
```

### 数据请求 API

```python
# [FIXED] 获取历史 OHLCV 数据
hist = context.get_history(
    assets=assets,           # 交易对列表，例如 ["BTCUSDT", "ETHUSDT"]
    window=window,           # 回溯窗口（K线数量）
    frequency=frequency,     # "1m" | "5m" | "15m" | "1d"
    fields=["close"]         # 可选字段: ["open", "high", "low", "close", "volume"]
)
```

### 数据格式 (MultiIndex DataFrame)

`hist` DataFrame 具有 MultiIndex，包含 `["asset", "datetime"]` 两个层级：

```
                                        open      high      low     close    volume
asset    datetime
BTCUSDT  2025-11-13 04:01:00+00:00    100.0    100.2     99.7    100.0    37215.0
         2025-11-13 04:02:00+00:00    100.0    100.5     99.8    100.3    42156.0
ETHUSDT  2025-11-13 04:01:00+00:00    105.1    105.1    104.7    105.0    74304.2
         2025-11-13 04:02:00+00:00    105.0    105.3    104.9    105.2    68421.5
```

**常用数据操作模式：**
```python
# 获取单列作为 DataFrame（资产为列，日期时间为索引）
df = hist["close"].unstack(level=0)

# 结果:
#                            BTCUSDT   ETHUSDT
# datetime
# 2025-11-13 04:01:00+00:00   100.0    105.0
# 2025-11-13 04:02:00+00:00   100.3    105.2

# 获取最新价格
latest_prices = df.iloc[-1]
```

### 返回格式（必须遵守）

```python
{
    "SYMBOL": {
        "weight": float,                  # 仓位权重（参见下方规则）
        "presetStopLossPrice": float,     # 止损价格（可以为 None）
        "presetStopSurplusPrice": float   # 止盈价格（可以为 None）
    }
}
```

**权重规则：**
- **正值** = 做多仓位
- **负值** = 做空仓位
- **绝对值之和不得超过 1.0**：`sum(|weight|) <= 1.0`
- 每个权重代表分配给该交易对的保证金资金比例

**返回值示例：**
```python
return {
    "BTCUSDT": {"weight": 0.4, "presetStopLossPrice": 98000.0, "presetStopSurplusPrice": 105000.0},
    "ETHUSDT": {"weight": -0.3, "presetStopLossPrice": 4200.0, "presetStopSurplusPrice": 3800.0},
    "XRPUSDT": {"weight": 0.2, "presetStopLossPrice": None, "presetStopSurplusPrice": None}
}
```

### 策略文件模板

```python
"""
{Strategy Name}

=== 固定值 (请勿修改) ===

1. 导入路径
   - from common.xxx import ... (固定)
   - 服务器使用用户专属的 common 文件夹存储上传的模块文件

2. 函数签名
   - def strategy(context: DataContext, config_dict: dict) -> dict (固定)

3. 配置访问
   - assets = config_dict['assets'] (固定)
   - frequency = config_dict.get("frequency", "1m") (固定)
   - 其他 config_dict 参数为每个策略自定义

4. 历史数据 API
   - context.get_history(assets=, window=, frequency=, fields=) (固定)
   - fields: 从 ohlcv 中选择所需列 (例如 ["close"], ["open", "high", "low", "close"])
   - 返回值: MultiIndex DataFrame (asset, datetime)

5. 返回格式 (固定)
   {
       "SYMBOL": {
           "weight": float,              # 绝对值之和 <= 1，正值=做多，负值=做空
           "presetStopLossPrice": float, # 可以为 None
           "presetStopSurplusPrice": float # 可以为 None
       }
   }
"""

# [FIXED] 导入: from module.data_context
from module.data_context import DataContext

# [OPTIONAL] 从 common 文件夹导入自定义模块
# from common.your_module import your_function

import pandas as pd
import numpy as np


# [FIXED] def strategy(context: DataContext, config_dict: dict) -> dict
def strategy(context: DataContext, config_dict: dict) -> dict:

    # [FIXED] 从 config_dict 获取 assets, frequency
    assets = config_dict['assets']
    frequency = config_dict.get("frequency", "1m")

    # [CUSTOM] 从配置中获取策略专属参数
    # 访问嵌套配置，例如: config_dict['config']['your_section']['param']
    # 示例:
    # base_config = config_dict['config']['base']
    # window = base_config.get("window", 180)

    # [FIXED] context.get_history(assets=, window=, frequency=, fields=)
    # 返回值: MultiIndex DataFrame (asset, datetime)，包含 OHLCV 列
    hist = context.get_history(
        assets=assets,
        window=window,  # 从配置获取 (示例: 100)
        frequency=frequency,
        fields=["close"]  # 仅选择需要的字段
    )

    if hist.empty:
        return {}

    # === 在此处编写您的策略逻辑 ===

    # 示例: 转换为以资产为列的 DataFrame
    df = hist["close"].unstack(level=0)
    latest_prices = df.iloc[-1]

    # 计算您的信号和权重...
    weights = {}  # 您的权重计算逻辑

    # 构建结果
    result = {}
    for symbol in assets:
        weight = weights.get(symbol, 0.0)
        price = latest_prices[symbol]

        # 计算止损和止盈（可选）
        sl = None  # 您的止损逻辑
        tp = None  # 您的止盈逻辑

        # [FIXED] 返回格式
        result[symbol] = {
            "weight": weight,
            "presetStopLossPrice": sl,
            "presetStopSurplusPrice": tp,
        }

    return result
```

---

## 第二部分：配置文件 (`config.yaml`)

### 配置结构

```yaml
version: "2.0"

# =============================================================================
# SYSTEM - 通用设置
# =============================================================================
system:
  trade_type: futures                    # [必填] futures | spot
  trade_env: backtest                    # [必填] backtest | live
  rebalancing_interval_hours: 8          # [必填] 再平衡间隔 (示例: 8)。允许分数: "5/60" = 5分钟
  leverage: 5                            # [仅期货] 杠杆 (示例: 5). 现货不使用.
  tz_str: "Asia/Seoul"                   # 时区 (示例: Asia/Seoul, 默认: UTC)

# =============================================================================
# STRATEGY - 策略设置
# =============================================================================
strategy:
  name: your_strategy_name               # [必填] 策略名称（必须与文件名一致）
  assets:                                # [必填] 交易资产（必须以 USDT 结尾）
    - BTCUSDT
    - ETHUSDT
    - XRPUSDT
  frequency: "15m"                       # [必填] 数据频率: 1m | 5m | 15m | 1d

  # [可选] 自定义参数 - 结构完全灵活
  # 您可以定义任何适合策略需要的嵌套结构。
  # 示例:
  #   config:
  #     window: 180
  #     rsi_period: 14
  #   或
  #   params:
  #     indicators: {sma: 20, ema: 50}
  #     thresholds: {buy: 30, sell: 70}

# =============================================================================
# BACKTEST - 仅回测用（trade_env: backtest 时必填）
# =============================================================================
backtest:
  data_apikey: "YOUR_DATA_API_KEY"       # [必填] 数据 API 密钥
  start_date: "2025-10-01 09:00"         # [必填] 开始日期时间
  end_date: "2025-10-10 08:59"           # [必填] 结束日期时间
  lookback_bars: 220                     # [必填] 见下方说明: 必须 >= 策略中使用的最大 window/period
  initial_capital: 10000                 # [必填] 初始资金 (USD)
  generate_report: true                  # 生成 Pyfolio 报告 (默认: true)

# =============================================================================
# LIVE - 仅实盘交易用（trade_env: live 时必填）
# =============================================================================
# live:
#   trading_hours: 720                   # 运行时长。720 = 30 天
#   data_apikey: "YOUR_API_KEY"
#
#   # --- 期货设置 (trade_type: futures 时) ---
#   futures:                             # 当 trade_type: futures 时
#     total_allocation: 0.8              # 资金分配比例 (0~1)
#     margin_mode: crossed               # crossed
#     pos_mode: hedge_mode               # hedge_mode
#
#   # --- 现货设置 (trade_type: spot 时) ---
#   spot:                                # 当 trade_type: spot 时
#     quote_coin: usdt
#     total_allocation: 0.8
```

> **注意:** `config.yaml` 结构在期货和现货中共用。`trade_type` 字段决定激活哪种模式。期货设置 `leverage`；现货则省略。`live` 部分根据 `trade_type` 使用对应的子键（`futures:` 或 `spot:`）。

### 配置如何传递给策略

策略函数中的 `config_dict` 参数接收 `strategy:` 部分下的所有键值：
```python
config_dict = {
    "name": "your_strategy_name",             # [必填] 来自 strategy.name
    "assets": ["BTCUSDT", "ETHUSDT", ...],    # [必填] 来自 strategy.assets
    "frequency": "15m",                        # [必填] 来自 strategy.frequency
    # ... 您在 strategy: 部分下定义的其他自定义键值
}
```

**重要：** `strategy:` 下的结构是灵活的。只有 `name`、`assets` 和 `frequency` 是必填项。
您定义的任何其他键值都将直接传递给 `config_dict`。

**请勿复制示例结构（base/position/sltp）。** 根据您的策略需求设计自己的参数结构。示例：
```yaml
# 简单的扁平结构（示例值 - 根据您的策略自定义）
strategy:
  name: my_strategy
  assets: [BTCUSDT, ETHUSDT]
  frequency: "15m"
  your_param_1: ...                      # 定义您自己的参数
  your_param_2: ...

# 或嵌套结构（示例值 - 根据您的策略自定义）
strategy:
  name: my_strategy
  assets: [BTCUSDT]
  frequency: "15m"
  your_section:
    param_a: ...
    param_b: ...
```

---

### 重要：lookback_bars 计算

**规则：** `lookback_bars` 必须大于或等于策略所需的最大历史数据量。

```
lookback_bars >= max(策略中使用的所有 window/period 值) + 缓冲区 (10~20%)
```

**何时需要历史数据？**

| 场景 | 示例 | 所需 lookback_bars |
|------|---------|----------------------|
| `get_history(window=N)` 调用 | `get_history(assets, window=200, ...)` | >= 200 |
| 移动平均线 | `talib.SMA(close, 50)` | >= 50 |
| RSI 计算 | `talib.RSI(close, 14)` | >= 14 |
| 组合使用 | `get_history(200)` 然后 `SMA(50)` | >= 200 |

**计算示例：**

如果您的策略使用：
- `get_history(window=200)`
- `talib.SMA(close, 20)`（短期 SMA）
- `talib.SMA(close, 50)`（长期 SMA）
- `talib.RSI(close, 14)`

那么：
```
max(200, 20, 50, 14) = 200
lookback_bars = 200 + 缓冲区 = 220（推荐值）
```

**lookback_bars 过小时的错误：**
```
History window extends before YYYY-MM-DD. To use this history window,
start the backtest on or after YYYY-MM-DD.
```
**解决方案：** 增加 `lookback_bars` 使其 >= 策略中请求的 window 值。

---

## 完整示例：RSI 均值回归策略

**注意：** 这只是一个示例，包含示例值。请根据您自己的策略逻辑设计自己的参数名称、结构和值。请勿盲目复制这些值。

### 文件: `rsi_mean_reversion.py`

```python
"""
RSI Mean Reversion Strategy
- RSI < 超卖阈值时做多
- RSI > 超买阈值时做空
"""

from module.data_context import DataContext
import talib
import numpy as np


def strategy(context: DataContext, config_dict: dict) -> dict:

    # [FIXED] 必需参数
    assets = config_dict['assets']
    frequency = config_dict.get("frequency", "1m")

    # [CUSTOM] 您自己的参数名称 - 根据您的策略设计
    # 以下默认值仅为示例
    window = config_dict.get("window", 100)           # 示例默认值
    rsi_period = config_dict.get("rsi_period", 14)    # 示例默认值
    oversold = config_dict.get("oversold", 30)        # 示例默认值
    overbought = config_dict.get("overbought", 70)    # 示例默认值
    stop_loss_pct = config_dict.get("stop_loss_pct", 0.02)    # 示例默认值
    take_profit_pct = config_dict.get("take_profit_pct", 0.04) # 示例默认值

    # [FIXED] 获取历史数据
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

    for symbol in assets:
        close_array = df[symbol].values
        rsi = talib.RSI(close_array, timeperiod=rsi_period)
        current_rsi = rsi[-1]
        price = latest_prices[symbol]

        if np.isnan(current_rsi):
            weight = 0.0
            sl, tp = None, None
        elif current_rsi < oversold:
            weight = 0.3  # 做多（示例权重 - 根据您的策略自定义）
            sl = price * (1 - stop_loss_pct)
            tp = price * (1 + take_profit_pct)
        elif current_rsi > overbought:
            weight = -0.3  # 做空（示例权重 - 根据您的策略自定义）
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

### 文件: `config.yaml`

```yaml
version: "2.0"

system:
  trade_type: futures                    # futures | spot
  trade_env: backtest
  rebalancing_interval_hours: 4          # (示例)
  leverage: 5                            # (示例) [仅期货]
  tz_str: "Asia/Seoul"                   # (示例)

strategy:
  name: rsi_mean_reversion
  assets:                                # (示例资产)
    - BTCUSDT
    - ETHUSDT
    - XRPUSDT
  frequency: "15m"

  # 自定义参数 - 以下所有值均为示例
  window: 100                            # (示例)
  rsi_period: 14                         # (示例)
  oversold: 30                           # (示例)
  overbought: 70                         # (示例)
  stop_loss_pct: 0.02                    # (示例)
  take_profit_pct: 0.04                  # (示例)

backtest:
  data_apikey: "YOUR_DATA_API_KEY"
  start_date: "2025-10-01 09:00"         # (示例)
  end_date: "2025-10-15 08:59"           # (示例)
  lookback_bars: 120                     # (示例) >= window + 缓冲区
  initial_capital: 10000                 # (示例)
  generate_report: true

# live:
#   trading_hours: 720
#   data_apikey: "YOUR_API_KEY"
#   futures:                               # [仅期货]
#     total_allocation: 0.8
#     margin_mode: crossed
#     pos_mode: hedge_mode
#   spot:                                  # [仅现货]
#     quote_coin: usdt
#     total_allocation: 0.8
```

---

## 输出格式要求

生成代码时，请按以下确切格式提供输出：

### 文件: `{strategy_name}.py`

```python
# 策略文件的完整内容
```

### 文件: `config.yaml`

```yaml
# 配置文件的完整内容
```

### [可选] 文件: `common/{module_name}.py`

当可复用的工具函数对策略有益时，生成通用模块。

```python
# 通用模块的完整内容
# 示例: common/indicators.py, common/signals.py, common/utils.py
```

**通用模块指南：**
- 每个模块应具有**单一职责**（指标、信号、仓位管理等）
- 为每个函数添加**文档字符串**，说明输入/输出
- 使用**类型提示**以提高代码清晰度
- 模块必须是**独立的**（不依赖策略专属代码）

**通用模块结构示例：**
```python
"""
Custom Indicators Module
可复用的技术指标函数，用于交易策略。
"""

import numpy as np
import talib


def weighted_rsi(close: np.ndarray, period: int, weight: float) -> np.ndarray:
    """
    示例：计算加权 RSI。
    这只是一个示例函数 - 请根据您的策略需求创建自己的函数。

    Args:
        close: 收盘价数组
        period: RSI 周期
        weight: 权重乘数

    Returns:
        加权 RSI 值
    """
    rsi = talib.RSI(close, timeperiod=period)
    return rsi * weight
```

---

## 您的策略想法

**在下方描述您的策略：**

（您可以使用的提示示例：）
- "创建一个使用 20 和 50 周期 SMA 的简单移动平均线交叉策略"
- "实现基于 RSI 的均值回归策略：RSI < 30 时做多，RSI > 70 时做空"
- "使用布林带构建波动率突破策略"
- "创建结合绝对动量和相对动量的双动量策略"

---

现在请为我的策略生成完整的 Python 代码和 YAML 配置文件。
