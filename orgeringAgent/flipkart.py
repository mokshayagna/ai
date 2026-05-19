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
        {
            "item_id": "FK12345",
            "name": "iPhone 13",
            "quantity": 7
        },

        {
            "item_id": "FK54321",
            "name": "Samsung Galaxy S21",
            "quantity": 4
        },

        {
            "item_id": "FK67890",
            "name": "MacBook Pro",
            "quantity": 1
        }
    ]
    for item in flipkart_items_quantity:
        if item["item_id"] == item_id:
            return item["quantity"]

    return "Item not found"


@tool
def flipkart_item_with_discount(item_id: str,quantity: int) -> str:
    """Calculates discounted price for Flipkart items"""

    flipkart_items = [

        {
            "item_id": "FK12345",
            "name": "iPhone 13",
            "base_price": 5200,
            "discount": 12
        },

        {
            "item_id": "FK54321",
            "name": "Samsung Galaxy S21",
            "base_price": 3200,
            "discount": 18
        },

        {
            "item_id": "FK67890",
            "name": "MacBook Pro",
            "base_price": 2100,
            "discount": 7
        }
    ]

    for item in flipkart_items:
        if item["item_id"].lower() == item_id.lower():
            price_per_unit = item["base_price"]
            discount = item["discount"]
            available_quantity = flipkart_quantity_tool.invoke(
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