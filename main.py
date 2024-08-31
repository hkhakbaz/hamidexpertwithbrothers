import time

import MetaTrader5 as mt5
from hashem import *

if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

mt5.login(account=188670, server="s54ff5P!", password="AronMarkets-Demo", )

symbols = [{"name": "XAUUSD", "point": 250}, {"name": "EURUSD", "point": 30}, {"name": "GBPUSD", "point": 75},
           {"name": "NZDUSD", "point": 50},{"name": "XAGUSD", "point": 50}]

while True:
    try:
        # "DJI","DAXEUR",
        for item in symbols:
            point = item.get("point")
            symbol = item.get("name")
            sema = ema20('5m', symbol)
            print(sema)
            sKandels = kandel('5m', 5, symbol)
            print(sKandels[1]["close"])
            if sKandels[1]["close"] > sema:
                if is_pin_bar_top(sKandels[1]) and abs(sKandels[1]["close"] - sema) >= point:
                    tp = sKandels[1]["close"] + (sKandels[1]["close"] - sKandels[1]["low"]) * 0.01
                    sl = round(sKandels[1]["low"], 0)
                    create_order(symbol, 1.0, mt5.ORDER_TYPE_SELL, 1, sl, tp, "")
            else:
                if is_pin_bar_bottom(sKandels[1]) and abs(sema - sKandels[1]["close"]) <= point:
                    tp = round((sKandels[1]["close"] - (sKandels[1]["high"] - sKandels[1]["close"])), 0)
                    sl = round(sKandels[1]["high"], 0)
                    create_order(symbol, 1.0, mt5.ORDER_TYPE_BUY, 1, sl, tp, "")
    except Exception as e:
        print(e)
    time.sleep(60)
