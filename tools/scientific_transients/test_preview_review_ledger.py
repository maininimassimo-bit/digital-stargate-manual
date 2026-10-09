"""Offline frozen-preview history checks; all measurements and decisions are synthetic."""
import copy
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.scientific_transients import preview_review_ledger as ledger
from tools.pixinsight.local_pilot.broker import ProtocolError, encode, decode
from tools.scientific_transients import test_channel_review as review_cases
from tools.scientific_transients import test_cbat_preview as cbat_cases
from tools.scientific_transients import test_mpc_export as mpc_cases
from tools.scientific_transients import channel_review, cbat_preview, mpc_export
from tools.scientific_transients.local_registry import fingerprint


class PreviewLedgerTests(unittest.TestCase):
    def setUp(self):
        self.case=review_cases.ChannelReviewTests();self.case.setUp();self.addCleanup(self.case.doCleanups)
        self.source=self.case.export();self.root=self.case.root/'ledger-root';self.root.mkdir()
        self.receipt_sha=fingerprint(self.source/'export.json')['sha256']
        self.event={'eventRef':'1'*32,'actorRef':'2'*32,'recordedUTC':'2026-10-09T00:00:00Z',
                    'action':'KEEP_FOR_REVIEW','targetEventRef':None,'note':'Synthetic private review only'}

    def prepare(self):return ledger.PreviewReviewLedger.prepare(self.source,self.receipt_sha,'TNS',self.root,'f'*32)

    def test_all_four_actual_exporters_can_be_frozen_without_network(self):
        cases=[]
        for channel,kind,module in [('TNS',review_cases.ChannelReviewTests,channel_review),('VSX',review_cases.ChannelReviewTests,channel_review),
                                    ('CBAT',cbat_cases.CBATPreviewTests,cbat_preview),('MPC',mpc_cases.MPCExportTests,mpc_export)]:
            case=kind();case.setUp();self.addCleanup(case.doCleanups)
            if channel=='VSX':case.vsx()
            source=case.export();root=case.root/'ledger-root';root.mkdir()
            with patch('socket.socket',side_effect=AssertionError('network forbidden')):
                history=ledger.PreviewReviewLedger.prepare(source,fingerprint(source/'export.json')['sha256'],channel,root,'f'*32)
                result=history.inspect(history.anchor_sha)
            self.assertEqual(result['anchor']['preview']['channel'],channel)
            self.assertFalse(result['submissionAuthorized']);self.assertFalse(result['actorIdentityAttested'])
            self.assertEqual(result['events'],[])
            if channel=='MPC':self.assertIsNone(result['anchor']['preview']['candidateRef'])

    def test_restart_chain_head_pinning_and_append(self):
        history=self.prepare();result=history.append(self.event,history.anchor_sha)
        reopened=ledger.PreviewReviewLedger(history.directory,history.anchor_sha)
        value=reopened.inspect(result['headSha256'])
        self.assertEqual(value['events'][0]['decision'],self.event)
        self.assertFalse(value['scientificAcceptance']);self.assertEqual(value['externalSubmission'],'NONE')
        with self.assertRaises(ProtocolError):reopened.inspect(history.anchor_sha)

    def test_revocation_keeps_original_and_has_no_submission_effect(self):
        history=self.prepare();first=history.append(self.event,history.anchor_sha)
        before=fingerprint(history.directory/'events/0000.json')
        revoke={**self.event,'eventRef':'3'*32,'recordedUTC':'2026-10-09T00:00:01Z',
                'action':'REVOKE_REVIEW','targetEventRef':self.event['eventRef']}
        result=history.append(revoke,first['headSha256'])
        self.assertEqual(result['revokedEventRefs'],[self.event['eventRef']])
        self.assertEqual(fingerprint(history.directory/'events/0000.json'),before)
        self.assertEqual(len(result['events']),2);self.assertFalse(result['submissionAuthorized'])

    def test_same_event_current_head_is_idempotent_without_rewrite(self):
        history=self.prepare();first=history.append(self.event,history.anchor_sha)
        before=fingerprint(history.directory/'events/0000.json')
        self.assertEqual(history.append(self.event,first['headSha256']),first)
        self.assertEqual(fingerprint(history.directory/'events/0000.json'),before)
        with self.assertRaises(ProtocolError):history.append({**self.event,'note':'changed'},first['headSha256'])

    def test_future_or_already_revoked_target_rejected(self):
        history=self.prepare();first=history.append(self.event,history.anchor_sha)
        revoke={**self.event,'eventRef':'3'*32,'action':'REVOKE_REVIEW','targetEventRef':'4'*32}
        with self.assertRaises(ProtocolError):history.append(revoke,first['headSha256'])
        revoke['targetEventRef']=self.event['eventRef'];second=history.append(revoke,first['headSha256'])
        with self.assertRaises(ProtocolError):history.append({**revoke,'eventRef':'5'*32},second['headSha256'])

    def test_unsupported_authority_and_hidden_text_rejected(self):
        history=self.prepare()
        for update in [{'action':'AUTHORIZE_SUBMISSION'},{'submissionAuthorized':True},
                       {'note':'x\nsecond'},{'note':'x\u202e'},{'targetEventRef':'3'*32},
                       {'recordedUTC':'2026-02-30T00:00:00Z'},{'actorRef':'name'}]:
            with self.subTest(update=update),self.assertRaises(ProtocolError):history.append({**self.event,**update},history.anchor_sha)
        self.assertEqual(list((history.directory/'events').iterdir()),[])

    def test_backdated_event_rejected_before_write(self):
        history=self.prepare();first=history.append(self.event,history.anchor_sha)
        with self.assertRaises(ProtocolError):history.append({**self.event,'eventRef':'3'*32,'recordedUTC':'2026-10-08T23:59:59Z'},first['headSha256'])
        self.assertEqual(len(list((history.directory/'events').iterdir())),1)

    def test_snapshot_remains_readable_when_original_preview_removed(self):
        history=self.prepare()
        (self.source/'worksheet.txt').write_bytes(b'original changed after snapshot')
        value=history.inspect(history.anchor_sha)
        self.assertFalse(value['anchor']['completeDependencyArchive'])
        self.assertEqual(value['anchor']['preview']['receiptSha256'],self.receipt_sha)

    def test_source_hash_partial_extra_and_wrong_channel_rejected(self):
        with self.assertRaises(ProtocolError):ledger.PreviewReviewLedger.prepare(self.source,'0'*64,'TNS',self.root,'f'*32)
        with self.assertRaises(ProtocolError):ledger.PreviewReviewLedger.prepare(self.source,self.receipt_sha,'VSX',self.root,'f'*32)
        (self.source/'failed.json').write_bytes(b'{}')
        with self.assertRaises(ProtocolError):self.prepare()
        self.assertEqual(list(self.root.iterdir()),[])

    def test_copy_failure_preserved_and_no_retry_overwrite(self):
        with patch.object(ledger,'copy_verified',side_effect=OSError('synthetic disk failure')),self.assertRaises(OSError):self.prepare()
        directory=self.root/('f'*32)
        self.assertTrue((directory/'failed.json').is_file());self.assertFalse((directory/'ledger.json').exists())
        with self.assertRaises(FileExistsError):self.prepare()

    def test_second_source_check_catches_change_and_preserves_copies(self):
        original=ledger.inspect_preview;calls=[]
        def altered(*args):
            calls.append(1)
            if len(calls)==2:(self.source/'worksheet.txt').write_bytes(b'changed')
            return original(*args)
        with patch.object(ledger,'inspect_preview',side_effect=altered),self.assertRaises(ProtocolError):self.prepare()
        directory=self.root/('f'*32)
        self.assertTrue((directory/'failed.json').is_file());self.assertTrue((directory/'snapshot/worksheet.txt').exists())

    def test_snapshot_tamper_and_anchor_tamper_detected(self):
        history=self.prepare();anchor=(history.directory/'ledger.json').read_bytes()
        (history.directory/'ledger.json').write_bytes(anchor+b' ')
        with self.assertRaises(ProtocolError):history.inspect(history.anchor_sha)
        (history.directory/'ledger.json').write_bytes(anchor)
        (history.directory/'snapshot/worksheet.txt').write_bytes(b'changed')
        with self.assertRaises(ProtocolError):history.inspect(history.anchor_sha)

    def test_event_tamper_chain_rewrite_and_rollback_detected(self):
        history=self.prepare();first=history.append(self.event,history.anchor_sha);path=history.directory/'events/0000.json'
        event=decode(path.read_bytes());event['decision']['note']='rewritten';path.write_bytes(encode(event))
        with self.assertRaises(ProtocolError):history.inspect(first['headSha256'])
        path.unlink()  # Test-only synthetic removal proves rollback detection.
        with self.assertRaises(ProtocolError):history.inspect(first['headSha256'])

    def test_sequence_gap_extra_and_partial_record_block_reconciliation(self):
        history=self.prepare();path=history.directory/'events/0001.json';path.write_bytes(b'{')
        with self.assertRaises(ProtocolError):history.inspect(history.anchor_sha)
        path.rename(history.directory/'events/0000.json')
        with self.assertRaises(ProtocolError):history.inspect(history.anchor_sha)
        with self.assertRaises(ProtocolError):history.append(self.event,history.anchor_sha)

    def test_concurrent_same_sequence_is_exclusive_and_requires_reconciliation(self):
        history=self.prepare();original=ledger.write_new;competing={**self.event,'eventRef':'3'*32}
        second=ledger.PreviewReviewLedger(history.directory,history.anchor_sha);trigger=[]
        def interleave(path,event):
            if path.parent.name=='events' and not trigger:
                trigger.append(1);second.append(competing,history.anchor_sha)
            return original(path,event)
        with patch.object(ledger,'write_new',side_effect=interleave),self.assertRaises(FileExistsError):history.append(self.event,history.anchor_sha)
        head=fingerprint(history.directory/'events/0000.json')['sha256']
        self.assertEqual(history.inspect(head)['events'][0]['decision'],competing)

    def test_final_read_failure_does_not_rewrite_or_report_success(self):
        history=self.prepare();original=history.inspect;calls=[]
        def lost(*args):
            calls.append(1)
            if len(calls)==2:raise OSError('synthetic read failure after durable record')
            return original(*args)
        with patch.object(history,'inspect',side_effect=lost),self.assertRaises(OSError):history.append(self.event,history.anchor_sha)
        path=history.directory/'events/0000.json';head=fingerprint(path)['sha256']
        self.assertEqual(history.inspect(head)['events'][0]['decision'],self.event)

    def test_event_limit_and_root_overlap_fail_conservatively(self):
        history=self.prepare();first=history.append(self.event,history.anchor_sha)
        with patch.object(ledger,'MAX_EVENTS',1),self.assertRaises(ProtocolError):history.append({**self.event,'eventRef':'3'*32},first['headSha256'])
        for root in (self.source,self.case.root,self.source/'nested'):
            if root.name=='nested':root.mkdir()
            with self.assertRaises(ProtocolError):ledger.PreviewReviewLedger.prepare(self.source,self.receipt_sha,'TNS',root,'a'*32)

    def test_new_preview_revision_cannot_reuse_old_private_review(self):
        history=self.prepare();first=history.append(self.event,history.anchor_sha)
        matched=history.verify_current_preview(self.source,self.receipt_sha,first['headSha256'])
        self.assertEqual(matched['state'],'FROZEN_PREVIEW_BYTES_MATCH');self.assertFalse(matched['submissionAuthorized'])
        self.case.request['reviewRef']='c'*32;self.case.request['reporterDeclared']='Another synthetic reporter'
        new_source=self.case.export();new_sha=fingerprint(new_source/'export.json')['sha256']
        with self.assertRaises(ProtocolError):history.verify_current_preview(new_source,new_sha,first['headSha256'])
        self.assertEqual(len(history.inspect(first['headSha256'])['events']),1)

    def test_history_export_records_revocation_and_blocks_overwrite_or_overlap(self):
        history=self.prepare();first=history.append(self.event,history.anchor_sha)
        revoke={**self.event,'eventRef':'3'*32,'action':'REVOKE_REVIEW','targetEventRef':self.event['eventRef']}
        value=history.append(revoke,first['headSha256']);root=self.case.root/'history-exports';root.mkdir()
        directory=history.export_history(value['headSha256'],root,'a'*32)
        txt=(directory/'history.txt').read_text(encoding='utf-8')
        self.assertIn('Review revoked: YES',txt);self.assertIn('NO SUBMISSION AUTHORITY',txt)
        receipt=decode((directory/'export.json').read_bytes())
        for name,record in receipt['files'].items():self.assertEqual(fingerprint(directory/name),record)
        with self.assertRaises(FileExistsError):history.export_history(value['headSha256'],root,'a'*32)
        with self.assertRaises(ProtocolError):history.export_history(value['headSha256'],history.directory,'b'*32)

    def test_history_export_fails_conservatively_if_head_changes_mid_export(self):
        history=self.prepare();root=self.case.root/'history-exports';root.mkdir();original=history.inspect;calls=[]
        def interrupted(head):
            calls.append(1)
            if len(calls)==2:raise ProtocolError('LEDGER_CHANGED_DURING_EXPORT')
            return original(head)
        with patch.object(history,'inspect',side_effect=interrupted),self.assertRaises(ProtocolError):history.export_history(history.anchor_sha,root,'a'*32)
        directory=root/('a'*32)
        self.assertTrue((directory/'history.json').exists());self.assertTrue((directory/'failed.json').exists())
        self.assertFalse((directory/'export.json').exists())


if __name__=='__main__':unittest.main(verbosity=2)
