"""Private, one-shot campaign dispatch; no credential loading or native launch.

Every uncertain mutation stays consumed. Reads never reconstruct a reservation
or authorize replay. Local receipts contain correlation evidence, never leases.
"""
import copy
import re

from tools.pixinsight.local_pilot.broker import require, opaque, ProtocolError
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.queue import fields, digest, BINDING_FIELDS
from tools.scientific_transients.receipt_coordinator import TransientTransport
from tools.scientific_transients.reservation_intent import validate_fresh_job

PROTOCOL = 'DSG_CAMPAIGN_RESERVATION_V1'
BASE = '/v1/transient-analysis/worker/campaigns/'
RESERVE = '/v1/transient-analysis/worker/reserve'


class CampaignWorkerTransport(TransientTransport):
    """Existing bounded TLS transport with exactly two additional Worker POSTs."""
    def request(self, path, value=None):
        if path.startswith(BASE):
            require(re.fullmatch(BASE + r'[a-f0-9]{32}/(?:frame-closures|dispatch-intents/'
                    r'[a-f0-9]{64}/jobs/[0-2]/reserve-once)', path) is not None
                    and value is not None, 'CAMPAIGN_WORKER_ROUTE')
            return self._exchange(path, value, is_read=False)
        return super().request(path, value)


class CampaignReservationAdapter:
    @classmethod
    def prepare(cls, root, transport, plan_ref, intent_sha, ordinal, decision_id,
                request, binding, manifest_sha, operation_ref):
        fields(request, {'workerId','rootId','jobId','bindingRef','reservationRef'})
        fields(binding, BINDING_FIELDS)
        require(all(opaque(v) for v in binding.values()) and all(opaque(request[k]) for k in
                ('workerId','rootId','bindingRef','reservationRef')) and opaque(plan_ref)
                and opaque(decision_id) and opaque(operation_ref) and digest(intent_sha)
                and digest(manifest_sha) and type(ordinal) is int and 0 <= ordinal < 3
                and type(request['jobId']) is str and request['jobId'].startswith('TRN_')
                and opaque(request['jobId'][4:]) and request['bindingRef'] == binding['bindingRef'],
                'CAMPAIGN_ADAPTER_SELECTION')
        root = safe_path(root); require(root.is_dir(), 'CAMPAIGN_ADAPTER_ROOT')
        directory = root / request['reservationRef']; directory.mkdir()
        selection = {'protocol': PROTOCOL, 'planRef': plan_ref, 'intentSha256': intent_sha,
                     'ordinal': ordinal, 'decisionId': decision_id, 'reservation': copy.deepcopy(request),
                     'binding': copy.deepcopy(binding), 'manifestSha256': manifest_sha,
                     'operationRef': operation_ref, 'implicitReplay': False}
        selection_sha = write_new(directory / 'selection.json', selection)
        result = cls.__new__(cls)
        result.directory, result.transport = directory, transport
        result.selection, result.selection_sha = selection, selection_sha
        result.phase, result.mapping_sha = 'PREPARED', None
        return result

    def _verify(self):
        value, sha = read_json(self.directory / 'selection.json')
        require(value == self.selection and sha == self.selection_sha, 'CAMPAIGN_ADAPTER_CHANGED')
        if self.mapping_sha is not None:
            require(read_json(self.directory / 'admission.json')[1] == self.mapping_sha,
                    'CAMPAIGN_ADAPTER_MAPPING_CHANGED')

    def _freeze(self):
        self.phase = 'RECONCILIATION_REQUIRED'
        try:
            write_new(self.directory / 'unconfirmed.json', {'state': self.phase,
                      'nativeLaunchRequested': False, 'implicitReplay': False, 'leasePersisted': False})
        except (OSError, ProtocolError):
            pass

    def request(self, path, value=None):
        s = self.selection
        if path == RESERVE:
            require(self.phase == 'PREPARED' and value == s['reservation'], 'CAMPAIGN_ADAPTER_REPLAY_OR_SELECTION')
            self.phase = 'DISPATCHING'
            try:
                self._verify()
                body = {'protocol': PROTOCOL, 'decisionId': s['decisionId'], 'reservation': copy.deepcopy(value)}
                write_new(self.directory / 'dispatch-intent.json',
                          {'selectionSha256': self.selection_sha, 'request': body, 'implicitRetry': False})
                remote = BASE + s['planRef'] + '/dispatch-intents/' + s['intentSha256'] + '/jobs/' + str(s['ordinal']) + '/reserve-once'
                response = self.transport.request(remote, body)
                fields(response, {'protocol','disposition','admissionSha256','job'})
                require(response['protocol'] == PROTOCOL, 'CAMPAIGN_ADAPTER_PROTOCOL')
                if response['disposition'] == 'RECONCILIATION_REQUIRED':
                    require(response['admissionSha256'] is None and response['job'] is None,
                            'CAMPAIGN_ADAPTER_EXISTING_LEASE')
                    self._freeze()
                    return {'disposition': 'RECONCILIATION_REQUIRED', 'job': None}
                require(response['disposition'] == 'CREATED' and digest(response['admissionSha256']),
                        'CAMPAIGN_ADAPTER_ADMISSION')
                job = response['job']; validate_fresh_job(job, value, s['binding'])
                mapping = {'protocol': 'DSG_CAMPAIGN_ADMISSION_MAPPING_V1',
                           'selectionSha256': self.selection_sha, 'planRef': s['planRef'],
                           'intentSha256': s['intentSha256'], 'ordinal': s['ordinal'],
                           'admissionSha256': response['admissionSha256'], 'jobId': job['jobId'],
                           'attemptId': job['attemptId'], 'rootId': job['rootId'],
                           'binding': copy.deepcopy(job['binding']), 'manifestSha256': s['manifestSha256'],
                           'reservationRef': value['reservationRef'], 'leasePersisted': False,
                           'nativeLaunchRequested': False, 'scientificValidation': 'NOT_VALIDATED'}
                self.mapping_sha = write_new(self.directory / 'admission.json', mapping)
                self.phase = 'RESERVED'
                return {'disposition': 'CREATED', 'job': copy.deepcopy(job)}
            except BaseException:
                self._freeze()
                raise ProtocolError('CAMPAIGN_ADAPTER_UNCONFIRMED_NO_REPLAY') from None
        self._verify()
        require(self.phase == 'RESERVED' and value is None and path ==
                '/v1/transient-analysis/worker/jobs/' + s['reservation']['jobId'], 'CAMPAIGN_ADAPTER_ROUTE')
        return self.transport.request(path)

    def post(self, path, value):
        self._verify()
        require(self.phase == 'RESERVED' and path == '/v1/transient-analysis/worker/jobs/' +
                self.selection['reservation']['jobId'] + '/report', 'CAMPAIGN_ADAPTER_ROUTE')
        return self.transport.post(path, value)

    def mapping(self):
        self._verify()
        require(self.phase == 'RESERVED' and self.mapping_sha is not None, 'CAMPAIGN_ADAPTER_NO_MAPPING')
        return read_json(self.directory / 'admission.json')[0]


class CampaignOwnerOperations:
    """Durable Owner mutations through an explicitly supplied Owner transport.

    The transport must supply its own Owner authentication. This class neither
    loads credentials nor treats a Worker credential as Owner authority.
    """
    def __init__(self, root, transport, plan_ref):
        require(opaque(plan_ref), 'CAMPAIGN_OWNER_PLAN')
        self.root = safe_path(root); require(self.root.is_dir(), 'CAMPAIGN_OWNER_ROOT')
        self.transport, self.plan_ref = transport, plan_ref

    def _post(self, operation_ref, suffix, body, validate):
        require(opaque(operation_ref), 'CAMPAIGN_OWNER_OPERATION')
        directory = self.root / operation_ref; directory.mkdir()
        try:
            path = '/v1/transient-analysis/campaigns/' + self.plan_ref + suffix
            sha = write_new(directory / 'intent.json', {'path': path, 'request': body, 'implicitRetry': False})
            response = self.transport.request(path, copy.deepcopy(body))
            receipt = validate(response)
            write_new(directory / 'acknowledged.json', {'intentSha256': sha, 'receipt': receipt,
                      'implicitReplay': False, 'nativeLaunchRequested': False})
            return response
        except BaseException:
            try: write_new(directory / 'unconfirmed.json', {'implicitReplay': False, 'state': 'RECONCILIATION_REQUIRED'})
            except (OSError, ProtocolError): pass
            raise ProtocolError('CAMPAIGN_OWNER_UNCONFIRMED_NO_REPLAY') from None

    def prepare_intent(self, operation_ref, request):
        fields(request, {'decisionId','contextSha256','witnessRef','jobs','workerId','rootId','archiveSha256'})
        require(all(opaque(request[k]) for k in ('decisionId','witnessRef','workerId','rootId'))
                and digest(request['contextSha256']) and digest(request['archiveSha256'])
                and type(request['jobs']) is list and len(request['jobs']) == 3, 'CAMPAIGN_OWNER_INTENT')
        for item in request['jobs']:
            fields(item, {'requestId','binding'}); fields(item['binding'], BINDING_FIELDS)
            require(opaque(item['requestId']) and all(opaque(v) for v in item['binding'].values()), 'CAMPAIGN_OWNER_BINDING')
        body = copy.deepcopy(request)
        def validate(response):
            remote = copy.deepcopy(response['request'])
            namespace = remote.pop('queueNamespaceSha256', None)
            require(remote == body and digest(namespace) and digest(response['sha256'])
                    and response['kind'] == 'DISPATCH_INTENT', 'CAMPAIGN_OWNER_ACK')
            return {'intentSha256': response['sha256'], 'queueNamespaceSha256': namespace}
        return self._post(operation_ref, '/dispatch-intents', body, validate)

    def project(self, operation_ref, intent_sha, ordinal, request_id, binding):
        fields(binding, BINDING_FIELDS)
        require(digest(intent_sha) and type(ordinal) is int and 0 <= ordinal < 3
                and opaque(request_id) and all(opaque(v) for v in binding.values()), 'CAMPAIGN_OWNER_PROJECTION')
        def validate(job):
            require(job['jobId'] == 'TRN_' + request_id and job['binding'] == binding
                    and job['request'] == {'requestId': request_id, 'bindingRef': binding['bindingRef']}
                    and 'leaseToken' not in job and job['state'] == 'QUEUED', 'CAMPAIGN_OWNER_ACK')
            return {'jobId': job['jobId'], 'bindingRef': binding['bindingRef']}
        return self._post(operation_ref, '/dispatch-intents/' + intent_sha + '/jobs/' + str(ordinal) + '/project', {}, validate)
