import requests
import os

email = os.getenv("JIRA_USERNAME")
token = os.getenv("JIRA_API_TOKEN")
base_url = os.getenv("JIRA_BASE_URL")

resp = requests.get(
    f"{base_url}/rest/api/3/myself",
    auth=(email, token),
    headers={"Accept": "application/json"}
)

print(resp.status_code)
print(resp.text)