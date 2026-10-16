"""Opaque synthetic bytes only. No native launch or astronomical image decode."""
import hashlib
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients.native_retention import retain_opaque_product, CHUNK_BYTES
from tools.scientific_transients import native_retention


class NativeRetentionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source, self.retained = self.root / "work", self.root / "retained"
        self.source.mkdir(); self.retained.mkdir()
        self.raw = bytes(range(256)) * 777
        self.path = self.source / "checkpoint.xisf"
        self.path.write_bytes(self.raw)
        self.expected = {"sha256": hashlib.sha256(self.raw).hexdigest(), "byteLength": len(self.raw)}

    def run_copy(self, **kwargs):
        return retain_opaque_product(self.source, self.retained,
                                     kwargs.get("name", self.path.name),
                                     kwargs.get("expected", self.expected))

    def test_exact_bytes_once_and_collision_even_identical(self):
        result = self.run_copy()
        self.assertEqual((self.retained / self.path.name).read_bytes(), self.raw)
        self.assertEqual(result["scientificValidation"], "NOT_VALIDATED")
        with self.assertRaises(FileExistsError): self.run_copy()
        self.assertEqual(self.path.read_bytes(), self.raw)

    def test_existing_empty_file_is_never_overwritten(self):
        target = self.retained / self.path.name; target.touch()
        with self.assertRaises(FileExistsError): self.run_copy()
        self.assertEqual(target.read_bytes(), b"")

    def test_bad_hash_retains_failed_copy_and_retry_collides(self):
        with self.assertRaises(ProtocolError):
            self.run_copy(expected={**self.expected, "sha256": "0" * 64})
        self.assertEqual((self.retained / self.path.name).read_bytes(), self.raw)
        with self.assertRaises(FileExistsError): self.run_copy()

    def test_size_mismatch_rejected_before_output(self):
        with self.assertRaises(ProtocolError):
            self.run_copy(expected={**self.expected, "byteLength": len(self.raw) + 1})
        self.assertEqual(list(self.retained.iterdir()), [])

    def test_fsync_error_preserves_output(self):
        with patch("tools.scientific_transients.native_retention.os.fsync", side_effect=OSError("synthetic")):
            with self.assertRaises(OSError): self.run_copy()
        self.assertEqual((self.retained / self.path.name).read_bytes(), self.raw)
        with self.assertRaises(FileExistsError): self.run_copy()

    def test_same_size_source_mutation_during_fsync_rejected(self):
        original = os.fsync
        def mutate(fd):
            original(fd)
            self.path.write_bytes(b"x" * len(self.raw))
        with patch("tools.scientific_transients.native_retention.os.fsync", side_effect=mutate):
            with self.assertRaises(ProtocolError): self.run_copy()
        self.assertTrue((self.retained / self.path.name).exists())

    def test_readback_corruption_rejected(self):
        original = os.fsync
        def corrupt(fd):
            original(fd)
            with (self.retained / self.path.name).open("r+b") as stream: stream.write(b"corrupt")
        with patch("tools.scientific_transients.native_retention.os.fsync", side_effect=corrupt):
            with self.assertRaises(ProtocolError): self.run_copy()
        self.assertTrue((self.retained / self.path.name).exists())

    def test_empty_product_is_valid_if_pinned(self):
        self.path.write_bytes(b"")
        result = self.run_copy(expected={"sha256": hashlib.sha256(b"").hexdigest(), "byteLength": 0})
        self.assertEqual(result["byteLength"], 0)

    def test_same_bytes_source_replacement_after_destination_readback_rejected(self):
        original = native_retention._hash_bounded
        def replace_source(path, size, expected_stat):
            result = original(path, size, expected_stat)
            if path.parent == self.retained:
                replacement = self.source / "replacement"
                replacement.write_bytes(self.raw)
                replacement.replace(self.path)
            return result
        with patch.object(native_retention, "_hash_bounded", side_effect=replace_source):
            with self.assertRaisesRegex(ProtocolError, "RETENTION_IDENTITY_CHANGED"):
                self.run_copy()
        self.assertEqual((self.retained / self.path.name).read_bytes(), self.raw)
        with self.assertRaises(FileExistsError): self.run_copy()

    def test_invalid_names_limits_and_boolean_size_rejected(self):
        for name in ["../a", "a/b", "a\\b", "a:b", "CON.txt", "a..b", "a.", "é"]:
            with self.subTest(name=name), self.assertRaises(ProtocolError): self.run_copy(name=name)
        for size in [-1, True, 192 * 1024 * 1024 + 1]:
            with self.subTest(size=size), self.assertRaises(ProtocolError):
                self.run_copy(expected={**self.expected, "byteLength": size})
        self.assertEqual(list(self.retained.iterdir()), [])

    def test_overlapping_roots_rejected(self):
        for target in [self.source, self.source / "nested"]:
            target.mkdir(exist_ok=True)
            with self.assertRaises(ProtocolError):
                retain_opaque_product(self.source, target, self.path.name, self.expected)

    def test_hardlinked_source_rejected(self):
        os.link(self.path, self.root / "alias")
        with self.assertRaises(ProtocolError): self.run_copy()
        self.assertEqual(list(self.retained.iterdir()), [])

    def test_all_stream_reads_are_bounded(self):
        original = Path.open; reads = []
        class Reader:
            def __init__(self, stream): self.stream = stream
            def __enter__(self): self.stream.__enter__(); return self
            def __exit__(self, *args): return self.stream.__exit__(*args)
            def fileno(self): return self.stream.fileno()
            def read(self, count):
                reads.append(count)
                return self.stream.read(count)
        def opened(path, mode="r", *args, **kwargs):
            stream = original(path, mode, *args, **kwargs)
            return Reader(stream) if mode == "rb" else stream
        with patch.object(Path, "open", opened): self.run_copy()
        self.assertTrue(reads)
        self.assertTrue(all(0 < n <= CHUNK_BYTES for n in reads))


if __name__ == "__main__": unittest.main()
