from src.fw.validators import assert_status, assert_schema, assert_field_equals
from src.fw.data_provider import load_json

schema = load_json("schemas/user.schema.json")

def test_update_user_success(client):
    payload = {"name": "AliceUpdated", "age": 31}
    resp = client.put("/users/1", json_body=payload)

    assert_status(resp.status_code, 200)
    assert_schema(resp.json, schema)
    assert_field_equals(resp.json, "name", "AliceUpdated")
    assert_field_equals(resp.json, "age", 31)

def test_update_user_missing(client):
    payload = {"name": "X", "age": 10}
    resp = client.put("/users/9999", json_body=payload)
    assert_status(resp.status_code, 404)
