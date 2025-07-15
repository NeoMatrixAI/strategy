import pandas as pd
import numpy as np
import talib

def strategy(df: pd.DataFrame, config_dict: dict) -> dict:
    """
    SMA strategy for test
    """

    # Get settings
    strategy_specific_config = config_dict.get('strategy_config')
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    sma_short_period = strategy_specific_config.get("sma_short")
    sma_long_period = strategy_specific_config.get("sma_long")
    take_profit_ratio = strategy_specific_config.get("take_profit_ratio")
    stop_loss_ratio = strategy_specific_config.get("stop_loss_ratio")

    result = {}
    symbols = df.columns.drop('datetime')
    df = df.copy()
    df.set_index('datetime', inplace=True)

    for symbol in symbols:
        close = df[symbol].astype(float)
        sma_short = talib.SMA(close, timeperiod=sma_short_period)
        sma_long = talib.SMA(close, timeperiod=sma_long_period)

        # 유효 데이터 확인
        if len(close) < max(sma_short_period, sma_long_period) + 1:
            continue
        if np.isnan(sma_short.iloc[-1]) or np.isnan(sma_long.iloc[-1]):
            continue

        prev_short = sma_short.iloc[-2]
        prev_long = sma_long.iloc[-2]
        curr_short = sma_short.iloc[-1]
        curr_long = sma_long.iloc[-1]
        price = close.iloc[-1]

        # 매수/매도 신호 판별
        signal = None
        if prev_short < prev_long and curr_short > curr_long:
            signal = 'buy'
        elif prev_short > prev_long and curr_short < curr_long:
            signal = 'sell'

        if signal:
            size = 1
            if signal == 'buy':
                entry_price = price
                preset_take = round(entry_price * (1 + take_profit_ratio), 4)
                execute_take = round(entry_price * (1 + take_profit_ratio * 0.9), 4)
                preset_stop = round(entry_price * (1 - stop_loss_ratio), 4)
                execute_stop = round(entry_price * (1 - stop_loss_ratio * 0.8), 4)
            else:  # sell
                entry_price = price
                preset_take = round(entry_price * (1 - take_profit_ratio), 4)
                execute_take = round(entry_price * (1 - take_profit_ratio * 0.9), 4)
                preset_stop = round(entry_price * (1 + stop_loss_ratio), 4)
                execute_stop = round(entry_price * (1 + stop_loss_ratio * 0.8), 4)

            result[symbol] = {
                "size": str(size),
                "presetTakeProfitPrice": str(preset_take),
                "executeTakeProfitPrice": str(execute_take),
                "presetStopLossPrice": str(preset_stop),
                "executeStopLossPrice": str(execute_stop)
            }

    return result