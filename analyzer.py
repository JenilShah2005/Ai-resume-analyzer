from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("Gemini_API_KEY")
)
models = client.models.list()
for model in models:
    print(model.name)
def ask_ai(prompt):
    try:
        
        response = client.models.generate_content(
            model = "gemini-3.5-flash",
            contents = prompt
        )
        return response.text
    except Exception as e:
        print(f"Error: {e}")
   