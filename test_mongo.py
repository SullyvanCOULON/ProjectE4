from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["onisr_db"]
collection = db["articles"]

# Test de connexion
try:
    print("✅ Connexion à MongoDB réussie !")
    
    # Vérifie s'il y a des documents dans la collection
    count = collection.count_documents({})
    print(f"📄 Nombre de documents dans la collection 'articles' : {count}")
    
    # Affiche les 3 premiers documents pour vérifier
    for doc in collection.find().limit(3):
        print("--- Document ---")
        print(doc)
except Exception as e:
    print(f"❌ Erreur de connexion à MongoDB : {e}")