import numpy
import datetime
import time
import pandas as pd
import MetaTrader5 as mt5
import statistics
import ta
import yfinance as yf


# Total positions
def total_positons():
    positions_total = mt5.positions_total()
    return positions_total


# balance
def balance():
    balance = mt5.account_info()._asdict()['balance']
    return balance


# profit
def profit():
    positions = mt5.positions_get()
    profit = 0
    for position in positions:
        profit += position._asdict()['profit']
    return profit


# kandel
def kandel(timeframe='30m', limit=10, symbol='BTCUSD.'):
    symbol = symbol
    if timeframe == '5m':
        time = mt5.TIMEFRAME_M5
    if timeframe == '3m':
        time = mt5.TIMEFRAME_M3
    if timeframe == '1m':
        time = mt5.TIMEFRAME_M1
    if timeframe == '15m':
        time = mt5.TIMEFRAME_M15
    if timeframe == '30m':
        time = mt5.TIMEFRAME_M30
    if timeframe == '1h':
        time = mt5.TIMEFRAME_H1
    if timeframe == '4h':
        time = mt5.TIMEFRAME_H4
    if timeframe == '1d':
        time = mt5.TIMEFRAME_D1
    if timeframe == '1w':
        time = mt5.TIMEFRAME_W1
    candles = mt5.copy_rates_from_pos(symbol, time, 0, limit)
    df = pd.DataFrame(candles, columns=['time', 'open', 'high', 'low', 'close'])
    return df.iloc
#df.iloc
def is_pin_bar_top(candel):

    # اطلاعات کندل
    time_open = candel.time       # زمان افتتاح کندل
    open_price = candel.open             # قیمت افتتاح
    close_price = candel.close            # قیمت بسته شدن
    high_price = candel.high         # بیشینه قیمت در طول بازه
    low_price = candel.low           # کمینه قیمت در طول بازه

    # بررسی آیا کندل پین بار از بالا یا پایین است
    body_range = abs(open_price - close_price)
    total_range = high_price - low_price
    # محاسبه طول شمشیر بالایی و پایینی (سایه)
    upper_wick = (high_price - open_price) if (open_price > close_price) else (high_price - close_price)
    lower_wick = (close_price - low_price) if (open_price > close_price) else (open_price - low_price)

    # بررسی آیا کندل پین بار است
    if (upper_wick >= 2.5 * body_range) and (lower_wick <= (body_range*2)):
        #is_pin_bar = true;
        return 1
    else:
        return 0

def is_pin_bar_top_fors2(candel):

    # اطلاعات کندل
    time_open = candel.time       # زمان افتتاح کندل
    open_price = candel.open             # قیمت افتتاح
    close_price = candel.close            # قیمت بسته شدن
    high_price = candel.high         # بیشینه قیمت در طول بازه
    low_price = candel.low           # کمینه قیمت در طول بازه

    # بررسی آیا کندل پین بار از بالا یا پایین است
    body_range = abs(open_price - close_price)
    total_range = high_price - low_price
    # محاسبه طول شمشیر بالایی و پایینی (سایه)
    upper_wick = (high_price - open_price) if (open_price > close_price) else (high_price - close_price)
    lower_wick = (close_price - low_price) if (open_price > close_price) else (open_price - low_price)

    # بررسی آیا کندل پین بار است
    if (upper_wick >= 1.8 * body_range) and (lower_wick <= (body_range*2)):
        #is_pin_bar = true;
        return 1
    else:
        return 0

def is_pin_bar_bottom(candel):

    # اطلاعات کندل
    time_open = candel.time       # زمان افتتاح کندل
    open_price = candel.open             # قیمت افتتاح
    close_price = candel.close            # قیمت بسته شدن
    high_price = candel.high         # بیشینه قیمت در طول بازه
    low_price = candel.low           # کمینه قیمت در طول بازه

    # بررسی آیا کندل پین بار از بالا یا پایین است
    body_range = abs(open_price - close_price)
    total_range = high_price - low_price
    # محاسبه طول شمشیر بالایی و پایینی (سایه)
    upper_wick = (high_price - open_price) if (open_price > close_price) else (high_price - close_price)
    lower_wick = (close_price - low_price) if (open_price > close_price) else (open_price - low_price)
    # بررسی آیا کندل پین بار است
    if (lower_wick >= 2.5 * body_range) and (upper_wick < (body_range*2)):
        #is_pin_bar = true;
        return 1
    else:
        return 0

def is_pin_bar_bottom_fors2(candel):

    # اطلاعات کندل
    time_open = candel.time       # زمان افتتاح کندل
    open_price = candel.open             # قیمت افتتاح
    close_price = candel.close            # قیمت بسته شدن
    high_price = candel.high         # بیشینه قیمت در طول بازه
    low_price = candel.low           # کمینه قیمت در طول بازه

    # بررسی آیا کندل پین بار از بالا یا پایین است
    body_range = abs(open_price - close_price)
    total_range = high_price - low_price
    # محاسبه طول شمشیر بالایی و پایینی (سایه)
    upper_wick = (high_price - open_price) if (open_price > close_price) else (high_price - close_price)
    lower_wick = (close_price - low_price) if (open_price > close_price) else (open_price - low_price)
    # بررسی آیا کندل پین بار است
    if (lower_wick >= 1.8 * body_range) and (upper_wick < (body_range*2)):
        #is_pin_bar = true;
        return 1
    else:
        return 0

# rsi
def rsi(timeframe, symbol):
    ohlc = kandel(timeframe, 14 * 10, symbol)
    candles = pd.DataFrame(ohlc[:])
    candles['rsi'] = ta.momentum.RSIIndicator(candles['close'], window=14).rsi()
    rsi = candles['rsi'].tolist()
    return rsi[-1]


# lot
def qty(myBalance):
    if myBalance < 300:
        lot = 0.01
        return lot
    elif myBalance >= 300 and myBalance <= 499:
        lot = 0.02
        return lot
    elif myBalance >= 500 and myBalance <= 999:
        lot = 0.03
        return lot
    elif myBalance >= 1000 and myBalance <= 1499:
        lot = 0.04
        return lot
    elif myBalance >= 1500 and myBalance <= 1999:
        lot = 0.05
        return lot
    elif myBalance >= 2000 and myBalance <= 2499:
        lot = 0.06
        return lot
    elif myBalance >= 2500 and myBalance <= 2999:
        lot = 0.07
        return lot
    elif myBalance >= 3000 and myBalance <= 3999:
        lot = 0.08
        return lot
    elif myBalance >= 4000 and myBalance <= 5000:
        lot = 0.09
        return lot
    elif myBalance > 5000:
        lot = 0.1
        return lot


# create_order
def create_order(symbol, lot, order_type, price, sl, tp, comment):
    symbol_info = mt5.symbol_info(symbol)
    filling_mode = symbol_info.filling_mode
    if filling_mode == 1:
        filling_mode = mt5.ORDER_FILLING_FOK
    elif filling_mode == 2:
        filling_mode = mt5.ORDER_FILLING_IOC
    elif filling_mode != 1 and filling_mode != 2:
        filling_mode = mt5.ORDER_FILLING_FOK or mt5.ORDER_FILLING_IOC

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": filling_mode,
    }
    order = mt5.order_send(request)
    return order


# close_order
def close_order(symbol, lot, order_type, price, ticket):
    filling_modes = [mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_RETURN]

    for filling_mode in filling_modes:
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": order_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": 0,
            "comment": "Close position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": filling_mode,
        }

        result = mt5.order_send(request)


# moving average 26
def average26(timeframe, symbol='BTCUSD.'):
    ohlc = kandel(timeframe, limit=26, symbol=symbol)
    average = statistics.mean(item['low'] for item in ohlc)
    return average


# moving average 12
def average12(timeframe, symbol='BTCUSD.'):
    ohlc = kandel(timeframe, limit=12, symbol=symbol)
    average = statistics.mean(item['close'] for item in ohlc)
    return average


# moving average 50
def average50(timeframe, symbol='BTCUSD.'):
    ohlc = kandel(timeframe, limit=50, symbol=symbol)
    average = statistics.mean(item['close'] for item in ohlc)
    return average


# moving average 60
def average60(timeframe, symbol='BTCUSD.'):
    ohlc = kandel(timeframe, limit=60, symbol=symbol)
    average = statistics.mean(item['close'] for item in ohlc)
    return average


# moving average 162
def average162(timeframe, symbol='BTCUSD.'):
    ohlc = kandel(timeframe, limit=162, symbol=symbol)
    average = statistics.mean(item['close'] for item in ohlc)
    return average


# moving average 100
def average100(timeframe, symbol='BTCUSD.'):
    ohlc = kandel(timeframe, limit=100, symbol=symbol)
    average = statistics.mean(item['close'] for item in ohlc)
    return average


# moving average 200
def average200(timeframe, symbol='BTCUSD.'):
    ohlc = kandel(timeframe, limit=200, symbol=symbol)
    average = statistics.mean(item['close'] for item in ohlc)
    return average


# long or short
def whatKandel(timeframe='30m', candle=-1, symbol='BTCUSD.'):
    ohlc = kandel(timeframe, limit=10, symbol=symbol)
    if ohlc[candle]['open'] > ohlc[candle]['close']:
        return 'short'
    else:
        return 'long'


def isBeta(timeframe, candel, symbol='BTCUSD.', m=50):
    kandels = kandel(timeframe, limit=10, symbol=symbol)
    res = kandels[candel]
    if res['open'] > res['close']:
        # short kandel
        if res['open'] == res['high'] and (res['close'] - res['low']) <= res['open'] - res['close'] and body(timeframe,
                                                                                                             candel,
                                                                                                             symbol) >= m:
            return True
        else:
            return False
    elif res['open'] < res['close']:
        # long kandel
        if res['open'] == res['low'] and (res['high'] - res['close']) <= res['close'] - res['open'] and body(timeframe,
                                                                                                             candel,
                                                                                                             symbol) >= m:
            return True
        else:
            return False
    else:
        return False


def isBack(timeframe, candel, upOrDown, symbol='BTCUSD.'):
    kandels = kandel(timeframe, limit=10, symbol=symbol)
    res = kandels[candel]
    if res['open'] > res['close']:
        # short kandel
        if upOrDown == 'up' and (res['open'] - res['close']) * 3 < res['high'] - res['open'] and (
                res['close'] - res['low']) * 3 <= res['high'] - res['open']:
            return True

        elif upOrDown == 'down' and (res['open'] - res['close']) * 4 < res['close'] - res['low'] and (
                res['high'] - res['open']) * 3 <= res['close'] - res['low']:
            return True
        else:
            return False

    elif res['open'] < res['close']:
        # long kandel
        if upOrDown == 'up' and (res['close'] - res['open']) * 4 < res['high'] - res['close'] and res['high'] - res[
            'close'] > (res['open'] - res['low']) * 3:
            return True

        elif upOrDown == 'down' and (res['close'] - res['open']) * 3 < res['open'] - res['low'] and (
                res['high'] - res['close']) * 3 < res['open'] - res['low']:
            return True

        else:
            return False
    else:
        return False


def body(timeframe, candel, symbol='BTCUSD.'):
    kandels = kandel(timeframe, limit=10, symbol=symbol)
    res = kandels[candel]
    if res['open'] > res['close']:
        # short kandel
        body = res['open'] - res['close']
        return body

    elif res['open'] < res['close']:
        # long kandel
        body = res['close'] - res['open']
        return body
    else:
        return 0


def check_time(start_hour, end_hour):
    current_time = datetime.datetime.now(datetime.UTC).time()
    if current_time.hour >= start_hour and current_time.hour <= end_hour:
        return True
    else:
        return False


def hemayat(symbol):
    kandeld = kandel('1d', 5, symbol)
    kandelw = kandel('1w', 5, symbol)
    kande4h = kandel('4h', 5, symbol)
    kande1h = kandel('1h', 5, symbol)
    lines = [kandeld[-2]['high'], kandeld[-2]['low'], kandelw[-1]['high'], kandelw[-1]['low'], kandelw[-2]['high'],
             kandelw[-2]['low'], kande4h[-2]['high'], kande4h[-2]['low'], kande1h[-2]['high'], kande1h[-2]['low']]
    price = mt5.symbol_info_tick(symbol).ask
    line = []
    for i in lines:
        if i < price:
            line.append(i)
    if len(line) == 0:
        return False
    else:
        return max(line)


def moghavemat(symbol):
    kandeld = kandel('1d', 5, symbol)
    kandelw = kandel('1w', 5, symbol)
    kande4h = kandel('4h', 5, symbol)
    kande1h = kandel('1h', 5, symbol)
    lines = [kandeld[-2]['high'], kandeld[-2]['low'], kandelw[-1]['high'], kandelw[-1]['low'], kandelw[-2]['high'],
             kandelw[-2]['low'], kande4h[-2]['high'], kande4h[-2]['low'], kande1h[-2]['high'], kande1h[-2]['low']]
    price = mt5.symbol_info_tick(symbol).ask
    line = []
    for i in lines:
        if i > price:
            line.append(i)
    if len(line) == 0:
        return False
    else:
        return min(line)


def kijun_sen(symbol, timeframe, num):
    kandels = kandel(timeframe=timeframe, limit=num, symbol=symbol)
    high = []
    low = []
    i = -1
    for n in range(num):
        high.append(kandels[i]['high'])
        low.append(kandels[i]['low'])
        i -= 1
    mini = min(low)
    maxi = max(high)
    sen = (maxi + mini) / 2
    return sen


def kijun_sen_befor(symbol, timeframe, num):
    x = num + 2
    kandels = kandel(timeframe=timeframe, limit=x, symbol=symbol)
    high = []
    low = []
    i = -3
    for n in range(num):
        high.append(kandels[i]['high'])
        low.append(kandels[i]['low'])
        i -= 1
    mini = min(low)
    maxi = max(high)
    sen = (maxi + mini) / 2
    return sen


def get_ema_20(symbol, start_date, end_date, interval='1d'):
    # Fetch historical data
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)

    # Check if data was fetched
    if data.empty:
        print("No data fetched. Please check the symbol and date range.")
        return None

    # Calculate the 20-period EMA
    data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()

    return data

def ema20(timeframe, symbol):
    ohlc = kandel(timeframe, 20 * 10, symbol=symbol)
    prices = pd.DataFrame(ohlc[:])
    prices['ema'] = prices['close'].ewm(span=20).mean()
    ema = prices['ema'].values.tolist()
    try:
        return (ema)[-1]
    except:
        return (ema)


def ema50(timeframe, symbol):
    ohlc = kandel(timeframe, 50 * 10, symbol=symbol)
    prices = pd.DataFrame(ohlc[:])
    prices['ema'] = prices['close'].ewm(span=50).mean()
    ema = prices['ema'].values.tolist()
    return (ema)[-1]


def ema100(timeframe, symbol):
    ohlc = kandel(timeframe, 100 * 10, symbol=symbol)
    prices = pd.DataFrame(ohlc[:])
    prices['ema'] = prices['close'].ewm(span=100).mean()
    ema = prices['ema'].values.tolist()
    return (ema)[-1]


def ema200(timeframe, symbol):
    ohlc = kandel(timeframe, 200 * 10, symbol=symbol)
    prices = pd.DataFrame(ohlc[:])
    prices['ema'] = prices['close'].ewm(span=200).mean()
    ema = prices['ema'].values.tolist()
    return (ema)[-1]


def ema(timeframe, window, symbol):
    ohlc = kandel(timeframe, window * 10, symbol=symbol)
    prices = pd.DataFrame(ohlc[:])
    prices['ema'] = prices['close'].ewm(span=window).mean()
    ema = prices['ema'].values.tolist()
    return (ema)[-1]


def ema_all(timeframe, window, symbol):
    ohlc = kandel(timeframe, window * 10, symbol=symbol)
    prices = pd.DataFrame(ohlc[:])
    prices['ema'] = prices['close'].ewm(span=window).mean()
    ema = prices['ema'].values.tolist()
    return ema


# --------------------------------------------------------------------------------
def ema_cross(symbol, timeframe, ema1, ema2):
    if \
            ema_all(timeframe, ema1, symbol)[-2] < ema_all(timeframe, ema2, symbol)[-2] \
                    and ema_all(timeframe, ema1, symbol)[-1] > ema_all(timeframe, ema2, symbol)[-1]:

        return "down to up"

    elif \
            ema_all(timeframe, ema1, symbol)[-2] > ema_all(timeframe, ema2, symbol)[-2] \
                    and ema_all(timeframe, ema1, symbol)[-1] < ema_all(timeframe, ema2, symbol)[-1]:

        return "up to down"

    else:
        return False


def modify_position(ticket, new_stop_loss):
    position = mt5.positions_get(ticket=ticket)
    if not position:
        return False

    position = position[0]

    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": position.ticket,
        "sl": new_stop_loss,
        "tp": position.tp,
        "symbol": position.symbol,
        "type": position.type,
        "volume": position.volume,
    }

    result = mt5.order_send(request)


tokyo = check_time(0, 8)
londen = check_time(7, 15)
new_york = check_time(13, 19)
sydney = check_time(22, 5)

buy = mt5.ORDER_TYPE_BUY
sell = mt5.ORDER_TYPE_SELL
