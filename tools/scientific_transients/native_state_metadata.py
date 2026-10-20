"""S6 metadata checks only. Caller must prove raw pins, causal return and live ownership."""
import re

from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients import native_publication as pub


DEPENDENCIES={'coreSha256','wrapperSha256','parserSha256','primarySha256'}
EXPECTED={'operationRef','parametersSha256','sealSha256','sourceSha256','kernelSpecSha256','lineageSha256',
          'dependencies','pixInsightVersion','nativeProcessId','processSessionRef','ownerSha256','ownerReadySha256'}
EVIDENCE={'protocol','operationRef','nativeProcessId','processSessionRef','ownerSha256','ownerReadySha256',
          'sourceSha256','parametersSha256','kernelSpecSha256','lineageSha256','dependencies','pixInsightVersion',
          'sourceFormat','orientation','sourceValueImportCompared','allSourceValuesPreserved','checkpointKind',
          'checkpointReopenCompared','upstreamPixInsightHistory','fullPhysicalVariance','significance',
          'scientificValidation','qualifiedControls','provenanceVerified','physicalApplicabilityVerified'}


def _expected(value):
    pub._fields(value,EXPECTED)
    require(type(value['operationRef']) is str and re.fullmatch('[a-f0-9]{32}',value['operationRef']) and
            type(value['processSessionRef']) is str and re.fullmatch('[a-f0-9]{32}',value['processSessionRef']),
            'STATE_METADATA_IDENTITY')
    for key in EXPECTED-{'operationRef','processSessionRef','nativeProcessId','dependencies','pixInsightVersion'}:
        require(pub._sha(value[key]),'STATE_METADATA_EXPECTED_SHA')
    pub._fields(value['dependencies'],DEPENDENCIES)
    require(all(pub._sha(v) for v in value['dependencies'].values()),'STATE_METADATA_DEPENDENCIES')
    pid=value['nativeProcessId']; version=value['pixInsightVersion']
    require(type(pid) is str and re.fullmatch('[1-9][0-9]{0,9}',pid) and int(pid)<=4294967295,
            'STATE_METADATA_PID')
    require(type(version) is str and 1<=len(version)<=192 and version.isascii() and
            all(32<=ord(c)<127 for c in version),'STATE_METADATA_VERSION')


def _started(value,expected):
    pub._fields(value,{'protocol','operationRef','parametersSha256','sealSha256','pixInsightVersion','maxStarts'})
    require(value['protocol']=='DSG_NATIVE_LINEAR_STARTED_V1' and type(value['maxStarts']) is int
            and value['maxStarts']==1 and all(value[k]==expected[k] for k in
                ['operationRef','parametersSha256','sealSha256','pixInsightVersion']),'STATE_METADATA_STARTED')


def _evidence(value,expected):
    pub._fields(value,EVIDENCE); pub._fields(value['dependencies'],DEPENDENCIES)
    require(value['protocol']=='DSG_NATIVE_LINEAR_EVIDENCE_V2' and
            all(value[k]==expected[k] for k in EXPECTED-{'sealSha256'}),'STATE_METADATA_EVIDENCE_BINDING')
    require(value['sourceFormat']=='FLOAT32_BE' and value['orientation']=='FITS_AXIS1_FAST_NO_FLIP' and
            value['checkpointKind']=='NATIVE_MATERIALIZATION_OF_SOURCE_VALUES' and
            value['upstreamPixInsightHistory']=='NOT_PRESENT_IN_SOURCE_FITS','STATE_METADATA_IMPORT_PROFILE')
    require(all(value[k] is True for k in ['sourceValueImportCompared','allSourceValuesPreserved',
                'checkpointReopenCompared']),'STATE_METADATA_NATIVE_COMPARISONS')
    require(value['fullPhysicalVariance'] is None and value['significance'] is None and
            value['scientificValidation']=='NOT_VALIDATED' and type(value['qualifiedControls']) is int and
            value['qualifiedControls']==0 and value['provenanceVerified'] is False and
            value['physicalApplicabilityVerified'] is False,'STATE_METADATA_SCIENCE_FLAGS')


def check_state_metadata(terminal,started,evidence,expected):
    """Pure closed-schema metadata gate; no byte, process, image or acceptance proof.

    Input objects must be parsed from the immutable raw files already verified by
    the live supervisor. Passing matching JSON assertions cannot establish that fact.
    """
    _expected(expected)
    records=pub._terminal(terminal,expected['operationRef'])
    require(terminal['state']!='UNCERTAIN_RETENTION' and terminal['unclosedOwnedViews']==0
            and terminal['retentionErrorCode'] is None,'STATE_METADATA_UNCERTAIN_VIEWS')
    rows={r['name']:r for r in records}; names=set(rows)
    require({'started-native.json','native.log'}<=names,'STATE_METADATA_STARTED_LOG_REQUIRED')
    require(all(r['byteLength']>0 for n,r in rows.items() if n!='native.log'),'STATE_METADATA_EMPTY_ARTIFACT')
    _started(started,expected)
    if 'native-evidence.json' in names:
        _evidence(evidence,expected)
        require(pub.REQUIRED<=names,'STATE_METADATA_INCOMPLETE_EVIDENCE_SET')
    else: require(evidence is None,'STATE_METADATA_UNDECLARED_EVIDENCE')
    state=terminal['state']
    if state=='COMPLETED_CONDITIONAL_COMPUTATION':
        branch='COMPLETED_CONDITIONAL'
    else:
        require(state in {'FAILED_RETAINED','CANCELLED_RETAINED'},'STATE_METADATA_STATE')
        require((state=='CANCELLED_RETAINED')==(terminal['errorCode']=='NATIVE_LINEAR_CANCELLED'),
                'STATE_METADATA_CANCEL_CODE')
        if names==pub.REQUIRED:
            branch='FAILED_FULL_ARTIFACT_SET'
        elif names=={'started-native.json','native.log'}:
            branch='FAILED_BEFORE_IMAGE'
        else:
            require({'source-initial.js','closing-source.js','error-owned-1.xisf'}<=names,
                    'STATE_METADATA_SOURCE_ERROR_RETENTION')
            if 'checkpoint-initial.js' in names:
                require({'closing-checkpoint.js','error-owned-2.xisf'}<=names,
                        'STATE_METADATA_CHECKPOINT_ERROR_RETENTION')
            else:
                require(not names&{'checkpoint-current.js','closing-checkpoint.js','error-owned-2.xisf'},
                        'STATE_METADATA_ORPHAN_CHECKPOINT')
            branch='FAILED_ERROR_RETENTION'
    return {'stateMetadataConsistent':True,'retentionBranch':branch,'nativeState':state,
            'zeroOwnedViewsDeclared':True,'nativeCooperativeDeadlineExceeded':terminal['cooperativeDeadlineExceeded'],
            'conditionalComputationDeclaredComplete':state=='COMPLETED_CONDITIONAL_COMPUTATION',
            'processClosureAuthorized':False,'newNativeStartAllowed':False,'measurementAccepted':False,
            'fullPhysicalVariance':None,'significance':None,'scientificValidation':'NOT_VALIDATED','qualifiedControls':0}
