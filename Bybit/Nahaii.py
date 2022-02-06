#%%

from datetime import datetime
from time import time
from time import sleep
import os
from pybit import HTTP
import pandas as pd
from ta.volatility import AverageTrueRange
from tkinter import *
import requests

session = HTTP("https://api-testnet.bybit.com",
               api_key="qBpP1YrhKM6wWEHmJ7",
               api_secret="KI7GkmQ5cfMWBc4V9E70ew1v83WvfD1RbjMX")
sahm = ['BTCUSDT','ETHUSDT','SOLUSDT']
#----------------------------------------------------------------
#%%
root = Tk()
root.config(bg='#84a4f3')
# root.geometry('700x200')
root.resizable(width=False,height=False)
#---------------------------------------------------------------
A = Frame(root,bg='#f3d384')
A.grid(padx=10,pady=10,row=0,column=0)
B = Frame(root,bg='#f3d384')
B.grid(padx=10,pady=10,row=1,column=0)
C = Frame(root,bg='#84a4f3')
C.grid(padx=10,pady=10,row=3,column=0)
D = Frame(root,bg='#84a4f3')
D.grid(padx=10,pady=10,row=4,column=0)

Label(A,text='Risk',font=('Arial',10),bg='#f3d384').grid(padx=10,pady=10,row=0,column=0)
Risk = Entry(A,borderwidth=3,font=('Arial 11 bold'),justify='center')
Risk.grid(padx=10,pady=10,row=1,column=0)
Risk.insert(0,'5')
#----------------------------------
Label(A,text='USD $',font=('Arial',10),bg='#f3d384').grid(padx=10,pady=10,row=0,column=1)
USD = Entry(A,borderwidth=3,font=('Arial 11 bold'),justify='center')
USD.grid(padx=10,pady=10,row=1,column=1)
USD.insert(0,1000)
#------------------------------------
Label(A,text='interval_asl',font=('Arial',10),bg='#f3d384').grid(padx=10,pady=10,row=0,column=2)
interval_asl = Entry(A,borderwidth=3,font=('Arial 11 bold'),justify='center')
interval_asl.grid(padx=10,pady=10,row=1,column=2)
interval_asl.insert(0,5)
#---------------------------------------------------------------
x = IntVar()
xx = StringVar()
def name():
    symbolll = sahm[int(x.get())]
    return symbolll
for index in range(len(sahm)):
    R = Radiobutton(B,font=('Arial 12 bold'),text=sahm[index],variable=x,value=index,bg='#f3d384')
    R.grid(padx=10,pady=10,row=0,column=(index))

#***************************************************************
def Egrae_Asly(side,kharid,Risk,USD,interval_asl):
    StartAll = time()
    start = time()
    # side = 'Buy'
    side = side
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    kharid = kharid
    # kharid = True
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Risk = Risk
    USD = USD
    interval_asl = interval_asl
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Mohasebie Zaman )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def zaman(zaman,dore):
        startTime = datetime.timestamp(zaman)
        if type(dore)==int:
            st = startTime-2*60*dore
        elif dore=='D':
            st = startTime-2*86400
        st = str(int(st))
        return st

    st = zaman(datetime.now(),interval_asl)
    end = time()
    print(f'-----------{interval_asl}-----------------')
    print(name()[:-1])
    print(f'(1){end-start:.^10}')
    #***************************************************************
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Mohasebie Etlaat  )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    start=time()

    def etlaat(zaman,dore):
        startd = time()
        df = pd.DataFrame(session.query_kline(
            symbol= name(),
            interval=dore,
            limit=2,
            from_time=zaman
        )['result'])
        endd = time()
        df['dddd'] = pd.to_datetime(df.start_at,unit='s')
        startdd = time()
        #-----------------------------------------------------------
        url = f'https://www.alphavantage.co/query?function=ATR&symbol={name()[:-1]}&interval={interval_asl}min&time_period=14&series_type=close&apikey=24H6H312XIX3YT5Y'
        TT = requests.get(url).json()
        ATR = round(float(pd.Series(TT['Technical Analysis: ATR'])[0]['ATR']), 1)
        #-----------------------------------------------------------
        close_last = df['close'].iloc[-1]
        enddd = time()
        print(f'(ByBit)->{endd-startd}-----(alphavantage)->{enddd-startdd}')
        return close_last,ATR

    close_last,ATR = etlaat(st,interval_asl)

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Mohasebie Stop_Loss )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    if (side == 'Buy'):
        stop_loss = close_last - 2.5*ATR
        close_last=close_last
    elif (side == 'Sell'):
        stop_loss = close_last + 2.5*ATR
        close_last = close_last
    else:
        print('side ro vared kon')
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Mohasebie Leverage )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Range = ((abs((close_last-stop_loss))/close_last))*100
    leverage = round(Risk/Range,2)
    if leverage <1 :
        leverage = 1
    qty_cal = round((USD*leverage)/close_last,3)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Nataieg Nahaii )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    print(f'close      = {close_last:-^30}\n'
          f'stop_loss  = {stop_loss:-^30}\n'
          f'leverage   = {leverage:-^30}\n'
          f'hade zarar = {(abs(stop_loss-close_last)/close_last)*100:-^30}\n'
          f'qty_cal    = {qty_cal:-^30}\n'
          f'ATR        = {ATR:-^30}\n'
          f'sarbesar   = {round(leverage*2*0.075,3):-^30}')
    end=time()
    print(f'(2){end-start:.^10}')
    #***************************************************************
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( set_leverage )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    start=time()
    session.set_leverage(
        symbol= name(),
        buy_leverage=leverage,
        sell_leverage=leverage
    )
    end=time()
    print(f'(3){end-start:.^10}')
    #***************************************************************
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Barasie Order )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    start=time()
    with open(rf"{os.getcwd()}\\{name()}qty.text",'r') as aa:
        qty = float(aa.read())
    with open(rf"{os.getcwd()}\\{name()}SellAndBuy.text",'r') as aa:
        SellAndBuy = aa.read()

    if SellAndBuy=='Buy':
        SellAndBuy='Sell'
    elif SellAndBuy=='Sell':
        SellAndBuy='Buy'
    else:
        print(' Moamele Baz Nadashtim ')
    end=time()
    print(f'(4){end-start:.^10}')
    #***************************************************************
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Close Order )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    start=time()
    if qty>0:
        session.place_active_order(
            symbol= name(),
            side=SellAndBuy,
            # order_type="Market",
            order_type="Market",
            qty=qty,
            time_in_force="GoodTillCancel",
            reduce_only=True,
            close_on_trigger=False)

        with open(rf"{os.getcwd()}\\{name()}qty.text",'w') as aa:
            aa.write(str(0))
        with open(rf"{os.getcwd()}\\{name()}SellAndBuy.text",'w') as aa:
            aa.write(str(0))
    end=time()
    print(f'(5){end-start:.^10}')
    #***************************************************************
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Sell/Buy Order )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    start=time()
    if kharid == True :
        order = session.place_active_order(
            symbol= name(),
            side=side,
            order_type="Market",
            qty=qty_cal,
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False,
            stop_loss =stop_loss
        )
        print('ersal shod')
        qty = order["result"]["qty"]
        SellAndBuy = order["result"]["side"]
        print('------------------------')
        print('dariaft shod')

        with open(rf"{os.getcwd()}\\{name()}qty.text",'w') as tt:
            tt.write(str(qty))
        with open(rf"{os.getcwd()}\\{name()}SellAndBuy.text",'w') as tt:
            tt.write(str(SellAndBuy))
    end=time()
    print(f'(6){end-start:.^10}')
    #***************************************************************
    EndAll = time()
    print(f'All = {EndAll-StartAll:.^10}')

#------------------------------------

def Close(Risk=Risk,USD=USD,interval_asl=interval_asl):
    kharid = False
    side = 'Sell'
    Risk = float(Risk.get())
    USD = float(USD.get())
    if interval_asl.get()=='D':
        interval_asl = interval_asl.get()
    else:
        interval_asl = int(interval_asl.get())
    print(kharid, side, Risk, USD, interval_asl)
    Egrae_Asly(side=side,kharid=kharid,Risk=Risk,USD=USD,interval_asl=interval_asl)
    #Label(root, text='Close Anjam Shod !!!!',font=('Arial',10),fg='black',bg='yellow').pack(side=BOTTOM)
    xx.set('Close Anjam Shod !!!!')
#-------------------------------------
def Buy(Risk=Risk,USD=USD,interval_asl=interval_asl):
    kharid = True
    side = 'Buy'
    Risk = float(Risk.get())
    USD = float(USD.get())
    if interval_asl.get()=='D':
        interval_asl = interval_asl.get()
    else:
        interval_asl = int(interval_asl.get())
    print(kharid, side, Risk, USD, interval_asl)
    Egrae_Asly(side=side,kharid=kharid,Risk=Risk,USD=USD,interval_asl=interval_asl)
    #Label(root, text='Buy Anjam Shod !!!!',font=('Arial',10),fg='white',bg='blue').pack(side=BOTTOM)
    xx.set('Buy Anjam Shod !!!!')
#-------------------------------------
def Sell(Risk=Risk,USD=USD,interval_asl=interval_asl):
    kharid = True
    side = 'Sell'
    Risk = float(Risk.get())
    USD = float(USD.get())
    if interval_asl.get()=='D':
        interval_asl = interval_asl.get()
    else:
        interval_asl = int(interval_asl.get())
    print(kharid, side, Risk, USD, interval_asl)
    Egrae_Asly(side=side,kharid=kharid,Risk=Risk,USD=USD,interval_asl=interval_asl)
    #Label(root, text='Sell Anjam Shod !!!!',font=('Arial',10),fg='white',bg='red').pack(side=BOTTOM)
    xx.set('Sell Anjam Shod !!!!')
def clear():
    with open(rf"{os.getcwd()}\\{name()}qty.text",'w') as aa:
        aa.write(str(0))
    with open(rf"{os.getcwd()}\\{name()}SellAndBuy.text", 'w') as aa:
        aa.write(str(0))
    # Label(root, text='Clear Anjam Shod !!!!', font=('Arial', 10), fg='white', bg='black').pack(side=BOTTOM)
    xx.set('Clear Anjam Shod !!!!')
#-------------------------------------
Button(C,text='Buy',padx=20,font=('Arial 11 bold'),pady=10,command=lambda:Buy(),fg='white',bg='blue',width=3).grid(padx=10,pady=10,row=0,column=3)
Button(C,text='Close',padx=20,font=('Arial 11 bold'),pady=10,command=lambda:Close(),fg='black',bg='yellow',width=3).grid(padx=10,pady=10,row=0,column=2)
Button(C,text='Sell',padx=20,font=('Arial 11 bold'),pady=10,command=lambda:Sell(),fg='white',bg='red',width=3).grid(padx=10,pady=10,row=0,column=1)
Button(C,text='Celer',padx=20,font=('Arial 11 bold'),pady=10,command=lambda:clear(),fg='white',bg='black',width=3).grid(padx=10,pady=10,row=0,column=0)
Label(D,textvariable=xx,bg='#84a4f3',font=('Arial 10 bold')).grid(padx=10,pady=10,row=1,column=1)
root.mainloop()
