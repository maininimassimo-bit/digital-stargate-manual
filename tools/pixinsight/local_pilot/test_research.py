"""Research protocol tests: fake provider only, no native/paid calls."""
import base64
import copy
import hashlib
import io
import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from PIL import Image
from .broker import encode, decode, ProtocolError
from .intake import sha
from .adaptive_provider import AdaptiveProvider
from . import test_intake as intake_fixture
from . import test_adaptive_flow as adaptive_fixture
from .test_native_measurements import fixture
from .research_knowledge import packet, instructions
from .research_photometry import inspect
from . import research_contract as contract


def png(channels=1):
    out=io.BytesIO();Image.new('L' if channels == 1 else 'RGB',(64,64),64 if channels == 1 else (64,64,64)).save(out,format='PNG')
    return out.getvalue()


class ResearchTests(unittest.TestCase):
    def setUp(self):
        intake_fixture.IntakeTests.setUp(self)
        self.activation=patch.dict('os.environ',{'DSG_PIAI_ADAPTIVE':'LOCAL_WORKER_VERIFIED','DSG_PIAI_RESEARCH':'LOCAL_WORKER_VERIFIED'})
        self.activation.start();self.addCleanup(self.activation.stop)
        self.calls=[];self.action='TEST';self.process='SPCC';self.selected=None
        self.parameters={}
        self.portal.adaptive_provider=AdaptiveProvider('mock','gpt-6-luna',send=self.send)
        self.selection=intake_fixture.IntakeTests.selection(self);self.selection['prompt']='Preservare le strutture deboli'
        self.selection['researchPlanning']={'dataTransferConfirmed':True,'pixelStatisticsConfirmed':True,'previewTransferConfirmed':True}
        self.request_id=self.selection['requestId'];self.portal.create_intake(self.selection)

    def send(self,payload):
        self.calls.append(payload)
        projection=json.loads(payload['input'][0]['content'][0]['text'])
        decision={'action':self.action,'bindingSha256':payload['tools'][0]['parameters']['properties']['bindingSha256']['enum'][0],
            'parentId':projection['selectedId'],'checkpointId':self.selected,
            'step':{'process':self.process,'parameters':self.parameters} if self.action == 'TEST' else None,
            'rationale':'Prova sullo stesso genitore; verificare gli artefatti prima della scelta.',
            'limitations':'Misure descrittive; accettazione scientifica separata.'}
        return {'status':'completed','id':'resp_mock','model':'gpt-6-luna','output':[{'type':'function_call',
            'status':'completed','name':'choose_pixinsight_action','arguments':json.dumps(decision)}],
            'usage':{'input_tokens':100,'output_tokens':20,'total_tokens':120}}

    def analysis(self):
        body=adaptive_fixture.AdaptiveFlowTests.body(self)
        initial=body['evidence']['previews'][0];raw=body['assetsBase64'][0]
        body['evidence']['previews']=[{**copy.deepcopy(initial),'role':role} for role in ('R','G','B','L')]
        body['assetsBase64']=[raw]*4
        return {'workerId':self.broker.worker_id,'analysis':body,
            'backgroundROI':[0,0,64,64],
            'instrument':{'camera':'QHY695A','rgbFilters':['ZWO R','ZWO G','ZWO B'],'luminanceFilter':'Optolong L-Pro',
                          'qe':'Ideal QE curve','whiteReference':'Average Spiral Galaxy',
                          'limitations':'Nominal curves, substitute QE; L-Pro only L.','profileSha256':'d'*64},
            'executorSha256':hashlib.sha256((Path(__file__).parent/'research_executor.jsh').read_bytes()).hexdigest()}

    def approve(self):
        state=self.portal.research_analysis(self.request_id,self.analysis())
        return self.portal.research_approve(self.request_id,{'policySha256':sha(state['policy']),
            'nativeExecutionConfirmed':True,'approximationAcknowledged':True})

    def post(self,action,**body):
        return getattr(self.portal,'research_'+action)(self.request_id,{'workerId':self.broker.worker_id,**body})

    def comparison(self):
        from .image_previews import curve
        state=self.portal.research_state(self.request_id);parent=state['selectedId']
        nodes=[state['checkpoints'][parent]]+[n for n in state['checkpoints'].values()
            if n.get('parentId') == parent and n.get('stage') == state['stage']]
        if len(nodes) == 1 and parent == 'CP000':return {'previews':[],'assetsBase64':[]}
        previews=[];assets=[]
        for node in nodes:
            for crop in (False,True):
                for role in ('RGB','L'):
                    raw=png(3 if role == 'RGB' else 1)
                    previews.append({'checkpointId':node['id'],'role':role,'sha256':hashlib.sha256(raw).hexdigest(),
                        'displayCurve':curve(.05),'width':64,'height':64,'region':[0,0,64,64] if crop else None})
                    assets.append(base64.b64encode(raw).decode())
        return {'previews':previews,'assetsBase64':assets}

    def checkpoint(self):
        state=self.portal.research_state(self.request_id)
        permit=self.post('reserve',rootId='2'*32,policySha256=state['policySha256'])
        self.post('start',permitSha256=sha(permit),manifestSha256='1'*64)
        def rows(key):
            artifacts=[];reports=[];bindings={};stats={}
            for role,channels in (('RGB',3),('L',1)):
                source=sha({'id':key,'role':role});measured,binding=fixture()
                measured['sourceSha256']=source;measured['channels']=channels
                measured['regions']=[[0,0,64,64],[0,0,64,64]]
                noise=measured['noise'][0];fit=measured['fits'][0]
                measured['noise']=[{**copy.deepcopy(noise),'region':region,'channel':channel} for region in (0,1) for channel in range(channels)]
                measured['fits']=[{**copy.deepcopy(fit),'channel':channel} for channel in range(channels)]
                binding['sourceSha256']=source;binding['channels']=channels
                bindings[role]=binding;reports.append({'role':role,'report':measured})
                artifacts.append({'role':role,'sha256':source,'width':64,'height':64,'channels':channels,'historySha256':'f'*64})
                stats[role]=[{'sampleCount':4096,'negative':0,'overOne':0,'exactZero':0,'exactOne':0,'minimum':.01,'maximum':.9}]*channels
            return artifacts,reports,bindings,stats
        pa,pm,pb,pp=rows(permit['parentId']);ca,cm,cb,cp=rows(permit['checkpointId'])
        photo={'version':'DSG_SPCC_FIT_EVIDENCE_V1','status':'NATIVE_FIT_INSPECTABLE','profileSha256':'d'*64,
               'whiteReferenceInsideFitRange':'INSIDE_EXPORTED_RANGE_FROM_ROUNDED_NATIVE_PRODUCTS'} if permit['step']['process'] == 'SPCC' else None
        verification={'status':'PHYSICALLY_VERIFIED','permitSha256':sha(permit),'nativeManifestSha256':'1'*64,
            'nativeReportSha256':'e'*64,'originalGuard':[{**r,'unchanged':True} for r in self.analysis()['analysis']['inputs']],
            'parentArtifacts':pa,'artifacts':ca,'parentMeasurements':pm,'parentBindings':pb,'measurements':cm,'bindings':cb,
            'pixelStatistics':{'parent':pp,'current':cp},'photometricReceiptSha256':sha(photo) if photo else None,'photometry':photo}
        return self.post('checkpoint',permit=permit,verification=verification)

    def test_knowledge_changes_block_before_paid_send(self):
        value,digest=packet();text,same=instructions(digest)
        self.assertEqual(digest,same);self.assertIn('SPCC',text);self.assertIn('BlurXTerminator',text)
        self.assertLess(len(encode(value)),49152)
        with self.assertRaisesRegex(ProtocolError,'KNOWLEDGE_CHANGED'):instructions('f'*64)

    def test_analysis_is_idempotent_and_cannot_launch_without_owner(self):
        body=self.analysis();state=self.portal.research_analysis(self.request_id,body)
        self.assertEqual(self.portal.research_analysis(self.request_id,decode(encode(body))),state)
        self.assertEqual(self.calls,[]);self.assertIsNone(self.broker.claim(self.broker.worker_id,'2'*32))
        with self.assertRaisesRegex(ProtocolError,'DECISION_STATE'):self.post('decision',comparison={'previews':[],'assetsBase64':[]})

    def test_portable_guide_reaches_function_payload_with_no_private_paths(self):
        self.approve();state=self.post('decision',comparison={'previews':[],'assetsBase64':[]})
        self.assertEqual(state['status'],'NATIVE_PENDING')
        payload=self.calls[0]
        self.assertIn('Each candidate must derive directly from that parent',payload['instructions'])
        self.assertFalse(payload['store']);self.assertFalse(payload['parallel_tool_calls'])
        self.assertEqual(payload['tool_choice']['name'],'choose_pixinsight_action')
        self.assertNotIn('masterDirectory',json.dumps(payload));self.assertNotIn('F:',json.dumps(payload))
        self.assertNotIn('sourceSha256',json.dumps(payload));self.assertNotIn('imageIndex',json.dumps(payload))

    def test_lost_provider_response_is_counted_once_and_never_retried(self):
        self.approve()
        def lost(payload):self.calls.append(payload);raise TimeoutError()
        self.portal.adaptive_provider._send=lost
        with self.assertRaisesRegex(ProtocolError,'NO_RETRY'):self.post('decision',comparison={'previews':[],'assetsBase64':[]})
        state=self.portal.research_state(self.request_id)
        self.assertEqual(state['status'],'API_INDETERMINATE_NO_RETRY');self.assertEqual(state['apiCalls'],1)
        with self.assertRaises(ProtocolError):self.post('decision',comparison={'previews':[],'assetsBase64':[]})
        self.assertEqual(len(self.calls),1)

    def test_cancel_during_paid_send_accounts_known_receipt_without_launch(self):
        self.approve();original=self.portal.adaptive_provider._send
        def cancelling(payload):self.portal.research_cancel(self.request_id,{});return original(payload)
        self.portal.adaptive_provider._send=cancelling
        state=self.post('decision',comparison={'previews':[],'assetsBase64':[]})
        self.assertEqual(state['status'],'STOPPED_FOR_REVIEW');self.assertEqual(len(state['decisions']),1)
        self.assertEqual(state['decisions'][0]['provider']['usage']['total_tokens'],120)

    def test_cancel_after_reservation_prevents_paid_send(self):
        from . import research_flow
        self.approve();original=research_flow.immutable
        def cancelling(store,key,value):
            result=original(store,key,value)
            if key.startswith('science/research-reservations/'):
                self.portal.research_cancel(self.request_id,{})
            return result
        with patch.object(research_flow,'immutable',side_effect=cancelling):
            with self.assertRaisesRegex(ProtocolError,'BEFORE_SEND'):
                self.post('decision',comparison={'previews':[],'assetsBase64':[]})
        self.assertEqual(self.calls,[])
        self.assertEqual(self.portal.research_state(self.request_id)['status'],'VALIDATION_STOPPED_NO_SEND')

    def test_factory_must_match_approved_bytes_including_snapshot(self):
        from .research_native import validate_factory
        library=Path(__file__).parent
        runtime={'executorSha256':sha({'controller':hashlib.sha256((library/'adaptive_executor.jsh').read_bytes()).hexdigest(),
            'factory':hashlib.sha256((library/'adaptive_native.jsh').read_bytes()).hexdigest()})}
        validate_factory(runtime)
        with tempfile.TemporaryDirectory() as temp:
            factory=Path(temp)/'adaptive_native.jsh'
            factory.write_bytes((library/'adaptive_native.jsh').read_bytes()+b'\n// altered\n')
            with self.assertRaisesRegex(ProtocolError,'APPROVED_FACTORY_CHANGED'):
                validate_factory(runtime,factory)

    def test_delivery_replay_rechecks_native_files_and_archive(self):
        from . import research_worker
        coordinator=object.__new__(research_worker.ResearchWorker)
        coordinator.post=__import__('unittest.mock',fromlist=['Mock']).Mock(return_value={'status':'READY_FOR_OWNER_REVIEW'})
        # The production worker accepts Windows paths only. On Linux CI adapt
        # that boundary while exercising the real file hashes and delivery flow.
        with tempfile.TemporaryDirectory() as temp, patch.object(research_worker,'safe_path',
                side_effect=lambda value,root:Path(value).resolve()) if __import__('os').name != 'nt' else __import__('contextlib').nullcontext():
            session=Path(temp);attempt=session/'CP001';attempt.mkdir()
            (attempt/'result.json').write_text('{}',encoding='utf-8')
            (attempt/'binding.json').write_text('{}',encoding='utf-8')
            image=session/'RGB.xisf';image.write_bytes(b'original pixels')
            archive=session/'evidence.zip';archive.write_bytes(b'original archive')
            rows=[{'role':'RGB','path':str(image),'sha256':research_worker.fingerprint(image)}]
            coordinator.artifacts=lambda *_:rows
            context={'state':{'requestId':self.request_id,'selectedId':'CP001'}}
            body={'checkpointId':'CP001','artifacts':[{'role':'RGB','localPath':str(image),'sha256':rows[0]['sha256']}],
                'archive':{'localPath':str(archive),'sha256':research_worker.fingerprint(archive)}}
            (session/'delivery.json').write_text(json.dumps(body),encoding='utf-8')
            with patch.object(research_worker.native,'verify') as verify:
                self.assertEqual(coordinator.deliver(context,session),'READY_FOR_OWNER_REVIEW')
                verify.assert_called_once();coordinator.post.reset_mock()
                archive.write_bytes(b'changed archive')
                with self.assertRaisesRegex(ProtocolError,'ARCHIVE_CHANGED'):coordinator.deliver(context,session)
                coordinator.post.assert_not_called()
                image.write_bytes(b'changed pixels')
                with self.assertRaisesRegex(ProtocolError,'FILE_CHANGED'):coordinator.deliver(context,session)
                coordinator.post.assert_not_called()
            with patch.object(research_worker.native,'verify',side_effect=ProtocolError('NATIVE_CHANGED')):
                with self.assertRaisesRegex(ProtocolError,'NATIVE_CHANGED'):coordinator.deliver(context,session)
                coordinator.post.assert_not_called()

    def test_native_start_has_no_replay_and_requires_exact_permit(self):
        self.approve();self.post('decision',comparison={'previews':[],'assetsBase64':[]})
        permit=self.post('reserve',rootId='2'*32,policySha256=self.portal.research_state(self.request_id)['policySha256'])
        self.assertEqual(permit,self.post('reserve',rootId='2'*32,policySha256=permit['policySha256']))
        with self.assertRaises(ProtocolError):self.post('start',permitSha256='0'*64,manifestSha256='1'*64)
        self.post('start',permitSha256=sha(permit),manifestSha256='1'*64)
        with self.assertRaisesRegex(ProtocolError,'SINGLE_NATIVE_START'):self.post('start',permitSha256=sha(permit),manifestSha256='1'*64)

    def test_stage_and_exact_parent_gate_reject_provider_inventions(self):
        state=self.approve();state['status']='API_RESERVED';state['apiCalls']=1
        decision={'action':'TEST','bindingSha256':sha(state),'parentId':'CP000','checkpointId':None,
                  'step':{'process':'VIVIDNESS','parameters':{'saturation':.1}},'rationale':'Prova','limitations':'Limiti'}
        with self.assertRaisesRegex(ProtocolError,'STAGE_PROCESS'):contract.decide(decision,state)
        decision['step']={'process':'SPCC','parameters':{}};decision['parentId']='CP009'
        with self.assertRaisesRegex(ProtocolError,'EXACT_PARENT'):contract.decide(decision,state)
        decision['parentId']='CP000';decision['step']['parameters']={'code':'arbitrary'}
        with self.assertRaisesRegex(ProtocolError,'PINNED_PROFILE'):contract.decide(decision,state)

    def test_approved_intake_cannot_be_withdrawn_or_used_by_legacy_queue(self):
        self.approve()
        with self.assertRaisesRegex(ProtocolError,'USE_CANCEL'):self.portal.withdraw_intake(self.request_id,{})
        with self.assertRaisesRegex(ProtocolError,'DISTINCT_PLAN'):self.portal.propose(self.request_id,intake_fixture.IntakeTests.plan(self))

    def test_full_sibling_cycle_preserves_control_and_requires_final_owner_review(self):
        self.approve()
        for process,parameters in (('SPCC',{}),('STRETCH',{'targetBackground':.06}),('COMBINE',{})):
            self.action='TEST';self.process=process;self.parameters=parameters;self.selected=None
            self.post('decision',comparison=self.comparison());state=self.checkpoint()
            self.action='SELECT';self.selected=list(state['checkpoints'])[-1]
            state=self.post('decision',comparison=self.comparison())
            while state['stage'] in ('DETAIL','NOISE','PRESENTATION'):
                self.selected=state['selectedId'];state=self.post('decision',comparison=self.comparison())
        self.assertEqual(state['stage'],'FINAL');self.action='FINISH';self.selected=None
        state=self.post('decision',comparison=self.comparison());self.assertEqual(state['status'],'AWAITING_FINAL_DELIVERY')
        raw=png(3)
        result=self.post('final',checkpointId=state['selectedId'],
            artifacts=[{'role':r['role'],'sha256':r['sha256'],'localPath':'F:/private/'+r['role']+'.xisf'} for r in state['checkpoints'][state['selectedId']]['artifacts']],
            archive={'localPath':'F:/private/evidence.zip','sha256':'9'*64,'replayStatus':'EVIDENCE_ARCHIVE_WITH_EXTERNAL_LICENSED_RUNTIME'},
            previewBase64=base64.b64encode(raw).decode(),previewSha256=hashlib.sha256(raw).hexdigest())
        self.assertEqual(result['status'],'READY_FOR_OWNER_REVIEW');self.assertIsNone(result['review'])
        self.assertEqual(result['nativeTrials'],3);self.assertEqual(result['apiCalls'],10)
        self.assertEqual(len(result['checkpoints']),4)
        self.assertEqual(self.portal.research_result(self.request_id)['artifacts'][0]['sha256'],result['final']['artifacts'][0]['sha256'])
        self.portal.research_review(self.request_id,{'finalSha256':result['final']['receiptSha256'],'decision':'ACCEPT'})
        self.assertEqual(self.portal.research_state(self.request_id)['review']['decision'],'ACCEPT')
        self.assertNotIn('publication',result['review'] or {})

    def test_missing_any_sibling_image_blocks_paid_selection(self):
        self.approve();self.post('decision',comparison=self.comparison());self.checkpoint()
        self.action='SELECT';self.selected='CP001';body=self.comparison();body['assetsBase64'].pop()
        with self.assertRaisesRegex(ProtocolError,'ALL_SIBLING'):self.post('decision',comparison=body)
        self.assertEqual(len(self.calls),1)

    def test_known_provider_receipt_is_reconciled_without_second_send(self):
        self.approve()
        with patch.object(self.portal,'_research_complete',side_effect=RuntimeError('crash after durable receipt')):
            with self.assertRaises(RuntimeError):self.post('decision',comparison=self.comparison())
        self.assertEqual(self.portal.research_state(self.request_id)['status'],'API_RESERVED')
        state=self.post('decision',comparison={'previews':[],'assetsBase64':[]})
        self.assertEqual(state['status'],'NATIVE_PENDING');self.assertEqual(len(self.calls),1)

    def test_http_role_boundary_keeps_native_actions_and_owner_consent_separate(self):
        from http.server import HTTPServer
        import threading
        import urllib.request
        import urllib.error
        from .transport_http import handler_for,AuthError
        token='c'*64;origin='https://owner.invalid'
        def owner(value):
            if value != 'owner-test':raise AuthError()
        server=HTTPServer(('127.0.0.1',0),handler_for(self.broker,owner,origin,hashlib.sha256(token.encode()).hexdigest(),self.portal))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
        def post(path,body,credential=token,owner_origin=None):
            headers={'Authorization':'Bearer '+credential,'Content-Type':'application/json'}
            if owner_origin:headers['Origin']=owner_origin
            request=urllib.request.Request('http://127.0.0.1:'+str(server.server_port)+path,encode(body),headers,method='POST')
            with urllib.request.urlopen(request,timeout=5) as response:return decode(response.read())
        base='/v1/worker/science/intakes/'+self.request_id+'/research-'
        state=post(base+'analysis',self.analysis())
        approval={'policySha256':state['policySha256'],'nativeExecutionConfirmed':True,'approximationAcknowledged':True}
        with self.assertRaises(urllib.error.HTTPError) as denied:post(base+'approve',approval)
        self.assertEqual(denied.exception.code,404)
        with self.assertRaises(urllib.error.HTTPError) as denied:post('/v1/science/intakes/'+self.request_id+'/research-approve',approval)
        self.assertEqual(denied.exception.code,403)
        post('/v1/science/intakes/'+self.request_id+'/research-approve',approval,'owner-test',origin)
        for action in ('analysis','decision','reserve','start','checkpoint','final','halt'):
            with self.subTest(action=action),self.assertRaises(urllib.error.HTTPError) as denied:
                post(base+action,{},'owner-test',origin)
            self.assertEqual(denied.exception.code,403)
            with self.subTest(action=action),self.assertRaises(urllib.error.HTTPError) as denied:
                post('/v1/science/intakes/'+self.request_id+'/research-'+action,{},'owner-test',origin)
            self.assertEqual(denied.exception.code,404)

    def test_disabled_research_cannot_reserve_or_start_and_preserves_old_mode(self):
        self.approve();self.post('decision',comparison=self.comparison())
        with patch.dict('os.environ',{'DSG_PIAI_RESEARCH':''}):
            self.assertFalse(self.portal.research_enabled());self.assertTrue(self.portal.adaptive_enabled())
            with self.assertRaises(ProtocolError):self.post('reserve',rootId='2'*32,policySha256=self.portal.research_state(self.request_id)['policySha256'])
        self.assertEqual(self.portal.research_state(self.request_id)['nativeTrials'],0)


class PhotometryTests(unittest.TestCase):
    def products(self):
        header='x,y,alpha,delta,cat_0,cat_1,cat_2,img_0,img_1,img_2,cat_01,cat_21,img_01,img_21\n'
        csv=header+''.join(f'{i+1},{i+1},1,1,1,1,1,1,1,1,{x},{x},{x},{x}\n' for i,x in enumerate((.5,1,1.5)))
        log='f_R : R/G = +1.000000*FR/FG + 0.000000, sigma = 0.010000\nf_B : B/G = +1.000000*FB/FG + 0.000000, sigma = 0.020000\nW_R : 1.0000\nW_G : 1.0000\nW_B : 1.0000\n'
        return csv.encode(),log.encode()

    def test_native_fits_and_exported_sample_statistics_remain_distinct(self):
        result=inspect(*self.products(),geometry=[64,64],profile_sha256='a'*64)
        self.assertEqual(result['commonRGBMatches'],3)
        self.assertEqual(result['fits']['R/G']['exportedResidualRMS'],0)
        self.assertEqual(result['fits']['R/G']['nativeRobustSigma'],.01)
        self.assertEqual(result['fitRejectionCount'],'NOT_EXPORTED')
        self.assertTrue(result['fits']['R/G']['whiteInsideExportedRange'])

    def test_missing_or_duplicate_native_fit_cannot_be_accepted(self):
        csv,log=self.products()
        for bad in (b'',log+log,log.replace(b'+1.000000*FR',b'+nan*FR')):
            with self.subTest(bad=bad[:30]),self.assertRaises(ProtocolError):inspect(csv,bad,geometry=[64,64],profile_sha256='a'*64)


if __name__ == '__main__':unittest.main()
