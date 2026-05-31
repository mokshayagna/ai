from composio import Composio

client = Composio()

config = client.client.project.config.retrieve()

print(config)