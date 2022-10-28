import json
import os
import requests
from configparser import ConfigParser


def create_account():
    config_file = "settings.ini"

    if os.path.isfile(config_file) == False:
        print(f"Config missing: cp settings.template.ini {config_file}")
        print("See README.md for field explanations")
        return

    config = ConfigParser()
    config.read(config_file)
    api_token = config.get("main", "api_token")
    org_id = config.get("main", "org_id")
    role_id = config.get("main", "role_id")
    jwks_url = config.get("main", "jwks_url")

    url = f"https://api.snyk.io/rest/orgs/{org_id}/service_accounts?version=2022-07-08~experimental"
    headers = {
        "Authorization": f"token {api_token}",
        "Content-Type": "application/vnd.api+json",
    }
    payload = {
        "name": "Service-Account OAuth Demo",
        "auth_type": "oauth_private_key_jwt",
        "jwks_url": jwks_url,
        "role_id": role_id,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 201:
        print(f"Create service-account failed with status {response.status_code}.")
        print(f"Response: {response.text}")

    json_response = json.loads(response.text)

    # Note: these values _happen_ to be the same at the moment, but should be treated separately.
    service_account_id = json_response["data"]["id"]
    client_id = json_response["data"]["attributes"]["client_id"]

    config.set("main", "service_account_id", service_account_id)
    config.set("main", "client_id", client_id)
    with open(config_file, "w") as f:
        config.write(f)

    print("Service-account created successfully and stored in settings.ini")


if __name__ == "__main__":
    create_account()
