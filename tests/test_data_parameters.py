import logging

import pytest
import allure

from common.api_call import api_call
from common import settings


# ----------------------------------------------------------------------------------------------------------------------
# DATA PARAMETERS SUITE
# To validate that API returns the right response code for optional vs required parameters.
# It can also contain a mix of wrong parameters to validate right response.
# ----------------------------------------------------------------------------------------------------------------------


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Negative Test Scenarios

@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_uppercase_true_invalid():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?is_employee=TRUE"):
        response = api_call(method="GET", endpoint="/person?is_employee=TRUE")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    assert response.status_code == 422


@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_capital_false_invalid():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?is_employee=False"):
        response = api_call(method="GET", endpoint="/person?is_employee=False")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    assert response.status_code == 422


@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_yes_invalid():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?is_employee=yes"):
        response = api_call(method="GET", endpoint="/person?is_employee=yes")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    assert response.status_code == 422


@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_numeric_1_invalid():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?is_employee=1"):
        response = api_call(method="GET", endpoint="/person?is_employee=1")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    assert response.status_code == 422


@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_random_string_invalid():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?is_employee=abc123"):
        response = api_call(method="GET", endpoint="/person?is_employee=abc123")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    assert response.status_code == 422


@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_empty_value_invalid():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?is_employee="):
        response = api_call(method="GET", endpoint="/person?is_employee=")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    assert response.status_code == 422


@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_unexpected_query_param_rejected():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?unexpected_param=true"):
        response = api_call(method="GET", endpoint="/person?unexpected_param=true")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    assert response.status_code == 400
    assert "Unexpected query parameter" in response.json()["detail"]


@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_valid_param_with_unexpected_param():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?is_employee=true&foo=bar"):
        response = api_call(method="GET", endpoint="/person?is_employee=true&foo=bar")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    assert response.status_code == 400
    assert "Unexpected query parameter" in response.json()["detail"]


# Edge Case Test Scenarios

@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_encoded_space_invalid():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?is_employee=true%20"):
        response = api_call(method="GET", endpoint="/person?is_employee=true%20")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    assert response.status_code == 422


@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_leading_space_invalid():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?is_employee= false"):
        response = api_call(method="GET", endpoint="/person?is_employee= false")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    assert response.status_code == 422


@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_with_newline_invalid():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?is_employee=True\\n"):
        response = api_call(method="GET", endpoint="/person?is_employee=True\n")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    assert response.status_code == 422


@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_duplicate_conflicting_values():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?is_employee=true&is_employee=false"):
        response = api_call(method="GET", endpoint="/person?is_employee=true&is_employee=false")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    # FastAPI will take the last value by default in multi-query params unless specified.
    # This should still result in 200, but we test for behavior
    assert response.status_code == 200  # adjust based on actual API behavior


@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_null_value_invalid():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?is_employee=null"):
        response = api_call(method="GET", endpoint="/person?is_employee=null")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    assert response.status_code == 422


@allure.feature("Data parameter validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_wrong_case_param_name():
    allure.dynamic.parameter("env", settings.env)
    with allure.step("GET /person?IS_EMPLOYEE=true"):
        response = api_call(method="GET", endpoint="/person?IS_EMPLOYEE=true")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )
    assert response.status_code == 400
    assert "Unexpected query parameter" in response.json()["detail"]
