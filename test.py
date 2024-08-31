import MetaTrader5 as mt5
import ccxt
import yfinance as yf
import pandas as pd

if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()


# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()


def is_pin_bar_top(candle):
    # اطلاعات کندل
    time_open = candle.time  # زمان افتتاح کندل
    open_price = candle.open  # قیمت افتتاح
    close_price = candle.close  # قیمت بسته شدن
    high_price = candle.high  # بیشینه قیمت در طول بازه
    low_price = candle.low  # کمینه قیمت در طول بازه

    # بررسی آیا کندل پین بار از بالا یا پایین است
    body_range = abs(open_price - close_price)
    total_range = high_price - low_price

    # محاسبه طول شمشیر بالایی و پایینی (سایه)
    upper_wick = (high_price - open_price) if open_price > close_price else (high_price - close_price)
    lower_wick = (open_price - low_price) if open_price > close_price else (close_price - low_price)

    # بررسی آیا کندل پین بار است
    if (upper_wick >= 2.5 * body_range) and (lower_wick <= (body_range * 2)):
        return True
    else:
        return False


#aa.mt5_conn.__init__(account=188670, server = "s54ff5P!", password =  "AronMarkets-Demo",)
mt5.login(account=188670, server = "s54ff5P!", password =  "AronMarkets-Demo",)
#print('salam')
#price1 = mt5.symbol_info_tick('BTCUSD.').ask
#price = mt5.symbol_info_tick('ETHUSD.').ask
#print(price1)
#print(price)





import MetaTrader5 as mt5

from hashem import *

mt5.initialize(login=188670, server = "AronMarkets-Demo", password =  "s54ff5P!")
price1 = mt5.symbol_info_tick('XAUUSD.').ask
print(price1)



import MetaTrader5 as mt5

# اتصال به MT5
if not mt5.initialize(login=188670, server = "AronMarkets-Demo", password =  "s54ff5P!"):
    print("Failed to initialize MT5")
    mt5.shutdown()
    quit()

# تنظیم پارامترهای سفارش
symbol = "XAUUSD."
lot = 0.1

# بررسی اطلاعات نماد
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(f"Failed to get symbol info for {symbol}")
    mt5.shutdown()
    quit()

if symbol_info.trade_exemode == mt5.SYMBOL_TRADE_MODE_DISABLED:
    print(f"Trading is disabled for {symbol}")
    mt5.shutdown()
    quit()

# گرفتن قیمت جاری
tick_info = mt5.symbol_info_tick(symbol)
if tick_info is None:
    print(f"Failed to get tick info for {symbol}")
    mt5.shutdown()
    quit()

price = tick_info.ask
point = symbol_info.point
stop_loss = price - 100 * point
take_profit = price + 100 * point
deviation = 300  # افزایش بیشتر deviation

# ایجاد سفارش خرید
order = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": stop_loss,
    "tp": take_profit,
    "deviation": deviation,
    "magic": 234000,
    "comment": "Python script",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_FOK,  # تغییر این مقدار
}

# Test with FOK (Fill or Kill)
order['type_filling'] = mt5.ORDER_FILLING_FOK
result = mt5.order_send(order)

if result.retcode != mt5.TRADE_RETCODE_DONE:
    print(f"FOK failed, trying IOC...")
    # Test with IOC (Immediate or Cancel)
    order['type_filling'] = mt5.ORDER_FILLING_IOC
    result = mt5.order_send(order)

if result.retcode != mt5.TRADE_RETCODE_DONE:
    print(f"IOC failed, trying RETURN...")
    # Test with RETURN (Return)
    order['type_filling'] = mt5.ORDER_FILLING_RETURN
    result = mt5.order_send(order)

if result.retcode != mt5.TRADE_RETCODE_DONE:
    print(f"Order send failed, retcode={result.retcode}, result={result}")
else:
    print(f"Order send succeeded, {result}")




average50('5m' , 'XAUUSD.')








from hashem import *
import MetaTrader5 as mt5
import time

# تنظیمات اولیه و اتصال به MetaTrader 5
login = 189703
server = 'AronMarkets-Demo'
password = 'be732!cX'

if not mt5.initialize(login=login, server=server, password=password):
    print("Failed to connect to MetaTrader 5, last error:", mt5.last_error())
    quit()

print("Connected to MetaTrader 5")

# انتخاب نماد مورد نظر
symbol = 'XAUUSD.'

# اطمینان از فعال بودن نماد
if not mt5.symbol_select(symbol, True):
    print(f"Failed to select symbol {symbol}")
    mt5.shutdown()
    quit()

# تابعی برای ایجاد سفارش
def create_order(symbol, volume, order_type, price, sl, tp, comment):
    order_type_dict = {'buy': mt5.ORDER_TYPE_BUY, 'sell': mt5.ORDER_TYPE_SELL}
    request = {
        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': symbol,
        'volume': volume,
        'type': order_type_dict[order_type],
        'price': price,
        'sl': sl,
        'tp': tp,
        'deviation': 20,
        'magic': 234000,
        'comment': comment,
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC,
    }

    # ارسال سفارش
    result = mt5.order_send(request)
    return result

# اجرای معاملات بر اساس شرایط مشخص شده
while True:
    price = mt5.symbol_info_tick(symbol).ask
    if price is None:
        print(f"Failed to get price for {symbol}")
        break

    # مثال از شرایط ساده برای ایجاد سفارش خرید
    stg15M = False
    stg15M2 = False

    positions = mt5.positions_get(symbol=symbol)
    for position in positions:
        if position.comment == 'STG15M':
            stg15M = True
        elif position.comment == 'STG15M2':
            stg15M2 = True

    if not stg15M:
        sl = price - 10  # حد ضرر مثال
        tp = price + 20  # حد سود مثال
        result = create_order(symbol, 0.01, 'buy', price, sl, tp, 'STG15M')
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Order STG15M failed, error: {mt5.last_error()}")
        else:
            print("Order STG15M placed successfully")

    time.sleep(60)  # صبر برای 1 دقیقه

# پایان و قطع ارتباط با MetaTrader 5
mt5.shutdown()

