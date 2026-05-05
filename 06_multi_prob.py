from google import genai

client = genai.Client()

def query_by_model(model_name):
    prompt = "Who is the Prime minister of India?"
    prompt = "Who is the Prime minister of India?  Just answer to the question no more extra information is required"
    

    print(f"Querying: {model_name}")
    print(prompt)
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    print(response.text)
    print()

def main():
    model_name = "gemini-2.0-flash"
    query_by_model(model_name)

    model_name = "gemini-2.5-pro"
    query_by_model(model_name)


if __name__ == "__main__":
    main()
    