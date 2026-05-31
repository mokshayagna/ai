from composio import Composio

client = Composio()

response = client.connected_accounts.link(
    user_id="default",
    auth_config_id="ac_EG4B6ayFj5y2"
)

print("\nOpen this URL:\n")
print(response.redirect_url)