"""Historical provenance and withdrawal tests; synthetic, no scientific acceptance."""
import base64
import copy
import unittest
from unittest.mock import patch
import hashlib
from http.server import HTTPServer
import threading
import urllib.request
import urllib.error

from . import test_scientific_portal as fixtures
from .broker import ProtocolError, encode
from .historical_source import validate_historical
from .intake import sha
from .source_profile import selected_panels
from .worker import OSC_RECIPE, PROCESSING_DEFAULTS, actions
from .transport_http import handler_for, AuthError


class HistoricalTests(unittest.TestCase):
    setUp = fixtures.ScientificTests.setUp

    def selection(self):
        return {'requestId':'4'*32, 'masterDirectory':r'D:\M31_F4\12_Processing_All\master',
                'prompt':'Mosaico M31 su copie, risultato privato', 'catalogSha256':None, 'sessionIds':[],
                'parent':None, 'title':'M31 storico', 'processingDate':'2026-10-06', 'associationConfirmed':False,
                'historicalSource':{'target':'M31','provenance':'Riprese anteriori al portale; sessioni non importate','attested':True},
                'sourceProfile':{'mode':'OSC','layout':'SINGLE','bayerPattern':None,'panels':[]}}

    def propose(self):
        selection=self.selection()
        self.portal.create_intake(selection)
        registered={'inputRef':'5'*32,'target':'M31','recipe':OSC_RECIPE,'manifestSha256':'6'*64,
                    'historicalRequestId':selection['requestId']}
        self.portal.register(registered)
        plan={**registered,'workerId':fixtures.WORKER,'background':{'polyDegree':1,'boxSize':16,'boxSeparation':32},
              'processing':copy.deepcopy(PROCESSING_DEFAULTS),'rationale':'Piano del campo M31','limitations':'Synthetic only',
              'field':{'target':'M31','backgroundROI':[0.01,0.01,0.1,0.1],'maskLow':0.08,'maskHigh':0.7,
                       'contrastLargeRadius':128,'contrastSmallRadius':64,'starsStretch':100,'saturation':0.15},
              'masters':[{'role':'RGB','width':1000,'height':800,'imageIndex':0}]}
        del plan['target'];del plan['historicalRequestId']
        proposal=self.portal.propose(selection['requestId'],plan)
        return selection,proposal

    def test_historical_intake_never_loads_catalog_or_invents_sessions(self):
        with patch.object(self.portal,'catalog_loader',side_effect=AssertionError('catalog access')):
            selection,proposal=self.propose()
            job=self.portal.approve_plan(selection['requestId'],{'proposalSha256':proposal['proposalSha256']})
        context=self.portal.context(job['jobId'])
        self.assertEqual(context['sessionContext']['sessions'],[])
        self.assertIsNone(context['sessionContext']['catalogSha256'])
        self.assertEqual(context['associationEvidence'],'NOT_ESTABLISHED')
        self.assertEqual(context['sessionContext']['source'],'HISTORICAL_OWNER_DECLARATION')
        self.assertFalse(any(key.startswith('science/catalogs/') for key in self.store.items))

    def test_historical_rejects_catalog_parent_sessions_and_unattested_provenance(self):
        for change in [{'sessionIds':['SESSION-M27-1']},{'catalogSha256':'a'*64},
                       {'associationConfirmed':True},{'parent':self.request['parent']},
                       {'historicalSource':{'target':'M31','provenance':'Historical','attested':False}},
                       {'historicalSource':{'target':'UNKNOWN','provenance':'Historical','attested':True}}]:
            with self.subTest(change=change), self.assertRaises(ProtocolError):
                self.portal.create_intake({**self.selection(),**change})

    def test_historical_declaration_is_immutable_and_date_is_not_observation_date(self):
        selection=self.selection();self.portal.create_intake(selection)
        self.portal.create_intake(selection)
        with self.assertRaisesRegex(ProtocolError,'IDEMPOTENCY_CONFLICT'):
            self.portal.create_intake({**selection,'historicalSource':{**selection['historicalSource'],'provenance':'Changed'}})
        self.assertNotIn('observationDate',self.portal.intake(selection['requestId'])['selection'])
        with self.assertRaises(ProtocolError):validate_historical({**selection,'processingDate':'2026-02-30'})

    def test_suspension_blocks_new_historical_intakes_but_retains_existing_receipts_and_withdrawal(self):
        selection,proposal=self.propose()
        with patch.dict('os.environ',{'DSG_PIAI_HISTORICAL_INTAKE':'0'}):
            self.assertFalse(self.portal.options()['historicalIntakeEnabled'])
            self.portal.create_intake(selection)
            with self.assertRaisesRegex(ProtocolError,'HISTORICAL_INTAKE_SUSPENDED'):
                self.portal.create_intake({**selection,'requestId':'7'*32})
            self.portal.withdraw_intake(selection['requestId'],{})
            self.assertEqual(self.portal.intakes()[0]['state'],'WITHDRAWN')
            self.assertTrue(self.store.exists('science/plans/'+selection['requestId']))

    def test_registration_requires_matching_historical_intake_and_no_direct_bypass(self):
        value={'inputRef':'5'*32,'target':'M31','recipe':OSC_RECIPE,'manifestSha256':'6'*64}
        with self.assertRaisesRegex(ProtocolError,'TARGET_NOT_IMPORTED'):self.portal.register(value)
        self.portal.create_intake(self.selection())
        with self.assertRaisesRegex(ProtocolError,'HISTORICAL_INPUT_BINDING'):
            self.portal.register({**value,'target':'M42','historicalRequestId':'4'*32})
        self.portal.register({**value,'historicalRequestId':'4'*32})
        request={k:v for k,v in self.selection().items() if k not in {'masterDirectory','prompt','sourceProfile'}}
        with self.assertRaisesRegex(ProtocolError,'HISTORICAL_INTAKE_REQUIRED'):
            self.portal.create({**request,'inputRef':'5'*32})

    def test_historical_panels_have_no_catalog_associations(self):
        selection=self.selection();selection['sourceProfile']['layout']='PANELS'
        panels=[{'panelId':f'p{i}','directory':selection['masterDirectory'],'sessionIds':[],
                 'masters':{'RGB':{'filename':f'panel{i}.xisf','imageIndex':0}}} for i in range(2)]
        derived,_=selected_panels(selection,{'panels':panels,'rationale':'Four historical panels','limitations':'No imported sessions'})
        self.assertEqual([p['sessionIds'] for p in derived['sourceProfile']['panels']],[[],[]])
        panels[0]['sessionIds']=['SESSION-M27-1']
        with self.assertRaisesRegex(ProtocolError,'MOSAIC_PANEL_SESSIONS'):
            selected_panels(selection,{'panels':panels,'rationale':'Historical','limitations':'No sessions'})

    def test_withdrawal_retains_plan_and_blocks_approval_replay_and_broker_queue(self):
        selection,proposal=self.propose();rid=selection['requestId']
        self.portal.withdraw_intake(rid,{})
        self.portal.withdraw_intake(rid,{})
        self.assertEqual(self.portal.intakes()[0]['state'],'WITHDRAWN')
        self.assertTrue(self.store.exists('science/plans/'+rid))
        with self.assertRaisesRegex(ProtocolError,'INTAKE_WITHDRAWN'):self.portal.approve_plan(rid,{'proposalSha256':proposal['proposalSha256']})
        with self.assertRaisesRegex(ProtocolError,'INTAKE_WITHDRAWN'):self.portal.create_intake(selection)
        with self.assertRaisesRegex(ProtocolError,'INTAKE_WITHDRAWN'):
            self.broker.create({'schemaVersion':'1.0','requestId':rid,'inputRef':'5'*32,'recipe':OSC_RECIPE,'aiMode':'SESSION_ASSISTED'},'a'*64)
        self.assertEqual(self.portal.jobs(),[])

    def test_withdrawal_cannot_replace_job_cancel_or_revoke_native_preparation(self):
        selection,proposal=self.propose();rid=selection['requestId']
        self.portal.approve_plan(rid,{'proposalSha256':proposal['proposalSha256']})
        with self.assertRaisesRegex(ProtocolError,'JOB_ALREADY_CREATED'):self.portal.withdraw_intake(rid,{})
        other={**self.selection(),'requestId':'7'*32};self.portal.create_intake(other)
        self.broker._mutate(lambda state,now:state.setdefault('preparationAuthorizedIntakes',[]).append(other['requestId']))
        with self.assertRaisesRegex(ProtocolError,'PREPARATION_ALREADY_APPROVED'):self.portal.withdraw_intake(other['requestId'],{})

    def test_withdrawal_winning_between_context_write_and_queue_commit_blocks_native_authority(self):
        selection,proposal=self.propose();rid=selection['requestId'];create=self.broker.create
        def interrupted_create(envelope,context_sha):
            self.portal.withdraw_intake(rid,{})
            return create(envelope,context_sha)
        with patch.object(self.broker,'create',side_effect=interrupted_create):
            with self.assertRaisesRegex(ProtocolError,'INTAKE_WITHDRAWN'):
                self.portal.approve_plan(rid,{'proposalSha256':proposal['proposalSha256']})
        self.assertTrue(self.store.exists('science/contexts/PIAI_'+rid))
        self.assertEqual(self.portal.jobs(),[])
        self.assertIsNone(self.broker.claim(fixtures.WORKER,'8'*32))

    def test_private_delivery_retains_provenance_and_runtime_workflow_without_fake_catalog(self):
        selection,proposal=self.propose();rid=selection['requestId']
        job=self.portal.approve_plan(rid,{'proposalSha256':proposal['proposalSha256']})['jobId']
        claim=self.broker.claim(fixtures.WORKER,'8'*32)
        self.broker.report(job,fixtures.WORKER,{'leaseToken':claim['leaseToken'],'sequence':1,'stage':'COMPLETED',
                           'processCount':26,'outputCount':12,'verified':True})
        payload=fixtures.ScientificTests.payload(self,claim['leaseToken'])
        lines=['var Root = new ProcessContainer;']
        for i,action in enumerate(actions(OSC_RECIPE)):
            lines.extend([f'var P{i} = new {action[1]};',f'Root.add( P{i} );'])
        payload['workflowBase64']=base64.b64encode('\n'.join(lines).encode()).decode()
        payload['correlationsBase64']=base64.b64encode(encode({'jobId':job,'recipe':OSC_RECIPE,
            'upstreamHistoryCompleteness':'NOT_ESTABLISHED','instances':[{'ordinal':i+1,'variable':f'P{i}'} for i in range(26)]})).decode()
        result=self.portal.deliver(job,payload)
        self.assertEqual(result['context']['selection']['historicalSource'],selection['historicalSource'])
        self.assertEqual(result['context']['sessionContext']['sessions'],[])
        self.assertEqual(result['publication'],'NONE')
        self.assertEqual(result['scientificAcceptance'],'OWNER_REVIEW_REQUIRED')
        self.assertEqual(len(result['steps']),26)

    def test_http_worker_cannot_withdraw_and_owner_withdrawal_is_retained(self):
        selection,proposal=self.propose();rid=selection['requestId']
        def owner(token):
            if token!='OWNER':raise AuthError()
        server=HTTPServer(('127.0.0.1',0),handler_for(self.broker,owner,'https://portal.test',
                          hashlib.sha256(fixtures.TOKEN.encode()).hexdigest(),self.portal))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            for prefix,token,expected in [('worker/','Bearer '+fixtures.TOKEN,404),('','Bearer invalid',403),('','Bearer OWNER',200)]:
                headers={'Authorization':token,'Content-Type':'application/json'}
                if not prefix:headers['Origin']='https://portal.test'
                request=urllib.request.Request(f'http://127.0.0.1:{server.server_port}/v1/{prefix}science/intakes/{rid}/withdraw',
                                              data=encode({}),headers=headers)
                if expected==200:
                    with urllib.request.urlopen(request) as response:self.assertEqual(response.status,200)
                else:
                    with self.assertRaises(urllib.error.HTTPError) as caught:urllib.request.urlopen(request)
                    self.assertEqual(caught.exception.code,expected)
                    self.assertEqual(self.portal.intakes()[0]['state'],'PLAN_READY')
            self.assertEqual(self.portal.intakes()[0]['state'],'WITHDRAWN')
            self.assertEqual(self.portal.jobs(),[])
        finally:
            server.shutdown();server.server_close();thread.join()


if __name__=='__main__':unittest.main()
