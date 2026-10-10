"""Opt-in planning with durable one-send reservation and exact draft binding."""
import copy
import secrets

from .broker import decode, encode, require, opaque
from .intake import sha
from .openai_planner import validate_evidence, safe_text, VERSION
from .source_profile import source_profile
from tools.scientific_registry.ingestion_storage import immutable


def api_requested(selection):
    value = selection.get('openaiPlanning')
    return isinstance(value, dict) and set(value) == {'dataTransferConfirmed'} and value['dataTransferConfirmed'] is True


class OpenAIFlowMixin:
    def openai_state(self, request_id):
        state, _ = self.broker._state()
        attempt = state.get('openaiAttempts', {}).get(request_id)
        raw, _ = self.store.get('science/openai-results/' + request_id)
        if raw:
            return decode(raw)
        return {'state': 'AI_REQUEST_RESERVED_NO_RETRY' if attempt else 'AWAITING_LOCAL_EVIDENCE'}

    def generate_openai(self, request_id, value):
        require(self.planner is not None, 'AI_PROVIDER_DISABLED')
        intake = self.intake(request_id)
        require(api_requested(intake['selection']), 'AI_DATA_TRANSFER_CONSENT_REQUIRED')
        require(isinstance(value, dict) and set(value) == {'workerId', 'evidence'} and
                value['workerId'] == self.broker.worker_id, 'AI_WORKER_BINDING')
        profile = source_profile(intake['selection'])
        prepared = profile['mode'] == 'OSC_CFA' or profile['layout'] == 'PANELS'
        prep = self.preparation_state(request_id) if prepared else None
        require(not prepared or prep['preparationApproved'] and prep['preparationResult'], 'PREPARATION_RESULT_REQUIRED')
        evidence = validate_evidence(value['evidence'], intake['target'], profile['mode'])
        require(not prepared or evidence['masters'] == prep['preparationResult']['masters'], 'AI_PREPARATION_BINDING')
        safe_text(intake['selection']['prompt'])
        safe_text(intake['target'], 160)
        binding = sha({'intake': sha(intake), 'evidence': evidence, 'method': VERSION,
                       'model': self.planner.model})
        owner = secrets.token_hex(16)

        def reserve(state, now):
            require(request_id not in state.get('withdrawnIntakes', []) and
                    not any(j['jobId'] == 'PIAI_' + request_id for j in state['jobs']), 'AI_INTAKE_INACTIVE')
            require(not self.store.exists('science/plans/' + request_id), 'AI_PLAN_ALREADY_READY')
            attempts = state.setdefault('openaiAttempts', {})
            if request_id in attempts:
                require(attempts[request_id]['bindingSha256'] == binding, 'AI_EVIDENCE_CHANGED')
                return False
            require(len(attempts) < 16, 'AI_ATTEMPT_CAPACITY')
            require(sum(a['day'] == now[:10] for a in attempts.values()) < self.planner.daily_limit, 'AI_DAILY_LIMIT_REACHED')
            attempts[request_id] = {'bindingSha256': binding, 'owner': owner, 'day': now[:10]}
            return True

        reserved = self.broker._mutate(reserve)
        if not reserved:
            return self.openai_state(request_id)
        # Commit the reservation before any paid send; crashes never release it.
        try:
            # Recheck withdrawal after the durable reservation and before sending.
            self.intake(request_id)
            output, provenance = self.planner.generate(intake['selection']['prompt'], intake['target'], evidence)
            plan = {**output, 'recipe': evidence['recipe']}
            if evidence['field'] is not None:
                plan['field'] = copy.deepcopy(evidence['field'])
            result = {'state': 'AI_DRAFT_READY', 'plan': plan, 'evidence': evidence,
                'provenance': {**provenance, 'bindingSha256': binding, 'planSha256': sha(plan),
                               'evidenceSha256': sha(evidence)}}
        except Exception:
            result = {'state': 'AI_FAILED_NO_RETRY', 'reason': 'AI_PROVIDER_FAILED_NO_RETRY'}
        immutable(self.store, 'science/openai-results/' + request_id, encode(result))
        return result

    def validate_openai_plan(self, request_id, value):
        result = self.openai_state(request_id)
        require(result['state'] == 'AI_DRAFT_READY', 'AI_DRAFT_REQUIRED')
        fields = {'recipe', 'background', 'processing', 'rationale', 'limitations'}
        if 'field' in result['plan']:
            fields.add('field')
        require(all(value.get(k) == result['plan'][k] for k in fields) and
                value.get('masters') == result['evidence']['masters'], 'AI_DRAFT_BINDING')
        return copy.deepcopy(result['provenance'])
