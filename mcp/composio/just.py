from composio import Composio

client = Composio()

print("Connected Accounts:")

accounts = client.connected_accounts.list()

print(accounts)