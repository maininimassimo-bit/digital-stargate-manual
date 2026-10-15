"""Versioned private confirmatory campaign ledger for the trusted HTTP adapters.

Methods are application ports, not authentication APIs. Only the existing
Google-Owner / dedicated-worker HTTP boundaries may expose them. Worker facts
remain reported evidence; scientific qualification is an explicit Owner review
of exact private evidence, never an inference from COMPLETED or a local import.
No job dispatch, provider call, credential creation, or legacy-state migration.
"""
import copy
import datetime as dt
import hashlib
import math

from tools.pixinsight.local_pilot.broker import decode, encode, opaque, require
from tools.scientific_registry.ingestion_storage import Conflict
from tools.scientific_transients.queue import fields, digest

PROTOCOL = 'DSG_CONFIRMATORY_CAMPAIGNS_V1'
LIMIT = 8 * 1024 * 1024
NON_CONFIRMATORY_PURPOSES = frozenset({'DEVELOPMENT', 'SYNTHETIC'})
FRAME_FIELDS = {'frameRef', 'sha256', 'exposureRef', 'role', 'acquiredUTC',
                'metadataSha256', 'bandpassSha256', 'calibration', 'uncertainty', 'timeStatus'}


def fingerprint(value):
    return hashlib.sha256(encode(value)).hexdigest()


def utc(value):
    require(type(value) is str and len(value) <= 40, 'CAMPAIGN_UTC')
    try:
        stamp = dt.datetime.fromisoformat(value)
    except ValueError:
        require(False, 'CAMPAIGN_UTC')
    require(stamp.utcoffset() == dt.timedelta(0), 'CAMPAIGN_UTC')
    return stamp


def validate_inputs(value):
    fields(value, {'witnessRef', 'reportSha256', 'purpose', 'correlationRef', 'frames'})
    require(opaque(value['witnessRef']) and digest(value['reportSha256'])
            and opaque(value['correlationRef']), 'CAMPAIGN_INPUT_ID')
    require(type(value['purpose']) is str and value['purpose'] in {'CONFIRMATORY_RESERVED_REAL', 'DEVELOPMENT', 'SYNTHETIC'},
            'CAMPAIGN_INPUT_PURPOSE')
    require(type(value['frames']) is list and len(value['frames']) == 3, 'CAMPAIGN_INPUT_TRIPLET')
    for f in value['frames']:
        fields(f, FRAME_FIELDS)
        require(opaque(f['frameRef']) and opaque(f['exposureRef'])
                and all(digest(f[k]) for k in ('sha256', 'metadataSha256', 'bandpassSha256')),
                'CAMPAIGN_FRAME_ID')
        require(all(type(f[k]) is str for k in ('role','calibration','uncertainty','timeStatus'))
                and f['role'] in {'SCIENCE', 'TEMPLATE', 'DIFFERENCE', 'UNKNOWN'}
                and f['calibration'] in {'VERIFIED_FOR_DECLARED_MODEL', 'UNKNOWN'}
                and f['uncertainty'] in {'COMPLETE_FOR_DECLARED_MODEL', 'UNKNOWN'}
                and f['timeStatus'] in {'ACQUIRED_VERIFIED', 'UNKNOWN'}, 'CAMPAIGN_FRAME_SCOPE')
        if f['acquiredUTC'] is not None:
            utc(f['acquiredUTC'])
    return value


def input_blockers(value):
    reasons = []
    fs = value['frames']
    if value['purpose'] != 'CONFIRMATORY_RESERVED_REAL': reasons.append('NOT_RESERVED_REAL_CONTROL')
    if any(f['role'] != 'SCIENCE' for f in fs): reasons.append('NOT_THREE_SCIENCE_EXPOSURES')
    if len({f['sha256'] for f in fs}) != 3 or len({f['exposureRef'] for f in fs}) != 3:
        reasons.append('REPEATED_INPUT_OR_EXPOSURE')
    if len({f['bandpassSha256'] for f in fs}) != 1: reasons.append('BANDPASS_COMPARABILITY_MISSING')
    if any(f['calibration'] != 'VERIFIED_FOR_DECLARED_MODEL' or
           f['uncertainty'] != 'COMPLETE_FOR_DECLARED_MODEL' for f in fs):
        reasons.append('CALIBRATION_OR_FULL_MODEL_UNCERTAINTY_MISSING')
    if any(f['acquiredUTC'] is None or f['timeStatus'] != 'ACQUIRED_VERIFIED' for f in fs):
        reasons.append('ACQUISITION_TIME_NOT_VERIFIED')
    elif not all(utc(fs[i]['acquiredUTC']) < utc(fs[i+1]['acquiredUTC']) for i in range(2)):
        reasons.append('NOT_STRICTLY_CHRONOLOGICAL')
    return reasons


class ConfirmatoryCampaigns:
    def __init__(self, store, state_ref, worker_id, owner_ref, job_reader, clock=None):
        require(opaque(state_ref) and opaque(worker_id) and opaque(owner_ref)
                and callable(job_reader), 'CAMPAIGN_CONFIGURATION')
        self.worker_id, self.owner_ref = worker_id, owner_ref
        self.store, self.job_reader = store, job_reader
        self.key = 'control/transient-confirmatory/' + state_ref + '/state-v1.json'
        self.clock = clock or (lambda: dt.datetime.now(dt.timezone.utc))

    def _read(self):
        raw, generation = self.store.get(self.key)
        if raw is None:
            return {'protocol': PROTOCOL, 'workerId': self.worker_id, 'ownerRef': self.owner_ref,
                    'inputs': [], 'plans': [], 'lastRecordedUTC': None, 'stateSha256': None}, generation
        require(len(raw) <= LIMIT, 'CAMPAIGN_STORAGE_LIMIT')
        state = decode(raw)
        fields(state, {'protocol', 'workerId', 'ownerRef', 'inputs', 'plans', 'lastRecordedUTC', 'stateSha256'})
        require(state['workerId'] == self.worker_id and state['ownerRef'] == self.owner_ref
                and state['stateSha256'] == fingerprint({k:v for k,v in state.items() if k != 'stateSha256'}),
                'CAMPAIGN_STATE_IDENTITY_OR_INTEGRITY')
        require(state['protocol'] == PROTOCOL and type(state['inputs']) is list
                and type(state['plans']) is list and len(state['inputs']) <= 500
                and len(state['plans']) <= 8, 'CAMPAIGN_STATE')
        refs = set()
        for w in state['inputs']:
            validate_inputs(w['request'])
            require(w['sha256'] == fingerprint(w['request']) and w['request']['witnessRef'] not in refs,
                    'CAMPAIGN_INPUT_INTEGRITY')
            refs.add(w['request']['witnessRef'])
        for p in state['plans']:
            require(p['planSha256'] == fingerprint(p['request']), 'CAMPAIGN_PLAN_INTEGRITY')
            previous = None
            for event in p['events']:
                require(event['previous'] == previous and
                        event['sha256'] == fingerprint({k:v for k,v in event.items() if k != 'sha256'}),
                        'CAMPAIGN_EVENT_INTEGRITY')
                previous = event['sha256']
            require(previous == p['headSha256'], 'CAMPAIGN_HEAD_INTEGRITY')
        return state, generation

    def _mutate(self, operation):
        now = self.clock(); stamp = now.isoformat(); utc(stamp)
        for _ in range(8):
            state, generation = self._read(); before = encode(state)
            require(state['lastRecordedUTC'] is None or now >= utc(state['lastRecordedUTC']),
                    'CAMPAIGN_CLOCK_ROLLBACK')
            result = operation(state, stamp)
            if encode(state) != before:
                state['lastRecordedUTC'] = stamp
                state['stateSha256'] = fingerprint({k:v for k,v in state.items() if k != 'stateSha256'})
                raw = encode(state); require(len(raw) <= LIMIT, 'CAMPAIGN_STORAGE_LIMIT')
                try:
                    self.store.put(self.key, raw, generation)
                except Conflict:
                    continue
            return copy.deepcopy(result)
        raise Conflict('CAMPAIGN_STORAGE_CONFLICT')

    @staticmethod
    def _input(state, ref):
        require(opaque(ref), 'CAMPAIGN_INPUT_ID')
        matches = [w for w in state['inputs'] if w['request']['witnessRef'] == ref]
        require(len(matches) == 1, 'CAMPAIGN_INPUT_NOT_FOUND')
        return matches[0]

    @staticmethod
    def _plan(state, ref):
        require(opaque(ref), 'CAMPAIGN_PLAN_ID')
        matches = [p for p in state['plans'] if p['request']['planRef'] == ref]
        require(len(matches) == 1, 'CAMPAIGN_PLAN_NOT_FOUND')
        return matches[0]

    def _event(self, plan, kind, request, stamp, authority, facts=None):
        event = {'kind':kind, 'request':copy.deepcopy(request), 'recordedUTC':stamp,
                 'authority':authority, 'previous':plan['headSha256'], 'facts':copy.deepcopy(facts),
                 'actorRef':self.owner_ref if authority.startswith('AUTHENTICATED_OWNER') else self.worker_id}
        event['sha256'] = fingerprint(event)
        plan['events'].append(event); plan['headSha256'] = event['sha256']
        return event

    @staticmethod
    def _repeat(events, request):
        matches = [e for e in events if e['request'].get('decisionId') == request['decisionId']]
        if matches:
            require(len(matches) == 1 and matches[0]['request'] == request, 'CAMPAIGN_DECISION_CONFLICT')
            return matches[0]
        return None

    @staticmethod
    def _worker_record(record):
        value=copy.deepcopy(record);value.pop('review',None)
        return value

    def register_inputs(self, request):
        validate_inputs(request)
        def operation(state, stamp):
            existing = [w for w in state['inputs'] if w['request']['witnessRef'] == request['witnessRef']]
            if existing:
                require(existing[0]['request'] == request, 'CAMPAIGN_INPUT_CONFLICT')
                return self._worker_record(existing[0])
            require(len(state['inputs']) < 500, 'CAMPAIGN_INPUT_CAPACITY')
            row = {'request':copy.deepcopy(request), 'sha256':fingerprint(request),
                   'recordedUTC':stamp, 'evidenceOrigin':'AUTHENTICATED_WORKER_REPORTED_NOT_ATTESTED',
                   'review':None}
            state['inputs'].append(row); return self._worker_record(row)
        return self._mutate(operation)

    def review_input(self, ref, request):
        fields(request, {'decisionId', 'witnessSha256', 'nullReferenceSha256', 'independenceSha256',
                         'modelReviewSha256', 'separationEvidenceSha256', 'algorithmSha256', 'contractSha256', 'acceptNullReference',
                         'acceptIndependence', 'acceptScienceModel', 'acceptDevelopmentSeparation'})
        require(opaque(request['decisionId']) and all(digest(request[k]) for k in
                ('witnessSha256','nullReferenceSha256','independenceSha256',
                 'modelReviewSha256','separationEvidenceSha256','algorithmSha256','contractSha256')) and all(request[k] is True for k in
                ('acceptNullReference','acceptIndependence','acceptScienceModel','acceptDevelopmentSeparation')),
                'CAMPAIGN_SCIENTIFIC_REVIEW')
        def operation(state, stamp):
            w = self._input(state, ref)
            require(request['witnessSha256'] == w['sha256'] and not input_blockers(w['request']),
                    'CAMPAIGN_INPUT_NOT_ELIGIBLE')
            if w['review'] is not None:
                require(w['review']['request'] == request, 'CAMPAIGN_INPUT_REVIEW_CONFLICT')
                return w['review']
            review = {'request':copy.deepcopy(request), 'recordedUTC':stamp,
                      'authority':'AUTHENTICATED_OWNER_SCIENTIFIC_DECISION','actorRef':self.owner_ref}
            w['review'] = review; return review
        return self._mutate(operation)

    def create(self, request):
        fields(request, {'planRef','algorithmRef','algorithmSha256','contractRef','contractSha256',
                         'inputWitnessRefs','falsePositiveMaximum','confidence','requiredControls'})
        require(all(opaque(request[k]) for k in ('planRef','algorithmRef','contractRef'))
                and digest(request['algorithmSha256']) and digest(request['contractSha256'])
                and request['falsePositiveMaximum'] == .05 and request['confidence'] == .95
                and type(request['requiredControls']) is int and request['requiredControls'] == 59,
                'CAMPAIGN_FROZEN_RULES')
        refs = request['inputWitnessRefs']
        require(type(refs) is list and len(refs) == 59 and all(opaque(v) for v in refs)
                and len(set(refs)) == 59, 'CAMPAIGN_FIXED_SAMPLE')
        def operation(state, stamp):
            existing = [p for p in state['plans'] if p['request']['planRef'] == request['planRef']]
            if existing:
                require(existing[0]['request'] == request, 'CAMPAIGN_PLAN_CONFLICT')
                return self._summary(state, existing[0])
            for ref in refs: self._input(state, ref)
            require(len(state['plans']) < 8, 'CAMPAIGN_PLAN_CAPACITY')
            p = {'request':copy.deepcopy(request), 'planSha256':fingerprint(request),
                 'headSha256':None, 'events':[], 'frozenUTC':None, 'executions':[], 'revoked':False,
                 'developmentWitnessRefsAtFreeze':None, 'registrySnapshotSha256':None}
            self._event(p, 'CREATE', request, stamp, 'AUTHENTICATED_OWNER_REQUEST')
            state['plans'].append(p); return self._summary(state, p)
        return self._mutate(operation)

    def _sample_blockers(self, state, plan):
        reasons=[]; hashes=[]; frame_refs=[]; exposures=[]; clusters=[]
        for ref in plan['request']['inputWitnessRefs']:
            w=self._input(state, ref); v=w['request']; reasons += input_blockers(v)
            if w['review'] is None: reasons.append('OWNER_INPUT_REVIEW_MISSING')
            elif any(w['review']['request'][k] != plan['request'][k]
                     for k in ('algorithmSha256','contractSha256')):
                reasons.append('INPUT_REVIEW_DIFFERENT_ALGORITHM_OR_RULES')
            hashes += [f['sha256'] for f in v['frames']]
            frame_refs += [f['frameRef'] for f in v['frames']]
            exposures += [f['exposureRef'] for f in v['frames']]
            clusters.append(v['correlationRef'])
        if len(set(clusters)) != 59: reasons.append('DEPENDENCY_GROUP_REUSED')
        if any(len(set(v)) != 177 for v in (hashes,frame_refs,exposures)):
            reasons.append('OBSERVATION_REUSED')
        development_refs = ({w['request']['witnessRef'] for w in state['inputs']
                             if w['request']['purpose'] in NON_CONFIRMATORY_PURPOSES} if plan['frozenUTC'] is None
                            else set(plan['developmentWitnessRefsAtFreeze']))
        selected = {'sha256':set(hashes), 'frameRef':set(frame_refs), 'exposureRef':set(exposures)}
        development = [f for w in state['inputs']
                       if w['request']['witnessRef'] in development_refs for f in w['request']['frames']]
        if any(selected[key].intersection(f[key] for f in development) for key in selected):
            reasons.append('DEVELOPMENT_INPUT_OVERLAP')
        for other in state['plans']:
            if other is plan or other['frozenUTC'] is None: continue
            used=[f for ref in other['request']['inputWitnessRefs']
                  for f in self._input(state, ref)['request']['frames']]
            if any(selected[key].intersection(f[key] for f in used) for key in selected):
                reasons.append('EARLIER_FROZEN_SAMPLE_REUSED')
        return sorted(set(reasons))

    def _selected_reviews_sha(self, state, plan):
        return fingerprint([{'witnessSha256':self._input(state,r)['sha256'],
                             'review':self._input(state,r)['review']}
                            for r in plan['request']['inputWitnessRefs']])

    def freeze(self, ref, request):
        fields(request, {'decisionId','planHeadSha256','approveAlgorithm','approveRules',
                         'expectedInputReviewSha256','independenceReviewSha256',
                         'developmentSeparationReviewSha256','approveSampleIndependence',
                         'approveDevelopmentSeparation'})
        require(opaque(request['decisionId']) and digest(request['planHeadSha256'])
                and all(digest(request[k]) for k in ('expectedInputReviewSha256','independenceReviewSha256',
                                                    'developmentSeparationReviewSha256'))
                and request['approveAlgorithm'] is True and request['approveRules'] is True
                and request['approveSampleIndependence'] is True
                and request['approveDevelopmentSeparation'] is True,
                'CAMPAIGN_FREEZE_REVIEW')
        def operation(state, stamp):
            p=self._plan(state,ref); repeat=self._repeat(p['events'],request)
            if repeat: return repeat
            require(not p['revoked'] and p['frozenUTC'] is None and
                    p['headSha256']==request['planHeadSha256']
                    and request['expectedInputReviewSha256']==self._selected_reviews_sha(state,p)
                    and not self._sample_blockers(state,p),
                    'CAMPAIGN_FREEZE_BLOCKED')
            p['developmentWitnessRefsAtFreeze']=[w['request']['witnessRef'] for w in state['inputs']
                                                if w['request']['purpose'] in NON_CONFIRMATORY_PURPOSES]
            p['registrySnapshotSha256']=fingerprint(state['inputs'])
            p['frozenUTC']=stamp
            return self._event(p,'FREEZE',request,stamp,'AUTHENTICATED_OWNER_SCIENTIFIC_DECISION',
                               {'registrySnapshotSha256':p['registrySnapshotSha256'],
                                'inputReviewSnapshotSha256':request['expectedInputReviewSha256']})
        return self._mutate(operation)

    def record_execution(self, ref, request):
        fields(request, {'executionRef','planSha256','witnessRef','algorithmSha256','contractSha256',
                         'scienceEvidenceSha256','pipelineStatus','outcome','jobs'})
        require(opaque(request['executionRef']) and opaque(request['witnessRef'])
                and all(digest(request[k]) for k in ('planSha256','algorithmSha256',
                    'contractSha256','scienceEvidenceSha256'))
                and type(request['pipelineStatus']) is str and request['pipelineStatus'] in {'COMPLETE_UNDER_FROZEN_RULES','INCOMPLETE'}
                and type(request['outcome']) is str and request['outcome'] in {'NO_ALERT','FALSE_ALERT','INCONCLUSIVE'}
                and type(request['jobs']) is list and len(request['jobs'])==3,
                'CAMPAIGN_EXECUTION')
        for job in request['jobs']:
            fields(job, {'jobId','attemptId','frameRef','inputSha256','reportSha256'})
            require(type(job['jobId']) is str and job['jobId'].startswith('TRN_')
                    and opaque(job['jobId'][4:]) and opaque(job['frameRef']) and digest(job['inputSha256'])
                    and (job['attemptId'] is None or opaque(job['attemptId']))
                    and (job['reportSha256'] is None or digest(job['reportSha256'])), 'CAMPAIGN_EXECUTION_JOB')
        require(len({j['jobId'] for j in request['jobs']})==3, 'CAMPAIGN_JOB_REUSED')
        def operation(state, stamp):
            p=self._plan(state,ref);v=p['request']
            require(p['frozenUTC'] is not None and not p['revoked']
                    and request['planSha256']==p['planSha256']
                    and request['algorithmSha256']==v['algorithmSha256']
                    and request['contractSha256']==v['contractSha256']
                    and request['witnessRef'] in v['inputWitnessRefs'], 'CAMPAIGN_EXECUTION_BINDING')
            previous=[e for e in p['executions'] if e['request']['executionRef']==request['executionRef']]
            if previous:
                require(previous[0]['request']==request,'CAMPAIGN_EXECUTION_CONFLICT');return self._worker_record(previous[0])
            require(not any(e['request']['witnessRef']==request['witnessRef'] for e in p['executions']),
                    'CAMPAIGN_CASE_EXECUTION_ALREADY_RECORDED')
            w=self._input(state,request['witnessRef']); technical=True; snapshots=[]
            require([j['frameRef'] for j in request['jobs']]==[f['frameRef'] for f in w['request']['frames']],
                    'CAMPAIGN_FRAME_BINDING')
            for item,frame in zip(request['jobs'],w['request']['frames']):
                require(item['inputSha256']==frame['sha256'], 'CAMPAIGN_INPUT_DIGEST')
                job=self.job_reader(item['jobId']); binding=job['binding']
                require(job['jobId']==item['jobId'] and job.get('attemptId')==item['attemptId']
                        and binding['inputRef']==item['frameRef'] and binding['algorithmRef']==v['algorithmRef']
                        and binding['contractRef']==v['contractRef'] and utc(job['createdAt'])>utc(p['frozenUTC'])
                        and utc(job['updatedAt'])>=utc(job['createdAt']), 'CAMPAIGN_JOB_IDENTITY_OR_CHRONOLOGY')
                result=job.get('result')
                complete=(job['state']=='COMPLETED' and result is not None and
                          result['reportSha256']==item['reportSha256'] and result['bindingRef']==binding['bindingRef'] and
                          type(result['qualityCounts']['incomplete']) is int
                          and type(result['qualityCounts']['measured']) is int
                          and result['qualityCounts']['incomplete']==0 and result['qualityCounts']['measured']>0)
                require(item['reportSha256']==(None if result is None else result['reportSha256']),
                        'CAMPAIGN_REPORT_DIGEST')
                technical=technical and complete
                snapshots.append({'jobId':job['jobId'],'attemptId':job.get('attemptId'),
                                  'state':job['state'],'createdAt':job['createdAt'],
                                  'updatedAt':job['updatedAt'],'reportSha256':item['reportSha256']})
            if request['outcome']!='INCONCLUSIVE':
                require(technical and request['pipelineStatus']=='COMPLETE_UNDER_FROZEN_RULES',
                        'CAMPAIGN_INCOMPLETE_NOT_SUCCESS')
            record={'request':copy.deepcopy(request),'sha256':fingerprint(request),
                    'recordedUTC':stamp,'technicalCompleted':technical,'jobSnapshots':snapshots,
                    'evidenceOrigin':'AUTHENTICATED_WORKER_REPORTED_NOT_ATTESTED','review':None}
            p['executions'].append(record)
            self._event(p,'EXECUTION',{'executionSha256':record['sha256']},stamp,
                        'AUTHENTICATED_WORKER_REPORTED_NOT_ATTESTED')
            return self._worker_record(record)
        return self._mutate(operation)

    def review_outcome(self, ref, request):
        fields(request, {'decisionId','executionSha256','acceptRecordedOutcome'})
        require(opaque(request['decisionId']) and digest(request['executionSha256'])
                and request['acceptRecordedOutcome'] is True, 'CAMPAIGN_OUTCOME_REVIEW')
        def operation(state, stamp):
            p=self._plan(state,ref);repeat=self._repeat(p['events'],request)
            if repeat:return repeat
            rows=[e for e in p['executions'] if e['sha256']==request['executionSha256']]
            require(not p['revoked'] and len(rows)==1 and rows[0]['technicalCompleted']
                    and rows[0]['request']['pipelineStatus']=='COMPLETE_UNDER_FROZEN_RULES'
                    and rows[0]['request']['outcome']!='INCONCLUSIVE', 'CAMPAIGN_OUTCOME_INELIGIBLE')
            require(rows[0]['review'] is None,'CAMPAIGN_OUTCOME_ALREADY_REVIEWED')
            rows[0]['review']=self._event(p,'OUTCOME_REVIEW',request,stamp,
                                        'AUTHENTICATED_OWNER_SCIENTIFIC_DECISION')
            return rows[0]['review']
        return self._mutate(operation)

    def _summary(self, state, plan):
        blockers=self._sample_blockers(state,plan); executions=plan['executions']
        if plan['frozenUTC'] is None:blockers.append('PLAN_NOT_FROZEN')
        if plan['revoked']:blockers.append('PLAN_REVOKED')
        eligible_base=not blockers
        accepted=sum(e['review'] is not None and e['request']['outcome']=='NO_ALERT' for e in executions)
        reviewed=sum(e['review'] is not None for e in executions)
        false_alerts=sum(e['request']['outcome']=='FALSE_ALERT' for e in executions)
        if len(executions)!=59 or reviewed!=59:blockers.append('COMPLETE_REVIEWED_SAMPLE_MISSING')
        if false_alerts:blockers.append('ZERO_EVENT_CRITERION_FAILED')
        statistic=None
        if not blockers:
            bound=-math.expm1(math.log(.05)/59)
            statistic={'independentControls':59,'falseAlerts':0,'confidence':.95,
                       'oneSidedUpperBound':bound,'maximum':.05,'thresholdMet':bound<=.05,
                       'scope':'CONDITIONAL_ON_FROZEN_RULES_AND_AUTHENTICATED_OWNER_EVIDENCE_REVIEW'}
        final=any(e['kind']=='FINAL_OWNER_ACCEPTANCE' for e in plan['events'])
        return {'schema':'BKL051_CONFIRMATORY_CAMPAIGN_VIEW_V1','planRef':plan['request']['planRef'],
                'planSha256':plan['planSha256'],'headSha256':plan['headSha256'],
                'inputReviewSnapshotSha256':self._selected_reviews_sha(state,plan),
                'frozenUTC':plan['frozenUTC'],'candidateCases':59,'executionRecords':len(executions),
                'acceptedNoAlertRecords':accepted,'falseAlertRecords':false_alerts,
                'qualifiedControls':reviewed if eligible_base else 0,'statisticalResult':statistic,
                'ownerReviewedInputs':sum(self._input(state,r)['review'] is not None
                                          for r in plan['request']['inputWitnessRefs']),
                'cases':[{'witnessRef':r, 'inputReviewedByOwner':self._input(state,r)['review'] is not None,
                          'inputBlockers':input_blockers(self._input(state,r)['request']),
                          'executionSha256':next((e['sha256'] for e in executions
                              if e['request']['witnessRef']==r),None)} for r in plan['request']['inputWitnessRefs']],
                'status':'BLOCKED' if blockers else 'OWNER_ACCEPTED_CAMPAIGN_SCOPE_ONLY' if final
                         else 'READY_FOR_OWNER_FINAL_REVIEW','blockers':sorted(set(blockers)),
                'qualificationBasis':'AUTHENTICATED_OWNER_REVIEW_OF_WORKER_REPORTED_EVIDENCE',
                'scientificValidation':'OWNER_ACCEPTED_DECLARED_CAMPAIGN_ONLY' if final and not blockers
                                       else 'NOT_VALIDATED','publication':'NONE','implicitDispatch':False}

    def finalize(self, ref, request):
        fields(request, {'decisionId','planHeadSha256','acceptDeclaredCampaign'})
        require(opaque(request['decisionId']) and digest(request['planHeadSha256'])
                and request['acceptDeclaredCampaign'] is True,'CAMPAIGN_FINAL_REVIEW')
        def operation(state, stamp):
            p=self._plan(state,ref);repeat=self._repeat(p['events'],request)
            if repeat:return repeat
            summary=self._summary(state,p)
            require(p['headSha256']==request['planHeadSha256'] and
                    summary['status']=='READY_FOR_OWNER_FINAL_REVIEW','CAMPAIGN_FINAL_BLOCKED')
            return self._event(p,'FINAL_OWNER_ACCEPTANCE',request,stamp,
                               'AUTHENTICATED_OWNER_SCIENTIFIC_DECISION')
        return self._mutate(operation)

    def revoke(self, ref, request):
        fields(request, {'decisionId','planHeadSha256','evidenceSha256','reason'})
        require(opaque(request['decisionId']) and digest(request['planHeadSha256'])
                and digest(request['evidenceSha256']) and type(request['reason']) is str
                and request['reason'] in
                {'REFERENCE_INVALID','INDEPENDENCE_INVALID','ALGORITHM_ERROR','OWNER_WITHDRAWAL'},
                'CAMPAIGN_REVOCATION')
        def operation(state, stamp):
            p=self._plan(state,ref);repeat=self._repeat(p['events'],request)
            if repeat:return repeat
            require(p['headSha256']==request['planHeadSha256'],'CAMPAIGN_REVOCATION_HEAD')
            p['revoked']=True
            return self._event(p,'REVOCATION',request,stamp,'AUTHENTICATED_OWNER_SCIENTIFIC_DECISION')
        return self._mutate(operation)

    def view(self, ref=None):
        return self._mutate(lambda state,_: self._summary(state,self._plan(state,ref)) if ref is not None
                            else {'campaigns':[self._summary(state,p) for p in state['plans']]})

    def input_view(self, ref):
        return self._mutate(lambda state,_: self._input(state,ref))
