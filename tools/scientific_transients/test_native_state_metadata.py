"""Pure synthetic metadata; no image bytes, process observations or native results."""
import copy
import unittest

from tools.scientific_transients import native_publication as pub
from tools.scientific_transients.native_state_metadata import check_state_metadata


class NativeStateMetadataTests(unittest.TestCase):
    def setUp(self):
        self.expected=dict(operationRef='a'*32,parametersSha256='1'*64,sealSha256='2'*64,sourceSha256='3'*64,
            kernelSpecSha256='4'*64,lineageSha256='5'*64,dependencies=dict(coreSha256='6'*64,wrapperSha256='7'*64,
            parserSha256='8'*64,primarySha256='9'*64),pixInsightVersion='SYNTHETIC_PI',nativeProcessId='4242',
            processSessionRef='c'*32,ownerSha256='d'*64,ownerReadySha256='e'*64)
        self.started=dict(protocol='DSG_NATIVE_LINEAR_STARTED_V1',maxStarts=1,
            **{k:self.expected[k] for k in ['operationRef','parametersSha256','sealSha256','pixInsightVersion']})
        self.evidence=dict(protocol='DSG_NATIVE_LINEAR_EVIDENCE_V2',
            **{k:copy.deepcopy(v) for k,v in self.expected.items() if k!='sealSha256'},
            sourceFormat='FLOAT32_BE',orientation='FITS_AXIS1_FAST_NO_FLIP',sourceValueImportCompared=True,
            allSourceValuesPreserved=True,checkpointKind='NATIVE_MATERIALIZATION_OF_SOURCE_VALUES',
            checkpointReopenCompared=True,upstreamPixInsightHistory='NOT_PRESENT_IN_SOURCE_FITS',
            fullPhysicalVariance=None,significance=None,scientificValidation='NOT_VALIDATED',qualifiedControls=0,
            provenanceVerified=False,physicalApplicabilityVerified=False)
        self.terminal=dict(protocol='DSG_NATIVE_LINEAR_TERMINAL_V1',operationRef='a'*32,
            state='COMPLETED_CONDITIONAL_COMPUTATION',errorCode=None,retentionErrorCode=None,
            unclosedOwnedViews=0,cooperativeDeadlineExceeded=False,fullPhysicalVariance=None,significance=None,
            scientificValidation='NOT_VALIDATED',qualifiedControls=0,provenanceVerified=False,
            physicalApplicabilityVerified=False,products=[])
        self.products(pub.REQUIRED)

    def products(self,names):
        self.terminal['products']=[dict(role=n,name=n,sha256='f'*64,byteLength=0 if n=='native.log' else 1) for n in sorted(names)]

    def failed(self,names):
        self.terminal.update(state='FAILED_RETAINED',errorCode='SYNTHETIC_FAILURE')
        self.products(names)
        if 'native-evidence.json' not in names: self.evidence=None

    def inspect(self): return check_state_metadata(self.terminal,self.started,self.evidence,self.expected)

    def test_completed_metadata_is_not_byte_ownership_or_science_authority(self):
        result=self.inspect()
        self.assertEqual(result['retentionBranch'],'COMPLETED_CONDITIONAL')
        for key in ['processClosureAuthorized','newNativeStartAllowed','measurementAccepted']:
            self.assertFalse(result[key])
        self.assertEqual(result['qualifiedControls'],0)
        self.assertIsNone(result['significance'])

    def test_failed_full_artifact_set_can_only_be_cleanup_metadata(self):
        self.failed(pub.REQUIRED); self.terminal['cooperativeDeadlineExceeded']=True
        result=self.inspect()
        self.assertEqual(result['retentionBranch'],'FAILED_FULL_ARTIFACT_SET')
        self.assertFalse(result['conditionalComputationDeclaredComplete'])

    def test_failure_before_image_accepts_only_started_and_log(self):
        self.failed({'started-native.json','native.log'})
        self.assertEqual(self.inspect()['retentionBranch'],'FAILED_BEFORE_IMAGE')

    def test_source_error_retention_requires_all_three_causal_roles(self):
        names={'started-native.json','native.log','source-initial.js','closing-source.js','error-owned-1.xisf'}
        self.failed(names)
        self.assertEqual(self.inspect()['retentionBranch'],'FAILED_ERROR_RETENTION')
        for missing in ['source-initial.js','closing-source.js','error-owned-1.xisf']:
            self.products(names-{missing})
            with self.assertRaisesRegex(Exception,'STATE_METADATA_SOURCE_ERROR_RETENTION'): self.inspect()

    def test_checkpoint_error_retention_is_paired(self):
        names={'started-native.json','native.log','source-initial.js','closing-source.js','error-owned-1.xisf',
            'checkpoint-initial.js','closing-checkpoint.js','error-owned-2.xisf'}
        self.failed(names); self.inspect()
        for missing in ['closing-checkpoint.js','error-owned-2.xisf']:
            self.products(names-{missing})
            with self.assertRaisesRegex(Exception,'STATE_METADATA_CHECKPOINT_ERROR_RETENTION'): self.inspect()

    def test_checkpoint_saved_before_failed_reopen_is_preserved_without_reopen_claim(self):
        self.failed({'started-native.json','native.log','source-initial.js','closing-source.js',
            'error-owned-1.xisf','checkpoint.xisf','result.json'})
        self.assertEqual(self.inspect()['retentionBranch'],'FAILED_ERROR_RETENTION')

    def test_orphan_checkpoint_roles_are_rejected(self):
        base={'started-native.json','native.log','source-initial.js','closing-source.js','error-owned-1.xisf'}
        for orphan in ['checkpoint-current.js','closing-checkpoint.js','error-owned-2.xisf']:
            self.failed(base|{orphan})
            with self.assertRaisesRegex(Exception,'STATE_METADATA_ORPHAN_CHECKPOINT'): self.inspect()

    def test_full_completed_artifacts_plus_error_views_can_be_failed_retention(self):
        self.failed(pub.REQUIRED|{'error-owned-1.xisf','error-owned-2.xisf'})
        self.assertEqual(self.inspect()['retentionBranch'],'FAILED_ERROR_RETENTION')

    def test_native_comparison_flags_are_strict_true(self):
        for key in ['sourceValueImportCompared','allSourceValuesPreserved','checkpointReopenCompared']:
            original=self.evidence[key]
            for bad in [False,1,'true']:
                self.evidence[key]=bad
                with self.assertRaisesRegex(Exception,'STATE_METADATA_NATIVE_COMPARISONS'): self.inspect()
            self.evidence[key]=original

    def test_evidence_links_to_source_code_owner_session_and_version(self):
        for key in ['sourceSha256','parametersSha256','ownerSha256','ownerReadySha256',
                    'processSessionRef','nativeProcessId','pixInsightVersion']:
            original=self.evidence[key]; self.evidence[key]='MISMATCH'
            with self.assertRaisesRegex(Exception,'STATE_METADATA_EVIDENCE_BINDING'): self.inspect()
            self.evidence[key]=original

    def test_dependency_mismatch_is_rejected(self):
        self.evidence['dependencies']['wrapperSha256']='0'*64
        with self.assertRaisesRegex(Exception,'STATE_METADATA_EVIDENCE_BINDING'): self.inspect()

    def test_started_metadata_has_exact_single_start_and_source_binding(self):
        self.started['maxStarts']=True
        with self.assertRaisesRegex(Exception,'STATE_METADATA_STARTED'): self.inspect()
        self.started['maxStarts']=1; self.started['parametersSha256']='0'*64
        with self.assertRaisesRegex(Exception,'STATE_METADATA_STARTED'): self.inspect()

    def test_empty_history_or_checkpoint_is_not_retention(self):
        for name in ['source-initial.js','closing-checkpoint.js','checkpoint.xisf']:
            self.products(pub.REQUIRED)
            next(r for r in self.terminal['products'] if r['name']==name)['byteLength']=0
            with self.assertRaisesRegex(Exception,'STATE_METADATA_EMPTY_ARTIFACT'): self.inspect()

    def test_uncertain_retention_or_open_views_never_pass(self):
        self.failed(pub.REQUIRED); self.terminal['state']='UNCERTAIN_RETENTION'
        with self.assertRaisesRegex(Exception,'STATE_METADATA_UNCERTAIN_VIEWS'): self.inspect()
        self.terminal['state']='FAILED_RETAINED'; self.terminal['unclosedOwnedViews']=1
        with self.assertRaisesRegex(Exception,'STATE_METADATA_UNCERTAIN_VIEWS'): self.inspect()
        self.terminal['unclosedOwnedViews']=0; self.terminal['retentionErrorCode']='SYNTHETIC_RETENTION'
        with self.assertRaisesRegex(Exception,'STATE_METADATA_UNCERTAIN_VIEWS'): self.inspect()

    def test_cancelled_code_is_consistent_with_reviewed_wrapper(self):
        self.failed({'started-native.json','native.log'}); self.terminal['state']='CANCELLED_RETAINED'
        with self.assertRaisesRegex(Exception,'STATE_METADATA_CANCEL_CODE'): self.inspect()
        self.terminal['errorCode']='NATIVE_LINEAR_CANCELLED'; self.inspect()

    def test_positive_science_flags_and_unknown_fields_rejected(self):
        self.evidence['qualifiedControls']=True
        with self.assertRaisesRegex(Exception,'STATE_METADATA_SCIENCE_FLAGS'): self.inspect()
        self.evidence['qualifiedControls']=0; self.evidence['extra']='NO'
        with self.assertRaises(Exception): self.inspect()


if __name__=='__main__': unittest.main()
