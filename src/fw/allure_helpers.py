import json
import os
import allure
from src.fw.client import ApiResponse


def attach_response(resp: ApiResponse, name_prefix: str = "api"):
    """
    Allure'a request + response kanıtlarını ekler.
    """

    # =====================
    # REQUEST EVIDENCE
    # =====================
    req = resp.request

    allure.attach(
        req.method,
        name=f"{name_prefix}-request-method",
        attachment_type=allure.attachment_type.TEXT,
    )

    allure.attach(
        req.url,
        name=f"{name_prefix}-request-url",
        attachment_type=allure.attachment_type.TEXT,
    )

    if req.params:
        allure.attach(
            json.dumps(req.params, indent=2, ensure_ascii=False),
            name=f"{name_prefix}-request-params.json",
            attachment_type=allure.attachment_type.JSON,
        )

    if req.json_body:
        allure.attach(
            json.dumps(req.json_body, indent=2, ensure_ascii=False),
            name=f"{name_prefix}-request-body.json",
            attachment_type=allure.attachment_type.JSON,
        )

    allure.attach(
        json.dumps(req.headers, indent=2, ensure_ascii=False),
        name=f"{name_prefix}-request-headers.json",
        attachment_type=allure.attachment_type.JSON,
    )

    # =====================
    # RESPONSE EVIDENCE
    # =====================
    allure.attach(
        str(resp.status_code),
        name=f"{name_prefix}-response-status",
        attachment_type=allure.attachment_type.TEXT,
    )

    allure.attach(
        str(resp.elapsed_ms),
        name=f"{name_prefix}-response-elapsed-ms",
        attachment_type=allure.attachment_type.TEXT,
    )

    allure.attach(
        json.dumps(resp.headers, indent=2, ensure_ascii=False),
        name=f"{name_prefix}-response-headers.json",
        attachment_type=allure.attachment_type.JSON,
    )

    if resp.json is not None:
        allure.attach(
            json.dumps(resp.json, indent=2, ensure_ascii=False),
            name=f"{name_prefix}-response-body.json",
            attachment_type=allure.attachment_type.JSON,
        )
    else:
        allure.attach(
            resp.text,
            name=f"{name_prefix}-response-body.txt",
            attachment_type=allure.attachment_type.TEXT,
        )


def attach_log_file(log_path: str = "logs/test.log"):
    """
    Hata durumunda log dosyasını Allure'a ekler.
    """
    if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
        allure.attach.file(
            log_path,
            name="application-log",
            attachment_type=allure.attachment_type.TEXT,
        )
