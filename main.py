from time import sleep
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from datetime import datetime
from db import dataset

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

def saveLongShort():
    glob = request_client.get_global_long_short_accounts(symbol="BTCUSDT", period='5m', limit=1)
    top = request_client.get_top_long_short_accounts(symbol="BTCUSDT", period='5m', limit=1)
    print(datetime.fromtimestamp(glob[0]['timestamp']/1000.0))
    dataset.insert_one({'global': glob, 'top': top})


import schedule
schedule.every(5).minutes.do(saveLongShort)

while True:
    schedule.run_pending()
    sleep(1)
