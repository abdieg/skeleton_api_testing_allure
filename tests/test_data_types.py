import pytest
import logging
from common.api_call import api_call


# ----------------------------------------------------------------------------------------------------------------------
# DATA TYPES SUITE
# To validate that each key returns its corresponding data type value. Per example, that a Salary field returns numeric
# values or a certain key returns boolean.
# ----------------------------------------------------------------------------------------------------------------------


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def person_response():
    logger.info("Calling /person to retrieve data for type validation")
    response = api_call(method="GET", endpoint="/person")
    assert response.status_code == 200
    return response.json()


# Top-level fields

@pytest.mark.main
@pytest.mark.data_types
@pytest.mark.regression
def test_name_is_string(person_response):
    assert isinstance(person_response["name"], str)


@pytest.mark.main
@pytest.mark.data_types
@pytest.mark.regression
def test_dob_is_string(person_response):
    assert isinstance(person_response["dob"], str)


@pytest.mark.main
@pytest.mark.data_types
@pytest.mark.regression
def test_email_is_string(person_response):
    assert isinstance(person_response["email"], str)


@pytest.mark.main
@pytest.mark.data_types
@pytest.mark.regression
def test_phone_is_string(person_response):
    assert isinstance(person_response["phone"], str)


@pytest.mark.main
@pytest.mark.data_types
@pytest.mark.regression
def test_address_is_string(person_response):
    assert isinstance(person_response["address"], str)


@pytest.mark.main
@pytest.mark.data_types
@pytest.mark.regression
def test_zip_code_is_string(person_response):
    assert isinstance(person_response["zip_code"], str)


@pytest.mark.main
@pytest.mark.data_types
@pytest.mark.regression
def test_is_employee_is_boolean(person_response):
    assert isinstance(person_response["is_employee"], bool)


@pytest.mark.main
@pytest.mark.data_types
@pytest.mark.regression
def test_salary_is_float(person_response):
    assert isinstance(person_response["salary"], float)


@pytest.mark.main
@pytest.mark.data_types
@pytest.mark.regression
def test_company_is_string(person_response):
    assert isinstance(person_response["company"], str)


# Equipment list and nested items

@pytest.mark.main
@pytest.mark.data_types
@pytest.mark.regression
def test_equipment_items_have_correct_types(person_response):
    equipment = person_response["equipment"]
    for idx, item in enumerate(equipment):
        assert isinstance(item, dict), f"Item {idx} is not a dict"
        assert isinstance(item.get("product"), str), f"Item {idx} 'product' is not str"
        assert isinstance(item.get("price"), float), f"Item {idx} 'price' is not float"
        assert isinstance(item.get("date_given"), str), f"Item {idx} 'date_given' is not str"
