from mistralai import Mistral
import os
from models import DA

MISTRAL_API_KEY = os.getenv("Mistral_API_Key") # Get API key from environment variable
MODEL_NAME = "pixtral-large-2411" #  "mistral-large-latest" or "mistral-medium-latest"  Model must support images!


def ask_pixtral(images):
        client = Mistral(api_key=MISTRAL_API_KEY)
        ChatMessage=  [
                    {
                    "role": "system",
                    "content": [
                        {
                        "type": "text",
                        "text": "Tu es un assistant spécialisé dans l'extraction de données à partir d'une image de devis. Tu réponds au format JSON"
                        }
                    ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f""" Extrais les éléments textuels de l'image, et retourne le résultat formaté en JSON selon le format suivant:\n\n
                                    ```{DA.model_json_schema()}```
                                    Extrais du devis les frais de ports et traite les frais de ports comme un item.
                                    Le devis est réalisé pour France Energies Marines.
                                    Retourne **UNIQUEMENT** un objet JSON valide.
                                    Make sure property name enclosed in double quotes.
                                    """
                            },
                            {
                                "type": "image_url",
                                "image_url": f"data:image/jpeg;base64,{images}" 
                            }
                        ]
                    }
                ]
        # Get the chat response
        chat_response = client.chat.complete(
            model=MODEL_NAME,
            messages=ChatMessage,
            response_format={"type": "json_object"}
        )

        return chat_response.choices[0].message.content