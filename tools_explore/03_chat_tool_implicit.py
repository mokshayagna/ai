from google import genai
from google.genai import types

def get_product_info(product_name: str) -> dict:
    """Get the stock amount and identifier for a given product"""
    print(f"get_product_info called with {product_name}")
    return {"sku": "BPB-CBOOKS-KDP", "in_stock": "yes"}

def get_store_location(location: str) -> dict:
    """Get the location of the closest store"""
    print(f"get_store_location called with {location}")
    return {"store": "77/1, Marathahalli, Bengaluru, 560103, IND"}

def place_order(product: str, address: str) -> dict:
    """Place an order"""
    print(f"place_order called with {product} and {address}")
    return {"order_id": "ORD-12345", "status": "confirmed"}

def declare_functions():
    return [get_product_info, get_store_location, place_order]

def main():
    Model_name = "gemini-2.0-flash-001"
    
    client = genai.Client()
    
    tools = declare_functions()
    tools_config = types.GenerateContentConfig(tools=tools)
    
    chat = client.chats.create(model=Model_name)
    
    prompt = """Do you have the book titled 'Let Us C' available at your Outer Ring Road, Marathahalli branch? 
    I'd like to visit and also have it shipped to 6th Cross, Ambedkar Nagar, Sarjapur Road, Bengaluru - 560035, India."""
    
    response = chat.send_message(prompt, config=tools_config) 
    
    print(f"Final Response:\n{response.text}")
if __name__ == "__main__":
    main()