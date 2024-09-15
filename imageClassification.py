from dotenv import load_dotenv
import google.generativeai as genai
import os
import PyPDF2
import pandas as pd

# Load API key from environment variables
load_dotenv(dotenv_path="key.env")
api_key = os.getenv("API_KEY")
if api_key is None:
    raise ValueError("API_KEY not found in environment variables")

# Configure the Gemini API
genai.configure(api_key=api_key)

# Function to upload a file and return the file object
def upload_file(path, display_name):
    file = genai.upload_file(path=path, display_name=display_name)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text
        return extracted_text

# Step 1: Upload the image and the PDF file
image_file = upload_file("./images/zahnbuerste.jpg", "Product Image")
#pdf_file = upload_file("./data/hs-code-new.pdf", "HS Codes PDF")

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
    f"Return the result in the following format. Name the product in german.\n"
    f"Product Classification | Chapter Number | Chapter Description"
)

# Step 4: Use the Gemini model to classify the image and extract the relevant information
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content([image_file, prompt])

# Step 5: Extract the response text and split it into columns
response_text = response.text.strip()
print(f"API Response:\n {response_text}")
# Assuming the API returns the result in the format: Intrastat-Nummer | Ursprungsland | Gewicht
intrastat_nummer, ursprungsland, gewicht = response_text.split(" | ")

# Step 6: Load the existing Excel file or create a new one
output_path = "./results/results-data.xlsx"
try:
    df = pd.read_excel(output_path)
except FileNotFoundError:
    # If the file doesn't exist, create a new DataFrame with the correct columns
    df = pd.DataFrame(columns=["Intrastat-Nummer", "Ursprungsland", "Gewicht"])

# Step 7: Append the new data to the DataFrame
new_row = {
    "Intrastat-Nummer": intrastat_nummer,
    "Ursprungsland": ursprungsland,
    "Gewicht": gewicht
}
df = df.append(new_row, ignore_index=True)

# Step 8: Save the updated DataFrame back to the Excel file
df.to_excel(output_path, index=False)

print(f"Data saved to {output_path}")
print(df.tail())  # Display the last few rows to verify the result