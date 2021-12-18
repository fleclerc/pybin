# %% setup
from numpy import NaN
import pandas as pd
import pymongo
from datetime import datetime
# Establish connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Create a database
db = client.binance
print(db.depth.count_documents({}))
print(db.trades.count_documents({}))
print(db.longshort.count_documents({}))

# %% print trades
for entry in db.trades.find().limit(10):
    print (entry)

# %% build pipeline
def pipeline_prepare():
    return {"$addFields": {
       "t": "$eventTime",
       "dt": { "$toDate": "$eventTime" },
      "date": {"$dateToParts": {"date": { "$toDate": { "$toDate": "$eventTime" } } } }
       }
   }
def pipeline_group(to):
    base = {
        "year": "$date.year",
        "month": "$date.month",
        "day": "$date.day",
    }
    if to in ("hour", "minute", "second"): 
        base["hour"] = "$date.hour"
    if to in ("minute", "second"): 
        base["minute"] = "$date.minute"
    if to == "second":
        base["second"] = "$date.second"
    return {
        "$group": {
            "_id": {
                "date": base
            },
            "minPrc": { "$min": "$price" },
            "maxPrc": { "$max": "$price" },
            "volume" : {"$sum" : "$qty"},
            "timestamp" : { "$min" : { "$toDate": "$eventTime" }}
        }
    }

def pipeline_sortBy(sortBy):
    return { "$sort" : { sortBy : 1 } }

def pipeline_out(collection):
    return { "$out" : collection }

# %%
pipeline = []
pipeline.append( pipeline_prepare())
pipeline.append(pipeline_group("minute"))
pipeline.append(pipeline_sortBy("timestamp"))
pipeline.append(pipeline_out("trades1m"))
print(pipeline)
for entry in db.trades.aggregate(pipeline):
    print (entry)

# %%
print (db.trades1m.count_documents({}))
for entry in db.trades1m.find().limit(10):
    print (entry)

# %% load data long short
longshort_pipeline = [
    {
        '$project': {
            'global.longShortRatio': 1, 
            'top.longShortRatio': 1, 
            'timestamp': 1, 
            '_id': 0
        }
    }, {
        '$sort': {
            'timestamp': 1
        }
    }, {
        '$set': {
            'global.longShortRatio': {
                '$toDouble': '$global.longShortRatio'
            }, 
            'top.longShortRatio': {
                '$toDouble': '$top.longShortRatio'
            }, 
            'timestamp': {
                '$toDate': {"$add" : ['$timestamp' , 1]}
            }

        }
    }
]

# %%
for entry in db.longshort.aggregate(longshort_pipeline):
    print (entry)
    break

# %% load data long short
data = pd.json_normalize(list(db.longshort.aggregate(longshort_pipeline)))
lsdf = pd.DataFrame(data)
print(lsdf.head())
print(lsdf.dtypes)

# %% load data trades
data2 = pd.json_normalize(list(db.trades1m.find({}, {'_id' : 0})))
tradesdf = pd.DataFrame(data2)
print(tradesdf.head())
print(tradesdf.dtypes)

# %% plot
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [15, 8]
ax = lsdf.plot("timestamp", ["global.longShortRatio", "top.longShortRatio"])
tradesdf.plot("timestamp", ["minPrc", "maxPrc"], secondary_y=True, ax=ax)

# %% plot
import matplotlib.pyplot as plt
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

host.set_xlabel("timestamp")
host.set_ylabel("ratio")
par1.set_ylabel("price")
par2.set_ylabel("Volume")
host.legend(["global", "top", "minPrc", "maxPrc", "volume"])

host.axis["left"].label.set_color(p1.get_color())
par1.axis["right"].label.set_color(p2.get_color())
par2.axis["right"].label.set_color(p3.get_color())

plt.show()



#tradesdf.plot("timestamp", ["volume"], kind='bar')

# %% plot
#fig, ax = plt.subplots(figsize=(10,8))
#df.drop('Volume', axis=1).plot(ax=ax)
#ax.legend(loc='best')
#ax2.set_ylim([0, ax2.get_ylim()[1] * 10])
#ax2.legend(loc='best')


# %%
