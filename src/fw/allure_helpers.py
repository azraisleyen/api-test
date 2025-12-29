import json
import allure
from src.fw.client import ApiResponse

def attach_response(resp: ApiResponse, name_prefix: str = "api"):
    allure.attach(
        str(resp.status_code),
        name=f"{name_prefix}-status",
        attachment_type=allure.attachment_type.TEXT,
    )
    allure.attach(
        str(resp.elapsed_ms),
        name=f"{name_prefix}-elapsed_ms",
        attachment_type=allure.attachment_type.TEXT,
    )

    if resp.json is not None:
        allure.attach(
            json.dumps(resp.json, indent=2, ensure_ascii=False),
            name=f"{name_prefix}-response.json",
            attachment_type=allure.attachment_type.JSON,
        )
    else:
        allure.attach(
            resp.text,
            name=f"{name_prefix}-response.txt",
            attachment_type=allure.attachment_type.TEXT,
        )
