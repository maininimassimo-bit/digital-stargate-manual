import json
import unittest

from tools.scientific_registry.photo_ingestion import build_review, sha256, IngestionError


class PhotoIngestionTests(unittest.TestCase):
    def args(self):
        catalog = json.dumps({"schemaVersion": "1.5", "catalogStatus": "VERSIONED_ANALYTICS_PROJECTION",
                              "sessions": [{"sessionId": "night1", "target": "M31", "observationDate": "2026-07-14"},
                                           {"sessionId": "night2", "target": "M31"},
                                           {"sessionId": "night3", "target": "M42"}]}).encode()
        return dict(catalog_raw=catalog, catalog_digest=sha256(catalog),
                    session_ids=["night1", "night2"], title="M31", processing_date="2026-10-02",
                    original_raw=b"XISF0100test", original_media_type="application/x-xisf",
                    preview_raw=b"\xff\xd8\xfftest", preview_media_type="image/jpeg",
                    workflow_raw=b"unsupported export", receipt_id="BKL049-test", imported_at="2026-10-02T12:00:00Z",
                    preview_attested=True)

    def test_multinight_is_private_quarantined_and_not_promoted(self):
        result = build_review(**self.args())
        self.assertEqual(len(result["sessionContext"]["sessions"]), 2)
        self.assertFalse(result["publicationEligible"])
        self.assertEqual(result["original"]["state"], "QUARANTINED")
        self.assertEqual(result["workflow"]["extractionState"], "UNSUPPORTED")
        self.assertEqual(result["workflow"]["executionEvidence"], "NOT_ESTABLISHED")
        self.assertIsNone(result["sessionContext"]["sessions"][1]["configurationId"])

    def test_idempotent_across_retries_and_distinct_versions(self):
        args = self.args()
        first = build_review(**args)
        args["imported_at"] = "2026-10-02T13:00:00Z"
        args["receipt_id"] = "BKL049-retry"
        self.assertEqual(first["draftKey"], build_review(**args)["draftKey"])
        args["original_raw"] += b"new version"
        self.assertNotEqual(first["draftKey"], build_review(**args)["draftKey"])

    def test_large_spectrum_is_available_in_private_review_without_publication(self):
        spectrum = 'synthetic' * 8000
        args = self.args()
        args['workflow_raw'] = ('var Root=new ProcessContainer;'
            'var P=new SpectrophotometricColorCalibration;'
            'P.whiteReferenceSpectrum="'+spectrum+'";Root.add(P);').encode()
        review = build_review(**args)
        packet = review['workflow']
        self.assertEqual(packet['importerVersion'], '1.2')
        self.assertEqual(packet['extractionState'], 'PARSED_SUBSET')
        self.assertEqual(packet['archive']['instances']['P']['parameters']['whiteReferenceSpectrum'], spectrum)
        self.assertFalse(review['publicationEligible'])
        self.assertEqual(review['publicationState'], 'PRIVATE_NOT_APPROVED')
        self.assertEqual(packet['executionEvidence'], 'NOT_ESTABLISHED')

    def test_conflicting_target_unknown_session_duplicates_and_tampering_reject(self):
        for changes in ({"session_ids": ["night1", "night3"]}, {"session_ids": ["absent"]},
                        {"session_ids": ["night1", "night1"]}, {"catalog_digest": "0" * 64},
                        {"preview_attested": False}, {"preview_attested": 1},
                        {"preview_raw": b"<script>not a JPEG</script>"},
                        {"processing_date": "2026-02-30"}):
            with self.subTest(changes=changes), self.assertRaises(IngestionError):
                build_review(**(self.args() | changes))


if __name__ == "__main__":
    unittest.main()
