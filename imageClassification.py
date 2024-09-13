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
pdf_file = upload_file("./data/hs-code.pdf", "HS Codes PDF")

# Step 2: Extract the PDF content
pdf_text = extract_text_from_pdf('./data/hs-code.pdf')

# Step 3: Create a prompt for Gemini to classify the image and find the HS code, Ursprungsland, and Gewicht
prompt = (
    f"Classify the product in the image and find the corresponding information from the table in the PDF. "
    f"The Intrastat-Nummer is in column G (titled 'CN8'), the Ursprungsland and Gewicht are also present in the table. "
    f"Return the result in this format:\n"
    f"Intrastat-Nummer | Ursprungsland | Gewicht\n\nPDF Content:\n{pdf_text}"
)

# Step 4: Use the Gemini model to classify the image and extract the relevant information
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content([image_file, pdf_file, prompt])

# Step 5: Extract the response text and split it into columns
response_text = response.text.strip()
print(f"API Response: {response_text}")
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