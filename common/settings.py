import os


# API endpoint
endpoint_dev = "http://127.0.0.1:11000"
endpoint_qa = "http://127.0.0.1:11000"
endpoint_prod = "http://127.0.0.1:11000"

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
