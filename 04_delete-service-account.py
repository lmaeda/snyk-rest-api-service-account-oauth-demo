import json
import requests
from configparser import ConfigParser


def delete_account():
    config_file = "settings.ini"

    config = ConfigParser()
    config.read(config_file)
    api_token = config.get("main", "api_token")
    org_id = config.get("main", "org_id")
    service_account_id = config.get("main", "service_account_id")

    url = f"https://api.snyk.io/rest/orgs/{org_id}/service_accounts/{service_account_id}?version=2022-07-08~experimental"
    headers = {
        "Authorization": f"token {api_token}",
        "Content-Type": "application/vnd.api+json",
    }

    response = requests.delete(url, headers=headers)

    if response.status_code != 204:
        print(f"Delete service-account failed with status {response.status_code}.")
        print(f"Response: {response.text}")

    print("Service-account deleted successfully")


if __name__ == "__main__":
    delete_account()
