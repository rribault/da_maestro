import json
import base64
from src.LLM_query import pixtral, gemini
import os
from pdf2image import convert_from_path

# --- Configuration ---

ChoosenOne = {
    'pixtral' : pixtral.ask_pixtral,
    'gemini' : gemini.ask_gemini_vision
}

Model_choices = {}
for key in ChoosenOne:
    Model_choices[key] = key

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None

# --- JSON Validation ---
def is_valid_json(json_string):
    """Checks if a string is valid JSON."""
    try:
        json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False

# --- Main Execution ---
def extract_data_from_png(file_path:str, model:str='gemini'):
    """Converts images, interacts with the Mistral AI API (with image input), and saves the output as JSON."""

    #Convert image to base64
    images = encode_image(file_path)

    if images is None:
        print("Failed to convert PDF to images. Exiting.")
        return

    try:
        # Run the LLM model of your choice:
        response_text =ChoosenOne[model](images)

        if is_valid_json(response_text):
            response_text= json.loads(response_text)
        else:
            print(f"Error: Invalid JSON received from {model}.")
            print("Raw response from {model}:", response_text)
            # Handle error - maybe log the error and continue to the next image.

    except Exception as e:
        print(f"Error during {model} API call: {e}")
        # Handle the error - perhaps save what was extracted so far.

    return response_text

def pdf_to_image(pdf_path, output_folder="images", dpi=300, output_format="png"):
    """
    Converts a PDF file to a series of images.

    Args:
        pdf_path: Path to the input PDF file.
        output_folder: Folder where the images will be saved. Defaults to "images".
        dpi: Resolution of the output images in DPI.  Higher DPI means better quality.
        output_format: The image format (e.g., "png", "jpeg", "tiff"). Defaults to "png".
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the output folder if it doesn't exist

    try:
        images = convert_from_path(pdf_path, dpi=dpi)
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return

    for i, image in enumerate(images):
        output_path = os.path.join(output_folder, f"page_{i+1}.{output_format}")
        image.save(output_path, output_format.upper())  # Save the image

    print(f"PDF converted to images and saved in '{output_folder}'")


if __name__ == "__main__" :
    PNG_FILE_PATH = r"C:\Users\romain.ribault\Pictures\Screenshots\devis.png"
    response_text = extract_data_from_png(PNG_FILE_PATH)
    print(response_text)