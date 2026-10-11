"""Native segment permits, isolated from the legacy queue.

A permit grants one local attempt, never automatic replay. Physical adapters
must preserve and verify checkpoints before their receipts can advance the
decision journal. This module performs no native or provider dispatch.
"""
import copy
import secrets

from .broker import require, decode, opaque, STAGES, TERMINAL
from .adaptive_ledger import DecisionJournal, digest
from .intake import sha

VERSION = 'DSG_PIAI_ADAPTIVE_SEGMENT_PERMIT_V2'


class SegmentPermits:
    def __init__(self, portal):
        self.portal, self.broker, self.store = portal, portal.broker, portal.store

    def _approval(self, request_id):
        state = self.portal.adaptive_state(request_id)
        approval = state['executionPolicy']
        require(approval is not None, 'ADAPTIVE_NATIVE_OWNER_APPROVAL_REQUIRED')
        require(state['plan']['decision']['action'] == 'PROPOSE_GRAPH', 'ADAPTIVE_NATIVE_GRAPH_REQUIRED')
        require(sha(state['plan']['decision']['graph']) == approval['graphSha256'], 'ADAPTIVE_NATIVE_GRAPH_CHANGED')
        return approval, state['plan']['decision']['graph']

    def reserve(self, request_id, worker_id, root_id, approval_sha, decision_result_sha):
        require(self.portal.adaptive_enabled(), 'ADAPTIVE_DISABLED')
        require(worker_id == self.broker.worker_id and opaque(root_id), 'ADAPTIVE_NATIVE_IDENTITY')
        require(digest(approval_sha) and digest(decision_result_sha), 'ADAPTIVE_NATIVE_HASHES')
        approval, graph = self._approval(request_id)
        require(sha(approval) == approval_sha, 'ADAPTIVE_NATIVE_APPROVAL_CHANGED')
        job_id = 'PIAI_' + request_id
        journal = DecisionJournal(self.broker)
        owner = secrets.token_hex(32)

        def operation(state, now):
            job = journal._live(state, job_id)
            cursor = journal._cursor(state, job_id)
            require(state['rootId'] in (None, root_id), 'ROOT_ID_MISMATCH_RECOVERY_REQUIRED')
            active = [j for j in state['jobs'] if j['state'] in (STAGES - TERMINAL) | {'RECOVERY_REQUIRED'}]
            require(len(active) <= 1, 'QUEUE_INVARIANT')
            require(not active or active[0]['jobId'] == job_id, 'ADAPTIVE_NATIVE_BUSY')
            require(job.get('adaptiveExecutionApprovalSha256') == approval_sha and
                    cursor['state'] == 'AWAITING_EXECUTION' and cursor['resultSha256'] == decision_result_sha,
                    'ADAPTIVE_NATIVE_DECISION_PHASE')
            ordinal = cursor['ordinal']
            require(ordinal < len(graph['steps']), 'ADAPTIVE_NATIVE_PREFIX_COMPLETE')
            key = str(ordinal)
            permits = job.setdefault('adaptiveSegmentPermits', {})
            if key in permits:
                require(permits[key]['decisionResultSha256'] == decision_result_sha and
                        permits[key]['approvalSha256'] == approval_sha, 'ADAPTIVE_NATIVE_PERMIT_CHANGED')
                # A lost response never grants a replacement native attempt.
                # Recovery requires a local verified receipt, not another lease.
                return {'nativeStartAllowed': False, 'ordinal': ordinal,
                        'state': permits[key]['state'], 'recovery': 'LOCAL_RECEIPT_REQUIRED'}
            if ordinal == 0:
                step = copy.deepcopy(graph['steps'][0])
            else:
                raw, _ = self.store.get('science/adaptive-checkpoint-decisions/' + job_id + '/' + key)
                require(raw is not None, 'ADAPTIVE_NEXT_STEP_DECISION_REQUIRED')
                decision = decode(raw)
                recorded = decode(self.store.get(journal._key(job_id, ordinal, 'result'))[0])
                require(decision['decisionResultSha256'] == decision_result_sha and
                        decision['decision']['action'] == 'CONTINUE' and
                        sha(decision['decision']) == recorded['decision']['decisionSha256'],
                        'ADAPTIVE_NEXT_STEP_BINDING')
                step = copy.deepcopy(decision['decision']['nextStep'])
                require(step['process'] == graph['steps'][ordinal]['process'], 'ADAPTIVE_NEXT_PROCESS_CHANGED')
                from .adaptive_catalog import validate_step
                validate_step(step)
            permit = {'version': VERSION, 'jobId': job_id, 'ordinal': ordinal,
                      'approvalSha256': approval_sha, 'decisionResultSha256': decision_result_sha,
                      'runtimeSha256': cursor['scope']['runtimeSha256'], 'graphSha256': sha(graph),
                      'parentReceiptSha256': cursor['parentReceiptSha256'], 'step': step,
                      'state': 'RESERVED', 'owner': owner}
            permits[key] = permit
            job.update(state='RESERVED', rootId=root_id, updatedAt=now)
            state.update(rootId=root_id, lastSeen=now)
            return {'nativeStartAllowed': True, 'permit': copy.deepcopy(permit)}

        return self.broker._mutate(operation)

    def start(self, request_id, worker_id, permit):
        require(self.portal.adaptive_enabled() and worker_id == self.broker.worker_id,
                'ADAPTIVE_NATIVE_IDENTITY')
        require(isinstance(permit, dict) and set(permit) == {'version','jobId','ordinal',
                'approvalSha256','decisionResultSha256','runtimeSha256','graphSha256',
                'parentReceiptSha256','step','state','owner'} and digest(permit.get('owner')) and
                permit['version'] == VERSION and permit['state'] == 'RESERVED',
                'ADAPTIVE_NATIVE_PERMIT_REQUIRED')
        job_id = 'PIAI_' + request_id
        journal = DecisionJournal(self.broker)

        def operation(state, now):
            job = journal._live(state, job_id)
            cursor = journal._cursor(state, job_id)
            require(permit['jobId'] == job_id and type(permit['ordinal']) is int and
                    cursor['ordinal'] == permit['ordinal'] and cursor['state'] == 'AWAITING_EXECUTION' and
                    cursor['resultSha256'] == permit['decisionResultSha256'] and
                    cursor['scope']['runtimeSha256'] == permit['runtimeSha256'] and
                    job.get('adaptiveExecutionApprovalSha256') == permit['approvalSha256'],
                    'ADAPTIVE_NATIVE_START_BINDING')
            current = job.get('adaptiveSegmentPermits', {}).get(str(permit['ordinal']))
            require(current is not None and current['owner'] == permit['owner'] and
                    {k:v for k,v in current.items() if k != 'state'} ==
                    {k:v for k,v in permit.items() if k != 'state'}, 'ADAPTIVE_NATIVE_PERMIT_CHANGED')
            if current['state'] == 'STARTED':
                return {'executeAllowed': False, 'recovery': 'LOCAL_RECEIPT_REQUIRED'}
            require(current['state'] == 'RESERVED' and job['state'] == 'RESERVED', 'ADAPTIVE_NATIVE_PHASE')
            current['state'] = 'STARTED'
            job.update(state='RUNNING', updatedAt=now)
            state['lastSeen'] = now
            return {'executeAllowed': True, 'ordinal': permit['ordinal']}
        return self.broker._mutate(operation)

