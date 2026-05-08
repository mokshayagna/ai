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

    # Create client
    client = genai.Client()

    retail_tools = declare_functions()  # Declared but not used (same as original)

    auto_call = types.AutomaticFunctionCallingConfig(disable=True)
    tools_config = types.GenerateContentConfig(tools=retail_tools, automatic_function_calling=auto_call)

    prompt = "Do you have the book titled 'Let Us C'?"

    response = client.models.generate_content(model=MODEL, contents=prompt, config=tools_config)
    json_resp = response.to_json_dict()
    candidate = json_resp["candidates"][0]
    part = candidate["content"]["parts"][0]
    print(f"Response1:\n{part}")

    response = client.models.generate_content(model=MODEL, contents=prompt)
    json_resp = response.to_json_dict()
    candidate = json_resp["candidates"][0]
    part = candidate["content"]["parts"][0]
    print(f"Response2:\n{part}")


if __name__ == "__main__":
    main()