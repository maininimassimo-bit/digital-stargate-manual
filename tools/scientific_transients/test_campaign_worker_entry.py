"""Explicit Worker entry with synthetic server, mock native and nonsecret files."""
import contextlib
import copy
import io
import json
import os
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients import test_campaign_triplet as fixtures
from tools.scientific_transients import campaign_triplet as module
from tools.scientific_transients import campaign_worker_cli as cli
from tools.scientific_transients import native_supervisor
from tools.scientific_transients.campaign_handoff import make_handoff, COMMON, JOB
from tools.scientific_transients.attempt_journal import write_new
ref=fixtures.ref


class WorkerEntryTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.TripletTests();self.f.setUp();self.addCleanup(self.f.doCleanups)

    def inputs(self):
        f=self.f
        return (f.root/'coordinators',f.context_path,f.context_sha,f.archive,f.plans,ref(96000))

    def prepared(self):return module.CampaignTriplet.prepare(*self.inputs())

    def registered(self):
        triplet=self.prepared();triplet.register_all(self.f.worker);return triplet

    def owner_handoff(self,triplet):
        proposal=triplet.owner_proposal()
        intent=self.f.bridge.prepare_dispatch(ref(11),proposal['request'])
        for ordinal in range(3):self.f.bridge.project(ref(11),intent['sha256'],ordinal)
        rows=[self.f.bridge.technical_context(ref(11),intent['sha256'],i) for i in range(3)]
        return make_handoff({k:rows[0][k] for k in COMMON},[{k:r[k] for k in JOB} for r in rows])

    def run_worker(self,triplet,handoff):
        original=native_supervisor.collect_run
        def collect(*args,**kwargs):
            result=original(*args,**kwargs)
            # Ordering fixture only, never a scientific proof.
            result['qualityCounts']=dict(measured=1,excluded=0,incomplete=0);return result
        with patch.object(native_supervisor,'collect_run',side_effect=collect):
            return triplet.run_worker(handoff,self.f.worker,native_launch_authorized=True,
                spawn=self.f.spawn,clock=lambda:self.f.elapsed,sleep=self.f.sleep)

    def test_register_all_owner_handoff_and_worker_entry_have_separate_authority(self):
        triplet=self.registered();self.assertEqual(len(self.f.calls),3)
        handoff=self.owner_handoff(triplet)
        reopened=module.CampaignTriplet.reopen_registered(*self.inputs())
        result=self.run_worker(reopened,handoff)
        self.assertEqual(result['completedFrames'],3);self.assertEqual(result['qualifiedControls'],0)
        self.assertEqual(len(self.f.processes),3)
        self.assertTrue(all(p.closed for p in self.f.processes))
        self.assertTrue(all(role=='worker' for role,path in self.f.calls))
        self.assertEqual(len([p for _,p in self.f.calls if p.endswith('/register')]),3)
        with self.assertRaises((ProtocolError,FileExistsError)):module.CampaignTriplet.reopen_registered(*self.inputs())
        with self.assertRaises(ProtocolError):self.run_worker(reopened,handoff)

    def test_reopen_prepared_only_before_registration_and_proposal_requires_all_acks(self):
        triplet=self.prepared()
        with self.assertRaises(ProtocolError):triplet.owner_proposal()
        reopened=module.CampaignTriplet.reopen_prepared(*self.inputs());reopened.register_all(self.f.worker)
        self.assertEqual(reopened.owner_proposal()['request']['archiveSha256'],self.f.archive.sha)
        with self.assertRaises(ProtocolError):module.CampaignTriplet.reopen_prepared(*self.inputs())
        for path in reopened.directory.rglob('*.json'):
            self.assertNotIn(b'leaseToken',path.read_bytes());self.assertNotIn(b'Bearer ',path.read_bytes())

    def test_registration_loss_stops_all_further_bindings_and_no_proposal(self):
        triplet=self.prepared();original=self.f.worker.request
        def lost(path,value=None):
            original(path,value);raise OSError('synthetic lost registration ack')
        self.f.worker.request=lost
        with self.assertRaises(ProtocolError):triplet.register_all(self.f.worker)
        self.assertEqual(len(self.f.calls),1)
        with self.assertRaises(ProtocolError):triplet.owner_proposal()
        with self.assertRaises(ProtocolError):module.CampaignTriplet.reopen_registered(*self.inputs())
        with self.assertRaises(ProtocolError):module.CampaignTriplet.reopen_prepared(*self.inputs())

    def test_stale_consumed_handoff_and_observation_loss_never_resume(self):
        triplet=self.registered();handoff=self.owner_handoff(triplet)
        original=self.f.worker.request
        def unavailable(path,value=None):
            if path.endswith('/technical-context'):raise OSError('synthetic GET404 or unavailable')
            return original(path,value)
        self.f.worker.request=unavailable
        with self.assertRaises(ProtocolError):self.run_worker(triplet,handoff)
        self.f.worker.request=original
        with self.assertRaises(ProtocolError):self.run_worker(triplet,handoff)
        with self.assertRaises(ProtocolError):module.CampaignTriplet.reopen_registered(*self.inputs())
        self.assertEqual(self.f.processes,[])

    def test_wrong_handoff_local_bytes_refused_before_any_remote_read(self):
        triplet=self.registered();handoff=self.owner_handoff(triplet)
        common={k:handoff[k] for k in COMMON};common['archiveSha256']='f'*64
        forged=make_handoff(common,[{k:j[k] for k in JOB} for j in handoff['jobs']])
        before=len(self.f.calls)
        with self.assertRaises(ProtocolError):self.run_worker(triplet,forged)
        self.assertEqual(len(self.f.calls),before);self.assertEqual(self.f.processes,[])

    def test_launch_intent_fsync_failure_has_no_remote_reads_or_native(self):
        triplet=self.registered();handoff=self.owner_handoff(triplet);before=len(self.f.calls)
        with patch('tools.scientific_transients.attempt_journal.os.fsync',side_effect=OSError('synthetic fsync')):
            with self.assertRaises(ProtocolError):self.run_worker(triplet,handoff)
        self.assertEqual(len(self.f.calls),before);self.assertEqual(self.f.processes,[])
        with self.assertRaises(ProtocolError):module.CampaignTriplet.reopen_registered(*self.inputs())

    def test_lost_reservation_ack_halts_worker_entry(self):
        triplet=self.registered();handoff=self.owner_handoff(triplet);self.f.lose_reserve=True
        with self.assertRaises(ProtocolError):self.run_worker(triplet,handoff)
        self.assertEqual(self.f.processes,[])
        self.assertEqual(len([p for _,p in self.f.calls if p.endswith('/reserve-once')]),1)

    def test_lost_closure_ack_halts_worker_entry_before_second_frame(self):
        triplet=self.registered();handoff=self.owner_handoff(triplet);self.f.lose_closure=True
        with self.assertRaises(ProtocolError):self.run_worker(triplet,handoff)
        self.assertEqual(len(self.f.processes),1);self.assertTrue(self.f.processes[0].closed)
        self.assertNotIn('reserve-1',self.f.events)

    def test_consumed_server_admission_blocks_fresh_worker_entry(self):
        triplet=self.registered();handoff=self.owner_handoff(triplet)
        intent=handoff['intentSha256']
        self.f.bridge.admit_and_reserve(ref(11),intent,0,dict(workerId=ref(2),rootId=ref(64000),
            jobId=self.f.plans[0].value['jobId'],bindingRef=self.f.plans[0].value['binding']['bindingRef'],
            reservationRef=self.f.plans[0].value['reservationRef']),ref(71000))
        with self.assertRaises(ProtocolError):self.run_worker(triplet,handoff)
        self.assertEqual(self.f.processes,[])

    def test_cli_worker_dispatch_clears_token_before_explicit_run_entry(self):
        path,sha=self.config();triplet=self.registered();handoff=self.owner_handoff(triplet)
        handoff_path=self.f.root/'handoff.json';handoff_sha=write_new(handoff_path,handoff)
        token='d'*64;test=self;calls=[]
        def run(instance,received,transport,**options):
            test.assertNotIn('DSG_TRANSIENT_OPERATOR_TOKEN',os.environ)
            test.assertEqual(received,handoff);test.assertIs(options['native_launch_authorized'],True)
            calls.append(True)
            return dict(state='COMPLETED',completedFrames=3,qualifiedControls=0,scientificValidation='NOT_VALIDATED')
        with patch.dict(os.environ,{'DSG_TRANSIENT_OPERATOR_TOKEN':token}), \
             patch.object(cli,'CampaignWorkerTransport'),patch.object(module.CampaignTriplet,'run_worker',run), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(cli.main(['run-worker','--config',str(path),'--config-sha256',sha,
                '--handoff',str(handoff_path),'--handoff-sha256',handoff_sha,'--authorize-native-launch'],
                engine=self.f.natives[0].engine,catalog=self.f.natives[0].catalog),0)
            self.assertEqual(calls,[True]);self.assertNotIn(token,output.getvalue())

    def config(self):
        f=self.f
        value=dict(protocol='DSG_CAMPAIGN_LOCAL_RUN_CONFIG_V1',contextPath=str(f.context_path),
            contextFileSha256=f.context_sha,archiveDirectory=str(f.archive.directory),archiveSha256=f.archive.sha,
            coordinatorRoot=str(f.root/'coordinators'),decisionId=ref(96000),
            operatorPlans=[dict(path=str(p.path),sha256=p.sha) for p in f.plans])
        path=f.root/'worker-config.json';sha=write_new(path,value);return path,sha

    def test_cli_preflight_prepare_and_export_do_not_load_credentials(self):
        path,sha=self.config();base=['--config',str(path),'--config-sha256',sha]
        engine,catalog=self.f.natives[0].engine,self.f.natives[0].catalog
        with patch.object(cli,'CampaignWorkerTransport') as transport,patch.dict(os.environ,{},clear=True), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(cli.main(['preflight']+base,engine=engine,catalog=catalog),0)
            self.assertEqual(cli.main(['prepare']+base,engine=engine,catalog=catalog),0)
            transport.assert_not_called()
        triplet=module.CampaignTriplet.reopen_prepared(*self.inputs());triplet.register_all(self.f.worker)
        destination=self.f.root/'owner-proposal.json'
        with patch.object(cli,'CampaignWorkerTransport') as transport,contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(['export-owner-proposal']+base+['--output',str(destination)],engine=engine,catalog=catalog),0)
            transport.assert_not_called()
        raw=destination.read_text();self.assertNotIn(str(self.f.root),raw);self.assertNotIn('token',raw.lower())

    def test_cli_missing_launch_authorization_does_not_load_config_or_construct_transport(self):
        with patch.object(cli,'load_config') as load,patch.object(cli,'CampaignWorkerTransport') as transport, \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(['run-worker','--config','private','--config-sha256','a'*64,
                '--handoff','private','--handoff-sha256','b'*64]),2)
            load.assert_not_called();transport.assert_not_called()

    def test_cli_removes_dedicated_token_before_any_native_child_and_never_prints_it(self):
        path,sha=self.config();self.prepared();token='c'*64;test=self
        class Transport:
            def __init__(self,origin,secret):
                test.assertEqual(secret,token);test.assertNotIn('DSG_TRANSIENT_OPERATOR_TOKEN',os.environ)
            def request(self,path,value=None):
                test.assertNotIn('DSG_TRANSIENT_OPERATOR_TOKEN',os.environ)
                return test.f.worker.request(path,value)
        with patch.dict(os.environ,{'DSG_TRANSIENT_OPERATOR_TOKEN':token}), \
             patch.object(cli,'CampaignWorkerTransport',Transport),contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(cli.main(['register-all','--config',str(path),'--config-sha256',sha],
                engine=self.f.natives[0].engine,catalog=self.f.natives[0].catalog),0)
            self.assertNotIn(token,output.getvalue());self.assertNotIn(str(path),output.getvalue())
            self.assertNotIn('DSG_TRANSIENT_OPERATOR_TOKEN',os.environ)


if __name__=='__main__':unittest.main()
