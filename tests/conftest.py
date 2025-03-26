import pytest
from common.token import get_token


@pytest.fixture(scope="session")
def auth_token():
    return get_token()
