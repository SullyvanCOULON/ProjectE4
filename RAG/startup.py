from pathlib import Path
from byaldi import RAGMultiModalModel
from pdf2image import convert_from_path

# Définir les chemins
model_name = "vidore/colqwen2-v0.1"
local_model_dir = Path("./models") / model_name.replace("/", "_")
index_name = "onisr_index"
pdf_path = Path("./content/pdf_folder/repport2024.pdf")
images_dir = Path("./content/images")

def initialize():
    # Créer les répertoires
    local_model_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    # 1. Charger ou télécharger le modèle
    if local_model_dir.exists() and any(local_model_dir.iterdir()):
        print(f"Chargement du modèle local depuis {local_model_dir}")
        model = RAGMultiModalModel.from_pretrained(str(local_model_dir))
    else:
        print(f"Téléchargement du modèle {model_name}")
        model = RAGMultiModalModel.from_pretrained(model_name)

    # 2. Charger ou créer l'index
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

    return model, images_dir