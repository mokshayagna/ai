from google import genai
from google.genai import types

def get_product_info(product_name: str) -> dict:
    """Get the stock amount and identifier for a given product"""
    print(f"get_product_info called with {product_name}")
    pass

def get_store_location(location: str) -> dict:
    """Get the location of the closest store"""
    print(f"get_store_location called with {location}")
    pass

def place_order(product: str, address: str) -> dict:
    """Place an order"""
    print(f"place_order called with {product} and {address}")
    pass

def declare_functions():
    # New SDK: just return functions
    return [get_product_info, get_store_location, place_order]

def init_chat():
    client = genai.Client()
    chat_history = []
    tools = declare_functions()

    tools_config = types.GenerateContentConfig(tools=tools)

    return client, chat_history, tools_config

def send_message(client, chat_history, prompt, tools_config):
    # Add user message
    data = {
        "role": "user", 
        "parts": [{"text": prompt}]
        }
    chat_history.append(data)
    
    print("chat_history :", chat_history)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=chat_history,
        config=tools_config
    )

    json_resp = response.to_json_dict()
    candidate = json_resp["candidates"][0]
    content = candidate["content"]

    # Add model response to history (important for context)
    chat_history.append(content)

    part = content["parts"][0]
    return part

def main():
    client, chat_history, tools_config = init_chat()

    prompt = "Do you have the book titled 'Let Us C'?"
    part = send_message(client, chat_history, prompt, tools_config)
    print(f"==================={prompt}====================")
    print(f"response :\n{part}")

    prompt = "Share me store in Kadapa, AP that I can visit to try one out?"
    part = send_message(client, chat_history, prompt, tools_config)
    print(f"==================={prompt}====================")
    print(f"response :\n{part}")

    prompt = "What is the nearest store in Kadapa, AP?"
    part = send_message(client, chat_history, prompt, tools_config)
    print(f"==================={prompt}====================")
    print(f"response :\n{part}")


if __name__ == "__main__":
    main()