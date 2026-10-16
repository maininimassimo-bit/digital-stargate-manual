"""Offline synthetic Owner staging; never launches processes or sends HTTP."""
import copy
import unittest
from unittest.mock import patch
from tools.scientific_transients import owner_operation_stager as m
from tools.scientific_transients import test_campaign_triplet as fixtures
from tools.scientific_transients.confirmatory_campaign import fingerprint
from tools.scientific_transients.attempt_journal import read_json

class OwnerStagerTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.TripletTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
        self.triplet=self.f.prepare();self.triplet.register_all(self.f.worker)
        self.stager=m.OwnerOperationStager(self.triplet)
        self.proposal=self.stager.proposal
        self.path='/v1/transient-analysis/campaigns/'+self.proposal['planRef']+'/dispatch-intents'
        self.calls=list(self.f.calls)
    def challenge(self,nonce='a'*32):
        value=dict(protocol=m.CHALLENGE,nonce=nonce,action='DISPATCH_INTENT',planRef=self.proposal['planRef'],
                   proposalSha256=self.proposal['proposalSha256'],requestSha256=m.request_sha(self.proposal['request']),
                   routeSha256=m.route_sha(self.path))
        value['challengeSha256']=fingerprint(value);return value
    def test_retained_exact_envelope_without_transport_or_launch(self):
        envelope=self.stager.stage_intent(self.challenge())
        folder=self.stager.root/envelope['operationKeySha256']
        self.assertEqual(read_json(folder/'envelope.json')[0],envelope)
        self.assertEqual(read_json(folder/'intent.json')[0]['envelopeSha256'],envelope['envelopeSha256'])
        self.assertFalse(envelope['launchAuthorized']);self.assertEqual(self.f.calls,self.calls)
        self.assertEqual(self.f.processes,[])
    def test_new_nonce_cannot_repeat_semantic_operation(self):
        self.stager.stage_intent(self.challenge())
        with self.assertRaises(FileExistsError):self.stager.stage_intent(self.challenge('b'*32))
    def test_decision_identifier_cannot_change_semantic_key(self):
        changed=copy.deepcopy(self.proposal);changed['request']['decisionId']='c'*32
        self.assertEqual(m.operation_key(changed,'DISPATCH_INTENT'),m.operation_key(self.proposal,'DISPATCH_INTENT'))
    def test_wrong_route_fails_before_lock(self):
        challenge=self.challenge();challenge['routeSha256']='f'*64
        challenge['challengeSha256']=fingerprint({k:v for k,v in challenge.items() if k!='challengeSha256'})
        with self.assertRaises(m.ProtocolError):self.stager.stage_intent(challenge)
        self.assertEqual(list(self.stager.root.iterdir()),[])
    def test_failed_durable_write_preserves_lock_and_forbids_replay(self):
        with patch.object(m,'write_new',side_effect=OSError('synthetic disk failure')):
            with self.assertRaises(m.ProtocolError):self.stager.stage_intent(self.challenge())
        self.assertTrue((self.stager.root/m.operation_key(self.proposal,'DISPATCH_INTENT')).is_dir())
        with self.assertRaises(FileExistsError):self.stager.stage_intent(self.challenge('b'*32))
    def test_failed_readback_preserves_uncertain_marker(self):
        with patch.object(m,'read_json',side_effect=OSError('synthetic read failure')):
            with self.assertRaises(m.ProtocolError):self.stager.stage_intent(self.challenge())
        folder=self.stager.root/m.operation_key(self.proposal,'DISPATCH_INTENT')
        self.assertEqual(read_json(folder/'unconfirmed.json')[0]['state'],'RECONCILIATION_REQUIRED')
        with self.assertRaises(FileExistsError):self.stager.stage_intent(self.challenge())

    def projection(self,ordinal=0):
        receipt=dict(protocol=m.INTENT_RECEIPT,planRef=self.proposal['planRef'],intentSha256='d'*64,
                     contextSha256=self.proposal['request']['contextSha256'],archiveSha256=self.proposal['request']['archiveSha256'],
                     queueNamespaceSha256='e'*64,orderedJobSelectionDigests=[fingerprint(j) for j in self.proposal['request']['jobs']],
                     operationKeySha256=m.operation_key(self.proposal,'DISPATCH_INTENT'),
                     requestSha256=m.request_sha(self.proposal['request']),launchAuthorized=False,scientificValidation='NOT_VALIDATED')
        receipt['receiptSha256']=fingerprint(receipt)
        path=self.path+'/'+receipt['intentSha256']+'/jobs/'+str(ordinal)+'/project'
        challenge=dict(protocol=m.CHALLENGE,nonce='b'*32,action='PROJECT_JOB',planRef=self.proposal['planRef'],
                       proposalSha256=m.projection_selection_sha(self.proposal,receipt,ordinal),
                       requestSha256=m.request_sha({}),routeSha256=m.route_sha(path))
        challenge['challengeSha256']=fingerprint(challenge)
        return challenge,receipt
    def test_projection_requires_retained_intent(self):
        challenge,receipt=self.projection()
        with self.assertRaises(FileNotFoundError):self.stager.stage_projection(challenge,receipt,0)
    def test_projection_is_separately_locked_without_launch(self):
        self.stager.stage_intent(self.challenge());challenge,receipt=self.projection()
        envelope=self.stager.stage_projection(challenge,receipt,0)
        self.assertEqual(envelope['request'],{});self.assertFalse(envelope['launchAuthorized'])
        with self.assertRaises(FileExistsError):self.stager.stage_projection(challenge,receipt,0)
        self.assertEqual(self.f.calls,self.calls)
    def test_uncertain_prior_intent_blocks_projection(self):
        from tools.scientific_transients.attempt_journal import write_new
        envelope=self.stager.stage_intent(self.challenge())
        write_new(self.stager.root/envelope['operationKeySha256']/'unconfirmed.json',{'state':'RECONCILIATION_REQUIRED'})
        challenge,receipt=self.projection()
        with self.assertRaises(m.ProtocolError):self.stager.stage_projection(challenge,receipt,0)
    def test_rehashed_wrong_prior_route_blocks_projection(self):
        from tools.pixinsight.local_pilot.broker import encode
        envelope=self.stager.stage_intent(self.challenge())
        folder=self.stager.root/envelope['operationKeySha256']
        envelope['relativePath']='/wrong'
        envelope['envelopeSha256']=fingerprint({k:v for k,v in envelope.items() if k!='envelopeSha256'})
        (folder/'envelope.json').write_bytes(encode(envelope))
        intent=read_json(folder/'intent.json')[0];intent['envelopeSha256']=envelope['envelopeSha256']
        (folder/'intent.json').write_bytes(encode(intent))
        challenge,receipt=self.projection()
        with self.assertRaises(m.ProtocolError):self.stager.stage_projection(challenge,receipt,0)

if __name__=='__main__':unittest.main()
