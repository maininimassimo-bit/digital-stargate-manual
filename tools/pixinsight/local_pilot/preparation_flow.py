"""Owner-approved local preparation phase, separate from nonlinear queue approval."""
import copy
import hashlib
import re
from pathlib import Path

from .broker import decode, encode, opaque, require
from .source_profile import MODES, source_profile, selected_panels
from .preparation import validate, specification
from tools.scientific_registry.ingestion_storage import immutable


def sha(value):
    return hashlib.sha256(encode(value)).hexdigest()


def source_digest(request):
    return sha({k:request[k] for k in ('mode','layout','bayerPattern','canvas','shrink','feather')} |
               {'inputs':[{k:v for k,v in row.items() if k!='path'} for row in request['inputs']]})


def output_digest(inputs):
    return sha([{k:v for k,v in row.items() if k!='path'} for row in inputs])


def effective_selection(intake):
    selection=intake['selection']
    if source_profile(selection)['layout']=='PANELS':
        require(intake.get('sourceSelectionApproved') is True,'SOURCE_SELECTION_APPROVAL_REQUIRED')
        return selected_panels(selection,intake['sourcePlan'])
    return selection,None


def validate_plan(intake, plan, worker_id):
    fields={'workerId','sourceManifestSha256','sourcePlanSha256','mode','layout','bayerPattern',
            'canvas','shrink','feather','masters','rationale','limitations'}
    require(isinstance(plan,dict) and set(plan)==fields and plan['workerId']==worker_id,'PREPARATION_PLAN_FIELDS')
    selection,mappings=effective_selection(intake);profile=source_profile(selection)
    require(profile['layout']=='PANELS' or profile['mode']=='OSC_CFA','PREPARATION_NOT_REQUIRED')
    require(all(plan[k]==profile[k] for k in ('mode','layout','bayerPattern')),'PREPARATION_PROFILE_BINDING')
    expected_source_sha=sha(intake['sourcePlan']) if profile['layout']=='PANELS' else None
    require(plan['sourcePlanSha256']==expected_source_sha,'PREPARATION_SOURCE_SELECTION_BINDING')
    require(isinstance(plan['sourceManifestSha256'],str) and re.fullmatch(r'[a-f0-9]{64}',plan['sourceManifestSha256']),'PREPARATION_SOURCE_DIGEST')
    require(all(isinstance(plan[k],str) and 1<=len(plan[k].strip())<=4000 for k in ('rationale','limitations')),'PREPARATION_EXPLANATION')
    panels=[p['panelId'] for p in profile['panels']] if profile['layout']=='PANELS' else ['P1']
    require(isinstance(plan['masters'],list) and len(plan['masters'])==len(panels)*len(MODES[profile['mode']]),'PREPARATION_MASTER_COUNT')
    inputs=[]
    for row in plan['masters']:
        require(isinstance(row,dict) and set(row)=={'panelId','role','imageIndex','width','height','filename'} and
                isinstance(row['filename'],str) and 1<=len(row['filename'])<=255 and row['filename'].lower().endswith('.xisf') and
                not any(c in row['filename'] for c in '/\\:*?"<>|') and not any(ord(c)<32 for c in row['filename']),'PREPARATION_MASTER_FIELDS')
        inputs.append({**{k:v for k,v in row.items() if k!='filename'},'path':str(Path(__file__).resolve())+'.'+str(len(inputs))+'.xisf','sha256':'0'*64})
    require([(r['panelId'],r['role']) for r in inputs]==[(p,r) for p in panels for r in MODES[profile['mode']]],'PREPARATION_MASTER_ORDER')
    if mappings:
        expected=[(mapping[role]['filename'],mapping[role]['imageIndex']) for mapping in mappings for role in MODES[profile['mode']]]
        require([(row['filename'],row['imageIndex']) for row in plan['masters']]==expected,'PREPARATION_SELECTED_FILES_BINDING')
    request={k:plan[k] for k in ('mode','layout','bayerPattern','canvas','shrink','feather')}
    request.update(schemaVersion='1.0',jobId='PreparationProposal',inputs=inputs)
    try:spec=validate(request,verify_files=False)
    except (ValueError,TypeError,KeyError):require(False,'PREPARATION_PLAN_BOUNDS')
    return spec


class PreparationFlowMixin:
    def preparation_state(self, request_id):
        raw,_=self.store.get('science/preparation-plans/'+request_id)
        plan=decode(raw) if raw else None
        approval,_=self.store.get('science/preparation-approvals/'+request_id)
        approved=bool(plan and approval and decode(approval)=={'preparationPlanSha256':sha(plan)})
        result,_=self.store.get('science/preparation-results/'+request_id)
        result=decode(result) if result else None
        return {'preparationPlan':plan,'preparationPlanSha256':sha(plan) if plan else None,
                'preparationApproved':approved,'preparationResult':result,
                'preparationResultSha256':sha(result) if result else None}

    def _preparation_intake(self, request_id):
        intake=self.intake(request_id)
        source,_=self.store.get('science/source-plans/'+request_id)
        approval,_=self.store.get('science/source-approvals/'+request_id)
        if source:
            intake={**intake,'sourcePlan':decode(source),'sourceSelectionApproved':bool(approval and decode(approval)=={'sourcePlanSha256':sha(decode(source))})}
        return intake

    def propose_preparation(self, request_id, value):
        intake=self._preparation_intake(request_id)
        spec=validate_plan(intake,value,self.broker.worker_id)
        plan={**copy.deepcopy(value),'nativeProcessCount':spec['nativeProcessCount'],
              'checkpointCount':len(spec['outputs']),'verification':'WORKER_REPORTED_NOT_ATTESTED'}
        immutable(self.store,'science/preparation-plans/'+request_id,encode(plan))
        return {'requestId':request_id,'preparationPlanSha256':sha(plan),'state':'PREPARATION_REVIEW','nativeStarted':False}

    def approve_preparation(self, request_id, value):
        require(isinstance(value,dict) and set(value)=={'preparationPlanSha256'},'PREPARATION_APPROVAL_FIELDS')
        state=self.preparation_state(request_id);plan=state['preparationPlan']
        require(plan and value['preparationPlanSha256']==state['preparationPlanSha256'],'PREPARATION_PLAN_CHANGED')
        intake=self._preparation_intake(request_id)
        validate_plan(intake,{k:v for k,v in plan.items() if k not in {'nativeProcessCount','checkpointCount','verification'}},self.broker.worker_id)
        if not state['preparationApproved']:
            from .historical_source import historical
            require(historical(intake['selection']) or hashlib.sha256(self.catalog_loader()).hexdigest()==intake['selection']['catalogSha256'],'CATALOG_CHANGED_REFRESH')
        def authorize(current, _now):
            require(request_id not in current.get('withdrawnIntakes', []), 'INTAKE_WITHDRAWN')
            rows=current.setdefault('preparationAuthorizedIntakes', [])
            if request_id not in rows:rows.append(request_id)
            return {'requestId':request_id}
        self.broker._mutate(authorize)
        immutable(self.store,'science/preparation-approvals/'+request_id,encode(value))
        return {'requestId':request_id,'state':'LOCAL_PREPARATION_APPROVED','nativeStarted':False}

    def record_preparation(self, request_id, value):
        state=self.preparation_state(request_id);plan=state['preparationPlan']
        fields={'workerId','preparationPlanSha256','sourceManifestSha256','outputManifestSha256',
                'verificationSha256','nativeInstancesSha256','masters','nativeProcessCount','checkpointCount'}
        require(state['preparationApproved'] and isinstance(value,dict) and set(value)==fields and value['workerId']==self.broker.worker_id,'PREPARATION_RESULT_APPROVAL')
        require(value['preparationPlanSha256']==state['preparationPlanSha256'] and value['sourceManifestSha256']==plan['sourceManifestSha256'],'PREPARATION_RESULT_BINDING')
        require(all(isinstance(value[k],str) and re.fullmatch(r'[a-f0-9]{64}',value[k]) for k in ('outputManifestSha256','verificationSha256','nativeInstancesSha256')),'PREPARATION_RESULT_DIGEST')
        require(type(value['nativeProcessCount']) is int and type(value['checkpointCount']) is int and value['nativeProcessCount']==plan['nativeProcessCount'] and value['checkpointCount']==plan['checkpointCount'],'PREPARATION_RESULT_COMPLETENESS')
        roles=('RGB',) if plan['mode']=='OSC_CFA' else MODES[plan['mode']]
        require(isinstance(value['masters'],list) and len(value['masters'])==len(roles),'PREPARATION_RESULT_MASTERS')
        width,height=(plan['canvas']['width'],plan['canvas']['height']) if plan['layout']=='PANELS' else (plan['masters'][0]['width'],plan['masters'][0]['height'])
        require(all(row=={'role':role,'width':width,'height':height,'imageIndex':0} for role,row in zip(roles,value['masters'])),'PREPARATION_RESULT_GEOMETRY')
        result={**copy.deepcopy(value),'status':'COMPLETED','nonLinear':False,'scientificAcceptance':'OWNER_REVIEW_REQUIRED',
                'verification':'WORKER_REPORTED_NOT_ATTESTED','upstreamHistoryCompleteness':'NOT_ESTABLISHED'}
        immutable(self.store,'science/preparation-results/'+request_id,encode(result))
        return {'requestId':request_id,'preparationResultSha256':sha(result),'state':'AWAITING_PROCESSING_PLAN','nativeStarted':False}
