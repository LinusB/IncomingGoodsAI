from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv(dotenv_path="key.env")
api_key = os.getenv("API_KEY")
if api_key is None:
    raise ValueError("API_KEY not found in environment variables")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Zähle von 1 bis 10")
print(response.text)