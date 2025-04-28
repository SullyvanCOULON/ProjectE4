from flask import Flask, request, jsonify
import base64
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  

from utils.search_mongo import search_documents
from RAG.initialize import initialize
from AccesLLM import query_image_base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialiser tout au démarrage
model, images_dir = initialize()

@app.route('/api/message', methods=['POST'])
def handle_message():
    content = request.json.get('message')
    if not content:
        return jsonify({'response': 'Aucun message reçu'}), 400

    query = content
    results = model.search(query, k=1)
    paragraphs = search_documents(query)

    print("\n--- CONTEXTE RÉCUPÉRÉ DE MONGO ---")
    for i, p in enumerate(paragraphs):
        print(f"[Extrait {i+1}]\n{p}\n")
    context = "\n".join(paragraphs)
    
    page_num = results[0].page_num if results else 1
    print("\n--- PAGE DU PDF LA PLUS PERTINENTE ---")
    print(f"Page n.: {page_num}")
    print("--- FIN CONTEXTE ---\n")
    image_path = images_dir / f"page_{page_num}.png"
    
    with open(image_path, "rb") as image_file:
        returned_page = base64.b64encode(image_file.read()).decode('utf-8')

    response = query_image_base64(returned_page, context, query)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True, use_reloader=False)