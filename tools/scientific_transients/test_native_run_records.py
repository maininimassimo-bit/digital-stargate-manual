"""Synthetic opaque work bundle, fake bootstrap and fake held queries; no starts."""
import datetime as dt
import json
import unittest
from unittest.mock import patch

from tools.scientific_transients import native_publication as pub
from tools.scientific_transients import test_native_publication as fixtures
from tools.scientific_transients import test_native_held_process as held_fixtures
from tools.scientific_transients.native_run_budget import LiveNativeBudget
from tools.scientific_transients.native_run_records import NativeRunRecords


class NativeRunRecordsTests(unittest.TestCase):
    def setUp(self):
        self.fixture=fixtures.NativePublicationTests(); self.fixture.setUp(); self.addCleanup(self.fixture.doCleanups)
        f=self.fixture
        # Remove only the synthetic runtime products created by this test fixture.
        for path in f.work.iterdir():
            if path.name in pub.ALLOWED: path.unlink()
        self.mono=1
        self.budget=LiveNativeBudget(monotonic=lambda:self.mono,
            wall=lambda:dt.datetime(2026,10,16,10,0,0,tzinfo=dt.timezone.utc))
        self.holder=held_fixtures.HeldNativeProcessTests(); self.holder.setUp(); self.addCleanup(self.holder.doCleanups)
        self.holder.held.capture()

    def records(self):
        f=self.fixture
        return NativeRunRecords(f.work,f.archive,f.journal,f.binding,bootstrap_session=f.session,budget=self.budget)

    def consume(self,records): return records.consume('2026-10-16T10:00:01Z')

    def test_consumed_and_owner_records_bind_same_held_identity_and_raw_copies(self):
        records=self.records(); consumed=self.consume(records)
        outcome=records.write_owner(self.holder.held); records.verify()
        f=self.fixture
        start=json.loads((f.journal/'start-consumed.json').read_bytes())
        held=json.loads((f.journal/'held-process.json').read_bytes())
        owner=json.loads((f.work/'native-owner.json').read_bytes())
        ready=json.loads((f.work/'native-owner-ready.json').read_bytes())
        self.assertEqual(start['permission'],'ONE_ATTEMPT_NO_REPLAY')
        self.assertEqual(held['startConsumedSha256'],consumed['startConsumedSha256'])
        self.assertEqual(owner['nativeProcessId'],'4242')
        self.assertEqual(ready['ownerSha256'],outcome['ownerSha256'])
        for name in ['native-owner.json','native-owner-ready.json']:
            self.assertEqual((f.work/name).read_bytes(),(f.journal/name).read_bytes())
        self.assertFalse(outcome['processClosureAuthorized'])
        self.assertFalse(records.diagnostic()['newNativeStartAllowed'])

    def test_consumption_is_monouse_and_existing_record_blocks_reconstruction(self):
        records=self.records(); self.consume(records)
        before=(self.fixture.journal/'start-consumed.json').read_bytes()
        with self.assertRaisesRegex(Exception,'RUN_RECORDS_START_REPLAY'): self.consume(records)
        with self.assertRaisesRegex(Exception,'RUN_RECORDS_PRIOR_ATTEMPT'): self.records()
        self.assertEqual((self.fixture.journal/'start-consumed.json').read_bytes(),before)

    def test_missing_consumption_cannot_commit_owner(self):
        records=self.records()
        with self.assertRaisesRegex(Exception,'RUN_RECORDS_HELD_REQUIRED'): records.write_owner(self.holder.held)
        self.assertTrue(records.diagnostic()['failed'])
        self.assertFalse((self.fixture.work/'native-owner.json').exists())

    def test_owner_replay_is_blocked(self):
        records=self.records(); self.consume(records); records.write_owner(self.holder.held)
        with self.assertRaisesRegex(Exception,'RUN_RECORDS_OWNER_REPLAY'): records.write_owner(self.holder.held)

    def test_input_change_before_consumption_preserves_failed_memory_without_start(self):
        records=self.records(); (self.fixture.work/'source.fits').write_bytes(b'CHANGED_SYNTHETIC')
        with self.assertRaises(Exception): self.consume(records)
        self.assertTrue(records.diagnostic()['failed'])
        self.assertFalse((self.fixture.journal/'start-consumed.json').exists())
        with self.assertRaisesRegex(Exception,'RUN_RECORDS_START_REPLAY'): self.consume(records)

    def test_unknown_work_entry_before_consumption_blocks(self):
        records=self.records(); (self.fixture.work/'unknown.dat').write_bytes(b'SYNTHETIC')
        with self.assertRaisesRegex(Exception,'RUN_RECORDS_PRESTART_INVENTORY'): self.consume(records)

    def test_failed_identity_cannot_write_owner(self):
        records=self.records(); self.consume(records); self.holder.failure=True
        with self.assertRaises(Exception): records.write_owner(self.holder.held)
        self.assertFalse((self.fixture.work/'native-owner.json').exists())
        self.assertIs(records._held,self.holder.held)

    def test_parent_ready_failure_preserves_owner_but_does_not_commit_native_ready(self):
        records=self.records(); self.consume(records); original=pub._write_control
        def fail(path,value):
            if path==self.fixture.journal/'native-owner-ready.json': raise OSError('SYNTHETIC_METADATA_IO')
            return original(path,value)
        with patch.object(pub,'_write_control',side_effect=fail):
            with self.assertRaises(OSError): records.write_owner(self.holder.held)
        self.assertTrue((self.fixture.work/'native-owner.json').exists())
        self.assertFalse((self.fixture.work/'native-owner-ready.json').exists())
        self.assertTrue(records.diagnostic()['failed'])
        with self.assertRaisesRegex(Exception,'RUN_RECORDS_OWNER_REPLAY'): records.write_owner(self.holder.held)

    def test_overrun_after_native_commit_retains_ready_and_uncertainty_in_memory(self):
        records=self.records(); self.consume(records); original=pub._write_control
        def cross(path,value):
            result=original(path,value)
            if path==self.fixture.work/'native-owner-ready.json': self.mono=181
            return result
        with patch.object(pub,'_write_control',side_effect=cross):
            with self.assertRaisesRegex(Exception,'NATIVE_BUDGET_EXPIRED'): records.write_owner(self.holder.held)
        self.assertTrue((self.fixture.work/'native-owner-ready.json').exists())
        self.assertTrue(records.diagnostic()['failed'])
        self.assertFalse(records.diagnostic()['ownerCommitted'])

    def test_source_attestation_change_blocks_consumption(self):
        records=self.records()
        name=next(iter(self.fixture.control_case.sources))
        self.fixture.control_case.sources[name]['sha256']='0'*64
        with self.assertRaises(Exception): self.consume(records)
        self.assertFalse((self.fixture.journal/'start-consumed.json').exists())

    def test_cancel_arrives_during_owner_copy_blocks_native_ready(self):
        records=self.records(); self.consume(records); original=pub._write_control
        def cancel(path,value):
            result=original(path,value)
            if path==self.fixture.work/'native-owner.json': (self.fixture.work/'cancel.json').write_bytes(b'SYNTHETIC_CANCEL')
            return result
        with patch.object(pub,'_write_control',side_effect=cancel):
            with self.assertRaisesRegex(Exception,'RUN_RECORDS_UNCERTAINTY_OR_CANCEL'): records.write_owner(self.holder.held)
        self.assertFalse((self.fixture.work/'native-owner-ready.json').exists())

    def test_caller_cannot_replace_original_deadline(self):
        self.budget=LiveNativeBudget(monotonic=lambda:1,
            wall=lambda:dt.datetime(2026,10,16,11,0,0,tzinfo=dt.timezone.utc))
        with self.assertRaisesRegex(Exception,'RUN_RECORDS_ORIGINAL_DEADLINE'): self.records()

    def test_consumption_at_deadline_is_not_a_fresh_timestamp(self):
        records=self.records()
        with self.assertRaisesRegex(Exception,'RUN_RECORDS_TIME_ORDER'): records.consume('2026-10-16T10:03:00Z')
        self.assertFalse((self.fixture.journal/'start-consumed.json').exists())

    def test_consumption_before_parent_intent_is_rejected(self):
        records=self.records()
        with self.assertRaisesRegex(Exception,'RUN_RECORDS_TIME_ORDER'): records.consume('2026-10-16T09:59:59Z')

    def test_identical_start_record_replacement_does_not_reestablish_identity(self):
        records=self.records(); self.consume(records)
        path=self.fixture.journal/'start-consumed.json'; replacement=path.with_name('replacement.json')
        replacement.write_bytes(path.read_bytes()); replacement.replace(path)
        with self.assertRaises(Exception): records.write_owner(self.holder.held)
        self.assertFalse((self.fixture.work/'native-owner.json').exists())

    def test_runtime_names_after_ready_are_not_computation_acceptance(self):
        records=self.records(); self.consume(records); records.write_owner(self.holder.held)
        (self.fixture.work/'started-native.json').write_bytes(b'SYNTHETIC_PARTIAL_RUNTIME')
        records.verify()
        self.assertFalse(records.diagnostic()['processClosureAuthorized'])


if __name__=='__main__': unittest.main()
