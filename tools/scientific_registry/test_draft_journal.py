"""Synthetic draft retention boundaries; no real scientific data."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.pixinsight.workflow_archive.archive import ArchiveError, digest, encode
from .draft_journal import (build_draft, verify_draft, retain_draft, load_chain,
                            filename, MAX_SOURCE_BYTES)


def draft(revision=1, previous=None, source=b'{"missing":["validFromUtc"],"value":null}'):
    return build_draft(source, digest(source), submission_id='REG-SYNTHETIC', revision=revision,
                       previous_digest=previous, recorded_at='2026-10-01T10:00:00Z')


class DraftJournalTests(unittest.TestCase):
    def test_preserves_original_bytes_without_promoting_embedded_claims(self):
        source = b'{ "state": "ACCEPTED", "scientificAuthority": "AP-014" }\n'
        row = draft(source=source)
        import base64
        self.assertEqual(base64.b64decode(row['source']['originalBase64']), source)
        self.assertEqual(row['state'], 'DRAFT_NOT_ACCEPTED')
        self.assertEqual(row['scientificAuthority'], 'NONE')
        self.assertFalse(row['catalogWritePerformed'])

    def test_chain_retry_and_separate_trust_anchor(self):
        with tempfile.TemporaryDirectory() as root:
            first = retain_draft(draft(), root, expected_head=None)
            second_draft = draft(2, first['sha256'], b'{"revisionEvidence":"new"}')
            second = retain_draft(second_draft, root, expected_head=first['sha256'])
            self.assertEqual(retain_draft(second_draft, root, expected_head=second['sha256'])['outcome'],
                             'DUPLICATE_NOOP')
            chain = load_chain(root, 'REG-SYNTHETIC', expected_head=second['sha256'])
            self.assertEqual(len(chain), 2)
            self.assertEqual(chain[0], draft())
            with self.assertRaisesRegex(ArchiveError, 'REGISTRY_STALE_HEAD'):
                load_chain(root, 'REG-SYNTHETIC', expected_head=first['sha256'])

    def test_source_integrity_and_json_boundaries(self):
        for source in (b'[]', b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":1e999}', b'\xff',
                       b'{"x":' + b'[' * 1500 + b'0' + b']' * 1500 + b'}'):
            with self.subTest(source=source[:30]), self.assertRaises(ArchiveError):
                draft(source=source)
        with self.assertRaisesRegex(ArchiveError, 'REGISTRY_SOURCE_SIZE'):
            draft(source=b' ' * (MAX_SOURCE_BYTES+1))
        with self.assertRaisesRegex(ArchiveError, 'REGISTRY_SOURCE_INTEGRITY'):
            build_draft(b'{}', '0'*64, submission_id='REG-SYNTHETIC', revision=1,
                        previous_digest=None, recorded_at='2026-10-01T10:00:00Z')

    def test_invalid_revision_id_time_or_predecessor(self):
        base = dict(submission_id='REG-SYNTHETIC', revision=1, previous_digest=None,
                    recorded_at='2026-10-01T10:00:00Z')
        for key, value in [('submission_id','../escape'),('submission_id','REG-X\n'),
                           ('revision',True),('revision',0),('revision',129),
                           ('previous_digest','0'*64),('recorded_at','2026-02-31T00:00:00Z')]:
            args={**base,key:value}
            with self.subTest(key=key,value=value), self.assertRaises(ArchiveError):
                build_draft(b'{}', digest(b'{}'), **args)

    def test_forged_accepted_envelope_and_duplicate_keys_reject(self):
        for key, value in [('state','ACCEPTED'),('scientificAuthority','AP-014'),
                           ('catalogWritePerformed',True),('unexpected',True)]:
            row=deepcopy(draft()); row[key]=value; raw=encode(row)
            with self.assertRaises(ArchiveError): verify_draft(raw,digest(raw))
        raw=encode(draft()).replace(b'"revision":1', b'"revision":1,"revision":1')
        with self.assertRaises(ArchiveError): verify_draft(raw,digest(raw))

    def test_corruption_missing_revision_and_rollback_reject(self):
        for mutation in ('corrupt','missing','rollback'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as root:
                first=retain_draft(draft(),root,expected_head=None)
                second=retain_draft(draft(2,first['sha256']),root,expected_head=first['sha256'])
                path=Path(root)/first['filename']
                if mutation=='corrupt': path.write_bytes(b'{}')
                elif mutation=='missing': path.unlink()
                else: (Path(root)/second['filename']).unlink()
                with self.assertRaises(ArchiveError):
                    load_chain(root,'REG-SYNTHETIC',expected_head=second['sha256'])

    def test_conflicting_writer_and_old_expected_head(self):
        with tempfile.TemporaryDirectory() as root:
            first=retain_draft(draft(),root,expected_head=None)
            retain_draft(draft(2,first['sha256']),root,expected_head=first['sha256'])
            with self.assertRaises(ArchiveError):
                retain_draft(draft(2,first['sha256'],b'{"other":true}'),root,expected_head=first['sha256'])

    def test_atomic_failure_keeps_previous_chain(self):
        with tempfile.TemporaryDirectory() as root:
            first=retain_draft(draft(),root,expected_head=None)
            with patch('tools.pixinsight.workflow_archive.archive.os.link',side_effect=OSError('synthetic')):
                with self.assertRaises(ArchiveError):
                    retain_draft(draft(2,first['sha256']),root,expected_head=first['sha256'])
            self.assertEqual(len(load_chain(root,'REG-SYNTHETIC',expected_head=first['sha256'])),1)
            self.assertEqual(len(list(Path(root).iterdir())),1)

    def test_simultaneous_conflicting_append_has_one_winner(self):
        from concurrent.futures import ThreadPoolExecutor
        from threading import Barrier
        from . import draft_journal
        barrier = Barrier(2)
        original = draft_journal.write_immutable
        def commit(raw, path):
            barrier.wait(timeout=10)
            return original(raw, path)
        with tempfile.TemporaryDirectory() as root:
            def writer(source):
                try:
                    return retain_draft(draft(source=source), root, expected_head=None)
                except ArchiveError:
                    return None
            with patch.object(draft_journal, 'write_immutable', side_effect=commit):
                with ThreadPoolExecutor(max_workers=2) as pool:
                    results = list(pool.map(writer, [b'{"writer":1}', b'{"writer":2}']))
            winners = [value for value in results if value is not None]
            self.assertEqual(len(winners), 1)
            self.assertEqual(len(load_chain(root, 'REG-SYNTHETIC',
                                           expected_head=winners[0]['sha256'])), 1)

    def test_backup_restore_preserves_chain_and_external_anchor(self):
        import shutil
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as restored:
            first=retain_draft(draft(),root,expected_head=None)
            second=retain_draft(draft(2,first['sha256']),root,expected_head=first['sha256'])
            for path in Path(root).iterdir(): shutil.copyfile(path,Path(restored)/path.name)
            self.assertEqual(load_chain(root,'REG-SYNTHETIC',expected_head=second['sha256']),
                             load_chain(restored,'REG-SYNTHETIC',expected_head=second['sha256']))

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            first=retain_draft(draft(),root,expected_head=None)
            path=Path(root)/first['filename']; retained=path.read_bytes(); path.unlink()
            real=Path(root)/'real'; real.write_bytes(retained)
            try: path.symlink_to(real)
            except OSError: self.skipTest('local symlink privilege unavailable')
            with self.assertRaises(ArchiveError):
                load_chain(root,'REG-SYNTHETIC',expected_head=first['sha256'])

    def test_time_order_and_unknown_matching_file_reject(self):
        with tempfile.TemporaryDirectory() as root:
            first=retain_draft(draft(),root,expected_head=None)
            row=draft(2,first['sha256']); row['recordedAt']='2026-09-30T10:00:00Z'
            with self.assertRaisesRegex(ArchiveError,'REGISTRY_TIME_ORDER'):
                retain_draft(row,root,expected_head=first['sha256'])
            (Path(root)/(digest(b'REG-SYNTHETIC')+'.extra')).write_bytes(b'{}')
            with self.assertRaisesRegex(ArchiveError,'REGISTRY_CHAIN_GAP'):
                load_chain(root,'REG-SYNTHETIC',expected_head=first['sha256'])


if __name__ == '__main__': unittest.main()
