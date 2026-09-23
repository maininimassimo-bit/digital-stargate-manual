"""Google Identity gateway for the BKL-042 private read-only relay."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

try:
    from google.auth.transport.requests import Request
    from google.oauth2 import id_token
    AUTH_IMPORT_ERROR = ""
except ImportError as exc:  # Offline repository checks do not require cloud dependencies.
    Request = None
    id_token = None
    AUTH_IMPORT_ERROR = type(exc).__name__


MAX_BODY = 20000
ALLOWED_FIELDS = {"correlation_id", "question", "mode", "evidence", "citations"}


def _config() -> dict[str, str]:
    return {
        "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
        "allowed_email": os.getenv("BKL042_ALLOWED_EMAIL", "maininimassimo@gmail.com").lower(),
        "relay_url": os.getenv("BKL042_PRIVATE_RELAY_URL", "").rstrip("/"),
        "portal_origin": os.getenv(
            "BKL042_PORTAL_ORIGIN",
            "https://maininimassimo-bit.github.io",
        ),
    }


def readiness() -> dict[str, Any]:
    config = _config()
    reasons = []
    if not config["client_id"]:
        reasons.append("GOOGLE_CLIENT_ID_NOT_CONFIGURED")
    if not config["relay_url"]:
        reasons.append("PRIVATE_RELAY_URL_NOT_CONFIGURED")
    if id_token is None:
        reasons.append(f"GOOGLE_AUTH_CLIENT_UNAVAILABLE:{AUTH_IMPORT_ERROR}")
    return {
        "status": "READY" if not reasons else "NOT_READY",
        "bounded_read_only": True,
        "tools_enabled": False,
        "command_authority": "NONE",
        "safety_authority": "NONE",
        "reasons": reasons,
    }


def _json_response(response: Any) -> dict[str, Any]:
    return json.loads(response.read().decode("utf-8"))


def forward(payload: dict[str, Any], google_token: str) -> tuple[int, dict[str, Any]]:
    config = _config()
    if readiness()["status"] != "READY":
        return 503, {"error": "GATEWAY_NOT_READY"}
    try:
        claims = id_token.verify_oauth2_token(  # type: ignore[union-attr]
            google_token, Request(), config["client_id"]
        )
    except Exception:
        return 401, {"error": "INVALID_GOOGLE_ID_TOKEN"}
    if not claims.get("email_verified") or str(claims.get("email", "")).lower() != config["allowed_email"]:
        return 403, {"error": "GOOGLE_IDENTITY_NOT_ALLOWED"}
    try:
        relay_identity_token = id_token.fetch_id_token(  # type: ignore[union-attr]
            Request(), config["relay_url"]
        )
        request = urllib.request.Request(
            f"{config['relay_url']}/v1/bkl042-chat",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {relay_identity_token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, _json_response(response)
    except urllib.error.HTTPError as exc:
        return exc.code, {"error": "PRIVATE_RELAY_REQUEST_FAILED"}
    except urllib.error.URLError:
        return 503, {"error": "PRIVATE_RELAY_UNAVAILABLE"}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, data: dict[str, Any], cors: bool = False) -> None:
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        if cors and self.headers.get("Origin") == _config()["portal_origin"]:
            self.send_header("Access-Control-Allow-Origin", _config()["portal_origin"])
            self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
            self.send_header("Vary", "Origin")
        self.end_headers()
        self.wfile.write(encoded)

    def do_OPTIONS(self) -> None:  # noqa: N802
        if self.headers.get("Origin") != _config()["portal_origin"]:
            self._send(403, {"error": "ORIGIN_NOT_ALLOWED"})
            return
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", _config()["portal_origin"])
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Vary", "Origin")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send(200, readiness())
            return
        self._send(404, {"error": "NOT_FOUND"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/bkl042-chat":
            self._send(404, {"error": "NOT_FOUND"}, cors=True)
            return
        origin = self.headers.get("Origin")
        if origin != _config()["portal_origin"]:
            self._send(403, {"error": "ORIGIN_NOT_ALLOWED"})
            return
        authorization = self.headers.get("Authorization", "")
        if not authorization.startswith("Bearer "):
            self._send(401, {"error": "GOOGLE_ID_TOKEN_REQUIRED"}, cors=True)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY:
                raise ValueError("request body size is invalid")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            if set(payload) - ALLOWED_FIELDS:
                raise ValueError("unsupported request field")
            status, data = forward(payload, authorization.removeprefix("Bearer ").strip())
            self._send(status, data, cors=True)
        except (ValueError, json.JSONDecodeError) as exc:
            self._send(400, {"error": str(exc)}, cors=True)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", int(os.getenv("PORT", "8080"))), Handler).serve_forever()
