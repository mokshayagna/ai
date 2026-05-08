from google import genai
from google.genai import types

client = genai.Client()

def main():
    
    file_path = "/mnt/c/AI/resource/forgotten-history.pdf"
    
    with open(file_path,"rb") as f:
        data = f.read()
    
    prompt = """
    Please analyze the content of the provided PDF document about ancient Indian dynasties.

    Based on the document, perform the following tasks:
    1. Who are all the rulers and their time period?
    2. Can you give me a structured output in a table format(make sure the columns and rows should be alligned properly?
    """
    # 3. Make sure there is a column which specifies, duration of the ruler in years
    
    pdf_part = types.Part.from_bytes(
        data = data,
        mime_type = "application/pdf"
    )
    contents = [pdf_part,prompt]
    
    model_name="gemini-2.0-flash"
    
    response = client.models.generate_content(
        model=model_name,
        contents=contents
    )
    print(response.text)
    
if __name__ == "__main__":
    main()