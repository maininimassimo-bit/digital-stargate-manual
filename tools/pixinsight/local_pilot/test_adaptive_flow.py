"""Owner/worker admission and crash accounting, with mocked paid transport."""
import base64
import copy
import json
import hashlib
from http.server import HTTPServer
import threading
import urllib.request
import urllib.error
import unittest
from unittest.mock import patch

from . import test_intake as intake_fixture
from .test_adaptive_provider import inputs, response
from .adaptive_provider import AdaptiveProvider
from .adaptive_flow import EXECUTION_POLICY_VERSION
from .adaptive_ledger import DecisionJournal
from .broker import ProtocolError, encode, decode
from .intake import sha
from .transport_http import handler_for,AuthError


class AdaptiveFlowTests(unittest.TestCase):
    def setUp(self):
        intake_fixture.IntakeTests.setUp(self)
        self.calls=[]
        self.portal.adaptive_provider=AdaptiveProvider('mock','gpt-6-luna',send=self.send)
        self.activation=patch.dict('os.environ',{'DSG_PIAI_ADAPTIVE':'LOCAL_WORKER_VERIFIED'})
        self.activation.start();self.addCleanup(self.activation.stop)
        self.selection=intake_fixture.IntakeTests.selection(self)
        self.selection['prompt']='Preservare le strutture deboli'
        self.selection['adaptivePlanning']={'dataTransferConfirmed':True,'pixelStatisticsConfirmed':True,'previewTransferConfirmed':True}
        self.request_id=self.selection['requestId']
        self.portal.create_intake(self.selection)

    def send(self, payload):
        self.calls.append(payload)
        result=response()
        decision=json.loads(result['output'][0]['content'][0]['text'])
        decision['graph']['steps'] += [{'process':'STRETCH','parameters':{'targetBackground':.12}},
                                     {'process':'COMBINE','parameters':{}}]
        result['output'][0]['content'][0]['text']=json.dumps(decision)
        return result

    def body(self):
        _, evidence, bindings, assets=inputs()
        for digit, measured in zip(('5','6','7','8'), evidence['measurements']):
            measured['report']['sourceSha256']=digit*64
            bindings[measured['role']]['sourceSha256']=digit*64
        rows=[{'role':r,'sha256':bindings[r]['sourceSha256'], **{k:bindings[r][k] for k in ('imageIndex','width','height','channels')}}
              for r in ('R','G','B','L')]
        evidence['provenance']['sourceSha256']=sha(rows)
        runtime={'version':'DSG_PIAI_ADAPTIVE_RUNTIME_V2','coreVersion':evidence['measurements'][0]['report']['coreVersion'],
                 'executorSha256':'1'*64,'measurementSha256':'b'*64,'starDetectorSha256':'c'*64,
                 'dependenciesSha256':'2'*64,'suiteSha256':'3'*64,
                 'models':{name:{'selectedVersion':v,'fileSha256':'4'*64} for name,v in
                           (('BLURX',4),('NOISEX',3.1),('STARX',11))}}
        return {'workerId':self.broker.worker_id,'inputs':rows,'runtime':runtime,'evidence':evidence,
                'bindings':bindings,'assetsBase64':[base64.b64encode(a).decode() for a in assets]}

    def test_analysis_consent_creates_proposal_but_no_legacy_native_claim(self):
        body=self.body();state=self.portal.generate_adaptive(self.request_id,body)
        self.assertEqual(state['plan']['decision']['action'],'PROPOSE_GRAPH')
        self.assertEqual(state['cursor']['usage']['total_tokens'],120)
        self.assertIsNone(state['executionPolicy'])
        self.assertIsNone(self.broker.claim(self.broker.worker_id,'2'*32))
        self.assertEqual(self.portal.generate_adaptive(self.request_id,body),state)
        self.assertEqual(len(self.calls),1)

    def test_exact_owner_approval_is_separate_from_analysis_and_not_acceptance(self):
        state=self.portal.generate_adaptive(self.request_id,self.body())
        value={'proposalSha256':state['proposalSha256'],'adaptationScope':'NEXT_STEP_PARAMETERS_ONLY',
               'nativeExecutionConfirmed':True}
        with self.assertRaisesRegex(ProtocolError,'EXACT_GRAPH'):
            self.portal.approve_adaptive(self.request_id,{**value,'proposalSha256':'9'*64})
        approved=self.portal.approve_adaptive(self.request_id,value)
        self.assertEqual(approved['executionPolicy']['version'],EXECUTION_POLICY_VERSION)
        self.assertEqual(approved['scientificAcceptance'],'NONE')
        self.assertIsNone(self.broker.claim(self.broker.worker_id,'2'*32))
        self.assertEqual(self.portal.approve_adaptive(self.request_id,value),approved)

    def test_lost_provider_response_is_not_retried(self):
        def lost(payload):self.calls.append(payload);raise TimeoutError()
        self.portal.adaptive_provider=AdaptiveProvider('mock','gpt-6-luna',send=lost)
        body=self.body();result=self.portal.generate_adaptive(self.request_id,body)
        self.assertEqual(result['cursor']['state'],'RESERVED')
        self.assertFalse(result['cursor']['usageComplete'])
        self.portal.generate_adaptive(self.request_id,body)
        self.assertEqual(len(self.calls),1)

    def test_crash_after_result_publication_recovers_without_paid_send(self):
        body=self.body()
        with patch.object(DecisionJournal,'record',side_effect=RuntimeError('synthetic crash')):
            with self.assertRaises(RuntimeError):self.portal.generate_adaptive(self.request_id,body)
        result=self.portal.generate_adaptive(self.request_id,body)
        self.assertTrue(result['cursor']['usageComplete'])
        self.assertEqual(result['cursor']['usage']['total_tokens'],120)
        self.assertEqual(len(self.calls),1)

    def test_source_runtime_and_worker_changes_fail_before_provider(self):
        for changed in ('source','runtime','worker'):
            body=self.body()
            if changed=='source':body['inputs'][0]['sha256']='9'*64
            elif changed=='runtime':body['runtime']['models']['BLURX']['selectedVersion']=0
            else:body['workerId']='9'*32
            with self.assertRaises(ValueError):self.portal.generate_adaptive(self.request_id,body)
        self.assertEqual(self.calls,[])

    def test_preview_consent_is_owner_intake_authority(self):
        selection=copy.deepcopy(self.selection);selection['requestId']='9'*32
        selection['adaptivePlanning']['previewTransferConfirmed']=False
        with self.assertRaisesRegex(ProtocolError,'CONSENT'):
            self.portal.create_intake(selection)
        self.assertEqual(self.calls,[])

    def test_withdrawn_adaptive_intake_stays_readable_without_creating_job(self):
        self.portal.withdraw_intake(self.request_id,{})
        self.assertEqual(self.portal.intakes()[0]['state'],'WITHDRAWN')
        self.assertIsNone(self.portal.intakes()[0]['adaptive'])
        with self.assertRaisesRegex(ProtocolError,'WITHDRAWN'):
            self.portal.generate_adaptive(self.request_id,self.body())
        self.assertEqual(self.calls,[])

    def test_loopback_routes_keep_owner_approval_distinct_from_worker_analysis(self):
        worker_token='c'*64;origin='https://owner.invalid'
        def owner(token):
            if token!='owner-test':raise AuthError()
        server=HTTPServer(('127.0.0.1',0),handler_for(self.broker,owner,origin,
            hashlib.sha256(worker_token.encode()).hexdigest(),self.portal))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
        def post(path,body,token=worker_token,owner_origin=None):
            headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'}
            if owner_origin:headers['Origin']=owner_origin
            request=urllib.request.Request('http://127.0.0.1:'+str(server.server_port)+path,
                encode(body),headers,method='POST')
            with urllib.request.urlopen(request,timeout=5) as response:return decode(response.read())
        base='/v1/worker/science/intakes/'+self.request_id
        state=post(base+'/adaptive-analysis',self.body())
        self.assertNotIn('owner',state['cursor'].get('pending') or {})
        approval={'proposalSha256':state['proposalSha256'],'adaptationScope':'NEXT_STEP_PARAMETERS_ONLY',
                  'nativeExecutionConfirmed':True}
        with self.assertRaises(urllib.error.HTTPError) as denied:post(base+'/adaptive-approve',approval)
        self.assertEqual(denied.exception.code,404)
        with self.assertRaises(urllib.error.HTTPError) as denied:
            post('/v1/science/intakes/'+self.request_id+'/adaptive-approve',approval)
        self.assertEqual(denied.exception.code,403)
        approved=post('/v1/science/intakes/'+self.request_id+'/adaptive-approve',approval,'owner-test',origin)
        self.assertEqual(approved['executionPolicy']['adaptationScope'],'NEXT_STEP_PARAMETERS_ONLY')

    def test_cancellation_blocks_new_paid_send_and_plan_approval(self):
        body=self.body();state=self.portal.generate_adaptive(self.request_id,body)
        self.broker.cancel(state['job']['jobId'])
        with self.assertRaisesRegex(ProtocolError,'INACTIVE'):
            self.portal.generate_adaptive(self.request_id,body)
        with self.assertRaisesRegex(ProtocolError,'INACTIVE'):
            self.portal.approve_adaptive(self.request_id,{'proposalSha256':state['proposalSha256'],
                'adaptationScope':'NEXT_STEP_PARAMETERS_ONLY','nativeExecutionConfirmed':True})
        self.assertEqual(len(self.calls),1)

if __name__=='__main__':unittest.main()
