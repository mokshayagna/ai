from composio import Composio

client = Composio()

# Step 1: List auth configs
configs = client.auth_configs.list()

print(configs)