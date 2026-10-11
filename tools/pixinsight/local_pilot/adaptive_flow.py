"""Authenticated adaptive analysis and exact Owner graph admission.

Analysis consent grants no native execution. Only a separate exact graph approval
can admit a bounded execution policy. Physical evidence remains worker-reported.
"""
import base64
import copy
import os

from .broker import require, encode, decode
from .intake import sha
from .source_profile import source_profile
from .adaptive_ledger import DecisionJournal, VERSION, digest
from . import adaptive_catalog as catalog
from .native_measurements import validate as validate_measurement
from tools.scientific_registry.ingestion_storage import immutable

EXECUTION_POLICY_VERSION = 'DSG_PIAI_ADAPTIVE_EXECUTION_POLICY_V2'


class AdaptiveFlowMixin:
    def adaptive_enabled(self):
        return self.adaptive_provider is not None and os.environ.get('DSG_PIAI_ADAPTIVE') == 'LOCAL_WORKER_VERIFIED'

    def adaptive_state(self, request_id):
        self.intake(request_id)
        raw, _ = self.store.get('science/adaptive-plans/' + request_id)
        state, _ = self.broker._state()
        cursor = state.get('adaptiveSessions', {}).get('PIAI_' + request_id)
        public_cursor = copy.deepcopy(cursor)
        if public_cursor and public_cursor.get('pending'):
            public_cursor['pending'].pop('owner', None)
        jobs = [j for j in state['jobs'] if j['jobId'] == 'PIAI_' + request_id]
        approval = self.store.get('science/adaptive-approvals/' + request_id)[0]
        approved_policy = decode(approval) if approval else None
        if not jobs or not approved_policy or jobs[0].get('adaptiveExecutionApprovalSha256') != sha(approved_policy):
            approved_policy = None
        return {'plan': decode(raw) if raw else None,
                'proposalSha256': sha(decode(raw)) if raw else None,
                'cursor': public_cursor,
                'job': self.broker._view(jobs[0]) if jobs else None,
                'executionPolicy': approved_policy,
                'executionEvidence': 'WORKER_REPORTED_NOT_INDEPENDENTLY_ATTESTED',
                'scientificAcceptance': 'NONE', 'publication': 'NONE'}

    def generate_adaptive(self, request_id, value):
        require(self.adaptive_enabled(), 'ADAPTIVE_DISABLED')
        intake = self.intake(request_id)
        consent = intake['selection'].get('adaptivePlanning')
        require(isinstance(consent, dict) and all(consent.get(k) is True for k in
                ('dataTransferConfirmed', 'pixelStatisticsConfirmed', 'previewTransferConfirmed')),
                'ADAPTIVE_CONSENT_REQUIRED')
        fields = {'workerId', 'inputs', 'runtime', 'evidence', 'bindings', 'assetsBase64'}
        require(isinstance(value, dict) and set(value) == fields and
                value['workerId'] == self.broker.worker_id, 'ADAPTIVE_ANALYSIS_FIELDS')
        profile = source_profile(intake['selection'])
        require(profile['layout'] == 'SINGLE' and profile['mode'] in catalog.MODES,
                'ADAPTIVE_VERIFIED_PREPARATION_ADAPTER_REQUIRED')
        evidence = value['evidence']
        require(isinstance(evidence, dict) and evidence.get('mode') == profile['mode'] and
                evidence.get('intent') == intake['selection']['prompt'], 'ADAPTIVE_INTAKE_BINDING')
        roles = {'LRGB':['R','G','B','L'], 'OSC':['RGB'], 'SHO':['SII','Ha','OIII'], 'HOO':['Ha','OIII']}[profile['mode']]
        inputs = value['inputs']
        require(isinstance(inputs, list) and len(inputs) == len(roles), 'ADAPTIVE_INPUTS')
        for row, role in zip(inputs, roles):
            require(isinstance(row, dict) and set(row) == {'role', 'sha256', 'imageIndex', 'width', 'height', 'channels'} and
                    row['role'] == role and digest(row['sha256']) and type(row['imageIndex']) is int and
                    0 <= row['imageIndex'] < 16 and all(type(row[k]) is int and 32 <= row[k] <= 12000 for k in ('width','height')) and
                    type(row['channels']) is int and row['channels'] == (3 if role == 'RGB' else 1), 'ADAPTIVE_INPUT_DESCRIPTOR')
        require(len({(row['sha256'],row['imageIndex']) for row in inputs}) == len(inputs),
                'ADAPTIVE_ROLE_SOURCE_REUSED')
        input_sha = sha(inputs)
        facts = catalog.provenance(evidence.get('provenance'))
        require(facts['sourceSha256'] == input_sha, 'ADAPTIVE_INPUT_SET_BINDING')
        runtime = value['runtime']
        runtime_fields = {'version', 'coreVersion', 'executorSha256', 'measurementSha256',
                          'starDetectorSha256', 'dependenciesSha256', 'suiteSha256', 'models'}
        require(isinstance(runtime, dict) and set(runtime) == runtime_fields and
                runtime['version'] == 'DSG_PIAI_ADAPTIVE_RUNTIME_V2' and
                isinstance(runtime['coreVersion'], dict) and set(runtime['coreVersion']) ==
                {'major','minor','release','revision','build'} and
                all(type(v) is int and 0 <= v <= 1000000 for v in runtime['coreVersion'].values()) and
                all(digest(runtime[k]) for k in runtime_fields - {'version','coreVersion','models'}), 'ADAPTIVE_RUNTIME_FIELDS')
        models = runtime['models']
        require(isinstance(models, dict) and set(models) == {'BLURX','NOISEX','STARX'}, 'ADAPTIVE_RUNTIME_MODELS')
        for model in models.values():
            require(isinstance(model, dict) and set(model) == {'selectedVersion','fileSha256'} and
                    type(model['selectedVersion']) in (int,float) and 0 < model['selectedVersion'] < 100 and
                    digest(model['fileSha256']), 'ADAPTIVE_PINNED_MODEL_REQUIRED')
        require(isinstance(value['bindings'], dict) and set(value['bindings']) == set(roles) and
                isinstance(evidence.get('measurements'), list) and len(evidence['measurements']) == len(roles),
                'ADAPTIVE_LOCAL_BINDINGS')
        for row, measured in zip(inputs, evidence['measurements']):
            binding = value['bindings'][row['role']]
            require(isinstance(binding, dict) and all(binding.get(k) == row[r] for k,r in
                    (('sourceSha256','sha256'),('imageIndex','imageIndex'),('width','width'),('height','height'),('channels','channels'))) and
                    binding.get('adapterSha256') == runtime['measurementSha256'] and
                    binding.get('starDetectorSha256') == runtime['starDetectorSha256'] and
                    measured.get('role') == row['role'] and measured.get('report',{}).get('coreVersion') == runtime['coreVersion'],
                    'ADAPTIVE_PHYSICAL_REPORT_BINDING')
            try:
                validate_measurement(measured['report'], binding)
            except ValueError:
                require(False, 'ADAPTIVE_NATIVE_MEASUREMENT_INVALID')
        require(isinstance(value['assetsBase64'], list) and 1 <= len(value['assetsBase64']) <= 4,
                'ADAPTIVE_ASSETS')
        assets = []
        for asset in value['assetsBase64']:
            require(isinstance(asset,str) and len(asset) <= 1398104, 'ADAPTIVE_ASSET_LIMIT')
            try:
                raw = base64.b64decode(asset, validate=True)
            except ValueError:
                require(False, 'ADAPTIVE_ASSET_ENCODING')
            require(len(raw) <= 1048576, 'ADAPTIVE_ASSET_LIMIT')
            assets.append(raw)
        policy = {'version':VERSION, 'catalogSha256':catalog.fingerprint(), 'runtimeSha256':sha(runtime),
                  'inputSetSha256':input_sha, 'mode':profile['mode'], 'model':self.adaptive_provider.model, **consent}
        policy_sha = sha(policy)
        immutable(self.store, 'science/adaptive-policies/' + policy_sha, encode(policy))
        analysis = {'intakeSha256':sha(intake), 'inputs':inputs, 'runtime':runtime,
                    'evidence':evidence, 'bindings':value['bindings'], 'policySha256':policy_sha}
        immutable(self.store, 'science/adaptive-analysis/' + request_id, encode(analysis))
        job_id = 'PIAI_' + request_id

        def admit(state, now):
            require(request_id not in state.get('withdrawnIntakes', []), 'ADAPTIVE_WITHDRAWN')
            existing = [j for j in state['jobs'] if j['jobId'] == job_id]
            if existing:
                require(existing[0].get('adaptivePolicySha256') == policy_sha and
                        existing[0]['request'].get('aiMode') == 'OPENAI_API_ADAPTIVE', 'ADAPTIVE_JOB_CONFLICT')
                return
            require(len(state['jobs']) < 16, 'QUEUE_CAPACITY')
            state['jobs'].append({'jobId':job_id, 'request':{'requestId':request_id, 'aiMode':'OPENAI_API_ADAPTIVE'},
                'state':'QUEUED', 'cancelRequested':False, 'sequence':0, 'report':None,
                'createdAt':now, 'updatedAt':now, 'adaptivePolicySha256':policy_sha})
        self.broker._mutate(admit)
        journal = DecisionJournal(self.broker)
        journal.open(job_id, policy_sha)
        saved, _ = self.store.get('science/adaptive-plans/' + request_id)
        if saved is not None:
            result = decode(saved)
            require(result['analysisSha256'] == sha(analysis) and result['policySha256'] == policy_sha,
                    'ADAPTIVE_PLAN_BINDING')
            state, _ = self.broker._state()
            cursor = journal._cursor(state, job_id)
            if cursor['state'] == 'RESERVED':
                # Crash after immutable provider result: recover accounting from
                # that exact result without another send or a new reservation.
                request = decode(self.store.get(journal._key(job_id, 0, 'request'))[0])
                reservation = {'sendAllowed':True, 'request':request, 'owner':cursor['pending']['owner']}
                journal.record(reservation, {'action':'EXECUTE_GRAPH' if result['decision']['action'] == 'PROPOSE_GRAPH' else 'STOP_FOR_REVIEW',
                    'decisionSha256':sha(result['decision'])}, result['provider']['usage'])
            return self.adaptive_state(request_id)
        refs = {k:policy[k] for k in ('catalogSha256','runtimeSha256','inputSetSha256')}
        reservation = journal.reserve(job_id, {**refs, 'policySha256':policy_sha, 'evidenceSha256':sha(evidence)})
        if not reservation['sendAllowed']:
            return self.adaptive_state(request_id)
        # A cancellation after durable reservation must block the paid send.
        state, _ = self.broker._state()
        journal._live(state, job_id)
        try:
            decision, receipt = self.adaptive_provider.generate_initial(reservation, evidence, value['bindings'], assets,
                data_transfer_confirmed=consent['dataTransferConfirmed'],
                statistics_transfer_confirmed=consent['pixelStatisticsConfirmed'],
                preview_transfer_confirmed=consent['previewTransferConfirmed'])
        except Exception:
            # Preserve unknown usage and reservation; no paid resend on restart.
            return self.adaptive_state(request_id)
        result = {'decision':decision, 'provider':receipt, 'analysisSha256':sha(analysis), 'policySha256':policy_sha}
        immutable(self.store, 'science/adaptive-plans/' + request_id, encode(result))
        journal.record(reservation, {'action':'EXECUTE_GRAPH' if decision['action'] == 'PROPOSE_GRAPH' else 'STOP_FOR_REVIEW',
                                    'decisionSha256':sha(decision)}, receipt['usage'])
        return self.adaptive_state(request_id)

    def approve_adaptive(self, request_id, value):
        require(self.adaptive_enabled(), 'ADAPTIVE_DISABLED')
        fields = {'proposalSha256','adaptationScope','nativeExecutionConfirmed'}
        require(isinstance(value, dict) and set(value) == fields and digest(value['proposalSha256']) and
                value['adaptationScope'] == 'NEXT_STEP_PARAMETERS_ONLY' and value['nativeExecutionConfirmed'] is True,
                'ADAPTIVE_EXECUTION_APPROVAL_FIELDS')
        intake = self.intake(request_id)
        result = self.adaptive_state(request_id)
        require(result['plan'] is not None and result['proposalSha256'] == value['proposalSha256'] and
                result['plan']['decision']['action'] == 'PROPOSE_GRAPH', 'ADAPTIVE_EXACT_GRAPH_REQUIRED')
        analysis = decode(self.store.get('science/adaptive-analysis/' + request_id)[0])
        require(analysis['intakeSha256'] == sha(intake), 'ADAPTIVE_INTAKE_CHANGED')
        graph = catalog.validate_graph(result['plan']['decision']['graph'],
                                      analysis['evidence']['mode'], analysis['evidence']['provenance'])
        processes = [s['process'] for s in graph['steps']]
        require(analysis['evidence']['provenance']['domain'] != 'LINEAR_ATTESTED' or 'STRETCH' in processes,
                'ADAPTIVE_PRESENTATION_STRETCH_REQUIRED')
        require(analysis['evidence']['mode'] != 'LRGB' or 'COMBINE' in processes,
                'ADAPTIVE_LRGB_COMPOSITION_REQUIRED')
        approval = {'version':EXECUTION_POLICY_VERSION, **value, 'graphSha256':sha(graph),
                    'analysisSha256':sha(analysis), 'policySha256':analysis['policySha256'],
                    'scientificAcceptance':'NONE', 'publication':'NONE'}
        state, _ = self.broker._state()
        DecisionJournal(self.broker)._live(state, 'PIAI_' + request_id)
        immutable(self.store, 'science/adaptive-approvals/' + request_id, encode(approval))
        def approve(state, now):
            journal = DecisionJournal(self.broker)
            job = journal._live(state, 'PIAI_' + request_id)
            if job.get('adaptiveExecutionApprovalSha256') is not None:
                require(job['adaptiveExecutionApprovalSha256'] == sha(approval), 'ADAPTIVE_APPROVAL_CHANGED')
                return
            cursor = journal._cursor(state, job['jobId'])
            require(cursor['state'] == 'AWAITING_EXECUTION' and cursor['ordinal'] == 0,
                    'ADAPTIVE_APPROVAL_PHASE')
            job.update(adaptiveExecutionApprovalSha256=sha(approval), updatedAt=now)
        self.broker._mutate(approve)
        return self.adaptive_state(request_id)
