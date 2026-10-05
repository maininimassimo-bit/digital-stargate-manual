"""Synthetic phase/bridge rejection tests, never native or cloud acceptance."""
import base64
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from . import worker
from .broker import ProtocolError, encode, decode
from . import test_scientific_portal as scientific_fixtures
from . import test_intake as intake_fixtures
from . import test_preparation as preparation_fixtures
from .preparation import collect
from .preparation_flow import sha, source_digest
from .preparation_bridge import prepared_inputs, verify_trace, runtime_graph
from tools.scientific_registry.ingestion_storage import Conflict

WORKER=scientific_fixtures.WORKER


class PreparationFlowTests(unittest.TestCase):
    setUp=scientific_fixtures.ScientificTests.setUp
    selection=intake_fixtures.IntakeTests.selection

    def proposal(self, mode='OSC_CFA', layout='SINGLE'):
        return {'workerId':WORKER,'sourceManifestSha256':'4'*64,'sourcePlanSha256':None,
                'mode':mode,'layout':layout,'bayerPattern':'RGGB' if mode=='OSC_CFA' else None,
                'canvas':None,'shrink':0,'feather':0,
                'masters':[{'panelId':'P1','role':'CFA','width':1000,'height':800,'imageIndex':0,'filename':'CFA.xisf'}],
                'rationale':'Pattern dichiarato, preparazione RGB su copie','limitations':'Risultato lineare, piano finale separato'}

    def begin(self):
        selection={**self.selection(),'sourceProfile':{'mode':'OSC_CFA','layout':'SINGLE','bayerPattern':'RGGB','panels':[]}}
        self.portal.create_intake(selection)
        rid=selection['requestId'];proposal=self.portal.propose_preparation(rid,self.proposal())
        return rid,proposal

    def packet(self, rid):
        state=self.portal.preparation_state(rid)
        return {'workerId':WORKER,'preparationPlanSha256':state['preparationPlanSha256'],'sourceManifestSha256':'4'*64,
                'outputManifestSha256':'5'*64,'verificationSha256':'6'*64,'nativeInstancesSha256':'7'*64,
                'masters':[{'role':'RGB','width':1000,'height':800,'imageIndex':0}],
                'nativeProcessCount':1,'checkpointCount':2}

    def field(self):
        return {'target':'M27','backgroundROI':[.01,.01,.1,.1],'maskLow':.1,'maskHigh':.6,
                'contrastLargeRadius':64,'contrastSmallRadius':32,'starsStretch':100,'saturation':.15}

    def test_preparation_requires_exact_owner_approval_then_separate_final_queue_approval(self):
        rid,proposal=self.begin()
        self.assertEqual(self.portal.jobs(),[])
        with self.assertRaisesRegex(ProtocolError,'RESULT_APPROVAL'):self.portal.record_preparation(rid,self.packet(rid))
        with self.assertRaisesRegex(ProtocolError,'PLAN_CHANGED'):self.portal.approve_preparation(rid,{'preparationPlanSha256':'0'*64})
        self.portal.approve_preparation(rid,{'preparationPlanSha256':proposal['preparationPlanSha256']})
        result=self.portal.record_preparation(rid,self.packet(rid));self.assertEqual(self.portal.jobs(),[])
        registration={'inputRef':'8'*32,'target':'M27','recipe':worker.OSC_RECIPE,'manifestSha256':'9'*64,
                      'preparation':{'requestId':rid,'resultSha256':result['preparationResultSha256']}}
        self.portal.register(registration)
        plan={'workerId':WORKER,'inputRef':'8'*32,'manifestSha256':'9'*64,'recipe':worker.OSC_RECIPE,
              'background':{'polyDegree':1,'boxSize':16,'boxSeparation':32},'processing':copy.deepcopy(worker.PROCESSING_DEFAULTS),
              'field':self.field(),'masters':self.packet(rid)['masters'],'rationale':'Piano RGB sul master preparato',
              'limitations':'Colori non certificati fotometricamente','preparationResultSha256':result['preparationResultSha256']}
        proposed=self.portal.propose(rid,plan);self.assertEqual(self.portal.jobs(),[])
        with self.assertRaisesRegex(ProtocolError,'PLAN_CHANGED'):self.portal.approve_plan(rid,{'proposalSha256':'0'*64})
        job=self.portal.approve_plan(rid,{'proposalSha256':proposed['proposalSha256']})
        context=self.portal.context(job['jobId'])
        self.assertEqual(context['intent']['plan']['preparation']['resultSha256'],result['preparationResultSha256'])
        self.assertEqual(len(self.portal.jobs()),1)

    def test_wrong_pattern_master_filename_counts_digest_or_geometry_cannot_complete(self):
        selection={**self.selection(),'sourceProfile':{'mode':'OSC_CFA','layout':'SINGLE','bayerPattern':'RGGB','panels':[]}}
        self.portal.create_intake(selection);rid=selection['requestId']
        for mutate in [lambda p:p.update(bayerPattern='BGGR'),lambda p:p['masters'][0].update(filename='../other.xisf'),
                       lambda p:p.update(shrink=1),lambda p:p['masters'][0].update(imageIndex=True)]:
            proposal=self.proposal();mutate(proposal)
            with self.assertRaises(ProtocolError):self.portal.propose_preparation(rid,proposal)
        proposal=self.portal.propose_preparation(rid,self.proposal())
        self.portal.approve_preparation(rid,{'preparationPlanSha256':proposal['preparationPlanSha256']})
        for mutate in [lambda p:p.update(sourceManifestSha256='0'*64),lambda p:p.update(nativeProcessCount=True),
                       lambda p:p.update(checkpointCount=1),lambda p:p['masters'][0].update(width=1200)]:
            packet=self.packet(rid);mutate(packet)
            with self.assertRaises(ProtocolError):self.portal.record_preparation(rid,packet)
        self.assertEqual(self.portal.jobs(),[])

    def test_replay_retains_authorization_and_conflicting_preparation_cannot_replace_it(self):
        rid,proposal=self.begin();approval={'preparationPlanSha256':proposal['preparationPlanSha256']}
        self.portal.approve_preparation(rid,approval);self.catalog+=b' '
        self.portal.approve_preparation(rid,approval)
        with self.assertRaises(Conflict):self.portal.propose_preparation(rid,{**self.proposal(),'rationale':'Changed'})
        result=self.portal.record_preparation(rid,self.packet(rid))
        self.assertEqual(self.portal.record_preparation(rid,self.packet(rid)),result)
        self.assertEqual(self.portal.jobs(),[])

    def test_panels_cannot_prepare_before_source_selection_is_approved(self):
        selection={**self.selection(),'sourceProfile':{'mode':'OSC','layout':'PANELS','bayerPattern':None,'panels':[]}}
        self.portal.create_intake(selection)
        with self.assertRaisesRegex(ProtocolError,'SOURCE_SELECTION_APPROVAL_REQUIRED'):
            self.portal.propose_preparation(selection['requestId'],self.proposal('OSC','PANELS'))

    def test_delivery_requires_preparation_instances_and_matching_runtime_trace(self):
        self.test_preparation_requires_exact_owner_approval_then_separate_final_queue_approval()
        rid=self.request['requestId'];job_id='PIAI_'+rid;claim=self.broker.claim(WORKER,'2'*32)
        self.broker.report(job_id,WORKER,{'leaseToken':claim['leaseToken'],'sequence':1,'stage':'COMPLETED',
            'processCount':len(worker.actions(worker.OSC_RECIPE)),'outputCount':len(worker.expected_outputs(worker.OSC_RECIPE)),'verified':True})
        import io
        from PIL import Image
        preview=io.BytesIO();Image.new('RGB',(4,3),'blue').save(preview,format='JPEG')
        processes=['Debayer']+[p for _,p in worker.actions(worker.OSC_RECIPE)]
        workflow='var Root = new ProcessContainer;\n'+'\n'.join(f'var P{i} = new {p}; Root.add( P{i} );' for i,p in enumerate(processes))
        result=self.portal.preparation_state(rid)['preparationResult']
        trace={k:result[k] for k in ('preparationPlanSha256','sourceManifestSha256','verificationSha256','nativeInstancesSha256','outputManifestSha256')}|{'requestId':rid}
        correlations={'jobId':job_id,'recipe':worker.OSC_RECIPE,'upstreamHistoryCompleteness':'NOT_ESTABLISHED',
            'instances':[{'ordinal':i+1,'variable':f'P{i}','dependencies':[]} for i in range(len(processes))],
            'preparation':{'trace':trace,'nativeInstanceCount':1},'runtimeRelations':[{'target':'PREPARED_RGB','dependencies':['RGB_Debayered']}]}
        payload={'workerId':WORKER,'leaseToken':claim['leaseToken'],'original':{'sha256':'3'*64,'byteSize':100,'width':1000,'height':800,'nonLinear':True},
                 'previewBase64':base64.b64encode(preview.getvalue()).decode(),'workflowBase64':base64.b64encode(workflow.encode()).decode(),
                 'correlationsBase64':base64.b64encode(encode(correlations)).decode()}
        wrong=copy.deepcopy(correlations);wrong['preparation']['trace']['verificationSha256']='0'*64
        with self.assertRaisesRegex(ProtocolError,'PREPARATION_BINDING'):
            self.portal.deliver(job_id,{**payload,'correlationsBase64':base64.b64encode(encode(wrong)).decode()})
        receipt=self.portal.deliver(job_id,payload)
        self.assertEqual(receipt['workflowCompleteness'],'RUNTIME_PREPARATION_AND_RECIPE_ONLY')
        self.assertEqual(len(receipt['steps']),len(processes));self.assertEqual(receipt['publication'],'NONE')

    def test_all_mosaic_modes_bind_selected_files_preparation_counts_and_separate_processing_plan(self):
        from .source_profile import MODES
        for mode in MODES:
            with self.subTest(mode=mode):
                self.setUp();rid=self.request['requestId']
                selection={**self.selection(),'sourceProfile':{'mode':mode,'layout':'PANELS','bayerPattern':'RGGB' if mode=='OSC_CFA' else None,'panels':[]}}
                self.portal.create_intake(selection)
                source_plan={'panels':[{'panelId':p,'directory':selection['masterDirectory'],'sessionIds':selection['sessionIds'],
                    'masters':{r:{'filename':r+'-'+p+'.xisf','imageIndex':0} for r in MODES[mode]}} for p in ('P1','P2')],
                    'rationale':'Selezione esplicita dei pannelli','limitations':'Sorgenti e griglia da verificare sul PC'}
                source=self.portal.propose_sources(rid,source_plan)
                self.portal.approve_sources(rid,{'sourcePlanSha256':source['sourcePlanSha256']})
                preplan={**self.proposal(mode,'PANELS'),'sourcePlanSha256':source['sourcePlanSha256'],
                    'canvas':{'centerRA':10,'centerDec':40,'resolution':.0003,'rotation':0,'width':1000,'height':800},'shrink':1,'feather':10,
                    'masters':[{'panelId':p,'role':r,'filename':r+'-'+p+'.xisf','imageIndex':0,'width':1000,'height':800} for p in ('P1','P2') for r in MODES[mode]]}
                wrong=copy.deepcopy(preplan);wrong['masters'][0]['filename']='Other.xisf'
                with self.assertRaisesRegex(ProtocolError,'SELECTED_FILES_BINDING'):self.portal.propose_preparation(rid,wrong)
                proposed=self.portal.propose_preparation(rid,preplan)
                self.portal.approve_preparation(rid,{'preparationPlanSha256':proposed['preparationPlanSha256']})
                roles=('RGB',) if mode=='OSC_CFA' else MODES[mode]
                native_count=3 if mode=='OSC_CFA' else len(roles)
                packet={**self.packet(rid),'nativeProcessCount':native_count,'checkpointCount':5 if mode=='OSC_CFA' else 3*len(roles),
                    'masters':[{'role':r,'width':1000,'height':800,'imageIndex':0} for r in roles]}
                result=self.portal.record_preparation(rid,packet)
                recipe=next(k for k,v in worker.RECIPE_MODES.items() if v==('OSC' if mode=='OSC_CFA' else mode))
                self.portal.register({'inputRef':'8'*32,'target':'M27','recipe':recipe,'manifestSha256':'9'*64,
                    'preparation':{'requestId':rid,'resultSha256':result['preparationResultSha256']}})
                plan={'workerId':WORKER,'inputRef':'8'*32,'manifestSha256':'9'*64,'recipe':recipe,'background':{'polyDegree':1,'boxSize':16,'boxSeparation':32},
                    'processing':copy.deepcopy(worker.PROCESSING_DEFAULTS),'field':self.field(),'masters':packet['masters'],
                    'rationale':'Piano finale sul mosaico lineare','limitations':'Colori non certificati','preparationResultSha256':result['preparationResultSha256']}
                final=self.portal.propose(rid,plan);self.assertEqual(self.portal.jobs(),[])
                job=self.portal.approve_plan(rid,{'proposalSha256':final['proposalSha256']})
                self.assertEqual(job['state'],'QUEUED')
                self.assertEqual(self.portal.context(job['jobId'])['intent']['plan']['preparation']['plan']['nativeProcessCount'],native_count)

    def test_http_preparation_proposal_result_and_owner_approval_have_separate_authority(self):
        import hashlib
        from http.server import HTTPServer
        import threading
        import urllib.request
        import urllib.error
        from .transport_http import handler_for, AuthError
        rid=self.request['requestId']
        selection={**self.selection(),'sourceProfile':{'mode':'OSC_CFA','layout':'SINGLE','bayerPattern':'RGGB','panels':[]}}
        self.portal.create_intake(selection)
        def owner(token):
            if token!='OWNER':raise AuthError()
        token=scientific_fixtures.TOKEN
        server=HTTPServer(('127.0.0.1',0),handler_for(self.broker,owner,'https://portal.test',hashlib.sha256(token.encode()).hexdigest(),self.portal))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        def request(path,body,identity):
            headers={'Authorization':'Bearer '+identity,'Content-Type':'application/json'}
            if identity=='OWNER':headers['Origin']='https://portal.test'
            return urllib.request.urlopen(urllib.request.Request(f'http://127.0.0.1:{server.server_port}'+path,encode(body),headers=headers))
        try:
            stem='/science/intakes/'+rid
            with self.assertRaises(urllib.error.HTTPError) as denied:request('/v1/worker'+stem+'/preparation',self.proposal(),'OWNER')
            self.assertEqual(denied.exception.code,403)
            with request('/v1/worker'+stem+'/preparation',self.proposal(),token) as response:proposal=decode(response.read())
            approval={'preparationPlanSha256':proposal['preparationPlanSha256']}
            with self.assertRaises(urllib.error.HTTPError) as denied:request('/v1'+stem+'/approve-preparation',approval,token)
            self.assertEqual(denied.exception.code,403)
            with request('/v1'+stem+'/approve-preparation',approval,'OWNER') as response:self.assertFalse(decode(response.read())['nativeStarted'])
            with self.assertRaises(urllib.error.HTTPError) as denied:request('/v1/worker'+stem+'/prepared',self.packet(rid),'OWNER')
            self.assertEqual(denied.exception.code,403)
            with request('/v1/worker'+stem+'/prepared',self.packet(rid),token) as response:self.assertEqual(decode(response.read())['state'],'AWAITING_PROCESSING_PLAN')
            self.assertEqual(self.portal.jobs(),[])
        finally:server.shutdown();server.server_close();thread.join()


class PreparationBridgeTests(unittest.TestCase):
    def fixture(self, base):
        rid='1'*32;helper=preparation_fixtures.PreparationTests()
        root,job,engine,source=helper.collection_fixture(base,'PREP_'+rid,width=1000,height=800)
        request=decode((job/'request.json').read_bytes())
        plan={'workerId':WORKER,'sourceManifestSha256':source_digest(request),'masters':[{'panelId':'P1','role':'CFA','width':1000,'height':800,'imageIndex':0,'filename':source.name}],
              'mode':'OSC_CFA','layout':'SINGLE','bayerPattern':'RGGB','canvas':None,'shrink':0,'feather':0}
        intake={'selection':{'requestId':rid,'masterDirectory':source.parent.as_posix(),'sourceProfile':{'mode':'OSC_CFA','layout':'SINGLE','bayerPattern':'RGGB','panels':[]}},'preparationPlan':plan,'preparationPlanSha256':sha(plan),'preparationApproved':True}
        worker.write_new(job/'owner-authorization.json',{'requestId':rid,'preparationPlanSha256':sha(plan),'sourceManifestSha256':source_digest(request),'intake':intake})
        with patch('tools.pixinsight.local_pilot.preparation.INSTALLED_ENGINE',engine):collect(root,job.name)
        return root,job,engine,source,rid

    def test_verified_preparation_is_only_exception_to_worker_internal_source_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            root,job,_,_,rid=self.fixture(Path(directory));inputs,trace=prepared_inputs(root,rid)
            request={'schemaVersion':'1.0','jobId':'FinalTest','recipe':worker.OSC_RECIPE,'inputs':inputs,
                     'background':{'polyDegree':1,'boxSize':16,'boxSeparation':32},'processing':copy.deepcopy(worker.PROCESSING_DEFAULTS),
                     'field':PreparationFlowTests.field(self),'preparationTrace':trace}
            with self.assertRaisesRegex(ValueError,'must be separate'):worker.prepare(root,{k:v for k,v in request.items() if k!='preparationTrace'})
            altered=copy.deepcopy(request);altered['preparationTrace']['outputManifestSha256']='0'*64
            with self.assertRaisesRegex(ProtocolError,'PROCESSING_INPUT_BINDING'):worker.prepare(root,altered)
            final=worker.prepare(root,request)
            self.assertEqual(decode((final/'manifest.json').read_bytes())['preparationTrace'],trace)
            self.assertEqual(worker.digest(final/'inputs/RGB.xisf'),inputs[0]['sha256'])

    def test_changed_original_output_journal_authorization_or_unclosed_stage_never_bridges(self):
        for conflict in ('original','output','journal','authorization','closed'):
            with self.subTest(conflict=conflict),tempfile.TemporaryDirectory() as directory:
                root,job,_,source,rid=self.fixture(Path(directory))
                if conflict=='original':source.write_bytes(source.read_bytes()+b'changed')
                elif conflict=='output':(job/'outputs/RGB-linear.xisf').write_bytes(b'changed')
                elif conflict=='journal':(job/'events/0001.json').write_bytes(b'{}')
                elif conflict=='closed':(job/'reservation-closed.json').rename(job/'closed-missing.json')
                else:
                    value=decode((job/'owner-authorization.json').read_bytes());value['intake']['preparationApproved']=False
                    (job/'owner-authorization.json').write_bytes(encode(value))
                with self.assertRaises((ValueError,ProtocolError)):prepared_inputs(root,rid)

    def test_runtime_graph_links_cfa_source_to_prepared_rgb_and_keeps_native_source_local(self):
        with tempfile.TemporaryDirectory() as directory:
            root,job,_,_,rid=self.fixture(Path(directory));_,trace=prepared_inputs(root,rid)
            instances,relations,roles=runtime_graph(root,trace)
            self.assertEqual([p['process'] for p in instances],['Debayer'])
            self.assertEqual(relations[-1]['target'],'PREPARED_RGB')
            self.assertEqual(relations[0]['dependencies'],['MASTER_CFA_P1'])
            self.assertEqual(len(roles),1)
            self.assertNotIn(root.as_posix(),json.dumps(relations))

    def test_combined_export_orders_preparation_before_recipe_and_minimizes_source_dependencies(self):
        from .scientific_delivery import minimized_correlations
        from tools.pixinsight.workflow_archive.export_parser import parse_export
        with tempfile.TemporaryDirectory() as directory:
            root,_,_,_,rid=self.fixture(Path(directory));inputs,trace=prepared_inputs(root,rid)
            request={'schemaVersion':'1.0','jobId':'PartialFinal','recipe':worker.OSC_RECIPE,'inputs':inputs,
                'background':{'polyDegree':1,'boxSize':16,'boxSeparation':32},'processing':copy.deepcopy(worker.PROCESSING_DEFAULTS),
                'field':PreparationFlowTests.field(self),'preparationTrace':trace}
            final=worker.prepare(root,request);manifest=decode((final/'manifest.json').read_bytes())
            worker.write_new(final/'events/0001.json',{'event':'process-started','data':{'label':'background-RGB','target':'FinalRGB','dependencies':[inputs[0]['sha256']],'nativeSource':'var P = new AutomaticBackgroundExtractor;'}})
            worker.write_new(final/'events/0002.json',{'event':'process-completed','data':{'label':'background-RGB','target':'FinalRGB'}})
            exported=worker.export_runtime_instances(final,{'recipe':worker.OSC_RECIPE,'jobId':request['jobId'],'processCount':1})
            self.assertEqual(exported['instanceCount'],2)
            parsed=parse_export((final/'workflow.js').read_text(),profile='1.2');instances=parsed['instances'];parent=instances[parsed['root']]
            self.assertEqual([instances[name]['process'] for name in parent['children']],['Debayer','AutomaticBackgroundExtractor'])
            correlations=decode(minimized_correlations((final/'runtime-correlations.json').read_bytes(),manifest))
            self.assertEqual(correlations['instances'][1]['dependencies'],['PREPARED_RGB'])
            self.assertEqual(correlations['preparation']['trace'],trace)
            self.assertEqual(correlations['runtimeRelations'][0]['dependencies'],['MASTER_CFA_P1'])
