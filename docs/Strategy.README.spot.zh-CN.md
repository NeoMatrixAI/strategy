# 现货策略开发指南 - AI 提示

> **交易类型: 现货 (Spot)**
>
> 本 README 提供多语言版本：
> - [English](../spot/README.md)
> - [Korean](Strategy.README.spot.ko.md)
> - Chinese (简体中文) - 当前文件

---

> 复制本 README 的全部内容，粘贴到 Claude、GPT、Gemini 或任何 AI 助手中。
> 然后描述您的策略想法，AI 将为本系统生成兼容的代码。

---

## AI 指令

您是一位专业的交易系统助手。
您的任务是严格按照以下规定的结构生成文件：

**必需文件：**
1. **`{strategy_name}.py`** - 策略逻辑文件
2. **`config.yaml`** - 配置文件

**可选文件（在有需要时生成）：**
3. **`common/{module_name}.py`** - 可复用的工具模块

用户将提供策略想法、技术指标或交易逻辑，您需要在固定模板中实现它们。

### 何时创建公共模块

在以下情况下，在 `common/` 文件夹中创建独立模块：
- 逻辑可以**在多个策略之间复用**（指标、信号生成器、仓位管理）
- 代码通过**分离关注点**提高可读性（例如，复杂计算）
- 函数是**独立的工具函数**（例如，自定义指标、数据转换器）

**不要为以下情况创建公共模块：**
- 不会被复用的策略特定逻辑
- 简单的一行计算
- 配置或常量（保留在 config.yaml 中）

---

## 现货交易规则 (重要)

**本系统用于现货交易。必须遵守以下约束条件：**

1. **仅做多** - 现货交易不能做空。所有权重必须 >= 0。
2. **无杠杆** - 现货交易不使用杠杆。
3. **权重 = 0 表示卖出** - 将权重设为 0（或省略该交易对）将卖出全部持仓。
4. **止盈字段** - 使用 `presetTakeProfitPrice`（不是期货使用的 `presetStopSurplusPrice`）。

---

## 系统架构概览

```
strategy/
├── common/                        # 共享模块（按需创建）
│   └── {module_name}.py           # 例如：indicators.py, signals.py, utils.py
└── spot/
    └── {strategy_name}/           # 策略文件夹（名称 = 策略名称）
        ├── {strategy_name}.py     # 策略逻辑（文件名必须与文件夹名一致）
        └── config.yaml            # 配置文件
```

**公共模块的导入路径：**
```python
from common.{module_name} import your_function
# 示例：from common.indicators import custom_rsi
```

---

## 必需的包版本 (重要)

**您必须编写与以下精确包版本兼容的代码。**
系统在回测和实盘交易中均使用这些版本。

| 包名 | 版本 | 用途 |
|------|------|------|
| pandas | 1.5.3 | DataFrame 数据处理 |
| numpy | 1.24.4 | 数值运算 |
| ta-lib | 0.4.30 | 技术指标（RSI、MACD、SMA、EMA 等） |
| scipy | 1.10.1 | 统计/数学函数 |

### TA-Lib 使用示例

```python
import talib
import numpy as np

# 将 pandas Series 转换为 numpy 数组以供 TA-Lib 使用
close_array = df["close"].values

# 简单移动平均线
sma_20 = talib.SMA(close_array, timeperiod=20)

# 指数移动平均线
ema_12 = talib.EMA(close_array, timeperiod=12)

# RSI（相对强弱指数）
rsi = talib.RSI(close_array, timeperiod=14)

# MACD
macd, macd_signal, macd_hist = talib.MACD(close_array, fastperiod=12, slowperiod=26, signalperiod=9)

# 布林带
upper, middle, lower = talib.BBANDS(close_array, timeperiod=20, nbdevup=2, nbdevdn=2)

# ATR（平均真实波幅）- 需要最高价、最低价、收盘价
atr = talib.ATR(high_array, low_array, close_array, timeperiod=14)

# 随机指标
slowk, slowd = talib.STOCH(high_array, low_array, close_array,
                           fastk_period=14, slowk_period=3, slowd_period=3)
```

### 重要的兼容性说明

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
    fields=["close"]         # 可选字段：["open", "high", "low", "close", "volume"]
)
```

### 数据格式（MultiIndex DataFrame）

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

# 结果：
#                            BTCUSDT   ETHUSDT
# datetime
# 2025-11-13 04:01:00+00:00   100.0    105.0
# 2025-11-13 04:02:00+00:00   100.3    105.2

# 获取最新价格
latest_prices = df.iloc[-1]
```

### 返回格式（必须遵守 - 现货）

```python
{
    "SYMBOL": {
        "weight": float,                  # 必须 >= 0（仅做多，不能做空）
        "presetTakeProfitPrice": float,   # 止盈价格（可以为 None）
        "presetStopLossPrice": float      # 止损价格（可以为 None）
    }
}
```

**可选的额外止盈/止损字段（用于高级控制）：**
```python
{
    "SYMBOL": {
        "weight": float,
        "presetTakeProfitPrice": float,
        "presetStopLossPrice": float,
        "executeTakeProfitPrice": float,    # 可选：执行止盈价格
        "executeStopLossPrice": float       # 可选：执行止损价格
    }
}
```

**权重规则（现货 - 仅做多）：**
- **所有权重必须 >= 0**（现货交易不能做空）
- **weight = 0** 表示无仓位 / 如果当前持有则卖出全部
- **省略某个交易对** 表示如果当前持有该交易对则全部卖出
- **所有权重之和不得超过 1.0**：`sum(weight) <= 1.0`
- 每个权重代表该交易对的资金分配比例

**返回示例：**
```python
return {
    "BTCUSDT": {"weight": 0.5, "presetTakeProfitPrice": 105000.0, "presetStopLossPrice": 98000.0},
    "ETHUSDT": {"weight": 0.3, "presetTakeProfitPrice": 4200.0, "presetStopLossPrice": 3500.0},
    "XRPUSDT": {"weight": 0.2, "presetTakeProfitPrice": None, "presetStopLossPrice": None}
}
```

### 策略文件模板

```python
"""
{Strategy Name}

=== 固定值（请勿修改）===

1. 导入路径
   - from common.xxx import ... (FIXED)
   - 服务器使用用户专属的 common 文件夹存储上传的模块文件

2. 函数签名
   - def strategy(context: DataContext, config_dict: dict) -> dict (FIXED)

3. 配置访问
   - assets = config_dict['assets'] (FIXED)
   - frequency = config_dict.get("frequency", "1m") (FIXED)
   - 其他 config_dict 参数由每个策略自定义

4. 历史数据 API
   - context.get_history(assets=, window=, frequency=, fields=) (FIXED)
   - fields：从 ohlcv 中选择所需列（例如 ["close"]、["open", "high", "low", "close"]）
   - 返回值：MultiIndex DataFrame (asset, datetime)

5. 返回格式 (FIXED - 现货)
   {
       "SYMBOL": {
           "weight": float,              # >= 0，仅做多，sum <= 1.0
           "presetTakeProfitPrice": float, # 可以为 None
           "presetStopLossPrice": float    # 可以为 None
       }
   }
"""

# [FIXED] 导入：from module.data_context
from module.data_context import DataContext

# [OPTIONAL] 从 common 文件夹导入自定义模块
# from common.your_module import your_function

import pandas as pd
import numpy as np


# [FIXED] def strategy(context: DataContext, config_dict: dict) -> dict
def strategy(context: DataContext, config_dict: dict) -> dict:

    # [FIXED] 从 config_dict 获取 assets 和 frequency
    assets = config_dict['assets']
    frequency = config_dict.get("frequency", "1m")

    # [CUSTOM] 从配置中获取策略特定参数
    # 访问嵌套配置：config_dict['config']['your_section']['param']
    # 示例：
    # base_config = config_dict['config']['base']
    # window = base_config.get("window", 180)

    # [FIXED] context.get_history(assets=, window=, frequency=, fields=)
    # 返回值：MultiIndex DataFrame (asset, datetime)，包含 OHLCV 列
    hist = context.get_history(
        assets=assets,
        window=window,  # 从配置获取（示例：100）
        frequency=frequency,
        fields=["close"]  # 仅选择您需要的字段
    )

    if hist.empty:
        return {}

    # === 在此处编写您的策略逻辑 ===

    # 示例：转换为以资产为列的 DataFrame
    df = hist["close"].unstack(level=0)
    latest_prices = df.iloc[-1]

    # 计算您的信号和权重...
    weights = {}  # 您的权重计算逻辑

    # 构建结果
    result = {}
    for symbol in assets:
        weight = weights.get(symbol, 0.0)
        price = latest_prices[symbol]

        # 现货：权重必须 >= 0（仅做多）
        weight = max(weight, 0.0)

        # 计算止损和止盈（可选，仅用于有效仓位）
        sl = None  # 您的止损逻辑
        tp = None  # 您的止盈逻辑

        if weight > 0:
            sl = price * (1 - 0.05)  # 示例：5% 止损
            tp = price * (1 + 0.10)  # 示例：10% 止盈

        # [FIXED] 返回格式（现货）
        result[symbol] = {
            "weight": weight,
            "presetTakeProfitPrice": tp,
            "presetStopLossPrice": sl,
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
  trade_type: spot                     # [必需] futures | spot
  trade_env: backtest                  # [必需] backtest | live
  rebalancing_interval_hours: 8        # [必需] 再平衡间隔（小时）。允许使用分数："5/60" = 5分钟
  tz_str: "Asia/Seoul"                 # 时区（默认：UTC）
  # leverage: 5                          # [仅期货] 现货交易不使用

# =============================================================================
# STRATEGY - 策略设置
# =============================================================================
strategy:
  name: your_strategy_name               # [必需] 策略名称（必须与文件名一致）
  assets:                                # [必需] 交易资产（必须以 USDT 结尾）
    - BTCUSDT
    - ETHUSDT
    - XRPUSDT
  frequency: "15m"                       # [必需] 数据频率：1m | 5m | 15m | 1d

  # [可选] 自定义参数 - 结构完全灵活
  # 您可以定义任何适合您策略需求的嵌套结构。
  # 示例：
  #   config:
  #     window: 180
  #     rsi_period: 14
  #   或
  #   params:
  #     indicators: {sma: 20, ema: 50}
  #     thresholds: {buy: 30, sell: 70}

# =============================================================================
# BACKTEST - 仅回测（trade_env 为 backtest 时必需）
# =============================================================================
backtest:
  data_apikey: "YOUR_DATA_API_KEY"       # [必需] 数据 API 密钥
  start_date: "2025-10-01 09:00"         # [必需] 开始日期时间
  end_date: "2025-10-10 08:59"           # [必需] 结束日期时间
  lookback_bars: 220                     # [必需] 见下文：必须 >= 策略中使用的最大 window/period 值
  initial_capital: 10000                 # [必需] 初始资金（USD）
  generate_report: true                  # 生成 Pyfolio 报告（默认：true）

# =============================================================================
# LIVE - 仅实盘交易（trade_env 为 live 时必需）
# =============================================================================
# live:
#   trading_hours: 720                   # 运行时长。720 = 30 天
#   data_apikey: "YOUR_API_KEY"
#
#   # --- 期货设置 (trade_type: futures 时) ---
#   futures:                             # [仅期货]
#     total_allocation: 0.8
#     margin_mode: crossed
#     pos_mode: hedge_mode
#
#   # --- 现货设置 (trade_type: spot 时) ---
#   spot:                                # [仅现货]
#     quote_coin: usdt                   # 计价货币（默认：usdt）
#     total_allocation: 0.8              # 资金分配比例 (0~1)
```

> **注意:** `config.yaml` 结构在期货和现货中共用。`trade_type` 字段决定激活哪种模式。现货不使用 `leverage`。`live` 部分根据 `trade_type` 使用对应的子键（`futures:` 或 `spot:`）。

### 配置如何传递给策略

策略函数中的 `config_dict` 参数接收 `strategy:` 部分下的所有键：
```python
config_dict = {
    "name": "your_strategy_name",             # [必需] 来自 strategy.name
    "assets": ["BTCUSDT", "ETHUSDT", ...],    # [必需] 来自 strategy.assets
    "frequency": "15m",                        # [必需] 来自 strategy.frequency
    # ... 您在 strategy: 部分下定义的任何其他自定义键
}
```

**重要：** `strategy:` 下的结构是灵活的。只有 `name`、`assets` 和 `frequency` 是必需的。
您定义的任何其他键都会直接传递到 `config_dict`。

**不要复制示例结构（base/position/sltp）。** 请根据您策略的需求设计自己的参数结构。示例：
```yaml
# 简单的平面结构（示例值 - 请根据您的策略自定义）
strategy:
  name: my_strategy
  assets: [BTCUSDT, ETHUSDT]
  frequency: "15m"
  your_param_1: ...                      # 定义您自己的参数
  your_param_2: ...

# 或嵌套结构（示例值 - 请根据您的策略自定义）
strategy:
  name: my_strategy
  assets: [BTCUSDT]
  frequency: "15m"
  your_section:
    param_a: ...
    param_b: ...
```

---

### 重要：lookback_bars 的计算

**规则：** `lookback_bars` 必须大于或等于策略所需的最大历史数据量。

```
lookback_bars >= max(策略中使用的所有 window/period 值) + 缓冲区 (10~20%)
```

**何时需要历史数据？**

| 场景 | 示例 | 所需 lookback_bars |
|------|------|-------------------|
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

## 完整示例：RSI 均值回归策略（现货）

**注意：** 这只是一个示例，包含示例值。请根据您自己的策略逻辑设计参数名称、结构和值。不要盲目复制这些值。

### 文件：`rsi_mean_reversion.py`

```python
"""
RSI 均值回归策略（现货 - 仅做多）
- 当 RSI < 超卖阈值时买入（做多入场）
- 当 RSI > 超买阈值时卖出（weight=0）（现货不能做空）
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
            weight = 0.3  # 做多（示例权重 - 请根据您的策略自定义）
            sl = price * (1 - stop_loss_pct)
            tp = price * (1 + take_profit_pct)
        elif current_rsi > overbought:
            # 现货：不能做空 - 持有现金（weight = 0）
            weight = 0.0
            sl, tp = None, None
        else:
            weight = 0.0
            sl, tp = None, None

        result[symbol] = {
            "weight": weight,
            "presetTakeProfitPrice": tp,
            "presetStopLossPrice": sl,
        }

    return result
```

### 文件：`config.yaml`

```yaml
version: "2.0"

system:
  trade_type: spot                         # futures | spot
  trade_env: backtest
  rebalancing_interval_hours: 4            # （示例）
  tz_str: "Asia/Seoul"                     # （示例）
  # leverage: 5                            # [仅期货] 现货不使用

strategy:
  name: rsi_mean_reversion
  assets:                                  # （示例资产）
    - BTCUSDT
    - ETHUSDT
    - XRPUSDT
  frequency: "15m"

  # 自定义参数 - 以下所有值均为示例
  window: 100                              # （示例）
  rsi_period: 14                           # （示例）
  oversold: 30                             # （示例）
  overbought: 70                           # （示例）
  stop_loss_pct: 0.02                      # （示例）
  take_profit_pct: 0.04                    # （示例）

backtest:
  data_apikey: "YOUR_DATA_API_KEY"
  start_date: "2025-10-01 09:00"           # （示例）
  end_date: "2025-10-15 08:59"             # （示例）
  lookback_bars: 120                       # （示例）>= window + 缓冲区
  initial_capital: 10000                   # （示例）
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

生成代码时，请按照以下格式提供输出：

### 文件：`{strategy_name}.py`

```python
# 策略文件的完整内容
```

### 文件：`config.yaml`

```yaml
# 配置文件的完整内容
```

### [可选] 文件：`common/{module_name}.py`

当可复用的工具函数对策略有益时，生成公共模块。

```python
# 公共模块的完整内容
# 示例：common/indicators.py, common/signals.py, common/utils.py
```

**公共模块指南：**
- 每个模块应具有**单一职责**（指标、信号、仓位管理等）
- 为每个函数添加**文档字符串**，说明输入/输出
- 使用**类型提示**以提高代码清晰度
- 模块必须是**独立的**（不依赖于策略特定代码）

**公共模块结构示例：**
```python
"""
自定义指标模块
用于交易策略的可复用技术指标函数。
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

（您可以使用的示例提示：）
- "创建一个简单的移动平均线交叉策略，当 SMA 20 上穿 SMA 50 时买入"
- "实现基于 RSI 的均值回归策略：RSI < 30 时买入，RSI > 70 时卖出"
- "使用布林带构建波动率突破策略 - 在触及下轨时买入"
- "创建一个动量策略，将资金分配给表现最好的资产"

---

现在请为我的策略生成完整的 Python 代码和 YAML 配置。
