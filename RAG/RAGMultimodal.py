import sys
import os
import httpx

#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Désactive CUDA proprement
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pathlib import Path
from openai import OpenAI
from utils.search_mongo import search_documents


# Définir les infos du serveur
api_key = "JpQAceF80Htu21tCbZx8eZGHwye2UP2V"
base_url = "https://llm.intellisphere.fr:9081/v1"

# Initialiser le client OpenAI-like
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# Récupérer le modèle dispo sur le serveur (comme dans ton 2e code)
model_name = client.models.list().data[0].id
print(f"Modèle utilisé : {model_name}")

# Tester la connexion au serveur (optionnel mais utile)
def test_server_connection(base_url, api_key):
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = httpx.get(f"{base_url}/models", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ Serveur accessible, connexion OK.")
            print("Liste des modèles disponibles :", response.json())
            return True
        else:
            print(f"⚠️ Le serveur a répondu mais avec le statut : {response.status_code}")
            return False
    except httpx.ConnectTimeout:
        print("❌ Erreur : connexion impossible (timeout)")
        return False
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        return False

# Test de connexion avant d’envoyer quoi que ce soit
if not test_server_connection(base_url, api_key):
    print("❌ Serveur inaccessible, arrêt du script.")
    sys.exit(1)

# Recherche MongoDB
query = "quelle est la vitesse maximale autorisée sur les routes nationales ?"
print("Recherche via MongoDB...")
paragraphs = search_documents(query)

print("\n--- CONTEXTE RÉCUPÉRÉ DE MONGO ---")
for i, p in enumerate(paragraphs):
    print(f"[Extrait {i+1}]\n{p}\n")
print("--- FIN CONTEXTE ---\n")



context = "\n".join(paragraphs)

prompt = f"""
Voici des extraits d’articles officiels de l’ONISR :

{context}

Réponds précisément à la question suivante : {query}
"""

# Envoyer la requête à l’API (sans byaldi, avec l’API OpenAI-like)
response = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=300,
)

print("Réponse du modèle :")
print(response.choices[0].message.content)