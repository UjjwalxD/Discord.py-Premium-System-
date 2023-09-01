from pymongo import MongoClient
uri = "# python mongourl db"

cluster = MongoClient(uri)
db = cluster['cwp']
print("Database Connected: MongoDb")

premium_db = db['premium']


