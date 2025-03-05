from google import genai
from google.genai import types
import base64
from models import DA
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def ask_gemini_vision(images, gemini_api_key=GEMINI_API_KEY, model_name="gemini-1.5-pro-latest"): # or "gemini-pro-vision"

    """
    Extracts text from an image and returns a JSON formatted result using Gemini Vision.

    Args:
        images: A base64 encoded string representing the image.
        gemini_api_key: Your Google Gemini API key.
        model_name: The name of the Gemini model to use.  Defaults to "gemini-1.5-pro-latest". "gemini-pro-vision" is another possibility.  The proper choice depends on your needs.

    Returns:
        A JSON string containing the extracted information, or None if an error occurred.
    """

    client = genai.Client(api_key=gemini_api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents = [
            f"""
            Extrais les éléments textuels de l'image, et retourne le résultat formaté en JSON selon le format suivant:\n\n
            ```{DA.model_json_schema()}```
            Extrais du devis les frais de ports et traite les frais de ports comme un item.
            Le devis est réalisé pour France Energies Marines.  
            Retourne **UNIQUEMENT** un objet JSON valide.
            Make sure property name enclosed in double quotes.
            """,
            types.Part.from_bytes(data=base64.b64decode(images), mime_type="image/jpeg"),  # Decode base64 and create image part.  Assumes JPEG format.
        ]
    )
    return response.text.replace('```json\n','').replace('```','')


    # {\n  \"provider_contact\": \"user@example.com\",\n \"provider\": \"maritech\",\n \"quotation_nb\": \"125abc\",\n \"items\": [{\"description\": \"item description\", \n \"qty\":1, \"price\": 1000}]\n}\n