from google import genai
from google.genai import types


def get_product_info(product_name: str) -> dict:
    """Get the stock amount and identifier for a given product"""
    pass

def get_store_location(location: str) -> dict:
    """Get the location of the closest store"""
    pass

def place_order(product: str, address: str) -> dict:
    """Place an order"""
    pass

def declare_functions():
    return [get_product_info, get_store_location, place_order]

def main():
    MODEL = "gemini-2.0-flash-001"
    
    client = genai.Client()

    retail_tools = declare_functions()
    auto_call = types.AutomaticFunctionCallingConfig(disable=True)
    tools_config = types.GenerateContentConfig(tools=retail_tools, automatic_function_calling=auto_call)

    # This prompt does NOT match any of the declared tools —
    # model should respond with plain text instead of a function_call
    prompt = "What is the average temperature in Kadapa?"
    response = client.models.generate_content(model=MODEL, contents=prompt, config=tools_config)

    json_resp = response.to_json_dict()
    part = json_resp["candidates"][0]["content"]["parts"][0]
    print(f"==================={prompt}====================")
    print(f"Response:\n{part}")

if __name__ == "__main__":
    main()
    