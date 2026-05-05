from google import genai

def main():
    MODEL = "gemini-2.0-flash-001"
    client = genai.Client()
    prompt = "who is the president of India?"
    response = client.models.generate_content(model=MODEL, contents=prompt)
    print(response.text) 
    
    response = client.models.count_tokens(model=MODEL, contents=prompt)
    print(response)
if __name__ == "__main__":   
    main()