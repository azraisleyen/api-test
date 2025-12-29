# tests/conftest.py
import os
import sys
import time
import subprocess

import pytest
import requests

from src.fw.config import load_config
from src.fw.logger import setup_logger
from src.fw.client import ApiClient


def _wait_until_ready(base_url: str, timeout_s: int = 40) -> None:
    """
    API hazır olana kadar bekle. Hazırlık sinyali olarak /health varsa onu,
    yoksa /__reset'i kullanır.
    """
    deadline = time.time() + timeout_s
    last_err: Exception | None = None

    # Önce health dene, yoksa reset'e düş
    health_url = f"{base_url}/health"
    reset_url = f"{base_url}/__reset"

    while time.time() < deadline:
        try:
            # health endpoint varsa en temiz yöntem
            r = requests.get(health_url, timeout=2)
            if r.status_code == 200:
                return
        except Exception as e:
            last_err = e

        try:
            # health yoksa, reset ile de "ulaşılabilirlik" kanıtı olur
            r = requests.post(reset_url, json={}, timeout=2)
            if 200 <= r.status_code < 500:
                return
        except Exception as e:
            last_err = e

        time.sleep(1)

    raise RuntimeError(f"API did not become ready in time. Last error: {last_err}")


@pytest.fixture(scope="session", autouse=True)
def api_server():
    """
    GitHub Actions (CI) ortamında demo API'yi otomatik başlatır.
    Local'de API'yi sen ayrı terminalde çalıştırmaya devam edebilirsin.
    """
    in_ci = os.getenv("GITHUB_ACTIONS") == "true"
    if not in_ci:
        # local: dışarıdan uvicorn çalıştırıyorsun varsayımı
        yield
        return

    base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")

    cmd = [
        sys.executable, "-m", "uvicorn",
        "demo_api.app:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--log-level", "info",
    ]

    # stdout'u yakalamak teşhis için faydalı; CI loglarına basabiliriz
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        _wait_until_ready(base_url, timeout_s=60)
        yield
    finally:
        # Süreci temiz kapat
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.fixture(scope="session")
def cfg():
    c = load_config("config/config.yaml")
    setup_logger(c.logging.level, c.logging.file)
    return c


@pytest.fixture(scope="session")
def client(cfg):
    return ApiClient(
        base_url=cfg.base_url,
        timeout_seconds=cfg.timeout_seconds,
        auth_type=cfg.auth.type,
        token=cfg.auth.token,
    )


@pytest.fixture(autouse=True)
def reset_demo_api_state(client):
    # her testten önce DB'yi başlangıca al
    client.post("/__reset", json_body={})
    yield
