from google import genai
from google.genai import types

def annual_income() -> int:
    print("in annual_income:")
    annual_profit = 10000
    annual_expenses = 5000
    net_annual_profit = 5000
    return net_annual_profit

def employee_bonus() -> str:
    print("in employee_bonus:")
    employees = [
        {"name": "Aarav", "rating": 9},
        {"name": "Diya", "rating": 8},
        {"name": "Rohan", "rating": 7},
    ]
    return employees

    
def main():
    client = genai.Client()
    
    model_name = "gemini-2.0-flash-001"
    
    prompt = """
    You are a financial analyst.
    1.net annual income will be given from the function annual_income. 
    2.Employee details with there name and rating will be there in employee_bonus function.
    3. Calculate the share for each employee based on their rating and net annual income.
    
    provide me the bonus details for each employee in the format:
    Employee Name: Bonus Amount
    """
    
    tools_config = types.GenerateContentConfig(tools=[annual_income, employee_bonus])
    response = client.models.generate_content(model=model_name, contents=prompt, config=tools_config)
    print(response.text)

    
if __name__ == "__main__":
    main()