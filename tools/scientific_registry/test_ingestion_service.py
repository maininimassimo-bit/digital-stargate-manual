import io
import json
import unittest
from unittest.mock import patch
from PIL import Image

from .ingestion_service import IngestionService, json_bytes, CHUNK_BYTES
from .ingestion_storage import MemoryStore, Conflict
from .photo_ingestion import IngestionError, sha256


class Scanner:
    def __init__(self, state="PASS"):
        self.state = state
    def scan(self, _):
        return self.state


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.store = MemoryStore()
        self.catalog = json_bytes({"schemaVersion": "1.5", "catalogStatus": "VERSIONED_ANALYTICS_PROJECTION",
            "sessions": [{"sessionId": "night1", "target": "M31"}, {"sessionId": "night2", "target": "M31"}]})
        self.service = IngestionService(self.store, self.catalog, Scanner(), "https://example.run.app")
        output = io.BytesIO()
        image = Image.new("RGB", (30, 20), "red")
        exif = Image.Exif()
        exif[270] = "private description"
        image.save(output, format="JPEG", exif=exif)
        self.files = {"original": b"XISF0100scientific bytes", "preview": output.getvalue(),
                      "workflow": b'var P = new PixelMath; P.expression = "private path"; P.n = 0.250;'}
        self.request = {"idempotencyKey": "synthetic-key-001", "catalogSha256": sha256(self.catalog), "imageId": None, "title": "M31 final",
            "sessionIds": ["night1", "night2"], "processingDate": "2026-10-02", "previewAttested": True,
            "files": {role: {"byteSize": len(raw), "sha256": sha256(raw), "mediaType": media}
                for (role, raw), media in zip(self.files.items(), ("application/x-xisf", "image/jpeg", "text/plain"))}}
        self.owner = "owner@example.com"

    def uploaded(self):
        item = self.service.create(self.request, self.owner)
        for role, raw in self.files.items():
            for i in range((len(raw) + CHUNK_BYTES - 1) // CHUNK_BYTES):
                self.service.chunk(item["id"], role, i, raw[i * CHUNK_BYTES:(i + 1) * CHUNK_BYTES], self.owner)
        return item["id"]

    def selection(self, uid, publish=True):
        review = self.service.review_summary(uid, self.owner)
        return {"reviewSha256": review["reviewSha256"], "publish": publish, "rightsConfirmed": publish,
                "steps": [{"stepId": s["stepId"], "processId": s["processId"], "parameters": []} for s in review["steps"]]}

    def test_complete_private_then_public_withdrawal_and_exact_source_preservation(self):
        uid = self.uploaded()
        selection = self.selection(uid, False)
        self.assertEqual(self.service.commit(uid, selection, self.owner)["state"], "SAVED_PRIVATE")
        self.assertEqual(self.service.collection()["records"], [])
        selection.update(publish=True, rightsConfirmed=True)
        self.service.commit(uid, selection, self.owner)
        public = self.service.collection()["records"][0]
        self.assertEqual(public["sessionIds"], ["night1", "night2"])
        self.assertIsNone(public["validUntil"])
        self.assertNotIn("private path", json.dumps(public))
        preview = self.service.preview(uid)
        with Image.open(io.BytesIO(preview)) as image:
            self.assertFalse(image.getexif())
        for raw in self.files.values():
            self.assertEqual(self.store.get("assets/" + sha256(raw))[0], raw)
        before = len(self.service._state()[0]["audit"])
        self.service.commit(uid, selection, self.owner)
        self.assertEqual(len(self.service._state()[0]["audit"]), before)
        self.service.withdraw(uid, self.owner)
        self.assertEqual(self.service.collection()["records"], [])
        with self.assertRaises(IngestionError):
            self.service.preview(uid)
        with self.assertRaises(IngestionError):
            self.service.commit(uid, selection, self.owner)

    def test_versions_and_restart_keep_previous_assets(self):
        uid = self.uploaded()
        self.service.commit(uid, self.selection(uid, False), self.owner)
        self.service = IngestionService(self.store, self.catalog, Scanner(), "https://example.run.app")
        self.assertEqual(self.service.archive(self.owner)[0]["state"], "SAVED_PRIVATE")
        self.request["imageId"] = self.service.archive(self.owner)[0]["imageId"]
        self.request["idempotencyKey"] = "synthetic-key-002"
        uid2 = self.uploaded()
        self.service.commit(uid2, self.selection(uid2), self.owner)
        self.assertNotEqual(uid, uid2)
        self.assertEqual(self.service.archive(self.owner)[0]["imageId"], self.service.collection()["records"][0]["imageId"])

    def test_resume_chunk_retry_conflicting_bytes_and_incomplete_upload(self):
        self.files["original"] = b"XISF0100" + b"0" * CHUNK_BYTES
        self.request["files"]["original"].update(byteSize=len(self.files["original"]), sha256=sha256(self.files["original"]))
        item = self.service.create(self.request, self.owner)
        uid = item["id"]
        first = self.files["original"][:CHUNK_BYTES]
        self.service.chunk(uid, "original", 0, first, self.owner)
        self.service.chunk(uid, "original", 0, first, self.owner)
        with self.assertRaises(Conflict):
            self.service.chunk(uid, "original", 0, b"1" * CHUNK_BYTES, self.owner)
        self.assertEqual(self.service.status(uid, self.owner)["received"]["original"], [0])
        with self.assertRaises(IngestionError):
            self.service.review(uid, self.owner)
        self.assertEqual(self.service.create(self.request, self.owner)["id"], uid)
        self.request["title"] = "changed"
        with self.assertRaises(IngestionError):
            self.service.create(self.request, self.owner)

    def test_scanner_unavailable_or_malware_cannot_publish_but_private_retention_works(self):
        for state in ("UNAVAILABLE", "FAIL"):
            with self.subTest(state=state):
                self.setUp()
                self.service.scanner = Scanner(state)
                uid = self.uploaded()
                selection = self.selection(uid)
                with self.assertRaises(IngestionError):
                    self.service.commit(uid, selection, self.owner)
                selection.update(publish=False, rightsConfirmed=False)
                self.assertEqual(self.service.commit(uid, selection, self.owner)["state"], "SAVED_PRIVATE")

    def test_stale_approval_changed_parameter_or_another_actor_reject(self):
        uid = self.uploaded()
        selection = self.selection(uid)
        with self.assertRaises(IngestionError):
            self.service.status(uid, "other@example.com")
        with self.assertRaises(IngestionError):
            self.service.commit(uid, selection | {"reviewSha256": "0" * 64}, self.owner)
        from tools.pixinsight.workflow_archive.archive import ArchiveError
        selection["steps"][0]["parameters"] = [{"name": "n", "valueSha256": "0" * 64}]
        with self.assertRaises(ArchiveError):
            self.service.commit(uid, selection, self.owner)

    def test_lost_generation_is_retried_and_no_partial_publication(self):
        uid = self.uploaded()
        selection = self.selection(uid)
        previous = self.store.put
        failures = []
        def conflict_once(key, raw, generation=0):
            if key == "control/state.json" and not failures:
                failures.append(True)
                raise Conflict("simulated concurrent update")
            return previous(key, raw, generation)
        with patch.object(self.store, "put", side_effect=conflict_once):
            self.service.commit(uid, selection, self.owner)
        self.assertEqual(len(self.service.collection()["records"]), 1)

    def test_recheck_replaces_quarantined_review_and_rejects_old_approval(self):
        self.service.scanner = Scanner("UNAVAILABLE")
        uid = self.uploaded()
        old = self.selection(uid, False)
        self.service.commit(uid, old, self.owner)
        self.service.scanner = Scanner("PASS")
        current = self.service.review_summary(uid, self.owner, recheck=True)
        self.assertTrue(current["publicationEligible"])
        self.assertNotEqual(current["reviewSha256"], old["reviewSha256"])
        with self.assertRaises(IngestionError):
            self.service.commit(uid, old, self.owner)

    def test_catalogue_changed_new_upload_rejects_but_exact_resume_uses_retained_snapshot(self):
        uid = self.uploaded()
        old_request = json.loads(json.dumps(self.request))
        new_catalog = self.catalog.replace(b'M31', b'M42')
        self.service.catalog_loader = lambda: new_catalog
        self.assertEqual(self.service.create(old_request, self.owner)["id"], uid)
        saved = self.service.status(uid, self.owner)
        self.assertEqual(saved["request"], old_request)
        self.assertEqual(saved["frozenSessionContext"][0]["target"], "M31")
        self.assertEqual([s["sessionId"] for s in saved["frozenSessionContext"]], old_request["sessionIds"])
        self.request["idempotencyKey"] = "synthetic-new-key"
        with self.assertRaisesRegex(IngestionError, "CATALOG_CHANGED_REFRESH"):
            self.service.create(self.request, self.owner)
        self.assertEqual(self.service.review_summary(uid, self.owner)["target"], "M31")

    def test_exact_selected_parameter_stays_selected_in_readonly_published_review(self):
        uid = self.uploaded()
        review = self.service.review_summary(uid, self.owner)
        selection = self.selection(uid)
        parameter = next(p for p in review["steps"][0]["parameters"] if p["name"] == "n")
        selection["steps"][0]["parameters"] = [{"name": parameter["name"], "valueSha256": parameter["valueSha256"]}]
        self.service.commit(uid, selection, self.owner)
        current = self.service.review_summary(uid, self.owner)
        self.assertEqual(current["publishedFields"]["steps"][0]["parameters"], [{"name": "n", "lexicalJson": parameter["lexicalJson"]}])
        self.assertNotIn("private-path", json.dumps(current["publishedFields"]))

    def test_separate_backup_failure_prevents_primary_write_and_replay(self):
        from .ingestion_storage import BackedUpStore
        backup = MemoryStore()
        primary = self.store
        self.service.store = BackedUpStore(primary, backup)
        uid = self.uploaded()
        selection = self.selection(uid)
        for key, (raw, _) in primary.items.items():
            recovery_key = "recovery/" + sha256(key.encode()) + "/" + sha256(raw)
            self.assertEqual(backup.get(recovery_key)[0], raw)
        previous_state = primary.get("control/state.json")
        with patch.object(backup, "put", side_effect=OSError("backup unavailable")):
            with self.assertRaises(OSError):
                self.service.commit(uid, selection, self.owner)
        self.assertEqual(primary.get("control/state.json"), previous_state)
        self.assertEqual(self.service.collection()["records"], [])


if __name__ == "__main__":
    unittest.main()
