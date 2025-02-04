import json
import requests
import argparse
import time

# Define API version, URL base and Delay
API_VERSION = "2024-08-22"
API_BASE_URL = "https://api.snyk.io"
RATE_LIMIT_DELAY = 0.2


# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--group", required=True, help="Group ID")
parser.add_argument("--token", required=True, help="API token")
args = parser.parse_args()

def get_organizations(group_id, api_key):
    url = f"{API_BASE_URL}/rest/groups/{group_id}/orgs?version={API_VERSION}&limit=100"
    headers = {"accept": "application/vnd.api+json", "authorization": f"{api_key}"}
    organizations = []
    
    while url:
        response = requests.get(url, headers=headers)
        data = response.json()
        organizations.extend(data["data"])

        time.sleep(RATE_LIMIT_DELAY)

        # Check for next page link
        links = data.get("links", {})
        url = links.get("next")

        if url and not url.startswith("https://"):
            url = f"{API_BASE_URL}{url}"

    return organizations


def get_integrations(org_id, api_key):
    url = f"{API_BASE_URL}/v1/org/{org_id}/integrations"
    headers = { "Content-Type": "application/json; charset=utf-8", "Authorization": f"token {api_key}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    return data

if __name__ == "__main__":
    group_id = args.group
    api_key = args.token

    organizations = get_organizations(group_id, api_key)
    integrations = []

    for org in organizations:
        org_name = org["attributes"]["name"]
        org_id = org["id"]
        integrations = get_integrations(org_id, api_key)
        github_id = integrations['github']

        print(f"Snyk Org Name: {org_name} - Org ID: {org_id} - GH Integration ID: {github_id}")

