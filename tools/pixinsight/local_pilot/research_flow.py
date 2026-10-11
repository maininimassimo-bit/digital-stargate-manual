"""Private, Owner-confirmed research sessions on the existing authenticated service."""
import base64
import copy
import secrets
from pathlib import Path
from .broker import require, encode, decode, opaque
from .intake import sha
from .source_profile import source_profile
from .research_knowledge import packet as knowledge_packet
from . import research_contract as contract
from tools.scientific_registry.ingestion_storage import immutable


# Research image dependencies are needed only when the feature is used.
# Preserve the existing stdlib-only import path for disabled services.
def measurement_projection(*args, **kwargs):
    from .adaptive_provider import measurement_projection as project
    return project(*args, **kwargs)


def provider_image(*args, **kwargs):
    from .image_previews import provider_image as image
    return image(*args, **kwargs)


def validate_curve(*args, **kwargs):
    from .image_previews import validate_curve as validate
    return validate(*args, **kwargs)


def generate(*args, **kwargs):
    from .research_provider import generate as send
    return send(*args, **kwargs)


class ResearchFlowMixin:
    def research_enabled(self):
        import os
        return self.adaptive_enabled() and os.environ.get('DSG_PIAI_RESEARCH') == 'LOCAL_WORKER_VERIFIED'

    def _research(self, request_id):
        require(opaque(request_id), 'RESEARCH_ID')
        self.intake(request_id)
        state, _ = self.broker._state()
        return copy.deepcopy(state.get('researchSessions', {}).get(request_id))

    def research_state(self, request_id):
        return self._research(request_id)

    def _research_mutate(self, request_id, operation):
        def apply(state, now):
            row = state.setdefault('researchSessions', {}).get(request_id)
            require(row is not None, 'RESEARCH_PENDING')
            return operation(row, now)
        return self.broker._mutate(apply)

    def research_analysis(self, request_id, value):
        require(self.research_enabled() and isinstance(value, dict) and set(value) ==
                {'workerId', 'analysis', 'instrument', 'executorSha256','backgroundROI'}, 'RESEARCH_ANALYSIS_FIELDS')
        require(value['workerId'] == self.broker.worker_id, 'RESEARCH_WORKER')
        intake = self.intake(request_id)
        require('researchPlanning' in intake['selection'] and
                source_profile(intake['selection'])['mode'] == 'LRGB', 'RESEARCH_LRGB_SOURCE_REQUIRED')
        analysis = value['analysis']
        require(set(analysis) == {'workerId', 'inputs', 'runtime', 'bindings', 'evidence', 'assetsBase64'} and
                analysis['workerId'] == self.broker.worker_id, 'RESEARCH_INITIAL_ANALYSIS')
        inputs = analysis['inputs']; evidence = analysis['evidence']
        from .adaptive_catalog import provenance
        facts=provenance(evidence['provenance'])
        require(facts['runtime'] == facts['registration'] == facts['backgroundROI'] == facts['stellarPSF'] == 'VERIFIED',
                'RESEARCH_INITIAL_PRECONDITIONS')
        require(isinstance(inputs, list) and [r.get('role') for r in inputs] == ['R','G','B','L'] and
                evidence['mode'] == 'LRGB' and evidence['intent'] == intake['selection']['prompt'] and
                evidence['provenance']['domain'] == 'LINEAR_ATTESTED' and
                evidence['provenance']['sourceSha256'] == sha(inputs), 'RESEARCH_INITIAL_BINDING')
        runtime=analysis['runtime']
        fields={'version','coreVersion','executorSha256','measurementSha256','starDetectorSha256',
                'dependenciesSha256','suiteSha256','models'}
        require(isinstance(runtime,dict) and set(runtime) == fields and
                runtime['version'] == 'DSG_PIAI_ADAPTIVE_RUNTIME_V2' and
                all(contract.digest(runtime[k]) for k in fields-{'version','coreVersion','models'}) and
                set(runtime['coreVersion']) == {'major','minor','release','revision','build'} and
                all(type(x) is int and 0 <= x <= 1000000 for x in runtime['coreVersion'].values()) and
                set(runtime['models']) == {'BLURX','NOISEX','STARX'}, 'RESEARCH_RUNTIME')
        for model in runtime['models'].values():
            require(set(model) == {'selectedVersion','fileSha256'} and contract.digest(model['fileSha256']) and
                    type(model['selectedVersion']) in (int,float) and 0 < model['selectedVersion'] < 100,
                    'RESEARCH_RUNTIME_MODEL')
        require(all(set(r) == {'role','sha256','imageIndex','width','height','channels'} and
                contract.digest(r['sha256']) and type(r['imageIndex']) is int and 0 <= r['imageIndex'] < 16 and
                all(type(r[k]) is int and 32 <= r[k] <= 12000 for k in ('width','height')) and
                r['channels'] == 1 and (r['width'],r['height']) == (inputs[0]['width'],inputs[0]['height'])
                for r in inputs), 'RESEARCH_INPUTS')
        require([r.get('role') for r in evidence['measurements']] == ['R','G','B','L'], 'RESEARCH_MEASUREMENT_ROLES')
        roi=value['backgroundROI']
        require(isinstance(roi,list) and len(roi) == 4 and all(type(n) is int for n in roi) and
                0 <= roi[0] < roi[2] <= inputs[0]['width'] and 0 <= roi[1] < roi[3] <= inputs[0]['height'] and
                min(roi[2]-roi[0],roi[3]-roi[1]) >= 32 and
                all(roi in r['report']['regions'] for r in evidence['measurements']),
                'RESEARCH_MEASURED_BACKGROUND_ROI_REQUIRED')
        projected = {}
        require(set(analysis['bindings']) == {'R','G','B','L'}, 'RESEARCH_BINDING_ROLES')
        for row, inp in zip(evidence['measurements'], inputs):
            binding = analysis['bindings'][row['role']]
            require(all(binding.get(k) == inp[r] for k,r in
                    (('sourceSha256','sha256'),('imageIndex','imageIndex'),('width','width'),('height','height'),('channels','channels'))) and
                    binding['adapterSha256'] == analysis['runtime']['measurementSha256'] and
                    binding['starDetectorSha256'] == analysis['runtime']['starDetectorSha256'] and
                    row['report']['coreVersion'] == runtime['coreVersion'], 'RESEARCH_INITIAL_MEASUREMENT_BINDING')
            projected[row['role']] = measurement_projection(row['report'], binding)
        require(contract.digest(value['executorSha256']) and value['executorSha256'] ==
                __import__('hashlib').sha256((Path(__file__).parent/'research_executor.jsh').read_bytes()).hexdigest(),
                'RESEARCH_EXECUTOR_CHANGED')
        instrument = value['instrument']
        require(isinstance(instrument, dict) and set(instrument) ==
                {'camera','rgbFilters','luminanceFilter','qe','whiteReference','limitations','profileSha256'},
                'RESEARCH_INSTRUMENT_FIELDS')
        from .openai_planner import safe_text
        for key in ('camera','luminanceFilter','qe','whiteReference','limitations'):
            safe_text(instrument[key])
        require(isinstance(instrument['rgbFilters'], list) and len(instrument['rgbFilters']) == 3 and
                all(isinstance(x,str) and len(x) <= 160 for x in instrument['rgbFilters']) and
                contract.digest(instrument['profileSha256']), 'RESEARCH_INSTRUMENT')
        self._research_initial_previews(analysis)
        knowledge, knowledge_sha = knowledge_packet()
        immutable(self.store, 'science/research-knowledge/'+knowledge_sha, encode(knowledge))
        immutable(self.store, 'science/research-analysis/'+request_id, encode(value))
        initial = {'id':'CP000','parentId':None,'stage':None,'step':None,'verified':True,
                   'domain':'LINEAR_ATTESTED','measurements':projected,'artifacts':inputs,
                   'photometricReceiptSha256':None,'photometry':None,'pixelStatistics':None}
        approved_policy = contract.policy(sha(value), sha(analysis['runtime']), knowledge_sha)
        def operation(state, _now):
            rows = state.setdefault('researchSessions', {})
            if request_id in rows:
                require(rows[request_id]['policy'] == approved_policy, 'RESEARCH_ANALYSIS_CONFLICT')
                return rows[request_id]
            require(len(rows) < 4 and len(encode(state)) < 524288, 'RESEARCH_SESSION_CAPACITY')
            rows[request_id] = {'version':contract.VERSION,'requestId':request_id,'policy':approved_policy,
                'policySha256':sha(approved_policy),
                'instrument':copy.deepcopy(instrument),'backgroundROI':copy.deepcopy(roi),
                'inputGeometry':[inputs[0]['width'],inputs[0]['height']],
                'approved':False,'status':'AWAITING_OWNER_PERIMETER','stage':'CALIBRATION','selectedId':'CP000',
                'checkpoints':{'CP000':initial},'decisions':[],'apiCalls':0,'nativeTrials':0,
                'pending':None,'final':None,'review':None,'cancelRequested':False}
            return rows[request_id]
        return self.broker._mutate(operation)

    def _research_initial_previews(self, analysis):
        previews = analysis['evidence']['previews']; raw_assets = analysis['assetsBase64']
        require(isinstance(previews,list) and len(previews) == len(raw_assets) == 4, 'RESEARCH_INITIAL_PREVIEWS')
        for preview, raw, inp in zip(previews, raw_assets, analysis['inputs']):
            require(preview['role'] == inp['role'] and preview['region'] is None, 'RESEARCH_INITIAL_PREVIEW_BINDING')
            validate_curve(preview['displayCurve'])
            require(preview['displayCurve'] == previews[0]['displayCurve'], 'RESEARCH_INITIAL_COMMON_DISPLAY')
            scale = min(1,512/max(inp['width'],inp['height']))
            provider_image(base64.b64decode(raw,validate=True),preview['sha256'],
                           expected_geometry=[max(1,round(inp[k]*scale)) for k in ('width','height')],expected_channels=1)

    def research_approve(self, request_id, value):
        require(self.research_enabled() and isinstance(value,dict) and set(value) == {'policySha256','nativeExecutionConfirmed','approximationAcknowledged'} and
                value['nativeExecutionConfirmed'] is True and value['approximationAcknowledged'] is True,
                'RESEARCH_OWNER_APPROVAL_REQUIRED')
        row=self._research(request_id)
        require(row and not row['cancelRequested'] and value['policySha256'] == sha(row['policy']) and
                row['status'] in ('AWAITING_OWNER_PERIMETER','AWAITING_DECISION'), 'RESEARCH_POLICY_CHANGED')
        approval_key='science/research-approvals/'+request_id
        previous,_=self.store.get(approval_key)
        approval={'requestId':request_id,'policy':row['policy'],'confirmation':value}
        receipt=decode(previous) if previous else {**approval,'confirmedAt':self.broker.clock().isoformat()}
        require({k:v for k,v in receipt.items() if k != 'confirmedAt'} == approval,'RESEARCH_APPROVAL_CONFLICT')
        immutable(self.store,approval_key,encode(receipt))
        def apply(row,_now):
            require(value['policySha256'] == sha(row['policy']), 'RESEARCH_POLICY_CHANGED')
            require(row['status'] in ('AWAITING_OWNER_PERIMETER','AWAITING_DECISION'), 'RESEARCH_APPROVAL_STATE')
            row['approved'] = True; row['status'] = 'AWAITING_DECISION'
            row.setdefault('approvedAt',receipt['confirmedAt'])
            return row
        return self._research_mutate(request_id,apply)

    def research_context(self, request_id):
        row = self._research(request_id)
        require(row is not None, 'RESEARCH_PENDING')
        raw,_ = self.store.get('science/research-analysis/'+request_id)
        analysis = decode(raw)
        raw,_ = self.store.get('science/research-knowledge/'+row['policy']['knowledgeSha256'])
        require(raw is not None and sha(decode(raw)) == row['policy']['knowledgeSha256'], 'RESEARCH_KNOWLEDGE_BINDING')
        return {'state':row,'analysis':analysis,'scientificKnowledge':decode(raw)}

    def research_decision(self, request_id, value):
        require(self.research_enabled() and isinstance(value,dict) and set(value) == {'workerId','comparison'} and
                value['workerId'] == self.broker.worker_id, 'RESEARCH_DECISION_REQUEST')
        row = self._research(request_id)
        if row and row['status'] == 'API_RESERVED':
            key='science/research-decisions/'+request_id+'/'+str(row['apiCalls'])
            result_raw,_=self.store.get(key)
            reservation_raw,_=self.store.get('science/research-reservations/'+request_id+'/'+str(row['apiCalls']))
            require(result_raw is not None and reservation_raw is not None,'RESEARCH_RESERVED_NO_KNOWN_RESPONSE_NO_RETRY')
            return self._research_complete(request_id,decode(reservation_raw),decode(result_raw))
        require(row and row['approved'] and row['status'] == 'AWAITING_DECISION' and
                not row['cancelRequested'] and row['apiCalls'] < contract.MAX_CALLS, 'RESEARCH_DECISION_STATE')
        knowledge_packet(row['policy']['knowledgeSha256'])
        assets = self._research_comparison(row, value['comparison'])
        owner = secrets.token_hex(32)
        binding = sha(row)
        def reserve(current,_now):
            require(sha(current) == binding, 'RESEARCH_CONCURRENT_DECISION')
            current['apiCalls'] += 1; current['status'] = 'API_RESERVED'
            current['pending'] = {'owner':owner,'ordinal':current['apiCalls'],'kind':'API'}
            return current
        reserved = self._research_mutate(request_id,reserve)
        immutable(self.store,'science/research-reservations/'+request_id+'/'+str(reserved['apiCalls']),encode(reserved))
        context = self.research_context(request_id); analysis = context['analysis']
        projection = {'intent':analysis['analysis']['evidence']['intent'],'stage':reserved['stage'],
            'selectedId':reserved['selectedId'],'instrument':analysis['instrument'],
            'checkpoints':[{k:v for k,v in n.items() if k not in ('artifacts',)} for n in reserved['checkpoints'].values()
                if n['id'] == reserved['selectedId'] or n.get('parentId') == reserved['selectedId'] and n.get('stage') == reserved['stage']],
            'comparisonLimitations':{'pairedStellarFits':'NOT_ESTABLISHED_NEW_DETECTION_PER_CHECKPOINT',
                'backgroundValidity':'NOT_ESTABLISHED','scientificAcceptance':'NOT_ESTABLISHED',
                'cropCoverage':'ONE_CENTRAL_256_PIXEL_CROP_PER_TRACK_NOT_FULL_FIELD_ARTIFACT_SURVEY',
                'interpretation':'Use observed native measures and common-display images; do not infer photon SNR or new resolution.'}}
        try:
            current = self._research(request_id)
            require(current and current['approved'] and not current['cancelRequested'] and
                    current['status'] == 'API_RESERVED' and current['pending'] == reserved['pending'] and
                    current['policySha256'] == reserved['policySha256'], 'RESEARCH_CANCELLED_OR_CHANGED_BEFORE_SEND')
            result = generate(self.adaptive_provider,reserved,projection,assets,owner=owner,
                              knowledge_sha256=reserved['policy']['knowledgeSha256'])
        except Exception:
            def fail(current,_now):
                if current['pending'] and current['pending'].get('owner') == owner:
                    current['status'] = 'API_INDETERMINATE_NO_RETRY' if owner in self.adaptive_provider._sent else 'VALIDATION_STOPPED_NO_SEND'
                return current
            self._research_mutate(request_id,fail)
            raise
        immutable(self.store,'science/research-decisions/'+request_id+'/'+str(reserved['apiCalls']),encode(result))
        return self._research_complete(request_id,reserved,result)

    def _research_complete(self,request_id,reserved,result):
        contract.decide(result['decision'],reserved)
        def complete(current,_now):
            require(current['status'] == 'API_RESERVED' and current['pending'] == reserved['pending'],
                    'RESEARCH_RESERVED_STATE_CHANGED')
            d = result['decision']; current['decisions'].append(result); current['pending'] = None
            if current['cancelRequested']:
                current['status']='STOPPED_FOR_REVIEW';return current
            if d['action'] == 'TEST':
                current['status'] = 'NATIVE_PENDING'; current['pending'] = {'kind':'NATIVE','decisionSha256':sha(result)}
            elif d['action'] == 'SELECT':
                current['selectedId'] = d['checkpointId']
                current['stage'] = contract.STAGES[contract.STAGES.index(current['stage'])+1]
                current['status'] = 'AWAITING_DECISION'
            else: current['status'] = 'AWAITING_FINAL_DELIVERY' if d['action'] == 'FINISH' else 'STOPPED_FOR_REVIEW'
            return current
        return self._research_mutate(request_id,complete)

    def _research_comparison(self, row, value):
        require(isinstance(value,dict) and set(value) == {'previews','assetsBase64'}, 'RESEARCH_COMPARISON_FIELDS')
        if row['selectedId'] == 'CP000' and not any(n.get('parentId') == 'CP000' for n in row['checkpoints'].values()):
            require(value == {'previews':[],'assetsBase64':[]}, 'RESEARCH_INITIAL_COMPARISON')
            context=self.research_context(row['requestId'])['analysis']['analysis']
            result=[]
            for i,(preview,raw,inp) in enumerate(zip(context['evidence']['previews'],context['assetsBase64'],context['inputs'])):
                scale=min(1,512/max(inp['width'],inp['height']))
                result.append({'raw':base64.b64decode(raw,validate=True),'sha256':preview['sha256'],
                    'geometry':[max(1,round(inp[k]*scale)) for k in ('width','height')],'channels':1,
                    'label':('INITIAL_R','INITIAL_G','INITIAL_B','INITIAL_L')[i]})
            return result
        control=row['selectedId']
        nodes=[row['checkpoints'][control]]+[n for n in row['checkpoints'].values()
            if n.get('parentId') == control and n.get('stage') == row['stage']]
        require(len(nodes) <= 4 and isinstance(value['previews'],list) and
                len(value['previews']) == len(value['assetsBase64']) == 4*len(nodes),
                'RESEARCH_ALL_SIBLING_PREVIEWS_REQUIRED')
        pairs={};result=[]
        expected_frames=[(node,role,crop) for node in nodes for crop in (False,True) for role in ('RGB','L')]
        for preview,raw,(node,role,crop) in zip(value['previews'],value['assetsBase64'],expected_frames):
            require(set(preview) == {'checkpointId','role','sha256','displayCurve','width','height','region'} and
                    preview['checkpointId'] == node['id'] and preview['role'] == role, 'RESEARCH_PAIR_BINDING')
            display=validate_curve(preview['displayCurve'])
            previous=pairs.setdefault(role,display);require(previous == display,'RESEARCH_SHARED_DISPLAY_REQUIRED')
            artifact=next(a for a in node['artifacts'] if a['role'] == role)
            w,h=artifact['width'],artifact['height'];scale=min(1,512/max(w,h))
            expected=[max(1,round(w*scale)),max(1,round(h*scale))]
            if crop:
                cw,ch=min(256,w),min(256,h);x,y=(w-cw)//2,(h-ch)//2
                require(preview['region'] == [x,y,x+cw,y+ch],'RESEARCH_NATIVE_CROP_BINDING')
                expected=[cw,ch]
            else:require(preview['region'] is None,'RESEARCH_FULL_FIELD_BINDING')
            require([preview['width'],preview['height']] == expected,'RESEARCH_PREVIEW_GRID')
            decoded=base64.b64decode(raw,validate=True)
            channels=3 if role == 'RGB' else 1
            provider_image(decoded,preview['sha256'],expected_geometry=expected,expected_channels=channels)
            label=('CONTROL' if node['id'] == control else 'CANDIDATE')+'_'+node['id']+'_'+role+('_CROP' if crop else '')
            result.append({'raw':decoded,'sha256':preview['sha256'],'geometry':expected,'channels':channels,'label':label})
        return result

    def research_reserve(self, request_id, value):
        require(self.research_enabled() and isinstance(value,dict) and set(value) == {'workerId','rootId','policySha256'} and
                value['workerId'] == self.broker.worker_id and opaque(value['rootId']), 'RESEARCH_NATIVE_RESERVE')
        def apply(row,_now):
            require(row['approved'] and not row['cancelRequested'] and value['policySha256'] == sha(row['policy']),
                    'RESEARCH_APPROVED_PERIMETER_REQUIRED')
            require(row['status'] in ('NATIVE_PENDING','NATIVE_RESERVED'), 'RESEARCH_NATIVE_RESERVE_STATE')
            if row['status'] == 'NATIVE_RESERVED':
                require(row['pending']['rootId'] == value['rootId'], 'RESEARCH_NATIVE_ROOT_CHANGED')
                return row['pending']
            require(row['nativeTrials'] < contract.MAX_TRIALS, 'RESEARCH_TRIAL_LIMIT')
            decision=row['decisions'][-1]['decision']
            require(decision['action'] == 'TEST' and decision['parentId'] == row['selectedId'], 'RESEARCH_NATIVE_DECISION')
            row['nativeTrials'] += 1
            row['pending']={'kind':'NATIVE','rootId':value['rootId'],'checkpointId':f"CP{row['nativeTrials']:03d}",
                'parentId':row['selectedId'],'stage':row['stage'],'step':decision['step'],
                'nonce':secrets.token_hex(16),'policySha256':sha(row['policy'])}
            row['status']='NATIVE_RESERVED'
            return row['pending']
        return self._research_mutate(request_id,apply)

    def research_start(self, request_id, value):
        require(self.research_enabled() and isinstance(value,dict) and set(value) == {'workerId','permitSha256','manifestSha256'} and
                value['workerId'] == self.broker.worker_id and contract.digest(value['manifestSha256']),
                'RESEARCH_NATIVE_START')
        def apply(row,_now):
            require(row['approved'] and not row['cancelRequested'] and row['status'] == 'NATIVE_RESERVED' and
                    value['permitSha256'] == sha(row['pending']), 'RESEARCH_SINGLE_NATIVE_START')
            row['status']='NATIVE_STARTED'
            row['pending']['manifestSha256']=value['manifestSha256']
            return {'status':'NATIVE_START_ACKNOWLEDGED','manifestSha256':value['manifestSha256']}
        return self._research_mutate(request_id,apply)

    def research_checkpoint(self, request_id, value):
        require(isinstance(value,dict) and set(value) == {'workerId','permit','verification'} and
                value['workerId'] == self.broker.worker_id, 'RESEARCH_CHECKPOINT_FIELDS')
        row=self._research(request_id); permit=value['permit']; verification=value['verification']
        require(row and row['status'] == 'NATIVE_STARTED' and isinstance(permit,dict) and
                {k:v for k,v in row['pending'].items() if k != 'manifestSha256'} == permit,
                'RESEARCH_CHECKPOINT_PERMIT')
        fields={'status','permitSha256','nativeManifestSha256','nativeReportSha256','originalGuard',
                'parentArtifacts','artifacts','parentMeasurements','parentBindings','measurements','bindings',
                'photometricReceiptSha256','photometry','pixelStatistics'}
        require(isinstance(verification,dict) and set(verification) == fields and
                verification['status'] == 'PHYSICALLY_VERIFIED' and verification['permitSha256'] == sha(permit) and
                verification['nativeManifestSha256'] == row['pending']['manifestSha256'] and
                contract.digest(verification['nativeReportSha256']), 'RESEARCH_NATIVE_RECEIPT')
        context=self.research_context(request_id); analysis=context['analysis']['analysis']
        require(verification['originalGuard'] == [{**r,'unchanged':True} for r in analysis['inputs']],
                'RESEARCH_ORIGINAL_GUARD')
        def artifacts(rows):
            require(isinstance(rows,list) and [r.get('role') for r in rows] == ['RGB','L'], 'RESEARCH_OUTPUT_ROLES')
            for r in rows:
                require(set(r) == {'role','sha256','width','height','channels','historySha256'} and
                        contract.digest(r['sha256']) and contract.digest(r['historySha256']) and
                        (r['width'],r['height']) == (analysis['inputs'][0]['width'],analysis['inputs'][0]['height']) and
                        r['channels'] == (3 if r['role'] == 'RGB' else 1), 'RESEARCH_OUTPUT_BINDING')
        artifacts(verification['parentArtifacts']); artifacts(verification['artifacts'])
        import math
        statistics=verification['pixelStatistics']
        require(isinstance(statistics,dict) and set(statistics) == {'parent','current'},'RESEARCH_PIXEL_STATISTICS')
        for phase,rows in (('parent',verification['parentArtifacts']),('current',verification['artifacts'])):
            require(set(statistics[phase]) == {'RGB','L'},'RESEARCH_PIXEL_ROLES')
            for artifact in rows:
                stats=statistics[phase][artifact['role']];count=artifact['width']*artifact['height']
                require(isinstance(stats,list) and len(stats) == artifact['channels'],'RESEARCH_PIXEL_CHANNELS')
                for item in stats:
                    require(isinstance(item,dict) and set(item) ==
                            {'sampleCount','negative','overOne','exactZero','exactOne','minimum','maximum'} and
                            item['sampleCount'] == count and
                            all(type(item[k]) is int and 0 <= item[k] <= count for k in
                                ('negative','overOne','exactZero','exactOne')) and
                            sum(item[k] for k in ('negative','overOne','exactZero','exactOne')) <= count and
                            all(type(item[k]) in (float,int) and math.isfinite(item[k]) for k in ('minimum','maximum')) and
                            item['minimum'] <= item['maximum'],'RESEARCH_FINITE_PIXEL_STATISTICS')
        parent=row['checkpoints'][permit['parentId']]
        if permit['parentId'] != 'CP000':
            require(verification['parentArtifacts'] == parent['artifacts'], 'RESEARCH_EXACT_PARENT_ARTIFACTS')
        projected={}
        require([r.get('role') for r in verification['measurements']] == ['RGB','L'] and
                set(verification['bindings']) == {'RGB','L'}, 'RESEARCH_CHECKPOINT_MEASUREMENTS')
        for measured,artifact in zip(verification['measurements'],verification['artifacts']):
            binding=verification['bindings'][artifact['role']]
            require(binding['sourceSha256'] == artifact['sha256'] and binding['imageIndex'] == 0 and
                    binding['adapterSha256'] == analysis['runtime']['measurementSha256'] and
                    binding['starDetectorSha256'] == analysis['runtime']['starDetectorSha256'] and
                    measured['report']['coreVersion'] == analysis['runtime']['coreVersion'] and
                    measured['report']['regions'] == [context['analysis']['backgroundROI'],
                        [0,0,artifact['width'],artifact['height']]], 'RESEARCH_OUTPUT_MEASUREMENT_RUNTIME')
            projected[artifact['role']]=measurement_projection(measured['report'],binding)
        photometric=verification['photometricReceiptSha256']
        require((contract.digest(photometric) if permit['step']['process'] == 'SPCC' else photometric is None),
                'RESEARCH_SPCC_NATIVE_PRODUCTS_REQUIRED')
        photo=verification['photometry']
        if permit['step']['process'] == 'SPCC':
            from .research_photometry import VERSION
            require(isinstance(photo,dict) and photo.get('version') == VERSION and
                    photo.get('status') == 'NATIVE_FIT_INSPECTABLE' and sha(photo) == photometric and
                    photo.get('profileSha256') == context['analysis']['instrument']['profileSha256'],
                    'RESEARCH_PHOTOMETRIC_PRODUCTS_BINDING')
        else:require(photo is None,'RESEARCH_UNEXPECTED_PHOTOMETRY')
        parent_projected={}
        require([r.get('role') for r in verification['parentMeasurements']] == ['RGB','L'] and
                set(verification['parentBindings']) == {'RGB','L'},'RESEARCH_PARENT_MEASUREMENTS')
        for measured,artifact in zip(verification['parentMeasurements'],verification['parentArtifacts']):
            b=verification['parentBindings'][artifact['role']]
            require(b['sourceSha256'] == artifact['sha256'] and b['imageIndex'] == 0 and
                    b['adapterSha256'] == analysis['runtime']['measurementSha256'] and
                    b['starDetectorSha256'] == analysis['runtime']['starDetectorSha256'] and
                    measured['report']['coreVersion'] == analysis['runtime']['coreVersion'] and
                    measured['report']['regions'] == [context['analysis']['backgroundROI'],
                        [0,0,artifact['width'],artifact['height']]],
                    'RESEARCH_PARENT_MEASUREMENT_BINDING')
            parent_projected[artifact['role']]=measurement_projection(measured['report'],b)
        immutable(self.store,'science/research-checkpoints/'+request_id+'/'+permit['checkpointId'],encode(value))
        def apply(current,_now):
            require(current['status'] == 'NATIVE_STARTED' and current['pending'] == row['pending'],
                    'RESEARCH_CHECKPOINT_CONCURRENT_CHANGE')
            if permit['parentId'] == 'CP000':
                current['checkpoints']['CP000']['artifacts']=verification['parentArtifacts']
                current['checkpoints']['CP000']['measurements']=parent_projected
                current['checkpoints']['CP000']['pixelStatistics']=statistics['parent']
            current['checkpoints'][permit['checkpointId']]={'id':permit['checkpointId'],'parentId':permit['parentId'],
                'stage':permit['stage'],'step':permit['step'],'verified':True,
                'domain':'NONLINEAR_ATTESTED' if permit['step']['process'] == 'STRETCH' else parent['domain'],
                'measurements':projected,'artifacts':verification['artifacts'],
                'photometricReceiptSha256':photometric,'photometry':photo,'pixelStatistics':statistics['current'],
                'verificationSha256':sha(value)}
            current['pending']=None
            current['status']='STOPPED_FOR_REVIEW' if current['cancelRequested'] else 'AWAITING_DECISION'
            return current
        return self._research_mutate(request_id,apply)

    def research_cancel(self, request_id, value):
        require(value == {}, 'RESEARCH_CANCEL_FIELDS')
        def apply(row,_now):
            require(row['final'] is None, 'RESEARCH_ALREADY_DELIVERED')
            row['cancelRequested']=True
            if row['status'] not in ('API_RESERVED','NATIVE_STARTED'):
                row['status']='STOPPED_FOR_REVIEW'
            return row
        return self._research_mutate(request_id,apply)

    def research_halt(self, request_id, value):
        require(isinstance(value,dict) and set(value) == {'workerId','reason'} and
                value['workerId'] == self.broker.worker_id and value['reason'] in
                ('LOCAL_REVIEW_REQUIRED','NATIVE_FAILURE_PRESERVED','NO_TERMINAL_RECEIPT'), 'RESEARCH_HALT')
        def apply(row,_now):
            require(row['final'] is None, 'RESEARCH_ALREADY_DELIVERED')
            require(row['status'] not in ('API_RESERVED','API_INDETERMINATE_NO_RETRY'),
                    'RESEARCH_API_ACCOUNTING_MUST_BE_PRESERVED')
            row['status']='RECOVERY_REQUIRED'; row['haltReason']=value['reason']
            return row
        return self._research_mutate(request_id,apply)

    def research_final(self, request_id, value):
        require(isinstance(value,dict) and set(value) == {'workerId','checkpointId','artifacts','archive','previewBase64','previewSha256'} and
                value['workerId'] == self.broker.worker_id, 'RESEARCH_FINAL_FIELDS')
        row=self._research(request_id)
        require(row and row['status'] in ('AWAITING_FINAL_DELIVERY','READY_FOR_OWNER_REVIEW') and not row['cancelRequested'] and
                value['checkpointId'] == row['selectedId'], 'RESEARCH_FINAL_STATE')
        from .intake import local_directory
        require(isinstance(value['artifacts'],list) and len(value['artifacts']) == 2, 'RESEARCH_FINAL_ARTIFACTS')
        for artifact,expected in zip(value['artifacts'],row['checkpoints'][row['selectedId']]['artifacts']):
            require(set(artifact) == {'role','sha256','localPath'} and artifact['role'] == expected['role'] and
                    artifact['sha256'] == expected['sha256'], 'RESEARCH_FINAL_ARTIFACT_BINDING')
            local_directory(artifact['localPath'])
        archive=value['archive']
        require(isinstance(archive,dict) and set(archive) == {'localPath','sha256','replayStatus'} and
                contract.digest(archive['sha256']) and archive['replayStatus'] == 'EVIDENCE_ARCHIVE_WITH_EXTERNAL_LICENSED_RUNTIME',
                'RESEARCH_FINAL_ARCHIVE')
        local_directory(archive['localPath'])
        selected=row['checkpoints'][row['selectedId']]['artifacts'][0]
        scale=min(1,512/max(selected['width'],selected['height']))
        raw=base64.b64decode(value['previewBase64'],validate=True)
        provider_image(raw,value['previewSha256'],expected_geometry=[max(1,round(selected[k]*scale)) for k in ('width','height')],expected_channels=3)
        immutable(self.store,'science/research-final/'+request_id,encode(value))
        def apply(current,_now):
            require(current['selectedId'] == value['checkpointId'] and not current['cancelRequested'], 'RESEARCH_FINAL_CHANGED')
            current['final']={k:v for k,v in value.items() if k not in ('workerId','previewBase64')}
            current['final']['receiptSha256']=sha(value)
            current['status']='READY_FOR_OWNER_REVIEW'
            return current
        return self._research_mutate(request_id,apply)

    def research_result(self, request_id):
        row=self._research(request_id)
        require(row and row['final'], 'RESEARCH_RESULT_PENDING')
        return decode(self.store.get('science/research-final/'+request_id)[0])

    def research_review(self, request_id, value):
        require(isinstance(value,dict) and set(value) == {'finalSha256','decision'} and
                value['decision'] in ('ACCEPT','REJECT'), 'RESEARCH_REVIEW_FIELDS')
        final=self.research_result(request_id)
        require(value['finalSha256'] == sha(final), 'RESEARCH_REVIEW_CHANGED')
        immutable(self.store,'science/research-reviews/'+request_id,encode(value))
        def apply(row,_now):
            require(row['status'] == 'READY_FOR_OWNER_REVIEW' and row['review'] in (None,value), 'RESEARCH_REVIEW_CONFLICT')
            row['review']=copy.deepcopy(value)
            return row
        return self._research_mutate(request_id,apply)
