from composio import Composio

client = Composio()

accounts = client.connected_accounts.list()

print(accounts)