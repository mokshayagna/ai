import random
from langchain_core.tools import tool
@tool
def flipkart_item_id_tool(item_name: str) -> str:
    """Retrieves item id from Flipkart"""

    flipkart_items = [
        {"item_id": "FK12345", "name": "iPhone 13"},
        {"item_id": "FK54321", "name": "Samsung Galaxy S21"},
        {"item_id": "FK67890", "name": "MacBook Pro"}
    ]

    for item in flipkart_items:

        if item["name"].lower() == item_name.lower():

            return item["item_id"]

    return "Item not found"


@tool
def flipkart_quantity_tool(item_id: str) -> int:
    """Retrieves available quantity of the item from Flipkart"""

    flipkart_items_quantity = [
        {"item_id": "FK12345", "name": "iPhone 13", "quantity": 7},
        {"item_id": "FK54321", "name": "Samsung Galaxy S21", "quantity": 4},
        {"item_id": "FK67890", "name": "MacBook Pro", "quantity": 1}
    ]

    for item in flipkart_items_quantity:

        if item["item_id"] == item_id:

            return item["quantity"]
    return f"that much quantity not found but we have {item['quantity']} quantity available"

