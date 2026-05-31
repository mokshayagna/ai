from composio import Composio

client = Composio()

print(
client.client.project.config
)

print()

print(
dir(
client.client.project.config
)
)