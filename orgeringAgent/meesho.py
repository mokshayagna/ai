from langchain_core.tools import tool

def meesho_item_id_tool(item_name: str) -> str:
    """Retrieves item id from Amazon"""

    amazon_items = {
        "iPhone 13": "MS12345",
        "Samsung Galaxy S21": "MS54321",
        "MacBook Pro": "MS67890"
    }

    for item in amazon_items:
        if item.lower() == item_name.lower():
            return amazon_items[item]

    return "Item not found"

@tool
def meesho_quantity_tool(item_id: str) -> int:
    """Retrieves available quantity of the item from Meesho"""

    # Simulating quantity retrieval with random numbers for demonstration
    meesho_items_quantity = {
        "item_id": "MS12345","name": "iPhone 13", "quantity": 15,
        "item_id": "MS54321","name": "Samsung Galaxy S21", "quantity": 8,
        "item_id": "MS67890","name": "MacBook Pro", "quantity": 3
    }
    
    for item in meesho_items_quantity:
        if item["item_id"] == item_id:
            retval = item["quantity"]
            return retval
    return f"that much quantity not found but we have {item['quantity']} quantity available"


