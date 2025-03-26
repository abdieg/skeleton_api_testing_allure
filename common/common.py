import requests
import settings
import logging


# Optional: configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def api_call(parameters, token, timeout=10):
    url = f"{settings.endpoint}{parameters}"
    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/json'  # Good practice if expecting JSON
    }

    try:
        logger.info(f"Making API call to: {url}")
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise an error for bad status codes (4xx/5xx)
        return response
    except requests.exceptions.HTTPError as http_err:
        logger.error(
            f"HTTP error: {http_err} - Response: {http_err.response.text if http_err.response else 'No response'}")
    except requests.exceptions.Timeout:
        logger.error(f"Request to {url} timed out.")
    except requests.exceptions.RequestException as err:
        logger.error(f"Error during request to {url}: {err}")

    return None  # Return None if something failed
