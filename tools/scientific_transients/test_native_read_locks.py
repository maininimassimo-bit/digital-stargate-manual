"""Synthetic file bytes only. No PixInsight, subprocess or real image access."""
import hashlib
import os
from pathlib import Path
import tempfile
import unittest

from tools.scientific_transients.native_read_locks import NativeReadLocks


@unittest.skipUnless(os.name == 'nt', 'Windows sharing contract')
class NativeReadLocksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)/'synthetic.dat'
        self.raw = b'SYNTHETIC_OPAQUE_BYTES'*7000; self.path.write_bytes(self.raw)
        self.row = dict(path=self.path.as_posix(),sha256=hashlib.sha256(self.raw).hexdigest(),byteLength=len(self.raw))

    def acquire(self, records=None, guard=lambda:None):
        locks=NativeReadLocks([self.row] if records is None else records,guard=guard)
        self.addCleanup(locks.release); return locks

    def test_read_allowed_write_and_replace_denied_until_release(self):
        locks=self.acquire()
        self.assertEqual(self.path.read_bytes(),self.raw)
        with self.assertRaises(OSError): self.path.write_bytes(b'CHANGED')
        replacement=self.path.parent/'replacement.dat'; replacement.write_bytes(self.raw)
        with self.assertRaises(OSError): replacement.replace(self.path)
        locks.verify(); locks.release()
        replacement.replace(self.path)
        self.path.write_bytes(b'AFTER_RELEASE')
        with self.assertRaisesRegex(Exception,'READ_LOCK_RELEASED'): locks.verify()

    def test_wrong_hash_releases_acquired_handle_without_repairing_source(self):
        self.row['sha256']='0'*64
        with self.assertRaisesRegex(Exception,'READ_LOCK_HASH'): self.acquire()
        self.assertEqual(self.path.read_bytes(),self.raw)
        self.path.write_bytes(b'UNLOCKED_AFTER_FAILED_CONSTRUCTION')

    def test_existing_writer_blocks_acquisition(self):
        with self.path.open('r+b'):
            with self.assertRaises(OSError): self.acquire()

    def test_duplicate_path_rejects_and_releases_first(self):
        with self.assertRaisesRegex(Exception,'READ_LOCK_PATH'): self.acquire([self.row,self.row])
        self.path.write_bytes(b'UNLOCKED')

    def test_hardlink_is_rejected(self):
        alias=self.path.parent/'alias.dat'; os.link(self.path,alias)
        with self.assertRaisesRegex(Exception,'READ_LOCK_FILE_TYPE'): self.acquire()

    def test_wrong_size_and_bool_size_rejected(self):
        for size in [len(self.raw)-1,True]:
            with self.subTest(size=size):
                self.row['byteLength']=size
                with self.assertRaises(Exception): self.acquire()
                self.path.write_bytes(self.raw)

    def test_guard_failure_during_hash_releases_before_start(self):
        calls=[0]
        def guard():
            calls[0]+=1
            if calls[0]==3: raise RuntimeError('SYNTHETIC_BUDGET')
        with self.assertRaisesRegex(RuntimeError,'SYNTHETIC_BUDGET'): self.acquire(guard=guard)
        self.path.write_bytes(b'UNLOCKED')

    def test_empty_initializer_can_be_locked(self):
        self.path.write_bytes(b''); self.row.update(sha256=hashlib.sha256(b'').hexdigest(),byteLength=0)
        locks=self.acquire(); locks.verify()

    def test_separate_chunk_guard_preserves_original_read_locks(self):
        full=[]; progress=[]
        locks=NativeReadLocks([self.row],guard=lambda:full.append(True),
            progress_guard=lambda:progress.append(True)); self.addCleanup(locks.release)
        self.assertEqual(len(full),3)  # acquisition, verify-record, verify-end
        self.assertGreater(len(progress),len(full))
        with self.assertRaises(OSError): self.path.write_bytes(b'LOCK_STILL_HELD')
        before=len(full); locks.verify(); self.assertEqual(len(full)-before,2)

    def test_separate_chunk_failure_releases_only_failed_construction(self):
        def fail(): raise RuntimeError('SYNTHETIC_PROGRESS_DEADLINE')
        with self.assertRaisesRegex(RuntimeError,'PROGRESS_DEADLINE'):
            NativeReadLocks([self.row],guard=lambda:None,progress_guard=fail)
        self.path.write_bytes(b'NO_NATIVE_START_LOCK_RELEASED')

    def test_invalid_optional_callback_is_rejected_before_acquiring(self):
        with self.assertRaisesRegex(Exception,'PROGRESS_GUARD'):
            NativeReadLocks([self.row],guard=lambda:None,progress_guard=False)
        self.path.write_bytes(b'NOT_LOCKED')

    def test_reentrant_progress_cannot_return_a_false_verified_digest(self):
        locks=self.acquire(); entered=False
        def progress():
            nonlocal entered
            if not entered:
                entered=True; locks.verify()
        locks._progress_guard=progress
        with self.assertRaisesRegex(Exception,'READ_LOCK_SHORT_READ'): locks.verify()
        self.assertFalse(locks._released)
        with self.assertRaises(OSError): self.path.write_bytes(b'STILL_HELD_AFTER_VERIFY_FAILURE')


if __name__=='__main__': unittest.main()
