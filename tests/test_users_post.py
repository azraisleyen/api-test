from src.fw.validators import assert_status, assert_schema
from src.fw.data_provider import load_json
import allure
from src.fw.allure_helpers import attach_response

schema = load_json("schemas/user.schema.json")

def test_create_user(client):
    payload = {"name": "Charlie", "age": 40}
    resp = client.post("/users", json_body=payload)

    with allure.step("Attach create-user response"):
        attach_response(resp, "create-user")
    assert_status(resp.status_code, 201)
    assert_schema(resp.json, schema)
