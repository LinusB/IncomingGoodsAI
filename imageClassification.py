from dotenv import load_dotenv
import google.generativeai as genai
import os
import base64

# load API-KEY
load_dotenv(dotenv_path="key.env")
api_key = os.getenv("API_KEY")
if api_key is None:
    raise ValueError("API_KEY not found in environment variables")

# Config API-Key
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Folder images
image_folder = "./images"

# load and encode images in base64
def load_and_encode_images(folder, limit=5):
    encoded_images = []
    files = os.listdir(folder)[:limit]  # Begrenzung der Bilder
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):  # Unterstützte Bildformate
            file_path = os.path.join(folder, file)
            with open(file_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                encoded_images.append(encoded_image)
    return encoded_images

# Bilder laden und kodieren
images = load_and_encode_images(image_folder)

# API-Aufruf vorbereiten
# Hier wird angenommen, dass die API einen Parameter für Bilder und den Prompt erwartet
prompt = "Bestimme die Warennummer für die folgenden Bilder"
response = model.generate_content(prompt, images=images)

# Die API-Antwort verarbeiten
if response:
    print("Warennummern für die Bilder:")
    for i, image in enumerate(images):
        # Hier wird angenommen, dass die Antwort die Warennummern enthält
        print(f"Bild {i + 1}: Warennummer {response.text[i]}")  # Beispiel wie die Warennummer verwendet werden könnte
else:
    print("Keine Antwort von der API erhalten.")