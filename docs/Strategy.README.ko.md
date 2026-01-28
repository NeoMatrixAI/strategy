# 전략 개발 가이드 - AI 프롬프트

> 이 README는 여러 언어로 제공됩니다:
> - [English (default)](../futures/README.md)
> - Korean - 이 파일
> - [Chinese](Strategy.README.zh-CN.md)

---

> 이 README 전체를 복사하여 Claude, GPT, Gemini 또는 다른 AI 어시스턴트에 붙여넣으세요.
> 그 후 전략 아이디어를 설명하면 AI가 이 시스템에 호환되는 코드를 생성합니다.

---

## AI 지시사항

당신은 전문 트레이딩 시스템 어시스턴트입니다.
아래의 필수 구조를 엄격히 따르는 파일을 생성해야 합니다:

**필수 파일:**
1. **`{strategy_name}.py`** - 전략 로직 파일
2. **`config.yaml`** - 설정 파일

**선택 파일 (유용할 때 생성):**
3. **`common/{module_name}.py`** - 재사용 가능한 유틸리티 모듈

사용자가 전략 아이디어, 지표, 매매 로직을 제공하면 고정된 템플릿 안에 구현해야 합니다.

### Common 모듈 생성 시점

다음 경우에 `common/` 폴더에 별도 모듈을 생성하세요:
- **여러 전략에서 재사용** 가능한 로직 (지표, 시그널 생성기, 포지션 사이징)
- 관심사 분리로 **가독성이 향상**되는 코드 (예: 복잡한 계산)
- **독립적인 유틸리티** 함수 (예: 커스텀 지표, 데이터 변환기)

**Common 모듈을 생성하지 말아야 할 경우:**
- 재사용되지 않을 전략 특화 로직
- 단순한 한 줄 계산
- 설정이나 상수 (config.yaml에 유지)

---

## 시스템 아키텍처 개요

```
strategy/
├── common/                        # 공유 모듈 (필요시 생성)
│   └── {module_name}.py           # 예: indicators.py, signals.py, utils.py
└── futures/
    └── {strategy_name}/           # 전략 폴더 (이름 = 전략명)
        ├── {strategy_name}.py     # 전략 로직 (파일명은 폴더명과 일치해야 함)
        └── config.yaml            # 설정 파일
```

**Common 모듈 import 경로:**
```python
from common.{module_name} import your_function
# 예시: from common.indicators import custom_rsi
```

---

## 필수 패키지 버전 (중요)

**반드시 아래 정확한 패키지 버전과 호환되는 코드를 작성해야 합니다.**
시스템은 백테스팅과 실거래 모두에서 이 버전들을 사용합니다.

| 패키지 | 버전 | 용도 |
|--------|------|------|
| pandas | 1.5.3 | DataFrame 처리 |
| numpy | 1.24.4 | 수치 연산 |
| ta-lib | 0.4.30 | 기술적 지표 (RSI, MACD, SMA, EMA 등) |
| scipy | 1.10.1 | 통계/수학 함수 |

### TA-Lib 사용 예시

```python
import talib
import numpy as np

# pandas Series를 TA-Lib용 numpy 배열로 변환
close_array = df["close"].values

# 단순 이동평균
sma_20 = talib.SMA(close_array, timeperiod=20)

# 지수 이동평균
ema_12 = talib.EMA(close_array, timeperiod=12)

# RSI (상대강도지수)
rsi = talib.RSI(close_array, timeperiod=14)

# MACD
macd, macd_signal, macd_hist = talib.MACD(close_array, fastperiod=12, slowperiod=26, signalperiod=9)

# 볼린저 밴드
upper, middle, lower = talib.BBANDS(close_array, timeperiod=20, nbdevup=2, nbdevdn=2)

# ATR (평균진정범위) - high, low, close 필요
atr = talib.ATR(high_array, low_array, close_array, timeperiod=14)

# 스토캐스틱
slowk, slowd = talib.STOCH(high_array, low_array, close_array,
                           fastk_period=14, slowk_period=3, slowd_period=3)
```

### 중요 호환성 참고사항

1. **pandas 1.5.3**: 위치 인덱싱은 `.iloc[]`, 라벨 인덱싱은 `.loc[]` 사용
2. **numpy 1.24.4**: `np.NaN`은 deprecated, `np.nan` 사용
3. **ta-lib 0.4.30**: 입력은 pandas Series가 아닌 numpy 배열이어야 함 (`.values` 사용)
4. **scipy 1.10.1**: 고급 통계 계산에 사용 가능

---

## Part 1: 전략 파일 (`{strategy_name}.py`)

### 고정 규칙 (반드시 준수)

1. **함수 이름**은 반드시 `strategy`
2. **함수 시그니처**는 정확히 다음과 같아야 함:
```python
def strategy(context: DataContext, config_dict: dict) -> dict:
```

3. **필수 import**:
```python
from module.data_context import DataContext
```

4. **선택적 imports** (common 폴더에서 - 사용자 업로드 모듈):
```python
from common.your_module import your_function
```

### 데이터 요청 API

```python
# [FIXED] 과거 OHLCV 데이터 조회
hist = context.get_history(
    assets=assets,           # 심볼 리스트, 예: ["BTCUSDT", "ETHUSDT"]
    window=window,           # 조회 기간 (봉 개수)
    frequency=frequency,     # "1m" | "5m" | "15m" | "1d"
    fields=["close"]         # 선택: ["open", "high", "low", "close", "volume"]
)
```

### 데이터 형식 (MultiIndex DataFrame)

`hist` DataFrame은 `["asset", "datetime"]` 레벨의 MultiIndex를 가집니다:

```
                                        open      high      low     close    volume
asset    datetime
BTCUSDT  2025-11-13 04:01:00+00:00    100.0    100.2     99.7    100.0    37215.0
         2025-11-13 04:02:00+00:00    100.0    100.5     99.8    100.3    42156.0
ETHUSDT  2025-11-13 04:01:00+00:00    105.1    105.1    104.7    105.0    74304.2
         2025-11-13 04:02:00+00:00    105.0    105.3    104.9    105.2    68421.5
```

**일반적인 데이터 처리 패턴:**
```python
# 단일 컬럼을 DataFrame으로 변환 (자산이 컬럼, datetime이 인덱스)
df = hist["close"].unstack(level=0)

# 결과:
#                            BTCUSDT   ETHUSDT
# datetime
# 2025-11-13 04:01:00+00:00   100.0    105.0
# 2025-11-13 04:02:00+00:00   100.3    105.2

# 최신 가격 조회
latest_prices = df.iloc[-1]
```

### 반환 형식 (반드시 준수)

```python
{
    "SYMBOL": {
        "weight": float,                  # 포지션 비중 (아래 규칙 참조)
        "presetStopLossPrice": float,     # 손절가 (None 가능)
        "presetStopSurplusPrice": float   # 익절가 (None 가능)
    }
}
```

**Weight 규칙:**
- **양수** = 롱 포지션
- **음수** = 숏 포지션
- **절대값 합계는 1.0을 초과할 수 없음**: `sum(|weight|) <= 1.0`
- 각 weight는 해당 심볼에 할당된 마진 자본 비율을 나타냄

**반환 예시:**
```python
return {
    "BTCUSDT": {"weight": 0.4, "presetStopLossPrice": 98000.0, "presetStopSurplusPrice": 105000.0},
    "ETHUSDT": {"weight": -0.3, "presetStopLossPrice": 4200.0, "presetStopSurplusPrice": 3800.0},
    "XRPUSDT": {"weight": 0.2, "presetStopLossPrice": None, "presetStopSurplusPrice": None}
}
```

### 전략 파일 템플릿

```python
"""
{Strategy Name}

=== 고정값 (변경 불가) ===

1. Import 경로
   - from common.xxx import ... (FIXED)
   - 서버는 업로드된 모듈 파일을 위해 사용자별 common 폴더 사용

2. 함수 시그니처
   - def strategy(context: DataContext, config_dict: dict) -> dict (FIXED)

3. Config 접근
   - assets = config_dict['assets'] (FIXED)
   - frequency = config_dict.get("frequency", "1m") (FIXED)
   - 기타 config_dict 파라미터는 전략별 커스텀

4. History API
   - context.get_history(assets=, window=, frequency=, fields=) (FIXED)
   - fields: ohlcv에서 필요한 컬럼 리스트 (예: ["close"], ["open", "high", "low", "close"])
   - 반환: MultiIndex DataFrame (asset, datetime)

5. 반환 형식 (FIXED)
   {
       "SYMBOL": {
           "weight": float,              # 절대값 합 <= 1, 양수=롱, 음수=숏
           "presetStopLossPrice": float, # None 가능
           "presetStopSurplusPrice": float # None 가능
       }
   }
"""

# [FIXED] Import: from module.data_context
from module.data_context import DataContext

# [OPTIONAL] common 폴더에서 커스텀 모듈 import
# from common.your_module import your_function

import pandas as pd
import numpy as np


# [FIXED] def strategy(context: DataContext, config_dict: dict) -> dict
def strategy(context: DataContext, config_dict: dict) -> dict:

    # [FIXED] config_dict에서 assets, frequency
    assets = config_dict['assets']
    frequency = config_dict.get("frequency", "1m")

    # [CUSTOM] config에서 전략 특화 파라미터
    # 중첩 config 접근 예: config_dict['config']['your_section']['param']
    # 예시:
    # base_config = config_dict['config']['base']
    # window = base_config.get("window", 180)

    # [FIXED] context.get_history(assets=, window=, frequency=, fields=)
    # 반환: OHLCV 컬럼을 가진 MultiIndex DataFrame (asset, datetime)
    hist = context.get_history(
        assets=assets,
        window=window,  # config에서 (예시: 100)
        frequency=frequency,
        fields=["close"]  # 필요한 필드만 선택
    )

    if hist.empty:
        return {}

    # === 여기에 전략 로직 구현 ===

    # 예시: 자산을 컬럼으로 하는 DataFrame으로 변환
    df = hist["close"].unstack(level=0)
    latest_prices = df.iloc[-1]

    # 시그널과 weight 계산...
    weights = {}  # weight 계산 로직

    # 결과 생성
    result = {}
    for symbol in assets:
        weight = weights.get(symbol, 0.0)
        price = latest_prices[symbol]

        # 손절/익절 계산 (선택사항)
        sl = None  # 손절 로직
        tp = None  # 익절 로직

        # [FIXED] 반환 형식
        result[symbol] = {
            "weight": weight,
            "presetStopLossPrice": sl,
            "presetStopSurplusPrice": tp,
        }

    return result
```

---

## Part 2: 설정 파일 (`config.yaml`)

### 설정 구조

```yaml
version: "2.0"

# =============================================================================
# SYSTEM - 공통 설정
# =============================================================================
system:
  trade_type: futures                    # [Required] futures | spot
  trade_env: backtest                    # [Required] backtest | live
  rebalancing_interval_hours: 8          # [Required] 리밸런싱 간격 (예시: 8). 분수 허용: "5/60" = 5분
  leverage: 5                            # 레버리지 (예시: 5)
  tz_str: "Asia/Seoul"                   # 타임존 (예시: Asia/Seoul, 기본값: UTC)

# =============================================================================
# STRATEGY - 전략 설정
# =============================================================================
strategy:
  name: your_strategy_name               # [Required] 전략명 (파일명과 일치해야 함)
  assets:                                # [Required] 거래 자산 (USDT로 끝나야 함)
    - BTCUSDT
    - ETHUSDT
    - XRPUSDT
  frequency: "15m"                       # [Required] 데이터 주기: 1m | 5m | 15m | 1d

  # [OPTIONAL] 커스텀 파라미터 - 구조는 완전히 자유
  # 전략 필요에 맞는 어떤 중첩 구조든 정의 가능
  # 예시:
  #   config:
  #     window: 180
  #     rsi_period: 14
  #   또는
  #   params:
  #     indicators: {sma: 20, ema: 50}
  #     thresholds: {buy: 30, sell: 70}

# =============================================================================
# BACKTEST - 백테스트 전용 (trade_env: backtest일 때 필수)
# =============================================================================
backtest:
  data_apikey: "YOUR_DATA_API_KEY"       # [Required] 데이터 API 키
  start_date: "2025-10-01 09:00"         # [Required] 시작 일시
  end_date: "2025-10-10 08:59"           # [Required] 종료 일시
  lookback_bars: 220                     # [Required] 아래 참조: 전략에서 사용하는 최대 window/period 이상이어야 함
  initial_capital: 10000                 # [Required] 초기 자본 (USD)
  generate_report: true                  # Pyfolio 리포트 생성 (기본값: true)

# =============================================================================
# LIVE - 실거래 전용 (trade_env: live일 때 필수)
# =============================================================================
# live:
#   trading_hours: 720                   # 운영 시간. 720 = 30일
#   data_apikey: "YOUR_API_KEY"
#
#   futures:                             # trade_type: futures일 때
#     total_allocation: 0.8              # 자본 배분 비율 (0~1)
#     margin_mode: crossed               # crossed
#     pos_mode: hedge_mode               # hedge_mode
#
#   spot:                                # trade_type: spot일 때
#     quote_coin: usdt
#     total_allocation: 0.8
```

### Config가 전략에 전달되는 방식

전략 함수의 `config_dict` 파라미터는 `strategy:` 섹션 아래의 모든 키를 받습니다:
```python
config_dict = {
    "name": "your_strategy_name",             # [Required] strategy.name에서
    "assets": ["BTCUSDT", "ETHUSDT", ...],    # [Required] strategy.assets에서
    "frequency": "15m",                        # [Required] strategy.frequency에서
    # ... strategy: 섹션에 정의한 다른 모든 커스텀 키
}
```

**중요:** `strategy:` 아래 구조는 자유롭습니다. `name`, `assets`, `frequency`만 필수입니다.
정의한 추가 키들은 `config_dict`에 직접 전달됩니다.

**예시 구조를 그대로 복사하지 마세요.** 전략 필요에 맞게 자신만의 파라미터 구조를 설계하세요. 예시:
```yaml
# 단순 평면 구조 (예시 값 - 전략에 맞게 커스터마이즈)
strategy:
  name: my_strategy
  assets: [BTCUSDT, ETHUSDT]
  frequency: "15m"
  your_param_1: ...                      # 자신만의 파라미터 정의
  your_param_2: ...

# 또는 중첩 구조 (예시 값 - 전략에 맞게 커스터마이즈)
strategy:
  name: my_strategy
  assets: [BTCUSDT]
  frequency: "15m"
  your_section:
    param_a: ...
    param_b: ...
```

---

### 중요: lookback_bars 계산

**규칙:** `lookback_bars`는 전략이 필요로 하는 최대 과거 데이터 이상이어야 합니다.

```
lookback_bars >= max(전략에서 사용하는 모든 window/period 값) + 버퍼 (10~20%)
```

**언제 과거 데이터가 필요한가?**

| 경우 | 예시 | 필요한 lookback_bars |
|------|------|---------------------|
| `get_history(window=N)` 호출 | `get_history(assets, window=200, ...)` | >= 200 |
| 이동평균 | `talib.SMA(close, 50)` | >= 50 |
| RSI 계산 | `talib.RSI(close, 14)` | >= 14 |
| 복합 사용 | `get_history(200)` 후 `SMA(50)` | >= 200 |

**계산 예시:**

전략이 다음을 사용하는 경우:
- `get_history(window=200)`
- `talib.SMA(close, 20)` (단기 SMA)
- `talib.SMA(close, 50)` (장기 SMA)
- `talib.RSI(close, 14)`

그러면:
```
max(200, 20, 50, 14) = 200
lookback_bars = 200 + 버퍼 = 220 (권장)
```

**lookback_bars가 너무 작을 때 오류:**
```
History window extends before YYYY-MM-DD. To use this history window,
start the backtest on or after YYYY-MM-DD.
```
**해결:** `lookback_bars`를 전략에서 요청하는 window 이상으로 늘리세요.

---

## 완전한 예시: RSI 평균회귀 전략

**참고:** 이것은 예시 값을 가진 하나의 예시일 뿐입니다. 당신의 전략 로직에 맞게 자신만의 파라미터 이름, 구조, 값을 설계하세요. 이 값들을 그대로 복사하지 마세요.

### 파일: `rsi_mean_reversion.py`

```python
"""
RSI 평균회귀 전략
- RSI < 과매도 임계값일 때 롱
- RSI > 과매수 임계값일 때 숏
"""

from module.data_context import DataContext
import talib
import numpy as np


def strategy(context: DataContext, config_dict: dict) -> dict:

    # [FIXED] 필수 파라미터
    assets = config_dict['assets']
    frequency = config_dict.get("frequency", "1m")

    # [CUSTOM] 자신만의 파라미터명 - 전략에 맞게 설계
    # 아래 기본값은 예시일 뿐
    window = config_dict.get("window", 100)           # 예시 기본값
    rsi_period = config_dict.get("rsi_period", 14)    # 예시 기본값
    oversold = config_dict.get("oversold", 30)        # 예시 기본값
    overbought = config_dict.get("overbought", 70)    # 예시 기본값
    stop_loss_pct = config_dict.get("stop_loss_pct", 0.02)    # 예시 기본값
    take_profit_pct = config_dict.get("take_profit_pct", 0.04) # 예시 기본값

    # [FIXED] 과거 데이터 조회
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
            weight = 0.3  # 롱 (예시 weight - 전략에 맞게 커스터마이즈)
            sl = price * (1 - stop_loss_pct)
            tp = price * (1 + take_profit_pct)
        elif current_rsi > overbought:
            weight = -0.3  # 숏 (예시 weight - 전략에 맞게 커스터마이즈)
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

### 파일: `config.yaml`

```yaml
version: "2.0"

system:
  trade_type: futures
  trade_env: backtest
  rebalancing_interval_hours: 4          # (예시)
  leverage: 5                            # (예시)
  tz_str: "Asia/Seoul"                   # (예시)

strategy:
  name: rsi_mean_reversion
  assets:                                # (예시 자산)
    - BTCUSDT
    - ETHUSDT
    - XRPUSDT
  frequency: "15m"

  # 커스텀 파라미터 - 아래 모든 값은 예시임
  window: 100                            # (예시)
  rsi_period: 14                         # (예시)
  oversold: 30                           # (예시)
  overbought: 70                         # (예시)
  stop_loss_pct: 0.02                    # (예시)
  take_profit_pct: 0.04                  # (예시)

backtest:
  data_apikey: "YOUR_DATA_API_KEY"
  start_date: "2025-10-01 09:00"         # (예시)
  end_date: "2025-10-15 08:59"           # (예시)
  lookback_bars: 120                     # (예시) >= window + 버퍼
  initial_capital: 10000                 # (예시)
  generate_report: true
```

---

## 출력 형식 요구사항

코드 생성 시 정확히 다음 형식으로 출력하세요:

### 파일: `{strategy_name}.py`

```python
# 전략 파일의 전체 내용
```

### 파일: `config.yaml`

```yaml
# 설정 파일의 전체 내용
```

### [선택] 파일: `common/{module_name}.py`

재사용 가능한 유틸리티가 전략에 도움이 될 때 common 모듈을 생성하세요.

```python
# common 모듈의 전체 내용
# 예시: common/indicators.py, common/signals.py, common/utils.py
```

**Common 모듈 가이드라인:**
- 각 모듈은 **단일 책임**을 가져야 함 (지표, 시그널, 포지션 사이징 등)
- 각 함수에 입출력을 설명하는 **docstring** 포함
- 코드 명확성을 위해 **type hints** 사용
- 모듈은 **독립적**이어야 함 (전략 특화 코드에 의존하지 않음)

**Common 모듈 구조 예시:**
```python
"""
커스텀 지표 모듈
트레이딩 전략을 위한 재사용 가능한 기술적 지표 함수.
"""

import numpy as np
import talib


def weighted_rsi(close: np.ndarray, period: int, weight: float) -> np.ndarray:
    """
    예시: 가중 RSI 계산.
    이것은 예시 함수일 뿐 - 전략 필요에 맞게 자신만의 함수를 만드세요.

    Args:
        close: 종가 배열
        period: RSI 기간
        weight: 가중치 승수

    Returns:
        가중 RSI 값
    """
    rsi = talib.RSI(close, timeperiod=period)
    return rsi * weight
```

---

## 나의 전략 아이디어

**아래에 전략을 설명하세요:**

(사용 가능한 예시 프롬프트:)
- "20일과 50일 SMA를 사용한 단순 이동평균 크로스오버 전략을 만들어주세요"
- "RSI 기반 평균회귀 구현: RSI < 30이면 롱, RSI > 70이면 숏"
- "볼린저 밴드를 사용한 변동성 돌파 전략을 만들어주세요"
- "절대 모멘텀과 상대 모멘텀을 결합한 듀얼 모멘텀 전략을 만들어주세요"

---

이제 나의 전략에 대한 완전한 Python 코드와 YAML 설정을 생성하세요.
