"""Nonsecret correlation files, never transferable launch authority or a lease."""
import copy

from tools.pixinsight.local_pilot.broker import require, opaque, encode
from tools.scientific_transients.queue import fields, digest
from tools.scientific_transients.confirmatory_campaign import fingerprint

HANDOFF = 'DSG_CAMPAIGN_WORKER_HANDOFF_V1'
TECHNICAL = 'DSG_CAMPAIGN_TECHNICAL_CONTEXT_V1'
COMMON = {'planRef','intentSha256','queueNamespaceSha256','contextSha256','archiveSha256','workerId','rootId'}
JOB = {'ordinal','jobId','requestId','bindingRef','bindingSha256','inputSha256'}
SELECTION = COMMON | JOB
STATES = {'QUEUED','RESERVED','RUNNING','COMPLETED','FAILED','CANCELLED','RECOVERY_REQUIRED'}


def selection_sha(value):
    value = {key: value[key] for key in SELECTION}
    require(all(opaque(value[key]) for key in ('planRef','workerId','rootId','requestId','bindingRef'))
            and all(digest(value[key]) for key in ('intentSha256','queueNamespaceSha256','contextSha256',
                                                  'archiveSha256','bindingSha256','inputSha256'))
            and type(value['ordinal']) is int and 0 <= value['ordinal'] < 3
            and value['jobId'] == 'TRN_' + value['requestId'], 'CAMPAIGN_HANDOFF_SELECTION')
    return fingerprint({'protocol': 'DSG_CAMPAIGN_REQUEST_SELECTION_V1', **value})


def make_handoff(common, jobs):
    fields(common, COMMON)
    require(type(jobs) is list and len(jobs) == 3, 'CAMPAIGN_HANDOFF_JOBS')
    value = {'protocol': HANDOFF, **copy.deepcopy(common), 'jobs': [],
             'launchAuthorized': False, 'scientificValidation': 'NOT_VALIDATED'}
    for ordinal, job in enumerate(jobs):
        fields(job, JOB); require(job['ordinal'] == ordinal, 'CAMPAIGN_HANDOFF_ORDER')
        value['jobs'].append({**copy.deepcopy(job), 'requestSelectionSha256': selection_sha({**common, **job})})
    value['handoffSha256'] = fingerprint(value)
    return validate_handoff(value)


def validate_handoff(value):
    fields(value, COMMON | {'protocol','jobs','handoffSha256','launchAuthorized','scientificValidation'})
    require(value['protocol'] == HANDOFF and value['launchAuthorized'] is False
            and value['scientificValidation'] == 'NOT_VALIDATED' and digest(value['handoffSha256'])
            and type(value['jobs']) is list and len(value['jobs']) == 3, 'CAMPAIGN_HANDOFF_PROTOCOL')
    common = {key: value[key] for key in COMMON}
    for ordinal, job in enumerate(value['jobs']):
        fields(job, JOB | {'requestSelectionSha256'})
        require(type(job['ordinal']) is int and job['ordinal'] == ordinal
                and job['requestSelectionSha256'] == selection_sha({**common, **job}), 'CAMPAIGN_HANDOFF_BINDING')
    for key in ('jobId','requestId','bindingRef','inputSha256'):
        require(len({j[key] for j in value['jobs']}) == 3, 'CAMPAIGN_HANDOFF_DUPLICATE')
    require(fingerprint({k:v for k,v in value.items() if k != 'handoffSha256'}) == value['handoffSha256']
            and len(encode(value)) <= 16384, 'CAMPAIGN_HANDOFF_HASH_OR_SIZE')
    return copy.deepcopy(value)


def validate_technical(value):
    fields(value, SELECTION | {'protocol','requestSelectionSha256','projectionState','revoked',
                              'reservationConsumed','launchAuthorized','scientificValidation'})
    require(value['protocol'] == TECHNICAL and value['requestSelectionSha256'] == selection_sha(value)
            and type(value['projectionState']) is str and value['projectionState'] in STATES
            and type(value['revoked']) is bool and type(value['reservationConsumed']) is bool
            and value['launchAuthorized'] is False and value['scientificValidation'] == 'NOT_VALIDATED',
            'CAMPAIGN_TECHNICAL_CONTEXT')
    return copy.deepcopy(value)


def compare_technical(handoff, response, ordinal):
    handoff = validate_handoff(handoff); response = validate_technical(response)
    require(type(ordinal) is int and 0 <= ordinal < 3, 'CAMPAIGN_HANDOFF_ORDER')
    expected = {key: handoff[key] for key in COMMON} | handoff['jobs'][ordinal]
    require(all(response[key] == value for key, value in expected.items()), 'CAMPAIGN_HANDOFF_REMOTE_MISMATCH')
    require(not response['revoked'] and not response['reservationConsumed']
            and response['projectionState'] == 'QUEUED', 'CAMPAIGN_HANDOFF_NOT_FRESH')
    # This comparison supplies no launch grant and cannot restore local freshness.
    return {'matched': True, 'launchAuthorized': False, 'scientificValidation': 'NOT_VALIDATED'}


def inspect_remote(handoff, transport):
    handoff = validate_handoff(handoff)
    for ordinal in range(3):
        path = '/v1/transient-analysis/worker/campaigns/' + handoff['planRef'] + '/dispatch-intents/' + \
               handoff['intentSha256'] + '/jobs/' + str(ordinal) + '/technical-context'
        compare_technical(handoff, transport.request(path), ordinal)
    return {'matchedJobs': 3, 'launchAuthorized': False, 'scientificValidation': 'NOT_VALIDATED'}
