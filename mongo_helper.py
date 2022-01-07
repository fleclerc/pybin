print( "loading mongo_helper")

def pipeline_addFieldDatePart(timestampField):
    return {"$addFields": {
      "date": {"$dateToParts": {"date": { "$toDate": { "$toDate": f"${timestampField}" } } } }
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
                "date": base,
                "symbol": "$symbol"
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

def buildTradesPeriodTable(db, period = 'minute'):
    pipeline = []
    pipeline.append(pipeline_addFieldDatePart("eventTime"))
    pipeline.append(pipeline_group(period))
    pipeline.append(pipeline_sortBy("timestamp"))
    collection = f"trades_{period}"
    pipeline.append(pipeline_out(collection))
    print(pipeline)
    db.trades.aggregate(pipeline)
    print (db.get_collection(collection).count_documents({}))

def prepareLongShortData(db, symbol):
    longshort_pipeline = [
        {
            '$match' : {"global.symbol" : symbol}
        },
        {
            # keep only the fields we need otherwise too much junk
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
            # convert fields to usable types 
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
    return db.longshort.aggregate(longshort_pipeline)

def test():
    return 42