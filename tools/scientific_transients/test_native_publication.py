"""Synthetic opaque product sets. No PixInsight process or real image decoding."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import encode, ProtocolError
from tools.scientific_transients import native_publication as pub
from tools.scientific_transients import test_native_launch_control as control_fixture


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
        self.control_case=control_fixture.LaunchControlTests()
        self.control_case.setUp();self.addCleanup(self.control_case.doCleanups)
        self.control=self.control_case.value
        self.fixed={r['role']:r for r in self.control['files'] if r['role']!='PARENT_SOURCE'}
        for role,name in [('CORE','native_linear_uncertainty.jsh'),('PARSER','strict_passive_json.jsh'),
            ('PRIMARY','native_float32_primary.jsh'),('WRAPPER','native_linear_measurement.jsh')]:
            row=self.fixed[role];path=self.work/name;path.write_bytes(Path(row['path']).read_bytes())
            row.update(path=path.as_posix(),name=name)
        for name,raw in [('source.fits',b'SYNTHETIC_OPAQUE_INPUT'),('kernel-spec.json',b'{}'),('source-lineage.json',b'{}')]:
            (self.work/name).write_bytes(raw)
        p=dict(protocol='DSG_NATIVE_LINEAR_MEASUREMENT_V2',operationRef=self.operation,ownerNonce=self.control['ownerNonce'],
            processSessionRef=self.control['processSessionRef'],expectedPixInsightVersion=self.control['expectedPixInsightVersion'],
            dependencies={key:self.fixed[role]['sha256'] for role,key in [('CORE','coreSha256'),('PARSER','parserSha256'),
                ('PRIMARY','primarySha256'),('WRAPPER','wrapperSha256')]})
        (self.work/'parameters.json').write_bytes(encode(p))
        self.seal=dict(protocol='DSG_NATIVE_LINEAR_LAUNCH_SEAL_V1',operationRef=self.operation,createdUTC='2026-10-16T10:00:00Z',
            arbSha256=self.control['arbSha256'],rqSha256=self.control['rqSha256'],inputClosureAccepted=False,
            files=[dict(role=path.name,name=path.name,sha256=sha(path.read_bytes()),byteLength=path.stat().st_size) for path in self.work.iterdir()])
        (self.work/'launch-seal.json').write_bytes(encode(self.seal))
        (self.work/'launch-grant.json').write_bytes(encode(dict(protocol='DSG_NATIVE_LINEAR_SINGLE_START_GRANT_V1',
            operationRef=self.operation,sealSha256=sha(encode(self.seal)))))
        for name,label in [('_dsg_verified_bootstrap','bootstrap-source.py'),('_dsg_pinned_source_loader','loader-source.py')]:
            path=self.control_case.root/label;raw=('SYNTHETIC_'+label).encode('ascii');path.write_bytes(raw)
            row=dict(path=path.as_posix(),sha256=sha(raw),byteLength=len(raw))
            self.control_case.sources[name]=row
            self.control['files'].append(dict(role='PARENT_SOURCE',name=name,**row))
        sm=self.control_case.root/'source-manifest.json';sm.write_bytes(b'{}')
        boot=dict(protocol='DSG_NATIVE_BOOTSTRAP_MANIFEST_V1',
            bootstrapSha256=self.control_case.sources['_dsg_verified_bootstrap']['sha256'],
            entrySha256=self.control['bootstrapEntrySha256'],pythonVersion=self.control['expectedPythonVersion'],
            pythonExecutable=self.fixed['PYTHON_EXECUTABLE']['path'],pythonExecutableSha256=self.fixed['PYTHON_EXECUTABLE']['sha256'],
            loaderPath=self.control_case.sources['_dsg_pinned_source_loader']['path'],
            loaderSha256=self.control_case.sources['_dsg_pinned_source_loader']['sha256'],sourcesManifestPath=sm.as_posix(),
            sourcesManifestSha256=sha(b'{}'),entryModule='tools.synthetic',entryCallable='main')
        raw=encode(boot);Path(self.fixed['BOOTSTRAP_MANIFEST']['path']).write_bytes(raw)
        self.fixed['BOOTSTRAP_MANIFEST'].update(sha256=sha(raw),byteLength=len(raw));self.control['bootstrapManifestSha256']=sha(raw)
        self.control.update(sealSha256=sha((self.work/'launch-seal.json').read_bytes()),grantSha256=sha((self.work/'launch-grant.json').read_bytes()))
        self.bootstrap=dict(bootstrapManifestSha256=self.control['bootstrapManifestSha256'],bootstrapEntrySha256=boot['entrySha256'],
            bootstrapSourceSha256=boot['bootstrapSha256'],loaderSha256=boot['loaderSha256'],sourcesManifestSha256=boot['sourcesManifestSha256'],
            expectedPythonVersion=boot['pythonVersion'],pythonExecutable=boot['pythonExecutable'],pythonExecutableSha256=boot['pythonExecutableSha256'])
        case=self
        class SyntheticSession:
            # This is deliberately a fake live callback, never native ownership/consent.
            def attest_sources(self):return copy.deepcopy(case.control_case.sources)
            def attest_bootstrap(self):return copy.deepcopy(case.bootstrap)
            def assert_intact(self):return True
        self.session=SyntheticSession()
        raw=encode(self.control);(self.journal/'launch-control.json').write_bytes(raw)
        self.intent = {"protocol": "DSG_NATIVE_LINEAR_PARENT_INTENT_V2", "operationRef": self.operation,
                       "createdUTC": "2026-10-16T10:00:00Z", "sealSha256": self.control['sealSha256'],
                       "grantSha256":self.control['grantSha256'],'launchControlSha256':sha(raw)}
        for prefix, path in zip(["nativeWork", "retained", "supervision"], [self.work, self.archive, self.journal]):
            info = path.stat()
            self.intent[prefix + "CanonicalPath"] = path.as_posix()
            self.intent[prefix + "DirectoryIdentity"] = [info.st_dev, info.st_ino]
        self.binding = {"operationRef": self.operation, "parentIntentSha256": "0" * 64,
                        "sealSha256": self.control['sealSha256'], "grantSha256":self.control['grantSha256'],
                        'launchControlSha256':self.intent['launchControlSha256']}
        self.write_intent()
        self.write_owner()
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
        returned=dict(protocol='DSG_NATIVE_LINEAR_RETURNED_V1',operationRef=self.operation,sealSha256=self.control['sealSha256'],
            wrapperSha256=self.fixed['WRAPPER']['sha256'],terminalSha256=sha(raw),readySha256=sha((self.work/'terminal-ready.json').read_bytes()),
            state=self.terminal['state'],unclosedOwnedViews=self.terminal['unclosedOwnedViews'],fullPhysicalVariance=None,
            significance=None,scientificValidation='NOT_VALIDATED',qualifiedControls=0,nativeProcessId='4242',
            processSessionRef=self.control['processSessionRef'],ownerSha256=sha((self.work/'native-owner.json').read_bytes()),
            ownerReadySha256=sha((self.work/'native-owner-ready.json').read_bytes()))
        (self.work/'native-return.json').write_bytes(encode(returned))

    def write_owner(self):
        owner=dict(protocol='DSG_NATIVE_LINEAR_OWNER_V1',operationRef=self.operation,processSessionRef=self.control['processSessionRef'],
            ownerNonce=self.control['ownerNonce'],sealSha256=self.control['sealSha256'],grantSha256=self.control['grantSha256'],
            launchControlSha256=self.binding['launchControlSha256'],parentIntentSha256=self.binding['parentIntentSha256'],
            nativeProcessId='4242',processCreationFileTime='0123456789abcdef',parentDeadlineUTC=self.control['parentDeadlineUTC'])
        raw=encode(owner);(self.work/'native-owner.json').write_bytes(raw)
        (self.work/'native-owner-ready.json').write_bytes(encode(dict(protocol='DSG_NATIVE_LINEAR_OWNER_READY_V1',
            operationRef=self.operation,processSessionRef=owner['processSessionRef'],ownerNonce=owner['ownerNonce'],ownerSha256=sha(raw))))

    def publish(self, clock=lambda: 1, deadline=180):
        return pub.publish_native_bundle(self.work, self.archive, self.journal,
                                         self.binding, clock=clock, deadline=deadline,bootstrap_session=self.session)

    def assert_uncertain(self):
        self.assertTrue((self.journal / "publication-uncertain.json").exists())
        self.assertFalse((self.archive / "retained-native-terminal.json").exists())

    def test_missing_causal_return_blocks_before_copy(self):
        (self.work/'native-return.json').unlink()
        with self.assertRaises(pub.PublicationFailure): self.publish()
        self.assert_uncertain()
        self.assertEqual(list(self.archive.iterdir()), [])

    def test_owner_identity_disagrees_with_return(self):
        path=self.work/'native-return.json'
        import json
        value=json.loads(path.read_bytes()); value['nativeProcessId']='4243'
        path.write_bytes(encode(value))
        with self.assertRaises(pub.PublicationFailure): self.publish()
        self.assert_uncertain()

    def test_live_bootstrap_binding_disagreement_blocks(self):
        self.bootstrap['bootstrapEntrySha256']='0'*64
        with self.assertRaises(pub.PublicationFailure): self.publish()
        self.assert_uncertain()

    def test_v1_parent_intent_is_not_accepted(self):
        self.intent['protocol']='DSG_NATIVE_LINEAR_PARENT_INTENT_V1'
        self.write_intent(); self.write_owner(); self.write_terminal()
        with self.assertRaises(pub.PublicationFailure): self.publish()
        self.assert_uncertain()

    def test_unlisted_work_file_blocks(self):
        (self.work/'unexpected.txt').write_bytes(b'UNLISTED')
        with self.assertRaises(pub.PublicationFailure): self.publish()
        self.assert_uncertain()

    def test_sealed_input_changed_blocks(self):
        (self.work/'source.fits').write_bytes(b'CHANGED_SYNTHETIC_INPUT')
        with self.assertRaises(pub.PublicationFailure): self.publish()
        self.assert_uncertain()

    def test_valid_initial_cancel_can_be_retained_without_authority(self):
        (self.work/'cancel.json').write_bytes(encode(dict(
            protocol='DSG_NATIVE_LINEAR_CANCEL_V1',operationRef=self.operation,requested=True)))
        outcome=self.publish()
        self.assertFalse(outcome['processClosureAuthorized'])
        self.assertFalse(outcome['newNativeStartAllowed'])

    def test_cancel_arriving_during_last_marker_readback_blocks_return(self):
        original=pub._hash_bounded
        def late_cancel(path, size, info):
            result=original(path,size,info)
            if Path(path).name=='retained-native-terminal.json':
                (self.work/'cancel.json').write_bytes(encode(dict(
                    protocol='DSG_NATIVE_LINEAR_CANCEL_V1',operationRef=self.operation,requested=True)))
            return result
        with patch.object(pub,'_hash_bounded',side_effect=late_cancel):
            with self.assertRaisesRegex(pub.PublicationFailure,'PUBLICATION_CANCEL_CHANGED'): self.publish()
        self.assertTrue((self.archive/'retained-native-terminal.json').exists())
        self.assertTrue((self.journal/'publication-uncertain.json').exists())

    def test_existing_cancel_changed_during_last_marker_readback_blocks_return(self):
        path=self.work/'cancel.json'
        path.write_bytes(encode(dict(protocol='DSG_NATIVE_LINEAR_CANCEL_V1',operationRef=self.operation,requested=True)))
        original=pub._hash_bounded
        def late_change(target,size,info):
            result=original(target,size,info)
            if Path(target).name=='retained-native-terminal.json': path.write_bytes(b'CHANGED_CANCEL')
            return result
        with patch.object(pub,'_hash_bounded',side_effect=late_change):
            with self.assertRaises(pub.PublicationFailure): self.publish()
        self.assertTrue((self.archive/'retained-native-terminal.json').exists())
        self.assertTrue((self.journal/'publication-uncertain.json').exists())

    def test_deadline_crossed_in_final_cancel_readback_is_uncertain(self):
        (self.work/'cancel.json').write_bytes(encode(dict(
            protocol='DSG_NATIVE_LINEAR_CANCEL_V1',operationRef=self.operation,requested=True)))
        original=pub._hash_bounded; now=[179]; marker_read=[False]
        def cross(target,size,info):
            result=original(target,size,info)
            if Path(target).name=='retained-native-terminal.json': marker_read[0]=True
            if marker_read[0] and Path(target).name=='cancel.json': now[0]=181
            return result
        with patch.object(pub,'_hash_bounded',side_effect=cross):
            with self.assertRaisesRegex(pub.PublicationFailure,'PUBLICATION_DEADLINE_CROSSED_DURING_MARKER'):
                self.publish(clock=lambda:now[0])
        self.assertTrue((self.journal/'publication-uncertain.json').exists())

    def test_complete_set_raw_chain_and_no_lifecycle_or_science_authority(self):
        outcome = self.publish()
        marker = outcome["marker"]
        self.assertEqual(len(marker["products"]), 17)
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

    def test_live_verification_is_private_and_json_marker_is_only_metadata(self):
        import json
        outcome=self.publish(); live=outcome['liveVerification']
        result=live.verify()
        self.assertTrue(result['verifiedAfterReturn'])
        self.assertFalse(result['processClosureAuthorized'])
        self.assertFalse(result['measurementAccepted'])
        self.assertEqual(result['markerSha256'],outcome['markerSha256'])
        json.dumps(outcome['marker'])
        with self.assertRaises(TypeError): json.dumps(outcome)
        with self.assertRaisesRegex(Exception,'PUBLICATION_LIVE_FACTORY_REQUIRED'):
            pub.LivePublicationVerification(None,lambda:False,outcome['markerSha256'],False)

    def test_exported_marker_mutation_cannot_change_private_expected_records(self):
        outcome=self.publish(); live=outcome['liveVerification']
        row=next(r for r in outcome['marker']['products'] if r['name']=='result.json')
        changed=b'X'*row['byteLength']; row['sha256']=sha(changed)
        outcome['marker']['nativeState']='UNCERTAIN_RETENTION'
        live.verify()  # Exported metadata is an independent copy.
        (self.work/'result.json').write_bytes(changed)
        (self.archive/'result.json').write_bytes(changed)
        with self.assertRaises(Exception): live.verify()
        self.assertTrue(live.diagnostic()['verificationFailed'])

    def test_live_verification_rejects_identical_source_replacement(self):
        live=self.publish()['liveVerification']; path=self.work/'result.json'
        replacement=self.work/'replacement.dat'; replacement.write_bytes(path.read_bytes()); replacement.replace(path)
        with self.assertRaises(Exception): live.verify()
        with self.assertRaisesRegex(Exception,'PUBLICATION_LIVE_UNCERTAIN'): live.verify()

    def test_live_verification_rejects_identical_retained_marker_replacement(self):
        live=self.publish()['liveVerification']; path=self.archive/'retained-native-terminal.json'
        replacement=self.archive/'replacement.dat'; replacement.write_bytes(path.read_bytes()); replacement.replace(path)
        with self.assertRaises(Exception): live.verify()

    def test_live_verification_rejects_identical_parent_source_replacement(self):
        live=self.publish()['liveVerification']
        row=next(iter(self.control_case.sources.values())); path=Path(row['path'])
        replacement=path.with_name('replacement-source.py'); replacement.write_bytes(path.read_bytes()); replacement.replace(path)
        with self.assertRaises(Exception): live.verify()

    def test_live_verification_fence_failure_stays_sticky_after_file_removed(self):
        live=self.publish()['liveVerification']; fence=self.work/'native-publication-uncertain.json'
        fence.write_bytes(b'SYNTHETIC_PARTIAL_FENCE')
        with self.assertRaises(Exception): live.verify()
        fence.unlink()  # Synthetic test only: restoring absence must not reset live uncertainty.
        with self.assertRaisesRegex(Exception,'PUBLICATION_LIVE_UNCERTAIN'): live.verify()

    def test_live_verification_rejects_new_cancellation(self):
        live=self.publish()['liveVerification']
        (self.work/'cancel.json').write_bytes(encode(dict(protocol='DSG_NATIVE_LINEAR_CANCEL_V1',
            operationRef=self.operation,requested=True)))
        with self.assertRaises(Exception): live.verify()

    def test_live_verification_rejects_parent_supervision_uncertainty(self):
        live=self.publish()['liveVerification']
        (self.journal/'supervision-uncertain.json').write_bytes(b'SYNTHETIC_PARTIAL')
        with self.assertRaisesRegex(Exception,'PUBLICATION_SUPERVISION_UNCERTAINTY'): live.verify()
        self.assertTrue(live.diagnostic()['verificationFailed'])

    def test_prior_supervision_uncertainty_blocks_before_publication_reservation(self):
        path=self.journal/'supervision-uncertain.json'; path.write_bytes(b'SYNTHETIC_PARTIAL')
        with self.assertRaisesRegex(pub.PublicationFailure,'PUBLICATION_SUPERVISION_UNCERTAINTY'): self.publish()
        self.assertFalse((self.journal/'publication-intent.json').exists())
        self.assertEqual(path.read_bytes(),b'SYNTHETIC_PARTIAL')

    def test_live_verification_later_overrun_is_cleanup_only_without_marker_rewrite(self):
        now=[1]; outcome=self.publish(clock=lambda:now[0]); live=outcome['liveVerification']
        path=self.archive/'retained-native-terminal.json'; before=path.read_bytes(); now[0]=181
        result=live.verify()
        self.assertFalse(result['publicationParentMonotonicDeadlineExceeded'])
        self.assertTrue(result['currentParentMonotonicDeadlineExceeded'])
        self.assertFalse(result['measurementAccepted'])
        self.assertEqual(path.read_bytes(),before)

    def test_live_verification_clock_failure_is_sticky(self):
        now=[1]; live=self.publish(clock=lambda:now[0])['liveVerification']; now[0]=0
        with self.assertRaisesRegex(Exception,'PUBLICATION_CLOCK_CHANGED'): live.verify()
        now[0]=2
        with self.assertRaisesRegex(Exception,'PUBLICATION_LIVE_UNCERTAIN'): live.verify()

    def test_retained_inventory_change_during_last_marker_readback_blocks_initial_return(self):
        original=pub._hash_bounded
        def late_entry(path,size,info):
            result=original(path,size,info)
            if Path(path).name=='retained-native-terminal.json': (self.archive/'unlisted.dat').write_bytes(b'SYNTHETIC')
            return result
        with patch.object(pub,'_hash_bounded',side_effect=late_entry):
            with self.assertRaisesRegex(pub.PublicationFailure,'PUBLICATION_FINAL_RETAINED_INVENTORY'): self.publish()
        self.assertTrue((self.archive/'retained-native-terminal.json').exists())
        self.assertTrue((self.journal/'publication-uncertain.json').exists())

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
        now=[179];original=pub._write_control
        def cross(path,value):
            result=original(path,value)
            if path.name=='retained-native-terminal.json':now[0]=181
            return result
        with patch.object(pub,'_write_control',side_effect=cross),self.assertRaisesRegex(pub.PublicationFailure, "PUBLICATION_DEADLINE_CROSSED_DURING_MARKER"):
            self.publish(clock=lambda: now[0])
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
        self.assertEqual(len(list(self.archive.iterdir())), 17)

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
