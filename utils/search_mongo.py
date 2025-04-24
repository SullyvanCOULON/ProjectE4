# mongo_search.py
from pymongo import MongoClient

def search_documents(query, db_name="onisr_db", collection_name="articles"):
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    collection = db[collection_name]

    # Recherche sur les paragraphes
    results = collection.find({
        "paragraphs": {
            "$elemMatch": {
                "$regex": query,
                "$options": "i"
            }
        }
    })

    docs = []
    for doc in results:
        for p in doc.get("paragraphs", []):
            if query.lower() in p.lower():
                docs.append(p)

    return docs