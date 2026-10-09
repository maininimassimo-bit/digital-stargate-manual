import importlib.util
import json
import os
from pathlib import Path
import sys

import pytest

os.environ.setdefault("RECEIPT_BUCKET", "test-receipts")
APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
SPEC = importlib.util.spec_from_file_location("bkl043_f4_receiver_app", APP_PATH)
receiver = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = receiver
SPEC.loader.exec_module(receiver)


RECORD_ID = "a0d06a14-8f17-4b12-94dc-b0d74fd91f91"
TASK_NAMES = [
    "Digital StarGate - Daily Session Upload",
    "Digital StarGate - OneDrive Export",
    "DigitalStarGate-EagleHealthTelemetry",
]


class FakeBlob:
    def __init__(self, bucket, name):
        self.bucket = bucket
        self.name = name

    def upload_from_string(self, body, content_type, if_generation_match):
        assert content_type == "application/json"
        assert if_generation_match == 0
        if self.name in self.bucket.objects:
            from google.api_core.exceptions import PreconditionFailed
            raise PreconditionFailed("exists")
        self.bucket.objects[self.name] = body

    def download_as_bytes(self):
        return self.bucket.objects[self.name]


class FakeBucket:
    def __init__(self):
        self.objects = {}

    def blob(self, name):
        return FakeBlob(self, name)


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setattr(receiver, "_bucket", FakeBucket())
    receiver.app.config.update(TESTING=True)
    return receiver.app.test_client()


def eagle_payload():
    return {
        "schema_version": 1,
        "record_id": RECORD_ID,
        "source_id": "dsg-eagle-f4",
        "host_identity": "EAGLE30154",
        "boot_epoch_id": "2026-09-28T08:00:00Z",
        "sequence_id": 3600,
        "source_observed_at_utc": "2026-09-28T10:00:00Z",
        "source_clock_quality": "VALID",
        "signals": {
            "os": {
                "caption": "Microsoft Windows 10 Enterprise LTSC",
                "version": "10.0.17763",
                "build": "17763",
                "architecture": "64 bit",
            },
            "uptime_seconds": 7200,
            "disks": [
                {"device_id": "C:", "free_bytes": 46188761088},
                {"device_id": "D:", "free_bytes": 340746747904},
            ],
            "tasks": [
                {
                    "name": name,
                    "state": "Ready",
                    "last_task_result": 0,
                    "result_hex": "0x00000000",
                    "outcome_interpretation": "SUCCESS",
                    "last_run_utc": "2026-09-28T08:00:00Z",
                    "process_present": False,
                }
                for name in TASK_NAMES
            ],
            "nina_plugin_projection": {
                "exists": True,
                "last_write_utc": "2026-09-28T10:00:00Z",
                "age_seconds": 5.0,
                "freshness": "FRESH",
            },
        },
    }


def github_payload():
    run_id, attempt = "36400000123", 1
    return {
        "schema_version": 1,
        "event_id": f"github/maininimassimo-bit/digital-stargate-manual/{run_id}/{attempt}",
        "repository": "maininimassimo-bit/digital-stargate-manual",
        "workflow_name": "BKL-031 F9 MeteoHub Refresh",
        "run_id": run_id,
        "run_attempt": attempt,
        "event": "schedule",
        "status": "completed",
        "conclusion": "success",
        "head_sha": "a" * 40,
        "created_at_utc": "2026-09-28T10:00:00Z",
        "started_at_utc": "2026-09-28T10:00:05Z",
        "completed_at_utc": "2026-09-28T10:01:10Z",
    }


def test_eagle_receipt_is_durably_created_and_acknowledged(client):
    response = client.post("/v1/receipts", json=eagle_payload())
    assert response.status_code == 200
    assert response.json["ack"] == "DURABLE_CREATED"
    assert response.json["record_id"] == RECORD_ID
    assert set(receiver._bucket.objects) == {f"v1/{RECORD_ID}.json"}


def test_nonzero_task_result_is_review_not_automatic_failure(client):
    payload = eagle_payload()
    payload["signals"]["tasks"][0]["last_task_result"] = 259
    payload["signals"]["tasks"][0]["result_hex"] = "0x00000103"
    payload["signals"]["tasks"][0]["outcome_interpretation"] = "NONZERO_REVIEW"
    response = client.post("/v1/receipts", json=payload)
    assert response.status_code == 200
    stored = json.loads(next(iter(receiver._bucket.objects.values())))
    task = stored["payload"]["signals"]["tasks"][0]
    assert task["last_task_result"] == 259
    assert task["outcome_interpretation"] == "NONZERO_REVIEW"


def test_identical_eagle_retry_is_acknowledged_without_second_object(client):
    payload = eagle_payload()
    first = client.post("/v1/receipts", json=payload)
    second = client.post("/v1/receipts", json=payload)
    assert first.status_code == second.status_code == 200
    assert first.json["ack"] == "DURABLE_CREATED"
    assert second.json["ack"] == "DURABLE_DUPLICATE"
    assert len(receiver._bucket.objects) == 1


def test_same_receipt_id_with_different_payload_is_rejected(client):
    payload = eagle_payload()
    client.post("/v1/receipts", json=payload)
    payload["signals"]["uptime_seconds"] += 1
    response = client.post("/v1/receipts", json=payload)
    assert response.status_code == 400
    assert response.json["error"] == "record_id_conflict"
    assert len(receiver._bucket.objects) == 1


@pytest.mark.parametrize("mutation", [
    lambda p: p.update({"unexpected": "private"}),
    lambda p: p.update({"host_identity": "OTHER"}),
    lambda p: p["signals"]["tasks"].pop(),
    lambda p: p["signals"]["nina_plugin_projection"].update({"freshness": "STALE"}),
    lambda p: p["signals"].update({"process_command_line": "must never be accepted"}),
])
def test_eagle_contract_rejects_out_of_scope_or_inconsistent_data(client, mutation):
    payload = eagle_payload()
    mutation(payload)
    response = client.post("/v1/receipts", json=payload)
    assert response.status_code == 400
    assert receiver._bucket.objects == {}


def test_unknown_clock_pauses_durable_admission(client):
    payload = eagle_payload()
    payload["source_clock_quality"] = "UNKNOWN"
    payload["source_observed_at_utc"] = None
    response = client.post("/v1/receipts", json=payload)
    assert response.status_code == 400
    assert response.json["error"] == "clock_quality_unknown_admission_paused"
    assert receiver._bucket.objects == {}

def test_invalid_calendar_timestamp_is_rejected(client):
    payload = eagle_payload()
    payload["source_observed_at_utc"] = "2026-99-50T10:00:00Z"
    response = client.post("/v1/receipts", json=payload)
    assert response.status_code == 400


def test_github_outcomes_are_stored_immutably_and_distinctly(client):
    payload = github_payload()
    response = client.post("/v1/github-workflow-outcome", json=payload)
    assert response.status_code == 200
    assert response.json["ack"] == "DURABLE_CREATED"
    assert set(receiver._bucket.objects) == {"github/36400000123/1.json"}


@pytest.mark.parametrize("conclusion", ["cancelled", "skipped", "failure", "action_required", "neutral", "stale", "timed_out", "startup_failure"])
def test_non_success_github_conclusions_remain_valid_distinct_values(client, conclusion):
    payload = github_payload()
    payload["conclusion"] = conclusion
    response = client.post("/v1/github-workflow-outcome", json=payload)
    assert response.status_code == 200
    stored = json.loads(next(iter(receiver._bucket.objects.values())))
    assert stored["payload"]["conclusion"] == conclusion


def test_unapproved_github_workflow_is_rejected(client):
    payload = github_payload()
    payload["workflow_name"] = "Deploy MkDocs artifact to GitHub Pages"
    response = client.post("/v1/github-workflow-outcome", json=payload)
    assert response.status_code == 400
    assert receiver._bucket.objects == {}


def test_duplicate_json_keys_and_oversized_bodies_are_rejected(client):
    duplicate = b'{"schema_version":1,"schema_version":1}'
    assert client.post("/v1/receipts", data=duplicate, content_type="application/json").status_code == 400
    assert client.post("/v1/receipts", data=b"x" * 4097, content_type="application/json").status_code == 413
    assert receiver._bucket.objects == {}


def test_acknowledgement_is_withheld_when_storage_is_unavailable(client, monkeypatch):
    class FailedBucket:
        def blob(self, name):
            raise OSError("synthetic unavailable")
    monkeypatch.setattr(receiver, "_bucket", FailedBucket())
    response = client.post("/v1/receipts", json=eagle_payload())
    assert response.status_code == 503
    assert response.json["error"] == "durable_write_unavailable"
