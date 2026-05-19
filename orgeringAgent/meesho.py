from langchain_core.tools import tool

@tool
def meesho_item_id_tool(item_name: str) -> str:
    """Retrieves item id from Meesho"""
    meesho_items = [
        {"item_id": "MS12345", "name": "iPhone 13"},

        {"item_id": "MS54321", "name": "Samsung Galaxy S21"},

        {"item_id": "MS67890", "name": "MacBook Pro"}
    ]
    for item in meesho_items:
        if item["name"].lower() == item_name.lower():
            return item["item_id"]
    return "Item not found"


@tool
def meesho_quantity_tool(item_id: str) -> int:
    """Retrieves available quantity of the item from Meesho"""
    meesho_items_quantity = [
        {
            "item_id": "MS12345",
            "name": "iPhone 13",
            "quantity": 5
        },

        {
            "item_id": "MS54321",
            "name": "Samsung Galaxy S21",
            "quantity": 8
        },

        {
            "item_id": "MS67890",
            "name": "MacBook Pro",
            "quantity": 3
        }
    ]
    for item in meesho_items_quantity:
        if item["item_id"] == item_id:
            return item["quantity"]
    return "Item not found"


@tool
def meesho_item_with_discount(item_id: str,quantity: int) -> str:
    """Calculates discounted price for Meesho items"""
    meesho_items = [
        {
            "item_id": "MS12345",
            "name": "iPhone 13",
            "base_price": 4800,
            "discount": 8
        },

        {
            "item_id": "MS54321",
            "name": "Samsung Galaxy S21",
            "base_price": 2800,
            "discount": 14
        },

        {
            "item_id": "MS67890",
            "name": "MacBook Pro",
            "base_price": 1900,
            "discount": 6
        }
    ]
    for item in meesho_items:
        if item["item_id"].lower() == item_id.lower():
            price_per_unit = item["base_price"]
            discount = item["discount"]
            available_quantity = meesho_quantity_tool.invoke(
                {"item_id": item["item_id"]}
            )
            if quantity > available_quantity:
                return (
                    f"Only {available_quantity} units of "
                    f"{item['name']} are available."
                )
            total_price = price_per_unit * quantity
            discount_amount = total_price * (discount / 100)
            final_price = total_price - discount_amount
            return (
                f"Item: {item['name']}\n"
                f"Price per unit: {price_per_unit}\n"
                f"Requested Quantity: {quantity}\n"
                f"Discount: {discount}%\n"
                f"Final Price: {final_price}"
            )
    return "Item not found"