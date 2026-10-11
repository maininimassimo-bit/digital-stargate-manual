import copy
import json
import unittest
import numpy as np
from .checkpoint_provider import CheckpointProvider
from .adaptive_provider import LEDGER_VERSION,sha
from .image_previews import render,curve
from .test_native_measurements import fixture
from .test_checkpoint_control import facts,graph,decision
from .test_adaptive_provider import CONSENTS

def measurements():
    rows=[];bindings={}
    for role,channels in (('RGB',3),('L',1)):
        value,binding=fixture();value['channels']=channels;binding['channels']=channels
        value['noise']=[{**copy.deepcopy(value['noise'][0]),'channel':c} for c in range(channels)]
        rows.append({'role':role,'report':value});bindings[role]=binding
    return rows,bindings

def inputs():
    parent,pb=measurements();current,cb=measurements();previews=[];assets=[]
    for phase,value in (('PARENT',.05),('CURRENT',.08)):
        raw,record=render(np.full((64,64,1),value,dtype=np.float32),curve(.05))
        assets.append(raw);previews.append({'role':'L','phase':phase,'sha256':record['sha256'],
            'displayCurve':record['displayCurve'],'region':None})
    evidence={'mode':'LRGB','intent':'Conservare le strutture deboli','graph':graph(),
        'initialProvenance':facts(),'parentProvenance':facts(),
        'currentProvenance':{**facts(),'domain':'NONLINEAR_ATTESTED'},'completedSteps':1,
        'bindingSha256':'c'*64,'parentMeasurements':parent,'currentMeasurements':current,'previews':previews}
    reservation={'sendAllowed':True,'owner':'a'*32,'request':{'version':LEDGER_VERSION,'jobId':'PIAI_'+'1'*32,
        'ordinal':1,'parentReceiptSha256':'d'*64,'policySha256':'e'*64,'catalogSha256':graph()['catalogSha256'],
        'runtimeSha256':'f'*64,'inputSetSha256':'b'*64,'evidenceSha256':sha(evidence)}}
    return reservation,evidence,{'PARENT':pb,'CURRENT':cb},assets

def response(value=None):
    return {'status':'completed','id':'resp_checkpoint_mock','model':'gpt-6-luna',
        'output':[{'type':'message','role':'assistant','status':'completed',
                   'content':[{'type':'output_text','text':json.dumps(value or decision(step=graph()['steps'][1]))}]}],
        'usage':{'input_tokens':100,'output_tokens':50,'total_tokens':150}}

class CheckpointProviderTests(unittest.TestCase):
    def test_projects_paired_data_without_private_bindings(self):
        calls=[];provider=CheckpointProvider('mock','gpt-6-luna',send=lambda payload:calls.append(payload) or response())
        value,receipt=provider.generate_checkpoint(*inputs(),**CONSENTS)
        self.assertEqual(value['nextStep']['process'],'MASK_BUILD');self.assertEqual(receipt['usage']['total_tokens'],150)
        raw=json.dumps(calls[0]);self.assertNotIn('sourceSha256',raw);self.assertNotIn('recordSha256',raw)
        self.assertIn('NOT_ESTABLISHED_NEW_DETECTION_PER_CHECKPOINT',raw)
        projected=json.loads(calls[0]['input'][0]['content'][0]['text'])
        self.assertFalse(projected['comparisonLimitations']['sameRecordedDomain'])
        self.assertTrue(projected['comparisonLimitations']['sameMeasurementRuntime'])
    def test_different_measurement_runtime_is_reported_as_comparison_limit(self):
        args=inputs();args[2]['CURRENT']['L']['adapterSha256']='9'*64
        args[1]['currentMeasurements'][1]['report']['adapterSha256']='9'*64
        args[0]['request']['evidenceSha256']=sha(args[1]);calls=[]
        provider=CheckpointProvider('mock','gpt-6-luna',send=lambda payload:calls.append(payload) or response())
        provider.generate_checkpoint(*args,**CONSENTS)
        projected=json.loads(calls[0]['input'][0]['content'][0]['text'])
        self.assertFalse(projected['comparisonLimitations']['sameMeasurementRuntime'])
    def test_unpaired_or_independently_stretched_previews_prevent_send(self):
        for mutation in (lambda e:e['previews'][1].update(phase='PARENT'),
                         lambda e:e['previews'][1].update(displayCurve=curve(.08)),
                         lambda e:e['previews'][1].update(region=[0,0,32,32])):
            args=inputs();mutation(args[1]);args[0]['request']['evidenceSha256']=sha(args[1]);calls=[]
            provider=CheckpointProvider('mock','gpt-6-luna',send=lambda payload:calls.append(payload))
            with self.assertRaises(ValueError):provider.generate_checkpoint(*args,**CONSENTS)
            self.assertEqual(calls,[])
    def test_changed_native_binding_or_skipped_prefix_prevents_send(self):
        for changed in ('hash','prefix'):
            args=inputs();calls=[]
            if changed=='hash':args[2]['CURRENT']['L']['sourceSha256']='d'*64
            else:args[1]['completedSteps']=3;args[0]['request']['evidenceSha256']=sha(args[1])
            provider=CheckpointProvider('mock','gpt-6-luna',send=lambda payload:calls.append(payload))
            with self.assertRaises(ValueError):provider.generate_checkpoint(*args,**CONSENTS)
            self.assertEqual(calls,[])
    def test_parameter_adjustment_accepted_but_changed_process_rejected(self):
        step=copy.deepcopy(graph()['steps'][1]);step['parameters']['maskLow']=.08
        provider=CheckpointProvider('mock','gpt-6-luna',send=lambda payload:response(decision(step=step)))
        result,_=provider.generate_checkpoint(*inputs(),**CONSENTS)
        self.assertEqual(result['nextStep']['parameters']['maskLow'],.08)
        provider=CheckpointProvider('mock','gpt-6-luna',send=lambda payload:response(decision(step=graph()['steps'][0])))
        with self.assertRaisesRegex(ValueError,'NO_RETRY'):provider.generate_checkpoint(*inputs(),**CONSENTS)
    def test_lost_response_is_not_retried(self):
        calls=[]
        def send(payload):calls.append(payload);raise TimeoutError()
        provider=CheckpointProvider('mock','gpt-6-luna',send=send);args=inputs()
        with self.assertRaisesRegex(ValueError,'NO_RETRY'):provider.generate_checkpoint(*args,**CONSENTS)
        with self.assertRaisesRegex(ValueError,'ALREADY_ATTEMPTED'):provider.generate_checkpoint(*args,**CONSENTS)
        self.assertEqual(len(calls),1)
    def test_completion_is_owner_review_and_not_scientific_acceptance(self):
        args=inputs();args[1]['completedSteps']=4;args[1]['currentProvenance']['mask']='VERIFIED'
        args[0]['request']['ordinal']=4;args[0]['request']['evidenceSha256']=sha(args[1])
        provider=CheckpointProvider('mock','gpt-6-luna',send=lambda payload:response(decision('COMPLETE_FOR_REVIEW')))
        value,_=provider.generate_checkpoint(*args,**CONSENTS)
        self.assertEqual(value['action'],'COMPLETE_FOR_REVIEW');self.assertIsNone(value['nextStep'])

if __name__=='__main__':unittest.main()
