from google import genai
from google.genai import types

client = genai.Client()

def main():
    
    file_path = "/mnt/c/AI/resource/forgotten-history.pdf"
    
    with open(file_path,"rb") as f:
        data = f.read()
    
    #prompt = """
    #You are expert in analyzer I will ask some questions and you answer me, how many Dynasties are there
    #and what are they?
    #"""
    
    prompt = """ can you generate some question from the book?"""
    
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