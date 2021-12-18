# %% setup
import pymongo
from datetime import datetime
# Establish connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Create a database
db = client.binancetest
print(db.depth.count_documents({}))
print(db.trades.count_documents({}))
print(db.longshort.count_documents({}))

# %%
db.createCollection(
    "tradests",
  {
       "timeseries": {
          "timeField": "eventTime",
       }
    }
)

# %%
for entry in db.trades.find():
    entry["eventTime"] = datetime.fromtimestamp(entry["eventTime"]/1000.0)
    db.tradests.insert_one(entry)

# %%
pipeline = [
    { "$sort" : { "eventTime" : 1 } },
    {"$addFields": {
       "t": "$eventTime",
       "dt": { "$toDate": "$eventTime" },
      "date": {"$dateToParts": {"date": { "$toDate": { "$toDate": "$eventTime" } } } }
       }
   }]
# %%
pipeline.append(
   {
      "$group": {
         "_id": {
            "date": {
               "year": "$date.year",
               "month": "$date.month",
               "day": "$date.day",
               "hour": "$date.hour",
               "minute": "$date.minute",
            }
         },
         "minPrc": { "$min": "$price" },
         "maxPrc": { "$max": "$price" }
      }
   }
)

# %%
for entry in db.trades.aggregate(pipeline):
    print (entry)
    

# %%  print depth
for entry in db.depth.find():
    print(entry)
    break

# %%  print trades
#db.trades.drop()
for entry in db.trades.find():
    print(entry)
    break

# %%  print longshort
for entry in db.longshort.find():
    print(entry)
    break

# %%
prev = None
gdiff = []
tdiff = []
for entry in db.longshort.find().sort( [( "global.timestamp", 1 )] ):
    if not prev: 
        prev = entry
    gls = entry["global"]["longShortRatio"]
    tls = entry["top"]["longShortRatio"]
    pgls = prev["global"]["longShortRatio"]
    ptls = prev["top"]["longShortRatio"]
    gdiff.append(float(gls)-float(pgls))
    tdiff.append( float(tls)-float(ptls))
    #timestamp = entry["timestamp"][0] if isinstance(entry["timestamp"], list) else entry["timestamp"]
    timestamp = entry["timestamp"]
    print (datetime.fromtimestamp(float(timestamp)/1000.0))
print (f"global min: {min(gdiff)} max: {max(gdiff)}   top min: {min(tdiff)} max: {max(tdiff)}" )

# %%
import pandas as pd
data = pd.json_normalize(list(db.longshort.find().sort( [( "timestamp", 1 )] )))
data2 = pd.json_normalize(list(db.trades.find()))
#'global',
#['timestamp', 'longShortRatio']
#)
#print(data.head())
pd.date_range
df = pd.DataFrame(data)
df['global.longShortRatio'] = pd.to_numeric(df['global.longShortRatio'],errors='coerce')
df['top.longShortRatio'] = pd.to_numeric(df['top.longShortRatio'],errors='coerce')
print(df.plot("timestamp", ["global.longShortRatio", "top.longShortRatio"]))

# %%
for entry in db.longshort.aggregate([
   { "$addFields": { "globalx": { "$first": "$global" } } }
]):
    print(entry)
    break


#%%

# Create a database
db2 = client.classDB.binance
print(db2.count_documents({}))

db3 = client.newDB
db3.longshort.insert(db.longshort.find({}))
db3.longshort.insert(db2.find({}))
print(db3.longshort.count_documents({}))

# %%
db3.longshort.drop()
# %%
print(db3.longshort.count_documents({}))

# %%  print longshort
for entry in db3.longshort.find():
    print(entry)
    break

#%%
db3.longshort.update_many( {"timestamp" : { "$type": "array" }},
  [
    { "$set": { "timestamp": { "$first" : "$timestamp" }
        }
    }
  ]
)

# %%
