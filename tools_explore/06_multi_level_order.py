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
    MODEL = "gemini-2.0-flash-001"
    client = genai.Client()

    retail_tools = declare_functions()
    tools_config = types.GenerateContentConfig(tools=retail_tools)

    prompt = """Do you have the book titled 'Let Us C' available at your Outer Ring Road, Marathahalli branch? 
    I'd like to visit and also have it shipped to 6th Cross, Ambedkar Nagar, Sarjapur Road, Bengaluru - 560035, India.
    if stock available place order for above address"""
    
    prompt = """Do you have the book titled 'Let Us C' available at your Outer Ring Road, Marathahalli branch? 
    where is book available?I'd like to visit and also have it shipped to 6th Cross, Ambedkar Nagar, Sarjapur Road, Bengaluru - 560035, India.
    if stock available place order 45 books for above address
    
    [Instruction]
    1. Check the stock availability before ordering.
    2. If the sufficient stock is available, Place the order to above addresses
    3. otherwise, place whatever quantity is available in stock.
    4. Make sure to quantify the order with the quantity mentioned in the prompt should match
    or available in stock. Do not place order without quantity.
    5. At the end tell me what is available in stock after placing the order and what is the order id and status for each order placed.     
    """
    
    response = client.models.generate_content(model=MODEL, contents=prompt, config=tools_config)

    print(f"Final Response:\n{response.text}")

if __name__ == "__main__":
    main()
