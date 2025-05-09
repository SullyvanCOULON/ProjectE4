from pymongo import MongoClient
import os

def search_documents(query, db_name="onisr_db", collection_name="articles", top_k=5):
    # Récupère l'hôte MongoDB depuis les variables d'environnement, sinon localhost par défaut
    mongo_host = os.getenv("MONGO_HOST", "localhost")
    mongo_uri = f"mongodb://{mongo_host}:27017/"
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    print("📊 Nombre total de documents dans la collection :", collection.count_documents({}))

    keywords = query.lower().split()
    results = []

    for doc in collection.find():
        for p in doc.get("paragraphs", []):
            score = sum(1 for word in keywords if word in p.lower())
            if score > 0:
                results.append((score, p))

    # Trier par pertinence
    results.sort(reverse=True, key=lambda x: x[0])
    top_paragraphs = [p for score, p in results[:top_k]]

    print(f"🔎 {len(top_paragraphs)} paragraphes trouvés pour la requête : '{query}'")
    return top_paragraphs