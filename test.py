import os
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
response = client.models.generate_content(
    model="models/gemini-flash-lite-latest",
    contents="Say hello in one word"
)
print(response.text)