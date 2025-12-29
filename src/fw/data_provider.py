from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List

def load_json(path: str | Path) -> Any:
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8"))

def load_test_cases(path: str | Path) -> List[Dict[str, Any]]:
    data = load_json(path)
    if not isinstance(data, list):
        raise ValueError("Test data must be a list of objects")
    return data
