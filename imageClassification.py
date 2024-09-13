from dotenv import load_dotenv
import google.generativeai as genai
import os
import PyPDF2

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

# Step 3: Create a prompt for Gemini to classify the image and find the HS code from the PDF
prompt = f"Classify the product in the image and find the corresponding HS code from the table in the PDF. The HS code is in column G, titled 'CN8'.\n\nPDF Content:\n{pdf_text}"

# Step 4: Use the Gemini model to classify the image and extract the HS code
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content([image_file, pdf_file, prompt])

# Step 5: Print the result
print(response.text)