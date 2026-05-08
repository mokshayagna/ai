from google import genai
from google.genai import types

client = genai.Client()

def main():
    file_url = "https://storage.googleapis.com/promptlyai-public-bucket/forgotten-history.pdf"
    prompt = """
    You are a professional document summarization specialist.
    Please summarize the given document, capturing the key points and main arguments.
    """

    model_name = "gemini-2.0-flash"
    pdf_part = types.Part.from_uri(file_uri=file_url, mime_type="application/pdf")
    contents = [pdf_part, prompt]

    response = client.models.generate_content(
        model=model_name,
        contents=contents
    )
    print(response.text)
    
if __name__ == "__main__":
    main()
    