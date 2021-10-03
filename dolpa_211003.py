
import time
import pyupbit
import datetime
import pandas as pd
import numpy as np
import requests
import pause


access = "bbZGbVfCJ4xvm3wja3NU7wPUmurynDhbLeEPlfll"     
secret = "S2ksETmtVg4S5Pawqzy6WdIphBzhucVbVPHPRiYR"     
upbit = pyupbit.Upbit(access, secret)                   

now = datetime.datetime.now()
print(now)



def hpr_top_coin(n):
    try:
        ticker = pyupbit.get_tickers("KRW")
        for i in len(ticker) :
            df = pyupbit.get_ohlcv(ticker[i])
            #df = df['2021']
            df = df.loc['2021-10']
            df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
            df['range'] = (df['high'] - df['low']) * 0.5
            df['target'] = df['open'] + df['range'].shift(1)
            df['bull'] = df['open'] > df['ma5']
            fee = 0.0032
            df['ror'] = np.where((df['high'] > df['target']) & df['bull'],
            df['close'] / df['target'] - fee, 1)
            df['hpr'] = df['ror'].cumprod()
            df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
            return df['hpr'][-2]
    except:
        return 1


def get_hpr_top_coin(n) :

    tickers = pyupbit.get_tickers("KRW")
    hprs = []
    for ticker in tickers:
        hpr = hpr_top_coin(ticker)
        hprs.append((ticker, hpr))
        time.sleep(0.1)
    append_hprs = sorted(hprs, key=lambda x:x[1], reverse=True)
    A = hprs[:n]
    A = [x[0] for x in A] 
    return A
    

def money_top_coin(n):
    coin_list = []
    tickers = pyupbit.get_tickers(fiat="KRW")
    market_code = ','.join(tickers)
    url = "https://api.upbit.com/v1/ticker"
    params = {"markets": market_code}
    response = requests.get(url, params=params).json()
    for info in response:
        coin_list.append([info['market'], info['acc_trade_price_24h']])
    coin_list.sort(key=lambda x: x[1], reverse=True)
    top_k_list = []
    for i in coin_list:
        top_k_list.append(i[0])
        time.sleep(0.1)
    return top_k_list[:n]

def get_money_top_coin(n) :
    B = money_top_coin(n)
    return B

def get_trading_coin(n) :
    A = get_hpr_top_coin(n)
    B= get_money_top_coin(n)
    SetList1 = set(A)
    SetList2 = set(B)
    C = list((SetList2.difference(SetList1)))
    ticker = A + C
    return ticker

trading_coin = get_trading_coin(15)
ticker = trading_coin

now = datetime.datetime.now()
print(now)


cash = 100000
K = 0.1
lost_cut  = 0
profit_cut = 0
target_buy = 0
lost_buy = 0


now = datetime.datetime.now()
delta_5min = datetime.timedelta(minutes = -5)
delta_1day = datetime.timedelta(days = 1)

start_time = datetime.datetime(now.year, now.month, now.day, 8, 55, 0)
end_time = datetime.datetime(now.year, now.month, now.day, 8, 59, 59)

start_time2 = datetime.datetime(now.year, now.month, now.day, 9, 0, 0)
end_time2 = datetime.datetime(now.year, now.month, now.day, 8, 59, 59) + delta_1day + delta_5min

print(now)
print(start_time)
print(end_time) 

print(start_time2)
print(end_time2) 



while True :

        
    for i in range( len(ticker) ) : 


        try :

            current_price = pyupbit.get_current_price(ticker[i])
            balance = float(upbit.get_balance( ticker[i].split('-')[1] ))
            amount = float(balance * current_price)
            average_price = float(upbit.get_avg_buy_price(ticker[i]))

            T = time.strftime('[%m-%d %H:%M:%S]')    
            now = datetime.datetime.now()



            if start_time < now < end_time :

                for i in range( len(ticker) ) : 

                    T = time.strftime('[%m-%d %H:%M:%S]')

                    if amount >= 5025 :
                        upbit.sell_market_order(ticker[i], balance)
                        i += i
                        time.sleep(2) 

                    elif i > len(ticker) : 
                        time.sleep(1) 
                        exit

                time.sleep(1) 
                pause.until(datetime.datetime(now.year, now.month, now.day, 8, 59, 59))


            else :
                
                bit_df = pyupbit.get_ohlcv("KRW-BTC", interval = 'day', count = 2) 
                bit_open_price = bit_df.iloc[-1]['open']
                bit_current_price = pyupbit.get_current_price("KRW-BTC")
                bit_con = bit_current_price - bit_open_price
                bit_con_per = (bit_current_price - bit_open_price)/bit_current_price * 100
                bit_df = pyupbit.get_ohlcv("KRW-BTC", interval = 'day', count = 7) 
                bit_ma5 = bit_df['close'].rolling(window=5).mean()
                bit_df = pyupbit.get_ohlcv("KRW-BTC", interval = 'minute30', count = 7) 
                bit_min30_ma5 = bit_df['close'].rolling(window=5).mean()
                bit_df = pyupbit.get_ohlcv("KRW-BTC", interval = 'minute5', count = 7) 
                bit_min5_ma5 = bit_df['close'].rolling(window=5).mean()
                
                

                for i in range( len(ticker) ) : 

                    T = time.strftime('[%m-%d %H:%M:%S]')    

                    df = pyupbit.get_ohlcv(ticker[i], interval = 'day', count = 10)
                    volatility = (df.iloc[-2]['high'] - df.iloc[-2]['low'])
                    target_price = df.iloc[-1]['open'] + volatility * K
                    open_price = df.iloc[-1]['open']
                    
                    time.sleep(0.1) 

                    df = pyupbit.get_ohlcv(ticker[i], interval = 'day', count = 10)
                    ma5 = df['close'].rolling(window=5).mean() 
                    df = pyupbit.get_ohlcv(ticker[i], interval = 'minute60', count = 10)
                    min60_ma5 = df['close'].rolling(window=5).mean()
                    df = pyupbit.get_ohlcv(ticker[i], interval = 'minute5', count = 10)
                    min5_ma5 = df['close'].rolling(window=5).mean()

                    current_price = pyupbit.get_current_price(ticker[i])
                    balance = float(upbit.get_balance( ticker[i].split('-')[1] ))
                    amount = float(balance * current_price)
                    average_price = float(upbit.get_avg_buy_price(ticker[i]))

                    profit = (balance * current_price) - (balance * average_price)
                    
                    if (balance * current_price) > 0.0 :
                        per_profit = ( profit / (balance * average_price) ) * 100
                    else :
                        per_profit = 0.0

                    
                    if (bit_min30_ma5[-1] < bit_current_price) and (bit_min5_ma5[-1] < bit_current_price) :
                    
                        if (current_price >= target_price) : 
                        
                            if (current_price >= ma5[-1] ) and  (current_price >= min60_ma5[-1] ) and (current_price >= min5_ma5[-1] ) :
                            
                                if target_buy == 0 and amount == 0 :
                                    upbit.buy_market_order(ticker[i], cash)
                                    target_buy == 1

                                elif target_buy == 1 and (cash - amount) >= 5025 and (current_price >= average_price) :    
                                    amount = float(balance * current_price)
                                    upbit.buy_market_order(ticker[i], cash - amount)
                                    target_buy == 1
                                    

                    else : 
                    
                        if (current_price >= target_price) : 
                        
                            if (current_price >= ma5[-1] ) and  (current_price >= min60_ma5[-1] ) and (current_price >= min5_ma5[-1] ) :
                            
                                if target_buy == 0 and amount == 0 :
                                    upbit.buy_market_order(ticker[i], cash*1.2)
                                    target_buy == 1
                                    

                                elif target_buy == 1 and (cash - amount) >= 5025 and (current_price >= average_price) :    
                                    amount = float(balance * current_price)
                                    upbit.buy_market_order(ticker[i], cash*1.2 - amount)
                                    target_buy == 1
                                    

                    if current_price <= min60_ma5[-1] or current_price <= min5_ma5[-1] : 
                    
                        if lost_cut == 0 and current_price <= (average_price*0.95) : 
                        
                            if amount >= 50000 : 
                                balance = float(upbit.get_balance( ticker[i].split('-')[1] ))
                                upbit.sell_market_order(ticker[i], balance*0.5) 
                                lost_cut == 1

                            else :
                                balance = float(upbit.get_balance( ticker[i].split('-')[1] ))
                                upbit.sell_market_order(ticker[i], balance) 
                                lost_cut == 0

                        if lost_cut == 1 and current_price <= (average_price*0.95) : 
                                balance = float(upbit.get_balance( ticker[i].split('-')[1] ))
                                upbit.sell_market_order(ticker[i], balance) 
                                lost_cut == 0
                    else :
                        exit



                    if profit_cut == 0 and per_profit >= 3.0 and (current_price >= ma5[-1] >= ma5[-2]) and (current_price >= min5_ma5[-1] >= min5_ma5[-2] ):
                        if df.iloc[-1]['high'] == current_price :  
                            profit_cut = 0
                        else : 
                            balance = float(upbit.get_balance( ticker[i].split('-')[1] ))
                            upbit.sell_market_order(ticker[i], balance*0.3)

                            amount = float(balance * current_price)
                            upbit.buy_market_order(ticker[i], cash*1.5 - amount)
                            profit_cut = 1

                    elif profit_cut == 1 and per_profit >= 5 and (current_price >= ma5[-1] >= ma5[-2]) and (current_price >= min5_ma5[-1] >= min5_ma5[-2] ):
                        if df.iloc[-1]['high'] == current_price :  
                            profit_cut = 1

                        else :
                            amount = float(balance * current_price)
                            upbit.sell_market_order(ticker[i], balance)
                            profit_cut = 0


        except Exception as e:
            print(e)
            time.sleep(1)