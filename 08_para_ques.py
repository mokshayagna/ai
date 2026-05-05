from google import genai

def main():
    MODEL = "gemini-2.0-flash-001"
    client = genai.Client()
    
    chat = client.chats.create(model=MODEL)
    
    prompt = """
           On a hot summer day, a thirsty crow was flying across the sky in search of water. 
            It had been flying for a long time and was feeling very weak. After searching everywhere, 
            the crow finally spotted a pot near a house. It quickly flew down, hoping to find water inside.

            When the crow looked into the pot, it saw that there was only a little water at the bottom. 
            Its beak could not reach the water, no matter how hard it tried. The crow became worried but did not give up. 
            It started thinking of a solution.

            After some time, the crow noticed small stones lying nearby. 
            It got an idea. One by one, the crow picked up the stones and dropped them into the pot. 
            With each stone, the water level slowly began to rise. The crow patiently continued this process.

            Finally, the water came up high enough for the crow to reach it. 
            The crow happily drank the water and felt refreshed. It then flew away, 
            satisfied and proud of its clever idea.
    """
    response = chat.send_message(prompt)
    prompt = "can you give me moral in one word?"
    response = chat.send_message(prompt)
    print(response.text)
if __name__ == "__main__":
    main()
