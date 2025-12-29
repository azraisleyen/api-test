import pytest
from src.fw.validators import assert_status
import allure
from src.fw.allure_helpers import attach_response

@pytest.mark.parametrize("payload", [
    {"name": "", "age": 10},      # invalid name
    {"name": "X", "age": -1},     # invalid age
    {"name": "Y", "age": 999},    # invalid age
])
def test_create_user_negative(client, payload):
    resp = client.post("/users", json_body=payload)
    with allure.step("Attach negative create-user response"):
        attach_response(resp, "create-user-negative")
    # FastAPI validation -> 422
    assert_status(resp.status_code, 422)
