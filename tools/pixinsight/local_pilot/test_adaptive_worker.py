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


if __name__=='__main__':unittest.main()
