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
                and not hasattr(queue, '_campaign_guard'), 'CAMPAIGN_QUEUE_COMPOSITION')
        self.campaigns, self.queue = campaigns, queue
        self.namespace_sha = fingerprint({'campaignKey': campaigns.key, 'queueKey': queue.state_key,
                                         'workerId': queue.worker_id, 'ownerRef': campaigns.owner_ref})
        self._guard = object()
        queue._campaign_guard = self._guard

    def _intent(self, plan_ref, intent_sha, ordinal):
        require(opaque(plan_ref) and digest(intent_sha) and type(ordinal) is int and 0 <= ordinal < 3,
                'CAMPAIGN_QUEUE_SELECTION')
        receipt = self.campaigns.dispatch_receipt(plan_ref, intent_sha)
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
            'workerId': request['workerId'], 'rootId': request['rootId']})
        if admitted['disposition'] != 'CREATED':
            require(admitted == {'disposition': 'RECONCILIATION_REQUIRED', 'admission': None},
                    'CAMPAIGN_QUEUE_ADMISSION_RESPONSE')
            return {'disposition': 'RECONCILIATION_REQUIRED', 'job': None}
        admission = admitted['admission']
        require(admission['facts']['jobId'] == request['jobId']
                and admission['facts']['binding'] == selected['binding']
                and admission['facts']['inputSha256'] == origin['inputSha256'],
                'CAMPAIGN_QUEUE_ADMISSION_BINDING')
        # If this call fails or its acknowledgement is lost, the admission is
        # already consumed and remains in flight. No rollback or resend here.
        return self.queue._reserve_campaign_once(copy.deepcopy(request), origin, admission['sha256'],
                                                 guard=self._guard)
