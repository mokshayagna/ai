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
        {
            "item_id": "AM12345",
            "name": "iPhone 13",
            "quantity": 5
        },

        {
            "item_id": "AM54321",
            "name": "Samsung Galaxy S21",
            "quantity": 10
        },

        {
            "item_id": "AM67890",
            "name": "MacBook Pro",
            "quantity": 2
        }
    ]
    for item in amazon_items_quantity:
        if item["item_id"] == item_id:
            return item["quantity"]
    return "Item not found"


@tool
def amazon_item_with_discount(item_id: str, quantity: int) -> str:
    """Calculates discounted price if quantity is available"""
    amazon_items = [
        {
            "item_id": "AM12345",
            "name": "iPhone 13",
            "base_price": 5000,
            "discount": 10
        },

        {
            "item_id": "AM54321",
            "name": "Samsung Galaxy S21",
            "base_price": 3000,
            "discount": 15
        },

        {
            "item_id": "AM67890",
            "name": "MacBook Pro",
            "base_price": 2000,
            "discount": 5
        }
    ]
    for item in amazon_items:
        if item["item_id"].lower() == item_id.lower():
            price_per_unit = item["base_price"]
            discount = item["discount"]
            available_quantity = amazon_quantity_tool.invoke(
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