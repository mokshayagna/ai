from google import genai
from google.genai import types


def is_even(n: int) -> bool: 
    print(f"In is_even: {n}") 
    return n % 2 == 0 

def main():
    MODEL_NAME = "gemini-2.0-flash-001"
    
    prompt = "Is nine even?"

    client = genai.Client()

    # Automatic execution of tool
    tools_config = types.GenerateContentConfig(tools=[is_even]) 
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt, config=tools_config)
    print(response.text)
    
    # Disable Automatic execution of tool
    #auto_call = types.AutomaticFunctionCallingConfig(disable=True) # Disable automatic function calling
    #tools_config = types.GenerateContentConfig(tools=[is_even], automatic_function_calling=auto_call)
    #response = client.models.generate_content(model=MODEL_NAME, contents=prompt, config=tools_config)
    #print(response)
    
    
if __name__ == "__main__":
    main()
