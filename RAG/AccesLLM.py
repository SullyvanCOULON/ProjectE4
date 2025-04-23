from openai import OpenAI
import base64

# Initialiser le client OpenAI
client = OpenAI(
    api_key="JpQAceF80Htu21tCbZx8eZGHwye2UP2V",
    base_url="https://llm.intellisphere.fr:9081/v1"
)

model_name = client.models.list().data[0].id
print(f"[image_query] Modèle utilisé : {model_name}")

def query_image_base64(img_base64: str, question: str) -> str:
    try:
        # Construire le message
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                ]
            }
        ]

        # Faire la requête
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=200
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Erreur lors de la requête image+texte : {e}"