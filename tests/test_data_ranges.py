from datetime import datetime
import pytest
import logging
from common.api_call import api_call


# ----------------------------------------------------------------------------------------------------------------------
# DATA RANGES SUITE
# To validate that key ranges are within the expected results.
# Remember that MIN, MIN-1, MAX and MAX+1 could also be validated although sometimes a mockup is needed.
# ----------------------------------------------------------------------------------------------------------------------


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def person_response():
    logger.info("Calling /person to retrieve data for range validation")
    response = api_call(method="GET", endpoint="/person")
    assert response.status_code == 200
    return response.json()


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
