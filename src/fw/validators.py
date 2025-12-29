from __future__ import annotations
from typing import Any, Dict, Optional
from jsonschema import validate as jsonschema_validate
from jsonschema.exceptions import ValidationError

def assert_status(resp_status: int, expected: int) -> None:
    assert resp_status == expected, f"Expected status={expected}, got={resp_status}"

def assert_response_time(elapsed_ms: int, threshold_ms: int) -> None:
    assert elapsed_ms <= threshold_ms, f"Response time {elapsed_ms}ms exceeded threshold {threshold_ms}ms"

def assert_schema(resp_json: Any, schema: Dict[str, Any]) -> None:
    try:
        jsonschema_validate(instance=resp_json, schema=schema)
    except ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e.message}") from e

def assert_field_equals(resp_json: Dict[str, Any], field: str, expected: Any) -> None:
    assert field in resp_json, f"Missing field '{field}'"
    assert resp_json[field] == expected, f"Field '{field}' expected={expected}, got={resp_json[field]}"
