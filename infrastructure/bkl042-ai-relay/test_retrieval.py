import unittest
import importlib.util
from pathlib import Path

from app import validate_answer
from retrieval import SOURCES, _safe_url, retrieve

EXTRA_PROJECTIONS = {
    "docs/data/session-comparison-projection.json": {
        "projectionType": "SESSION_COMPARISON_PROJECTION", "comparisonSetId": "BKL037-SQM-CATALOG-V1",
        "generatedAt": "2026-09-23T05:54:41Z",
        "dimension": "SQM_MEDIAN", "unit": "mag/arcsec2", "comparisonState": "COMPARABLE",
        "descriptiveSummary": {"sampleSize": 15, "median": 20.57},
        "authority": {"acceptanceAuthority": False, "actionAuthority": "NONE"},
    },
    "docs/data/scientific-data-quality-projection.json": {
        "projectionState": "EXPERIMENTAL_NOT_ACCEPTED", "generatedAt": "2026-09-23T05:54:41Z",
        "authority": {"productionUseAuthorized": False, "acceptanceAuthority": False, "actionAuthority": "NONE"},
        "assessments": [{"sessionId": "2026-08-14_2026-08-15", "target": "M 27", "observedAt": "2026-08-14T20:00:00Z",
                         "assessment": {"assessmentState": "UNAVAILABLE", "score": 99.9, "decomposition": [{"value": "must-not-leak"}]}}],
    },
}


def fixture_fetch(fixtures):
    return lambda path: fixtures[path] if path in fixtures else EXTRA_PROJECTIONS[path]

gateway_path = Path(__file__).parents[1] / "bkl042-portal-gateway" / "app.py"
gateway_spec = importlib.util.spec_from_file_location("bkl042_portal_gateway", gateway_path)
gateway = importlib.util.module_from_spec(gateway_spec)
gateway_spec.loader.exec_module(gateway)


class RetrievalTests(unittest.TestCase):
    def test_allowlisted_records_exclude_sensitive_session_fields(self):
        fixtures = {
            "docs/data/scientific-observation-index.json": {"catalogItems": [], "searchDocuments": []},
            "docs/data/target-knowledge-read-model.json": {"targets": [{"canonical_name": "M 27", "identity_state": "validated", "conflict_refs": ["private-conflict-ref"], "target_id": "must-not-leak"}]},
            "docs/data/scientific-session-catalog.json": {
                "sessions": [{
                    "sessionId": "2026-08-14_2026-08-15", "observationDate": "2026-08-14", "target": "M 27",
                    "analyticsState": "ATTENTION_REQUIRED", "metadataState": "REGISTERED",
                    "evidenceState": "SOURCE_METRICS_AVAILABLE", "integrationHours": 4,
                    "completionPct": 25, "severity": "AMBER", "raDeg": 123.4,
                    "decDeg": 55.6, "sourceMetricsPath": "private/path", "serial": "secret",
                }]
            },
        }
        result = retrieve("M 27 session", fixture_fetch(fixtures))
        self.assertEqual(result["state"], "CONFLICT_REQUIRES_REVIEW")
        self.assertGreaterEqual(len(result["records"]), 2)
        serialized = str(result)
        for forbidden in ("123.4", "55.6", "private/path", "secret"):
            self.assertNotIn(forbidden, serialized)
        self.assertTrue(any(record["conflict"] for record in result["records"]))
        self.assertNotIn("private-conflict-ref", serialized)
        self.assertNotIn("must-not-leak", serialized)
        self.assertEqual(result["state"], "CONFLICT_REQUIRES_REVIEW")
        self.assertEqual(len(SOURCES), 5)

    def test_no_match_returns_insufficient_evidence(self):
        fixtures = {
            "docs/data/scientific-observation-index.json": {"catalogItems": [], "searchDocuments": []},
            "docs/data/target-knowledge-read-model.json": {"targets": []},
            "docs/data/scientific-session-catalog.json": {"sessions": []},
        }
        result = retrieve("unlisted imaginary subject", fixture_fetch(fixtures))
        self.assertEqual(result["state"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(result["records"], [])

    def test_compact_astronomical_designation_matches_spaced_catalog_name(self):
        fixtures = {
            "docs/data/scientific-observation-index.json": {"catalogItems": [], "searchDocuments": []},
            "docs/data/target-knowledge-read-model.json": {"targets": []},
            "docs/data/scientific-session-catalog.json": {
                "sessions": [{
                    "sessionId": "2026-08-14_2026-08-15", "observationDate": "2026-08-14", "target": "M 27",
                    "analyticsState": "VALIDATED_ANALYTICS", "metadataState": "REGISTERED",
                    "evidenceState": "CANONICAL_EVIDENCE",
                }]
            },
        }
        result = retrieve("riassumi le sessioni per m27 e indica le fonti", fixture_fetch(fixtures))
        self.assertEqual(result["state"], "EVIDENCE_FOUND")
        self.assertTrue(any(record["source_id"] == "session-catalog" for record in result["records"]))
        self.assertEqual(sum(record["source_id"] == "scientific-data-quality" for record in result["records"]), 0)
        self.assertEqual(sum(record["source_id"] == "session-catalog" for record in result["records"]), 1)
        self.assertEqual(result["method_version"], "bkl042-static-projection-retrieval-v3")

    def test_spaced_designation_matches_compact_index_term(self):
        fixtures = {
            "docs/data/scientific-observation-index.json": {
                "catalogItems": [{"catalogItemId": "catalog-1", "entityId": "session-1"}],
                "searchDocuments": [{"catalogItemId": "catalog-1", "title": "M27", "keywords": []}],
            },
            "docs/data/target-knowledge-read-model.json": {"targets": []},
            "docs/data/scientific-session-catalog.json": {"sessions": [{
                "sessionId": "2026-08-14_2026-08-15", "observationDate": "2026-08-14", "target": "M 27",
            }]},
        }
        result = retrieve("sessioni per M 27", fixture_fetch(fixtures))
        self.assertEqual(result["state"], "EVIDENCE_FOUND")

    def test_quality_source_is_experimental_and_never_exposes_synthetic_scores(self):
        fixtures = {
            "docs/data/scientific-observation-index.json": {"catalogItems": [], "searchDocuments": []},
            "docs/data/target-knowledge-read-model.json": {"targets": []},
            "docs/data/scientific-session-catalog.json": {"sessions": []},
        }
        result = retrieve("M 27 experimental quality", fixture_fetch(fixtures))
        quality = next(record for record in result["records"] if record["source_id"] == "scientific-data-quality")
        self.assertEqual(quality["freshness"], "VERSIONED_EXPERIMENTAL_PROJECTION")
        self.assertEqual(quality["authority"], "EXPERIMENTAL_CONTEXT_ONLY")
        self.assertIn("EXPERIMENTAL_NOT_ACCEPTED", quality["summary"])
        self.assertNotIn("99.9", str(result))
        self.assertNotIn("must-not-leak", str(result))

    def test_sq_m_comparison_query_retrieves_descriptive_projection(self):
        fixtures = {
            "docs/data/scientific-observation-index.json": {"catalogItems": [], "searchDocuments": []},
            "docs/data/target-knowledge-read-model.json": {"targets": []},
            "docs/data/scientific-session-catalog.json": {"sessions": []},
        }
        result = retrieve("confronto SQM sessioni", fixture_fetch(fixtures))
        comparison = next(record for record in result["records"] if record["source_id"] == "session-comparison")
        self.assertEqual(comparison["authority"], "DESCRIPTIVE_PROJECTION")
        self.assertIn("not a quality score", comparison["summary"])

    def test_comparison_citation_route_is_allowlisted(self):
        self.assertEqual(_safe_url("session-comparison/"), "https://maininimassimo-bit.github.io/digital-stargate-manual/session-comparison/")
        self.assertEqual(_safe_url("scientific-data-quality/"), "https://maininimassimo-bit.github.io/digital-stargate-manual/scientific-data-quality/")

    def test_empty_query_and_invalid_projection_fail_closed(self):
        self.assertEqual(retrieve("a", lambda _path: {})["method_version"], "bkl042-static-projection-retrieval-v3")
        with self.assertRaisesRegex(RuntimeError, "SOURCE_INVALID"):
            retrieve("observatory", lambda _path: {})

    def test_missing_source_fails_closed(self):
        def fail(_path):
            raise RuntimeError("SOURCE_UNAVAILABLE")

        with self.assertRaisesRegex(RuntimeError, "SOURCE_UNAVAILABLE"):
            retrieve("observatory", fail)

    def test_citation_routes_are_allowlisted(self):
        self.assertTrue(_safe_url("scientific-session-detail/?sessionId=2026-08-14_2026-08-15"))
        self.assertEqual(_safe_url("https://attacker.invalid/"), "")
        self.assertEqual(_safe_url("scientific-session-detail/?sessionId=../../secret"), "")

    def test_answer_requires_citations_bound_to_retrieved_records(self):
        records = [{"ref": "session-1", "title": "M 27", "url": "https://example.test"}]
        answer = {
            "state": "ANSWERED", "answer": "M 27 è presente nel catalogo.",
            "facts": [{"text": "M 27", "citation_refs": ["session-1"]}],
            "inferences": [], "recommendations": [], "citation_refs": ["session-1"], "limitations": [],
        }
        self.assertEqual(validate_answer(answer, records), records)
        answer["citation_refs"] = ["invented-source"]
        with self.assertRaisesRegex(RuntimeError, "PROVIDER_RESPONSE_INVALID"):
            validate_answer(answer, records)

    def test_gateway_strips_legacy_client_evidence(self):
        payload = {"question": "M 27", "mode": "consultative", "correlation_id": "test-1",
                   "evidence": "untrusted", "citations": ["untrusted"]}
        self.assertEqual(gateway._normalize_payload(payload), {
            "correlation_id": "test-1", "question": "M 27", "mode": "consultative",
        })
        with self.assertRaisesRegex(ValueError, "request fields are invalid"):
            gateway._normalize_payload({**payload, "extra": "reject"})


if __name__ == "__main__":
    unittest.main()
