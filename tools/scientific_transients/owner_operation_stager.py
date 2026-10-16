"""Offline one-shot Owner envelopes; no token, network or launch authority."""
import argparse
import copy
import json

from tools.pixinsight.local_pilot.broker import require, opaque, ProtocolError, encode
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.confirmatory_campaign import fingerprint
from tools.scientific_transients.queue import fields, digest
from tools.scientific_transients.operator_run import ORIGIN
from tools.scientific_transients.campaign_triplet import CampaignTriplet
from tools.scientific_transients.campaign_worker_cli import load_config
from tools.scientific_transients.native_aperture import ENGINE, CATALOG

CHALLENGE = 'DSG_CAMPAIGN_OWNER_CHALLENGE_V1'
ENVELOPE = 'DSG_CAMPAIGN_OWNER_DURABLE_OPERATION_V1'
INTENT_RECEIPT = 'DSG_CAMPAIGN_OWNER_INTENT_RECEIPT_V1'


def request_sha(request):
    return fingerprint({'protocol': 'DSG_CAMPAIGN_OWNER_REQUEST_V1', 'request': request})


def route_sha(path):
    return fingerprint({'protocol': 'DSG_CAMPAIGN_OWNER_ROUTE_V1', 'relativePath': path})


def validate_challenge(value):
    fields(value, {'protocol','nonce','action','planRef','proposalSha256','requestSha256','routeSha256','challengeSha256'})
    require(value['protocol'] == CHALLENGE and opaque(value['nonce']) and opaque(value['planRef'])
            and value['action'] in {'DISPATCH_INTENT','PROJECT_JOB'}
            and all(digest(value[k]) for k in ('proposalSha256','requestSha256','routeSha256','challengeSha256'))
            and value['challengeSha256'] == fingerprint({k:v for k,v in value.items() if k != 'challengeSha256'}),
            'OWNER_OPERATION_CHALLENGE')
    return copy.deepcopy(value)


def operation_key(proposal, action, receipt=None, ordinal=None):
    common = {'protocol': 'DSG_CAMPAIGN_OWNER_OPERATION_KEY_V1', 'serviceOrigin': ORIGIN,
              'action': action, 'planRef': proposal['planRef']}
    if action == 'DISPATCH_INTENT':
        common.update(witnessRef=proposal['request']['witnessRef'], contextSha256=proposal['request']['contextSha256'])
    else:
        require(action == 'PROJECT_JOB' and type(ordinal) is int and 0 <= ordinal < 3 and receipt is not None,
                'OWNER_OPERATION_SELECTION')
        common.update(intentSha256=receipt['intentSha256'], ordinal=ordinal)
    # decisionId and challenge must never create an alternate semantic lock.
    return fingerprint(common)


def validate_intent_receipt(value, proposal):
    fields(value, {'protocol','planRef','intentSha256','contextSha256','archiveSha256','queueNamespaceSha256',
                   'orderedJobSelectionDigests','operationKeySha256','requestSha256','launchAuthorized',
                   'scientificValidation','receiptSha256'})
    require(value['protocol'] == INTENT_RECEIPT and value['planRef'] == proposal['planRef']
            and value['contextSha256'] == proposal['request']['contextSha256']
            and value['archiveSha256'] == proposal['request']['archiveSha256']
            and digest(value['intentSha256']) and digest(value['queueNamespaceSha256'])
            and value['orderedJobSelectionDigests'] == [fingerprint(j) for j in proposal['request']['jobs']]
            and value['operationKeySha256'] == operation_key(proposal, 'DISPATCH_INTENT')
            and value['requestSha256'] == request_sha(proposal['request'])
            and value['launchAuthorized'] is False and value['scientificValidation'] == 'NOT_VALIDATED'
            and value['receiptSha256'] == fingerprint({k:v for k,v in value.items() if k != 'receiptSha256'}),
            'OWNER_OPERATION_INTENT_RECEIPT')
    return copy.deepcopy(value)


def projection_selection_sha(proposal, receipt, ordinal):
    require(type(ordinal) is int and 0 <= ordinal < 3, 'OWNER_OPERATION_ORDINAL')
    return fingerprint({'protocol': 'DSG_CAMPAIGN_OWNER_PROJECTION_SELECTION_V1',
                        'proposalSha256': proposal['proposalSha256'], 'intentReceipt': receipt,
                        'ordinal': ordinal, 'bindingSha256': fingerprint(proposal['request']['jobs'][ordinal]['binding'])})


class OwnerOperationStager:
    def __init__(self, triplet):
        require(type(triplet) is CampaignTriplet, 'OWNER_OPERATION_LOCAL_PACKAGE')
        self.triplet = triplet
        self.proposal = triplet.owner_proposal()  # Rechecks archive/plans and all registration ACKs.
        # One configured root shared by every package; no per-call alternate root.
        root = safe_path(triplet.directory.parent)
        self.root = root / '_owner-operations-v1'
        self.root.mkdir(exist_ok=True)
        safe_path(self.root); require(self.root.is_dir(), 'OWNER_OPERATION_ROOT')

    def stage_intent(self, challenge):
        proposal = self.triplet.owner_proposal()
        require(proposal == self.proposal, 'OWNER_OPERATION_PACKAGE_CHANGED')
        return self._stage(challenge, 'DISPATCH_INTENT', proposal['request'],
                           '/v1/transient-analysis/campaigns/' + proposal['planRef'] + '/dispatch-intents',
                           proposal['proposalSha256'], operation_key(proposal, 'DISPATCH_INTENT'))

    def stage_projection(self, challenge, receipt, ordinal):
        proposal = self.triplet.owner_proposal()
        require(proposal == self.proposal, 'OWNER_OPERATION_PACKAGE_CHANGED')
        receipt = validate_intent_receipt(receipt, proposal)
        require(type(ordinal) is int and 0 <= ordinal < 3, 'OWNER_OPERATION_ORDINAL')
        # The earlier intent lock must exist in this configured local root.
        intent_dir = self.root / operation_key(proposal, 'DISPATCH_INTENT')
        safe_path(intent_dir)
        require(not (intent_dir / 'unconfirmed.json').exists(), 'OWNER_OPERATION_PRIOR_UNCONFIRMED')
        intent, _ = read_json(intent_dir / 'intent.json')
        envelope, _ = read_json(intent_dir / 'envelope.json')
        fields(envelope, {'protocol','action','planRef','operationKeySha256','challenge','request',
                          'requestSha256','relativePath','launchAuthorized','scientificValidation','envelopeSha256'})
        prior_challenge = validate_challenge(envelope['challenge'])
        intent_path = '/v1/transient-analysis/campaigns/' + proposal['planRef'] + '/dispatch-intents'
        require(envelope == {
            'protocol': ENVELOPE, 'action': 'DISPATCH_INTENT', 'planRef': proposal['planRef'],
            'operationKeySha256': receipt['operationKeySha256'], 'challenge': prior_challenge,
            'request': proposal['request'], 'requestSha256': request_sha(proposal['request']),
            'relativePath': intent_path, 'launchAuthorized': False, 'scientificValidation': 'NOT_VALIDATED',
            'envelopeSha256': fingerprint({k:v for k,v in envelope.items() if k != 'envelopeSha256'})}
            and prior_challenge['action'] == 'DISPATCH_INTENT' and prior_challenge['planRef'] == proposal['planRef']
            and prior_challenge['proposalSha256'] == proposal['proposalSha256']
            and prior_challenge['requestSha256'] == request_sha(proposal['request'])
            and prior_challenge['routeSha256'] == route_sha(intent_path)
            and intent == {'protocol': 'DSG_CAMPAIGN_LOCAL_OWNER_INTENT_V1', 'serviceOrigin': ORIGIN,
                           'operationKeySha256': receipt['operationKeySha256'], 'action': 'DISPATCH_INTENT',
                           'relativePath': intent_path, 'request': proposal['request'], 'challenge': prior_challenge,
                           'envelopeSha256': envelope['envelopeSha256'], 'implicitRetry': False},
            'OWNER_OPERATION_PRIOR_INTENT')
        path = '/v1/transient-analysis/campaigns/' + proposal['planRef'] + '/dispatch-intents/' + \
               receipt['intentSha256'] + '/jobs/' + str(ordinal) + '/project'
        return self._stage(challenge, 'PROJECT_JOB', {}, path, projection_selection_sha(proposal, receipt, ordinal),
                           operation_key(proposal, 'PROJECT_JOB', receipt, ordinal))

    def _stage(self, challenge, action, request, path, selection_sha, key):
        challenge = validate_challenge(challenge)
        require(challenge['action'] == action and challenge['planRef'] == self.proposal['planRef']
                and challenge['proposalSha256'] == selection_sha and challenge['requestSha256'] == request_sha(request)
                and challenge['routeSha256'] == route_sha(path), 'OWNER_OPERATION_CHALLENGE_MISMATCH')
        directory = self.root / key; directory.mkdir()  # Atomic semantic lock, never removed.
        try:
            value = {'protocol': ENVELOPE, 'action': action, 'planRef': self.proposal['planRef'],
                     'operationKeySha256': key, 'challenge': challenge, 'request': copy.deepcopy(request),
                     'requestSha256': request_sha(request), 'relativePath': path,
                     'launchAuthorized': False, 'scientificValidation': 'NOT_VALIDATED'}
            value['envelopeSha256'] = fingerprint(value)
            intent = {'protocol': 'DSG_CAMPAIGN_LOCAL_OWNER_INTENT_V1', 'serviceOrigin': ORIGIN,
                      'operationKeySha256': key, 'action': action, 'relativePath': path,
                      'request': copy.deepcopy(request), 'challenge': challenge,
                      'envelopeSha256': value['envelopeSha256'], 'implicitRetry': False}
            require(len(encode(value)) <= 16384, 'OWNER_OPERATION_ENVELOPE_SIZE')
            intent_sha = write_new(directory / 'intent.json', intent)
            require(read_json(directory / 'intent.json') == (intent, intent_sha), 'OWNER_OPERATION_RETENTION')
            envelope_sha = write_new(directory / 'envelope.json', value)
            require(read_json(directory / 'envelope.json') == (value, envelope_sha)
                    and read_json(directory / 'intent.json') == (intent, intent_sha), 'OWNER_OPERATION_RETENTION')
            return copy.deepcopy(value)
        except BaseException:
            try: write_new(directory / 'unconfirmed.json', {'implicitRetry': False, 'state': 'RECONCILIATION_REQUIRED'})
            except (OSError, ProtocolError): pass
            raise ProtocolError('OWNER_OPERATION_UNCONFIRMED_NO_REPLAY') from None


def main(argv=None, *, engine=ENGINE, catalog=CATALOG):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['dispatch-intent','project-job'])
    for name in ('config','config-sha256','challenge','challenge-sha256','output'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--receipt'); parser.add_argument('--receipt-sha256'); parser.add_argument('--ordinal',type=int)
    args = parser.parse_args(argv)
    try:
        require((args.receipt is not None) == (args.action == 'project-job')
                and (args.receipt_sha256 is not None) == (args.action == 'project-job')
                and (args.ordinal is not None) == (args.action == 'project-job'), 'OWNER_OPERATION_ARGUMENTS')
        triplet = CampaignTriplet.reopen_registered(*load_config(args.config, args.config_sha256, engine=engine, catalog=catalog))
        stager = OwnerOperationStager(triplet)
        challenge, actual = read_json(args.challenge)
        require(digest(args.challenge_sha256) and actual == args.challenge_sha256, 'OWNER_OPERATION_CHALLENGE_FILE')
        if args.action == 'dispatch-intent': envelope = stager.stage_intent(challenge)
        else:
            receipt, actual = read_json(args.receipt)
            require(digest(args.receipt_sha256) and actual == args.receipt_sha256, 'OWNER_OPERATION_RECEIPT_FILE')
            envelope = stager.stage_projection(challenge, receipt, args.ordinal)
        from pathlib import Path
        require(Path(args.output).is_absolute(), 'OWNER_OPERATION_OUTPUT_PATH')
        write_new(Path(args.output), envelope)
        print(json.dumps({'operationPrepared': True, 'networkRequested': False, 'launchAuthorized': False,
                          'scientificValidation': 'NOT_VALIDATED'},sort_keys=True));return 0
    except (Exception, KeyboardInterrupt):
        print(json.dumps({'operationPrepared': False, 'evidenceMustBePreserved': True, 'implicitRetry': False,
                          'scientificValidation': 'NOT_VALIDATED'},sort_keys=True));return 2


if __name__ == '__main__': raise SystemExit(main())
