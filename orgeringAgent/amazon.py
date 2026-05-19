from langchain_core.tools import tool

@tool
def amazon_item_id_tool(item_name: str) -> str:
    """Retrieves item id from Amazon"""

    amazon_items = [
        {"item_id": "AM12345", "name": "iPhone 13"},
        {"item_id": "AM54321", "name": "Samsung Galaxy S21"},
        {"item_id": "AM67890", "name": "MacBook Pro"}
    ]

    for item in amazon_items:

        if item["name"].lower() == item_name.lower():

            return item["item_id"]

    return "Item not found"


@tool
def amazon_quantity_tool(item_id: str) -> int:
    """Retrieves available quantity of the item from Amazon"""

    amazon_items_quantity = [
        {"item_id": "AM12345", "name": "iPhone 13", "quantity": 5},
        {"item_id": "AM54321", "name": "Samsung Galaxy S21", "quantity": 10},
        {"item_id": "AM67890", "name": "MacBook Pro", "quantity": 2}
    ]

    for item in amazon_items_quantity:

        if item["item_id"] == item_id:

            return item["quantity"]

    return f"that much quantity not found but we have {item['quantity']} quantity available"