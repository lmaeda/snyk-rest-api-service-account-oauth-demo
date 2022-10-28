import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import os.path
from jwcrypto import jwk

PEM_FILE = "key.pem"


class JWKSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open(PEM_FILE, "rb") as pem:
            key = jwk.JWK.from_pem(pem.read())

        public_key = key.export_public(as_dict=True)
        public_key["use"] = "sig"
        jwks = {"keys": [public_key]}

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(jwks).encode())


def generate_key():
    if os.path.isfile(PEM_FILE):
        print(f"Using existing private key: {PEM_FILE}")
        return

    print(f"Generating private key: {PEM_FILE}")
    key = jwk.JWK.generate(kty="RSA", size=2048)

    with open(PEM_FILE, "wb") as pem:
        pem.write(key.export_to_pem(private_key=True, password=None))


def run_server():
    server_address = ("localhost", 9090)
    print(f"JWKS endpoint running on: {server_address}")
    print("Next step: expose this to the world via TLS! See README.md")

    httpd = HTTPServer(server_address, JWKSHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    generate_key()
    run_server()
