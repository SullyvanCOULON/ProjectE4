import os
from pathlib import Path
from byaldi import RAGMultiModalModel
#from together import Together
from openai import OpenAI
from pdf2image import convert_from_path

# Définir les chemins
model_name = "vidore/colqwen2-v0.1"
local_model_dir = Path("./models") / model_name.replace("/", "_")
index_name = "onisr_index"
#pdf_path = Path("./content/pdf_folder/Codedelaroute.pdf")

pdf_path = Path("./content/pdf_folder/PANNEAUX.pdf")
images_dir = Path("./content/images")

# Initialiser le client OpenAI
client = OpenAI(
    api_key='',
    base_url="http://10.3.0.3:23333/v1"
)

# Créer les répertoires si nécessaire
local_model_dir.mkdir(parents=True, exist_ok=True)
images_dir.mkdir(parents=True, exist_ok=True)


# 1. Charger ou télécharger le modèle
if local_model_dir.exists() and any(local_model_dir.iterdir()):
    print(f"Chargement du modèle local depuis {local_model_dir}")
    model = RAGMultiModalModel.from_pretrained(str(local_model_dir))
else:
    print(f"Téléchargement du modèle {model_name}")
    model = RAGMultiModalModel.from_pretrained(model_name)
    # Sauvegarder le modèle localement pour une utilisation future
    #model.save_pretrained(str(local_model_dir))

# 2. Vérifier si l'index existe déjà
index_path = Path(f"./{index_name}")
if index_path.exists():
    print(f"Chargement de l'index existant depuis {index_path}")
    model.load_index(index_name=index_name, index_path=str(index_path))
else:
    print(f"Création d'un nouvel index pour {pdf_path}")
    model.index(input_path=pdf_path,
                index_name=index_name,
                store_collection_with_index=True,
                overwrite=True)

# 3. Convertir le PDF en images une seule fois
if not any(images_dir.iterdir()):
    print(f"Conversion du PDF en images et sauvegarde dans {images_dir}")
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        image.save(images_dir / f"page_{i+1}.png", "PNG")
else:
    print(f"Images déjà présentes dans {images_dir}, chargement direct")

# Requête de recherche
query = "Quelle est la description du panneau AB4 ?"
results = model.search(query, k=1)

print(f"Résultats de la recherche pour '{query}':")
for result in results:
    print(f"Doc ID: {result.doc_id}, Page: {result.page_num}, Score: {result.score}")

# Charger l'image de la page retournée
page_num = model.search(query, k=1)[0].page_num
image_path = images_dir / f"page_{page_num}.png"

# Lire l'image en base64
with open(image_path, "rb") as image_file:
    import base64
    returned_page = base64.b64encode(image_file.read()).decode('utf-8')

# Appel à l'API Together
#client = Together(api_key='c4bf084df6c344eb437607fb0f04ea627d17bbc84eb5ab1c621f874d36ec3b1b')

model_name = client.models.list().data[0].id
print(f"Modèle utilisé : {model_name}")

response = client.chat.completions.create(
    model=model_name,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{returned_page}",
                    },
                },
            ],
        }
    ],
    max_tokens=200,
)

print(response.choices[0].message.content)