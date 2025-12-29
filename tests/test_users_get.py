import pytest
from src.fw.data_provider import load_test_cases, load_json
from src.fw.validators import assert_status, assert_response_time, assert_schema, assert_field_equals
import allure
from src.fw.allure_helpers import attach_response

schema = load_json("schemas/user.schema.json")

@pytest.mark.parametrize("tc", load_test_cases("data/users.json"), ids=lambda x: x["case"])
def test_get_user(client, cfg, tc):
    resp = client.get(f"/users/{tc['user_id']}")

    with allure.step("Attach response evidence"):
        attach_response(resp, "get-user")

    if tc["case"] == "missing_user":
        assert_status(resp.status_code, tc["expected_status"])
        return

    assert_status(resp.status_code, 200)
    assert_response_time(resp.elapsed_ms, cfg.response_time_threshold_ms)
    assert_schema(resp.json, schema)
    assert_field_equals(resp.json, "name", tc["expected_name"])
