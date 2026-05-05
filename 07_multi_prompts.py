from google import genai

def main():
    MODEL = "gemini-2.0-flash-001"
    client = genai.Client()
    prompt1 = "who is the president of India?"
    prompt2 = "add 2 numbers 5 and 10"
    response = client.models.generate_content(model=MODEL, contents=[prompt1, prompt2])
    print(response.text) 
if __name__ == "__main__":
    main()
    