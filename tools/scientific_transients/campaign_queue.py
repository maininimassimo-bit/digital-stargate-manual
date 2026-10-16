"""Trusted campaign-to-queue composition; no HTTP, credentials or native launch.

Campaign admission and queue lease emission are separate CAS operations. A gap,
failed queue write or lost acknowledgement preserves the campaign fence. This
adapter cannot turn a read receipt into a new admission or recover an old lease.
"""
import copy

from tools.pixinsight.local_pilot.broker import require, opaque
from tools.scientific_transients.confirmatory_campaign import ConfirmatoryCampaigns, fingerprint
from tools.scientific_transients.queue import TransientQueue, CAMPAIGN_PROFILE, fields, digest


class CampaignQueue:
    def __init__(self, campaigns, queue):
        require(type(campaigns) is ConfirmatoryCampaigns and type(queue) is TransientQueue
                and campaigns.worker_id == queue.worker_id and campaigns.store is queue.store
                and queue.capacity_profile == CAMPAIGN_PROFILE
                and not hasattr(queue, '_campaign_guard') and not hasattr(campaigns, '_queue_guard'),
                'CAMPAIGN_QUEUE_COMPOSITION')
        self.campaigns, self.queue = campaigns, queue
        self.namespace_sha = fingerprint({'campaignKey': campaigns.key, 'queueKey': queue.state_key,
                                         'workerId': queue.worker_id, 'ownerRef': campaigns.owner_ref})
        self._guard = object()
        queue._campaign_guard = self._guard
        campaigns._queue_guard = self._guard
        campaigns._queue_namespace_sha = self.namespace_sha
        campaigns._queue_job_reader = queue.status
        campaigns.job_reader = queue.status

    def _assert_composition(self):
        require(self.campaigns.store is self.queue.store
                and self.campaigns.job_reader == self.queue.status == self.campaigns._queue_job_reader
                and self._guard is self.queue._campaign_guard is self.campaigns._queue_guard
                and self.namespace_sha == self.campaigns._queue_namespace_sha == fingerprint({
                    'campaignKey': self.campaigns.key, 'queueKey': self.queue.state_key,
                    'workerId': self.queue.worker_id, 'ownerRef': self.campaigns.owner_ref}),
                'CAMPAIGN_QUEUE_COMPOSITION_CHANGED')

    def prepare_dispatch(self, plan_ref, request):
        """Owner port injecting the configured namespace, never a browser hash."""
        self._assert_composition()
        return self.campaigns.prepare_dispatch(plan_ref, request, queue_guard=self._guard)

    def _bound_intent(self, plan_ref, intent_sha, ordinal):
        self._assert_composition()
        require(opaque(plan_ref) and digest(intent_sha) and type(ordinal) is int and 0 <= ordinal < 3,
                'CAMPAIGN_QUEUE_SELECTION')
        receipt = self.campaigns.dispatch_receipt(plan_ref, intent_sha)
        require(receipt['queueNamespaceSha256'] == self.namespace_sha
                and receipt['intent']['request'].get('queueNamespaceSha256') == self.namespace_sha,
                'CAMPAIGN_QUEUE_NAMESPACE_MISMATCH')
        return receipt

    def _intent(self, plan_ref, intent_sha, ordinal):
        receipt = self._bound_intent(plan_ref, intent_sha, ordinal)
        require(not receipt['revoked'], 'CAMPAIGN_QUEUE_REVOKED')
        intent = receipt['intent']; context = intent['facts']['context']
        current = self.campaigns.dispatch_context(plan_ref, intent['request']['witnessRef'])
        require(current == context and context['planRef'] == plan_ref
                and intent['request']['workerId'] == self.queue.worker_id,
                'CAMPAIGN_QUEUE_CONTEXT_CHANGED')
        return intent, context

    def _origin(self, intent, context, ordinal):
        value = {'protocol': 'DSG_CAMPAIGN_JOB_ORIGIN_V1', 'namespaceSha256': self.namespace_sha,
                 'planRef': context['planRef'], 'planSha256': context['planSha256'],
                 'freezeEventSha256': context['freezeEventSha256'], 'contextSha256': context['contextSha256'],
                 'intentSha256': intent['sha256'], 'witnessRef': context['witnessRef'],
                 'witnessSha256': context['witnessSha256'], 'ordinal': ordinal,
                 'inputSha256': context['frames'][ordinal]['sha256'],
                 'algorithmSha256': context['algorithmSha256'], 'contractSha256': context['contractSha256'],
                 'bindingSha256': fingerprint(intent['request']['jobs'][ordinal]['binding']),
                 'workerId': self.queue.worker_id, 'rootId': intent['request']['rootId']}
        return value

    def project(self, plan_ref, intent_sha, ordinal):
        """Owner-authorized intent projection, outside any campaign CAS callback.

        Exact repeats are lease-free metadata receipts only; local durable
        submission code must still refuse retries after an uncertain POST.
        """
        intent, context = self._intent(plan_ref, intent_sha, ordinal)
        selected = intent['request']['jobs'][ordinal]
        request = {'requestId': selected['requestId'], 'bindingRef': selected['binding']['bindingRef']}
        return self.queue._create_campaign(request, selected['binding'], self._origin(intent, context, ordinal),
                                           guard=self._guard)

    def admit_and_reserve(self, plan_ref, intent_sha, ordinal, request, decision_id):
        response = self.reserve_envelope(plan_ref, intent_sha, ordinal, request, decision_id)
        return {'disposition': response['disposition'], 'job': response['job']}

    def reserve_envelope(self, plan_ref, intent_sha, ordinal, request, decision_id):
        """Worker technical port consuming a fresh admission, then one queue lease.

        The future authenticated boundary must supply this exact request after
        durable local intent. Never call generic claim/reserve as a fallback.
        """
        fields(request, {'workerId', 'rootId', 'jobId', 'bindingRef', 'reservationRef'})
        require(opaque(decision_id) and all(opaque(request[k]) for k in
                ('workerId', 'rootId', 'bindingRef', 'reservationRef')), 'CAMPAIGN_QUEUE_RESERVATION')
        intent, context = self._intent(plan_ref, intent_sha, ordinal)
        selected = intent['request']['jobs'][ordinal]
        origin = self._origin(intent, context, ordinal)
        require(request['jobId'] == 'TRN_' + selected['requestId']
                and request['bindingRef'] == selected['binding']['bindingRef']
                and request['workerId'] == origin['workerId'] and request['rootId'] == origin['rootId'],
                'CAMPAIGN_QUEUE_RESERVATION_BINDING')
        before = self.queue._campaign_snapshot(request['jobId'], guard=self._guard)
        require(before['campaignOrigin'] == origin and before['binding'] == selected['binding']
                and before['request'] == {'requestId': selected['requestId'], 'bindingRef': request['bindingRef']},
                'CAMPAIGN_QUEUE_ORIGIN_MISMATCH')
        admitted = self.campaigns.admit_frame(plan_ref, {
            'decisionId': decision_id, 'dispatchIntentSha256': intent_sha, 'ordinal': ordinal,
            'workerId': request['workerId'], 'rootId': request['rootId']}, queue_guard=self._guard)
        if admitted['disposition'] != 'CREATED':
            require(admitted == {'disposition': 'RECONCILIATION_REQUIRED', 'admission': None},
                    'CAMPAIGN_QUEUE_ADMISSION_RESPONSE')
            return {'protocol': 'DSG_CAMPAIGN_RESERVATION_V1',
                    'disposition': 'RECONCILIATION_REQUIRED', 'admissionSha256': None, 'job': None}
        admission = admitted['admission']
        require(admission['facts']['jobId'] == request['jobId']
                and admission['facts']['binding'] == selected['binding']
                and admission['facts']['inputSha256'] == origin['inputSha256'],
                'CAMPAIGN_QUEUE_ADMISSION_BINDING')
        # If this call fails or its acknowledgement is lost, the admission is
        # already consumed and remains in flight. No rollback or resend here.
        response = self.queue._reserve_campaign_once(copy.deepcopy(request), origin, admission['sha256'],
                                                     guard=self._guard)
        require(response['disposition'] == 'CREATED' and response['job'] is not None,
                'CAMPAIGN_QUEUE_FRESH_RESERVATION_REQUIRED')
        return {'protocol': 'DSG_CAMPAIGN_RESERVATION_V1', 'disposition': 'CREATED',
                'admissionSha256': admission['sha256'], 'job': response['job']}

    def dispatch_receipt(self, plan_ref, intent_sha):
        return self._bound_intent(plan_ref, intent_sha, 0)

    def close_frame(self, plan_ref, request):
        self._assert_composition()
        return self.campaigns.close_frame(plan_ref, request, queue_guard=self._guard)

    def _unreserved_snapshot(self, plan_ref, intent_sha, ordinal):
        receipt = self._bound_intent(plan_ref, intent_sha, ordinal)
        intent = receipt['intent']; context = intent['facts']['context']
        admissions = [e for e in receipt['admissions'] if e['request']['ordinal'] == ordinal]
        require(len(admissions) == 1, 'CAMPAIGN_QUEUE_UNRESERVED_ADMISSION')
        admission = admissions[0]
        snapshot = self.queue._campaign_fenced_snapshot(admission['facts']['jobId'], guard=self._guard)
        selected = intent['request']['jobs'][ordinal]
        require(snapshot['campaignOrigin'] == self._origin(intent, context, ordinal)
                and snapshot['binding'] == selected['binding'] == admission['facts']['binding']
                and admission['facts']['queueNamespaceSha256'] == self.namespace_sha,
                'CAMPAIGN_QUEUE_UNRESERVED_ORIGIN')
        return snapshot, admission

    def unreserved_context(self, plan_ref, intent_sha, ordinal):
        """Owner read of exact stable barrier identity; never returns a lease."""
        snapshot, admission = self._unreserved_snapshot(plan_ref, intent_sha, ordinal)
        return {'admissionSha256': admission['sha256'], 'jobId': snapshot['jobId'],
                'fenceSnapshotSha256': fingerprint(snapshot), 'queueNamespaceSha256': self.namespace_sha}

    def close_unreserved(self, plan_ref, intent_sha, ordinal, request):
        """Owner-only technical cleanup; no queue cancellation or resend here."""
        fields(request, {'decisionId', 'admissionSha256', 'jobId', 'fenceSnapshotSha256',
                         'cancellationEvidenceSha256'})
        snapshot, admission = self._unreserved_snapshot(plan_ref, intent_sha, ordinal)
        require(request.get('admissionSha256') == admission['sha256'], 'CAMPAIGN_QUEUE_UNRESERVED_ADMISSION')
        return self.campaigns._close_unreserved(plan_ref, request, snapshot, queue_guard=self._guard)
