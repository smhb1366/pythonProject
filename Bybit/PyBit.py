from pybit import HTTP
session = HTTP("https://api-testnet.bybit.com",
               api_key="qBpP1YrhKM6wWEHmJ7",
               api_secret="KI7GkmQ5cfMWBc4V9E70ew1v83WvfD1RbjMX")
#%%

# try:
#     print(session.place_active_order(
#         symbol="BTCUSDT",
#         side="Buy",
#         order_type="Limit",
#         qty=0.01,
#         price=41750,
#         time_in_force="GoodTillCancel",
#         reduce_only=False,
#         close_on_trigger=False,
#         stop_loss=41600
#     ))
# except:
#     print('vasl nashod')
#%%

