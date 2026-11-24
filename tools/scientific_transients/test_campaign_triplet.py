"""Synthetic triplet ordering with actual local driver and owned mock processes.

No native image processing or scientific validation. The positive ordering test
injects explicitly synthetic quality counts into the mock collector; it cannot
prove the real aperture engine has complete uncertainty or qualify a control.
"""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import encode, ProtocolError
from tools.scientific_transients import test_native_aperture as native_fixtures
from tools.scientific_transients import test_native_supervisor as supervisor_fixtures
from tools.scientific_transients import test_confirmatory_campaign as campaign_fixtures
from tools.scientific_transients import native_supervisor
from tools.scientific_transients import campaign_triplet as module
from tools.scientific_transients.campaign_triplet import CampaignTriplet
from tools.scientific_transients.campaign_dispatch import BASE
from tools.scientific_transients.campaign_input_archive import CampaignInputArchive
from tools.scientific_transients.campaign_queue import CampaignQueue
from tools.scientific_transients.local_registry import LocalRegistry, fingerprint
from tools.scientific_transients.attempt_journal import write_new
from tools.scientific_transients.operator_run import OperatorPlan, ORIGIN
from tools.scientific_transients.queue import TransientQueue, CAMPAIGN_PROFILE
ref=campaign_fixtures.ref


class TripletTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        for name in ('source','archives','coordinators'): (self.root/name).mkdir()
        self.f=campaign_fixtures.CampaignTests();self.f.setUp()
        self.plans=[];self.natives=[];frames=[];files=[]
        self.events=[];self.elapsed=0;self.active=None;self.processes=[];self.calls=[]
        self.lose_reserve=False;self.lose_closure=False;self.timeout=False
        self.owner_lost=False;self.revoke_after_closure=False
        for ordinal in range(3):
            native=native_fixtures.NativeReceiptTests();native.setUp();self.addCleanup(native.doCleanups)
            self.natives.append(native);native.operation=ref(70000+ordinal)
            native.input.write_bytes(('SYNTHETIC INPUT '+str(ordinal)).encode())
            artifacts=native.root/'artifacts';artifacts.mkdir();native.runs=artifacts/'runs';native.runs.mkdir()
            run=native.prepare();registry=native.root/'registry';registry.mkdir()
            local=LocalRegistry(artifacts,registry)
            binding=dict(bindingRef=ref(61000+ordinal),inputRef=ref(1000+ordinal),referenceRef=ref(62000),
                         algorithmRef=ref(20),contractRef=ref(30))
            for name in ('reference.json','contract.json','provenance.json'):
                (artifacts/name).write_bytes(b'SYNTHETIC fixture proof')
            paths=dict(INPUT=run/'input.xisf',PARAMETERS=run/'parameters.json',ALGORITHM=run/'native_aperture.jsh',
                       REFERENCE=artifacts/'reference.json',CONTRACT=artifacts/'contract.json',PROVENANCE=artifacts/'provenance.json')
            manifest={'protocol':'DSG_TRANSIENT_LOCAL_BINDING_V1','binding':binding,'files':[
                dict(role=role,path=path.relative_to(artifacts).as_posix(),**fingerprint(path)) for role,path in paths.items()]}
            registered=local.register(encode(manifest))
            roots=dict(artifacts=artifacts,registry=registry,run=run)
            for name in ('intents','journals','outboxes'):roots[name]=native.root/name;roots[name].mkdir()
            plan=dict(protocol='DSG_TRANSIENT_OPERATOR_PLAN_V1',serviceOrigin=ORIGIN,workerId=ref(2),rootId=ref(64000),
                jobId='TRN_'+ref(60000+ordinal),reservationRef=ref(71000+ordinal),binding=binding,
                manifestSha256=registered['manifestSha256'],operationRef=native.operation,
                paths={k:str(v) for k,v in roots.items()},timeoutSeconds=10)
            path=native.root/'operator-plan.json';sha=write_new(path,plan)
            self.plans.append(OperatorPlan.load(path,sha,engine=native.engine,catalog=native.catalog))
            frame=copy.deepcopy(self.f.inputs[0]['frames'][ordinal]);hashes={}
            for role in ('IMAGE','METADATA','BANDPASS','CALIBRATION_PROOF','UNCERTAINTY_PROOF','TIME_PROOF'):
                raw=native.input.read_bytes() if role=='IMAGE' else b'SYNTHETIC '+role.encode()
                name=str(ordinal)+'-'+role+'.dat';(self.root/'source'/name).write_bytes(raw)
                mark=fingerprint(self.root/'source'/name);hashes[role]=mark['sha256']
                files.append(dict(role=role,frameRef=frame['frameRef'],path=name,**mark))
            frame.update(sha256=hashes['IMAGE'],metadataSha256=hashes['METADATA'],bandpassSha256=hashes['BANDPASS'])
            frames.append(frame)
        source=dict(protocol='DSG_CAMPAIGN_INPUT_SOURCE_V1',witness=dict(witnessRef=ref(90000),
            purpose='CONFIRMATORY_RESERVED_REAL',correlationRef=ref(90001),frames=frames),files=files)
        # REAL purpose is protocol-shaped fixture metadata, never a real observation.
        manifest=self.root/'manifest.json';manifest_sha=write_new(manifest,source)
        self.archive=CampaignInputArchive.prepare(self.root/'source',manifest,manifest_sha,self.root/'archives')
        witness=self.archive.verify();self.f.service.register_inputs(witness);self.f.inputs[0]=witness
        request=copy.deepcopy(self.f.request);request['planRef']=ref(11);request['inputWitnessRefs'][0]=witness['witnessRef']
        request['algorithmSha256']=fingerprint(self.plans[0].roots['run']/'native_aperture.jsh')['sha256']
        request['contractSha256']=fingerprint(self.plans[0].roots['artifacts']/'contract.json')['sha256']
        self.f.service.create(request)
        for i,item in enumerate(self.f.inputs):
            review=dict(decisionId=ref(91000+i),witnessSha256=campaign_fixtures.fingerprint(item),
                nullReferenceSha256=campaign_fixtures.sha(8000+i),independenceSha256=campaign_fixtures.sha(9000+i),
                modelReviewSha256=campaign_fixtures.sha(10000+i),separationEvidenceSha256=campaign_fixtures.sha(11000+i),
                algorithmSha256=request['algorithmSha256'],contractSha256=request['contractSha256'],
                acceptNullReference=True,acceptIndependence=True,acceptScienceModel=True,acceptDevelopmentSeparation=True)
            self.f.service.review_input(item['witnessRef'],review)
        self.f.service.freeze(ref(11),self.f.freeze_request(ref(11)))
        self.queue=TransientQueue(self.f.store,ref(2),clock=lambda:self.f.now,state_ref=ref(95000),capacity_profile=CAMPAIGN_PROFILE)
        self.bridge=CampaignQueue(self.f.service,self.queue)
        self.context=self.f.service.dispatch_context(ref(11),witness['witnessRef'])
        self.context_path=self.root/'context.json';self.context_sha=write_new(self.context_path,self.context)
        test=self
        class Owner:
            def request(self,path,body):
                test.calls.append(('owner',path));test.events.append('owner-post')
                if path.endswith('/dispatch-intents'):result=test.bridge.prepare_dispatch(ref(11),body)
                else:
                    parts=path.split('/');result=test.bridge.project(ref(11),parts[-4],int(parts[-2]))
                if test.owner_lost:raise OSError('synthetic Owner ack lost')
                return result
        class Worker:
            def request(self,path,value=None):
                test.calls.append(('worker',path))
                if path.endswith('/register'):return test.queue.register(value)
                if path.endswith('/technical-context'):
                    parts=path.split('/');return test.bridge.technical_context(ref(11),parts[-4],int(parts[-2]))
                if path.endswith('/reserve-once'):
                    parts=path.split('/');test.events.append('reserve-'+parts[-2])
                    result=test.bridge.reserve_envelope(ref(11),parts[-4],int(parts[-2]),value['reservation'],value['decisionId'])
                    if test.lose_reserve:raise OSError('synthetic reserve ack lost')
                    return result
                if path.endswith('/frame-closures'):
                    event=test.bridge.close_frame(ref(11),value)
                    ordinal=len([e for e in test.events if e.startswith('closure-')])
                    test.events.append('closure-'+str(ordinal))
                    if test.revoke_after_closure:
                        test.f.service.revoke(ref(11),dict(decisionId=ref(99000),
                            planHeadSha256=test.f.service.view(ref(11))['headSha256'],evidenceSha256='a'*64,reason='OWNER_WITHDRAWAL'))
                    if test.lose_closure:raise OSError('synthetic closure ack lost')
                    return dict(protocol='DSG_CAMPAIGN_FRAME_CLOSURE_RECEIPT_V1',closureSha256=event['sha256'],
                        admissionSha256=value['admissionSha256'],status=value['technicalState'],nativeStoppedAttested=False,
                        scientificValidation='NOT_VALIDATED')
                return test.queue.worker_receipt(path.rsplit('/',1)[-1])
            def post(self,path,value):return test.queue.report(path.split('/')[-2],value)
        self.owner,self.worker=Owner(),Worker()

    def prepare(self):return CampaignTriplet.prepare(self.root/'coordinators',self.context_path,self.context_sha,
                                                    self.archive,self.plans,ref(96000))

    def spawn(self,directory):
        ordinal=next(i for i,p in enumerate(self.plans) if p.roots['run']==directory)
        self.assertTrue(all(p.closed for p in self.processes))
        self.active=ordinal;self.events.append('start-'+str(ordinal))
        process=supervisor_fixtures.OwnedMock();self.processes.append(process);return process

    def sleep(self,seconds):
        self.elapsed+=seconds
        if not self.timeout:self.natives[self.active].terminal(self.plans[self.active].roots['run'])

    def run_triplet(self,triplet,synthetic_complete_counts=False):
        original=native_supervisor.collect_run
        def collect(*args,**kwargs):
            value=original(*args,**kwargs)
            if synthetic_complete_counts:value['qualityCounts']=dict(measured=1,excluded=0,incomplete=0)
            return value
        with patch.object(native_supervisor,'collect_run',side_effect=collect):
            return triplet.run(self.owner,self.worker,native_launch_authorized=True,
                spawn=self.spawn,clock=lambda:self.elapsed,sleep=self.sleep)

    def test_three_mock_starts_are_sequential_and_each_requires_previous_closure_ack(self):
        triplet=self.prepare();result=self.run_triplet(triplet,True)
        self.assertEqual(result['completedFrames'],3);self.assertEqual(result['qualifiedControls'],0)
        self.assertEqual([e for e in self.events if e.startswith(('reserve-','start-','closure-'))],
            ['reserve-0','start-0','closure-0','reserve-1','start-1','closure-1','reserve-2','start-2','closure-2'])
        self.assertTrue(all(p.closed for p in self.processes))
        self.assertEqual(self.f.service.view(ref(11))['qualifiedControls'],0)
        with self.assertRaises(ProtocolError):self.run_triplet(triplet,True)
        calls=len(self.calls)
        with self.assertRaises((FileExistsError,ProtocolError)):self.prepare()
        self.assertEqual(len(self.calls),calls)
        for path in triplet.directory.rglob('*.json'):
            self.assertNotIn(b'leaseToken',path.read_bytes())

    def test_incomplete_real_diagnostic_report_cannot_advance_to_second_frame(self):
        triplet=self.prepare()
        with self.assertRaises(ProtocolError):self.run_triplet(triplet)
        self.assertEqual([e for e in self.events if e.startswith('start-')],['start-0'])
        self.assertTrue(self.processes[0].closed)
        self.assertNotIn('closure-0',self.events)
        self.assertEqual(triplet.phase,'RECONCILIATION_REQUIRED')

    def test_lost_reservation_ack_has_no_start_and_no_repeat(self):
        triplet=self.prepare();self.lose_reserve=True
        with self.assertRaises(ProtocolError):self.run_triplet(triplet,True)
        self.assertEqual(self.processes,[]);calls=len(self.calls)
        with self.assertRaises(ProtocolError):self.run_triplet(triplet,True)
        self.assertEqual(len(self.calls),calls)

    def test_lost_closure_ack_stops_after_first_owned_process_closed(self):
        triplet=self.prepare();self.lose_closure=True
        with self.assertRaises(ProtocolError):self.run_triplet(triplet,True)
        self.assertEqual(len(self.processes),1);self.assertTrue(self.processes[0].closed)
        self.assertNotIn('reserve-1',self.events)

    def test_timeout_retains_process_and_blocks_second_frame(self):
        triplet=self.prepare();self.timeout=True
        with self.assertRaises(ProtocolError):self.run_triplet(triplet,True)
        self.assertEqual(len(self.processes),1);self.assertFalse(self.processes[0].closed)
        self.assertNotIn('reserve-1',self.events)

    def test_revoke_after_first_closure_prevents_next_projection_and_start(self):
        triplet=self.prepare();self.revoke_after_closure=True
        with self.assertRaises(ProtocolError):self.run_triplet(triplet,True)
        self.assertEqual(len(self.processes),1);self.assertNotIn('reserve-1',self.events)

    def test_changed_context_and_wrong_frame_order_refuse_before_network(self):
        self.plans.reverse()
        with self.assertRaises(ProtocolError):self.prepare()
        self.plans.reverse();triplet=self.prepare()
        self.context_path.write_bytes(self.context_path.read_bytes()+b' ')
        with self.assertRaises(ProtocolError):self.run_triplet(triplet,True)
        self.assertEqual(self.calls,[])

    def test_no_explicit_launch_and_owner_ack_lost_never_start(self):
        triplet=self.prepare()
        for flag in (False,1,None):
            with self.assertRaises(ProtocolError):triplet.run(self.owner,self.worker,native_launch_authorized=flag)
        self.assertEqual(self.calls,[])
        self.owner_lost=True
        with self.assertRaises(ProtocolError):self.run_triplet(triplet,True)
        self.assertEqual(self.processes,[])

    def test_missing_owned_stop_receipt_blocks_closure_and_next_start(self):
        triplet=self.prepare();original=module.read_json
        def read(path):
            if path.name=='owned-process-closed.json':raise OSError('synthetic missing stop record')
            return original(path)
        with patch.object(module,'read_json',side_effect=read):
            with self.assertRaises(ProtocolError):self.run_triplet(triplet,True)
        self.assertEqual(len(self.processes),1);self.assertTrue(self.processes[0].closed)
        self.assertNotIn('closure-0',self.events);self.assertNotIn('reserve-1',self.events)

    def test_closure_ack_retention_failure_never_advances_even_after_server_commit(self):
        triplet=self.prepare();original=module.write_new
        def write(path,value):
            if path.name=='closure-ack.json':raise OSError('synthetic retention failure')
            return original(path,value)
        with patch.object(module,'write_new',side_effect=write):
            with self.assertRaises(ProtocolError):self.run_triplet(triplet,True)
        self.assertEqual(len(self.processes),1);self.assertIn('closure-0',self.events)
        self.assertNotIn('reserve-1',self.events)

    def test_lost_binding_registration_ack_has_no_projection_or_native_start(self):
        triplet=self.prepare();original=self.worker.request
        def request(path,value=None):
            result=original(path,value)
            if path.endswith('/register'):raise OSError('synthetic register ack lost')
            return result
        self.worker.request=request
        with self.assertRaises(ProtocolError):self.run_triplet(triplet,True)
        self.assertEqual(self.processes,[])
        self.assertEqual(len([p for role,p in self.calls if role=='owner']),1)

    def test_archive_mutation_is_detected_before_owner_mutation(self):
        triplet=self.prepare();path=self.archive.directory/'manifest.json'
        path.write_bytes(path.read_bytes()+b' ')
        with self.assertRaises(ProtocolError):self.run_triplet(triplet,True)
        self.assertEqual(self.calls,[])


if __name__=='__main__':unittest.main()
