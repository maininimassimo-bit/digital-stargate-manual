"""Private P5 scientific context and review. No publication or native dispatch."""
import base64
import copy
import hashlib
import re

from .broker import decode, encode, require, opaque
from .worker import NONLINEAR_RECIPE, actions
from tools.scientific_registry.ingestion_storage import immutable, Conflict
from tools.scientific_registry.photo_ingestion import build_review
from tools.scientific_registry.ingestion_security import sanitize_preview


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class ScientificPortal:
    def __init__(self, broker, catalog_loader, gallery_loader):
        self.broker, self.store = broker, broker.store
        self.catalog_loader, self.gallery_loader = catalog_loader, gallery_loader

    def register(self, value):
        require(isinstance(value, dict) and set(value) == {"inputRef", "target", "recipe", "manifestSha256"}, "INPUT_FIELDS")
        require(opaque(value["inputRef"]) and value["target"] == "M27" and value["recipe"] == NONLINEAR_RECIPE and
                isinstance(value["manifestSha256"], str) and re.fullmatch(r"[a-f0-9]{64}", value["manifestSha256"]), "INPUT_INVALID")
        immutable(self.store, "science/inputs/" + value["inputRef"], encode(value))
        # Reuse the only mutable object authorized by the existing P4 IAM.
        def operation(state, _now):
            index = state.setdefault("scientificInputs", [])
            if value["inputRef"] not in index:
                require(len(index) < 8, "INPUT_CAPACITY")
                index.append(value["inputRef"])
            return value
        return self.broker._mutate(operation)

    def options(self):
        state, _ = self.broker._state()
        inputs = [decode(self.store.get("science/inputs/" + ref)[0]) for ref in state.get("scientificInputs", [])]
        catalog = self.catalog_loader()
        parsed = decode(catalog)
        require(parsed.get("schemaVersion") == "1.5" and parsed.get("catalogStatus") == "VERSIONED_ANALYTICS_PROJECTION", "CATALOG_PROFILE")
        gallery = self.gallery_loader()
        return {"inputs": inputs, "catalogSha256": digest(catalog),
                "sessions": [{"sessionId": s["sessionId"], "target": s["target"], "observationDate": s.get("observationDate")}
                             for s in parsed["sessions"] if s.get("target") == "M27"],
                "images": [{k: row[k] for k in ("imageId", "imageVersionId", "workflowId", "title", "target")}
                           for row in gallery["records"] if row["target"] == "M27"]}

    def create(self, value):
        fields = {"requestId", "inputRef", "catalogSha256", "sessionIds", "parent", "title", "processingDate", "associationConfirmed"}
        require(isinstance(value, dict) and set(value) == fields and opaque(value["requestId"]) and opaque(value["inputRef"]), "SCIENTIFIC_FIELDS")
        key = "science/contexts/PIAI_" + value["requestId"]
        raw, _ = self.store.get(key)
        if raw:
            context = decode(raw)
            require(context["selection"] == value, "IDEMPOTENCY_CONFLICT")
        else:
            registered, _ = self.store.get("science/inputs/" + value["inputRef"])
            require(registered is not None, "INPUT_NOT_REGISTERED")
            registered = decode(registered)
            catalog = self.catalog_loader()
            require(digest(catalog) == value["catalogSha256"], "CATALOG_CHANGED_REFRESH")
            context_review = build_review(catalog_raw=catalog, catalog_digest=digest(catalog), session_ids=value["sessionIds"],
                title=value["title"], processing_date=value["processingDate"], original_raw=b"XISF0100",
                original_media_type="application/x-xisf", preview_raw=b"\xff\xd8\xff", preview_media_type="image/jpeg",
                workflow_raw=b"", receipt_id="BKL049-P5-selection", imported_at=self.broker.clock().strftime("%Y-%m-%dT%H:%M:%SZ"),
                preview_attested=value["associationConfirmed"])
            require(context_review["target"] == registered["target"], "INPUT_TARGET_CONFLICT")
            parent = value["parent"]
            require(parent is None or (isinstance(parent, dict) and set(parent) == {"imageId", "imageVersionId", "workflowId"}), "PARENT_FIELDS")
            if parent is not None:
                matches = [r for r in self.gallery_loader()["records"] if all(r.get(k) == v for k, v in parent.items())]
                require(len(matches) == 1 and matches[0]["target"] == registered["target"], "PARENT_NOT_CURRENT")
            context = {"selection": copy.deepcopy(value), "input": registered, "sessionContext": context_review["sessionContext"],
                       "createdAt": self.broker.clock().strftime("%Y-%m-%dT%H:%M:%SZ"), "associationEvidence": "OWNER_DECLARED"}
            immutable(self.store, "science/catalogs/" + digest(catalog), catalog)
            immutable(self.store, key, encode(context))
        envelope = {"schemaVersion": "1.0", "requestId": value["requestId"], "inputRef": value["inputRef"],
                    "recipe": NONLINEAR_RECIPE, "aiMode": "SESSION_ASSISTED"}
        return self.broker.create(envelope, digest(encode(context)))

    def context(self, job_id):
        # Job must exist; a staged context alone never grants execution authority.
        job = self.broker.status(job_id)["job"]
        raw, _ = self.store.get("science/contexts/" + job_id)
        require(raw is not None, "SCIENTIFIC_JOB_REQUIRED")
        require(digest(raw) == job.get("scientificContextSha256"), "CONTEXT_INTEGRITY")
        return decode(raw)

    def deliver(self, job_id, value):
        require(isinstance(value, dict) and set(value) == {"workerId", "leaseToken", "original", "previewBase64", "workflowBase64", "correlationsBase64"}, "RESULT_FIELDS")
        state, _ = self.broker._state()
        job = self.broker._job(state, job_id)
        import secrets
        require(value["workerId"] == self.broker.worker_id and isinstance(value["leaseToken"], str) and
                secrets.compare_digest(value["leaseToken"], job.get("leaseToken", "")), "RESULT_BINDING")
        require(job["state"] == "COMPLETED" and job["report"]["verified"] is True, "RESULT_NOT_COMPLETED")
        context = self.context(job_id)
        original = value["original"]
        require(isinstance(original, dict) and set(original) == {"sha256", "byteSize", "width", "height", "nonLinear"} and
                isinstance(original["sha256"], str) and re.fullmatch(r"[a-f0-9]{64}", original["sha256"]) and
                type(original["byteSize"]) is int and 0 < original["byteSize"] <= 1073741824 and original["nonLinear"] is True and
                all(type(original[k]) is int and 0 < original[k] <= 12000 for k in ("width", "height")), "ORIGINAL_DESCRIPTOR")
        assets = {}
        for name, maximum in (("preview", 4 * 1024 * 1024), ("workflow", 2 * 1024 * 1024), ("correlations", 256 * 1024)):
            text = value[name + "Base64"]
            require(isinstance(text, str) and 0 < len(text) <= ((maximum + 2) // 3) * 4, "RESULT_SIZE")
            try:
                assets[name] = base64.b64decode(text, validate=True)
            except ValueError:
                require(False, "RESULT_ENCODING")
            require(0 < len(assets[name]) <= maximum, "RESULT_SIZE")
        preview = sanitize_preview(assets["preview"], "image/jpeg")
        selection = context["selection"]
        catalog, _ = self.store.get("science/catalogs/" + selection["catalogSha256"])
        review = build_review(catalog_raw=catalog, catalog_digest=selection["catalogSha256"], session_ids=selection["sessionIds"],
            title=selection["title"], processing_date=selection["processingDate"], original_raw=b"XISF0100",
            original_media_type="application/x-xisf", preview_raw=preview, preview_media_type="image/jpeg",
            workflow_raw=assets["workflow"], receipt_id="BKL049-" + job_id, imported_at=context["createdAt"], preview_attested=True)
        packet = review["workflow"]
        require(packet["extractionState"] == "PARSED_SUBSET", "RUNTIME_WORKFLOW_REQUIRED")
        archive = packet["archive"]
        instances = archive["instances"]
        root = instances[archive["root"]]
        require(root["process"] == "ProcessContainer", "RUNTIME_WORKFLOW_REQUIRED")
        steps = [{"ordinal": i + 1, "processId": instances[name]["process"]} for i, name in enumerate(root["children"])]
        require([s["processId"] for s in steps] == [a[1] for a in actions(NONLINEAR_RECIPE)], "RUNTIME_WORKFLOW_REQUIRED")
        correlations = decode(assets["correlations"])
        require(isinstance(correlations, dict) and correlations.get("jobId") == job_id and correlations.get("recipe") == NONLINEAR_RECIPE and
                correlations.get("upstreamHistoryCompleteness") == "NOT_ESTABLISHED" and isinstance(correlations.get("instances"), list) and
                len(correlations["instances"]) == 29 and
                [i.get("ordinal") for i in correlations["instances"]] == list(range(1,30)) and
                [i.get("variable") for i in correlations["instances"]] == root["children"], "CORRELATIONS_BINDING")
        # Dependencies are local view identifiers or manifest-bound master roles.
        for row in correlations["instances"] + correlations.get("runtimeRelations", []):
            require(isinstance(row, dict) and all(isinstance(dep, str) and
                    re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", dep) and not re.fullmatch(r"[a-f0-9]{64}", dep)
                    for dep in row.get("dependencies", [])), "CORRELATIONS_PRIVACY")
        receipt = {"jobId": job_id, "context": context, "original": original,
                   "imageId": selection["parent"]["imageId"] if selection["parent"] else "IMG-" + job_id[5:],
                   "imageVersionId": "VER-" + job_id[5:], "workflowId": "WF-" + job_id[5:],
                   "previewSha256": digest(preview), "workflowSha256": digest(assets["workflow"]),
                   "correlationsSha256": digest(assets["correlations"]),
                   "steps": steps, "executionEvidence": "WORKER_REPORTED_NOT_ATTESTED",
                   "workflowCompleteness": "RUNTIME_RECIPE_ONLY", "upstreamHistoryCompleteness": "NOT_ESTABLISHED",
                   "scientificAcceptance": "OWNER_REVIEW_REQUIRED", "publication": "NONE", "originalLocation": "OWNER_PC"}
        receipt["reviewSha256"] = digest(encode(receipt))
        immutable(self.store, "science/assets/" + receipt["previewSha256"], preview)
        immutable(self.store, "science/assets/" + receipt["workflowSha256"], assets["workflow"])
        immutable(self.store, "science/assets/" + receipt["correlationsSha256"], assets["correlations"])
        immutable(self.store, "science/results/" + job_id, encode(receipt))
        return receipt

    def result(self, job_id):
        context = self.context(job_id)
        raw, _ = self.store.get("science/results/" + job_id)
        require(raw is not None, "RESULT_PENDING")
        result = decode(raw)
        require(result.get("jobId") == job_id and result.get("context") == context and
                result.get("reviewSha256") == digest(encode({k:v for k,v in result.items() if k != "reviewSha256"})), "RESULT_INTEGRITY")
        decision, _ = self.store.get("science/decisions/" + job_id)
        result["decision"] = decode(decision) if decision else None
        require(result["decision"] is None or (result["decision"].get("reviewSha256") == result["reviewSha256"] and
                result["decision"].get("decision") in {"ACCEPT_PRIVATE", "REJECT"}), "DECISION_INTEGRITY")
        return result

    def asset(self, job_id, role):
        require(role in {"preview", "workflow", "correlations"}, "ASSET_ROLE")
        result = self.result(job_id)
        raw, _ = self.store.get("science/assets/" + result[role + "Sha256"])
        require(raw is not None and digest(raw) == result[role + "Sha256"], "ASSET_INTEGRITY")
        return raw

    def decide(self, job_id, value):
        result = self.result(job_id)
        require(isinstance(value, dict) and set(value) == {"reviewSha256", "decision"} and value["reviewSha256"] == result["reviewSha256"] and
                value["decision"] in {"ACCEPT_PRIVATE", "REJECT"}, "REVIEW_CHANGED")
        immutable(self.store, "science/decisions/" + job_id, encode(value))
        return {"decision": value, "publication": "NONE"}

    def jobs(self):
        state, _ = self.broker._state()
        return [self.broker._view(j) for j in state["jobs"] if j.get("scientificContextSha256") and self.store.exists("science/contexts/" + j["jobId"])]
