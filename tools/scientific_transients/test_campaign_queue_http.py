"""Synthetic HTTP authority tests; no cloud or native process."""
import hashlib
import threading
import unittest
from http.server import HTTPServer

from tools.pixinsight.local_pilot.broker import Broker, ProtocolError
from tools.pixinsight.local_pilot.transport_http import handler_for, AuthError
from tools.scientific_transients import test_campaign_queue as queue_fixtures
from tools.scientific_transients import test_confirmatory_http as http_fixtures
from tools.scientific_transients.reservation_intent import JOB_FIELDS

TOKEN, LEGACY_TOKEN = http_fixtures.TOKEN, http_fixtures.LEGACY_TOKEN
BASE, WORKER = http_fixtures.BASE, http_fixtures.WORKER


class ProtectedCampaignHttpTests(unittest.TestCase):
    request = http_fixtures.CampaignHttpTests.request
    close = http_fixtures.CampaignHttpTests.close

    def setUp(self):
        self.f = queue_fixtures.CampaignQueueTests(); self.f.setUp()
        self.ref = self.f.fixture.f.request['planRef']
        self.intent = self.f.intent['sha256']
        def owner(token):
            if token != 'synthetic-owner': raise AuthError()
        self.owner = owner
        self.server = HTTPServer(('127.0.0.1', 0), self.handler())
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start(); self.addCleanup(self.close)

    def handler(self, enabled=True, **overrides):
        values = dict(transient=self.f.q, campaigns=self.f.s,
                      transient_worker_digest=hashlib.sha256(TOKEN.encode()).hexdigest(),
                      campaign_queue=self.f.bridge if enabled else None)
        values.update(overrides)
        return handler_for(Broker(self.f.f.store, 'a'*32), self.owner, 'https://portal.invalid',
                           hashlib.sha256(LEGACY_TOKEN.encode()).hexdigest(), **values)

    def path(self, worker=False, suffix='receipt'):
        return (WORKER if worker else BASE)+'/'+self.ref+'/dispatch-intents/'+self.intent+'/'+suffix

    def body(self):
        return dict(protocol='DSG_CAMPAIGN_RESERVATION_V1', decisionId='e'*32,
                    reservation=self.f.request)

    def test_fresh_envelope_exact_admission_and_repeat_has_no_lease(self):
        path=self.path(True, 'jobs/0/reserve-once')
        code, result=self.request(path, self.body(), TOKEN)
        self.assertEqual(code, 200)
        self.assertEqual(set(result), {'protocol','disposition','admissionSha256','job'})
        self.assertEqual(set(result['job']), JOB_FIELDS)
        self.assertEqual(result['admissionSha256'], self.f.receipt()['admissions'][0]['sha256'])
        code, repeated=self.request(path, self.body(), TOKEN)
        self.assertEqual(code, 200)
        self.assertEqual(repeated, dict(protocol='DSG_CAMPAIGN_RESERVATION_V1',
            disposition='RECONCILIATION_REQUIRED', admissionSha256=None, job=None))

    def test_roles_and_receipt_never_disclose_lease(self):
        path=self.path(True, 'jobs/0/reserve-once')
        self.assertEqual(self.request(path,self.body(),'synthetic-owner',True)[0],403)
        self.assertEqual(self.request(self.path(),token=TOKEN)[0],403)
        _, result=self.request(path,self.body(),TOKEN)
        code, receipt=self.request(self.path(),token='synthetic-owner',owner=True)
        self.assertEqual(code,200)
        self.assertFalse(receipt['launchAuthorized'])
        self.assertNotIn(result['job']['leaseToken'],str(receipt))

    def test_invalid_envelope_and_ordinal_cannot_admit(self):
        for body in ({}, dict(self.body(),queueNamespaceSha256='a'*64),
                     dict(self.body(),protocol='unknown')):
            self.assertEqual(self.request(self.path(True,'jobs/0/reserve-once'),body,TOKEN)[0],400)
        self.assertEqual(self.request(self.path(True,'jobs/3/reserve-once'),self.body(),TOKEN)[0],404)
        self.assertEqual(self.f.receipt()['admissions'],[])

    def test_disabled_composition_and_wrong_identity(self):
        self.server.RequestHandlerClass=self.handler(False)
        self.assertEqual(self.request(self.path(),token='synthetic-owner',owner=True)[0],404)
        self.assertEqual(self.request(self.path(True,'jobs/0/reserve-once'),self.body(),TOKEN)[0],404)
        self.assertEqual(self.f.receipt()['admissions'],[])
        with self.assertRaisesRegex(ProtocolError,'CAMPAIGN_QUEUE_HTTP_COMPOSITION'):
            self.handler(campaigns=None)

    def test_owner_project_and_no_worker_alias(self):
        path=self.path(False,'jobs/0/project')
        self.assertEqual(self.request(path,{},TOKEN)[0],403)
        self.assertEqual(self.request(path,{'extra':True},'synthetic-owner',True)[0],400)
        code, job=self.request(path,{},'synthetic-owner',True)
        self.assertEqual(code,200);self.assertEqual(job,self.f.job)
        self.assertEqual(self.request(self.path(True,'jobs/0/project'),{},TOKEN)[0],404)

    def test_owner_unreserved_cleanup_over_http_is_separate_from_cancel(self):
        self.f.s.admit_frame(self.ref,self.f.fixture.admission_request(),queue_guard=self.f.bridge._guard)
        context_path=self.path(False,'jobs/0/unreserved-context')
        self.assertEqual(self.request(context_path,token='synthetic-owner',owner=True)[0],400)
        self.assertEqual(self.request('/v1/transient-analysis/jobs/'+self.f.job['jobId']+'/cancel',
                                      {},'synthetic-owner',True)[0],200)
        code, context=self.request(context_path,token='synthetic-owner',owner=True)
        self.assertEqual(code,200)
        body={key:context[key] for key in ('admissionSha256','jobId','fenceSnapshotSha256')}
        body.update(decisionId='d'*32,cancellationEvidenceSha256='d'*64)
        code, closure=self.request(self.path(False,'jobs/0/close-unreserved'),body,'synthetic-owner',True)
        self.assertEqual(code,200)
        self.assertEqual(closure['facts']['status'],'NOT_STARTED_FENCED')
        self.assertEqual(self.f.s.view(self.ref)['qualifiedControls'],0)

    def test_owner_intent_rejects_namespace_from_client(self):
        body=dict(self.f.owner,queueNamespaceSha256='d'*64)
        path=BASE+'/'+self.ref+'/dispatch-intents'
        self.assertEqual(self.request(path,body,'synthetic-owner',True)[0],400)
        code, repeated=self.request(path,self.f.owner,'synthetic-owner',True)
        self.assertEqual(code,200);self.assertEqual(repeated,self.f.intent)

    def test_worker_closure_receipt_omits_owner_recovery_declaration(self):
        _, reserved=self.request(self.path(True,'jobs/0/reserve-once'),self.body(),TOKEN)
        job=reserved['job']
        self.f.q.report(job['jobId'],dict(attemptId=job['attemptId'],leaseToken=job['leaseToken'],
                                        sequence=1,stage='RECOVERY_REQUIRED',result=None))
        owner_recovery=dict(decisionId='c'*32,attemptId=job['attemptId'],rootId=job['rootId'],
            bindingRef=job['binding']['bindingRef'],evidenceSha256='f'*64,quiescenceConfirmed=True)
        self.f.q.close_recovery(job['jobId'],owner_recovery)
        body=dict(decisionId='b'*32,admissionSha256=reserved['admissionSha256'],jobId=job['jobId'],
            attemptId=job['attemptId'],reportSha256=None,nativeStopEvidenceSha256='f'*64,
            technicalState='RECOVERY_REQUIRED',processStoppedReported=True)
        path=WORKER+'/'+self.ref+'/frame-closures'
        self.assertEqual(self.request(path,body,'synthetic-owner',True)[0],403)
        code, receipt=self.request(path,body,TOKEN)
        self.assertEqual(code,200)
        self.assertEqual(set(receipt),{'protocol','closureSha256','admissionSha256','status',
                                      'nativeStoppedAttested','scientificValidation'})
        self.assertEqual(receipt['status'],'RECOVERY_REQUIRED')
        self.assertFalse(receipt['nativeStoppedAttested'])
        self.assertNotIn(owner_recovery['decisionId'],str(receipt))
        self.assertNotIn(owner_recovery['evidenceSha256'],str(receipt))
        self.assertNotIn(job['leaseToken'],str(receipt))
        closure=self.f.receipt()['closures'][0]
        self.assertEqual(closure['sha256'],receipt['closureSha256'])
        self.assertEqual(closure['facts']['ownerRecoveryClosure']['request']['decisionId'],owner_recovery['decisionId'])


if __name__ == '__main__': unittest.main()
