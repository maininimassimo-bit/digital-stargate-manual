"""Minimal IAM-gated durable receipt receiver for the BKL-043 F4 pilot.

Cloud Run IAM must require authentication for every request. This application
validates an allowlisted payload and acknowledges only after Cloud Storage has
created the immutable receipt object.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
from datetime import datetime, timezone
from uuid import UUID

from flask import Flask, jsonify, request
from werkzeug.exceptions import RequestEntityTooLarge
from google.api_core.exceptions import PreconditionFailed
from google.cloud import storage

MAX_REQUEST_BYTES = 4096
BUCKET_NAME = os.environ.get("RECEIPT_BUCKET", "")
EAGLE_HOST = "EAGLE30154"
TASK_NAMES = {
    "Digital StarGate - Daily Session Upload",
    "Digital StarGate - OneDrive Export",
    "DigitalStarGate-EagleHealthTelemetry",
}
ALLOWED_CONCLUSIONS = {"success", "failure", "cancelled", "skipped", "action_required", "neutral", "stale", "timed_out", "startup_failure"}
ALLOWED_WORKFLOWS = {
    "BKL-031 F9 MeteoHub Refresh",
    "Analyze Observatory Session Automatically",
}
ID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_REQUEST_BYTES
_bucket = None

def _get_bucket():
    global _bucket
    if _bucket is None:
        if not BUCKET_NAME:
            raise RuntimeError("RECEIPT_BUCKET is not configured")
        _bucket = storage.Client().bucket(BUCKET_NAME)
    return _bucket


class InvalidPayload(ValueError):
    pass


def _no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidPayload("duplicate_json_key")
        result[key] = value
    return result


def _parse_body() -> dict:
    if request.content_length is not None and request.content_length > MAX_REQUEST_BYTES:
        raise RequestEntityTooLarge()
    raw = request.get_data(cache=False)
    if not raw or len(raw) > MAX_REQUEST_BYTES:
        raise RequestEntityTooLarge() if len(raw) > MAX_REQUEST_BYTES else InvalidPayload("empty_body")
    try:
        value = json.loads(raw, object_pairs_hook=_no_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InvalidPayload("invalid_json") from exc
    if not isinstance(value, dict):
        raise InvalidPayload("json_object_required")
    return value


def _exact_keys(value: dict, expected: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        raise InvalidPayload(f"{label}_fields_mismatch")


def _utc(value, label: str, nullable: bool = False) -> None:
    if value is None and nullable:
        return
    if not isinstance(value, str) or not UTC_RE.fullmatch(value):
        raise InvalidPayload(f"{label}_must_be_utc_z")
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise InvalidPayload(f"{label}_invalid_timestamp") from exc


def _validate_eagle(payload: dict) -> str:
    expected = {
        "schema_version", "record_id", "source_id", "host_identity",
        "boot_epoch_id", "sequence_id", "source_observed_at_utc",
        "source_clock_quality", "signals",
    }
    _exact_keys(payload, expected, "receipt")
    if payload["schema_version"] != 1:
        raise InvalidPayload("unsupported_schema_version")
    if not isinstance(payload["record_id"], str) or not ID_RE.fullmatch(payload["record_id"]):
        raise InvalidPayload("record_id_must_be_uuid")
    if payload["source_id"] != "dsg-eagle-f4" or payload["host_identity"] != EAGLE_HOST:
        raise InvalidPayload("source_or_host_not_authorized")
    if not isinstance(payload["boot_epoch_id"], str) or len(payload["boot_epoch_id"]) > 64:
        raise InvalidPayload("invalid_boot_epoch_id")
    if type(payload["sequence_id"]) is not int or payload["sequence_id"] < 0:
        raise InvalidPayload("invalid_sequence_id")
    if payload["source_clock_quality"] not in {"VALID", "UNKNOWN"}:
        raise InvalidPayload("invalid_clock_quality")
    _utc(payload["source_observed_at_utc"], "source_observed_at_utc",
         nullable=payload["source_clock_quality"] == "UNKNOWN")
    if payload["source_clock_quality"] == "UNKNOWN":
        raise InvalidPayload("clock_quality_unknown_admission_paused")
        raise InvalidPayload("unknown_clock_must_not_claim_utc")

    signals = payload["signals"]
    if not isinstance(signals, dict):
        raise InvalidPayload("signals_object_required")
    _exact_keys(signals, {"os", "uptime_seconds", "disks", "tasks", "nina_plugin_projection"}, "signals")
    os_info = signals["os"]
    _exact_keys(os_info, {"caption", "version", "build", "architecture"}, "os")
    for key in ("caption", "version", "build", "architecture"):
        if not isinstance(os_info[key], str) or len(os_info[key]) > 100:
            raise InvalidPayload("invalid_os_field")
    if type(signals["uptime_seconds"]) is not int or signals["uptime_seconds"] < 0:
        raise InvalidPayload("invalid_uptime")
    disks = signals["disks"]
    if not isinstance(disks, list) or {d.get("device_id") for d in disks if isinstance(d, dict)} != {"C:", "D:"} or len(disks) != 2:
        raise InvalidPayload("disk_set_must_be_c_and_d")
    for disk in disks:
        _exact_keys(disk, {"device_id", "free_bytes"}, "disk")
        if type(disk["free_bytes"]) is not int or disk["free_bytes"] < 0:
            raise InvalidPayload("invalid_disk_free_bytes")
    tasks = signals["tasks"]
    if not isinstance(tasks, list) or len(tasks) != 3:
        raise InvalidPayload("three_task_results_required")
    seen = set()
    for task in tasks:
        _exact_keys(task, {"name", "state", "last_task_result", "result_hex", "outcome_interpretation", "last_run_utc", "process_present"}, "task")
        if task["name"] not in TASK_NAMES or task["name"] in seen:
            raise InvalidPayload("invalid_or_duplicate_task")
        seen.add(task["name"])
        if not isinstance(task["state"], str) or len(task["state"]) > 32:
            raise InvalidPayload("invalid_task_state")
        if type(task["last_task_result"]) is not int:
            raise InvalidPayload("invalid_task_result")
        if not isinstance(task["result_hex"], str) or not re.fullmatch(r"0x[0-9A-F]{8}", task["result_hex"]):
            raise InvalidPayload("invalid_task_result_hex")
        expected_interpretation = "SUCCESS" if task["last_task_result"] == 0 else "NONZERO_REVIEW"
        if task["outcome_interpretation"] != expected_interpretation:
            raise InvalidPayload("invalid_task_outcome_interpretation")
        _utc(task["last_run_utc"], "task_last_run_utc", nullable=True)
        if type(task["process_present"]) is not bool:
            raise InvalidPayload("invalid_process_presence")
    if seen != TASK_NAMES:
        raise InvalidPayload("incomplete_task_set")

    heartbeat = signals["nina_plugin_projection"]
    _exact_keys(heartbeat, {"exists", "last_write_utc", "age_seconds", "freshness"}, "nina_projection")
    if type(heartbeat["exists"]) is not bool or heartbeat["freshness"] not in {"FRESH", "STALE", "UNKNOWN"}:
        raise InvalidPayload("invalid_nina_heartbeat")
    if heartbeat["last_write_utc"] is not None:
        _utc(heartbeat["last_write_utc"], "nina_last_write_utc")
    age = heartbeat["age_seconds"]
    if age is not None and (type(age) not in (int, float) or age < 0):
        raise InvalidPayload("invalid_nina_age")
    if not heartbeat["exists"] and (heartbeat["last_write_utc"] is not None or age is not None or heartbeat["freshness"] != "UNKNOWN"):
        raise InvalidPayload("inconsistent_missing_nina_projection")
    if heartbeat["freshness"] == "UNKNOWN" and age is not None:
        raise InvalidPayload("inconsistent_nina_unknown")
    if heartbeat["freshness"] == "FRESH" and (not heartbeat["exists"] or heartbeat["last_write_utc"] is None or age is None or age > 60):
        raise InvalidPayload("inconsistent_nina_freshness")
    if heartbeat["freshness"] == "STALE" and (not heartbeat["exists"] or heartbeat["last_write_utc"] is None or age is None or age <= 60):
        raise InvalidPayload("inconsistent_nina_freshness")
    return f"v1/{payload['record_id']}.json"


def _validate_github(payload: dict) -> str:
    expected = {
        "schema_version", "event_id", "repository", "workflow_name", "run_id",
        "run_attempt", "event", "status", "conclusion", "head_sha",
        "created_at_utc", "started_at_utc", "completed_at_utc",
    }
    _exact_keys(payload, expected, "github_outcome")
    if payload["schema_version"] != 1 or payload["repository"] != "maininimassimo-bit/digital-stargate-manual":
        raise InvalidPayload("github_source_not_authorized")
    if payload["workflow_name"] not in ALLOWED_WORKFLOWS:
        raise InvalidPayload("workflow_not_allowlisted")
    run_id, attempt = payload["run_id"], payload["run_attempt"]
    if type(run_id) not in (str, int) or not str(run_id).isdigit() or type(attempt) is not int or attempt < 1:
        raise InvalidPayload("invalid_run_identity")
    expected_id = f"github/{payload['repository']}/{run_id}/{attempt}"
    if payload["event_id"] != expected_id:
        raise InvalidPayload("invalid_event_id")
    if payload["conclusion"] not in ALLOWED_CONCLUSIONS or payload["status"] != "completed":
        raise InvalidPayload("invalid_run_conclusion")
    if not isinstance(payload["event"], str) or len(payload["event"]) > 40:
        raise InvalidPayload("invalid_trigger_event")
    if not isinstance(payload["head_sha"], str) or not re.fullmatch(r"[0-9a-f]{40}", payload["head_sha"]):
        raise InvalidPayload("invalid_head_sha")
    for key in ("created_at_utc", "started_at_utc", "completed_at_utc"):
        _utc(payload[key], key, nullable=key == "started_at_utc")
    return f"github/{run_id}/{attempt}.json"


def _store_immutable(object_name: str, payload: dict):
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()
    stored = {
        "payload": payload,
        "payload_sha256": digest,
        "receiver_received_at_utc": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    }
    body = json.dumps(stored, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    blob = _get_bucket().blob(object_name)
    try:
        blob.upload_from_string(body, content_type="application/json", if_generation_match=0)
        return "DURABLE_CREATED", digest
    except PreconditionFailed:
        existing = _get_bucket().blob(object_name)
        try:
            existing_payload = json.loads(existing.download_as_bytes())
        except Exception as exc:  # A corrupt existing object must not be acknowledged.
            raise RuntimeError("duplicate_object_unreadable") from exc
        if existing_payload.get("payload_sha256") != digest:
            raise InvalidPayload("record_id_conflict")
        return "DURABLE_DUPLICATE", digest


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify(error="payload_too_large"), 413


@app.errorhandler(InvalidPayload)
def invalid_payload(error):
    return jsonify(error=str(error)), 400


@app.post("/v1/receipts")
def ingest_eagle_receipt():
    payload = _parse_body()
    key = _validate_eagle(payload)
    try:
        outcome, digest = _store_immutable(key, payload)
    except InvalidPayload:
        raise
    except Exception:
        logging.exception("eagle_receipt_durable_write_failed")
        return jsonify(error="durable_write_unavailable"), 503
    return jsonify(ack=outcome, record_id=payload["record_id"], payload_sha256=digest), 200


@app.post("/v1/github-workflow-outcome")
def ingest_github_outcome():
    payload = _parse_body()
    key = _validate_github(payload)
    try:
        outcome, digest = _store_immutable(key, payload)
    except InvalidPayload:
        raise
    except Exception:
        logging.exception("github_outcome_durable_write_failed")
        return jsonify(error="durable_write_unavailable"), 503
    return jsonify(ack=outcome, event_id=payload["event_id"], payload_sha256=digest), 200
