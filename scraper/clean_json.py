import json
import re
from pathlib import Path

def clean_text(text: str) -> str:
    """Nettoie une chaîne de texte : espaces, ponctuation isolée, caractères spéciaux."""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)  # remplace les espaces multiples
    text = re.sub(r"^\W+$", "", text)  # supprime les lignes composées uniquement de ponctuation
    return text

def clean_json_file(input_file: str, output_file: str):
    input_path = Path(input_file)
    output_path = Path(output_file)

    with input_path.open(encoding="utf-8") as f:
        raw_data = json.load(f)

    cleaned_data = []

    for i, doc in enumerate(raw_data):
        title = clean_text(doc.get("title", ""))
        subtitles = [clean_text(s) for s in doc.get("subtitles", []) if len(clean_text(s)) > 20]
        paragraphs = [clean_text(p) for p in doc.get("paragraphs", []) if len(clean_text(p)) > 50]

        # Construction du champ "content"
        full_text = ". ".join([title] + subtitles + paragraphs)
        full_text = clean_text(full_text)

        if full_text:  # On garde uniquement les docs avec contenu utile
            cleaned_data.append({
                "doc_id": i + 1,
                "title": title,
                "content": full_text
            })

    # Sauvegarde du fichier nettoyé
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Fichier nettoyé sauvegardé sous : {output_file}")
    print(f"📊 Nombre de documents conservés : {len(cleaned_data)}")

# Exemple d'exécution
if __name__ == "__main__":
    clean_json_file("scraper/output/data.json", "scraper/output/clean_data.json")
