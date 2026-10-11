"""Authenticated native receipt admission and checkpoint decisions.

Physical verification runs on the PC. The backend binds worker-reported
evidence; it never claims independently inspected native pixels or History.
"""
import base64
import copy

from .broker import require, encode, decode
from .intake import sha
from .adaptive_ledger import DecisionJournal, NATIVE_RECEIPT_VERSION, digest
from .adaptive_segments import SegmentPermits
from .adaptive_catalog import validate_dispatch, validate_next_decision
from tools.scientific_registry.ingestion_storage import immutable

VERIFICATION_VERSION = 'DSG_PIAI_ADAPTIVE_PHYSICAL_VERIFICATION_V2'


class AdaptiveExecutionMixin:
    def adaptive_reserve(self, request_id, value):
        require(isinstance(value, dict) and set(value) ==
                {'workerId','rootId','approvalSha256','decisionResultSha256'}, 'ADAPTIVE_RESERVE_FIELDS')
        return SegmentPermits(self).reserve(request_id, value['workerId'], value['rootId'],
                                            value['approvalSha256'], value['decisionResultSha256'])

    def adaptive_start(self, request_id, value):
        require(isinstance(value, dict) and set(value) == {'workerId','permit'}, 'ADAPTIVE_START_FIELDS')
        return SegmentPermits(self).start(request_id, value['workerId'], value['permit'])

    def _adaptive_analysis(self, request_id):
        raw, _ = self.store.get('science/adaptive-analysis/' + request_id)
        require(raw is not None, 'ADAPTIVE_ANALYSIS_REQUIRED')
        return decode(raw)

    def adaptive_checkpoint(self, request_id, value):
        require(self.adaptive_enabled() and isinstance(value, dict) and
                set(value) == {'workerId','permit','verification'} and value['workerId'] == self.broker.worker_id,
                'ADAPTIVE_CHECKPOINT_FIELDS')
        analysis = self._adaptive_analysis(request_id)
        job_id = 'PIAI_' + request_id
        state, _ = self.broker._state()
        journal = DecisionJournal(self.broker)
        job = journal._live(state, job_id)
        permit = value['permit']
        require(isinstance(permit, dict) and type(permit.get('ordinal')) is int and permit['jobId'] == job_id,
                'ADAPTIVE_CHECKPOINT_PERMIT')
        ordinal = permit['ordinal']
        stored = job.get('adaptiveSegmentPermits', {}).get(str(ordinal))
        require(stored and stored['state'] == 'STARTED' and
                {k:v for k,v in stored.items() if k!='state'} ==
                {k:v for k,v in permit.items() if k!='state'}, 'ADAPTIVE_CHECKPOINT_PERMIT_CHANGED')
        v = value['verification']
        fields = {'version','jobId','ordinal','permitSha256','approvalSha256','runtimeSha256',
                  'nativeManifestSha256','outputs','historySha256','sourceGuard','currentProvenance',
                  'executedStep','parentOutputs','parentProvenance','status'}
        require(isinstance(v, dict) and set(v) == fields and v['version'] == VERIFICATION_VERSION and
                v['status'] == 'PHYSICALLY_VERIFIED' and v['jobId'] == job_id and
                type(v['ordinal']) is int and v['ordinal'] == ordinal and v['permitSha256'] == sha(permit) and
                v['approvalSha256'] == permit['approvalSha256'] and v['runtimeSha256'] == sha(analysis['runtime']) and
                all(digest(v[k]) for k in ('nativeManifestSha256','historySha256')), 'ADAPTIVE_PHYSICAL_BINDING')
        expected_guard = [{'role':i['role'],'sha256':i['sha256'],'imageIndex':i['imageIndex'],
                           'unchanged':True} for i in analysis['inputs']]
        require(v['sourceGuard'] == expected_guard and v['executedStep'] == permit['step'],
                'ADAPTIVE_SOURCES_OR_STEP_CHANGED')
        approval = decode(self.store.get('science/adaptive-approvals/' + request_id)[0])
        width, height = approval['preparation']['workingGeometry']
        outputs = v['outputs']
        require(isinstance(outputs, list) and 2 <= len(outputs) <= 5 and
                len({o.get('role') for o in outputs}) == len(outputs) and
                {'RGB','L'} <= {o.get('role') for o in outputs}, 'ADAPTIVE_OUTPUT_TRACKS')
        for o in outputs:
            require(isinstance(o, dict) and set(o) == {'role','sha256','width','height','channels','historySha256'} and
                    o['role'] in {'RGB','L','RGB_STARS','L_STARS','MASK'} and
                    digest(o['sha256']) and digest(o['historySha256']) and
                    type(o['width']) is int and type(o['height']) is int and (o['width'],o['height']) == (width,height) and
                    type(o['channels']) is int and o['channels'] == (3 if o['role'] in {'RGB','RGB_STARS'} else 1),
                    'ADAPTIVE_OUTPUT_DESCRIPTOR')
        from .adaptive_catalog import provenance
        facts = provenance(v['currentProvenance'])
        parent_facts = provenance(v['parentProvenance'])
        require(parent_facts['sourceSha256'] == sha(analysis['inputs']), 'ADAPTIVE_PARENT_SOURCE_SET')
        if ordinal:
            previous = decode(self.store.get('science/adaptive-checkpoints/' + job_id + '/' + str(ordinal-1))[0])
            require(v['parentOutputs'] == previous['outputs'] and parent_facts == previous['currentProvenance'],
                    'ADAPTIVE_PARENT_CHECKPOINT_CHANGED')
        else:
            require(parent_facts['domain'] == analysis['evidence']['provenance']['domain'], 'ADAPTIVE_BASELINE_DOMAIN')
        require(isinstance(v['parentOutputs'],list) and 2 <= len(v['parentOutputs']) <= 5 and
                {'RGB','L'} <= {o.get('role') for o in v['parentOutputs']}, 'ADAPTIVE_PARENT_OUTPUTS')
        for o in v['parentOutputs']:
            require(isinstance(o,dict) and set(o)=={'role','sha256','width','height','channels','historySha256'} and
                    o['role'] in {'RGB','L','RGB_STARS','L_STARS','MASK'} and digest(o['sha256']) and
                    digest(o['historySha256']) and type(o['width']) is int and type(o['height']) is int and
                    (o['width'],o['height'])==(width,height) and type(o['channels']) is int and
                    o['channels']==(3 if o['role'] in {'RGB','RGB_STARS'} else 1), 'ADAPTIVE_PARENT_DESCRIPTOR')
        require(facts['sourceSha256'] == sha(analysis['inputs']), 'ADAPTIVE_CHECKPOINT_SOURCE_SET')
        graph = self.adaptive_state(request_id)['plan']['decision']['graph']
        domain = analysis['evidence']['provenance']['domain']
        if any(s['process'] == 'STRETCH' for s in graph['steps'][:ordinal+1]):
            domain = 'NONLINEAR_ATTESTED'
        require(facts['domain'] == domain, 'ADAPTIVE_CHECKPOINT_DOMAIN')
        checkpoint_key = 'science/adaptive-checkpoints/' + job_id + '/' + str(ordinal)
        immutable(self.store, checkpoint_key, encode(v))
        receipt = {'version':NATIVE_RECEIPT_VERSION,'jobId':job_id,'ordinal':ordinal,
                   'decisionResultSha256':permit['decisionResultSha256'],'runtimeSha256':permit['runtimeSha256'],
                   'checkpointSha256':sha(v),'historySha256':v['historySha256'],'status':'CHECKPOINT_VERIFIED'}
        receipt_sha = sha(receipt)
        immutable(self.store, 'science/adaptive-native/' + receipt_sha, encode(receipt))
        cursor = journal._cursor(state, job_id)
        if cursor['ordinal'] == ordinal:
            journal.checkpoint(job_id, receipt_sha, permit['decisionResultSha256'])
        else:
            require(cursor['ordinal'] == ordinal+1 and cursor['parentReceiptSha256'] == receipt_sha,
                    'ADAPTIVE_CHECKPOINT_REPLAY_CHANGED')
        return self.adaptive_state(request_id)

    def adaptive_decision(self, request_id, value):
        require(self.adaptive_enabled() and isinstance(value, dict) and
                set(value) == {'workerId','evidence','bindings','assetsBase64'} and
                value['workerId'] == self.broker.worker_id, 'ADAPTIVE_DECISION_FIELDS')
        analysis = self._adaptive_analysis(request_id)
        job_id = 'PIAI_' + request_id
        journal = DecisionJournal(self.broker)
        state, _ = self.broker._state()
        journal._live(state, job_id)
        cursor = journal._cursor(state, job_id)
        ordinal = cursor['ordinal']
        require(0 < ordinal < 16, 'ADAPTIVE_DECISION_CHECKPOINT_REQUIRED')
        evidence = value['evidence']
        checkpoint = decode(self.store.get('science/adaptive-checkpoints/' + job_id + '/' + str(ordinal-1))[0])
        graph = self.adaptive_state(request_id)['plan']['decision']['graph']
        require(evidence['mode'] == analysis['evidence']['mode'] and evidence['intent'] == analysis['evidence']['intent'] and
                evidence['graph'] == graph and evidence['initialProvenance'] == analysis['evidence']['provenance'] and
                evidence['currentProvenance'] == checkpoint['currentProvenance'] and
                evidence['parentProvenance'] == checkpoint['parentProvenance'] and
                type(evidence['completedSteps']) is int and evidence['completedSteps'] == ordinal,
                'ADAPTIVE_DECISION_EVIDENCE_BINDING')
        require(evidence['bindingSha256'] == sha({'checkpointSha256':sha(checkpoint),
                'graphSha256':sha(graph),'ordinal':ordinal,'runtimeSha256':sha(analysis['runtime'])}),
                'ADAPTIVE_DECISION_CONTEXT_HASH')
        # Both phases refer to exact saved scientific tracks; PNGs are display-only.
        require(isinstance(value['bindings'], dict) and set(value['bindings']) == {'PARENT','CURRENT'},
                'ADAPTIVE_DECISION_BINDINGS')
        for phase in ('PARENT','CURRENT'):
            require(set(value['bindings'][phase]) == {'RGB','L'}, 'ADAPTIVE_DECISION_TRACK_BINDINGS')
        for phase, rows in (('PARENT',checkpoint['parentOutputs']),('CURRENT',checkpoint['outputs'])):
            for o in rows:
                if o['role'] in {'RGB','L'}:
                    binding = value['bindings'][phase][o['role']]
                    require(binding['sourceSha256'] == o['sha256'] and binding['imageIndex'] == 0 and
                            binding['adapterSha256']==analysis['runtime']['measurementSha256'] and
                            binding['starDetectorSha256']==analysis['runtime']['starDetectorSha256'],
                            'ADAPTIVE_TRACK_OR_ADAPTER_CHANGED')
        key = 'science/adaptive-checkpoint-decisions/' + job_id + '/' + str(ordinal)
        saved = self.store.get(key)[0]
        if saved:
            result = decode(saved)
            require(result['evidenceSha256'] == sha(evidence) and result['bindingsSha256'] == sha(value['bindings']),
                    'ADAPTIVE_DECISION_REPLAY_CHANGED')
            if cursor['state'] == 'RESERVED':
                request = decode(self.store.get(journal._key(job_id,ordinal,'request'))[0])
                journal.record({'sendAllowed':True,'request':request,'owner':cursor['pending']['owner']},
                    {'action':result['decision']['action'],'decisionSha256':sha(result['decision'])},result['provider']['usage'])
            return self.adaptive_state(request_id)
        assets = self._adaptive_assets(value['assetsBase64'])
        refs = {k:cursor['scope'][k] for k in ('catalogSha256','runtimeSha256','inputSetSha256')}
        reservation = journal.reserve(job_id, {**refs,'policySha256':cursor['policySha256'],'evidenceSha256':sha(evidence)})
        if not reservation['sendAllowed']:
            return self.adaptive_state(request_id)
        state, _ = self.broker._state()
        journal._live(state,job_id)
        consent = self.intake(request_id)['selection']['adaptivePlanning']
        try:
            decision, provider = self.adaptive_provider.generate_checkpoint(reservation,evidence,value['bindings'],assets,
                data_transfer_confirmed=consent['dataTransferConfirmed'],
                statistics_transfer_confirmed=consent['pixelStatisticsConfirmed'],
                preview_transfer_confirmed=consent['previewTransferConfirmed'])
        except Exception:
            return self.adaptive_state(request_id)
        validate_next_decision(decision,evidence['bindingSha256'],graph,evidence['mode'],
                               evidence['initialProvenance'],evidence['currentProvenance'],ordinal)
        result = {'decision':decision,'provider':provider,'evidenceSha256':sha(evidence),
                  'bindingsSha256':sha(value['bindings']),'decisionResultSha256':None}
        # Result digest has no circular self-reference; this is the ledger digest.
        ledger_result = {'requestSha256':sha(reservation['request']),
                         'decision':{'action':decision['action'],'decisionSha256':sha(decision)},'usage':provider['usage']}
        result['decisionResultSha256'] = sha(ledger_result)
        immutable(self.store,key,encode(result))
        journal.record(reservation,ledger_result['decision'],provider['usage'])
        return self.adaptive_state(request_id)

    @staticmethod
    def _adaptive_assets(value):
        require(isinstance(value,list) and 1 <= len(value) <= 4, 'ADAPTIVE_ASSETS')
        result = []
        for item in value:
            require(isinstance(item,str) and len(item) <= 1398104, 'ADAPTIVE_ASSET_LIMIT')
            try:
                raw = base64.b64decode(item,validate=True)
            except ValueError:
                require(False,'ADAPTIVE_ASSET_ENCODING')
            require(len(raw) <= 1048576,'ADAPTIVE_ASSET_LIMIT')
            result.append(raw)
        return result

    def adaptive_context(self, request_id):
        require(self.adaptive_enabled(),'ADAPTIVE_DISABLED')
        state=self.adaptive_state(request_id)
        ordinal=state['cursor']['ordinal'] if state['cursor'] else 0
        checkpoint=self.store.get('science/adaptive-checkpoints/PIAI_'+request_id+'/'+str(ordinal-1))[0] if ordinal else None
        decision=self.store.get('science/adaptive-checkpoint-decisions/PIAI_'+request_id+'/'+str(ordinal))[0] if ordinal else None
        checkpoints=[decode(self.store.get('science/adaptive-checkpoints/PIAI_'+request_id+'/'+str(n))[0])
                     for n in range(ordinal)]
        return {**state,'intake':self.intake(request_id),'analysis':self._adaptive_analysis(request_id),'checkpoints':checkpoints,
                'checkpoint':decode(checkpoint) if checkpoint else None,'checkpointDecision':decode(decision) if decision else None}

    def adaptive_final(self, request_id, value):
        require(self.adaptive_enabled() and isinstance(value,dict) and
                set(value)=={'workerId','verification','delivery'} and value['workerId']==self.broker.worker_id,
                'ADAPTIVE_FINAL_FIELDS')
        job_id='PIAI_'+request_id
        state,_=self.broker._state();journal=DecisionJournal(self.broker)
        cursor=journal._cursor(state,job_id)
        approval=self.adaptive_state(request_id)['executionPolicy']
        require(approval is not None,'ADAPTIVE_FINAL_OWNER_APPROVAL')
        graph=self.adaptive_state(request_id)['plan']['decision']['graph']
        require(cursor['ordinal']==len(graph['steps']) and cursor['state'] in
                {'AWAITING_FINAL_VERIFICATION','READY_FOR_OWNER_REVIEW'},'ADAPTIVE_FINAL_PREFIX')
        checkpoint=decode(self.store.get('science/adaptive-checkpoints/'+job_id+'/'+str(cursor['ordinal']-1))[0])
        v=value['verification']
        require(isinstance(v,dict) and set(v)=={'outputs','historySha256','sourceGuard','status'} and
                v['status']=='FINAL_FILES_REVERIFIED' and v['outputs']==checkpoint['outputs'] and
                v['historySha256']==checkpoint['historySha256'] and v['sourceGuard']==checkpoint['sourceGuard'],
                'ADAPTIVE_FINAL_OUTPUT_CHANGED')
        delivery=value['delivery']
        require(isinstance(delivery,dict) and set(delivery)=={'version','artifacts','archive','previewBase64','previewSha256'} and
                delivery['version']=='DSG_PIAI_ADAPTIVE_PRIVATE_DELIVERY_V2' and
                isinstance(delivery['artifacts'],list) and 2<=len(delivery['artifacts'])<=5,
                'ADAPTIVE_DELIVERY_FIELDS')
        from .intake import local_directory
        require([{k:o[k] for k in ('role','sha256')} for o in delivery['artifacts']]==
                [{k:o[k] for k in ('role','sha256')} for o in v['outputs']], 'ADAPTIVE_DELIVERY_OUTPUTS')
        for o in delivery['artifacts']:
            require(set(o)=={'role','sha256','localPath'} and local_directory(o['localPath']).lower().endswith('.xisf'),
                    'ADAPTIVE_DELIVERY_PRIVATE_XISF')
        require(isinstance(delivery['archive'],dict) and set(delivery['archive'])=={'localPath','sha256','externalDependencies','replayStatus'} and
                digest(delivery['archive']['sha256']) and delivery['archive']['externalDependencies']==
                ['LICENSED_PIXINSIGHT_INSTALLATION','LICENSED_RC_ASTRO_MODULES','LOCAL_PATH_RELOCATION_REQUIRED'] and
                delivery['archive']['replayStatus']=='EVIDENCE_ARCHIVE_NOT_AUTONOMOUS_REPLAY' and
                local_directory(delivery['archive']['localPath']).lower().endswith('.zip'), 'ADAPTIVE_COMPLETE_ARCHIVE')
        asset=self._adaptive_assets([delivery['previewBase64']])[0]
        from .image_previews import provider_image
        provider_image(asset,delivery['previewSha256'],expected_channels=3)
        result={'delivery':delivery,'verification':v,'scientificAcceptance':'NONE','publication':'NONE',
                'executionEvidence':'WORKER_REPORTED_NOT_INDEPENDENTLY_ATTESTED'}
        immutable(self.store,'science/adaptive-deliveries/'+request_id,encode(result))
        receipt={'version':NATIVE_RECEIPT_VERSION,'jobId':job_id,'ordinal':cursor['ordinal'],
                 'decisionResultSha256':cursor['resultSha256'],'runtimeSha256':cursor['scope']['runtimeSha256'],
                 'parentReceiptSha256':cursor['parentReceiptSha256'],'approvalSha256':sha(approval),
                 'outputsSha256':sha(v['outputs']),'historySha256':v['historySha256'],
                 'sourceGuardSha256':sha(v['sourceGuard']),'status':'FINAL_VERIFIED_FOR_OWNER_REVIEW'}
        immutable(self.store,'science/adaptive-native/'+sha(receipt),encode(receipt))
        if cursor['state']!='READY_FOR_OWNER_REVIEW':
            journal.final_verification(job_id,sha(receipt),cursor['resultSha256'])
        def complete(state,now):
            job=self.broker._job(state,job_id)
            if job['state']=='COMPLETED':return
            journal._live(state,job_id)
            require(journal._cursor(state,job_id)['state']=='READY_FOR_OWNER_REVIEW','ADAPTIVE_FINAL_READINESS')
            job.update(state='COMPLETED',updatedAt=now,adaptiveDeliverySha256=sha(result))
        self.broker._mutate(complete)
        return self.adaptive_state(request_id)

    def adaptive_result(self, request_id):
        state=self.adaptive_state(request_id)
        raw=self.store.get('science/adaptive-deliveries/'+request_id)[0]
        require(raw and state['job']['state']=='COMPLETED' and
                state['job'].get('adaptiveDeliverySha256')==sha(decode(raw)),'ADAPTIVE_RESULT_NOT_READY')
        result=decode(raw)
        review=self.store.get('science/adaptive-reviews/'+request_id)[0]
        return {**result,'deliverySha256':sha(result),'ownerReview':decode(review) if review else None}

    def adaptive_review(self, request_id, value):
        result=self.adaptive_result(request_id)
        require(isinstance(value,dict) and set(value)=={'deliverySha256','decision','note'} and
                value['deliverySha256']==result['deliverySha256'] and
                value['decision'] in {'ACCEPTED_PRIVATELY','REVISION_REQUESTED'},'ADAPTIVE_OWNER_REVIEW_FIELDS')
        from .openai_planner import safe_text
        safe_text(value['note'])
        immutable(self.store,'science/adaptive-reviews/'+request_id,encode(value))
        return self.adaptive_result(request_id)

    def adaptive_halt(self, request_id, value):
        require(self.adaptive_enabled() and isinstance(value,dict) and
                set(value)=={'workerId','permitSha256','reason','localReceiptSha256'} and
                value['workerId']==self.broker.worker_id and digest(value['permitSha256']) and
                digest(value['localReceiptSha256']) and value['reason'] in {'CANCELLED','FAILED','STOP_FOR_REVIEW'},
                'ADAPTIVE_HALT_FIELDS')
        def stop(state,now):
            job=self.broker._job(state,'PIAI_'+request_id)
            require(job['request'].get('aiMode')=='OPENAI_API_ADAPTIVE' and
                    any(sha({**p,'state':'RESERVED'})==value['permitSha256'] for p in
                        job.get('adaptiveSegmentPermits',{}).values()),'ADAPTIVE_HALT_PERMIT')
            next_state='CANCELLED' if job['cancelRequested'] else 'FAILED' if value['reason']=='FAILED' else 'RECOVERY_REQUIRED'
            if job['state'] in {'CANCELLED','FAILED','RECOVERY_REQUIRED'}:
                require(job.get('adaptiveHalt')==value,'ADAPTIVE_HALT_CHANGED');return
            require(job['state']!='COMPLETED','ADAPTIVE_COMPLETED_HALT')
            job.update(state=next_state,updatedAt=now,adaptiveHalt=copy.deepcopy(value))
        self.broker._mutate(stop)
        return self.adaptive_state(request_id)
