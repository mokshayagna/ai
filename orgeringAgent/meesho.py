from langchain_core.tools import tool

def meesho_item_id_tool(item_name: str) -> str:
    """Retrieves item id from Amazon"""

    meesho_items = [
        {"item_id": "MS12345","name": "iPhone 13"},
        {"item_id": "MS54321","name": "Samsung Galaxy S21"},
        {"item_id": "MS67890","name": "MacBook Pro"}
    ]

    for item in meesho_items:
        if item["name"].lower() == item_name.lower():
            return item["item_id"]

    return "Item not found"

@tool
def meesho_quantity_tool(item_id: str) -> int:
    """Retrieves available quantity of the item from Meesho"""

    # Simulating quantity retrieval with random numbers for demonstration
    meesho_items_quantity = [
        {"item_id": "MS12345","name": "iPhone 13", "quantity": 1},
        {"item_id": "MS54321","name": "Samsung Galaxy S21", "quantity": 8},
        {"item_id": "MS67890","name": "MacBook Pro", "quantity": 3}
    ]
    
    for item in meesho_items_quantity:
        if item["item_id"] == item_id:
            retval = item["quantity"]
            return retval
    return f"that much quantity not found but we have {item['quantity']} quantity available"


