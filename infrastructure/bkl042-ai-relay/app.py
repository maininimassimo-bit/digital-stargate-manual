"""Bounded read-only AI relay for BKL-042.

The relay is deliberately fail-closed. It never exposes the provider key,
never accepts tools/actions, and will not call the provider unless runtime
enablement and a persistent quota ledger are explicitly configured.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

try:
    from google.cloud import firestore
except ImportError:  # Offline repository checks do not require cloud dependencies.
    firestore = None


PROVIDER_URL = "https://api.openai.com/v1/responses"
ALLOWED_MODES = {"triage", "consultative", "escalation"}
MODEL_BY_MODE = {
    "triage": "gpt-6-luna",
    "consultative": "gpt-6-sol",
    "escalation": "gpt-6-astra",
}
MAX_INPUT_CHARS = 12000
MAX_CITATIONS = 20
_quota_lock = threading.Lock()


def _bool_env(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes"}


def _config() -> dict[str, Any]:
    return {
        "enabled": _bool_env("BKL042_RUNTIME_ENABLED"),
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "firestore_collection": os.getenv("BKL042_FIRESTORE_COLLECTION", ""),
        "max_requests": int(os.getenv("BKL042_MAX_PILOT_REQUESTS", "100")),
    }


def readiness() -> dict[str, Any]:
    config = _config()
    reasons = []
    if not config["enabled"]:
        reasons.append("RUNTIME_DISABLED")
    if not config["api_key"]:
        reasons.append("OPENAI_API_KEY_NOT_CONFIGURED")
    if not config["firestore_collection"]:
        reasons.append("PERSISTENT_QUOTA_LEDGER_NOT_CONFIGURED")
    if firestore is None:
        reasons.append("FIRESTORE_CLIENT_UNAVAILABLE")
    return {
        "status": "READY" if not reasons else "NOT_READY",
        "bounded_read_only": True,
        "tools_enabled": False,
        "command_authority": "NONE",
        "safety_authority": "NONE",
        "reasons": reasons,
    }


def choose_model(mode: str, correlation_id: str) -> str:
    if mode not in ALLOWED_MODES:
        raise ValueError("mode must be triage, consultative, or escalation")
    # The correlation id makes routing reproducible for audit/replay. The
    # default consultative route is Sol; the UI must request escalation.
    del correlation_id
    return MODEL_BY_MODE[mode]


def _reserve_request(collection: str, maximum: int) -> int:
    if firestore is None:
        raise RuntimeError("FIRESTORE_CLIENT_UNAVAILABLE")
    client = firestore.Client()
    document = client.collection(collection).document("pilot-quota")
    transaction = client.transaction()

    @firestore.transactional
    def reserve(current_transaction: Any) -> int:
        snapshot = document.get(transaction=current_transaction)
        data = snapshot.to_dict() if snapshot.exists else {}
        used = int(data.get("requests_used", 0))
        if used >= maximum:
            raise RuntimeError("PILOT_REQUEST_LIMIT_REACHED")
        current_transaction.set(
            document,
            {"requests_used": used + 1, "max_requests": maximum},
            merge=True,
        )
        return used + 1

    with _quota_lock:
        return reserve(transaction)


def _extract_text(response: dict[str, Any]) -> str:
    if isinstance(response.get("output_text"), str):
        return response["output_text"]
    parts = []
    for item in response.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                parts.append(content.get("text", ""))
    return "\n".join(part for part in parts if part)


def generate(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("request must be a JSON object")
    question = str(payload.get("question", "")).strip()
    evidence = str(payload.get("evidence", "")).strip()
    citations = payload.get("citations", [])
    mode = str(payload.get("mode", "consultative"))
    correlation_id = str(payload.get("correlation_id", ""))
    if not question or len(question) > MAX_INPUT_CHARS:
        raise ValueError("question is required and must be <= 12000 characters")
    if len(evidence) > MAX_INPUT_CHARS:
        raise ValueError("evidence must be <= 12000 characters")
    if not isinstance(citations, list) or len(citations) > MAX_CITATIONS:
        raise ValueError("citations must be a list of at most 20 items")
    if not correlation_id:
        raise ValueError("correlation_id is required")
    config = _config()
    state = readiness()
    if state["status"] != "READY":
        raise RuntimeError("RUNTIME_NOT_READY")
    model = choose_model(mode, correlation_id)
    request_number = _reserve_request(config["firestore_collection"], config["max_requests"])
    prompt = {
        "question": question,
        "evidence": evidence,
        "citations": citations,
        "constraints": [
            "Answer only from the supplied evidence and citations.",
            "If evidence is insufficient, say NOT_EVALUABLE_CURRENT_EVIDENCE.",
            "Do not issue commands, remediation, scheduling, or safety decisions.",
        ],
    }
    body = json.dumps({
        "model": model,
        "store": False,
        "input": [
            {"role": "system", "content": "You are a bounded read-only observatory assistant."},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
    }).encode("utf-8")
    request = urllib.request.Request(
        PROVIDER_URL,
        data=body,
        headers={"Authorization": f"Bearer {config['api_key']}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            provider_response = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise RuntimeError("PROVIDER_REQUEST_FAILED") from exc
    return {
        "correlation_id": correlation_id,
        "model": model,
        "request_number": request_number,
        "answer": _extract_text(provider_response),
        "bounded_read_only": True,
        "runtime_event_published": False,
        "command_authority": "NONE",
        "safety_authority": "NONE",
        "input_digest": hashlib.sha256(question.encode("utf-8")).hexdigest(),
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, data: dict[str, Any]) -> None:
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send(200, readiness())
            return
        self._send(404, {"error": "NOT_FOUND"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/bkl042-chat":
            self._send(404, {"error": "NOT_FOUND"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            self._send(200, generate(payload))
        except ValueError as exc:
            self._send(400, {"error": str(exc)})
        except RuntimeError as exc:
            self._send(503, {"error": str(exc)})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
