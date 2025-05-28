import pytest
import logging
import allure
from common.api_call import api_call
from common import settings


# ----------------------------------------------------------------------------------------------------------------------
# SMOKE SUITE
# To validate that API is up and running.
# ----------------------------------------------------------------------------------------------------------------------


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@allure.feature("Health-check endpoint")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.main
@pytest.mark.smoke
@pytest.mark.regression
def test_health_check_return_200():
    """
    Smoke test to validate API is reachable and responding with 200 OK.
    """
    allure.dynamic.parameter("env", settings.env)
    logger.debug(f"[test] Environment: {settings.env}")
    logger.debug(f"[test] Full URL tested: {settings.endpoint}/person")

    with allure.step("Send GET /person"):
        response = api_call(method="GET", endpoint="/person")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON
        )
    logger.info(f"Received status code: {response.status_code}")
    assert response.status_code == 200
