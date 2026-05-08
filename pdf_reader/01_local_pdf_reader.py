from google import genai
from google.genai import types

client = genai.Client()

def main():
    file_path = "/mnt/c/AI/resource/forgotten-history.pdf"

    with open(file_path, "rb") as f:
        data = f.read()
    
    pdf_part = types.Part.from_bytes(
        data=data,
        mime_type="application/pdf"
    )
    
    prompt = """
    You are a PDF analyzer. Analyze the PDF and give a summary.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[pdf_part, prompt]   
    )
    
    print(response.text)   

if __name__ == "__main__":
    main()