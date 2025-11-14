import pandas as pd

def calculate_momentum(df: pd.DataFrame, periods: list) -> dict:
    """
    Calculate the momentum of each stock in DataFrame(df).
    df index = datetime, columns = symbols
    """
    momentum = {}

    for col in df.columns:
        col_momentum = 0
        for p in periods:
            if len(df) > p:
                first_price = df[col].iloc[-p-1]
                last_price = df[col].iloc[-1]
                if first_price != 0:
                    col_momentum += (last_price / first_price) - 1

        momentum[col] = col_momentum / len(periods)

    return momentum


def normalize_weights(momentum: dict, long_ratio: float, short_ratio: float) -> dict:
    longs = {k: v for k, v in momentum.items() if v > 0}
    shorts = {k: v for k, v in momentum.items() if v < 0}

    weights = {}

    total_long = sum(longs.values())
    total_short = -sum(shorts.values())

    for k, v in longs.items():
        weights[k] = (v / total_long) * long_ratio if total_long != 0 else 0

    for k, v in shorts.items():
        weights[k] = (v / total_short) * short_ratio if total_short != 0 else 0

    # 스케일 조정
    abs_sum = sum(abs(w) for w in weights.values())
    if abs_sum > 1:
        scale = 1.0 / abs_sum
        for k in weights:
            weights[k] *= scale

    return weights
