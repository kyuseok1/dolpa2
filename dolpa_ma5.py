import time
import pyupbit
import datetime

tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-ADA", "KRW-ETC", "KRW-LTC"]

# tickers = pyupbit.get_tickers("KRW")

access = "bbZGbVfCJ4xvm3wja3NU7wPUmurynDhbLeEPlfll"     
secret = "S2ksETmtVg4S5Pawqzy6WdIphBzhucVbVPHPRiYR"     
upbit = pyupbit.Upbit(access, secret)                  


def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def get_yesterday_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()
    return ma[-2]

cash = 1000000 

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

while True:
    

    for ticker in tickers:
        

        try:

            ma5 = get_yesterday_ma5(ticker)          # <class 'numpy.float64'>
            target_price = get_target_price(ticker)  # <class 'numpy.float64'>

            now = datetime.datetime.now()  # <class 'datetime.datetime'>
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)  # <class 'datetime.datetime'>
            plus = mid + datetime.timedelta(seconds=10)  # <class 'datetime.datetime'>


            if mid < now < mid + datetime.timedelta(seconds=10) : 
                target_price = get_target_price(ticker)
                upbit.sell_market_order(ticker, cash)

            # now = datetime.datetime.now()
            # if now.hour == 8 and now.minute == 59 and 50 <= now.second <= 59 :
            
            else : 
                current_price = pyupbit.get_current_price(ticker)
                if (current_price > target_price) and (current_price > ma5):
                    upbit.buy_market_order(ticker, cash)

            
            current_price = pyupbit.get_current_price(ticker)             # <class 'float'>
            average_price = float(upbit.get_avg_buy_price(ticker))        # <class 'float'>
            balance = float(upbit.get_balance(ticker))                    # <class 'float'>
            amount = float(balance * average_price)                       # <class 'float'>
            profit = (amount * current_price) - (amount * average_price)  # <class 'float'>

           

        except:
            print("error!")

        time.sleep(1)

    print('----------------------------------------------------------------------------------------------------------------------------------------')    


