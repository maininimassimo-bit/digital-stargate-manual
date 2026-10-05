"""Synthetic intake/approval and local inspection, never native acceptance evidence."""
import copy
import hashlib
from http.server import HTTPServer
from pathlib import Path
import struct
import tempfile
import threading
import unittest
from unittest.mock import patch
import urllib.request
import urllib.error

from .broker import ProtocolError, encode, decode
from .intake import local_directory, sha
from .intake_assistant import inspect, master_metadata, propose
from . import test_scientific_portal as fixtures
from .transport_http import handler_for, AuthError
from .worker import NONLINEAR_RECIPE, PROCESSING_DEFAULTS, RECIPE_MODES, actions, expected_outputs, input_roles
from tools.scientific_registry.ingestion_storage import Conflict


WORKER, REF, TOKEN = fixtures.WORKER, fixtures.REF, fixtures.TOKEN


class IntakeTests(unittest.TestCase):
    setUp = fixtures.ScientificTests.setUp

    def selection(self):
        return {**{k:v for k,v in self.request.items() if k != 'inputRef'},
                'masterDirectory':r'F:\Astro\M27\Master', 'prompt':'Dettaglio interno e fondo naturale'}

    def plan(self):
        return {'workerId':WORKER,'inputRef':REF,'manifestSha256':'f'*64,'recipe':NONLINEAR_RECIPE,
                'processing':copy.deepcopy(PROCESSING_DEFAULTS),
                'background':{'polyDegree':1,'boxSize':16,'boxSeparation':32},
                'rationale':'Piano M27 con dettaglio mascherato e fondo moderato',
                'limitations':'Ricetta M27 bounded; linearità e idoneità native da verificare',
                'masters':[{'role':role,'width':4634,'height':2808,'imageIndex':0} for role in ('R','G','B','L')]}

    def test_intake_alone_never_creates_or_claims_job(self):
        result=self.portal.create_intake(self.selection())
        self.assertEqual(result['state'],'AWAITING_ASSISTANT_PLAN')
        self.assertEqual(self.portal.jobs(),[])
        self.assertIsNone(self.broker.claim(WORKER,'2'*32))
        with self.assertRaisesRegex(ProtocolError,'PLAN_APPROVAL_REQUIRED'):
            self.portal.create(self.request)
        with self.assertRaisesRegex(ProtocolError,'PLAN_PENDING'):
            self.portal.approve_plan(self.request['requestId'],{'proposalSha256':'0'*64})

    def test_local_path_rejects_unc_relative_urls_commands_and_controls(self):
        for value in [r'\\server\share',r'C:relative','https://host/master','../master',
                      r'C:\Master\..\Other','C:\\Master\nOther',r'C:\Master:stream',r'C:\Master\trailing.']:
            with self.subTest(value=value),self.assertRaises(ProtocolError):local_directory(value)
        self.assertEqual(local_directory(r'F:\Astro\M27\Master'),r'F:\Astro\M27\Master')

    def test_intake_exact_replay_and_prompt_treated_as_data(self):
        selection={**self.selection(),'prompt':'<script>alert(1)</script> do not run this'}
        self.portal.create_intake(selection)
        self.catalog+=b' '
        self.portal.create_intake(selection)
        self.assertEqual(self.portal.intake(selection['requestId'])['selection'],selection)
        with self.assertRaisesRegex(ProtocolError,'IDEMPOTENCY_CONFLICT'):
            self.portal.create_intake({**selection,'prompt':'Changed intent'})

    def test_plan_binding_and_approval_exact_hash_are_immutable(self):
        self.portal.create_intake(self.selection())
        result=self.portal.propose(self.request['requestId'],self.plan())
        self.assertEqual(self.portal.jobs(),[])
        with self.assertRaisesRegex(ProtocolError,'PLAN_CHANGED'):
            self.portal.approve_plan(self.request['requestId'],{'proposalSha256':'0'*64})
        job=self.portal.approve_plan(self.request['requestId'],{'proposalSha256':result['proposalSha256']})
        context=self.portal.context(job['jobId'])
        self.assertEqual(context['intent']['intake']['selection']['prompt'],self.selection()['prompt'])
        self.assertEqual(context['intent']['plan']['background'],self.plan()['background'])
        self.catalog+=b' '
        replay=self.portal.approve_plan(self.request['requestId'],{'proposalSha256':result['proposalSha256']})
        self.assertEqual(job['jobId'],replay['jobId']);self.assertEqual(len(self.portal.jobs()),1)
        with self.assertRaises(Conflict):
            self.portal.propose(self.request['requestId'],{**self.plan(),'rationale':'Changed plan'})

    def test_invalid_plan_registered_hash_or_unbounded_process_rejected(self):
        self.portal.create_intake(self.selection())
        for change in [{'manifestSha256':'0'*64},{'workerId':'9'*32},{'recipe':'ARBITRARY_JS'},
                       {'script':'danger()'},{'processing':{**PROCESSING_DEFAULTS,'sharpenL':1}},
                       {'background':{'polyDegree':20,'boxSize':16,'boxSeparation':32}}]:
            with self.subTest(change=change),self.assertRaises(ProtocolError):
                self.portal.propose(self.request['requestId'],{**self.plan(),**change})
        self.assertEqual(self.portal.jobs(),[])

    def test_catalog_changed_between_plan_and_approval_never_queues(self):
        self.portal.create_intake(self.selection());plan=self.portal.propose(self.request['requestId'],self.plan())
        self.catalog+=b' '
        with self.assertRaisesRegex(ProtocolError,'CATALOG_CHANGED_REFRESH'):
            self.portal.approve_plan(self.request['requestId'],{'proposalSha256':plan['proposalSha256']})
        self.assertEqual(self.portal.jobs(),[])

    def test_other_target_profiles_bind_exact_owner_plan_before_queue(self):
        for ordinal, (recipe, mode) in enumerate(RECIPE_MODES.items(), 3):
            with self.subTest(mode=mode):
                selection = {**self.selection(), 'requestId':str(ordinal)*32,
                    'sessionIds':['SESSION-M42-1'], 'parent':None, 'title':'M42 field',
                    'sourceProfile':{'mode':mode,'layout':'SINGLE','bayerPattern':None,'panels':[]}}
                registered = {**self.input,'inputRef':str(ordinal)*32,'target':'M42','recipe':recipe}
                self.portal.register(registered)
                self.portal.create_intake(selection)
                field = {'target':'M42','backgroundROI':[0.01,0.01,0.10,0.10],
                    'maskLow':0.1,'maskHigh':0.4,'contrastLargeRadius':96,
                    'contrastSmallRadius':48,'starsStretch':100,'saturation':0.1}
                plan = {**self.plan(),'inputRef':registered['inputRef'],'recipe':recipe,'field':field,
                    'masters':[{'role':r,'width':1000,'height':800,'imageIndex':0} for r in input_roles(recipe)]}
                before = len(self.portal.jobs())
                proposed = self.portal.propose(selection['requestId'],plan)
                self.assertEqual(len(self.portal.jobs()),before)
                saved = self.portal.intakes()[-1]['plan']
                self.assertEqual(saved['steps'],[a[1] for a in actions(recipe)])
                self.assertEqual(saved['checkpointCount'],len(expected_outputs(recipe)))
                job = self.portal.approve_plan(selection['requestId'],{'proposalSha256':proposed['proposalSha256']})
                context = self.portal.context(job['jobId'])
                self.assertEqual(context['input']['target'],'M42')
                self.assertEqual(context['intent']['plan']['field'],field)
                self.assertEqual(context['intent']['intake']['selection']['sourceProfile']['mode'],mode)

    def test_mosaic_and_cfa_inventory_never_bypass_execution_validation(self):
        for mode,layout,pattern in [('OSC','PANELS',None),('OSC_CFA','SINGLE','RGGB')]:
            self.setUp()
            selection = {**self.selection(),'sourceProfile':{'mode':mode,'layout':layout,
                'bayerPattern':pattern,'panels':[]}}
            self.portal.create_intake(selection)
            with self.assertRaisesRegex(ProtocolError,'PREPARATION_RESULT_REQUIRED'):
                self.portal.propose(selection['requestId'],self.plan())
            self.assertEqual(self.portal.jobs(),[])

    def test_other_target_rejects_m27_recipe_and_mismatched_scene(self):
        selection = {**self.selection(),'sessionIds':['SESSION-M42-1'],'parent':None}
        self.portal.create_intake(selection)
        with self.assertRaisesRegex(ProtocolError,'M27_RECIPE_TARGET'):
            self.portal.propose(selection['requestId'],self.plan())
        self.assertEqual(self.portal.jobs(),[])

    def source_plan(self):
        return {'panels':[{'panelId':f'P{n}','directory':self.selection()['masterDirectory'],
                'sessionIds':self.selection()['sessionIds'],
                'masters':{'RGB':{'filename':f'Panel{n}.xisf','imageIndex':0}}} for n in (1,2)],
                'rationale':'Due immagini integration selezionate esplicitamente',
                'limitations':'Astrometria e assemblaggio richiedono verifica nativa'}

    def test_mosaic_source_selection_is_immutable_owner_review_and_never_execution_authority(self):
        selection = {**self.selection(),'sourceProfile':{'mode':'OSC','layout':'PANELS','bayerPattern':None,'panels':[]}}
        self.portal.create_intake(selection)
        before=copy.deepcopy(selection)
        proposal=self.portal.propose_sources(selection['requestId'],self.source_plan())
        self.assertFalse(self.portal.intakes()[0]['sourceSelectionApproved'])
        with self.assertRaisesRegex(ProtocolError,'SOURCE_PLAN_CHANGED'):
            self.portal.approve_sources(selection['requestId'],{'sourcePlanSha256':'0'*64})
        result=self.portal.approve_sources(selection['requestId'],{'sourcePlanSha256':proposal['sourcePlanSha256']})
        self.assertFalse(result['nativeStarted']);self.assertEqual(self.portal.jobs(),[])
        self.assertTrue(self.portal.intakes()[0]['sourceSelectionApproved'])
        self.assertEqual(self.portal.intake(selection['requestId'])['selection'],before)
        with self.assertRaises(Conflict):
            self.portal.propose_sources(selection['requestId'],{**self.source_plan(),'rationale':'Changed'})
        with self.assertRaisesRegex(ProtocolError,'PREPARATION_RESULT_REQUIRED'):
            self.portal.propose(selection['requestId'],self.plan())

    def test_mosaic_source_plan_rejects_outside_scope_duplicate_source_and_catalog_change(self):
        selection={**self.selection(),'sourceProfile':{'mode':'OSC','layout':'PANELS','bayerPattern':None,'panels':[]}}
        self.portal.create_intake(selection)
        for mutate in [lambda p:p['panels'][1].update(directory=r'F:\Other'),
                lambda p:p['panels'][1].update(sessionIds=['UNKNOWN']),
                lambda p:p['panels'][1]['masters']['RGB'].update(filename='Panel1.xisf'),
                lambda p:p['panels'][1]['masters']['RGB'].update(filename='../escape.xisf'),
                lambda p:p['panels'][1]['masters']['RGB'].update(imageIndex=True)]:
            plan=self.source_plan();mutate(plan)
            with self.assertRaises(ProtocolError):self.portal.propose_sources(selection['requestId'],plan)
        proposal=self.portal.propose_sources(selection['requestId'],self.source_plan())
        self.catalog+=b' '
        with self.assertRaisesRegex(ProtocolError,'CATALOG_CHANGED_REFRESH'):
            self.portal.approve_sources(selection['requestId'],{'sourcePlanSha256':proposal['sourcePlanSha256']})
        self.assertFalse(self.portal.intakes()[0]['sourceSelectionApproved'])

    def test_private_routes_separate_owner_and_worker_authority(self):
        def owner(token):
            if token!='OWNER':raise AuthError()
        server=HTTPServer(('127.0.0.1',0),handler_for(self.broker,owner,'https://portal.test',hashlib.sha256(TOKEN.encode()).hexdigest(),self.portal))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        origin=f'http://127.0.0.1:{server.server_port}'
        def request(path,body=None,identity='OWNER'):
            headers={'Authorization':'Bearer '+identity,'Content-Type':'application/json'}
            if identity=='OWNER':headers['Origin']='https://portal.test'
            return urllib.request.urlopen(urllib.request.Request(origin+path,None if body is None else encode(body),headers=headers))
        try:
            with request('/v1/science/intakes',self.selection()) as response:self.assertEqual(response.status,200)
            for path in ['/v1/science/intakes','/v1/worker/science/intakes']:
                with self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(origin+path)
                self.assertEqual(error.exception.code,403)
            with self.assertRaises(urllib.error.HTTPError) as error:request('/v1/worker/science/intakes/'+self.request['requestId']+'/plan',self.plan())
            self.assertEqual(error.exception.code,403)
            with request('/v1/worker/science/intakes/'+self.request['requestId']+'/plan',self.plan(),TOKEN) as response:
                plan=decode(response.read())
            with self.assertRaises(urllib.error.HTTPError) as error:request('/v1/science/intakes/'+self.request['requestId']+'/approve',{'proposalSha256':plan['proposalSha256']},TOKEN)
            self.assertEqual(error.exception.code,403)
            with request('/v1/science/intakes/'+self.request['requestId']+'/approve',{'proposalSha256':plan['proposalSha256']}) as response:
                self.assertEqual(decode(response.read())['state'],'QUEUED')
            unicode_selection={**self.selection(),'requestId':'8'*32,'prompt':'🌌'*4000}
            self.assertGreater(len(encode(unicode_selection)),16384)
            with request('/v1/science/intakes',unicode_selection) as response:
                self.assertEqual(response.status,200)
            self.assertEqual(self.portal.intake('8'*32)['selection']['prompt'],unicode_selection['prompt'])
            self.assertEqual(len(self.portal.jobs()),1)
            selection={**self.selection(),'requestId':'7'*32,'sourceProfile':{'mode':'OSC','layout':'PANELS','bayerPattern':None,'panels':[]}}
            with request('/v1/science/intakes',selection) as response:self.assertEqual(response.status,200)
            stem='/science/intakes/'+selection['requestId']
            with self.assertRaises(urllib.error.HTTPError) as error:
                request('/v1/worker'+stem+'/sources',self.source_plan())
            self.assertEqual(error.exception.code,403)
            with request('/v1/worker'+stem+'/sources',self.source_plan(),TOKEN) as response:source_plan=decode(response.read())
            for path in ['/v1'+stem+'/approve-sources','/v1/worker'+stem+'/approve-sources']:
                with self.assertRaises(urllib.error.HTTPError) as error:
                    request(path,{'sourcePlanSha256':source_plan['sourcePlanSha256']},TOKEN)
                self.assertEqual(error.exception.code,403 if path.startswith('/v1/science') else 404)
            with request('/v1'+stem+'/approve-sources',{'sourcePlanSha256':source_plan['sourcePlanSha256']}) as response:
                self.assertFalse(decode(response.read())['nativeStarted'])
            self.assertEqual(len(self.portal.jobs()),1)
        finally:server.shutdown();thread.join();server.server_close()


class LocalInspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name)
        for role in ('Red','Green','Blue','L'):
            self.write(role+'.xisf')
        self.intake={'selection':{'requestId':'1'*32,'masterDirectory':r'F:\Synthetic\M27'}}

    def write(self,name,extra=b''):
        header=b'<xisf><Image geometry="1000:800:1" sampleFormat="Float32" colorSpace="Gray"/>'+extra+b'</xisf>'
        path=self.folder/name;path.write_bytes(b'XISF0100'+struct.pack('<II',len(header),0)+header)
        return path

    def test_exact_roles_headers_hashes_and_ambiguous_role_rejection(self):
        with patch('tools.pixinsight.local_pilot.intake_assistant.local_directory',return_value=str(self.folder)):
            rows=inspect(self.intake)
            self.assertEqual([r['role'] for r in rows],['R','G','B','L'])
            self.write('Red_copy.xisf')
            with self.assertRaisesRegex(ProtocolError,'AMBIGUOUS_ROLES'):inspect(self.intake)

    def test_multi_image_requires_explicit_selection_and_no_escape(self):
        path=self.write('Red.xisf',b'<Image geometry="10:10:1" sampleFormat="Float32" colorSpace="Gray"/>')
        with self.assertRaisesRegex(ProtocolError,'MULTI_IMAGE'):master_metadata(path)
        self.assertEqual(master_metadata(path,0)['width'],1000)
        mapping={role:{'filename':name+'.xisf','imageIndex':0} for role,name in zip(('R','G','B','L'),('Red','Green','Blue','L'))}
        with patch('tools.pixinsight.local_pilot.intake_assistant.local_directory',return_value=str(self.folder)):
            self.assertEqual(len(inspect(self.intake,mapping)),4)
            mapping['R']['filename']='../Red.xisf'
            with self.assertRaisesRegex(ProtocolError,'ROLE_FILENAME'):inspect(self.intake,mapping)

    def test_proposal_atomically_registers_exact_configuration_no_native_or_ai_api(self):
        class FakeTransport:
            def __init__(self):self.posts=[]
            def post(self,path,value):self.posts.append((path,value));return {'state':'PLAN_READY'}
        transport=FakeTransport();config=self.folder/'worker-config.json'
        config.write_bytes(encode({'serviceOrigin':'https://service.run.app','workerId':WORKER,'workerRoot':str(self.folder),'registry':{}}))
        plan={'recipe':NONLINEAR_RECIPE,'background':{'polyDegree':1,'boxSize':16,'boxSeparation':32},'processing':copy.deepcopy(PROCESSING_DEFAULTS),'rationale':'Synthetic proposal','limitations':'Synthetic only'}
        with patch('tools.pixinsight.local_pilot.intake_assistant.local_directory',return_value=str(self.folder)):
            propose(config,self.intake,plan,None,transport)
        self.assertEqual(len(decode(config.read_bytes())['registry']),1)
        self.assertTrue(list(self.folder.glob('*.backup')))
        self.assertEqual([p for p,_ in transport.posts],['/v1/worker/science/register','/v1/worker/science/intakes/'+'1'*32+'/plan'])
        self.assertNotIn('path',transport.posts[1][1]['masters'][0])


if __name__=='__main__':unittest.main()
