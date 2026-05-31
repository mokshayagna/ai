from composio import Composio

client = Composio()

toolkits = client.toolkits.list()

for toolkit in toolkits.items:
    if "github" in toolkit.slug.lower():
        print(toolkit)