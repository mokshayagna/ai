from google import genai

def main():
    MODEL = "gemini-2.0-flash-001"
    client = genai.Client()
    prompt = "who is the president of India?"
    response = client.models.generate_content(model=MODEL, contents=prompt)
    print(response.text)
    
    prompt = "In which year he/she became president?"
    response = client.models.generate_content(model=MODEL, contents=prompt)
    print(response.text) # LLM doesn't know the context of previous prompt and hence it will not be able to answer this question correctly. It will just give a generic answer to this question without knowing who is the president of India.
    
    prompt = "Who is the president of India and in which year he/she became president?"
    response = client.models.generate_content(model=MODEL, contents=prompt)
    print(response.text)
if __name__ == "__main__":    
    main()
    