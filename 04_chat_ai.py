from google import genai

def main():
    MODEL_NAME = "gemini-2.0-flash-001"
    client = genai.Client()
    
    chat = client.chats.create(model=MODEL_NAME)
    
    prompt = "who is the president of India?"
    response = chat.send_message(prompt)
    print(response.text)

    prompt = "In which year he/she became president?"
    response = chat.send_message(prompt)
    print(response.text) 

if __name__ == "__main__":
    main()