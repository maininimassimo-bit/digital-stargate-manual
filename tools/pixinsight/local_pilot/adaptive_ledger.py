"""Candidate decision journal. No HTTP routes, provider or native dispatch.

An authorized adapter must bind a job/policy before using this journal. A result
records a decision only; execution needs a separate immutable native receipt.
"""
import copy
import re
import secrets

from .broker import require, encode, decode, STAGES, TERMINAL
from .intake import sha
from tools.scientific_registry.ingestion_storage import immutable

VERSION = 'DSG_PIAI_ADAPTIVE_LEDGER_V2'
NATIVE_RECEIPT_VERSION = 'DSG_PIAI_ADAPTIVE_NATIVE_RECEIPT_V2'
MAX_DECISIONS = 16  # Finite graph/revision capacity; never a daily API quota.


def digest(value):
    return isinstance(value, str) and re.fullmatch('[a-f0-9]{64}', value) is not None


class DecisionJournal:
    def __init__(self, broker):
        self.broker, self.store = broker, broker.store

    @staticmethod
    def _cursor(state, job):
        require(isinstance(job, str) and re.fullmatch('PIAI_[a-f0-9]{32}', job), 'ADAPTIVE_JOB')
        require(job in state.get('adaptiveSessions', {}), 'ADAPTIVE_SESSION_REQUIRED')
        return state['adaptiveSessions'][job]

    def _key(self, job, ordinal, suffix):
        return 'science/adaptive/' + job + '/' + str(ordinal) + '/' + suffix

    def _live(self, state, job):
        item = self.broker._job(state, job)
        require(item.get('state') in (STAGES - TERMINAL) | {'QUEUED'} and
                item.get('cancelRequested') is False and
                job.removeprefix('PIAI_') not in state.get('withdrawnIntakes', []), 'ADAPTIVE_JOB_INACTIVE')
        return item

    def open(self, job, policy_sha):
        """Requires the job's separately recorded exact Owner policy approval."""
        require(digest(policy_sha), 'ADAPTIVE_POLICY_HASH')
        raw, _ = self.store.get('science/adaptive-policies/' + policy_sha)
        require(raw is not None and len(raw) <= 4096 and sha(decode(raw)) == policy_sha, 'ADAPTIVE_POLICY_REQUIRED')
        policy = decode(raw)
        require(isinstance(policy, dict) and set(policy) ==
                {'version', 'catalogSha256', 'runtimeSha256', 'inputSetSha256', 'mode', 'model',
                 'dataTransferConfirmed', 'pixelStatisticsConfirmed'} and policy['version'] == VERSION and
                all(digest(policy[k]) for k in ('catalogSha256', 'runtimeSha256', 'inputSetSha256')) and
                policy['mode'] in ('LRGB', 'OSC', 'SHO', 'HOO') and isinstance(policy['model'], str) and
                re.fullmatch('[a-zA-Z0-9][a-zA-Z0-9._-]{1,119}', policy['model']) and
                policy['dataTransferConfirmed'] is True and policy['pixelStatisticsConfirmed'] is True,
                'ADAPTIVE_POLICY_FIELDS')

        def operation(state, now):
            item = self._live(state, job)
            require(item.get('adaptivePolicySha256') == policy_sha and
                    item.get('request', {}).get('aiMode') == 'OPENAI_API_ADAPTIVE', 'ADAPTIVE_APPROVED_POLICY_REQUIRED')
            sessions = state.setdefault('adaptiveSessions', {})
            if job in sessions:
                require(sessions[job]['policySha256'] == policy_sha, 'ADAPTIVE_POLICY_CHANGED')
                return copy.deepcopy(sessions[job])
            require(len(sessions) < 16, 'ADAPTIVE_SESSION_CAPACITY')
            sessions[job] = {'version': VERSION, 'policySha256': policy_sha, 'ordinal': 0,
                             'scope': {k: policy[k] for k in ('catalogSha256', 'runtimeSha256', 'inputSetSha256', 'mode', 'model')},
                             'state': 'AWAITING_DECISION', 'parentReceiptSha256': None,
                             'pending': None, 'resultSha256': None,
                             'usage': {'input_tokens': 0, 'output_tokens': 0, 'total_tokens': 0},
                             'usageComplete': True}
            return copy.deepcopy(sessions[job])

        return self.broker._mutate(operation)

    def reserve(self, job, references):
        """Server allocates ordinal; reservation never expires into a new send."""
        keys = {'policySha256', 'catalogSha256', 'runtimeSha256', 'inputSetSha256', 'evidenceSha256'}
        require(isinstance(references, dict) and set(references) == keys and
                all(digest(v) for v in references.values()), 'ADAPTIVE_REFERENCES')
        state, _ = self.broker._state()
        self._live(state, job)
        cursor = self._cursor(state, job)
        require(cursor['state'] in {'AWAITING_DECISION', 'RESERVED'}, 'ADAPTIVE_PHASE_CLOSED')
        ordinal = cursor['ordinal']
        require(ordinal < MAX_DECISIONS and references['policySha256'] == cursor['policySha256'], 'ADAPTIVE_POLICY_OR_CAPACITY')
        require(all(references[k] == cursor['scope'][k] for k in ('catalogSha256', 'runtimeSha256', 'inputSetSha256')),
                'ADAPTIVE_IMMUTABLE_SCOPE')
        request = {'version': VERSION, 'jobId': job, 'ordinal': ordinal,
                   'parentReceiptSha256': cursor['parentReceiptSha256'], **references}
        request_sha = sha(request)
        # Immutable publication precedes CAS; a competing different request fails
        # closed. No assumption of an atomic transaction across objects.
        immutable(self.store, self._key(job, ordinal, 'request'), encode(request))
        owner = secrets.token_hex(16)

        def operation(state, now):
            self._live(state, job)
            current = self._cursor(state, job)
            require(current['ordinal'] == ordinal and current['parentReceiptSha256'] == request['parentReceiptSha256'],
                    'ADAPTIVE_CURSOR_CHANGED')
            if current['pending'] is not None:
                require(current['pending']['requestSha256'] == request_sha, 'ADAPTIVE_EVIDENCE_CHANGED')
                return {'sendAllowed': False, 'request': request}
            require(current['state'] == 'AWAITING_DECISION', 'ADAPTIVE_PHASE_CLOSED')
            current['pending'] = {'requestSha256': request_sha, 'owner': owner}
            current['state'] = 'RESERVED'
            current['usageComplete'] = False
            return {'sendAllowed': True, 'request': request, 'owner': owner}

        return self.broker._mutate(operation)

    def record(self, reservation, decision, usage):
        """Only the winning reservation can publish an already validated result."""
        require(isinstance(reservation, dict) and set(reservation) == {'sendAllowed', 'request', 'owner'} and
                reservation['sendAllowed'] is True, 'ADAPTIVE_RESERVATION_REQUIRED')
        request = reservation['request']
        job, ordinal = request['jobId'], request['ordinal']
        state, _ = self.broker._state()
        cursor = self._cursor(state, job)
        require(cursor['ordinal'] == ordinal and cursor['state'] == 'RESERVED' and
                cursor['pending'] == {'requestSha256': sha(request), 'owner': reservation['owner']}, 'ADAPTIVE_RESERVATION_BINDING')
        require(isinstance(decision, dict) and set(decision) == {'action', 'decisionSha256'} and
                decision['action'] in ('EXECUTE_GRAPH', 'CONTINUE', 'STOP_FOR_REVIEW') and
                digest(decision['decisionSha256']), 'ADAPTIVE_RESULT_REFERENCE')
        require(decision['action'] != 'EXECUTE_GRAPH' or ordinal == 0, 'ADAPTIVE_INITIAL_ONLY')
        require(decision['action'] != 'CONTINUE' or ordinal > 0, 'ADAPTIVE_CHECKPOINT_ONLY')
        require(isinstance(usage, dict) and set(usage) == {'input_tokens', 'output_tokens', 'total_tokens'} and
                all(type(v) is int and 0 <= v <= 10**9 for v in usage.values()) and
                usage['total_tokens'] == usage['input_tokens'] + usage['output_tokens'], 'ADAPTIVE_USAGE')
        result = {'requestSha256': sha(request), 'decision': copy.deepcopy(decision), 'usage': copy.deepcopy(usage)}
        immutable(self.store, self._key(job, ordinal, 'result'), encode(result))
        return self.reconcile(job)

    def reconcile(self, job):
        """Crash after result publication recovers it without another paid send."""
        def operation(state, now):
            cursor = self._cursor(state, job)
            if cursor['state'] != 'RESERVED':
                return copy.deepcopy(cursor)
            raw, _ = self.store.get(self._key(job, cursor['ordinal'], 'result'))
            if raw is None:
                # A lost provider response can have a real cost; it is unknown,
                # never replaced by zero and never advances the ordinal.
                return copy.deepcopy(cursor)
            result = decode(raw)
            require(result['requestSha256'] == cursor['pending']['requestSha256'], 'ADAPTIVE_RESULT_BINDING')
            cursor['resultSha256'] = sha(result)
            for key in cursor['usage']:
                cursor['usage'][key] += result['usage'][key]
            cursor['usageComplete'] = True
            cursor['state'] = 'STOP_FOR_REVIEW' if result['decision']['action'] == 'STOP_FOR_REVIEW' else 'AWAITING_EXECUTION'
            return copy.deepcopy(cursor)

        return self.broker._mutate(operation)

    def checkpoint(self, job, receipt_sha, decision_result_sha):
        """Caller must first validate and publish the distinct native receipt."""
        require(digest(receipt_sha) and digest(decision_result_sha), 'ADAPTIVE_EXECUTION_HASH')
        raw, _ = self.store.get('science/adaptive-native/' + receipt_sha)
        require(raw is not None and sha(decode(raw)) == receipt_sha, 'ADAPTIVE_NATIVE_RECEIPT_REQUIRED')
        receipt = decode(raw)
        require(isinstance(receipt, dict) and set(receipt) ==
                {'version', 'jobId', 'ordinal', 'decisionResultSha256', 'runtimeSha256', 'checkpointSha256', 'historySha256', 'status'} and
                receipt['version'] == NATIVE_RECEIPT_VERSION and
                receipt['jobId'] == job and receipt['status'] == 'CHECKPOINT_VERIFIED' and
                type(receipt['ordinal']) is int and receipt['decisionResultSha256'] == decision_result_sha and
                all(digest(receipt[k]) for k in ('runtimeSha256', 'checkpointSha256', 'historySha256')), 'ADAPTIVE_NATIVE_RECEIPT_FIELDS')

        def operation(state, now):
            self._live(state, job)
            cursor = self._cursor(state, job)
            require(cursor['state'] == 'AWAITING_EXECUTION' and cursor['resultSha256'] == decision_result_sha and
                    cursor['ordinal'] == receipt['ordinal'], 'ADAPTIVE_EXECUTION_BINDING')
            request_raw, _ = self.store.get(self._key(job, cursor['ordinal'], 'request'))
            require(decode(request_raw)['runtimeSha256'] == receipt['runtimeSha256'], 'ADAPTIVE_NATIVE_RUNTIME_BINDING')
            cursor['parentReceiptSha256'] = receipt_sha
            cursor['ordinal'] += 1
            cursor['pending'] = None
            cursor['resultSha256'] = None
            cursor['state'] = 'AWAITING_DECISION' if cursor['ordinal'] < MAX_DECISIONS else 'STOP_FOR_REVIEW'
            return copy.deepcopy(cursor)

        return self.broker._mutate(operation)
