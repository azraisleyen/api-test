from src.fw.validators import assert_status
import allure
from src.fw.allure_helpers import attach_response

def test_delete_user_success(client):
    # önce bir kullanıcı oluştur
    create_resp = client.post("/users", json_body={"name": "Temp", "age": 20})
    assert_status(create_resp.status_code, 201)
    new_id = create_resp.json["id"]

    # sonra sil
    del_resp = client.delete(f"/users/{new_id}")
    assert_status(del_resp.status_code, 204)

def test_delete_user_missing(client):
    resp = client.delete("/users/9999")
    with allure.step("Attach delete-user response"):
        attach_response(resp, "delete-user")
    assert_status(resp.status_code, 404)
