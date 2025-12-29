import pytest
from src.fw.config import load_config
from src.fw.logger import setup_logger
from src.fw.client import ApiClient

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