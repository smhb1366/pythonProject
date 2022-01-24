#%%

from datetime import datetime
from time import time
from pybit import HTTP
import pandas as pd
from ta.volatility import AverageTrueRange

#%%
StartAll = time()
start = time()
# side = 'Buy'
side = 'Sell'
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
karid = False
# karid = True
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Risk = 2
USD = 1000
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Mohasebie Zaman )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def zaman(zaman,dore):
    startTime = datetime.timestamp(zaman)
    if type(dore)==int:
        st = startTime-190*60*dore
    elif dore=='D':
        st = startTime-190*86400
    st = str(int(st))
    return st,dore

st,interval_asl = zaman(datetime.now(),1)
end = time()
print(f'(1){end-start:.^10}')
#%%
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Mohasebie Etlaat  )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
start=time()

def etlaat(zaman,dore):
    global session
    session = HTTP("https://api-testnet.bybit.com",
                   api_key="qBpP1YrhKM6wWEHmJ7",
                   api_secret="KI7GkmQ5cfMWBc4V9E70ew1v83WvfD1RbjMX")
    df = pd.DataFrame(session.query_kline(
        symbol="BTCUSDT",
        interval=dore,
        from_time=zaman
    )['result'])

    df['dddd'] = pd.to_datetime(df.start_at,unit='s')
    df['ATR'] = round(AverageTrueRange(window=14,high=df.high,low=df.low,close=df.close).average_true_range(),2)

    close_last = df.iloc[-1,-4]
    ATR = df.iloc[-1,-1]
    return close_last,ATR

close_last,ATR = etlaat(st,interval_asl)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Mohasebie Stop_Loss )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
if (side == 'Buy'):
    stop_loss = close_last - 2*ATR
elif (side == 'Sell'):
    stop_loss = close_last + 2*ATR
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
      f'qty_cal    = {qty_cal:-^30}')
end=time()
print(f'(2){end-start:.^10}')
#%%
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( set_leverage )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
start=time()
session.set_leverage(
    symbol="BTCUSDT",
    buy_leverage=leverage,
    sell_leverage=leverage
)
end=time()
print(f'(3){end-start:.^10}')
#%%
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Barasie Order )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
start=time()
with open(r"C:\Users\smhb1366\Desktop\pythonProject\Bybit\qty.text",'r') as aa:
    qty = float(aa.read())
with open(r"C:\Users\smhb1366\Desktop\pythonProject\Bybit\SellAndBuy.text",'r') as aa:
    SellAndBuy = aa.read()

if SellAndBuy=='Buy':
    SellAndBuy='Sell'
elif SellAndBuy=='Sell':
    SellAndBuy='Buy'
else:
    print(' Moamele Baz Nadashtim ')
end=time()
print(f'(4){end-start:.^10}')
#%%
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Close Order )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
start=time()
if qty>0:
    session.place_active_order(
        symbol="BTCUSDT",
        side=SellAndBuy,
        order_type="Market",
        qty=qty,
        # price=30000,
        time_in_force="GoodTillCancel",
        reduce_only=True,
        close_on_trigger=False)

    with open(r"C:\Users\smhb1366\Desktop\pythonProject\Bybit\qty.text",'w') as aa:
        aa.write(str(0))
    with open(r"C:\Users\smhb1366\Desktop\pythonProject\Bybit\SellAndBuy.text",'w') as aa:
        aa.write(str(0))
end=time()
print(f'(5){end-start:.^10}')
#%%
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^( Close Order )^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
start=time()
if karid == True :
    order = session.place_active_order(
        symbol="BTCUSDT",
        side=side,
        order_type="Market",
        qty=qty_cal,
        # price=30000,
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

    with open(r"C:\Users\smhb1366\Desktop\pythonProject\Bybit\qty.text",'w') as tt:
        tt.write(str(qty))
    with open(r"C:\Users\smhb1366\Desktop\pythonProject\Bybit\SellAndBuy.text",'w') as tt:
        tt.write(str(SellAndBuy))
end=time()
print(f'(6){end-start:.^10}')
#%%
EndAll = time()
print(f'All = {EndAll-StartAll:.^10}')

