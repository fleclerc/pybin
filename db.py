import pymongo

# Establish connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Create a database
db = client.classDB

dataset = db.binancetest

# db.classroom.insert_many(
#     [
#       {
#         'name': 'Jerry',
#         'hobbies': 'gardening',
#         'classroom_teacher': "Jerry's Dad",
#         'exam_scores': [1, 0, -25]
#       },
#       {
#         'name': 'Muhammed',
#         'hobbies': {'exercise': ['swimming', 'running'],
#                     'games': 'chess'},
#         'classroom_teacher': 'Jerry',
#         'exam_scores': [100, 100, 100]
#       }
#     ])
# for x in db.classroom.find():
#   print(x)