"""Local coordinator safety tests; no provider, desktop or native execution."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock,patch

from .adaptive_worker import AdaptiveWorker
from .broker import encode
from .image_analysis import fingerprint


class AdaptiveWorkerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);(self.root/'transport').mkdir()
        (self.root/'transport/root-identity.json').write_bytes(encode({'workerId':'worker-fixture','rootId':'1'*32}))
        for module in ('adaptive_worker','adaptive_native_adapter','native_analysis'):
            guard=patch('tools.pixinsight.local_pilot.'+module+'.local_directory',lambda p:p)
            guard.start();self.addCleanup(guard.stop)
        self.transport=Mock()
        self.config={'workerId':'worker-fixture','workerRoot':str(self.root)}
        self.settings={'allowedMasterRoots':[str(self.root)]}
        self.runner=AdaptiveWorker(self.config,self.settings,self.transport)

    def test_default_worker_cannot_launch_native_or_consume_start(self):
        with self.assertRaises(ValueError):self.runner.run_native('a'*32,self.root,{})
        self.transport.post.assert_not_called()
        self.assertFalse((self.root/'launch.json').exists())

    def test_initial_unprepared_intake_waits_without_provider_or_native_action(self):
        self.transport.request.return_value={'intakes':[{'selection':{'requestId':'a'*32,'adaptivePlanning':{}},
                                                          'state':'AWAITING_ASSISTANT_PLAN','adaptive':None}]}
        # Actual intake consents are retained; no missing record can generate analysis.
        self.transport.request.return_value['intakes'][0]['selection']['adaptivePlanning']={'previewTransferConfirmed':True}
        result=self.runner.cycle()
        self.assertEqual(result['requests'][0]['state'],'AWAITING_OWNER_OR_SUPERVISED_ANALYSIS')
        self.assertFalse(result['supervisedNativeLaunchEnabled'])
        self.transport.post.assert_not_called()

    def test_initial_catalog_reuses_verified_setup_for_new_intakes_without_inventing_consents(self):
        profile={'mode':'LRGB','layout':'SINGLE','bayerPattern':None,'panels':[],'additionalDirectories':[]}
        setup={'fixture':'bound native analysis'}
        entry={'masterDirectory':str(self.root),'mode':'LRGB','layout':'SINGLE','analysis':setup}
        self.settings['initialAnalysisCatalog']=[entry]
        for request_id in ('a'*32,'b'*32):
            intake={'selection':{'requestId':request_id,'masterDirectory':str(self.root),'sourceProfile':profile}}
            self.assertEqual(self.runner.initial_analysis(intake),setup)
            self.assertNotIn('adaptivePlanning',intake['selection'])
        other=self.root/'other';other.mkdir()
        intake['selection']['masterDirectory']=str(other)
        self.assertIsNone(self.runner.initial_analysis(intake))
        intake['selection']['masterDirectory']=str(self.root)
        intake['selection']['sourceProfile']={**profile,'mode':'SHO'}
        self.assertIsNone(self.runner.initial_analysis(intake))
        self.transport.post.assert_not_called()

    def test_duplicate_initial_catalog_entries_cannot_choose_an_arbitrary_analysis(self):
        entry={'masterDirectory':str(self.root),'mode':'LRGB','layout':'SINGLE','analysis':{'fixture':'native'}}
        self.settings['initialAnalysisCatalog']=[entry,entry]
        intake={'selection':{'requestId':'a'*32,'masterDirectory':str(self.root),'sourceProfile':
            {'mode':'LRGB','layout':'SINGLE','bayerPattern':None,'panels':[],'additionalDirectories':[]}}}
        with self.assertRaises(ValueError):self.runner.initial_analysis(intake)
        self.transport.post.assert_not_called()

    def test_close_lease_requires_exact_cleanup_receipt_and_owned_identity(self):
        attempt=self.runner.directory/'attempt';attempt.mkdir()
        binding={'jobId':'PIAI_'+'a'*32,'permitSha256':'b'*64}
        lease=self.root/'active-job.json';lease.write_bytes(encode(binding))
        with self.assertRaises(OSError):self.runner.close_lease(attempt,binding)
        (attempt/'native-done.json').write_bytes(encode({'status':'OWNED_VIEWS_CLOSED','permitSha256':'c'*64}))
        with self.assertRaises(ValueError):self.runner.close_lease(attempt,binding)
        self.assertTrue(lease.exists())
        (attempt/'native-done.json').write_bytes(encode({'status':'OWNED_VIEWS_CLOSED','permitSha256':'b'*64}))
        self.runner.close_lease(attempt,binding)
        self.assertFalse(lease.exists());self.assertTrue((attempt/'native-lease-closed.json').exists())

    def test_source_set_substitution_rejected_before_local_file_access(self):
        descriptor={'role':'L','sha256':'a'*64,'imageIndex':0,'width':64,'height':64,'channels':1}
        self.settings['sources']=[{**descriptor,'sha256':'b'*64,'path':'F:/private/master.xisf'}]
        with patch('tools.pixinsight.local_pilot.adaptive_worker.local_file',side_effect=AssertionError('No file access')):
            with self.assertRaises(ValueError):self.runner.source_set('a'*32,{'inputs':[descriptor]})

    def test_delivery_retry_rechecks_scientific_files_before_backend_mutation(self):
        session=self.runner.directory/'session';session.mkdir()
        image=session/'RGB.xisf';image.write_bytes(b'original')
        expected=fingerprint(image)
        (session/'delivery.json').write_bytes(encode({'delivery':{'artifacts':[{'localPath':str(image),'sha256':expected}]}}))
        image.write_bytes(b'changed')
        with self.assertRaises(ValueError):self.runner.deliver('a'*32,{},session)
        self.transport.post.assert_not_called()

    def test_committed_checkpoint_lost_reply_reconciles_owned_lease_before_decision(self):
        request_id='a'*32;job_id='PIAI_'+request_id
        session=self.runner.directory/job_id;session.mkdir()
        previous=session/'segment-0';previous.mkdir()
        binding={'jobId':job_id,'permitSha256':'b'*64,'manifestSha256':'c'*64,'permit':{'ordinal':0}}
        (previous/'binding.json').write_bytes(encode(binding))
        (previous/'native-done.json').write_bytes(encode({'status':'OWNED_VIEWS_CLOSED','permitSha256':'b'*64}))
        (self.root/'active-job.json').write_bytes(encode({'jobId':job_id,'permitSha256':'b'*64}))
        result={'verification':{'ordinal':0,'outputs':['FIXTURE']}}
        (previous/'verification.json').write_bytes(encode(result));(previous/'decision.json').write_bytes(encode({'fixture':'decision'}))
        context={'executionPolicy':{},'analysis':{},'cursor':{'ordinal':1,'state':'AWAITING_DECISION'},
                 'job':{'jobId':job_id,'state':'RUNNING','cancelRequested':False},'checkpoint':result['verification']}
        self.transport.request.return_value=context
        with patch('tools.pixinsight.local_pilot.adaptive_worker.verify',return_value=result) as physical:
            self.assertEqual(self.runner.advance(request_id),'CHECKPOINT_DECISION')
        physical.assert_called_once_with(previous,expected_manifest_sha256='c'*64,write_receipt=False)
        self.assertFalse((self.root/'active-job.json').exists())
        self.assertTrue((previous/'native-lease-closed.json').exists())
        self.assertEqual(self.transport.post.call_count,1)
        self.assertTrue(self.transport.post.call_args.args[0].endswith('/adaptive-decision'))

    def test_ready_cursor_with_unfinished_job_reconciles_final_delivery_without_native(self):
        request_id='a'*32
        self.transport.request.return_value={'executionPolicy':{},'analysis':{},
            'cursor':{'ordinal':1,'state':'READY_FOR_OWNER_REVIEW'},
            'job':{'jobId':'PIAI_'+request_id,'state':'RUNNING','cancelRequested':False}}
        with patch.object(self.runner,'deliver',return_value='READY_FOR_OWNER_REVIEW') as delivery:
            self.assertEqual(self.runner.advance(request_id),'READY_FOR_OWNER_REVIEW')
        delivery.assert_called_once();self.transport.post.assert_not_called()

    def test_current_segment_one_receipt_recovers_without_previous_lease_confusion(self):
        request_id='a'*32;job_id='PIAI_'+request_id
        session=self.runner.directory/job_id;session.mkdir()
        current=session/'segment-1';current.mkdir()
        binding={'jobId':job_id,'permitSha256':'b'*64,'manifestSha256':'c'*64,'permit':{'ordinal':1}}
        (current/'binding.json').write_bytes(encode(binding))
        (current/'native-done.json').write_bytes(encode({'status':'OWNED_VIEWS_CLOSED','permitSha256':'b'*64}))
        (current/'verification.json').write_bytes(encode({'verification':{'ordinal':1,'outputs':['FIXTURE']}}))
        (self.root/'active-job.json').write_bytes(encode({'jobId':job_id,'permitSha256':'b'*64}))
        self.transport.request.return_value={'executionPolicy':{},'analysis':{},
            'cursor':{'ordinal':1,'state':'AWAITING_EXECUTION'},
            'job':{'jobId':job_id,'state':'RUNNING','cancelRequested':False}}
        with patch.object(self.runner,'run_native',side_effect=AssertionError('No native replay')), \
             patch('tools.pixinsight.local_pilot.adaptive_worker.verify',return_value={'verification':{'ordinal':1,'outputs':['FIXTURE']}}) as physical:
            self.assertEqual(self.runner.advance(request_id),'CHECKPOINT_RECONCILED')
        physical.assert_called_once_with(current,expected_manifest_sha256='c'*64,write_receipt=False)
        self.assertFalse((self.root/'active-job.json').exists())
        self.assertTrue((current/'native-lease-closed.json').exists())
        self.assertEqual(self.transport.post.call_count,1)
        self.assertTrue(self.transport.post.call_args.args[0].endswith('/adaptive-checkpoint'))

    def test_changed_current_checkpoint_keeps_lease_and_cannot_advance_backend(self):
        request_id='a'*32;job_id='PIAI_'+request_id
        session=self.runner.directory/job_id;session.mkdir()
        current=session/'segment-1';current.mkdir()
        binding={'jobId':job_id,'permitSha256':'b'*64,'manifestSha256':'c'*64,'permit':{'ordinal':1}}
        (current/'binding.json').write_bytes(encode(binding))
        (current/'verification.json').write_bytes(encode({'verification':{'ordinal':1}}))
        (self.root/'active-job.json').write_bytes(encode({'jobId':job_id,'permitSha256':'b'*64}))
        self.transport.request.return_value={'executionPolicy':{},'analysis':{},
            'cursor':{'ordinal':1,'state':'AWAITING_EXECUTION'},
            'job':{'jobId':job_id,'state':'RUNNING','cancelRequested':False}}
        with patch('tools.pixinsight.local_pilot.adaptive_worker.verify',side_effect=ValueError('changed physical source/output/runtime/History')):
            with self.assertRaises(ValueError):self.runner.advance(request_id)
        self.transport.post.assert_not_called()
        self.assertTrue((self.root/'active-job.json').exists())


if __name__=='__main__':unittest.main()
