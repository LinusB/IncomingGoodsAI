from config import *
from dotenv import load_dotenv
import google.generativeai as genai
import os
import re
import PyPDF2
import pandas as pd

load_dotenv(dotenv_path="key.env")
api_key = os.getenv("API_KEY")
if api_key is None:
    raise ValueError("API_KEY not found in environment variables")
genai.configure(api_key=api_key)


def upload_file(path, display_name):
    file = genai.upload_file(path=path, display_name=display_name)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text
        return extracted_text
    
def update_config_product(product):
    config_file_path = './config/config.py'
    with open(config_file_path, 'r') as config_file:
        config_content = config_file.readlines()
    new_content = []
    for line in config_content:
        if re.match(r"^PRODUCT\s*=", line):
            new_content.append(f'PRODUCT = "{product}"\n')
        else:
            new_content.append(line)
    with open(config_file_path, 'w') as config_file:
        config_file.writelines(new_content)

def update_config_tax_chapter(chapter):
    config_file_path = './config/config.py'
    with open(config_file_path, 'r') as config_file:
        config_content = config_file.readlines()
    new_content = []
    for line in config_content:
        if re.match(r"^TAX_CHAPTER\s*=", line):
            new_content.append(f"TAX_CHAPTER = {chapter}\n")
        else:
            new_content.append(line)
    with open(config_file_path, 'w') as config_file:
        config_file.writelines(new_content)

def update_config_tax_chapter_description(description):
    config_file_path = './config/config.py'
    with open(config_file_path, 'r') as config_file:
        config_content = config_file.readlines()
    new_content = []
    for line in config_content:
        if re.match(r"^TAX_CHAPTER_DESCRIPTION\s*=", line):
            new_content.append(f'TAX_CHAPTER_DESCRIPTION = "{description}"\n')
        else:
            new_content.append(line)
    with open(config_file_path, 'w') as config_file:
        config_file.writelines(new_content)

def update_config_infrastat_number(number):
    config_file_path = './config/config.py'
    with open(config_file_path, 'r') as config_file:
        config_content = config_file.readlines()
    new_content = []
    for line in config_content:
        if re.match(r"^INFRASTAT_NUMBER\s*=", line):
            new_content.append(f"INFRASTAT_NUMBER = {number}\n")
        else:
            new_content.append(line)
    with open(config_file_path, 'w') as config_file:
        config_file.writelines(new_content)

def update_config_infrastat_description(desciption):
    config_file_path = './config/config.py'
    with open(config_file_path, 'r') as config_file:
        config_content = config_file.readlines()
    new_content = []
    for line in config_content:
        if re.match(r"^INFRASTAT_DESCRIPTION\s*=", line):
            new_content.append(f'INFRASTAT_DESCRIPTION = "{desciption}"\n')
        else:
            new_content.append(line)
    with open(config_file_path, 'w') as config_file:
        config_file.writelines(new_content)

def update_config_origin(origin):
    config_file_path = './config/config.py'
    with open(config_file_path, 'r') as config_file:
        config_content = config_file.readlines()
    new_content = []
    for line in config_content:
        if re.match(r"^ORIGIN\s*=", line):
            new_content.append(f'ORIGIN = "{origin}"\n')
        else:
            new_content.append(line)
    with open(config_file_path, 'w') as config_file:
        config_file.writelines(new_content)

def update_config_destination(destination):
    config_file_path = './config/config.py'
    with open(config_file_path, 'r') as config_file:
        config_content = config_file.readlines()
    new_content = []
    for line in config_content:
        if re.match(r"^DESTINATION\s*=", line):
            new_content.append(f'DESTINATION = "{destination}"\n')
        else:
            new_content.append(line)
    with open(config_file_path, 'w') as config_file:
        config_file.writelines(new_content)

def update_config_weight(weight):
    config_file_path = './config/config.py'
    with open(config_file_path, 'r') as config_file:
        config_content = config_file.readlines()
    new_content = []
    for line in config_content:
        if re.match(r"^WEIGHT\s*=", line):
            new_content.append(f"WEIGHT = {weight}\n")
        else:
            new_content.append(line)
    with open(config_file_path, 'w') as config_file:
        config_file.writelines(new_content)

def update_config_price(price):
    config_file_path = './config/config.py'
    with open(config_file_path, 'r') as config_file:
        config_content = config_file.readlines()
    new_content = []
    for line in config_content:
        if re.match(r"^PRICE\s*=", line):
            new_content.append(f"PRICE = {price}\n")
        else:
            new_content.append(line)
    with open(config_file_path, 'w') as config_file:
        config_file.writelines(new_content)



# -----------------------                       --------------------------------                       ----------------------- #
# -----------------------                                                                              ----------------------- #
# -----------------------                      IMAGE CLASSIFICATION & CATEGORIZING                     ----------------------- #
# -----------------------                                                                              ----------------------- #
# -----------------------                       --------------------------------                       ----------------------- #



# Step 1: Upload the image and the PDF file
image_file = upload_file("./images/zahnseide.jpg", "Product Image")

# Step 2: Extract the PDF content
#pdf_text = extract_text_from_pdf('./data/hs-code-new.pdf')

# Step 3: Create a prompt for Gemini to classify the image and find the HS code, Ursprungsland, and Gewicht
prompt = (
    f"Classify the product in the image and determine which chapter it belongs to based on the following chapters:\n"
    f"1. Lebende Tiere und Waren tierischen Ursprungs\n"
    f"2. Waren pflanzlichen Ursprungs\n"
    f"3. Tierische und pflanzliche Fette und Öle; Erzeugnisse ihrer Spaltung; genießbare verarbeitete Fette; Wachse tierischen und pflanzlichen Ursprungs\n"
    f"4. Waren der Lebensmittelindustrie; Getränke, alkoholhaltige Flüssigkeiten und Essig; Tabak und verarbeitete Tabakersatzstoffe\n"
    f"5. Mineralische Stoffe\n"
    f"6. Erzeugnisse der chemischen Industrie und verwandter Industrien\n"
    f"7. Kunststoffe und Waren daraus; Kautschuk und Waren daraus\n"
    f"8. Häute, Felle, Leder, Pelzfelle und Waren daraus; Sattlerwaren; Reiseartikel, Handtaschen und ähnliche Behältnisse; Waren aus Därmen\n"
    f"9. Holz und Holzwaren; Holzkohle; Kork und Korkwaren; Flechtwaren und Korbmacherwaren\n"
    f"10. Halbstoffe aus Holz oder anderen cellulosehaltigen Faserstoffen; Papier oder Pappe (Abfälle und Ausschuss) zur Wiedergewinnung; Papier, Pappe und Waren daraus\n"
    f"11. Textilien und Waren daraus\n"
    f"12. Schuhe, Kopfbedeckungen, Regen- und Sonnenschirme, Gehstöcke, Sitzstöcke, Peitschen, Reitpeitschen und Teile Davon; Zugerichtete Federn und Waren aus Federn; Künstliche Blumen; Waren aus Menschenhaaren\n"
    f"13. Waren aus Steinen, Gips, Zement, Asbest, Glimmer oder ähnlichen Stoffen; Keramische Waren; Glas und Glaswaren\n"
    f"14. Echte Perlen oder Zuchtperlen, Edelsteine oder Schmucksteine, Edelmetalle, Edelmetallplattierungen und Waren daraus; Fantasieschmuck; Münzen\n"
    f"15. Unedle Metalle und Waren daraus\n"
    f"16. Maschinen, Apparate, mechanische Geräte und elektrotechnische Waren, Teile davon; Tonaufnahme- oder Tonwiedergabegeräte, Fernseh-Bild- und -Tonaufzeichnungsgeräte oder Fernseh-Bild- und -Tonwiedergabegeräte, Teile und Zubehör für diese Geräte\n"
    f"17. Beförderungsmittel"
    f"18. Optische, fotografische oder kinematografische Instrumente, Apparate und Geräte; Mess-, Prüf- oder Präzisionsinstrumente, -Apparate und -Geräte; medizinische und chirurgische Instrumente, Apparate und Geräte; Uhrmacherwaren; Musikinstrumente; Teile und Zubehör für diese Instrumente, Apparate und Geräte\n"
    f"19. Waffen und Munition; Teile davon und Zubehör\n"
    f"20. Verschiedene Waren\n"
    f"21. Kunstgegenstände, Sammlungsstücke und Antiquitäten\n"
    f"Return the identified product name, the chapter and the description. Only answer with this format: Product | chapter | description of chapter \n"
    f"Answer in german. Only respond most necessary information without any column titles."
)

# Step 4: Use the Gemini model to classify the image and extract the relevant information
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content([image_file, prompt])

# Step 5: Extract the response text and remove any extra new lines or formatting characters
response_text = response.text.strip()
#print(response_text)
handling_text = response_text
product_parts = handling_text.split(" | ")  # Split by the column separator " , "
#print(product_parts)

if len(product_parts) == 3:
        product_classification = product_parts[0].strip()  # Extract product classification
        chapter_number = product_parts[1].strip()  # Extract chapter number
        chapter_description = product_parts[2].strip()  # Extract chapter description

        print(f"Product: {product_classification}, Chapter: {chapter_number}, Description: {chapter_description}")
        update_config_product(product_classification)
        update_config_tax_chapter(chapter_number)
        update_config_tax_chapter_description(chapter_description)
else:
    raise ValueError(f"Unexpected format in Response: {handling_text}")



# -----------------------                       --------------------------------                       ----------------------- #
# -----------------------                                                                              ----------------------- #
# -----------------------                       GIVING TAX IDENTIFICATION NUMBER                       ----------------------- #
# -----------------------                                                                              ----------------------- #
# -----------------------                       --------------------------------                       ----------------------- #



# Step 6: Load the relevant chapter's Excel file based on the chapter number
pdf_file = upload_file(f"./data/pdf/{chapter_number}.pdf", "PDF - Intrastat-Nummer")


# Step 7: Preparing new Prompt
prompt = (
    f"Find the Intrastat-Nummer and the corresponding description for the product '{product_classification}' "
    f"in the attached PDF. Column A is the Intrastat-Nummer and Column B the corresponding description.\n\n"
    f"Return the identified Instrastat-Nummer and the corresponding description. Only answer with this format: Intrastat-Numme | description of Intrastat-Nummer \n"
    f"Answer in german. Only respond most necessary information without any column titles."
)

# Step 8: Use the Gemini model to extract the relevant Intrastat-Nummer
response_hsCode = model.generate_content([pdf_file, prompt])

# Step 9: Extract the Intrastat-Nummer and description from the response
response_hsCode_text = response_hsCode.text.strip()
#print(response_hsCode_text)
handling_hsCode = response_hsCode_text
infrastat_parts = handling_hsCode.split(" | ")  # Split by the column separator " , "
#print(infrastat_parts)

if len(infrastat_parts) == 2:
        infrastat_number = infrastat_parts[0].strip()  # Extract Infrastat-Number
        infrastat_description = infrastat_parts[1].strip()  # Extract Description of Infrastat-Number

        print(f"Infrastat-Nummer: {infrastat_number}, Beschreibung: {infrastat_description}")
        update_config_infrastat_number(infrastat_number)
        update_config_infrastat_description(infrastat_description)
else:
    raise ValueError(f"Unexpected format in Response: {handling_hsCode}")