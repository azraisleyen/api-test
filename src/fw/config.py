from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass(frozen=True)
class AuthConfig:
    type: str = "none"   # none|bearer
    token: str = ""

@dataclass(frozen=True)
class LoggingConfig:
    level: str = "INFO"
    file: str = "logs/test.log"

@dataclass(frozen=True)
class AppConfig:
    base_url: str
    timeout_seconds: int = 5
    response_time_threshold_ms: int = 500
    auth: AuthConfig = AuthConfig()
    logging: LoggingConfig = LoggingConfig()

def load_config(path: str | Path) -> AppConfig:
    p = Path(path)
    data = yaml.safe_load(p.read_text(encoding="utf-8"))

    auth = data.get("auth", {}) or {}
    log = data.get("logging", {}) or {}

    return AppConfig(
        base_url=str(data["base_url"]).rstrip("/"),
        timeout_seconds=int(data.get("timeout_seconds", 5)),
        response_time_threshold_ms=int(data.get("response_time_threshold_ms", 500)),
        auth=AuthConfig(type=str(auth.get("type", "none")), token=str(auth.get("token", ""))),
        logging=LoggingConfig(level=str(log.get("level", "INFO")), file=str(log.get("file", "logs/test.log"))),
    )
