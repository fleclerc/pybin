import logging
import logging.config

from time import sleep
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from datetime import datetime
from db import dataset



def setupLogging():
    import yaml
    from yaml import Loader, Dumper
    cfg = yaml.load(open('logging.yml').read(), Loader=Loader)
    logging.config.dictConfig(cfg)


request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
def saveLongShort():
    glob = request_client.get_global_long_short_accounts(symbol="BTCUSDT", period='5m', limit=1)
    top = request_client.get_top_long_short_accounts(symbol="BTCUSDT", period='5m', limit=1)
    logger.info(f"saveLongShort {datetime.fromtimestamp(glob[0]['timestamp']/1000.0)}")
    dataset.insert_one({'global': glob, 'top': top})


setupLogging()
logger = logging.getLogger('pybin.main')
logger.info(f'info {logger.getEffectiveLevel()}')
import schedule
schedule.every(5).seconds.do(saveLongShort)

while True:
    schedule.run_pending()
    sleep(1)
