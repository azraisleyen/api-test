from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

log = logging.getLogger("fw.client")


@dataclass(frozen=True)
class RequestInfo:
    method: str
    url: str
    headers: Dict[str, str]
    params: Optional[Dict[str, Any]] = None
    json_body: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class ApiResponse:
    status_code: int
    json: Any
    text: str
    elapsed_ms: int
    headers: Dict[str, str]              # response headers
    request: RequestInfo                # request kanıtı


class ApiClient:
    def __init__(self, base_url: str, timeout_seconds: int = 5, auth_type: str = "none", token: str = ""):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout_seconds
        self.session = requests.Session()
        self.headers: Dict[str, str] = {"Accept": "application/json"}

        if auth_type == "bearer" and token:
            self.headers["Authorization"] = f"Bearer {token}"

    def _url(self, path: str) -> str:
        path = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{path}"

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.2, min=0.2, max=2.0),
        retry=retry_if_exception_type(requests.RequestException),
    )
    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> ApiResponse:
        url = self._url(path)
        log.info("GET %s params=%s", url, params)
        r = self.session.get(url, params=params, headers=self.headers, timeout=self.timeout)
        req = RequestInfo(method="GET", url=url, headers=dict(self.headers), params=params)
        return self._wrap(r, req)

    def post(self, path: str, json_body: Optional[Dict[str, Any]] = None) -> ApiResponse:
        url = self._url(path)
        log.info("POST %s body=%s", url, json_body)
        r = self.session.post(url, json=json_body, headers=self.headers, timeout=self.timeout)
        req = RequestInfo(method="POST", url=url, headers=dict(self.headers), json_body=json_body)
        return self._wrap(r, req)

    def put(self, path: str, json_body: Optional[Dict[str, Any]] = None) -> ApiResponse:
        url = self._url(path)
        log.info("PUT %s body=%s", url, json_body)
        r = self.session.put(url, json=json_body, headers=self.headers, timeout=self.timeout)
        req = RequestInfo(method="PUT", url=url, headers=dict(self.headers), json_body=json_body)
        return self._wrap(r, req)

    def delete(self, path: str) -> ApiResponse:
        url = self._url(path)
        log.info("DELETE %s", url)
        r = self.session.delete(url, headers=self.headers, timeout=self.timeout)
        req = RequestInfo(method="DELETE", url=url, headers=dict(self.headers))
        return self._wrap(r, req)

    def _wrap(self, r: requests.Response, req: RequestInfo) -> ApiResponse:
        elapsed_ms = int(r.elapsed.total_seconds() * 1000)

        try:
            j = r.json()
        except ValueError:
            j = None

        # İstersen response özetini de logla (log dosyasının boş kalmaması için faydalı)
        log.info("RESP %s %s status=%s elapsed_ms=%s", req.method, req.url, r.status_code, elapsed_ms)

        return ApiResponse(
            status_code=r.status_code,
            json=j,
            text=r.text,
            elapsed_ms=elapsed_ms,
            headers={k: v for k, v in r.headers.items()},
            request=req,
        )
