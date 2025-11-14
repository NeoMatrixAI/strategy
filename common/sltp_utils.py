def compute_sltp(price: float, weight: float, sl_pct: float, tp_pct: float):
    """ SL/TP price calculation according to position """
    
    if weight > 0:
        sl_price = price * (1 - sl_pct)
        tp_price = price * (1 + tp_pct)
    elif weight < 0:
        sl_price = price * (1 + sl_pct)
        tp_price = price * (1 - tp_pct)
    else:
        return None, None

    return round(sl_price, 4), round(tp_price, 4)
