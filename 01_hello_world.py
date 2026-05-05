from google import genai

MODEL_NAME = "gemini-2.0-flash-001"

client = genai.Client()
prompt = "when did the first world war start and end ?"

response = client.models.generate_content(model=MODEL_NAME, contents=prompt)    
print(response.text)
