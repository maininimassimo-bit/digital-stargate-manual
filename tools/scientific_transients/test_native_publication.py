"""Synthetic opaque product sets. No PixInsight process or real image decoding."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import encode, ProtocolError
from tools.scientific_transients import native_publication as pub


def sha(raw): return hashlib.sha256(raw).hexdigest()


class NativePublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.operation = "a" * 32
        self.work, self.archive, self.journal = [self.root / n / self.operation
            for n in ["native-work", "native-retained", "native-supervision"]]
        for path in [self.work, self.archive, self.journal]: path.mkdir(parents=True)
        for name in ["launch-seal.json", "launch-grant.json"]: (self.work / name).write_bytes(b"{}")
        self.intent = {"protocol": "DSG_NATIVE_LINEAR_PARENT_INTENT_V1", "operationRef": self.operation,
                       "createdUTC": "2026-10-16T10:00:00Z", "sealSha256": sha(b"{}"), "grantSha256": sha(b"{}")}
        for prefix, path in zip(["nativeWork", "retained", "supervision"], [self.work, self.archive, self.journal]):
            info = path.stat()
            self.intent[prefix + "CanonicalPath"] = path.as_posix()
            self.intent[prefix + "DirectoryIdentity"] = [info.st_dev, info.st_ino]
        self.binding = {"operationRef": self.operation, "parentIntentSha256": "0" * 64,
                        "sealSha256": sha(b"{}"), "grantSha256": sha(b"{}")}
        self.write_intent()
        self.records = []
        for name in sorted(pub.REQUIRED):
            # Deliberately opaque, not actual XISF/History/numeric result payloads.
            raw = ("SYNTHETIC_OPAQUE_" + name).encode("ascii")
            (self.work / name).write_bytes(raw)
            self.records.append({"role": name, "name": name, "sha256": sha(raw), "byteLength": len(raw)})
        self.terminal = {"protocol": "DSG_NATIVE_LINEAR_TERMINAL_V1", "operationRef": self.operation,
            "state": "COMPLETED_CONDITIONAL_COMPUTATION", "errorCode": None, "retentionErrorCode": None,
            "products": copy.deepcopy(self.records), "unclosedOwnedViews": 0, "cooperativeDeadlineExceeded": False,
            "fullPhysicalVariance": None, "significance": None, "scientificValidation": "NOT_VALIDATED",
            "qualifiedControls": 0, "provenanceVerified": False, "physicalApplicabilityVerified": False}
        self.write_terminal()

    def write_intent(self):
        raw = encode(self.intent)
        (self.journal / "parent-intent.json").write_bytes(raw)
        self.binding["parentIntentSha256"] = sha(raw)

    def write_terminal(self, raw=None):
        raw = encode(self.terminal) if raw is None else raw
        (self.work / "terminal.json").write_bytes(raw)
        (self.work / "terminal-ready.json").write_bytes(encode({
            "protocol": "DSG_NATIVE_LINEAR_TERMINAL_READY_V1", "operationRef": self.operation,
            "terminalSha256": sha(raw)}))

    def publish(self, clock=lambda: 1, deadline=180):
        return pub.publish_native_bundle(self.work, self.archive, self.journal,
                                         self.binding, clock=clock, deadline=deadline)

    def assert_uncertain(self):
        self.assertTrue((self.journal / "publication-uncertain.json").exists())
        self.assertFalse((self.archive / "retained-native-terminal.json").exists())

    def test_complete_set_raw_chain_and_no_lifecycle_or_science_authority(self):
        outcome = self.publish()
        marker = outcome["marker"]
        self.assertEqual(len(marker["products"]), 14)
        for row in marker["products"]:
            self.assertEqual((self.archive / row["name"]).read_bytes(), (self.work / row["name"]).read_bytes())
        self.assertFalse(outcome["processClosureAuthorized"])
        self.assertFalse(outcome["newNativeStartAllowed"])
        self.assertFalse(marker["measurementAccepted"])
        self.assertEqual(marker["qualifiedControls"], 0)
        self.assertEqual(outcome["markerSha256"], sha((self.archive / "retained-native-terminal.json").read_bytes()))
        before = (self.archive / "retained-native-terminal.json").read_bytes()
        with self.assertRaises(pub.PublicationFailure): self.publish()
        self.assertEqual((self.archive / "retained-native-terminal.json").read_bytes(), before)

    def test_missing_required_success_history_rejected(self):
        self.terminal["products"] = [r for r in self.terminal["products"] if r["name"] != "closing-source.js"]
        self.write_terminal()
        with self.assertRaisesRegex(pub.PublicationFailure, "PUBLICATION_INCOMPLETE_SUCCESS"): self.publish()
        self.assert_uncertain()

    def test_missing_ready_retains_uncertainty_and_reservation(self):
        (self.work / "terminal-ready.json").unlink()
        with self.assertRaises(pub.PublicationFailure): self.publish()
        self.assert_uncertain()
        self.assertTrue((self.journal / "publication-intent.json").exists())

    def test_prior_partial_uncertainty_without_reservation_blocks_before_any_copy(self):
        path = self.journal / "publication-uncertain.json"
        path.write_bytes(b'{"partial":')
        with self.assertRaisesRegex(pub.PublicationFailure, "PUBLICATION_PRIOR_UNCERTAINTY"):
            self.publish()
        self.assertEqual(path.read_bytes(), b'{"partial":')
        self.assertFalse((self.journal / "publication-intent.json").exists())
        self.assertEqual(list(self.archive.iterdir()), [])

    def test_native_partial_failure_fence_blocks_stale_ready_before_reservation(self):
        (self.work / "native-publication-uncertain.json").write_bytes(b'{"partial":')
        with self.assertRaisesRegex(pub.PublicationFailure, "PUBLICATION_NATIVE_UNCERTAINTY"):
            self.publish()
        self.assertFalse((self.journal / "publication-intent.json").exists())
        self.assert_uncertain()
        self.assertEqual(list(self.archive.iterdir()), [])

    def test_initial_reservation_write_failure_with_uncertainty_blocks_retry(self):
        original = pub._write_control
        def failure(path, value):
            if path.name == "publication-intent.json": raise OSError("synthetic pre-create failure")
            return original(path, value)
        with patch.object(pub, "_write_control", side_effect=failure):
            with self.assertRaises(pub.PublicationFailure) as raised: self.publish()
        self.assertTrue(raised.exception.uncertain_marker_written)
        self.assertFalse((self.journal / "publication-intent.json").exists())
        with self.assertRaisesRegex(pub.PublicationFailure, "PUBLICATION_PRIOR_UNCERTAINTY"):
            self.publish()
        self.assertEqual(list(self.archive.iterdir()), [])

    def test_collision_including_identical_file_rejected(self):
        name = "native.log"
        (self.archive / name).write_bytes((self.work / name).read_bytes())
        with self.assertRaisesRegex(pub.PublicationFailure, "PUBLICATION_RETAINED_COLLISION"): self.publish()
        self.assert_uncertain()
        self.assertEqual(len(list(self.archive.iterdir())), 1)

    def test_terminal_hash_or_duplicate_json_rejected(self):
        raw = (self.work / "terminal.json").read_bytes() + b" "
        (self.work / "terminal.json").write_bytes(raw)
        with self.assertRaisesRegex(pub.PublicationFailure, "PUBLICATION_TERMINAL_HASH"): self.publish()
        self.assert_uncertain()

    def test_duplicate_escaped_key_rejected(self):
        raw = encode(self.terminal)
        raw = b'{"\\u0070rotocol":"DSG_NATIVE_LINEAR_TERMINAL_V1",' + raw[1:]
        self.write_terminal(raw)
        with self.assertRaises(pub.PublicationFailure): self.publish()
        self.assert_uncertain()

    def test_false_or_nonzero_science_flags_rejected(self):
        for field, value in [("qualifiedControls", False), ("significance", 1), ("physicalApplicabilityVerified", True)]:
            modified = copy.deepcopy(self.terminal); modified[field] = value
            with self.subTest(field=field), self.assertRaises(ProtocolError): pub._terminal(modified, self.operation)

    def test_failure_can_be_archived_with_unclosed_views_without_close_permission(self):
        self.terminal.update(state="FAILED_RETAINED", errorCode="SYNTHETIC_FAILURE", unclosedOwnedViews=1)
        self.write_terminal()
        outcome = self.publish()
        self.assertEqual(outcome["marker"]["unclosedOwnedViews"], 1)
        self.assertFalse(outcome["processClosureAuthorized"])

    def test_parent_overrun_records_true_without_computation_acceptance(self):
        outcome = self.publish(clock=lambda: 200)
        self.assertTrue(outcome["marker"]["parentMonotonicDeadlineExceeded"])
        self.assertFalse(outcome["marker"]["measurementAccepted"])

    def test_deadline_crossing_marker_preserves_stale_marker_and_uncertainty(self):
        clock = iter([179, 181])
        with self.assertRaisesRegex(pub.PublicationFailure, "PUBLICATION_DEADLINE_CROSSED_DURING_MARKER"):
            self.publish(clock=lambda: next(clock))
        self.assertTrue((self.archive / "retained-native-terminal.json").exists())
        self.assertTrue((self.journal / "publication-uncertain.json").exists())
        with self.assertRaises(pub.PublicationFailure): self.publish()

    def test_backward_or_invalid_parent_clock_is_uncertain(self):
        clock = iter([10, 9])
        with self.assertRaisesRegex(pub.PublicationFailure, "PUBLICATION_CLOCK_CHANGED"):
            self.publish(clock=lambda: next(clock))
        self.assertTrue((self.journal / "publication-uncertain.json").exists())

    def test_same_bytes_earlier_source_replacement_detected_at_final_verification(self):
        original = pub.retain_opaque_product
        first = self.terminal["products"][0]["name"]
        def mutate(work, archive, name, expected):
            result = original(work, archive, name, expected)
            if name == "terminal-ready.json":
                replacement = work / "replacement"
                replacement.write_bytes((work / first).read_bytes())
                replacement.replace(work / first)
            return result
        with patch.object(pub, "retain_opaque_product", side_effect=mutate):
            with self.assertRaisesRegex(pub.PublicationFailure, "RETENTION_IDENTITY_CHANGED"): self.publish()
        self.assert_uncertain()
        self.assertEqual(len(list(self.archive.iterdir())), 14)

    def test_partial_copy_error_and_uncertainty_write_failure_never_return_success(self):
        original = pub.retain_opaque_product
        count = 0
        def fail_copy(*args):
            nonlocal count
            count += 1
            if count == 2: raise OSError("synthetic copy failure")
            return original(*args)
        original_write = pub._write_control
        def fail_uncertain(path, value):
            if path.name == "publication-uncertain.json": raise OSError("synthetic marker failure")
            return original_write(path, value)
        with patch.object(pub, "retain_opaque_product", side_effect=fail_copy), \
             patch.object(pub, "_write_control", side_effect=fail_uncertain):
            with self.assertRaises(pub.PublicationFailure) as raised: self.publish()
        self.assertFalse(raised.exception.uncertain_marker_written)
        self.assertEqual(len(list(self.archive.iterdir())), 1)
        self.assertTrue((self.journal / "publication-intent.json").exists())
        with self.assertRaises(pub.PublicationFailure): self.publish()

    def test_role_size_and_aggregate_checked_before_copy(self):
        self.terminal["products"][0]["byteLength"] = 192 * pub.MIB + 1
        self.write_terminal()
        with self.assertRaises(pub.PublicationFailure): self.publish()
        self.assert_uncertain()
        self.assertEqual(list(self.archive.iterdir()), [])

    def test_aggregate_excess_rejected_without_allocating_or_copying_large_payload(self):
        for record in self.terminal["products"]:
            if record["name"] == "checkpoint.xisf": record["byteLength"] = 192 * pub.MIB
        self.write_terminal()
        with self.assertRaisesRegex(pub.PublicationFailure, "PUBLICATION_AGGREGATE"): self.publish()
        self.assert_uncertain()
        self.assertEqual(list(self.archive.iterdir()), [])

    def test_marker_io_failure_preserves_payloads_and_uncertainty(self):
        original = pub._write_control
        def failure(path, value):
            result = original(path, value)
            if path.name == "retained-native-terminal.json": raise OSError("synthetic after marker IO")
            return result
        with patch.object(pub, "_write_control", side_effect=failure):
            with self.assertRaises(pub.PublicationFailure): self.publish()
        self.assertTrue((self.archive / "retained-native-terminal.json").exists())
        self.assertTrue((self.journal / "publication-uncertain.json").exists())
        with self.assertRaises(pub.PublicationFailure): self.publish()

    def test_mutations_during_marker_write_reject_positive_but_stale_marker(self):
        # Each case is a separate attempt, without modifying any real image.
        for target in ["retained-result", "source-result", "parent-pin", "marker-replacement", "inventory", "uncertainty", "native-uncertainty"]:
            with self.subTest(target=target):
                case = NativePublicationTests(methodName="test_complete_set_raw_chain_and_no_lifecycle_or_science_authority")
                case.setUp()
                self.addCleanup(case.doCleanups)
                original = pub._write_control
                def mutate(path, value):
                    result = original(path, value)
                    if path.name == "retained-native-terminal.json":
                        if target == "retained-result":
                            p = case.archive / "result.json"; p.write_bytes(b"x" * p.stat().st_size)
                        elif target == "source-result":
                            p = case.work / "result.json"; p.write_bytes(b"x" * p.stat().st_size)
                        elif target == "parent-pin":
                            p = case.journal / "parent-intent.json"; p.write_bytes(b"x" * p.stat().st_size)
                        elif target == "marker-replacement":
                            replacement = case.archive / "replacement"
                            replacement.write_bytes(path.read_bytes()); replacement.replace(path)
                        elif target == "inventory": (case.archive / "unexpected.dat").write_bytes(b"synthetic")
                        elif target == "uncertainty": (case.journal / "publication-uncertain.json").write_bytes(b"synthetic partial")
                        else: (case.work / "native-publication-uncertain.json").write_bytes(b"synthetic partial")
                    return result
                with patch.object(pub, "_write_control", side_effect=mutate):
                    with self.assertRaises(pub.PublicationFailure): case.publish()
                self.assertTrue((case.archive / "retained-native-terminal.json").exists())
                self.assertTrue((case.journal / "publication-uncertain.json").exists())
                with self.assertRaises(pub.PublicationFailure): case.publish()

    def test_wrong_parent_root_identity_rejected(self):
        self.intent["nativeWorkDirectoryIdentity"][1] += 1
        self.write_intent()
        with self.assertRaisesRegex(pub.PublicationFailure, "PUBLICATION_INTENT_ROOT"): self.publish()
        self.assert_uncertain()
        self.assertTrue((self.journal / "publication-intent.json").exists())

    def test_source_pin_change_rejected(self):
        (self.work / "launch-grant.json").write_bytes(b"{ }")
        with self.assertRaisesRegex(pub.PublicationFailure, "PUBLICATION_LAUNCH_PIN"): self.publish()
        self.assert_uncertain()

    def test_unlisted_error_product_rejected(self):
        (self.work / "error-owned-1.xisf").write_bytes(b"SYNTHETIC_UNLISTED")
        with self.assertRaisesRegex(pub.PublicationFailure, "PUBLICATION_UNLISTED_PRODUCT"): self.publish()
        self.assert_uncertain()

    def test_control_large_array_and_numeric_float_rejected(self):
        for raw in [encode({"a": list(range(21))}), b'{"x":1.5}', b'{"x":1e999}',
                    b'{"a":{"constructor":1}}']:
            path = self.work / "control-test.json"; path.write_bytes(raw)
            with self.subTest(raw=raw), self.assertRaises(ProtocolError): pub._read_control(path)

    def test_result_payload_is_opaque_not_array20_parsed(self):
        raw = encode({"latentResponses": list(range(200))})
        (self.work / "result.json").write_bytes(raw)
        for record in self.terminal["products"]:
            if record["name"] == "result.json": record.update(sha256=sha(raw), byteLength=len(raw))
        self.write_terminal()
        self.assertFalse(self.publish()["marker"]["measurementAccepted"])

    def test_fence_arriving_during_last_marker_readback_blocks_normal_return(self):
        for native in [True, False]:
            with self.subTest(native=native):
                case = NativePublicationTests(methodName="test_complete_set_raw_chain_and_no_lifecycle_or_science_authority")
                case.setUp(); self.addCleanup(case.doCleanups)
                original = pub._hash_bounded
                def late_fence(path, size, expected_stat):
                    result = original(path, size, expected_stat)
                    if path.name == "retained-native-terminal.json":
                        target = case.work / "native-publication-uncertain.json" if native else case.journal / "publication-uncertain.json"
                        target.write_bytes(b"SYNTHETIC_PARTIAL_FENCE")
                    return result
                with patch.object(pub, "_hash_bounded", side_effect=late_fence):
                    with self.assertRaises(pub.PublicationFailure): case.publish()
                self.assertTrue((case.archive / "retained-native-terminal.json").exists())
                self.assertTrue((case.journal / "publication-uncertain.json").exists())
                with self.assertRaises(pub.PublicationFailure): case.publish()


if __name__ == "__main__": unittest.main()
