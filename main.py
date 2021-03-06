import logging
import logging.config
from re import sub

from time import sleep
from binance_f import RequestClient, SubscriptionClient
from binance_f.model import *
from binance_f.constant.test import *
from binance_f.base.printobject import *
from datetime import datetime
from db import db
from binance_f.exception.binanceapiexception import BinanceApiException
import traceback

def setupLogging():
    import yaml
    from yaml import Loader, Dumper
    cfg = yaml.load(open('logging.yml').read(), Loader=Loader)
    logging.config.dictConfig(cfg)


class DepthSubscription:
    def __init__(self):
        self.sub_client = sub_client = SubscriptionClient(api_key=g_api_key, secret_key=g_secret_key)
        self.count = 0

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.sub_client.unsubscribe_all()
        return self

    def subscribeDepth(self):
        def error(e: 'BinanceApiException'):
            logger.error(e.error_code + e.error_message)
            traceback.print_exc()

        def depthCallback(data_type: 'SubscribeMessageType', event: 'any'):
            if data_type == SubscribeMessageType.RESPONSE:
                logger.info(f"RESPONSE - Event ID: {event}")
            elif  data_type == SubscribeMessageType.PAYLOAD:
                self.count += 1
                if self.count % 50 == 0:
                    logger.info(f"{self.count} depth events processed")
                db.depth.insert_one(event)
            else:
                logger.error("???")

        self.sub_client.subscribe_book_depth_event("btcusdt", 10, depthCallback, error, update_time=UpdateTime.NORMAL)
        self.sub_client.subscribe_book_depth_event("ethusdt", 10, depthCallback, error, update_time=UpdateTime.NORMAL)

class TradesSubscription:
    def __init__(self):
        self.sub_client = sub_client = SubscriptionClient(api_key=g_api_key, secret_key=g_secret_key)
        self.count = 0

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.sub_client.unsubscribe_all()
        return self

    def subscribeTrades(self):
        def error(e: 'BinanceApiException'):
            logger.error(e.error_code + e.error_message)
            traceback.print_exc()

        def callback(data_type: 'SubscribeMessageType', event: 'any'):
            if data_type == SubscribeMessageType.RESPONSE:
                logger.info(f"RESPONSE - Event ID: {event}")
            elif  data_type == SubscribeMessageType.PAYLOAD:
                self.count += 1
                if self.count % 50 == 0:
                    logger.info(f"{self.count} trades events processed")
                doc = event.toJSON()
                db.trades.insert_one(doc)
            else:
                logger.error("???")

        self.sub_client.subscribe_aggregate_trade_event("btcusdt", callback, error)
        self.sub_client.subscribe_aggregate_trade_event("ethusdt", callback, error)

class LiquidationSubscription:
    def __init__(self):
        self.sub_client = sub_client = SubscriptionClient(api_key=g_api_key, 
        secret_key=g_secret_key, receive_limit_ms=60*60*1000)
        self.count = 0

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.sub_client.unsubscribe_all()
        return self

    def subscribeLiquidations(self):
        def error(e: 'BinanceApiException'):
            logger.error(e.error_code + e.error_message)
            traceback.print_exc()

        def callback(data_type: 'SubscribeMessageType', event: 'any'):
            try:
                if data_type == SubscribeMessageType.RESPONSE:
                    logger.info(f"RESPONSE - Event ID: {event}")
                elif  data_type == SubscribeMessageType.PAYLOAD:
                    self.count += 1
                    logger.info(f"{self.count} liquidation events processed")
                    doc = event.toJSON()
                    db.liquidations.insert_one(doc)
                else:
                    logger.error("???")
            except Exception as ex:
                logger.error(str(ex))

        self.sub_client.subscribe_symbol_liquidation_event("btcusdt", callback, error)
        self.sub_client.subscribe_symbol_liquidation_event("ethusdt", callback, error)

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
def saveLongShort(symbol):
    glob = request_client.get_global_long_short_accounts(symbol=symbol, period='5m', limit=1)
    top = request_client.get_top_long_short_accounts(symbol=symbol, period='5m', limit=1)
    logger.info(f"saveLongShort {datetime.fromtimestamp(glob[0]['timestamp']/1000.0)}")
    db.longshort.insert_one({'symbol': symbol, 'timestamp': glob[0]['timestamp'], 'global': glob[0], 'top': top[0]})


setupLogging()
logger = logging.getLogger('pybin.main')
logger.info(f'info {logger.getEffectiveLevel()}')
import schedule
schedule.every(5).minutes.do(lambda : saveLongShort("BTCUSDT"))
schedule.every(5).minutes.do(lambda : saveLongShort("ETHUSDT"))

with DepthSubscription() as d, TradesSubscription() as t, LiquidationSubscription() as l:
    d.subscribeDepth()
    t.subscribeTrades()
    l.subscribeLiquidations()
    while True:
        schedule.run_pending()
        try:
            sleep(1)
        except KeyboardInterrupt:
            logger.info("done")
            raise

logger.info("exiting")