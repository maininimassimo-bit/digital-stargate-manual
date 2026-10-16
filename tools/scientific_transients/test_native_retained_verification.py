"""Opaque synthetic bundles and fake held/lock queries. No starts or image reads."""
import copy
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import encode
from tools.scientific_transients import native_publication as pub
from tools.scientific_transients import test_native_run_records as fixtures
from tools.scientific_transients import test_native_state_metadata as metadata_fixture
from tools.scientific_transients.native_read_locks import NativeReadLocks
from tools.scientific_transients.native_retained_verification import RetainedRunVerification
from tools.scientific_transients.native_supervision_signals import NativeSupervisionSignals


class RetainedVerificationTests(unittest.TestCase):
    def setUp(self):
        self.case=fixtures.NativeRunRecordsTests(); self.case.setUp(); self.addCleanup(self.case.doCleanups)
        c=self.case; f=c.fixture; self.f=f
        self.records=c.records(); self.signals=NativeSupervisionSignals(self.records)
        c.consume(self.records); self.signals.adopt_held(c.holder.held); self.records.write_owner(c.holder.held)
        r=self.records; pins={p.name:row for p,row,_ in r._pins if p.parent==f.work}
        m=metadata_fixture.NativeStateMetadataTests(); m.setUp()
        m.expected.update(operationRef=f.operation,parametersSha256=pins['parameters.json']['sha256'],
            sealSha256=f.binding['sealSha256'],sourceSha256=pins['source.fits']['sha256'],
            kernelSpecSha256=pins['kernel-spec.json']['sha256'],lineageSha256=pins['source-lineage.json']['sha256'],
            dependencies={key:f.fixed[role]['sha256'] for role,key in [('CORE','coreSha256'),('PARSER','parserSha256'),
                ('PRIMARY','primarySha256'),('WRAPPER','wrapperSha256')]},pixInsightVersion=f.control['expectedPixInsightVersion'],
            processSessionRef=f.control['processSessionRef'],ownerSha256=pins['native-owner.json']['sha256'],
            ownerReadySha256=pins['native-owner-ready.json']['sha256'])
        m.started.update(**{k:m.expected[k] for k in ['operationRef','parametersSha256','sealSha256','pixInsightVersion']})
        m.evidence.update(**{k:copy.deepcopy(v) for k,v in m.expected.items() if k!='sealSha256'})
        self.evidence=m.evidence
        for name in sorted(pub.REQUIRED):
            raw=encode(m.started) if name=='started-native.json' else (
                encode(m.evidence) if name=='native-evidence.json' else ('SYNTHETIC_OPAQUE_'+name).encode('ascii'))
            (f.work/name).write_bytes(raw)
        self.lock=object.__new__(NativeReadLocks); self.lock._released=False; self.lock._held=[]
        for path,row,_ in r._pins:
            if path.parent==f.work: self.add_lock(path,row)
        for role in ['ENTRY','LAUNCHER']:
            row=f.fixed[role]; self.add_lock(pub.safe_path(row['path']),row)
        # Deliberately fake file-lock queries. Real Windows sharing is tested in
        # test_native_read_locks, and real PJSR compatibility remains unproven.
        self.lock_patch=patch.object(NativeReadLocks,'verify',return_value=None)
        self.lock_patch.start(); self.addCleanup(self.lock_patch.stop)

    def add_lock(self,path,row):
        self.lock._held.append((object(),path,dict(path=path.as_posix(),sha256=row['sha256'],byteLength=row['byteLength']),()))

    def publish(self,names=pub.REQUIRED):
        f=self.f; f.terminal['products']=[]
        for name in sorted(names):
            raw=(f.work/name).read_bytes()
            f.terminal['products'].append(dict(role=name,name=name,sha256=fixtures.fixtures.sha(raw),byteLength=len(raw)))
        f.write_terminal()
        self.outcome=f.publish(clock=self.case.budget.publication_clock,deadline=self.case.budget.deadline_monotonic)
        return self.outcome

    def proof(self):
        return RetainedRunVerification(self.records,self.signals,self.outcome,[self.lock])

    def test_original_live_composition_has_no_close_start_or_science_authority(self):
        self.publish(); proof=self.proof(); value=proof.verify()
        self.assertTrue(value['retainedStateVerified'])
        self.assertEqual(value['nativeProcessId'],'4242')
        self.assertEqual(value['qualifiedControls'],0)
        for key in ['processClosureAuthorized','newNativeStartAllowed','measurementAccepted']:
            self.assertFalse(value[key])
        self.assertFalse(self.lock._released)

    def test_identical_start_replacement_is_not_original_record(self):
        self.publish(); proof=self.proof(); p=self.f.journal/'start-consumed.json'
        other=p.with_name('replacement.json'); other.write_bytes(p.read_bytes()); other.replace(p)
        with self.assertRaises(Exception): proof.verify()
        self.assertTrue(self.signals.diagnostic()['liveUncertain'])
        self.assertIs(self.records._held,self.case.holder.held)
        self.assertFalse(self.lock._released)

    def test_missing_lock_coverage_latches_uncertainty(self):
        self.publish(); self.lock._held.pop()
        with self.assertRaisesRegex(Exception,'RETAINED_LIVE_LOCK_COVERAGE'): self.proof()
        self.assertTrue(self.records._failed)

    def test_duplicate_lock_coverage_is_rejected(self):
        self.publish(); self.lock._held.append(self.lock._held[0])
        with self.assertRaisesRegex(Exception,'RETAINED_LIVE_DUPLICATE_LOCK'): self.proof()

    def test_released_lock_cannot_be_used(self):
        self.publish(); self.lock._released=True
        with self.assertRaisesRegex(Exception,'RETAINED_LIVE_RELEASED_LOCKS'): self.proof()

    def test_observed_uncertainty_without_file_blocks(self):
        self.publish(); self.signals._fail()
        self.assertFalse((self.f.journal/'supervision-uncertain.json').exists())
        with self.assertRaisesRegex(Exception,'RETAINED_LIVE_UNCERTAIN'): self.proof()

    def test_publication_marker_export_mutation_is_not_private_authority(self):
        self.publish(); self.outcome['marker']['products']=[]
        self.assertTrue(self.proof().verify()['retainedStateVerified'])

    def test_late_known_deadline_overrun_permits_read_only_proof(self):
        self.publish(); proof=self.proof(); self.case.mono=181
        value=proof.verify()
        self.assertTrue(value['parentMonotonicDeadlineExceeded'])
        self.assertFalse(value['processClosureAuthorized'])
        self.assertFalse(value['measurementAccepted'])

    def test_clock_reversal_is_sticky_even_if_clock_restored(self):
        self.publish(); proof=self.proof(); self.case.mono=0
        with self.assertRaises(Exception): proof.verify()
        self.case.mono=1
        with self.assertRaisesRegex(Exception,'RETAINED_LIVE_UNCERTAIN'): proof.verify()

    def test_comparison_assertion_false_blocks_even_coherent_byte_publication(self):
        self.evidence['checkpointReopenCompared']=False
        (self.f.work/'native-evidence.json').write_bytes(encode(self.evidence))
        self.publish()
        with self.assertRaisesRegex(Exception,'STATE_METADATA_NATIVE_COMPARISONS'): self.proof()

    def test_late_cancel_blocks_and_does_not_release_or_close(self):
        self.publish(); proof=self.proof()
        self.signals.request_cancel()
        with self.assertRaises(Exception): proof.verify()
        self.assertFalse(self.lock._released)
        self.assertTrue(self.signals.diagnostic()['liveUncertain'])

    def test_new_uncertainty_fence_cannot_be_erased_to_rearm(self):
        self.publish(); proof=self.proof(); p=self.f.work/'native-publication-uncertain.json'
        p.write_bytes(b'SYNTHETIC_PARTIAL')
        with self.assertRaises(Exception): proof.verify()
        p.unlink()  # Test-only removal cannot rehabilitate the original live object.
        with self.assertRaisesRegex(Exception,'RETAINED_LIVE_UNCERTAIN'): proof.verify()

    def test_reconstruction_from_same_live_objects_is_blocked(self):
        self.publish(); self.proof()
        with self.assertRaisesRegex(Exception,'RETAINED_LIVE_RECONSTRUCTION'): self.proof()

    def test_held_identity_change_is_not_a_matching_owner(self):
        self.publish(); proof=self.proof(); self.case.holder.failure=True
        with self.assertRaises(Exception): proof.verify()
        self.assertTrue(proof.diagnostic()['verificationFailed'])
        self.assertIs(self.records._held,self.case.holder.held)

    def test_failed_before_image_is_retention_only(self):
        names={'started-native.json','native.log'}
        for name in pub.REQUIRED-names: (self.f.work/name).unlink()
        self.f.terminal.update(state='FAILED_RETAINED',errorCode='SYNTHETIC_FAILURE')
        self.publish(names); value=self.proof().verify()
        self.assertEqual(value['retentionBranch'],'FAILED_BEFORE_IMAGE')
        self.assertFalse(value['conditionalComputationDeclaredComplete'])
        self.assertFalse(value['processClosureAuthorized'])

    def test_cancel_already_pinned_at_publication_is_reported_without_acceptance(self):
        self.signals.request_cancel(); self.publish(); value=self.proof().verify()
        self.assertTrue(value['parentCancelRequested'])
        self.assertFalse(value['measurementAccepted'])


if __name__=='__main__': unittest.main()
