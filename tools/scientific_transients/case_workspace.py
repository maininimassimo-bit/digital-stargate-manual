"""One minimised, coherent case view from a verified frozen dossier. No execution."""
from tools.pixinsight.local_pilot.broker import require,encode
from tools.scientific_transients.attempt_journal import read_json,write_new

def assemble(plan,package,ledger,head):
    receipt,content=package.verify()
    review=package.view(ledger,head,plan)
    require(review['packageStatus']=='RETAINED_PACKAGE_VERIFIED' and review['planStatus']=='LIVE_PLAN_MATCHES','WORKSPACE_CURRENT_BINDING')
    retained=package.directory/'retained'
    frozen,_=read_json(retained/'plan-view.json');triplet,_=read_json(retained/'triplet.json')
    current=plan.view()
    require(current==frozen and review['planSha256']==current['planSha256']
        and review['planHeadSha256']==triplet['headSha256']==current['headSha256']
        and review['caseRef']==triplet['caseRef'],'WORKSPACE_PLAN_CASE_BINDING')
    comparison=None
    if content['comparisonPresent']:
        comparison,_=read_json(retained/'comparison.json')
        require(comparison['planSha256']==current['planSha256'] and comparison['headSha256']==current['headSha256']
            and comparison['caseRef']==review['caseRef'],'WORKSPACE_COMPARISON_BINDING')
    recovery=None
    if review['schema']=='BKL051_CASE_DOSSIER_REVIEW_V2':
        binding,_=read_json(retained/'contextual-recovery.json')
        recovery,actual=read_json(retained/'contextual-recovery/Risultato-minimizzato-portale-v2.json')
        require(binding['relationship']==review['contextualRecoveryRelationship']=='CONTEXT_ONLY_NOT_CASE_RECOVERY_OR_VALIDATION'
            and binding['resultSha256']==actual and binding['sourceSha256']==recovery['sourceSha256'],'WORKSPACE_CONTEXT_BINDING')
    require(package.view(ledger,head,plan)==review and plan.view()==current,'WORKSPACE_CHANGED_DURING_EXPORT')
    value={'schema':'BKL051_CASE_WORKSPACE_V1','caseRef':review['caseRef'],'plan':current,'triplet':triplet,
        'dossier':review,'comparison':comparison,'contextualRecovery':recovery,
        'scope':'LOCAL_VERIFIED_EXPORT_IMPORTED_RECEIPT_NOT_REMOTE_BYTE_ATTESTATION',
        'scientificAcceptance':False,'submissionAuthorized':False,'qualifiedControls':0}
    require(len(encode(value))<=1048576,'WORKSPACE_PORTAL_SIZE_LIMIT')
    return value

def main():
    import argparse
    from pathlib import Path
    from tools.scientific_transients.test_plan import PlanVersion
    from tools.scientific_transients.case_dossier import CaseDossier
    from tools.scientific_transients.preview_review_ledger import PreviewReviewLedger
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('plan','plan-sha','package','package-sha','ledger','anchor-sha','head-sha','output'):p.add_argument('--'+key,required=True)
    a=p.parse_args()
    print(write_new(Path(a.output),assemble(PlanVersion(a.plan,a.plan_sha),CaseDossier(a.package,a.package_sha),
        PreviewReviewLedger(a.ledger,a.anchor_sha),a.head_sha)))

if __name__=='__main__':main()
