from google import genai
from google.genai import types

def is_even(number: int) -> bool:
    """Checks if a number is even."""
    return number % 2 == 0

def main():
    model_name = "gemini-2.0-flash-001"
    
    # Create client
    client = genai.Client()
    auto_call = types.AutomaticFunctionCallingConfig(disable=True)
    tools_config = types.GenerateContentConfig(tools=[is_even], automatic_function_calling=auto_call)
    
    prompt = "Is six even?"
    
    response = client.models.generate_content(model=model_name, contents=prompt, config=tools_config)
    
    data = response.to_json_dict() # this convert data to dict format
    print(type(data))
    print("\n")
   # print(data)
    
    candidate = data["candidates"][0]
    print("what is inside candidate\n")
    print(candidate)  # print the candidate inside the response, it contains part function_call and other details
    
    part = candidate["content"]["parts"][0]
    print("what is inside part\n")
    print(part)   #print contains the function call and its details like name and arguments passed to it
    
    if "function_call" in part:
        function_call = part["function_call"] #contains args,number and name of the function called by the model
    
        function_name = function_call["name"] # contains the name of the function called by the model
        print(function_name)
        arguments = function_call["args"] 
    
        number = arguments["number"] #
    
        print(f"Function called: {function_name}") #is_even
        print(f"Argument: {number}") #6
    else:
        print("No function call, model gave direct answer:")
        print(part.get("text"))
    
    user_output = is_even(number)
    print(f"Output of the function: {user_output}") 
    
    function_response_content = {
        "role": "user",   # NOTE: must be 'user' in new SDK
        "parts": [
            {
                "function_response": {
                    "name": function_name,
                    "response": {"result": user_output},
                }
            }
        ],
    }
    
    
    user_message = {
        "role": "user",
        "parts": [{"text": prompt}]
    }
    
    final_message = [user_message, function_response_content]
    response = client.models.generate_content(
        model=model_name,
        contents=[user_message, function_response_content]
    )
    print("Final response from model:")
    print(response.text)
       
if __name__ == "__main__":
    main()