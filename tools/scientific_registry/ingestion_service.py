"""Owner-only photo ingestion application, independent of device and AI runtimes.

Every state transition and its audit entry share one generation-guarded object.
Binary files, previews and review receipts are immutable. Unreferenced immutable
objects left by an interrupted operation never become published records.
"""
from copy import deepcopy
from datetime import datetime, timezone
import json
import math
import re

from tools.pixinsight.workflow_archive.archive import encode
from tools.pixinsight.workflow_archive.provenance import build_sidecar
from tools.pixinsight.workflow_archive.public_projection import select_steps
from .ingestion_storage import Conflict, immutable
from .ingestion_security import sanitize_preview
from .photo_ingestion import IngestionError, build_review, sha256, _text

CHUNK_BYTES = 4 * 1024 * 1024
LIMITS = {"original": 1024 * 1024 * 1024, "preview": 32 * 1024 * 1024, "workflow": 2 * 1024 * 1024}
MEDIA = {"original": {"application/x-xisf", "application/fits"},
         "preview": {"image/jpeg", "image/png"}, "workflow": {"text/plain"}}
STATE_KEY = "control/state.json"


def json_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode()


def stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class IngestionService:
    def __init__(self, store, catalog_raw, scanner, public_base, *, catalog_loader=None):
        self.store, self.catalog_raw, self.scanner = store, catalog_raw, scanner
        self.catalog_digest = sha256(catalog_raw)
        self.public_base = public_base.rstrip("/")
        self.catalog_loader = catalog_loader

    def _state(self):
        raw, generation = self.store.get(STATE_KEY)
        return (json.loads(raw) if raw else {"schemaVersion": "1.0", "uploads": {}, "audit": []}), generation

    def _change(self, actor, action, upload_id, change):
        for _ in range(8):
            state, generation = self._state()
            result = change(state)
            if result is None:  # idempotent retry: no new event or revision
                return state["uploads"][upload_id]
            if len(state["audit"]) >= 4096:
                raise IngestionError("AUDIT_CAPACITY_REACHED")
            state["audit"].append({"at": stamp(), "actor": actor, "action": action, "uploadId": upload_id})
            raw = json_bytes(state)
            if len(raw) > 2 * 1024 * 1024:
                raise IngestionError("STATE_CAPACITY_REACHED")
            try:
                self.store.put(STATE_KEY, raw, generation)
                return state["uploads"][upload_id]
            except Conflict:
                continue
        raise Conflict("STATE_BUSY_RETRY")

    def _upload(self, upload_id, actor):
        if not isinstance(upload_id, str) or not re.fullmatch(r"[a-f0-9]{64}", upload_id):
            raise IngestionError("UPLOAD_ID_INVALID")
        item = self._state()[0]["uploads"].get(upload_id)
        if item is None or item["actor"] != actor:
            raise IngestionError("UPLOAD_NOT_FOUND")
        return item

    def create(self, request, actor):
        if not isinstance(request, dict) or set(request) != {"idempotencyKey", "catalogSha256", "imageId", "sessionIds", "title", "processingDate", "files", "previewAttested"}:
            raise IngestionError("REQUEST_FIELDS_INVALID")
        key = request["idempotencyKey"]
        if not isinstance(key, str) or not re.fullmatch(r"[A-Za-z0-9_-]{16,80}", key):
            raise IngestionError("IDEMPOTENCY_KEY_INVALID")
        upload_id = sha256(json_bytes({"actor": actor, "key": key}))
        request_digest = sha256(json_bytes(request))
        existing = self._state()[0]["uploads"].get(upload_id)
        if existing:
            if existing["requestDigest"] != request_digest:
                raise IngestionError("IDEMPOTENCY_CONFLICT")
            return existing  # An exact retry pins its original snapshot, even after catalog updates.
        catalog_raw = self.catalog_loader() if self.catalog_loader else self.catalog_raw
        catalog_digest = sha256(catalog_raw)
        if request["catalogSha256"] != catalog_digest:
            raise IngestionError("CATALOG_CHANGED_REFRESH")
        files = request["files"]
        if not isinstance(files, dict) or set(files) != set(LIMITS):
            raise IngestionError("ASSET_ROLES_INVALID")
        for role, item in files.items():
            if not isinstance(item, dict) or set(item) != {"byteSize", "mediaType", "sha256"}:
                raise IngestionError("ASSET_FIELDS_INVALID")
            if type(item["byteSize"]) is not int or not 0 < item["byteSize"] <= LIMITS[role]:
                raise IngestionError("ASSET_SIZE_LIMIT")
            if not isinstance(item["mediaType"], str) or item["mediaType"] not in MEDIA[role] or not isinstance(item["sha256"], str) or not re.fullmatch(r"[a-f0-9]{64}", item["sha256"]):
                raise IngestionError("ASSET_DESCRIPTOR_INVALID")
        # Validate selection/date/attestation before accepting any large file.
        context = build_review(catalog_raw=catalog_raw, catalog_digest=catalog_digest,
                     session_ids=request["sessionIds"], title=request["title"], processing_date=request["processingDate"],
                     original_raw=b"XISF0100", original_media_type="application/x-xisf",
                     preview_raw=b"\xff\xd8\xff", preview_media_type="image/jpeg", workflow_raw=b"",
                     receipt_id="BKL049-validation", imported_at=stamp(), preview_attested=request["previewAttested"])
        def change(state):
            old = state["uploads"].get(upload_id)
            if old:
                if old["requestDigest"] != request_digest:
                    raise IngestionError("IDEMPOTENCY_CONFLICT")
                return None
            if len(state["uploads"]) >= 64:
                raise IngestionError("UPLOAD_CAPACITY_REACHED")
            image_id = request["imageId"]
            if image_id is not None:
                if not isinstance(image_id, str) or not re.fullmatch(r"IMG-[a-f0-9]{32}", image_id):
                    raise IngestionError("IMAGE_ID_INVALID")
                parents = [u for u in state["uploads"].values() if u["actor"] == actor and u["imageId"] == image_id
                           and u["state"] in {"SAVED_PRIVATE", "PUBLISHED", "WITHDRAWN"}]
                if not parents:
                    raise IngestionError("IMAGE_VERSION_PARENT_MISSING")
                if any(u["target"] != context["target"] for u in parents):
                    raise IngestionError("IMAGE_VERSION_TARGET_CONFLICT")
            else:
                image_id = "IMG-" + upload_id[:32]
            state["uploads"][upload_id] = {"id": upload_id, "actor": actor, "createdAt": stamp(),
                "imageId": image_id, "target": context["target"],
                "request": deepcopy(request), "requestDigest": request_digest, "catalogSha256": catalog_digest,
                "state": "UPLOADING", "reviewSha256": None, "publication": None}
            return True
        # Preserve the exact selected catalogue for replay, independently of future deploys.
        immutable(self.store, "catalogs/" + catalog_digest, catalog_raw)
        return self._change(actor, "UPLOAD_CREATED", upload_id, change)

    def chunk(self, upload_id, role, index, raw, actor):
        item = self._upload(upload_id, actor)
        if item["state"] != "UPLOADING" or role not in LIMITS or type(index) is not int:
            raise IngestionError("UPLOAD_STATE_INVALID")
        size = item["request"]["files"][role]["byteSize"]
        count = math.ceil(size / CHUNK_BYTES)
        if not 0 <= index < count or not isinstance(raw, bytes) or len(raw) != min(CHUNK_BYTES, size - index * CHUNK_BYTES):
            raise IngestionError("CHUNK_SIZE_INVALID")
        immutable(self.store, f"chunks/{upload_id}/{role}/{index}", raw)
        return {"accepted": index}

    def status(self, upload_id, actor):
        item = deepcopy(self._upload(upload_id, actor))
        catalog_raw, _ = self.store.get("catalogs/" + item["catalogSha256"])
        if catalog_raw is None or sha256(catalog_raw) != item["catalogSha256"]:
            raise IngestionError("CATALOG_ANCHOR_MISMATCH")
        source = {s["sessionId"]: s for s in json.loads(catalog_raw)["sessions"]}
        item["frozenSessionContext"] = [{"sessionId": sid, "target": source[sid]["target"],
            "observationDate": source[sid].get("observationDate")} for sid in item["request"]["sessionIds"]]
        item["received"] = {}
        for role, descriptor in item["request"]["files"].items():
            item["received"][role] = [i for i in range(math.ceil(descriptor["byteSize"] / CHUNK_BYTES))
                if self.store.exists(f"chunks/{upload_id}/{role}/{i}")]
        return item

    def _file(self, item, role):
        descriptor = item["request"]["files"][role]
        parts = []
        for i in range(math.ceil(descriptor["byteSize"] / CHUNK_BYTES)):
            raw, _ = self.store.get(f"chunks/{item['id']}/{role}/{i}")
            if raw is None:
                raise IngestionError("UPLOAD_INCOMPLETE")
            parts.append(raw)
        result = b"".join(parts)
        if len(result) != descriptor["byteSize"] or sha256(result) != descriptor["sha256"]:
            raise IngestionError("FULL_FILE_INTEGRITY_FAILED")
        return result

    def review(self, upload_id, actor, *, recheck=False):
        item = self._upload(upload_id, actor)
        if item["state"] == "WITHDRAWN":
            raise IngestionError("WITHDRAWN_TERMINAL")
        if recheck and item["state"] == "PUBLISHED":
            raise IngestionError("PUBLISHED_IMMUTABLE_NEW_VERSION_REQUIRED")
        if item["reviewSha256"] and not recheck:
            raw, _ = self.store.get("reviews/" + item["reviewSha256"])
            if raw is None or sha256(raw) != item["reviewSha256"]:
                raise IngestionError("REVIEW_INTEGRITY_FAILED")
            return json.loads(raw)
        request = item["request"]
        catalog, _ = self.store.get("catalogs/" + item["catalogSha256"])
        original = self._file(item, "original")
        preview = self._file(item, "preview")
        workflow = self._file(item, "workflow")
        result = build_review(catalog_raw=catalog, catalog_digest=item["catalogSha256"],
            session_ids=request["sessionIds"], title=request["title"], processing_date=request["processingDate"],
            original_raw=original, original_media_type=request["files"]["original"]["mediaType"],
            preview_raw=preview, preview_media_type=request["files"]["preview"]["mediaType"],
            workflow_raw=workflow, receipt_id="BKL049-" + upload_id, imported_at=item["createdAt"],
            preview_attested=request["previewAttested"])
        scans = {role: self.scanner.scan(raw) for role, raw in (("original", original), ("preview", preview), ("workflow", workflow))}
        if any(value not in {"PASS", "FAIL", "UNAVAILABLE"} for value in scans.values()):
            raise IngestionError("SCAN_RESULT_INVALID")
        result["securityScans"] = scans
        for role in ("original", "preview"):
            result[role]["securityScan"] = scans[role]
            result[role]["state"] = "STORED_PRIVATE" if scans[role] == "PASS" else "QUARANTINED"
        result["publicationEligible"] = all(value == "PASS" for value in scans.values())
        result["gaps"] = ["EXECUTION_NOT_ESTABLISHED", "SESSION_ASSOCIATION_OWNER_DECLARED"]
        if not result["publicationEligible"]:
            result["gaps"].append("SECURITY_SCAN_NOT_PASSED")
        # Do not decode potentially malicious previews before a passing scan.
        result["sanitizedPreview"] = None
        if scans["preview"] == "PASS":
            clean = sanitize_preview(preview, request["files"]["preview"]["mediaType"])
            digest = sha256(clean)
            immutable(self.store, "previews/" + digest, clean)
            result["sanitizedPreview"] = {"sha256": digest, "byteSize": len(clean), "mediaType": "image/jpeg"}
            result["preview"]["previewSanitation"] = "PASS"
        else:
            result["gaps"].append("PREVIEW_SANITATION_PENDING")
        packet = result["workflow"]
        result["steps"] = []
        if packet["archive"] is not None:
            sidecar = build_sidecar(encode(packet), sha256(encode(packet)), {
                "declaredBy": actor, "declaredAt": item["createdAt"], "sourceSha256": packet["source"]["sha256"],
                "scope": "EXPORTED_CONFIGURATIONS_ONLY"}, exported_at=item["createdAt"])
            result["steps"] = sidecar["workflow"]["steps"]
        immutable(self.store, "assets/" + sha256(original), original)
        immutable(self.store, "assets/" + sha256(preview), preview)
        immutable(self.store, "assets/" + sha256(workflow), workflow)
        raw = json_bytes(result)
        digest = sha256(raw)
        immutable(self.store, "reviews/" + digest, raw)
        def change(state):
            current = state["uploads"][upload_id]
            if current["reviewSha256"] and not recheck:
                return None
            if current["state"] not in ({"UPLOADING", "REVIEW", "SAVED_PRIVATE"} if recheck else {"UPLOADING"}):
                raise IngestionError("UPLOAD_STATE_INVALID")
            if recheck and current["reviewSha256"] != item["reviewSha256"]:
                raise IngestionError("REVIEW_CHANGED")
            current.update(reviewSha256=digest, state="REVIEW", publication=None, selectionSha256=None)
            return True
        stored = self._change(actor, "REVIEW_READY", upload_id, change)
        if stored["reviewSha256"] != digest:
            return self.review(upload_id, actor)
        return result

    def review_summary(self, upload_id, actor, *, recheck=False):
        review = self.review(upload_id, actor, recheck=recheck)
        item = self._upload(upload_id, actor)
        steps, remaining, omitted = [], 512 * 1024, 0
        for step in review["steps"]:
            parameters = []
            for name, value in step["parameters"]["bkl049LexicalV1"]["exportParameters"].items():
                lexical = encode(value)
                if len(parameters) >= 128 or len(lexical) > 4096 or len(lexical) + len(name) + 128 > remaining:
                    omitted += 1
                    continue
                remaining -= len(lexical) + len(name) + 128
                parameters.append({"name": name, "lexicalJson": lexical.decode("ascii"), "valueSha256": sha256(lexical)})
            steps.append({"stepId": step["stepId"], "ordinal": step["ordinal"], "processId": step["processId"], "parameters": parameters})
        return {key: review[key] for key in ("title", "target", "processingDate", "sessionContext", "original", "preview",
                "sanitizedPreview", "securityScans", "publicationEligible", "gaps")} | {
                "steps": steps, "unlistedParameterCount": omitted,
                "publishedFields": deepcopy(item["publication"]),
                "reviewSha256": item["reviewSha256"], "imageId": item["imageId"],
                "imageVersionId": "VER-" + upload_id[:32], "workflowId": "WF-" + upload_id[:32],
                "workflowState": review["workflow"]["extractionState"], "state": item["state"]}

    def commit(self, upload_id, request, actor):
        if not isinstance(request, dict) or set(request) != {"reviewSha256", "publish", "rightsConfirmed", "steps"}:
            raise IngestionError("COMMIT_FIELDS_INVALID")
        if type(request["publish"]) is not bool or type(request["rightsConfirmed"]) is not bool:
            raise IngestionError("COMMIT_FLAGS_INVALID")
        item = self._upload(upload_id, actor)
        if request["reviewSha256"] != item["reviewSha256"] or item["state"] not in {"REVIEW", "SAVED_PRIVATE", "PUBLISHED"}:
            raise IngestionError("REVIEW_CHANGED")
        review = self.review(upload_id, actor)
        steps = select_steps(review["steps"], request["steps"])
        publication = None
        if request["publish"]:
            if request["rightsConfirmed"] is not True or review["publicationEligible"] is not True or review["sanitizedPreview"] is None:
                raise IngestionError("PUBLICATION_NOT_ALLOWED")
            publication = {"schemaVersion": "1.0", "kind": "DSG_SESSION_PHOTO_V1",
                "imageId": item["imageId"], "imageVersionId": "VER-" + upload_id[:32],
                "workflowId": "WF-" + upload_id[:32], "title": review["title"], "target": review["target"],
                "sessionIds": [s["sessionId"] for s in review["sessionContext"]["sessions"]],
                "processingDate": review["processingDate"], "previewUrl": self.public_base + "/v1/previews/" + upload_id,
                "captureCompleteness": "PARTIAL" if steps else "UNAVAILABLE", "executionEvidence": "NOT_ESTABLISHED",
                "associationEvidence": "OWNER_DECLARED", "steps": steps,
                "omittedStepCount": len(review["steps"]) - len(steps), "validUntil": None}
            if len(json_bytes(publication)) > 256 * 1024:
                raise IngestionError("PUBLICATION_SIZE_LIMIT")
        selection = {"reviewSha256": request["reviewSha256"], "publish": request["publish"],
                     "rightsConfirmed": request["rightsConfirmed"], "steps": request["steps"]}
        selection_digest = sha256(json_bytes(selection))
        def change(state):
            current = state["uploads"][upload_id]
            if current["state"] == "WITHDRAWN" or current["reviewSha256"] != request["reviewSha256"]:
                raise IngestionError("REVIEW_CHANGED")
            if current.get("selectionSha256") == selection_digest:
                return None
            # Publishing an existing version never silently changes its approved fields.
            if current["state"] == "PUBLISHED":
                raise IngestionError("PUBLISHED_IMMUTABLE_NEW_VERSION_REQUIRED")
            current.update(state="PUBLISHED" if publication else "SAVED_PRIVATE", publication=publication,
                           selectionSha256=selection_digest, approvedAt=stamp())
            return True
        return self._change(actor, "PUBLISHED" if publication else "SAVED_PRIVATE", upload_id, change)

    def withdraw(self, upload_id, actor):
        self._upload(upload_id, actor)
        def change(state):
            item = state["uploads"][upload_id]
            if item["state"] == "WITHDRAWN":
                return None
            if item["state"] != "PUBLISHED":
                raise IngestionError("WITHDRAWAL_STATE_INVALID")
            item.update(state="WITHDRAWN", publication=None)
            return True
        return self._change(actor, "WITHDRAWN", upload_id, change)

    def collection(self):
        records = [deepcopy(item["publication"]) for item in self._state()[0]["uploads"].values() if item["state"] == "PUBLISHED"]
        return {"schemaVersion": "1.0", "kind": "DSG_SESSION_PHOTO_COLLECTION_V1", "records": records,
                "authority": "projection", "actionAuthority": "NONE"}

    def archive(self, actor):
        return [{"uploadId": u["id"], "imageId": u["imageId"], "title": u["request"]["title"],
                 "target": u["target"], "state": u["state"], "createdAt": u["createdAt"],
                 "sessionIds": u["request"]["sessionIds"]}
                for u in self._state()[0]["uploads"].values() if u["actor"] == actor]

    def preview(self, upload_id, actor=None):
        item = self._upload(upload_id, actor) if actor else self._state()[0]["uploads"].get(upload_id)
        if item is None or (actor is None and item["state"] != "PUBLISHED") or not item["reviewSha256"]:
            raise IngestionError("PREVIEW_UNAVAILABLE")
        raw, _ = self.store.get("reviews/" + item["reviewSha256"])
        if raw is None or sha256(raw) != item["reviewSha256"]:
            raise IngestionError("REVIEW_INTEGRITY_FAILED")
        descriptor = json.loads(raw)["sanitizedPreview"]
        if not descriptor:
            raise IngestionError("PREVIEW_UNAVAILABLE")
        pixels, _ = self.store.get("previews/" + descriptor["sha256"])
        if pixels is None or sha256(pixels) != descriptor["sha256"]:
            raise IngestionError("PREVIEW_INTEGRITY_FAILED")
        return pixels
