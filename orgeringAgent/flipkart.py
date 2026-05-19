import random
from langchain_core.tools import tool

@tool
def flipkart_item_id_tool(item_name: str) -> str:
    """Retrieves item id from Flipkart"""

    flipkart_items = {
        "iPhone 13": "FK12345",
        "Samsung Galaxy S21": "FK54321",
        "MacBook Pro": "FK67890"
    }

    for item in flipkart_items:
        if item.lower() == item_name.lower():
            return flipkart_items[item]

    return "Item not found"

@tool
def flipkart_quantity_tool(item_id: str) -> int:
    """Retrieves available quantity of the item from Flipkart"""

    # Simulating quantity retrieval with random numbers for demonstration
    flipkart_items_quantity = {
        "item_id": "FK12345","name": "iPhone 13", "quantity": 10,
        "item_id": "FK54321","name": "Samsung Galaxy S21", "quantity": 5,
        "item_id": "FK67890","name": "MacBook Pro", "quantity": 2
    }
    
    for item in flipkart_items_quantity:
        if item["item_id"] == item_id:
            retval = item["quantity"]
            return retval
    return f"that much quantity not found but we have {item['quantity']} quantity available"

