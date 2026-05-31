from composio import Composio
import inspect

client = Composio()

print(
inspect.signature(
client.tools.get
)
)