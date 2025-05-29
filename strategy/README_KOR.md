# 전략 가이드
## 📘 나만의 전략 함수 만들기

이 가이드는 코딩에 익숙하지 않은 사용자도 쉽게 따라 할 수 있도록 설계되었습니다.  
단계별로 전략 함수를 만드는 과정을 설명하며, 아래 예제를 참고해 같은 구조로 자신만의 전략을 만들 수 있습니다.

---

## ✅ 필수 구조 (고정 규칙)

- 함수 이름은 반드시 `strategy` 여야 합니다
- 함수 입력값: `df`, `config_dict`
- 함수 반환값: `long_candidates`, `short_candidates` (둘 다 리스트여야 함)
- 설정(config)은 다음과 같이 접근해야 합니다:

```python
strategy_specific_config = config_dict.get('strategy_config')
```

전략 설정은 다음과 같이 별도 파일 (예: config.py) 에 정의되어야 합니다:

```python
# config.py 예시
hours = 12  # 시간 단위

strategy_config = {
    "maximum_candidates": 5,  # 상하위 자산 개수
    "minutes": 60*hours       # 분 단위로 변환
}
```

> ⚠️ 시스템이 이 strategy_config를 config_dict로 감싸서 아래와 같이 전달합니다:

```python
longs, shorts = strategy.strategy(df, {'strategy_config': config.strategy_config})
```

사용자가 config_dict를 직접 만들 필요는 없습니다—위와 같이 호출만 하면 됩니다.

---

## 🧾 입력 데이터 구조 (`df`)

전략 함수로 들어오는 `df`는 시계열 가격 데이터프레임입니다:

- 인덱스: 분 단위 타임스탬프
- 컬럼: 자산 이름 (예: BTCUSDT, ETHUSDT 등)
- 값: 각 시점의 종가 (float)

예시 구조:

| 시간               | BTCUSDT | ETHUSDT | XRPUSDT | ... |
|--------------------|---------|---------|---------|-----|
| 2025-04-13 00:00:00| 84817.0 | 1655.26 | 2.1568  | ... |
| 2025-04-13 00:01:00| 84836.7 | 1655.39 | 2.1565  | ... |
| 2025-04-13 00:02:00| 84891.7 | 1656.20 | 2.1593  | ... |

> ✅ 전략 함수는 이 DataFrame을 기반으로 종목을 선택합니다.

---

## 🪄 전략 예시: 단순 수익률 기반 전략

```python
import pandas as pd

def strategy(df, config_dict):
    """
    단순 수익률 기반 전략 예제.
    최신 가격과 N분 전 가격을 비교하여
    수익률이 가장 높은 자산을 long, 낮은 자산을 short로 선택합니다.
    """
    strategy_specific_config = config_dict.get('strategy_config')

    period = strategy_specific_config.get("minutes")[0]  # 첫 번째 값만 사용
    maximum_candidates = strategy_specific_config.get("maximum_candidates")

    returns = df.iloc[-1] / df.iloc[-period] - 1  # 단순 수익률 계산
    sorted_returns = returns.sort_values(ascending=False)

    long_candidates = list(sorted_returns.head(maximum_candidates).index)
    short_candidates = list(sorted_returns.tail(maximum_candidates).index)

    return long_candidates, short_candidates
```

---

## 🧱 전체 구성 예시 (Config 포함)

```python
# 1. config.py 예시
hours = 12

strategy_config = {
    "maximum_candidates": 5,
    "minutes": 60 * hours
}

# 2. strategy.py: 위 전략 함수 포함

# 3. 실행 예시 (main.py 또는 Jupyter Notebook 등에서)
import strategy
import config

df = get_price_data_somehow()
longs, shorts = strategy.strategy(df, {"strategy_config": config.strategy_config})

print("📈 Long 종목:", longs)
print("📉 Short 종목:", shorts)
```

---

## ✅ 기대되는 출력 형식

```python
📈 Long 종목:
['BTCUSDT', 'ETHUSDT', 'XRPUSDT']

📉 Short 종목:
['SOLUSDT', 'AVAXUSDT', 'DOGEUSDT']
```

---

## ❓ 팁

- df는 시스템에서 자동으로 제공됩니다.
- 결과는 반드시 리스트 형태로 반환해야 합니다.
- 복잡한 전략은 이 예시를 기반으로 확장 가능합니다.


---

## 🛠 config.py 예시 템플릿

```python
# config.py

hours = 12

strategy_config = {
    "maximum_candidates": 5,
    "minutes": 60 * hours
}
```

✅ strategy_config는 시스템이 자동으로 strategy 함수에 전달합니다.


