import requests
from common import settings
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# def api_call(parameters, token):
#     headers = {'Authorization': f"Bearer {token}"}
#     response = requests.get(settings.endpoint + parameters, headers=headers)
#     return response


def api_call(method: str, endpoint: str, token: str = None, params=None, data=None, json=None, headers=None,
             timeout=10):
    """
    Generic API call function for use in tests.

    Args:
        method (str): HTTP method ('GET', 'POST', etc.)
        endpoint (str): Relative path or full URL.
        token (str, optional): Bearer token for Authorization header.
        params (dict, optional): Query parameters.
        data (dict, optional): Form-encoded data.
        json (dict, optional): JSON body.
        headers (dict, optional): Additional headers.
        timeout (int, optional): Request timeout in seconds.

    Returns:
        requests.Response: The raw response object (to be asserted in test).

    Raises:
        requests.RequestException or any HTTP error, allowing pytest to capture and assert as needed.
    """
    url = f"{settings.endpoint}{endpoint}" if not endpoint.startswith("http") else endpoint

    default_headers = {'Accept': 'application/json'}
    if token:
        default_headers['Authorization'] = f"Bearer {token}"

    if headers:
        default_headers.update(headers)

    response = requests.request(
        method=method.upper(),
        url=url,
        headers=default_headers,
        params=params,
        data=data,
        json=json,
        timeout=timeout
    )

    return response
