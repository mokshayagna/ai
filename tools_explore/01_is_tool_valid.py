from google import genai
from google.genai import types

def get_product_info(product_name: str) -> dict:
    """ Get the stock amount and identifier of the product. """
    pass

def get_store_location(store_name: str) -> dict:
    """ Get the location of the closest store. """
    pass

def place_order(product: str,address: str) -> dict:
    """ Place an order for the product to be delivered at the given address. """
    pass

def declare_functions():
    return [get_product_info, get_store_location, place_order]

def main():
    Model = "gemini-2.0-flash-001"
    client = genai.Client()
    
    retail_tools = declare_functions()
    
    auto_call = types.AutomaticFunctionCallingConfig(disable=True) 
    
    tool_Config = types.GenerateContentConfig(tools = retail_tools, automatic_function_calling = auto_call)
    
    prompt = "Do you have iphone 14 in stock? "
    
    response = client.models.generate_content(model = Model,contents=prompt, config=tool_Config)
    
    json_resp = response.to_json_dict()
    candidates = json_resp["candidates"][0]
    part = candidates["content"]["parts"][0]
    print(f"Response:\n")
    print(part)
    
if __name__ == "__main__":
    main()