"""Read-only inspections of synthetic local exports; no native/cloud operations."""
import hashlib
import unittest
from pathlib import Path
from unittest.mock import patch
from tools.pixinsight.local_pilot.broker import ProtocolError,encode
from tools.scientific_transients import test_owner_handoff as fixtures
from tools.scientific_transients import test_local_registry as registry_fixtures
from tools.scientific_transients import owner_handoff as exporter
from tools.scientific_transients import owner_handoff_inspection as module
from tools.scientific_transients.attempt_journal import write_new
from tools.scientific_transients.local_registry import LocalRegistry


def snapshot(root):
    return {p.relative_to(root).as_posix():(p.stat().st_mtime_ns,hashlib.sha256(p.read_bytes()).hexdigest())
            for p in root.rglob('*') if p.is_file()}

class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.OwnerHandoffTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
        self.triplet=self.f.triplet;self.output=self.f.f.root/'external-handoff.json'
        exporter.export_handoff(self.triplet,self.f.receipt,self.f.projections,self.output)
        self.folder=self.triplet.directory.parent/'_worker-handoffs-v1'/self.triplet.context['contextSha256']
    def inspect(self,path=None):return module.inspect_export(self.triplet,self.f.receipt,self.f.projections,path or self.output)
    def readonly(self,expected):
        before=snapshot(self.f.f.root);original=Path.open
        def guarded(path,mode='r',*args,**kwargs):
            if any(letter in mode for letter in ('w','a','x','+')):raise AssertionError('inspection attempted a write')
            return original(path,mode,*args,**kwargs)
        with patch.object(Path,'open',new=guarded),patch.object(LocalRegistry,'_write_new',side_effect=AssertionError('verification wrote receipt')):
            result=self.inspect()
        self.assertEqual(result['status'],expected);self.assertEqual(snapshot(self.f.f.root),before)
        self.assertFalse(result['launchAuthorized']);self.assertFalse(result['retryAuthorized']);return result
    def test_constructor_and_all_rechecks_are_read_only_for_consistent_copy(self):
        result=self.readonly('CONSISTENT_RETAINED_COPY');self.assertTrue(result['recordedCompletion'])
        self.assertFalse(result['needsAssistedRecovery']);self.assertNotIn(str(self.f.f.root),str(result))
    def test_consistent_uncertain_copy_keeps_marker_and_does_not_unlock(self):
        write_new(self.folder/'unconfirmed.json',dict(state='RECONCILIATION_REQUIRED',implicitRetry=False,nativeLaunchRequested=False))
        result=self.readonly('CONSISTENT_RETAINED_COPY');self.assertTrue(result['needsAssistedRecovery'])
        self.assertTrue(result['uncertaintyMarkerObserved']);self.assertTrue((self.folder/'unconfirmed.json').exists())
    def test_failed_source_verification_records_no_receipt_or_mutation(self):
        source=self.f.f.plans[0].roots['run']/'input.xisf';source.write_bytes(b'SYNTHETIC CHANGED SOURCE')
        self.readonly('INCOMPLETE_OR_CONFLICT')
    def test_missing_or_internal_external_copy_is_not_confirmed(self):
        self.assertEqual(self.inspect(self.f.f.root/'missing.json')['status'],'INCOMPLETE_OR_CONFLICT')
        self.assertEqual(self.inspect(self.folder/'handoff.json')['status'],'INCOMPLETE_OR_CONFLICT')
        self.assertFalse((self.f.f.root/'missing.json').exists())
    def test_retained_copy_changed_during_inspection_fails_closed(self):
        original=module.read_json
        def changing(path):
            result=original(path)
            if path==self.output:(self.folder/'handoff.json').write_bytes(encode({'changed':'synthetic concurrent writer'}))
            return result
        with patch.object(module,'read_json',side_effect=changing):result=self.inspect()
        self.assertEqual(result['status'],'INCOMPLETE_OR_CONFLICT');self.assertFalse(result['retryAuthorized'])
    def test_unknown_pid_artifact_does_not_establish_process_ownership(self):
        write_new(self.folder/'process.json',{'pid':12345})
        result=self.readonly('INCOMPLETE_OR_CONFLICT');self.assertFalse(result['nativeStoppedAttested'])

    def cli_arguments(self):
        f=self.f.f
        config=dict(protocol='DSG_CAMPAIGN_LOCAL_RUN_CONFIG_V1',contextPath=str(f.context_path),contextFileSha256=f.context_sha,
                    archiveDirectory=str(f.archive.directory),archiveSha256=f.archive.sha,coordinatorRoot=str(f.root/'coordinators'),
                    decisionId=self.f.proposal['request']['decisionId'],operatorPlans=[dict(path=str(p.path),sha256=p.sha) for p in f.plans])
        path=f.root/'inspection-config.json';sha=write_new(path,config)
        intent=f.root/'inspection-intent.json';intent_sha=write_new(intent,self.f.receipt)
        args=['--config',str(path),'--config-sha256',sha,'--intent-receipt',str(intent),
              '--intent-receipt-sha256',intent_sha,'--copy',str(self.output)]
        for ordinal,value in enumerate(self.f.projections):
            path=f.root/('inspection-projection-'+str(ordinal)+'.json');sha=write_new(path,value)
            args.extend(['--projection-receipt',str(path),sha])
        return args

    def test_cli_real_config_constructor_is_read_only_and_output_minimized(self):
        import io,json
        from contextlib import redirect_stdout
        args=self.cli_arguments();before=snapshot(self.f.f.root);out=io.StringIO()
        with patch.object(LocalRegistry,'_write_new',side_effect=AssertionError('CLI verification wrote')),redirect_stdout(out):
            code=module.main(args,engine=self.f.f.natives[0].engine,catalog=self.f.f.natives[0].catalog)
        self.assertEqual(code,0);self.assertEqual(json.loads(out.getvalue())['status'],'CONSISTENT_RETAINED_COPY')
        self.assertEqual(before,snapshot(self.f.f.root));self.assertNotIn(str(self.f.f.root),out.getvalue())

    def test_cli_config_error_does_not_write_verification_or_expose_paths(self):
        import io,json
        from contextlib import redirect_stdout
        args=self.cli_arguments();args[args.index('--config-sha256')+1]='0'*64
        before=snapshot(self.f.f.root);out=io.StringIO()
        with patch.object(LocalRegistry,'_write_new',side_effect=AssertionError('CLI error wrote')),redirect_stdout(out):
            code=module.main(args,engine=self.f.f.natives[0].engine,catalog=self.f.f.natives[0].catalog)
        self.assertEqual(code,2);self.assertEqual(json.loads(out.getvalue())['status'],'INCOMPLETE_OR_CONFLICT')
        self.assertEqual(before,snapshot(self.f.f.root));self.assertNotIn(str(self.f.f.root),out.getvalue())

class RegistryInspectionTests(unittest.TestCase):
    def setUp(self):
        self.f=registry_fixtures.RegistryTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
        self.registration=self.f.register()
    def test_default_verification_still_records_while_pure_path_does_not(self):
        count=len(self.f.receipts());local=LocalRegistry(self.f.artifacts,self.f.registry,record_verifications=False)
        with patch.object(LocalRegistry,'_write_new',side_effect=AssertionError('read path wrote')):
            self.assertEqual(local.verify(self.f.binding['bindingRef'],self.registration['manifestSha256']),self.f.manifest)
            self.assertEqual(local.inspect(self.f.binding['bindingRef'],self.registration['manifestSha256']),self.f.manifest)
        self.assertEqual(len(self.f.receipts()),count)
        self.f.local.verify(self.f.binding['bindingRef'],self.registration['manifestSha256'])
        self.assertEqual(len(self.f.receipts()),count+1)
    def test_false_verification_policy_does_not_make_registration_read_only(self):
        count=len(self.f.receipts());local=LocalRegistry(self.f.artifacts,self.f.registry,record_verifications=False)
        local.register(encode(self.f.manifest));self.assertEqual(len(self.f.receipts()),count+1)
    def test_policy_requires_boolean(self):
        for value in (0,1,None,'false'):
            with self.assertRaises(ProtocolError):LocalRegistry(self.f.artifacts,self.f.registry,record_verifications=value)

if __name__=='__main__':unittest.main()
