from google import genai

def query_by_model(model_name):
    prompt = "who is the president of India?"
    
    print(f"Querying model: {model_name}")
    client = genai.Client()
    response = client.models.generate_content(model=model_name, contents=prompt)

    print(response.text)
    
def main():
    model_name = "gemini-2.0-flash-001"
    query_by_model(model_name)
    model_name = "gemini-2.0-flash"
    query_by_model(model_name)

    
if __name__ == "__main__":
    main()
    