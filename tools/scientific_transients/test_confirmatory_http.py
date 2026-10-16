"""Real loopback HTTP with synthetic identities/data; no cloud, native run or scientific acceptance."""
import copy
import hashlib
import threading
import unittest
import urllib.request
import urllib.error
from http.server import HTTPServer

from tools.pixinsight.local_pilot.broker import Broker, encode, decode, ProtocolError
from tools.pixinsight.local_pilot.transport_http import handler_for, AuthError
from tools.scientific_transients.queue import TransientQueue, CAMPAIGN_PROFILE
from tools.scientific_transients.campaign_queue import CampaignQueue
from tools.scientific_transients import test_confirmatory_campaign as fixtures
ref,sha=fixtures.ref,fixtures.sha

TOKEN='b'*64
LEGACY_TOKEN='c'*64
BASE='/v1/transient-analysis/campaigns'
WORKER='/v1/transient-analysis/worker/campaigns'


class CampaignHttpTests(unittest.TestCase):
    def setUp(self):
        self.fixture=fixtures.CampaignTests();self.fixture.setUp();f=self.fixture
        self.queue=TransientQueue(f.store,ref(2),lambda:f.now,state_ref=ref(93),capacity_profile=CAMPAIGN_PROFILE)
        f.service.job_reader=self.queue.status
        def owner(token):
            if token!='synthetic-owner':raise AuthError()
        self.owner=owner
        self.server=HTTPServer(('127.0.0.1',0),self.handler())
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.addCleanup(self.close)

    def handler(self,enabled=True):
        return handler_for(Broker(self.fixture.store,ref(90)),self.owner,'https://portal.invalid',
               hashlib.sha256(LEGACY_TOKEN.encode()).hexdigest(),transient=self.queue,
               transient_worker_digest=hashlib.sha256(TOKEN.encode()).hexdigest(),
               campaigns=self.fixture.service if enabled else None)

    def close(self):
        self.server.shutdown();self.server.server_close();self.thread.join()

    def request(self,path,body=None,token=None,owner=False):
        headers={'Content-Type':'application/json'}
        if token:headers['Authorization']='Bearer '+token
        if owner:headers['Origin']='https://portal.invalid'
        request=urllib.request.Request('http://127.0.0.1:'+str(self.server.server_port)+path,
                    None if body is None else encode(body),headers)
        try:
            with urllib.request.urlopen(request,timeout=5) as response:return response.status,decode(response.read())
        except urllib.error.HTTPError as error:
            with error:return error.code,decode(error.read())

    def test_owner_worker_and_legacy_credentials_cannot_cross_campaign_roles(self):
        for token,origin in [(None,False),(TOKEN,False),('not-owner',True),(LEGACY_TOKEN,False)]:
            self.assertEqual(self.request(BASE,token=token,owner=origin)[0],403)
        code,_=self.request(BASE,token='synthetic-owner',owner=True);self.assertEqual(code,200)
        self.assertEqual(self.request(WORKER+'/inputs',self.fixture.inputs[0],'synthetic-owner',True)[0],403)
        self.assertEqual(self.request(BASE,self.fixture.request,TOKEN)[0],403)
        self.assertEqual(self.request(WORKER+'/'+ref(10)+'/freeze',{},TOKEN)[0],404)
        self.assertEqual(self.request(BASE+'/inputs/'+ref(100)+'/review',{},TOKEN)[0],403)

    def test_input_registration_read_and_owner_review_need_separate_roles(self):
        f=self.fixture;r=copy.deepcopy(f.inputs[0]);r['witnessRef']=ref(40000)
        code,row=self.request(WORKER+'/inputs',r,TOKEN);self.assertEqual(code,200)
        self.assertNotIn('review',row);self.assertEqual(row['evidenceOrigin'],'AUTHENTICATED_WORKER_REPORTED_NOT_ATTESTED')
        code,view=self.request(BASE+'/inputs/'+ref(40000),token='synthetic-owner',owner=True)
        self.assertEqual(code,200);self.assertEqual(view['sha256'],row['sha256'])
        f.review(0);review=f.service.input_view(ref(100))['review']['request']
        review=copy.deepcopy(review);review['witnessSha256']=row['sha256'];review['decisionId']=ref(40001)
        code,result=self.request(BASE+'/inputs/'+ref(40000)+'/review',review,'synthetic-owner',True)
        self.assertEqual(code,200);self.assertEqual(result['actorRef'],ref(3))
        self.assertNotIn('review',self.request(WORKER+'/inputs',r,TOKEN)[1])
        self.assertEqual(self.request(BASE+'/inputs/'+ref(40000)+'/review',review,TOKEN)[0],403)

    def test_server_side_job_binding_and_outcome_review_over_http(self):
        f=self.fixture;f.freeze();r=f.execution(0)
        for j,item in enumerate(r['jobs']):
            binding={'bindingRef':ref(16000+j),'inputRef':item['frameRef'],'referenceRef':ref(50000),
                     'algorithmRef':ref(20),'contractRef':ref(30)}
            self.queue.register(binding);self.queue.create({'requestId':item['jobId'][4:],'bindingRef':binding['bindingRef']})
            job=self.queue.claim({'workerId':ref(2),'rootId':ref(92)})['job'];item['attemptId']=job['attemptId']
            update={'attemptId':job['attemptId'],'leaseToken':job['leaseToken'],'sequence':1,'stage':'RUNNING','result':None}
            self.queue.report(job['jobId'],update)
            update.update(sequence=2,stage='COMPLETED',result={'reportSha256':item['reportSha256'],
                          'bindingRef':binding['bindingRef'],'qualityCounts':{'measured':1,'excluded':0,'incomplete':0}})
            self.queue.report(job['jobId'],update)
        code,record=self.request(WORKER+'/'+ref(10)+'/executions',r,TOKEN)
        self.assertEqual(code,200);self.assertTrue(record['technicalCompleted'])
        self.assertEqual(self.request(WORKER+'/'+ref(10)+'/executions',r,'synthetic-owner',True)[0],403)
        review={'decisionId':ref(40002),'executionSha256':record['sha256'],'acceptRecordedOutcome':True}
        self.assertEqual(self.request(BASE+'/'+ref(10)+'/review-outcome',review,TOKEN)[0],403)
        self.assertEqual(self.request(BASE+'/'+ref(10)+'/review-outcome',review,'synthetic-owner',True)[0],200)
        code,view=self.request(BASE+'/'+ref(10),token='synthetic-owner',owner=True)
        self.assertEqual(code,200);self.assertEqual(view['qualifiedControls'],1)
        self.assertNotIn('review',self.request(WORKER+'/'+ref(10)+'/executions',r,TOKEN)[1])
        self.assertIsNone(view['statisticalResult']);self.assertEqual(view['status'],'BLOCKED')
        self.assertNotIn('leaseToken',str(view));self.assertEqual(len(self.queue.status()['jobs']),3)

    def test_dispatch_context_is_owner_only_read_without_queue_or_state_mutation(self):
        self.fixture.freeze()
        path=BASE+'/'+ref(10)+'/inputs/'+ref(100)+'/dispatch-context'
        before=self.fixture.store.get(self.fixture.service.key)
        code,value=self.request(path,token='synthetic-owner',owner=True)
        self.assertEqual(code,200)
        self.assertFalse(value['launchAuthorized'])
        self.assertEqual(value['frames'],self.fixture.inputs[0]['frames'])
        self.assertEqual(before,self.fixture.store.get(self.fixture.service.key))
        self.assertEqual(self.queue.status()['jobs'],[])
        self.assertNotIn('leaseToken',str(value))
        self.assertNotIn('review',value)
        self.assertEqual(self.request(path,token=TOKEN)[0],403)
        worker_path=WORKER+'/'+ref(10)+'/inputs/'+ref(100)+'/dispatch-context'
        self.assertEqual(self.request(worker_path,token=TOKEN)[0],404)
        self.assertEqual(self.request(path,{},'synthetic-owner',True)[0],404)

    def test_dispatch_context_denies_unfrozen_and_revoked_plan(self):
        path=BASE+'/'+ref(10)+'/inputs/'+ref(100)+'/dispatch-context'
        self.assertEqual(self.request(path,token='synthetic-owner',owner=True)[0],400)
        self.fixture.freeze()
        self.fixture.service.revoke(ref(10),{'decisionId':ref(51000),
            'planHeadSha256':self.fixture.service.view(ref(10))['headSha256'],
            'evidenceSha256':sha(51000),'reason':'OWNER_WITHDRAWAL'})
        self.assertEqual(self.request(path,token='synthetic-owner',owner=True)[0],400)

    def test_marked_campaign_job_cannot_escape_through_legacy_http_lease_routes(self):
        f=self.fixture;f.freeze()
        context=f.service.dispatch_context(ref(10),ref(100))
        jobs=[{'requestId':ref(150000+i),'binding':{'bindingRef':ref(151000+i),
            'inputRef':frame['frameRef'],'referenceRef':ref(152000),
            'algorithmRef':ref(20),'contractRef':ref(30)}} for i,frame in enumerate(context['frames'])]
        intent=f.service.prepare_dispatch(ref(10),{'decisionId':ref(153000),
            'contextSha256':context['contextSha256'],'witnessRef':ref(100),'jobs':jobs,
            'workerId':ref(2),'rootId':ref(154000),'archiveSha256':sha(155000)})
        for item in jobs:self.queue.register(item['binding'])
        bridge=CampaignQueue(f.service,self.queue)
        projected=bridge.project(ref(10),intent['sha256'],0)
        request={'workerId':ref(2),'rootId':ref(154000),'jobId':projected['jobId'],
            'bindingRef':jobs[0]['binding']['bindingRef'],'reservationRef':ref(156000)}
        job=bridge.admit_and_reserve(ref(10),intent['sha256'],0,request,ref(157000))['job']
        for path,body in [('/v1/transient-analysis/worker/claim',{'workerId':ref(2),'rootId':ref(154000)}),
                          ('/v1/transient-analysis/worker/reserve',request)]:
            code,value=self.request(path,body,TOKEN)
            self.assertEqual(code,400);self.assertNotIn(job['leaseToken'],str(value))
        for path,token,owner in [('/v1/transient-analysis/jobs/'+job['jobId'],'synthetic-owner',True),
                                 ('/v1/transient-analysis/worker/jobs/'+job['jobId'],TOKEN,False)]:
            code,value=self.request(path,token=token,owner=owner)
            self.assertEqual(code,200);self.assertNotIn('leaseToken',str(value))
            self.assertNotIn('campaignOrigin',str(value));self.assertNotIn('campaignReservation',str(value))
        self.assertEqual(self.request(WORKER+'/'+ref(10)+'/admit-frame',{},TOKEN)[0],404)
        self.assertEqual(self.request(BASE+'/'+ref(10)+'/dispatch',{},'synthetic-owner',True)[0],404)

    def test_disabled_composition_keeps_authenticated_404(self):
        self.server.RequestHandlerClass=self.handler(enabled=False)
        self.assertEqual(self.request(BASE,token='synthetic-owner',owner=True)[0],404)
        self.assertEqual(self.request(BASE,token='not-owner',owner=True)[0],403)

    def test_forged_authority_field_and_malformed_payload_are_not_authenticated_reviews(self):
        r=copy.deepcopy(self.fixture.inputs[0]);r['authority']='AUTHENTICATED_OWNER_SCIENTIFIC_DECISION'
        self.assertEqual(self.request(WORKER+'/inputs',r,TOKEN)[0],400)
        r=copy.deepcopy(self.fixture.inputs[0]);r['frames'][0]['role']=[]
        self.assertEqual(self.request(WORKER+'/inputs',r,TOKEN)[0],400)
        self.assertEqual(self.fixture.service.view(ref(10))['qualifiedControls'],0)

    def test_campaign_worker_configuration_must_match_transient_queue(self):
        self.fixture.service.worker_id=ref(999)
        with self.assertRaisesRegex(ProtocolError,'WORKER_BINDING'):self.handler()


if __name__=='__main__':unittest.main()
