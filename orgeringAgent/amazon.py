from langchain_core.tools import tool
@tool
def amazon_item_id_tool(item_name: str) -> str:
    """Retrieves item id from Amazon"""

    amazon_items = {
        "iPhone 13": "AM12345",
        "Samsung Galaxy S21": "AM54321",
        "MacBook Pro": "AM67890"
    }

    for item in amazon_items:
        if item.lower() == item_name.lower():
            return amazon_items[item]

    return "Item not found"

@tool
def amazon_quantity_tool(item_id: str) -> int:
    """Retrieves available quantity of the item from Amazon"""

    # Simulating quantity retrieval with random numbers for demonstration
    amazon_items_quantity = {
        "item_id": "AM12345","name": "iPhone 13", "quantity": 15,
        "item_id": "AM54321","name": "Samsung Galaxy S21", "quantity": 8,
        "item_id": "AM67890","name": "MacBook Pro", "quantity": 3
    }
    
    for item in amazon_items_quantity:
        if item["item_id"] == item_id:
            retval = item["quantity"]
            return retval
    return f"that much quantity not found but we have {item['quantity']} quantity available"

