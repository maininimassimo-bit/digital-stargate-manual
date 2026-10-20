"""Read-only local export inspection. Never clears locks or authorizes retries."""
import copy
from pathlib import Path

from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients.attempt_journal import read_json
from tools.scientific_transients.confirmatory_campaign import fingerprint
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.owner_handoff import build_handoff
from tools.scientific_transients.campaign_triplet import CampaignTriplet
from tools.scientific_transients.operator_run import OperatorPlan


def _blocked():
    return dict(protocol='DSG_OWNER_HANDOFF_INSPECTION_V1',status='INCOMPLETE_OR_CONFLICT',
                localEvidenceOnly=True,consistentCopyObserved=False,recordedCompletion=False,
                uncertaintyMarkerObserved=None,evidenceHashes=None,needsAssistedRecovery=True,
                retryAuthorized=False,launchAuthorized=False,nativeStoppedAttested=False,
                scientificValidation='NOT_VALIDATED',qualifiedControls=0)


def _snapshot(directory,external):
    safe_path(directory)
    names={p.name for p in directory.iterdir()}
    require({'intent.json','receipts.json','handoff.json'}<=names
            and names<={'intent.json','receipts.json','handoff.json','completed.json','unconfirmed.json'},
            'HANDOFF_INSPECTION_ARTIFACT_SET')
    values={name:read_json(directory/name) for name in sorted(names)}
    values['externalCopy']=read_json(external)
    return values


def inspect_export(triplet,intent_receipt,projection_receipts,external):
    """Observe exact correlation only; a matching uncertain copy stays uncertain."""
    result=_blocked()
    try:
        intent_receipt=copy.deepcopy(intent_receipt);projection_receipts=copy.deepcopy(projection_receipts)
        require(type(triplet) is CampaignTriplet and triplet.phase=='REGISTERED','HANDOFF_INSPECTION_PACKAGE')
        # Reopen with pure verification before any constructor/preflight can log VERIFY.
        plans=[OperatorPlan.load(p.path,p.sha,engine=p.engine,catalog=p.catalog,record_verifications=False) for p in triplet.plans]
        triplet=CampaignTriplet.reopen_registered(triplet.directory.parent,triplet.context_path,triplet.context_file_sha,
            triplet.archive,plans,triplet.selection['request']['decisionId'])
        expected=build_handoff(triplet,intent_receipt,projection_receipts)
        external=Path(external);require(external.is_absolute() and '..' not in external.parts,'HANDOFF_INSPECTION_PATH')
        external=safe_path(external)
        protected=[triplet.directory.parent,triplet.archive.directory]
        for plan in triplet.plans:protected.extend(plan.roots.values())
        require(all(external!=root and root not in external.parents for root in protected),'HANDOFF_INSPECTION_COPY_OVERLAP')
        directory=triplet.directory.parent/'_worker-handoffs-v1'/triplet.context['contextSha256']
        before=_snapshot(directory,external)
        statement=dict(protocol='DSG_CAMPAIGN_OWNER_HANDOFF_EXPORT_V1',contextSha256=triplet.context['contextSha256'],
                       intentReceiptSha256=intent_receipt['receiptSha256'],
                       projectionReceiptSha256=[r['receiptSha256'] for r in projection_receipts],
                       handoffSha256=expected['handoffSha256'],nativeLaunchRequested=False,implicitRetry=False)
        for name,value in [('intent.json',statement),('receipts.json',dict(intent=intent_receipt,projections=projection_receipts)),
                           ('handoff.json',expected),('externalCopy',expected)]:
            require(fingerprint(before[name][0])==fingerprint(value),'HANDOFF_INSPECTION_ASSOCIATION')
        if 'completed.json' in before:
            completed=dict(handoffFileSha256=before['externalCopy'][1],nativeLaunchRequested=False,scientificValidation='NOT_VALIDATED')
            require(fingerprint(before['completed.json'][0])==fingerprint(completed),'HANDOFF_INSPECTION_COMPLETION')
        if 'unconfirmed.json' in before:
            marker=dict(state='RECONCILIATION_REQUIRED',implicitRetry=False,nativeLaunchRequested=False)
            require(fingerprint(before['unconfirmed.json'][0])==fingerprint(marker),'HANDOFF_INSPECTION_UNCERTAINTY')
        require(build_handoff(triplet,intent_receipt,projection_receipts)==expected,'HANDOFF_INSPECTION_SOURCE_CHANGED')
        after=_snapshot(directory,external)
        require(before.keys()==after.keys() and all(before[name][1]==after[name][1] for name in before),
                'HANDOFF_INSPECTION_OBSERVATION_CHANGED')
        uncertain='unconfirmed.json' in after
        result.update(status='CONSISTENT_RETAINED_COPY',consistentCopyObserved=True,
                      recordedCompletion='completed.json' in after,uncertaintyMarkerObserved=uncertain,
                      evidenceHashes={name:row[1] for name,row in after.items()},
                      needsAssistedRecovery=uncertain or 'completed.json' not in after)
        return result
    except Exception:
        return result


def main(argv=None,*,engine=None,catalog=None):
    import argparse,json
    from tools.scientific_transients.campaign_worker_cli import load_config
    from tools.scientific_transients.native_aperture import ENGINE,CATALOG
    from tools.scientific_transients.queue import digest
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('config','config-sha256','intent-receipt','intent-receipt-sha256','copy'):
        parser.add_argument('--'+name,required=True)
    parser.add_argument('--projection-receipt',action='append',nargs=2,metavar=('PATH','SHA256'),required=True)
    args=parser.parse_args(argv)
    try:
        require(len(args.projection_receipt)==3,'HANDOFF_INSPECTION_RECEIPT_COUNT')
        inputs=load_config(args.config,args.config_sha256,engine=ENGINE if engine is None else engine,
                           catalog=CATALOG if catalog is None else catalog,record_verifications=False)
        triplet=CampaignTriplet.reopen_registered(*inputs)
        intent,actual=read_json(args.intent_receipt)
        require(digest(args.intent_receipt_sha256) and actual==args.intent_receipt_sha256,'HANDOFF_INSPECTION_PIN')
        receipts=[]
        for path,expected in args.projection_receipt:
            value,actual=read_json(path);require(digest(expected) and actual==expected,'HANDOFF_INSPECTION_PIN')
            receipts.append(value)
        result=inspect_export(triplet,intent,receipts,args.copy)
    except (Exception,KeyboardInterrupt):result=_blocked()
    print(json.dumps(result,sort_keys=True))
    return 0 if result['status']=='CONSISTENT_RETAINED_COPY' else 2


if __name__=='__main__':raise SystemExit(main())
