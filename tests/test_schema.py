import pytest
import logging
from common.api_call import api_call
from common import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Expected structure
EXPECTED_TOP_LEVEL_KEYS = {
    "name",
    "dob",
    "email",
    "phone",
    "address",
    "zip_code",
    "is_employee",
    "salary",
    "company",
    "equipment"
}

EXPECTED_EQUIPMENT_KEYS = {
    "product",
    "price",
    "date_given"
}


@pytest.mark.main
@pytest.mark.schema
@pytest.mark.regression
def test_person_root_structure_only():
    """
    Validate that the /person response contains the expected top-level keys.
    """
    logger.info("Calling /person with no parameters")
    response = api_call(method="GET", endpoint="/person")

    logger.info(f"Status code: {response.status_code}")
    assert response.status_code == 200

    data = response.json()

    logger.info(f"Top-level keys received: {set(data.keys())}")
    assert set(data.keys()) == EXPECTED_TOP_LEVEL_KEYS


@pytest.mark.main
@pytest.mark.schema
@pytest.mark.regression
def test_person_equipment_structure_only():
    """
    Validate the structure of the 'equipment' field in the /person response.
    """
    logger.info("Calling /person with no parameters to check 'equipment' field")
    response = api_call(method="GET", endpoint="/person")

    logger.info(f"Status code: {response.status_code}")
    assert response.status_code == 200

    data = response.json()
    equipment = data.get("equipment")

    logger.info(f"'equipment' field type: {type(equipment)}")
    assert isinstance(equipment, list)
    assert 1 <= len(equipment) <= 5

    for idx, item in enumerate(equipment):
        logger.debug(f"Validating equipment item {idx + 1}: {item}")
        assert isinstance(item, dict)
        assert set(item.keys()) == EXPECTED_EQUIPMENT_KEYS


@pytest.mark.main
@pytest.mark.schema
@pytest.mark.parametrize("is_employee_param", [None, "true", "false"])
def test_person_is_employee_param(is_employee_param):
    """
    Validate the /person API response schema with and without query params.
    """
    params = f"?is_employee={is_employee_param}" if is_employee_param else ""
    logger.debug(f"Calling /person{params}")
    response = api_call(method="GET", endpoint=f"/person{params}")

    logger.info(f"Status code: {response.status_code}")
    assert response.status_code == 200

    data = response.json()

    # Validate top-level structure
    logger.debug(f"Top-level keys: {data.keys()}")
    assert set(data.keys()) == EXPECTED_TOP_LEVEL_KEYS

    # Validate individual fields
    assert isinstance(data["name"], str)
    assert isinstance(data["dob"], str)
    assert isinstance(data["email"], str)
    assert isinstance(data["phone"], str)
    assert isinstance(data["address"], str)
    assert isinstance(data["zip_code"], str)
    assert isinstance(data["is_employee"], bool)
    assert isinstance(data["salary"], float)
    assert isinstance(data["company"], str)

    # Validate equipment list
    equipment = data["equipment"]
    logger.debug(f"Equipment items count: {len(equipment)}")
    assert isinstance(equipment, list)
    assert 1 <= len(equipment) <= 5

    for item in equipment:
        assert set(item.keys()) == EXPECTED_EQUIPMENT_KEYS
        assert isinstance(item["product"], str)
        assert isinstance(item["price"], float)
        assert isinstance(item["date_given"], str)
