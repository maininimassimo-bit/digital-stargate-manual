"""Private folder/prompt intake; only reviewed, registered plans enter the queue."""
import copy
import hashlib
import re
from pathlib import PureWindowsPath

from .broker import decode, encode, opaque, require
from .worker import NONLINEAR_RECIPE, NONLINEAR_RECIPES, RECIPE_MODES, actions, input_roles, expected_outputs, processing_settings, field_settings
from .source_profile import source_profile, selected_panels
from .preparation_flow import PreparationFlowMixin
from .historical_source import historical, historical_review
from tools.scientific_registry.ingestion_storage import immutable
from tools.scientific_registry.photo_ingestion import build_review


def sha(value):
    return hashlib.sha256(encode(value)).hexdigest()


def local_directory(value):
    require(isinstance(value, str) and 3 <= len(value) <= 500 and
            re.match(r'^[A-Za-z]:[\\/]', value) and
            not any(ord(c) < 32 for c in value) and
            not any(c in value[2:] for c in ':*?"<>|') and
            '..' not in PureWindowsPath(value).parts and
            not any(part.endswith((' ', '.')) for part in PureWindowsPath(value).parts[1:]),
            'LOCAL_DIRECTORY_REQUIRED')
    return value


class IntakeMixin(PreparationFlowMixin):
    def intake(self, request_id):
        require(opaque(request_id), 'INTAKE_ID')
        state, _ = self.broker._state()
        require(request_id not in state.get('withdrawnIntakes', []), 'INTAKE_WITHDRAWN')
        raw, _ = self.store.get('science/intakes/' + request_id)
        require(raw is not None, 'INTAKE_NOT_FOUND')
        return decode(raw)

    def create_intake(self, value):
        fields = {'requestId', 'masterDirectory', 'prompt', 'catalogSha256', 'sessionIds',
                  'parent', 'title', 'processingDate', 'associationConfirmed'}
        require(isinstance(value, dict) and set(value) in (fields, fields | {'sourceProfile'},
                fields | {'historicalSource'}, fields | {'sourceProfile', 'historicalSource'}) and opaque(value['requestId']), 'INTAKE_FIELDS')
        local_directory(value['masterDirectory'])
        source_profile(value)
        require(isinstance(value['prompt'], str) and 1 <= len(value['prompt'].strip()) <= 4000 and
                not any(ord(c) < 32 and c not in '\n\r\t' for c in value['prompt']), 'PROMPT_REQUIRED')
        # A replay retains the original selection even after catalog publication changes.
        existing, _ = self.store.get('science/intakes/' + value['requestId'])
        if existing:
            require(decode(existing)['selection'] == value, 'IDEMPOTENCY_CONFLICT')
        else:
            catalog = self.catalog_loader() if not historical(value) else None
            require(historical(value) or hashlib.sha256(catalog).hexdigest() == value['catalogSha256'], 'CATALOG_CHANGED_REFRESH')
            from .scientific_portal import same_target, known_target
            review = historical_review(value) if historical(value) else build_review(catalog_raw=catalog, catalog_digest=value['catalogSha256'],
                session_ids=value['sessionIds'], title=value['title'], processing_date=value['processingDate'],
                original_raw=b'XISF0100', original_media_type='application/x-xisf', preview_raw=b'\xff\xd8\xff',
                preview_media_type='image/jpeg', workflow_raw=b'', receipt_id='BKL049-P5-intake',
                imported_at=self.broker.clock().strftime('%Y-%m-%dT%H:%M:%SZ'), preview_attested=value['associationConfirmed'])
            require(known_target(review['target']), 'TARGET_NOT_IDENTIFIED')
            parent = value['parent']
            require(parent is None or (isinstance(parent, dict) and
                    set(parent) == {'imageId', 'imageVersionId', 'workflowId'}), 'PARENT_FIELDS')
            if parent:
                rows = [r for r in self.gallery_loader()['records'] if all(r.get(k) == v for k, v in parent.items())]
                require(len(rows) == 1 and same_target(rows[0]['target'], review['target']), 'PARENT_NOT_CURRENT')
            immutable(self.store, 'science/intakes/' + value['requestId'], encode({
                'selection': copy.deepcopy(value), 'createdAt': self.broker.clock().isoformat(),
                'target': review['target'], 'authority': 'PLANNING_ONLY', 'aiMode': 'SESSION_ASSISTED'}))
        def index(state, _now):
            require(value['requestId'] not in state.get('withdrawnIntakes', []), 'INTAKE_WITHDRAWN')
            rows = state.setdefault('scientificIntakes', [])
            if value['requestId'] not in rows:
                require(len(rows) < 16, 'INTAKE_CAPACITY')
                rows.append(value['requestId'])
            return {'requestId': value['requestId'], 'state': 'AWAITING_ASSISTANT_PLAN'}
        return self.broker._mutate(index)

    def intakes(self):
        state, _ = self.broker._state()
        rows = []
        for request_id in state.get('scientificIntakes', []):
            item = decode(self.store.get('science/intakes/' + request_id)[0])
            raw, _ = self.store.get('science/plans/' + request_id)
            plan = decode(raw) if raw else None
            source_raw, _ = self.store.get('science/source-plans/' + request_id)
            source_plan = decode(source_raw) if source_raw else None
            approval_raw, _ = self.store.get('science/source-approvals/' + request_id)
            source_approved = bool(source_plan and approval_raw and
                decode(approval_raw)['sourcePlanSha256'] == sha(source_plan))
            jobs = [j for j in state['jobs'] if j['jobId'] == 'PIAI_' + request_id]
            rows.append({**item, 'plan': plan, 'proposalSha256': sha(plan) if plan else None,
                         **self.preparation_state(request_id),
                         'sourcePlan':source_plan,'sourcePlanSha256':sha(source_plan) if source_plan else None,
                         'sourceSelectionApproved':source_approved,
                         'state': 'WITHDRAWN' if request_id in state.get('withdrawnIntakes', []) else
                         'JOB_CREATED' if jobs else 'PLAN_READY' if plan else 'AWAITING_ASSISTANT_PLAN'})
        return rows

    def withdraw_intake(self, request_id, value):
        require(opaque(request_id) and value == {}, 'WITHDRAWAL_FIELDS')
        require(self.store.exists('science/intakes/' + request_id), 'INTAKE_NOT_FOUND')
        def operation(state, _now):
            require(not any(j['jobId'] == 'PIAI_' + request_id for j in state['jobs']), 'JOB_ALREADY_CREATED')
            require(request_id not in state.get('preparationAuthorizedIntakes', []) and
                    not self.store.exists('science/preparation-approvals/' + request_id), 'PREPARATION_ALREADY_APPROVED')
            rows = state.setdefault('withdrawnIntakes', [])
            if request_id not in rows:
                rows.append(request_id)
            return {'requestId': request_id, 'state': 'WITHDRAWN', 'nativeStarted': False}
        return self.broker._mutate(operation)

    def propose_sources(self, request_id, value):
        intake = self.intake(request_id)
        selected_panels(intake['selection'],value)
        # A selection proposal cannot create a processing plan or queue job.
        immutable(self.store,'science/source-plans/'+request_id,encode(copy.deepcopy(value)))
        return {'requestId':request_id,'sourcePlanSha256':sha(value),'state':'SOURCE_SELECTION_REVIEW',
                'nativeStarted':False}

    def approve_sources(self, request_id, value):
        require(isinstance(value,dict) and set(value) == {'sourcePlanSha256'}, 'SOURCE_APPROVAL_FIELDS')
        intake = self.intake(request_id)
        raw,_ = self.store.get('science/source-plans/'+request_id)
        require(raw is not None, 'SOURCE_PLAN_PENDING')
        plan = decode(raw)
        require(value['sourcePlanSha256'] == sha(plan), 'SOURCE_PLAN_CHANGED')
        selected_panels(intake['selection'],plan)
        require(historical(intake['selection']) or hashlib.sha256(self.catalog_loader()).hexdigest() == intake['selection']['catalogSha256'],
                'CATALOG_CHANGED_REFRESH')
        immutable(self.store,'science/source-approvals/'+request_id,encode(value))
        return {'requestId':request_id,'state':'SOURCE_SELECTION_APPROVED','nativeStarted':False}

    def propose(self, request_id, value):
        intake = self.intake(request_id)
        profile = source_profile(intake['selection'])
        from .scientific_portal import is_m27
        prepared=profile['mode']=='OSC_CFA' or profile['layout']=='PANELS'
        preparation=self.preparation_state(request_id) if prepared else None
        require(not prepared or preparation['preparationApproved'] and preparation['preparationResult'],
                'PREPARATION_RESULT_REQUIRED')
        fields = {'workerId', 'inputRef', 'manifestSha256', 'recipe', 'background', 'processing', 'rationale', 'limitations', 'masters'}
        if prepared:fields=fields|{'preparationResultSha256'}
        require(isinstance(value, dict) and set(value) in (fields, fields | {'field'}) and value['workerId'] == self.broker.worker_id,
                'PLAN_FIELDS')
        require(opaque(value['inputRef']) and value['recipe'] in NONLINEAR_RECIPES, 'PLAN_RECIPE')
        if value['recipe'] == NONLINEAR_RECIPE:
            require(not prepared and is_m27(intake.get('target')) and profile['mode'] == 'LRGB' and 'field' not in value, 'M27_RECIPE_TARGET')
        else:
            try:
                field_settings(value.get('field'))
            except ValueError:
                require(False, 'PLAN_FIELD_SETTINGS')
            require(value['field']['target'] == intake['target'], 'PLAN_FIELD_TARGET')
            require(RECIPE_MODES[value['recipe']] == ('OSC' if profile['mode']=='OSC_CFA' else profile['mode']), 'PLAN_SOURCE_PROFILE')
        registered, _ = self.store.get('science/inputs/' + value['inputRef'])
        require(registered is not None and decode(registered)['manifestSha256'] == value['manifestSha256'] and
                decode(registered)['recipe'] == value['recipe'], 'PLAN_REGISTERED_BINDING')
        require(decode(registered).get('historicalRequestId') == (request_id if historical(intake['selection']) else None),
                'HISTORICAL_INPUT_BINDING')
        if prepared:
            require(value['preparationResultSha256']==preparation['preparationResultSha256'] and
                    decode(registered).get('preparation')=={'requestId':request_id,'resultSha256':preparation['preparationResultSha256']} and
                    value['masters']==preparation['preparationResult']['masters'],'PLAN_PREPARATION_BINDING')
        require(all(isinstance(value[k], str) and 1 <= len(value[k].strip()) <= 4000 for k in ('rationale', 'limitations')),
                'PLAN_EXPLANATION')
        background = value['background']
        require(isinstance(background, dict) and set(background) == {'polyDegree', 'boxSize', 'boxSeparation'}, 'PLAN_BACKGROUND')
        for key, low, high in [('polyDegree', 0, 2), ('boxSize', 5, 32), ('boxSeparation', 5, 64)]:
            require(type(background[key]) is int and low <= background[key] <= high, 'PLAN_BACKGROUND')
        try:
            processing_settings(value['processing'])
        except ValueError:
            require(False, 'PLAN_PROCESSING')
        masters = value['masters']
        roles = input_roles(value['recipe'])
        require(isinstance(masters, list) and len(masters) == len(roles), 'PLAN_MASTERS')
        for role, master in zip(roles, masters):
            require(isinstance(master, dict) and set(master) == {'role', 'width', 'height', 'imageIndex'} and
                    master['role'] == role and all(type(master[k]) is int for k in ('width', 'height', 'imageIndex')) and
                    1000 <= master['width'] <= 12000 and 800 <= master['height'] <= 12000 and
                    0 <= master['imageIndex'] < 16, 'PLAN_MASTERS')
        require(len({(m['width'], m['height']) for m in masters}) == 1, 'PLAN_GEOMETRY')
        plan = {**copy.deepcopy(value), 'steps': [a[1] for a in actions(value['recipe'])],
                'checkpointCount': len(expected_outputs(value['recipe'])), 'verification': 'WORKER_REPORTED_NOT_ATTESTED'}
        if prepared:
            plan['preparation']={'plan':preparation['preparationPlan'],'planSha256':preparation['preparationPlanSha256'],
                                 'result':preparation['preparationResult'],'resultSha256':preparation['preparationResultSha256']}
        immutable(self.store, 'science/plans/' + request_id, encode(plan))
        return {'requestId': request_id, 'proposalSha256': sha(plan), 'state': 'PLAN_READY'}

    def approve_plan(self, request_id, value):
        require(isinstance(value, dict) and set(value) == {'proposalSha256'}, 'PLAN_APPROVAL_FIELDS')
        intake = self.intake(request_id)
        raw, _ = self.store.get('science/plans/' + request_id)
        require(raw is not None, 'PLAN_PENDING')
        plan = decode(raw)
        require(value['proposalSha256'] == sha(plan), 'PLAN_CHANGED')
        selection = {k: v for k, v in intake['selection'].items() if k not in {'masterDirectory', 'prompt', 'sourceProfile'}}
        selection['inputRef'] = plan['inputRef']
        return self.create(selection, intent={'intake': intake, 'plan': plan, 'proposalSha256': sha(plan)})
