from pymongo import MongoClient
import json

client = MongoClient("mongodb://mongo:27017/")  
db = client["onisr_db"]
collection = db["articles"]

with open("output/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

collection.insert_many(data)
print("Import terminé !")