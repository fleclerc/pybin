# %% setup
%load_ext autoreload
%autoreload 2
from numpy import NaN
import pandas as pd
import pymongo
from datetime import datetime
# Establish connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.binance
print(db.depth.estimated_document_count())
print(db.trades.estimated_document_count())
print(db.longshort.estimated_document_count())

# %% print trades
from mongo_helper import test 
print(test())
for entry in db.trades.find().limit(2):
    print (entry)

# %%
from mongo_helper import buildTradesPeriodTable
buildTradesPeriodTable(db, 'minute')

# %% graph data preparation functions
def loadLongShortGraphData(db, symbol):
    from mongo_helper import prepareLongShortData
    data = pd.json_normalize(list(prepareLongShortData(db, symbol)))
    lsdf = pd.DataFrame(data)
    print(lsdf.head())
    print(lsdf.dtypes)
    return lsdf

def loadTradesGraphData(db, symbol, period):
    collection = f"trades_{period}"
    data2 = pd.json_normalize(list(db.get_collection(collection).find({"_id.symbol": symbol}, {'_id' : 0})))
    tradesdf = pd.DataFrame(data2)
    print(tradesdf.head())
    print(tradesdf.dtypes)
    return tradesdf

# %% plot function
def plot(lsdf, tradesdf):
    import matplotlib.pyplot as plt
    plt.rcParams['figure.figsize'] = [20, 10]    
    from mpl_toolkits.axes_grid1 import host_subplot
    from mpl_toolkits import axisartist

    host = host_subplot(111, axes_class=axisartist.Axes)
    plt.subplots_adjust(right=0.75)

    par1 = host.twinx()
    par2 = host.twinx()
    #ax2 = host.add_subplot( 111, sharex = par1, frameon = False )

    par2.axis["right"] = par2.new_fixed_axis(loc="right", offset=(60, 0))
    par1.axis["right"].toggle(all=True)
    par2.axis["right"].toggle(all=True)

    p1, = host.plot(lsdf["timestamp"], lsdf["global.longShortRatio"])
    p2, = host.plot(lsdf["timestamp"], lsdf["top.longShortRatio"])
    p4, = par1.plot(tradesdf["timestamp"], tradesdf["minPrc"])
    p5, = par1.plot(tradesdf["timestamp"], tradesdf["maxPrc"])
    p3, = par2.plot(tradesdf["timestamp"],tradesdf["volume"])

    par2.set_ylim(0, 20000)

    host.set_xlabel("timestamp")
    host.set_ylabel("ratio")
    par1.set_ylabel("price")
    par2.set_ylabel("Volume")
    host.legend(["global", "top", "minPrc", "maxPrc", "volume"])

    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    par2.axis["right"].label.set_color(p3.get_color())

    plt.show()

# %% load data for graph
lsdf = loadLongShortGraphData(db, "BTCUSDT")
tradesdf = loadTradesGraphData(db, "BTCUSDT", "minute")


# %% plot
plot(lsdf, tradesdf)

# %%

        
for entry in db.trades1m.find({"_id.symbol": "BTCUSDT"}):
    print(entry)
    break

# %%

