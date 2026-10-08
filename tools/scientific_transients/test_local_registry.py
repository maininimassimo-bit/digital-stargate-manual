"""Synthetic files, actual read-only hashing and exclusive writes; no native OAT."""
import copy
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError, decode, encode
from tools.scientific_transients.local_registry import LocalRegistry, ROLES, fingerprint


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.artifacts, self.registry = root / "artifacts", root / "registry"
        self.artifacts.mkdir(); self.registry.mkdir()
        self.local = LocalRegistry(self.artifacts, self.registry)
        self.binding = {k: str(i) * 32 for i, k in enumerate(
            ["bindingRef", "inputRef", "referenceRef", "algorithmRef", "contractRef"], 1)}
        self.manifest = {"protocol": "DSG_TRANSIENT_LOCAL_BINDING_V1", "binding": self.binding, "files": []}
        for i, role in enumerate(sorted(ROLES)):
            path = self.artifacts / (role + ".dat")
            path.write_bytes(("private fixture " + str(i)).encode())
            self.manifest["files"].append({"role": role, "path": path.name, **fingerprint(path)})

    def register(self, value=None):
        return self.local.register(encode(self.manifest if value is None else value))

    def receipts(self):
        return [decode(p.read_bytes()) for p in self.registry.glob("verification-*.json")]

    def test_round_trip_restart_and_unchanged_artifacts(self):
        before = {p.name: p.read_bytes() for p in self.artifacts.iterdir()}
        result = self.register()
        reopened = LocalRegistry(self.artifacts, self.registry)
        value = reopened.verify(self.binding["bindingRef"], result["manifestSha256"])
        self.assertEqual(value, self.manifest)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.artifacts.iterdir()})
        self.assertEqual(result["scientificValidation"], "NOT_VALIDATED")
        self.assertEqual(len(self.receipts()), 2)

    def test_exact_retry_preserves_binding_and_journals_each_verification(self):
        a = self.register(); b = self.register()
        self.assertEqual(a, b)
        self.assertEqual(len(list(self.registry.glob("binding-*.json"))), 1)
        self.assertEqual(len(self.receipts()), 2)

    def test_changed_artifact_rejects_and_records_failure(self):
        result = self.register()
        path = self.artifacts / self.manifest["files"][0]["path"]
        path.write_bytes(b"mutated")
        with self.assertRaisesRegex(ProtocolError, "LOCAL_BYTES_MISMATCH"):
            self.local.verify(self.binding["bindingRef"], result["manifestSha256"])
        self.assertEqual(sum(r["status"] == "FAILED" for r in self.receipts()), 1)

    def test_conflicting_binding_never_overwrites_previous_manifest(self):
        self.register()
        path = self.registry / ("binding-" + self.binding["bindingRef"] + ".json")
        before = path.read_bytes()
        value = copy.deepcopy(self.manifest); value["binding"]["contractRef"] = "a" * 32
        with self.assertRaisesRegex(ProtocolError, "LOCAL_BINDING_CONFLICT"):
            self.register(value)
        self.assertEqual(path.read_bytes(), before)

    def test_partial_write_is_retained_and_not_repaired_on_retry(self):
        path = self.registry / ("binding-" + self.binding["bindingRef"] + ".json")
        path.write_bytes(b'{"partial":')
        with self.assertRaisesRegex(ProtocolError, "LOCAL_BINDING_CONFLICT"):
            self.register()
        self.assertEqual(path.read_bytes(), b'{"partial":')

    def test_manifest_mutation_rejected_by_expected_digest(self):
        result = self.register()
        path = self.registry / ("binding-" + self.binding["bindingRef"] + ".json")
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaisesRegex(ProtocolError, "LOCAL_MANIFEST_CHANGED"):
            self.local.verify(self.binding["bindingRef"], result["manifestSha256"])

    def test_closed_schema_duplicate_keys_missing_roles_and_unsafe_paths(self):
        for extra in ["https://example.org/a", "../outside", "/absolute", "a\\b", "a//b", ".", "a/../b"]:
            value = copy.deepcopy(self.manifest); value["files"][0]["path"] = extra
            with self.assertRaises(ProtocolError): self.register(value)
        for mutate in [lambda v: v.update(execute=True),
                       lambda v: v["files"].pop(),
                       lambda v: v["files"][0].update(bytes=True),
                       lambda v: v["files"][0].update(path=v["files"][1]["path"])]:
            value = copy.deepcopy(self.manifest); mutate(value)
            with self.assertRaises(ProtocolError): self.register(value)
        with self.assertRaises(ProtocolError): self.local.register(b'{"protocol":1,"protocol":2}')

    def test_invalid_claimed_bytes_do_not_create_binding(self):
        value = copy.deepcopy(self.manifest); value["files"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ProtocolError, "LOCAL_BYTES_MISMATCH"): self.register(value)
        self.assertFalse(list(self.registry.glob("binding-*.json")))
        self.assertEqual(self.receipts()[0]["status"], "FAILED")

    def test_nested_or_identical_roots_rejected(self):
        nested = self.artifacts / "nested"; nested.mkdir()
        for registry in [self.artifacts, nested]:
            with self.assertRaisesRegex(ProtocolError, "LOCAL_ROOT_OVERLAP"):
                LocalRegistry(self.artifacts, registry)
        with self.assertRaisesRegex(ProtocolError, "LOCAL_ROOT_TRAVERSAL"):
            LocalRegistry(self.artifacts, self.artifacts / ".." / "registry")

    def test_file_and_ancestor_symlinks_rejected(self):
        target = self.artifacts / self.manifest["files"][0]["path"]
        link = self.artifacts / "linked.dat"
        try: os.symlink(target, link)
        except OSError as error: self.skipTest("Runner has no symlink privilege: " + type(error).__name__)
        with self.assertRaisesRegex(ProtocolError, "LOCAL_LINK_OR_REPARSE"): fingerprint(link)
        ancestor = self.registry.parent / "linked-root"
        os.symlink(self.artifacts, ancestor, target_is_directory=True)
        with self.assertRaisesRegex(ProtocolError, "LOCAL_LINK_OR_REPARSE"):
            LocalRegistry(ancestor, self.registry)

    def test_receipt_write_failure_never_returns_success(self):
        original = self.local._write_new
        def fail_receipt(name, raw):
            if name.startswith("verification-"): raise OSError("fixture failure")
            return original(name, raw)
        with patch.object(self.local, "_write_new", side_effect=fail_receipt):
            with self.assertRaises(OSError): self.register()
        self.assertEqual(len(list(self.registry.glob("binding-*.json"))), 1)

    def test_identity_or_mtime_change_rejected_during_read(self):
        path = self.artifacts / self.manifest["files"][0]["path"]
        original = os.fstat
        calls = 0
        def altered(fd):
            nonlocal calls
            calls += 1
            result = original(fd)
            if calls == 2:
                from types import SimpleNamespace
                return SimpleNamespace(st_dev=result.st_dev, st_ino=result.st_ino,
                                       st_size=result.st_size, st_mtime_ns=result.st_mtime_ns + 1,
                                       st_ctime_ns=result.st_ctime_ns)
            return result
        with patch("os.fstat", side_effect=altered):
            with self.assertRaisesRegex(ProtocolError, "LOCAL_FILE_CHANGED"): fingerprint(path)


if __name__ == "__main__": unittest.main()
