from google import genai
import os

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)
print("os.getenv('GOOGLE_API_KEY'):", os.getenv("GOOGLE_API_KEY"))
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Hello"
)

print(response.text)