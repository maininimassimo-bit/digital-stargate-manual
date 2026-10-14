"""Offline derived-input association audit. No launch or permission is granted."""
from pathlib import Path
from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.local_registry import fingerprint, safe_path
from tools.scientific_transients.input_lineage import inspect_lineage
from tools.scientific_transients.native_aperture import LIBRARY


def signed_read_evidence(directory, expected_sha, algorithm_sha):
    """Check retained regression bytes, not independent scientific attestations."""
    directory=safe_path(directory)
    v,sha=read_json(directory/'verification.json')
    require(sha==expected_sha and v['scope']=='NEW_NATIVE_SYNTHETIC_SIGNED_READ_REGRESSION'
            and v['sourceLibrarySha256']==algorithm_sha
            and v['scienceValidation']=='NOT_VALIDATED' and v['qualifiedControls']==0
            and type(v['engineMaxAbsoluteError']) in {int,float} and v['engineMaxAbsoluteError']==0
            and type(v['checkpointMaxAbsoluteError']) in {int,float} and v['checkpointMaxAbsoluteError']==0
            and v['negativePixels']==1 and v['aboveOnePixels']==1
            and v['ownedInstanceStopped'] is True and v['userInstancesTouched'] is False,
            'DERIVED_SIGNED_REGRESSION')
    require(read_json(directory/'wrapper-terminal.json')[1]==v['wrapperTerminalSha256']
            and read_json(directory/'terminal.json')[1]==v['nativeTerminalSha256']
            and fingerprint(directory/'input.xisf')['sha256']==v['inputSha256']
            and fingerprint(directory/'checkpoint.xisf')['sha256']==v['checkpointSha256']
            and fingerprint(directory/'native_aperture.jsh')['sha256']==algorithm_sha,
            'DERIVED_SIGNED_REGRESSION_CHANGED')
    return sha


def preflight(plan, case_ref, frame_ref, operator, lineage_directory, lineage_receipt_sha,
              draft_path, draft_sha, *, signed_evidence_directory=None, signed_evidence_sha=None):
    anchor=plan.read();_,head=plan.events();operator.verify()
    case=next((c for c in anchor['draft']['cases'] if c['caseRef']==case_ref),None)
    frame=next((f for f in case['frames'] if f['frameRef']==frame_ref),None) if case else None
    require(frame is not None,'DERIVED_FRAME_UNKNOWN')
    lineage=inspect_lineage(lineage_directory,lineage_receipt_sha,draft_path,draft_sha)
    selected=next((r for r in lineage['inputs'] if r['rawSha256']==frame['sha256']),None)
    manifest=operator.registry.verify(operator.value['binding']['bindingRef'],operator.value['manifestSha256'])
    inputs=[r['sha256'] for r in manifest['files'] if r['role']=='INPUT']
    algorithms=[r['sha256'] for r in manifest['files'] if r['role']=='ALGORITHM']
    rules=[r['sha256'] for r in manifest['files'] if r['role']=='CONTRACT']
    expected_rules=next(r['sha256'] for r in anchor['evidence'] if r['role']=='RULES')
    signed_sha=None
    if signed_evidence_directory is not None:
        require(signed_evidence_sha is not None,'DERIVED_SIGNED_EVIDENCE_PIN')
        signed_sha=signed_read_evidence(signed_evidence_directory,signed_evidence_sha,anchor['draft']['algorithmRef'])
    else:
        require(signed_evidence_sha is None,'DERIVED_SIGNED_EVIDENCE_PIN')
    matches={'originalInSelectedCase':selected is not None,
             'sameCandidatePlan':lineage['candidatePlanRef']==anchor['draft']['planRef'],
             'originalInCandidateManifest':selected is not None and selected['sampleMembership']=='IN_CANDIDATE_MANIFEST',
             'derivedMatchesPreparedInput':selected is not None and inputs==[selected['derivedSha256']],
             'algorithmMatchesFrozenPlan':algorithms==[anchor['draft']['algorithmRef']],
             'rulesMatchFrozenPlan':rules==[expected_rules],
             'currentSignedReadImplementation':algorithms==[fingerprint(LIBRARY)['sha256']],
             'signedReadNativeRegressionPinned':signed_sha is not None}
    blocks=['DERIVED_ATTEMPT_ARCHIVE_LINK_REQUIRED','CALIBRATION_SCIENTIFIC_VALIDATION_MISSING',
            'FULL_UNCERTAINTY_MISSING','CONFIRMATORY_ATTESTATIONS_MISSING']
    reasons={'originalInSelectedCase':'ORIGINAL_NOT_IN_SELECTED_CASE','sameCandidatePlan':'CANDIDATE_PLAN_MISMATCH',
             'originalInCandidateManifest':'ORIGINAL_OUTSIDE_CANDIDATE_MANIFEST',
             'derivedMatchesPreparedInput':'DERIVED_INPUT_MISMATCH','algorithmMatchesFrozenPlan':'ALGORITHM_MISMATCH',
             'rulesMatchFrozenPlan':'RULES_MISMATCH','currentSignedReadImplementation':'SIGNED_READ_IMPLEMENTATION_MISMATCH',
             'signedReadNativeRegressionPinned':'SIGNED_READ_NATIVE_EVIDENCE_MISSING'}
    blocks.extend(reasons[k] for k,ok in matches.items() if not ok)
    return {'schema':'BKL051_DERIVED_INPUT_PREFLIGHT_V1','status':'BLOCKED',
            'planSha256':plan.sha,'headSha256':head,'caseRef':case_ref,'frameRef':frame_ref,
            'rawSha256':frame['sha256'],'derivedSha256':selected['derivedSha256'] if selected else None,
            'sourceReceiptSha256':lineage_receipt_sha,'candidateDraftSha256':draft_sha,
            'signedReadEvidenceSha256':signed_sha,'matches':matches,'blockers':blocks,
            'scope':'LOCAL_ASSOCIATIONS_ONLY_NO_EXECUTION_PERMISSION','executionAuthorized':False,
            'scienceValidation':'NOT_VALIDATED','qualifiedControls':0,'completeUncertainty':None,'significance':None}


def main():
    import argparse
    from tools.scientific_transients.test_plan import PlanVersion
    from tools.scientific_transients.operator_run import OperatorPlan
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('plan','plan-sha256','case','frame','operator','operator-sha256','lineage-directory',
                 'lineage-receipt-sha256','draft','draft-sha256','output'):
        p.add_argument('--'+name,required=True)
    p.add_argument('--signed-evidence-directory');p.add_argument('--signed-evidence-sha256')
    a=p.parse_args()
    value=preflight(PlanVersion(a.plan,a.plan_sha256),a.case,a.frame,OperatorPlan.load(Path(a.operator),a.operator_sha256),
        a.lineage_directory,a.lineage_receipt_sha256,Path(a.draft),a.draft_sha256,
        signed_evidence_directory=a.signed_evidence_directory,signed_evidence_sha=a.signed_evidence_sha256)
    print(write_new(Path(a.output),value))


if __name__=='__main__':main()
