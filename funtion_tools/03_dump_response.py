from google import genai
from google.genai import types
import json

def is_even(number: int) -> bool:
    """Checks if a number is even."""
    return number % 2 == 0

def main():
    MODEL = "gemini-2.0-flash-001"

    # Create client
    client = genai.Client()

    tools_config = types.GenerateContentConfig(tools=[is_even])
    auto_call = types.AutomaticFunctionCallingConfig(disable=True)
    
    tools_config = types.GenerateContentConfig(tools=[is_even], automatic_function_calling=auto_call)

    prompt = "Is 9 even?"

    response = client.models.generate_content(model=MODEL, contents=prompt, config=tools_config)

    # Print the response from the model
    json_resp = response.to_json_dict()
    print(json.dumps(json_resp, sort_keys=True, indent=4))
    
    #manually calling the function
    fc = response.function_calls[0]
    print(f"Function called: {fc.name}")

    number = fc.args["number"]
    print(f"Argument passed to function: {number}")
    
    result = is_even(number)
    print("Function output:", result)

if __name__ == "__main__":
    main()  
    