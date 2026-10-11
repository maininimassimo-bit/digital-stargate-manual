"""HTTP worker reports bind exact native attempts; fixtures are not native OAT."""
import base64
import copy
import json
import unittest
from unittest.mock import patch

from . import test_adaptive_flow as fixture
from .adaptive_execution import VERIFICATION_VERSION
from .broker import ProtocolError
from .intake import sha
from .checkpoint_provider import CheckpointProvider
from .test_native_measurements import fixture as measurement
from .image_previews import render, curve


class ExecutionTests(unittest.TestCase):
    def test_worker_context_retains_the_exact_initial_scientific_pack_for_archive(self):
        context = self.portal.adaptive_context(self.request_id)
        self.assertEqual(sha(context['scientificKnowledge']), context['plan']['provider']['scientificKnowledgeSha256'])
        self.assertEqual(context['scientificKnowledge']['authority'],
                         'GUIDANCE_ONLY_NEVER_CAPABILITIES_FACTS_OR_ACCEPTANCE')

    def setUp(self):
        fixture.AdaptiveFlowTests.setUp(self)
        self.body=lambda:fixture.AdaptiveFlowTests.body(self)
        result=self.portal.generate_adaptive(self.request_id,self.body())
        self.portal.approve_adaptive(self.request_id,{'proposalSha256':result['proposalSha256'],
            'adaptationScope':'NEXT_STEP_PARAMETERS_ONLY','nativeExecutionConfirmed':True})
        self.calls=[]
        self.portal.adaptive_provider=CheckpointProvider('mock','gpt-6-luna',send=self.send)

    def send(self,payload):
        if payload['text']['format']['name'] != 'DSG_PIAI_CHECKPOINT_PROVIDER_V2':
            return fixture.AdaptiveFlowTests.send(self,payload)
        self.calls.append(payload)
        context=json.loads(payload['input'][0]['content'][0]['text'])
        graph=context['approvedGraph'];completed=context['completedSteps']
        binding=payload['text']['format']['schema']['properties']['bindingSha256']['enum'][0]
        decision={'action':'CONTINUE' if completed<len(graph['steps']) else 'COMPLETE_FOR_REVIEW',
                  'bindingSha256':binding,'nextStep':graph['steps'][completed] if completed<len(graph['steps']) else None,
                  'rationale':'Confronto simulato','limitations':'Fixture, nessuna esecuzione fisica'}
        return {'status':'completed','id':'resp_checkpoint_mock','model':'gpt-6-luna',
                'output':[{'type':'message','role':'assistant','status':'completed',
                           'content':[{'type':'output_text','text':json.dumps(decision)}]}],
                'usage':{'input_tokens':100,'output_tokens':20,'total_tokens':120}}

    def reserve(self):
        state=self.portal.adaptive_state(self.request_id)
        return self.portal.adaptive_reserve(self.request_id,{'workerId':self.broker.worker_id,'rootId':'2'*32,
            'approvalSha256':sha(state['executionPolicy']),'decisionResultSha256':state['cursor']['resultSha256']})['permit']

    def checkpoint(self,permit):
        analysis=self.portal._adaptive_analysis(self.request_id)
        ordinal=permit['ordinal']
        facts=copy.deepcopy(analysis['evidence']['provenance'])
        parent=[{'role':r,'sha256':c*64,'width':64,'height':64,'channels':3 if r=='RGB' else 1,
                 'historySha256':'b'*64} for r,c in (('RGB','a'),('L','b'))]
        if ordinal:
            previous=json.loads(self.portal.store.get('science/adaptive-checkpoints/PIAI_'+self.request_id+'/'+str(ordinal-1))[0])
            facts=copy.deepcopy(previous['currentProvenance']);parent=previous['outputs']
        current=copy.deepcopy(facts)
        if permit['step']['process']=='STRETCH':current['domain']='NONLINEAR_ATTESTED'
        outputs=[{**o,'sha256':str(ordinal+1)*64} for o in parent]
        return {'workerId':self.broker.worker_id,'permit':permit,'verification':{
            'version':VERIFICATION_VERSION,'jobId':permit['jobId'],'ordinal':ordinal,'permitSha256':sha(permit),
            'approvalSha256':permit['approvalSha256'],'runtimeSha256':permit['runtimeSha256'],
            'nativeManifestSha256':'c'*64,'outputs':outputs,'parentOutputs':parent,
            'historySha256':'d'*64,'parentProvenance':facts,'currentProvenance':current,
            'sourceGuard':[{'role':i['role'],'sha256':i['sha256'],'imageIndex':i['imageIndex'],'unchanged':True}
                           for i in analysis['inputs']], 'executedStep':permit['step'],'status':'PHYSICALLY_VERIFIED'}}

    def decision_body(self,checkpoint):
        import numpy as np
        v=checkpoint['verification'];analysis=self.portal._adaptive_analysis(self.request_id)
        graph=self.portal.adaptive_state(self.request_id)['plan']['decision']['graph']
        bindings={'PARENT':{},'CURRENT':{}};rows={'PARENT':[],'CURRENT':[]};previews=[];assets=[]
        display=curve(.05)
        for phase,key in (('PARENT','parentOutputs'),('CURRENT','outputs')):
            for o in v[key]:
                report,binding=measurement()
                report['channels']=o['channels'];binding['channels']=o['channels']
                if o['channels']==3:
                    report['noise']=[{**copy.deepcopy(report['noise'][0]),'channel':i} for i in range(3)]
                    report['fits']=[{**copy.deepcopy(report['fits'][0]),'channel':i} for i in range(3)]
                report['sourceSha256']=o['sha256'];binding['sourceSha256']=o['sha256']
                bindings[phase][o['role']]=binding;rows[phase].append({'role':o['role'],'report':report})
                raw,png=render(np.full((64,64,o['channels']),.05,dtype=np.float32),display)
                previews.append({'role':o['role'],'phase':phase,'sha256':png['sha256'],'displayCurve':display,'region':None})
                assets.append(base64.b64encode(raw).decode())
        evidence={'mode':'LRGB','intent':analysis['evidence']['intent'],'graph':graph,
            'initialProvenance':analysis['evidence']['provenance'],'parentProvenance':v['parentProvenance'],
            'currentProvenance':v['currentProvenance'],'completedSteps':v['ordinal']+1,
            'bindingSha256':sha({'checkpointSha256':sha(v),'graphSha256':sha(graph),
                 'ordinal':v['ordinal']+1,'runtimeSha256':sha(analysis['runtime'])}),
            'parentMeasurements':rows['PARENT'],'currentMeasurements':rows['CURRENT'],'previews':previews}
        return {'workerId':self.broker.worker_id,'evidence':evidence,'bindings':bindings,'assetsBase64':assets}

    def test_native_receipt_advances_once_and_checkpoint_decision_is_not_repeated(self):
        permit=self.reserve()
        self.portal.adaptive_start(self.request_id,{'workerId':self.broker.worker_id,'permit':permit})
        body=self.checkpoint(permit)
        state=self.portal.adaptive_checkpoint(self.request_id,body)
        self.assertEqual(state['cursor']['ordinal'],1)
        self.assertEqual(self.portal.adaptive_checkpoint(self.request_id,body),state)
        decision=self.decision_body(body)
        result=self.portal.adaptive_decision(self.request_id,decision)
        self.assertEqual(result['cursor']['state'],'AWAITING_EXECUTION')
        self.assertEqual(self.portal.adaptive_decision(self.request_id,decision),result)
        self.assertEqual(len(self.calls),1)
        self.assertEqual(self.reserve()['step']['process'],'STRETCH')

    def test_forged_source_guard_geometry_or_nonce_cannot_advance(self):
        permit=self.reserve()
        self.portal.adaptive_start(self.request_id,{'workerId':self.broker.worker_id,'permit':permit})
        for kind in ('source','geometry','nonce','domain'):
            body=self.checkpoint(permit)
            if kind=='source':body['verification']['sourceGuard'][0]['unchanged']=False
            elif kind=='geometry':body['verification']['outputs'][0]['width']=32
            elif kind=='nonce':body['permit']['owner']='f'*64
            else:body['verification']['currentProvenance']['domain']='NONLINEAR_ATTESTED'
            with self.assertRaises(ProtocolError):self.portal.adaptive_checkpoint(self.request_id,body)
        self.assertEqual(self.portal.adaptive_state(self.request_id)['cursor']['ordinal'],0)

    def test_parent_or_adapter_substitution_blocks_paid_call(self):
        permit=self.reserve()
        self.portal.adaptive_start(self.request_id,{'workerId':self.broker.worker_id,'permit':permit})
        body=self.checkpoint(permit);self.portal.adaptive_checkpoint(self.request_id,body)
        for phase in ('PARENT','CURRENT'):
            decision=self.decision_body(body)
            decision['bindings'][phase]['RGB']['sourceSha256']='f'*64
            with self.assertRaises(ProtocolError):self.portal.adaptive_decision(self.request_id,decision)
        self.assertEqual(self.calls,[])

    def test_full_prefix_final_delivery_and_owner_review_are_separate(self):
        import numpy as np
        steps=self.portal.adaptive_state(self.request_id)['plan']['decision']['graph']['steps']
        for _ in steps:
            permit=self.reserve()
            self.portal.adaptive_start(self.request_id,{'workerId':self.broker.worker_id,'permit':permit})
            checkpoint=self.checkpoint(permit)
            self.portal.adaptive_checkpoint(self.request_id,checkpoint)
            self.portal.adaptive_decision(self.request_id,self.decision_body(checkpoint))
        self.assertEqual(self.portal.adaptive_state(self.request_id)['cursor']['state'],'AWAITING_FINAL_VERIFICATION')
        v=checkpoint['verification']
        raw,png=render(np.full((64,64,3),.05,dtype=np.float32),curve(.05))
        body={'workerId':self.broker.worker_id,
              'verification':{'outputs':v['outputs'],'historySha256':v['historySha256'],
                              'sourceGuard':v['sourceGuard'],'status':'FINAL_FILES_REVERIFIED'},
              'delivery':{'version':'DSG_PIAI_ADAPTIVE_PRIVATE_DELIVERY_V2',
                          'artifacts':[{'role':o['role'],'sha256':o['sha256'],'localPath':'F:/private/'+o['role']+'.xisf'}
                                       for o in v['outputs']],
                          'archive':{'localPath':'F:/private/archive.zip','sha256':'e'*64,
                                     'externalDependencies':['LICENSED_PIXINSIGHT_INSTALLATION','LICENSED_RC_ASTRO_MODULES','LOCAL_PATH_RELOCATION_REQUIRED'],
                                     'replayStatus':'EVIDENCE_ARCHIVE_NOT_AUTONOMOUS_REPLAY'},
                          'previewBase64':base64.b64encode(raw).decode(),'previewSha256':png['sha256']}}
        changed=copy.deepcopy(body);changed['verification']['outputs'][0]['sha256']='f'*64
        with self.assertRaises(ProtocolError):self.portal.adaptive_final(self.request_id,changed)
        original_mutate=self.broker._mutate
        def interrupt_completion(fn):
            if fn.__name__=='complete':
                raise RuntimeError('simulated interruption after final journal commit')
            return original_mutate(fn)
        with patch.object(self.broker,'_mutate',side_effect=interrupt_completion):
            with self.assertRaises(RuntimeError):
                self.portal.adaptive_final(self.request_id,body)
        interrupted=self.portal.adaptive_state(self.request_id)
        self.assertEqual(interrupted['cursor']['state'],'READY_FOR_OWNER_REVIEW')
        self.assertNotEqual(interrupted['job']['state'],'COMPLETED')
        paid_calls=len(self.calls)
        self.portal.adaptive_final(self.request_id,body)
        self.assertEqual(len(self.calls),paid_calls)
        result=self.portal.adaptive_result(self.request_id)
        self.assertEqual(result['scientificAcceptance'],'NONE')
        self.assertEqual(result['publication'],'NONE')
        self.assertIsNone(result['ownerReview'])
        review={'deliverySha256':result['deliverySha256'],'decision':'ACCEPTED_PRIVATELY','note':'Fixture privata'}
        changed={**review,'deliverySha256':'f'*64}
        with self.assertRaises(ProtocolError):self.portal.adaptive_review(self.request_id,changed)
        result=self.portal.adaptive_review(self.request_id,review)
        self.assertEqual(result['ownerReview'],review)
        self.assertEqual(result['publication'],'NONE')
