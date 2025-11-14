from module.data_context import DataContext
from common.momentum_utils import calculate_momentum, normalize_weights
from common.sltp_utils import compute_sltp

def strategy(context: DataContext, config_dict: dict) -> dict:
    strategy_config = config_dict['strategy_config']
    position_config = config_dict['position_config']
    sltp_config = config_dict['sltp_config']
    assets = config_dict['assets']
    
    window = strategy_config.get("window", 180)
    periods = strategy_config.get("minutes", [60, 120, 180])
    long_ratio = position_config.get("long_ratio", 0.7)
    short_ratio = position_config.get("short_ratio", 0.3)
    stop_loss_pct = sltp_config.get("stop_loss_pct", 0.02)
    take_profit_pct = sltp_config.get("take_profit_pct", 0.04)

    # 1분 데이터 로드
    hist = context.get_history(
        assets=assets,
        window=window + max(periods),
        frequency="1m",
        fields=["close"]
    )

    if hist.empty:
        return {}

    df = hist["close"].unstack(level=0)

    # 모듈 호출
    momentum = calculate_momentum(df, periods)
    weights = normalize_weights(momentum, long_ratio, short_ratio)

    latest_prices = df.iloc[-1]
    result = {}

    for symbol, weight in weights.items():
        price = latest_prices[symbol]

        sl, tp = compute_sltp(price, weight, stop_loss_pct, take_profit_pct)

        result[symbol] = {
            "weight": weight,
            "presetStopLossPrice": sl,
            "presetStopSurplusPrice": tp,
        }

    return result