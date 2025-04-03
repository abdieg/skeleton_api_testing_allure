import os
from dotenv import load_dotenv


# Load .env file if it exists
load_dotenv()

# Default endpoints
default_ip = "127.0.0.1"
default_port = "11000"

# Load custom IPs and ports from environment variables if present
dev_ip = os.getenv("DEV_IP", default_ip)
qa_ip = os.getenv("QA_IP", default_ip)
prod_ip = os.getenv("PROD_IP", default_ip)

dev_port = os.getenv("DEV_PORT", default_port)
qa_port = os.getenv("QA_PORT", default_port)
prod_port = os.getenv("PROD_PORT", default_port)

# Construct endpoint URLs
endpoint_dev = f"http://{dev_ip}:{dev_port}"
endpoint_qa = f"http://{qa_ip}:{qa_port}"
endpoint_prod = f"http://{prod_ip}:{prod_port}"

# Get current environment from environment variable (default to 'qa')
env = os.getenv("TEST_ENV", "qa").lower()

# Dynamically choose the active endpoint
if env == "dev":
    endpoint = endpoint_dev
elif env == "prod":
    endpoint = endpoint_prod
else:
    endpoint = endpoint_qa


# API security token
security_token_qa = {
    "key": "abc",
    "secret": "def",
    "apiUrl": "http",
    "authVersion": "v1",
    "greetingsVersion": "v2",
    "salutationsVersion": "v2",
    "authHost": "http",
}
