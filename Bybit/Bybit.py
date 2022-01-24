import bybit
import time,datetime
import config

client = bybit.bybit(test=False,api_key='qBpP1YrhKM6wWEHmJ7',api_secret='KI7GkmQ5cfMWBc4V9E70ew1v83WvfD1RbjMX')

print('loggedin')

info = client.Market.Market_symbolInfo().result()

keys = info[0]['result'][0]
for i in keys:
    print(i)
print(keys)

print('------------')
# print(client.Order.Order_new(side='Buy',symbol='BTCUSD',order_type='Limit',qty=0.01,price=10000,time_in_force='GoodTillCancel').result())