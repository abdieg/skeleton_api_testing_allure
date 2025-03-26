import requests
from requests.auth import HTTPBasicAuth
import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    consumer_key = settings.security_token_qa['key']
    consumer_secret = settings.security_token_qa['secret']
    authHost = settings.security_token_qa['authHost']
    authVersion = settings.security_token_qa['authVersion']
    greetingsVersion = settings.security_token_qa['greetingsVersion']
    salutationsVersion = settings.security_token_qa['salutationsVersion']
except (AttributeError, KeyError) as e:
    logger.error(f"Error loading settings: {e}")
    raise


def get_token():
    data = {
        "grant_type": "client_credentials",
        "authVersion": authVersion,
        "greetingsVersion": greetingsVersion,
        "salutationsVersion": salutationsVersion
    }

    try:
        response = requests.post(
            f"{authHost}/oauth2/default/v1/token",
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
            data=data,
            timeout=20  # timeout for robustness
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        err_response = http_err.response.text if http_err.response else 'No response'
        logger.error(f"HTTP error occurred: {http_err} - Response: {err_response}")
        return None
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error: {req_err}")
        return None

    try:
        token_response = response.json()
        access_token = token_response.get("access_token")
        if not access_token:
            logger.warning("Access token not found in response.")
        return access_token
    except ValueError as json_err:
        logger.error(f"JSON decode error: {json_err}")
        return None
