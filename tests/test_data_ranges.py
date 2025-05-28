from datetime import datetime
import logging

import pytest
import allure

from common.api_call import api_call
from common import settings


# ----------------------------------------------------------------------------------------------------------------------
# DATA RANGES SUITE
# To validate that key ranges are within the expected results.
# Remember that MIN, MIN-1, MAX and MAX+1 could also be validated although sometimes a mockup is needed.
# ----------------------------------------------------------------------------------------------------------------------


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def person_response():
    """Retrieve /person response for range‑validation tests."""
    allure.dynamic.parameter("env", settings.env)

    with allure.step("GET /person"):
        response = api_call(method="GET", endpoint="/person")
        allure.attach(
            str(response.json()),
            name="response-body",
            attachment_type=allure.attachment_type.JSON,
        )

    assert response.status_code == 200
    return response.json()


@allure.feature("Data range validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_ranges
@pytest.mark.regression
def test_dob_is_within_age_range(person_response):
    """
    Validate that 'dob' results in an age between 18 and 90 years.
    """
    dob_str = person_response["dob"]
    dob = datetime.strptime(dob_str, "%Y-%m-%d")
    today = datetime.today()
    age = (today - dob).days // 365

    logger.debug(f"Calculated age: {age}")
    assert 18 <= age <= 90


@allure.feature("Data range validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_ranges
@pytest.mark.regression
def test_salary_is_within_expected_range(person_response):
    """
    Validate that 'salary' is between 15,000 and 120,000.
    """
    salary = person_response["salary"]
    logger.debug(f"Salary: {salary}")
    assert 15000 <= salary <= 120000


@allure.feature("Data range validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_ranges
@pytest.mark.regression
def test_equipment_list_length_is_between_1_and_5(person_response):
    """
    Validate that 'equipment' list has between 1 and 5 items.
    """
    equipment = person_response["equipment"]
    logger.debug(f"Equipment count: {len(equipment)}")
    assert 1 <= len(equipment) <= 5


@allure.feature("Data range validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_ranges
@pytest.mark.regression
def test_equipment_price_is_within_expected_range(person_response):
    """
    Validate that each 'equipment.price' is between 10 and 500.
    """
    for idx, item in enumerate(person_response["equipment"]):
        price = item["price"]
        logger.debug(f"Item {idx} - price: {price}")
        assert 10 <= price <= 500


@allure.feature("Data range validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.main
@pytest.mark.data_ranges
@pytest.mark.regression
def test_equipment_date_given_is_in_current_decade(person_response):
    """
    Validate that each 'equipment.date_given' is within the current decade.
    """
    current_year = datetime.today().year
    decade_start = current_year - (current_year % 10)
    decade_end = decade_start + 9

    for idx, item in enumerate(person_response["equipment"]):
        date_str = item["date_given"]
        year = datetime.strptime(date_str, "%Y-%m-%d").year
        logger.debug(f"Item {idx} - date_given year: {year}")
        assert decade_start <= year <= decade_end
