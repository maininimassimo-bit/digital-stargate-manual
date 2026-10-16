"""Offline correlation handoff from retained Owner operations; no launch grant."""
import copy

from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients.attempt_journal import read_json
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.confirmatory_campaign import fingerprint
from tools.scientific_transients.campaign_handoff import make_handoff, selection_sha
from tools.scientific_transients.campaign_triplet import CampaignTriplet
from tools.scientific_transients import owner_operation_stager as staging
from tools.scientific_transients.operator_run import ORIGIN


def _retained(root, proposal, action, request, path, selection, key):
    directory = safe_path(root / key)
    require({p.name for p in directory.iterdir()} == {'intent.json','envelope.json'},
            'OWNER_HANDOFF_UNCONFIRMED_STAGE')
    intent, _ = read_json(directory / 'intent.json')
    envelope, _ = read_json(directory / 'envelope.json')
    challenge = staging.validate_challenge(envelope['challenge'])
    require(challenge['action'] == action and challenge['planRef'] == proposal['planRef']
            and challenge['proposalSha256'] == selection and challenge['requestSha256'] == staging.request_sha(request)
            and challenge['routeSha256'] == staging.route_sha(path), 'OWNER_HANDOFF_STAGE_CHALLENGE')
    expected = dict(protocol=staging.ENVELOPE, action=action, planRef=proposal['planRef'],operationKeySha256=key,
                    challenge=challenge,request=request,requestSha256=staging.request_sha(request),relativePath=path,
                    launchAuthorized=False,scientificValidation='NOT_VALIDATED')
    expected['envelopeSha256'] = fingerprint(expected)
    expected_intent = {
        'protocol':'DSG_CAMPAIGN_LOCAL_OWNER_INTENT_V1','serviceOrigin':ORIGIN,'operationKeySha256':key,
        'action':action,'relativePath':path,'request':request,'challenge':challenge,
        'envelopeSha256':expected['envelopeSha256'],'implicitRetry':False}
    require(fingerprint(envelope)==fingerprint(expected) and fingerprint(intent)==fingerprint(expected_intent),
            'OWNER_HANDOFF_STAGE_CHANGED')


def build_handoff(triplet, intent_receipt, projection_receipts):
    require(type(triplet) is CampaignTriplet, 'OWNER_HANDOFF_PACKAGE')
    intent_receipt=copy.deepcopy(intent_receipt);projection_receipts=copy.deepcopy(projection_receipts)
    proposal=triplet.owner_proposal()
    receipt=staging.validate_intent_receipt(intent_receipt,proposal)
    require(type(projection_receipts) is list and len(projection_receipts)==3, 'OWNER_HANDOFF_THREE_RECEIPTS')
    root=safe_path(triplet.directory.parent / '_owner-operations-v1')
    base='/v1/transient-analysis/campaigns/'+proposal['planRef']+'/dispatch-intents'
    _retained(root,proposal,'DISPATCH_INTENT',proposal['request'],base,proposal['proposalSha256'],
              staging.operation_key(proposal,'DISPATCH_INTENT'))
    common=dict(planRef=proposal['planRef'],intentSha256=receipt['intentSha256'],
                queueNamespaceSha256=receipt['queueNamespaceSha256'],contextSha256=proposal['request']['contextSha256'],
                archiveSha256=proposal['request']['archiveSha256'],workerId=proposal['request']['workerId'],rootId=proposal['request']['rootId'])
    jobs=[]
    for ordinal,(selected,frame,observed) in enumerate(zip(proposal['request']['jobs'],triplet.context['frames'],projection_receipts)):
        job=dict(ordinal=ordinal,jobId='TRN_'+selected['requestId'],requestId=selected['requestId'],
                 bindingRef=selected['binding']['bindingRef'],bindingSha256=fingerprint(selected['binding']),inputSha256=frame['sha256'])
        key=staging.operation_key(proposal,'PROJECT_JOB',receipt,ordinal)
        expected=dict(protocol='DSG_CAMPAIGN_OWNER_PROJECTION_RECEIPT_V1',planRef=proposal['planRef'],
                      intentSha256=receipt['intentSha256'],queueNamespaceSha256=receipt['queueNamespaceSha256'],
                      ordinal=ordinal,jobId=job['jobId'],requestSelectionSha256=selection_sha({**common,**job}),
                      projectionObserved=True,reservationFreshness='NOT_ATTESTED',operationKeySha256=key,
                      requestSha256=staging.request_sha({}),launchAuthorized=False,scientificValidation='NOT_VALIDATED')
        expected['receiptSha256']=fingerprint(expected)
        require(type(observed) is dict and type(observed.get('ordinal')) is int and fingerprint(observed)==fingerprint(expected),
                'OWNER_HANDOFF_PROJECTION_RECEIPT')
        _retained(root,proposal,'PROJECT_JOB',{},base+'/'+receipt['intentSha256']+'/jobs/'+str(ordinal)+'/project',
                  staging.projection_selection_sha(proposal,receipt,ordinal),key)
        jobs.append(job)
    require(triplet.owner_proposal()==proposal,'OWNER_HANDOFF_PACKAGE_CHANGED')
    return make_handoff(common,jobs)

def export_handoff(triplet, intent_receipt, projection_receipts, output):
    """Retain and export once; an uncertain export requires assisted reconciliation."""
    from pathlib import Path
    from tools.scientific_transients.attempt_journal import write_new
    from tools.pixinsight.local_pilot.broker import ProtocolError
    intent_receipt=copy.deepcopy(intent_receipt);projection_receipts=copy.deepcopy(projection_receipts)
    handoff=build_handoff(triplet,intent_receipt,projection_receipts)
    output=Path(output)
    require(output.is_absolute() and '..' not in output.parts,'OWNER_HANDOFF_OUTPUT_PATH')
    output=safe_path(output.parent)/output.name
    protected=[triplet.directory.parent,triplet.archive.directory]
    for plan in triplet.plans:protected.extend(plan.roots.values())
    require(all(output!=root and root not in output.parents for root in protected),'OWNER_HANDOFF_OUTPUT_OVERLAP')
    root=triplet.directory.parent/'_worker-handoffs-v1';root.mkdir(exist_ok=True);safe_path(root)
    directory=root/triplet.context['contextSha256'];directory.mkdir()  # Exclusive provenance lock, not launch authority.
    try:
        statement=dict(protocol='DSG_CAMPAIGN_OWNER_HANDOFF_EXPORT_V1',contextSha256=triplet.context['contextSha256'],
                       intentReceiptSha256=intent_receipt['receiptSha256'],
                       projectionReceiptSha256=[r['receiptSha256'] for r in projection_receipts],
                       handoffSha256=handoff['handoffSha256'],nativeLaunchRequested=False,implicitRetry=False)
        retained=[]
        for name,value in [('intent.json',statement),('receipts.json',dict(intent=intent_receipt,projections=projection_receipts)),
                           ('handoff.json',handoff)]:
            sha=write_new(directory/name,value);require(read_json(directory/name)==(value,sha),'OWNER_HANDOFF_RETENTION')
            retained.append((name,value,sha))
        require(build_handoff(triplet,intent_receipt,projection_receipts)==handoff,'OWNER_HANDOFF_SOURCE_CHANGED')
        require(all(read_json(directory/name)==(value,sha) for name,value,sha in retained),'OWNER_HANDOFF_RETENTION')
        exported_sha=write_new(output,handoff)
        require(read_json(output)==(handoff,exported_sha)
                and build_handoff(triplet,intent_receipt,projection_receipts)==handoff
                and all(read_json(directory/name)==(value,sha) for name,value,sha in retained),
                'OWNER_HANDOFF_EXPORT_UNCONFIRMED')
        completed=dict(handoffFileSha256=exported_sha,nativeLaunchRequested=False,scientificValidation='NOT_VALIDATED')
        completed_sha=write_new(directory/'completed.json',completed)
        require(read_json(directory/'completed.json')==(completed,completed_sha)
                and all(read_json(directory/name)==(value,sha) for name,value,sha in retained)
                and read_json(output)==(handoff,exported_sha)
                and build_handoff(triplet,intent_receipt,projection_receipts)==handoff,'OWNER_HANDOFF_COMPLETION')
        return copy.deepcopy(handoff)
    except BaseException:
        try:write_new(directory/'unconfirmed.json',dict(state='RECONCILIATION_REQUIRED',implicitRetry=False,nativeLaunchRequested=False))
        except (OSError,ProtocolError):pass
        raise ProtocolError('OWNER_HANDOFF_EXPORT_UNCONFIRMED_NO_REPLAY') from None


def main(argv=None):
    import argparse
    import json
    from tools.scientific_transients.campaign_worker_cli import load_config
    from tools.scientific_transients.queue import digest
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('config','config-sha256','intent-receipt','intent-receipt-sha256','output'):
        parser.add_argument('--'+name,required=True)
    parser.add_argument('--projection-receipt',action='append',nargs=2,metavar=('PATH','SHA256'),required=True)
    args=parser.parse_args(argv)
    try:
        require(len(args.projection_receipt)==3,'OWNER_HANDOFF_THREE_RECEIPTS')
        triplet=CampaignTriplet.reopen_registered(*load_config(args.config,args.config_sha256))
        intent,actual=read_json(args.intent_receipt)
        require(digest(args.intent_receipt_sha256) and actual==args.intent_receipt_sha256,'OWNER_HANDOFF_RECEIPT_FILE')
        receipts=[]
        for path,expected in args.projection_receipt:
            receipt,actual=read_json(path)
            require(digest(expected) and actual==expected,'OWNER_HANDOFF_RECEIPT_FILE');receipts.append(receipt)
        export_handoff(triplet,intent,receipts,args.output)
        print(json.dumps(dict(handoffExported=True,networkRequested=False,nativeLaunchRequested=False,
                              scientificValidation='NOT_VALIDATED'),sort_keys=True));return 0
    except (Exception,KeyboardInterrupt):
        print(json.dumps(dict(handoffExported=False,evidenceMustBePreserved=True,implicitRetry=False,
                              nativeLaunchRequested=False,scientificValidation='NOT_VALIDATED'),sort_keys=True));return 2


if __name__=='__main__':raise SystemExit(main())
