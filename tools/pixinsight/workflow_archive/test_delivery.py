"""Synthetic retention/replay failures; no real images, cloud or catalog writes."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from .archive import ArchiveError, digest, encode
from .delivery import build_delivery, load_delivery, retain_delivery, verify_delivery
from .test_binding import fixture, invoke


def candidate(parts=None):
    packet, declaration, snapshot, measured, association = parts or fixture()
    return build_delivery(encode(packet), digest(encode(packet)), declaration,
        exported_at='2026-09-30T18:02:00Z', snapshot_bytes=encode(snapshot),
        snapshot_digest=digest(encode(snapshot)), current_snapshot_digest=digest(encode(snapshot)),
        measurement_bytes=encode(measured), measurement_digest=digest(encode(measured)),
        association_bytes=encode(association), association_digest=digest(encode(association)))


def retained_handoff():
    """Used by the Node bridge: real local create/load, synthetic data only."""
    bundle = candidate()
    with tempfile.TemporaryDirectory() as folder:
        receipt = retain_delivery(bundle, folder, bundle['snapshotSha256'])
        return load_delivery(Path(folder) / receipt['filename'], receipt['sha256'], bundle['snapshotSha256'])


class DeliveryTests(unittest.TestCase):
    def test_full_roundtrip_is_guard_result_and_original_retained(self):
        bundle = candidate()
        self.assertEqual(retained_handoff(), invoke(fixture()))
        self.assertEqual(bundle['packet']['source'], fixture()[0]['source'])

    def test_retry_noop_and_changed_binding_content_never_overwrites(self):
        with tempfile.TemporaryDirectory() as folder:
            bundle = candidate(); anchor = bundle['snapshotSha256']
            first = retain_delivery(bundle, folder, anchor)
            self.assertEqual(first['outcome'], 'CREATED')
            path = Path(folder) / first['filename']; before = path.read_bytes()
            self.assertEqual(retain_delivery(bundle, folder, anchor)['outcome'], 'DUPLICATE_NOOP')
            parts = fixture(); parts[4]['declaredAt'] = '2026-09-30T18:01:30Z'
            with self.assertRaisesRegex(ArchiveError, 'RECEIPT_CONFLICT'):
                retain_delivery(candidate(parts), folder, anchor)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(len(list(Path(folder).iterdir())), 1)

    def test_explicit_revision_keeps_both_artifacts(self):
        with tempfile.TemporaryDirectory() as folder:
            original = candidate(); retain_delivery(original, folder, original['snapshotSha256'])
            parts = fixture(); parts[4]['bindingId'] += '-R2'; revised = candidate(parts)
            retain_delivery(revised, folder, revised['snapshotSha256'])
            self.assertEqual(len(list(Path(folder).iterdir())), 2)

    def test_changed_current_revision_rejects_write_and_load(self):
        with tempfile.TemporaryDirectory() as folder:
            bundle = candidate()
            with self.assertRaisesRegex(ArchiveError, 'BINDING_STALE_SNAPSHOT'):
                retain_delivery(bundle, folder, '0'*64)
            self.assertEqual(list(Path(folder).iterdir()), [])
            receipt = retain_delivery(bundle, folder, bundle['snapshotSha256'])
            with self.assertRaisesRegex(ArchiveError, 'BINDING_STALE_SNAPSHOT'):
                load_delivery(Path(folder)/receipt['filename'], receipt['sha256'], '0'*64)

    def test_external_anchor_required_and_corruption_rejected(self):
        bundle = candidate(); raw = encode(bundle)
        for anchor in (None, '', 'x'*64, '0'*64):
            with self.subTest(anchor=anchor), self.assertRaises(ArchiveError):
                verify_delivery(raw, anchor, bundle['snapshotSha256'])
        with self.assertRaisesRegex(ArchiveError, 'DELIVERY_INTEGRITY'):
            verify_delivery(raw+b' ', digest(raw), bundle['snapshotSha256'])

    def test_forged_derived_output_cannot_be_laundered_with_new_hash(self):
        for section in ('receipt', 'sidecar', 'reconciliationInput'):
            bundle = candidate(); bundle['result'][section] = {}
            raw = encode(bundle)
            with self.subTest(section=section), self.assertRaisesRegex(ArchiveError, 'DELIVERY_CONTENT_MISMATCH'):
                verify_delivery(raw, digest(raw), bundle['snapshotSha256'])

    def test_reformatted_duplicate_keys_and_invalid_structure_reject(self):
        bundle = candidate(); raw = encode(bundle)
        for bad in (raw+b' ', b'{"kind":"fake",'+raw[1:], b'null', b'[]', b'{', b'"private"'):
            with self.subTest(bad=bad[:20]), self.assertRaises(ArchiveError):
                verify_delivery(bad, digest(bad), bundle['snapshotSha256'])

    def test_changed_source_and_quarantine_reject_even_with_self_hash(self):
        bundle = candidate(); bundle['packet']['source']['originalBase64'] = 'YWJj'
        raw = encode(bundle)
        with self.assertRaises(ArchiveError):
            verify_delivery(raw, digest(raw), bundle['snapshotSha256'])
        parts = fixture(); parts[2]['assets'][0]['archiveState'] = 'QUARANTINED'
        parts[4]['snapshotSha256'] = digest(encode(parts[2]))
        with self.assertRaisesRegex(ArchiveError, 'BINDING_ASSET_INELIGIBLE'):
            candidate(parts)

    def test_atomic_failure_leaves_no_accepted_file(self):
        with tempfile.TemporaryDirectory() as folder:
            bundle = candidate()
            with patch('tools.pixinsight.workflow_archive.archive.os.link', side_effect=OSError), \
                    self.assertRaisesRegex(ArchiveError, 'ATOMIC_COMMIT_UNAVAILABLE'):
                retain_delivery(bundle, folder, bundle['snapshotSha256'])
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_cleanup_failure_reports_committed_artifact(self):
        with tempfile.TemporaryDirectory() as folder:
            bundle = candidate()
            with patch('tools.pixinsight.workflow_archive.archive.Path.unlink', side_effect=OSError):
                receipt = retain_delivery(bundle, folder, bundle['snapshotSha256'])
            self.assertEqual(receipt['outcome'], 'CREATED_CLEANUP_PENDING')
            self.assertEqual(load_delivery(Path(folder)/receipt['filename'], receipt['sha256'],
                                          bundle['snapshotSha256']), bundle['result'])

    def test_directory_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            real = Path(folder)/'real'; real.mkdir(); alias=Path(folder)/'alias'
            try:
                alias.symlink_to(real, target_is_directory=True)
            except OSError:
                self.skipTest('Platform permission does not allow directory symlinks')
            bundle = candidate()
            with self.assertRaisesRegex(ArchiveError, 'REPARSE_PATH'):
                retain_delivery(bundle, alias, bundle['snapshotSha256'])

    def test_input_objects_detached(self):
        parts = fixture(); original = deepcopy(parts); bundle = candidate(parts)
        self.assertEqual(parts, original)
        parts[1]['declaredBy'] = 'CHANGED'
        self.assertNotEqual(bundle['declaration']['declaredBy'], 'CHANGED')


if __name__ == '__main__':
    unittest.main()
