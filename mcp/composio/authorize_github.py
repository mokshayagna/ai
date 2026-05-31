from composio import Composio

client = Composio()

# Step 1 — find github auth config
auth_configs = client.auth_configs.list()

print("Auth configs:")
print(auth_configs)