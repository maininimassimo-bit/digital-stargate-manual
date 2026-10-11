import json,unittest


import numpy as np
from .image_previews import render,curve
from .adaptive_provider import AdaptiveProvider,catalog,sha,LEDGER_VERSION
from tools.pixinsight.local_pilot.test_native_measurements import fixture

def inputs():
    rows=[];bindings={}
    for role in ('R','G','B','L'):
        value,binding=fixture();rows.append({'role':role,'report':value});bindings[role]=binding
    raw,report=render(np.full((64,64,1),.05,dtype=np.float32),curve(.05))
    facts={'domain':'LINEAR_ATTESTED','sourceSha256':'d'*64,'recordSha256':'e'*64,
        **{k:'VERIFIED' for k in ('registration','backgroundROI','stellarPSF','runtime','mask')}}
    evidence={'mode':'LRGB','provenance':facts,'measurements':rows,'intent':'Preservare le strutture deboli',
        'previews':[{'role':'L','sha256':report['sha256'],'displayCurve':report['displayCurve'],'region':None}]}
    reservation={'sendAllowed':True,'owner':'a'*32,'request':{'ordinal':0,'parentReceiptSha256':None,
        'catalogSha256':catalog.fingerprint(),'evidenceSha256':sha(evidence),'version':LEDGER_VERSION,
        'jobId':'PIAI_'+'1'*32,'policySha256':'2'*64,'runtimeSha256':'3'*64,'inputSetSha256':'4'*64}}
    return reservation,evidence,bindings,[raw]

def response():
    graph={'catalog':catalog.VERSION,'catalogSha256':catalog.fingerprint(),'branch':'DIRECT',
        'steps':[{'process':'DENOISE','parameters':{'denoiseL':.4,'denoiseRGB':.3}}],
        'rationale':'Riduzione moderata da verificare','limitations':'Misure descrittive, nessuna accettazione'}
    return {'status':'completed','id':'resp_mock','model':'gpt-6-luna','output':[{'type':'message','role':'assistant',
        'status':'completed','content':[{'type':'output_text','text':json.dumps({'action':'PROPOSE_GRAPH','graph':graph,
        'rationale':'Proposta conservativa','limitations':'Confrontare i checkpoint'})}]}],
        'usage':{'input_tokens':100,'output_tokens':20,'total_tokens':120}}

CONSENTS={'preview_transfer_confirmed':True,'data_transfer_confirmed':True,'statistics_transfer_confirmed':True}

class ProviderTests(unittest.TestCase):
    def test_projection_omits_private_bindings_and_supports_images(self):
        calls=[];p=AdaptiveProvider('mock','gpt-6-luna',send=lambda payload:calls.append(payload) or response())
        decision,receipt=p.generate_initial(*inputs(),**CONSENTS)
        self.assertEqual(decision['action'],'PROPOSE_GRAPH');self.assertEqual(receipt['usage']['total_tokens'],120)
        payload=json.dumps(calls[0]);self.assertNotIn('sourceSha256',payload);self.assertNotIn('recordSha256',payload)
        self.assertIn('data:image/png;base64,',payload);self.assertFalse(calls[0]['store'])
    def test_missing_consent_or_changed_evidence_prevents_send(self):
        calls=[];p=AdaptiveProvider('mock','gpt-6-luna',send=lambda payload:calls.append(payload))
        with self.assertRaises(ValueError):p.generate_initial(*inputs())
        args=inputs();args[1]['intent']='Intento cambiato'
        with self.assertRaises(ValueError):p.generate_initial(*args,**CONSENTS)
        self.assertEqual(calls,[])
    def test_no_ambiguous_retry_after_response_lost(self):
        calls=[]
        def send(payload):calls.append(payload);raise TimeoutError()
        p=AdaptiveProvider('mock','gpt-6-luna',send=send);args=inputs()
        with self.assertRaisesRegex(ValueError,'NO_RETRY'):p.generate_initial(*args,**CONSENTS)
        with self.assertRaisesRegex(ValueError,'ALREADY_ATTEMPTED'):p.generate_initial(*args,**CONSENTS)
        self.assertEqual(len(calls),1)
    def test_code_unknown_step_refusal_and_bad_usage_fail(self):
        variants=[]
        r=response();r['usage']['total_tokens']=121;variants.append(r)
        r=response();r['output'][0]['content'][0]={'type':'refusal','refusal':'No'};variants.append(r)
        r=response();d=json.loads(r['output'][0]['content'][0]['text']);d['graph']['steps'][0]['process']='PixelMath';r['output'][0]['content'][0]['text']=json.dumps(d);variants.append(r)
        for r in variants:
            p=AdaptiveProvider('mock','gpt-6-luna',send=lambda payload:r)
            with self.assertRaisesRegex(ValueError,'NO_RETRY'):p.generate_initial(*inputs(),**CONSENTS)

if __name__=='__main__':unittest.main()
