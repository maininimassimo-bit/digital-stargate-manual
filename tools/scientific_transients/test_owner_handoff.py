"""Synthetic application receipts and retained local staging; no native launch."""
import copy
import unittest
from tools.scientific_transients import owner_handoff as module
from tools.scientific_transients import owner_operation_stager as staging
from tools.scientific_transients import test_campaign_triplet as fixtures
from tools.scientific_transients.confirmatory_campaign import fingerprint
from tools.scientific_transients.attempt_journal import write_new
from tools.scientific_transients.campaign_handoff import compare_technical
from tools.pixinsight.local_pilot.broker import ProtocolError

class OwnerHandoffTests(unittest.TestCase):
    def challenge(self,action,selection,request,path):
        value=dict(protocol=staging.CHALLENGE,nonce='a'*32,action=action,planRef=self.proposal['planRef'],
                   proposalSha256=selection,requestSha256=staging.request_sha(request),routeSha256=staging.route_sha(path))
        value['challengeSha256']=fingerprint(value);return value
    def setUp(self):
        self.f=fixtures.TripletTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
        self.triplet=self.f.prepare();self.triplet.register_all(self.f.worker)
        self.stager=staging.OwnerOperationStager(self.triplet);self.proposal=self.stager.proposal
        p=self.proposal;self.base='/v1/transient-analysis/campaigns/'+p['planRef']+'/dispatch-intents'
        self.stager.stage_intent(self.challenge('DISPATCH_INTENT',p['proposalSha256'],p['request'],self.base))
        event=self.f.owner.request(self.base,p['request'])
        self.receipt=dict(protocol=staging.INTENT_RECEIPT,planRef=p['planRef'],intentSha256=event['sha256'],
            contextSha256=p['request']['contextSha256'],archiveSha256=p['request']['archiveSha256'],
            queueNamespaceSha256=event['request']['queueNamespaceSha256'],
            orderedJobSelectionDigests=[fingerprint(j) for j in p['request']['jobs']],
            operationKeySha256=staging.operation_key(p,'DISPATCH_INTENT'),requestSha256=staging.request_sha(p['request']),
            launchAuthorized=False,scientificValidation='NOT_VALIDATED')
        self.receipt['receiptSha256']=fingerprint(self.receipt);self.projections=[];self.technical=[]
        for i in range(3):
            path=self.base+'/'+event['sha256']+'/jobs/'+str(i)+'/project'
            selection=staging.projection_selection_sha(p,self.receipt,i)
            self.stager.stage_projection(self.challenge('PROJECT_JOB',selection,{},path),self.receipt,i)
            self.f.owner.request(path,{})
            technical=self.f.bridge.technical_context(p['planRef'],event['sha256'],i);self.technical.append(technical)
            receipt=dict(protocol='DSG_CAMPAIGN_OWNER_PROJECTION_RECEIPT_V1',planRef=p['planRef'],intentSha256=event['sha256'],
                queueNamespaceSha256=self.receipt['queueNamespaceSha256'],ordinal=i,jobId=technical['jobId'],
                requestSelectionSha256=technical['requestSelectionSha256'],projectionObserved=True,reservationFreshness='NOT_ATTESTED',
                operationKeySha256=staging.operation_key(p,'PROJECT_JOB',self.receipt,i),requestSha256=staging.request_sha({}),
                launchAuthorized=False,scientificValidation='NOT_VALIDATED')
            receipt['receiptSha256']=fingerprint(receipt);self.projections.append(receipt)
    def test_exact_handoff_matches_actual_technical_context_without_transport_or_launch(self):
        calls=list(self.f.calls);handoff=module.build_handoff(self.triplet,self.receipt,self.projections)
        for i,row in enumerate(self.technical):self.assertFalse(compare_technical(handoff,row,i)['launchAuthorized'])
        self.assertEqual(self.f.calls,calls);self.assertEqual(self.f.processes,[])
        self.assertFalse(handoff['launchAuthorized']);self.assertEqual(len(handoff['jobs']),3)
    def test_missing_reordered_or_rehashed_different_namespace_receipts_rejected(self):
        for receipts in (self.projections[:2],list(reversed(self.projections))):
            with self.assertRaises(ProtocolError):module.build_handoff(self.triplet,self.receipt,receipts)
        receipts=copy.deepcopy(self.projections);receipts[0]['queueNamespaceSha256']='f'*64
        receipts[0]['receiptSha256']=fingerprint({k:v for k,v in receipts[0].items() if k!='receiptSha256'})
        with self.assertRaises(ProtocolError):module.build_handoff(self.triplet,self.receipt,receipts)
    def test_uncertain_stage_blocks_handoff_without_removing_evidence(self):
        key=staging.operation_key(self.proposal,'PROJECT_JOB',self.receipt,1)
        marker=self.stager.root/key/'unconfirmed.json';write_new(marker,{'state':'RECONCILIATION_REQUIRED'})
        with self.assertRaises(ProtocolError):module.build_handoff(self.triplet,self.receipt,self.projections)
        self.assertTrue(marker.is_file())
    def test_unknown_fields_or_launch_grant_in_receipt_cannot_be_transferred(self):
        for key,value in [('leaseToken','synthetic'),('launchAuthorized',True),('reservationFreshness','ATTESTED')]:
            receipts=copy.deepcopy(self.projections);receipts[0][key]=value
            receipts[0]['receiptSha256']=fingerprint({k:v for k,v in receipts[0].items() if k!='receiptSha256'})
            with self.assertRaises(ProtocolError):module.build_handoff(self.triplet,self.receipt,receipts)

    def test_export_retained_once_and_registered_package_remains_reopenable(self):
        from tools.scientific_transients.attempt_journal import read_json
        output=self.f.root/'handoff.json'
        handoff=module.export_handoff(self.triplet,self.receipt,self.projections,output)
        self.assertEqual(read_json(output)[0],handoff)
        reopened=fixtures.CampaignTriplet.reopen_registered(self.triplet.directory.parent,self.f.context_path,
            self.f.context_sha,self.f.archive,self.f.plans,self.proposal['request']['decisionId'])
        self.assertEqual(reopened.owner_proposal(),self.proposal)
        with self.assertRaises(FileExistsError):module.export_handoff(self.triplet,self.receipt,self.projections,self.f.root/'second.json')
        self.assertFalse((self.f.root/'second.json').exists());self.assertEqual(self.f.processes,[])

    def test_failed_export_fsync_preserves_lock_and_blocks_reexport(self):
        from unittest.mock import patch
        output=self.f.root/'handoff.json'
        with patch('tools.scientific_transients.attempt_journal.write_new',side_effect=OSError('synthetic fsync failure')):
            with self.assertRaises(ProtocolError):module.export_handoff(self.triplet,self.receipt,self.projections,output)
        folder=self.triplet.directory.parent/'_worker-handoffs-v1'/self.triplet.context['contextSha256']
        self.assertTrue(folder.is_dir());self.assertFalse(output.exists())
        with self.assertRaises(FileExistsError):module.export_handoff(self.triplet,self.receipt,self.projections,output)

    def test_existing_output_is_preserved_and_failed_export_marked_uncertain(self):
        output=self.f.root/'handoff.json';output.write_bytes(b'SYNTHETIC EXISTING OUTPUT')
        with self.assertRaises(ProtocolError):module.export_handoff(self.triplet,self.receipt,self.projections,output)
        self.assertEqual(output.read_bytes(),b'SYNTHETIC EXISTING OUTPUT')
        folder=self.triplet.directory.parent/'_worker-handoffs-v1'/self.triplet.context['contextSha256']
        self.assertTrue((folder/'unconfirmed.json').is_file())

    def test_changed_retained_stage_before_export_prevents_external_output(self):
        from unittest.mock import patch
        original=module.build_handoff;calls=[]
        def changing(*args):
            calls.append(1)
            if len(calls)==2:
                key=staging.operation_key(self.proposal,'PROJECT_JOB',self.receipt,0)
                write_new(self.stager.root/key/'unconfirmed.json',{'state':'RECONCILIATION_REQUIRED'})
            return original(*args)
        output=self.f.root/'handoff.json'
        with patch.object(module,'build_handoff',side_effect=changing):
            with self.assertRaises(ProtocolError):module.export_handoff(self.triplet,self.receipt,self.projections,output)
        self.assertFalse(output.exists())

    def test_numeric_boolean_aliases_cannot_match_canonical_receipts_or_stages(self):
        from tools.pixinsight.local_pilot.broker import encode
        from tools.scientific_transients.attempt_journal import read_json
        receipts=copy.deepcopy(self.projections);receipts[0]['launchAuthorized']=0
        with self.assertRaises(ProtocolError):module.build_handoff(self.triplet,self.receipt,receipts)
        key=staging.operation_key(self.proposal,'PROJECT_JOB',self.receipt,0)
        path=self.stager.root/key/'envelope.json';envelope=read_json(path)[0];envelope['launchAuthorized']=0
        path.write_bytes(encode(envelope))
        with self.assertRaises(ProtocolError):module.build_handoff(self.triplet,self.receipt,self.projections)

    def cli_arguments(self):
        intent=self.f.root/'intent-receipt.json';intent_sha=write_new(intent,self.receipt)
        args=['--config','synthetic-config','--config-sha256','1'*64,'--intent-receipt',str(intent),
              '--intent-receipt-sha256',intent_sha,'--output',str(self.f.root/'exported-handoff.json')]
        for i,receipt in enumerate(self.projections):
            path=self.f.root/('projection-'+str(i)+'.json');sha=write_new(path,receipt)
            args.extend(['--projection-receipt',str(path),sha])
        return args

    def test_cli_exports_without_network_or_native_authority(self):
        import io,json
        from contextlib import redirect_stdout
        from unittest.mock import patch
        args=self.cli_arguments();out=io.StringIO()
        config=(self.triplet.directory.parent,self.f.context_path,self.f.context_sha,self.f.archive,self.f.plans,
                self.proposal['request']['decisionId'])
        with patch('tools.scientific_transients.campaign_worker_cli.load_config',return_value=config),redirect_stdout(out):
            code=module.main(args)
        self.assertEqual(code,0);result=json.loads(out.getvalue())
        self.assertTrue(result['handoffExported']);self.assertFalse(result['nativeLaunchRequested'])
        self.assertFalse(result['networkRequested']);self.assertNotIn(str(self.f.root),out.getvalue())
        self.assertEqual(self.f.processes,[])

    def test_cli_changed_receipt_digest_fails_before_export(self):
        import io
        from contextlib import redirect_stdout
        from unittest.mock import patch
        args=self.cli_arguments();args[args.index('--intent-receipt-sha256')+1]='0'*64
        config=(self.triplet.directory.parent,self.f.context_path,self.f.context_sha,self.f.archive,self.f.plans,
                self.proposal['request']['decisionId'])
        with patch('tools.scientific_transients.campaign_worker_cli.load_config',return_value=config), \
             patch.object(module,'export_handoff',side_effect=AssertionError('should not export')),redirect_stdout(io.StringIO()):
            self.assertEqual(module.main(args),2)
        self.assertFalse((self.f.root/'exported-handoff.json').exists())

    def test_retained_handoff_changed_during_external_write_prevents_completion(self):
        from unittest.mock import patch
        from tools.scientific_transients import attempt_journal
        from tools.pixinsight.local_pilot.broker import encode
        output=self.f.root/'handoff.json'
        folder=self.triplet.directory.parent/'_worker-handoffs-v1'/self.triplet.context['contextSha256']
        original=attempt_journal.write_new
        def changing(path,value):
            sha=original(path,value)
            if path==output:(folder/'handoff.json').write_bytes(encode({'changed':'synthetic counterproof'}))
            return sha
        with patch.object(attempt_journal,'write_new',side_effect=changing):
            with self.assertRaises(ProtocolError):module.export_handoff(self.triplet,self.receipt,self.projections,output)
        self.assertTrue((folder/'unconfirmed.json').is_file());self.assertFalse((folder/'completed.json').exists())

if __name__=='__main__':unittest.main()
