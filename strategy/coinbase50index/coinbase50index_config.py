# ==========================
# Required System Settings
# ==========================

system_config = {
    "data_apikey": "Input your Data API key", # CoinAPI - data api key
    "strategy_name": "coinbase50index",
    "trading_hours": 336,
    "base_symbol": "BTCUSDT",
    "symbols": ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'SOLUSDT', 'DOGEUSDT', 'ADAUSDT', 'LINKUSDT', 'AVAXUSDT', 'XLMUSDT', 'SHIBUSDT', 'BCHUSDT', 'LTCUSDT', 'DOTUSDT', 'PEPEUSDT', 'AAVEUSDT', 'UNIUSDT', 'NEARUSDT', 'APTUSDT', 'ETCUSDT', 'ICPUSDT', 'RENDERUSDT', 'FETUSDT', 'POLUSDT', 'ATOMUSDT', 'ALGOUSDT', 'BONKUSDT', 'MKRUSDT', 'QNTUSDT', 'STXUSDT', 'INJUSDT', 'EOSUSDT', 'WIFUSDT', 'GRTUSDT', 'CRVUSDT', 'JASMYUSDT', 'ZECUSDT', 'LDOUSDT', 'SANDUSDT', 'HNTUSDT', 'XTZUSDT', 'MANAUSDT', 'APEUSDT', 'AEROUSDT', 'AXSUSDT', 'CHZUSDT', 'COMPUSDT', '1INCHUSDT', 'SNXUSDT', 'ROSEUSDT', 'LPTUSDT'],
    "productType": "usdt-futures",
    "posMode": "hedge_mode",
    "marginMode": "crossed",
    "holdSide": "long",
    "marginCoin": "usdt",
    "orderType": "market",
    "timeframe": "1min",
    "tradeType": "future",
    "is_portfolio": True,   
    "total_allocation": 0.90,
    "leverage": 1,
    "new_data_window": 5,
    "weight_method": "custom",
    "custom_weights": {
        'BTCUSDT': '0.5404', 'ETHUSDT': '0.2014', 'XRPUSDT': '0.0884', 
        'SOLUSDT': '0.0565', 'DOGEUSDT': '0.0216', 'ADAUSDT': '0.0175', 
        'LINKUSDT': '0.0064', 'AVAXUSDT': '0.0061', 'XLMUSDT': '0.0057', 
        'SHIBUSDT': '0.0056', 'BCHUSDT': '0.0054', 'LTCUSDT': '0.0048', 
        'DOTUSDT': '0.0046', 'PEPEUSDT': '0.0036', 'AAVEUSDT': '0.0027', 
        'UNIUSDT': '0.0024', 'NEARUSDT': '0.0021', 'APTUSDT': '0.0020', 
        'ETCUSDT': '0.0018', 'ICPUSDT': '0.0016', 'RENDERUSDT': '0.0016', 
        'FETUSDT': '0.0014', 'POLUSDT': '0.0013', 'ATOMUSDT': '0.0012', 
        'ALGOUSDT': '0.0012', 'BONKUSDT': '0.0010', 'MKRUSDT': '0.0009', 
        'QNTUSDT': '0.0009', 'STXUSDT': '0.0009', 'INJUSDT': '0.0008', 
        'EOSUSDT': '0.0008', 'WIFUSDT': '0.0007', 'GRTUSDT': '0.0007', 
        'CRVUSDT': '0.0006', 'JASMYUSDT': '0.0006', 'ZECUSDT': '0.0005',
        'LDOUSDT': '0.0005', 'SANDUSDT': '0.0005', 'HNTUSDT': '0.0005', 
        'XTZUSDT': '0.0004', 'MANAUSDT': '0.0004', 'APEUSDT': '0.0003', 
        'AEROUSDT': '0.0003', 'AXSUSDT': '0.0003', 'CHZUSDT': '0.0003', 
        'COMPUSDT': '0.0002', '1INCHUSDT': '0.0002', 'SNXUSDT': '0.0002', 
        'ROSEUSDT': '0.0001', 'LPTUSDT': '0.0001'} 
}

# ==========================
# Rebalancing Trade Parameters
# ==========================

rebalancing_config = {
    "rebalancing_interval_hours": 1/2, # Rebalancing cycle (hours)
    "minimum_candidates": 0
}


# ==========================
# Strategy Parameter Settings
# ==========================

strategy_config = {
}
