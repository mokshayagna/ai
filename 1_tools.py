from google import genai
from google.genai import types

def addition(a:int , b:int) -> int :
    """adds 2 integers which are derived from different sources   and then returns a int which is a sum of the 2 arguments """
    return a+ b
 
def subtraction(a: int, b: int) -> int:
    """subtracts 2 integers which are derived from different sources and then returns a int which is the difference of the 2 arguments"""
    return a - b


def multiplication(a: int, b: int) -> int:
    """multiplies 2 integers which are derived from different sources and then returns a int which is the product of the 2 arguments"""
    return a * b


def division(a: int, b: int) -> int:
    """divides 2 integers which are derived from different sources and then returns a int which is the quotient of the 2 arguments"""
    return a / b

def declare_functions():
    # In new SDK, just return Python functions directly
    return [addition,subtraction,multiplication,division]

def main():
    # MODEL = "gemini-3.1-flash-image-preview"
    MODEL = "gemini-2.0-flash-001"
    client = genai.Client()
    # client=genai.Client()
    print(client)
    cal_tools=declare_functions()
    print(cal_tools)
    auto_call=types.AutomaticFunctionCallingConfig(disable=True)
    print(auto_call)
    tools_config=types.GenerateContentConfig(tools=cal_tools,automatic_function_calling=auto_call)
    print("\n\n\n\n tools_config : ",tools_config,"\n\n\n\n")
    prompt="can you add seven and 8"
    response=client.models.generate_content(model=MODEL,contents=prompt,config=tools_config)
    print(response)
    json_resp=response.to_json_dict()
    print("\n\n",json_resp)
    
    candidate = json_resp["candidates"][0]
    part = candidate["content"]["parts"][0]

    print(f"Response:\n{part}")
if __name__ == "__main__":
    main()