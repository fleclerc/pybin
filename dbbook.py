# %% setup
import pymongo
from datetime import datetime
# Establish connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Create a database
db = client.binance
print(db.depth.count_documents({}))
print(db.longshort.count_documents({}))

# %%  print depth
for entry in db.depth.find():
    print(entry)
    break

# %%  print longshort
for entry in db3.longshort.find():
    print(entry)
    break

# %%
prev = None
gdiff = []
tdiff = []
for entry in db.longshort.find().sort( [( "global.timestamp", 1 )] ):
    if not prev: 
        prev = entry
    gls = entry["global"][0]["longShortRatio"]
    tls = entry["top"][0]["longShortRatio"]
    pgls = prev["global"][0]["longShortRatio"]
    ptls = prev["top"][0]["longShortRatio"]
    gdiff.append(float(gls)-float(pgls))
    tdiff.append( float(tls)-float(ptls))
print (f"global min: {min(gdiff)} max: {max(gdiff)}   top min: {min(tdiff)} max: {max(tdiff)}" )

# %%
import pandas as pd
df = pd.DataFrame(list(db.longshort.find().sort( [( "global.timestamp", 1 )] )))
df.head()

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
db3.longshort.update_many( {},
  [
    { "$replaceRoot": 
        { "newRoot": { 
            "timestamp" : "$global.timestamp", 
            "global" : {"$first" : "$global"}, 
            "top" : {"$first" : "$top" }
            }
        }
    }
  ]
)

# %%
