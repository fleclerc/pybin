import pymongo

# Establish connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Create a database
db = client.classDB

dataset = db.binancetest
