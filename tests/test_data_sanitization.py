import pytest
import logging
from common.api_call import api_call


# ----------------------------------------------------------------------------------------------------------------------
# DATA SANITIZATION SUITE
# To validate if API sanitizes inputs for query and URL params, payloads, database and system injections like SQL.
# ----------------------------------------------------------------------------------------------------------------------


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.main
@pytest.mark.data_sanitization
@pytest.mark.regression
def test_query_param_sql_injection_attempt():
    """
    Attempt SQL injection through 'is_employee' query param.
    """
    malicious_value = "' OR '1'='1"
    response = api_call(method="GET", endpoint=f"/person?is_employee={malicious_value}")
    logger.debug(f"Response: {response.status_code}")
    assert response.status_code in (400, 422)  # Should be rejected


@pytest.mark.main
@pytest.mark.data_sanitization
@pytest.mark.regression
def test_query_param_script_injection():
    """
    Attempt script injection through query param.
    """
    malicious_value = "<script>alert('XSS')</script>"
    response = api_call(method="GET", endpoint=f"/person?is_employee={malicious_value}")
    assert response.status_code in (400, 422)


# Asuming another endpoint like /user/{id}
# def test_url_param_sql_injection():
#     response = api_call(method="GET", endpoint="/user/1 OR 1=1")
#     assert response.status_code in (400, 404, 422)  # Should not return sensitive data


# When there is a POST
# def test_payload_with_sql_injection_in_text_field():
#     payload = {
#         "name": "Robert'); DROP TABLE Students;--",
#         "email": "user@example.com"
#     }
#     response = api_call(method="POST", endpoint="/user", json=payload)
#     assert response.status_code in (400, 422)


# JSON encoding example
# def test_payload_with_encoded_script_tag():
#     payload = {
#         "name": "%3Cscript%3Ealert('XSS')%3C%2Fscript%3E",
#         "email": "xss@example.com"
#     }
#     response = api_call(method="POST", endpoint="/user", json=payload)
#     assert response.status_code in (400, 422)
