import json
import time
import uuid
import requests
from jwcrypto import jwk, jwt
from configparser import ConfigParser


def load_config():
    config = ConfigParser()
    config.read("settings.ini")
    client_id = config.get("main", "client_id")

    with open("key.pem", "rb") as pem:
        key = jwk.JWK.from_pem(pem.read())

    return (client_id, key)


def generate_private_key_jwt(client_id, key):
    header = {"alg": "RS256", "kid": key.get("kid")}
    now = int(time.time())
    claims = {
        "sub": client_id,
        "iss": client_id,
        "aud": "https://api.snyk.io/oauth2/token",
        "jti": str(uuid.uuid4()),  # nonce to prevent replays
        "exp": now + 300,  # only valid for 5min. note this isn't the access-token exp
        "iat": now,
    }

    private_key_jwt = jwt.JWT(header=header, claims=claims)
    private_key_jwt.make_signed_token(key)

    return private_key_jwt


def fetch_access_token(private_key_jwt):
    url = "https://api.snyk.io/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": private_key_jwt.serialize(),
    }
    response = requests.post(url, data=payload)

    if response.status_code != 200:
        print(f"Token fetch failed with status {response.status_code}.")
        print(f"Response: {response.text}")

    json_response = json.loads(response.text)
    return json_response["access_token"]


if __name__ == "__main__":
    (client_id, key) = load_config()
    private_key_jwt = generate_private_key_jwt(client_id, key)
    access_token = fetch_access_token(private_key_jwt)

    print(access_token)
