from composio import Composio

client = Composio()

print("API Loaded")

print(client.client.api_key)

print()

print(client.toolkits.list())
