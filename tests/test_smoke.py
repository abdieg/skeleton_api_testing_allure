import pytest
import logging
from common.api_call import api_call
from common import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.smoke
def test_health_check_return_200():
    """
    Smoke test to validate API is reachable and responding with 200 OK.
    """
    logger.debug(f"[test] Environment: {settings.env}")
    logger.debug(f"[test] Full URL tested: {settings.endpoint}/person")

    response = api_call(method="GET", endpoint="/person")
    logger.info(f"Received status code: {response.status_code}")
    assert response.status_code == 200
