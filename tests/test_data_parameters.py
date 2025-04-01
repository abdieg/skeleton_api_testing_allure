import pytest
import logging
from common.api_call import api_call


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Negative Test Scenarios

@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_uppercase_true_invalid():
    response = api_call(method="GET", endpoint="/person?is_employee=TRUE")
    assert response.status_code == 422


@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_capital_false_invalid():
    response = api_call(method="GET", endpoint="/person?is_employee=False")
    assert response.status_code == 422


@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_yes_invalid():
    response = api_call(method="GET", endpoint="/person?is_employee=yes")
    assert response.status_code == 422


@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_numeric_1_invalid():
    response = api_call(method="GET", endpoint="/person?is_employee=1")
    assert response.status_code == 422


@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_random_string_invalid():
    response = api_call(method="GET", endpoint="/person?is_employee=abc123")
    assert response.status_code == 422


@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_empty_value_invalid():
    response = api_call(method="GET", endpoint="/person?is_employee=")
    assert response.status_code == 422


@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_unexpected_query_param_rejected():
    response = api_call(method="GET", endpoint="/person?unexpected_param=true")
    assert response.status_code == 400
    assert "Unexpected query parameter" in response.json()["detail"]


@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_valid_param_with_unexpected_param():
    response = api_call(method="GET", endpoint="/person?is_employee=true&foo=bar")
    assert response.status_code == 400
    assert "Unexpected query parameter" in response.json()["detail"]


# Edge Case Test Scenarios

@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_encoded_space_invalid():
    response = api_call(method="GET", endpoint="/person?is_employee=true%20")
    assert response.status_code == 422


@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_leading_space_invalid():
    response = api_call(method="GET", endpoint="/person?is_employee= false")
    assert response.status_code == 422


@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_with_newline_invalid():
    response = api_call(method="GET", endpoint="/person?is_employee=True\n")
    assert response.status_code == 422


@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_duplicate_conflicting_values():
    response = api_call(method="GET", endpoint="/person?is_employee=true&is_employee=false")
    # FastAPI will take the last value by default in multi-query params unless specified.
    # This should still result in 200, but we test for behavior
    assert response.status_code == 200  # adjust based on actual API behavior


@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_null_value_invalid():
    response = api_call(method="GET", endpoint="/person?is_employee=null")
    assert response.status_code == 422


@pytest.mark.main
@pytest.mark.data_parameters
@pytest.mark.regression
def test_is_employee_wrong_case_param_name():
    response = api_call(method="GET", endpoint="/person?IS_EMPLOYEE=true")
    assert response.status_code == 400
    assert "Unexpected query parameter" in response.json()["detail"]
