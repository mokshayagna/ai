from google import genai
from google.genai import types

def get_product_info(product_name: str) -> dict:
    """Get the stock amount and identifier for a given product"""
    print(f"get_product_info called with {product_name}")
    return {"id": "BPB-CBOOKS-KDP", "in_stock": "yes", "quantity": 120}

def get_store_location(location: str) -> dict:
    """Get the location of the closest store"""
    print(f"get_store_location called with {location}")
    pass

def place_order(product: str, address: str) -> dict:
    """Place an order"""
    print(f"place_order called with {product} and {address}")
    pass

def declare_functions():
    return [get_product_info, get_store_location, place_order]

def main():
    MODEL = "gemini-2.0-flash-001"

    client = genai.Client()
    retail_tools = declare_functions()

    tools_config = types.GenerateContentConfig(tools=retail_tools)

    prompt = "Do you have the book titled 'Let Us C'?"
    response = client.models.generate_content(model=MODEL, contents=prompt, config=tools_config)

    json_resp = response.to_json_dict()
    part = json_resp["candidates"][0]["content"]["parts"][0]
    print(f"==================={prompt}====================")
    print(f"Response:\n{part}")


if __name__ == "__main__":
    main()