from common.api_call import api_call


def test_health_check_return_200():
    """
    Smoke test to validate API is reachable and responding with 200 OK.
    """
    response = api_call(method="GET", endpoint="/person")
    assert response.status_code == 200
