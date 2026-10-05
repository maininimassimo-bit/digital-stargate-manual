"""P5 synthetic model and actual loopback HTTP; never native/cloud evidence."""
import base64
import copy
import hashlib
from http.server import HTTPServer
import io
import json
from pathlib import Path
import threading
import unittest
import urllib.request
import urllib.error

from PIL import Image
from .broker import Broker, ProtocolError, encode, decode
from .scientific_portal import ScientificPortal, digest
from .transport_http import handler_for, AuthError
from .worker import NONLINEAR_RECIPE, actions
from tools.scientific_registry.ingestion_storage import MemoryStore, Conflict

WORKER, REF, TOKEN = 'a' * 32, 'b' * 32, 'c' * 64


class ScientificTests(unittest.TestCase):
    def setUp(self):
        self.store = MemoryStore()
        self.broker = Broker(self.store, WORKER)
        self.catalog = encode({'schemaVersion':'1.5','catalogStatus':'VERSIONED_ANALYTICS_PROJECTION',
            'sessions':[{'sessionId':'SESSION-M27-1','target':'M27','observationDate':'2026-09-01'},
                        {'sessionId':'SESSION-M42-1','target':'M42','observationDate':'2026-09-01'}]})
        self.gallery = {'records':[{'imageId':'IMG-'+'d'*32,'imageVersionId':'VER-'+'e'*32,
                                    'workflowId':'WF-'+'e'*32,'target':'M27','title':'Published M27'}]}
        self.portal = ScientificPortal(self.broker, lambda:self.catalog, lambda:self.gallery)
        self.input = {'inputRef':REF,'target':'M27','recipe':NONLINEAR_RECIPE,'manifestSha256':'f'*64}
        self.portal.register(self.input)
        self.request = {'requestId':'1'*32,'inputRef':REF,'catalogSha256':digest(self.catalog),
                        'sessionIds':['SESSION-M27-1'],'parent':{k:v for k,v in self.gallery['records'][0].items() if k in {'imageId','imageVersionId','workflowId'}},
                        'title':'M27 pilot','processingDate':'2026-10-05','associationConfirmed':True}

    def complete(self):
        job = self.portal.create(self.request)
        claim = self.broker.claim(WORKER, '2'*32)
        report = {'leaseToken':claim['leaseToken'],'sequence':1,'stage':'COMPLETED',
                  'processCount':29,'outputCount':15,'verified':True}
        self.broker.report(job['jobId'], WORKER, report)
        return job['jobId'], claim['leaseToken']

    def payload(self, lease):
        preview = io.BytesIO()
        Image.new('RGB',(4,3),'blue').save(preview,format='JPEG',comment=b'PRIVATE_METADATA')
        lines = ['var Root = new ProcessContainer;']
        for i, action in enumerate(actions(NONLINEAR_RECIPE)):
            lines += [f'var P{i} = new {action[1]};',f'Root.add( P{i} );']
        workflow = '\n'.join(lines).encode()
        return {'workerId':WORKER,'leaseToken':lease,'original':{'sha256':'3'*64,'byteSize':100,'width':1000,'height':800,'nonLinear':True},
                'previewBase64':base64.b64encode(preview.getvalue()).decode(),'workflowBase64':base64.b64encode(workflow).decode(),
                'correlationsBase64':base64.b64encode(encode({'jobId':'PIAI_'+self.request['requestId'],'recipe':NONLINEAR_RECIPE,
                    'upstreamHistoryCompleteness':'NOT_ESTABLISHED','instances':[{'ordinal':i+1,'variable':f'P{i}'} for i in range(29)]})).decode()}

    def test_registered_identity_is_immutable_and_no_paths_accepted(self):
        self.assertEqual(self.portal.register(self.input), self.input)
        with self.assertRaises(Conflict):self.portal.register({**self.input,'manifestSha256':'0'*64})
        with self.assertRaises(ProtocolError):self.portal.register({**self.input,'path':'private'})
        self.assertEqual(self.portal.options()['inputs'],[self.input])
        self.assertEqual(len(self.portal.options()['sessions']),1)

    def test_second_registration_reuses_only_authorized_mutable_state(self):
        from .broker import STATE_KEY
        original_put = self.store.put
        def guarded_put(key, raw, generation=0):
            if generation != 0 and key != STATE_KEY:
                raise PermissionError("immutable object overwrite forbidden")
            return original_put(key, raw, generation)
        self.store.put = guarded_put
        second = {**self.input, "inputRef": "9"*32}
        self.portal.register(second)
        self.portal.register(second)
        self.assertEqual(self.portal.options()["inputs"], [self.input, second])
        self.assertFalse(self.store.exists("science/input-index"))

    def test_cloud_correlations_replace_master_hashes_with_roles(self):
        from .scientific_delivery import minimized_correlations
        raw = encode({"instances": [{"dependencies": ["a"*64, "RGB"]}],
                      "runtimeRelations": [{"dependencies": ["a"*64]}]})
        result = minimized_correlations(raw, {"inputs": [{"role": "R", "sha256": "a"*64}]})
        self.assertNotIn(b"a"*64, result)
        self.assertEqual(decode(result)["instances"][0]["dependencies"], ["MASTER_R", "RGB"])
        self.assertIn(b"a"*64, raw)

    def test_governed_spaced_target_alias_preserves_exact_scientific_context(self):
        self.catalog = self.catalog.replace(b'"M27"', b'"M 27"')
        self.gallery["records"][0]["target"] = "M 27"
        self.request["catalogSha256"] = digest(self.catalog)
        options = self.portal.options()
        self.assertEqual(options["sessions"][0]["target"], "M 27")
        self.assertEqual(options["images"][0]["target"], "M 27")
        job = self.portal.create(self.request)
        context = self.portal.context(job["jobId"])
        self.assertEqual(context["sessionContext"]["sessions"][0]["target"], "M 27")
        self.assertEqual(context["input"]["target"], "M27")
        self.assertEqual(context["selection"]["parent"], self.request["parent"])

    def test_catalog_selection_keeps_all_spaced_m27_sessions_and_excludes_other_targets(self):
        catalog = decode(self.catalog)
        selected = [{"sessionId": f"SESSION-M27-{i}", "target": "M 27", "observationDate": "2026-09-01"}
                    for i in range(1, 17)]
        catalog["sessions"] = selected + [catalog["sessions"][1]]
        self.catalog = encode(catalog)
        expected = [row["sessionId"] for row in selected]
        self.assertEqual([s["sessionId"] for s in self.portal.options()["sessions"]], expected)
        self.request["catalogSha256"] = digest(self.catalog)
        self.request["sessionIds"] = expected
        self.request["parent"] = None
        job = self.portal.create(self.request)
        context = self.portal.context(job["jobId"])
        self.assertEqual([s["sessionId"] for s in context["sessionContext"]["sessions"]], expected)

    def test_target_aliases_do_not_accept_other_or_ambiguous_targets(self):
        from .scientific_portal import is_m27
        for target in (None, "M270", "M-27", "m27", "M  27", "M27?", "NGC 281"):
            self.assertFalse(is_m27(target))
        for target in ("M27", "M 27"):
            self.assertTrue(is_m27(target))

    def test_selection_pins_sessions_parent_and_recipe(self):
        created = self.portal.create(self.request)
        context = self.portal.context(created['jobId'])
        self.assertEqual(context['selection']['parent'], self.request['parent'])
        self.assertEqual(context['associationEvidence'],'OWNER_DECLARED')
        self.assertEqual(created['request']['recipe'],NONLINEAR_RECIPE)
        self.assertEqual(created['scientificContextSha256'],digest(encode(context)))
        self.assertNotIn('path',encode(context).decode())

    def test_idempotent_retry_preserves_old_catalog_and_parent(self):
        first = self.portal.create(self.request)
        self.catalog = self.catalog.replace(b'2026-09-01',b'2026-09-02')
        self.gallery = {'records':[]}
        self.assertEqual(self.portal.create(self.request),first)
        with self.assertRaises(ProtocolError):self.portal.create({**self.request,'title':'Different'})
        with self.assertRaises(ProtocolError):self.broker.create(first['request'])

    def test_invalid_selection_never_queues(self):
        bad = [{'inputRef':'0'*32},{'catalogSha256':'0'*64},{'sessionIds':['SESSION-M42-1']},
               {'sessionIds':['missing']},{'associationConfirmed':False},
               {'parent':{**self.request['parent'],'imageVersionId':'VER-'+'0'*32}}, {'script':'evil'}]
        for change in bad:
            with self.assertRaises(ValueError):self.portal.create({**self.request,**change})
        self.assertEqual(self.broker._state()[0]['jobs'],[])

    def test_context_tampering_is_rejected(self):
        job = self.portal.create(self.request)
        key = 'science/contexts/'+job['jobId']
        raw,generation=self.store.get(key)
        self.store.put(key,raw.replace(b'M27 pilot',b'changed'),generation)
        with self.assertRaisesRegex(ProtocolError,'CONTEXT_INTEGRITY'):self.portal.context(job['jobId'])

    def test_delivery_idempotent_exact_ids_and_private_review(self):
        job, lease = self.complete()
        payload = self.payload(lease)
        first = self.portal.deliver(job,payload)
        self.assertEqual(first,self.portal.deliver(job,payload))
        self.assertEqual(first['imageId'],self.request['parent']['imageId'])
        self.assertEqual(first['workflowId'],'WF-'+self.request['requestId'])
        self.assertEqual(first['context']['selection']['sessionIds'],self.request['sessionIds'])
        self.assertEqual(len(first['steps']),29)
        self.assertEqual(first['publication'],'NONE')
        self.assertEqual(first['executionEvidence'],'WORKER_REPORTED_NOT_ATTESTED')
        raw = self.portal.asset(job,'preview')
        self.assertNotIn(b'PRIVATE_METADATA',raw)
        self.assertNotIn('leaseToken',encode(self.portal.result(job)).decode())
        decision={'reviewSha256':first['reviewSha256'],'decision':'ACCEPT_PRIVATE'}
        self.portal.decide(job,decision);self.portal.decide(job,decision)
        self.assertEqual(self.portal.result(job)['decision'],decision)
        with self.assertRaises(Conflict):self.portal.decide(job,{**decision,'decision':'REJECT'})

    def test_stale_review_and_changed_delivery_are_rejected(self):
        job,lease=self.complete();payload=self.payload(lease)
        self.portal.deliver(job,payload)
        with self.assertRaises(ProtocolError):self.portal.decide(job,{'reviewSha256':'0'*64,'decision':'ACCEPT_PRIVATE'})
        changed=copy.deepcopy(payload);changed['original']['sha256']='4'*64
        with self.assertRaises(Conflict):self.portal.deliver(job,changed)

    def test_stored_result_integrity_is_checked(self):
        job,lease=self.complete();self.portal.deliver(job,self.payload(lease))
        key='science/results/'+job
        raw,generation=self.store.get(key)
        self.store.put(key,raw.replace(b'OWNER_PC',b'OTHER_PC'),generation)
        with self.assertRaisesRegex(ProtocolError,'RESULT_INTEGRITY'):self.portal.result(job)

    def test_preview_comes_from_verified_float32_pixels_and_retains_source(self):
        import tempfile,struct
        from .scientific_delivery import preview_bytes
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'synthetic.xisf'
            header=b'<xisf><Image geometry="1:1:3" sampleFormat="Float32" colorSpace="RGB" location="attachment:4096:12"/></xisf>'
            raw=b'XISF0100'+struct.pack('<II',len(header),0)+header
            raw+=bytes(4096-len(raw))+struct.pack('<fff',0,0.5,1)
            path.write_bytes(raw)
            preview=preview_bytes(path)
            self.assertEqual(path.read_bytes(),raw)
            with Image.open(io.BytesIO(preview)) as image:
                self.assertEqual(image.size,(1,1));self.assertEqual(image.mode,'RGB')
                self.assertEqual(image.getexif(),{})

    def test_delivery_requires_bound_verified_completion_and_exact_recipe(self):
        job=self.portal.create(self.request)['jobId'];claim=self.broker.claim(WORKER,'2'*32)
        with self.assertRaisesRegex(ProtocolError,'RESULT_NOT_COMPLETED'):self.portal.deliver(job,self.payload(claim['leaseToken']))
        self.broker.report(job,WORKER,{'leaseToken':claim['leaseToken'],'sequence':1,'stage':'COMPLETED','processCount':29,'outputCount':15,'verified':True})
        for change in ({'leaseToken':'0'*64},{'workerId':'0'*32},{'workflowBase64':base64.b64encode(b'alert(1)').decode()},
                       {'previewBase64':'invalid%%'},{'original':{'sha256':'0'*64}}):
            with self.assertRaises(ValueError):self.portal.deliver(job,{**self.payload(claim['leaseToken']),**change})

    def test_preview_and_workflow_have_no_public_route(self):
        def owner(token):
            if token!='OWNER':raise AuthError()
        server=HTTPServer(('127.0.0.1',0),handler_for(self.broker,owner,'https://portal.test',hashlib.sha256(TOKEN.encode()).hexdigest(),self.portal))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        origin=f'http://127.0.0.1:{server.server_port}'
        job,lease=self.complete();self.portal.deliver(job,self.payload(lease))
        try:
            for role in ('preview','workflow','correlations','result'):
                url=origin+f'/v1/science/{job}/{role}'
                with self.assertRaises(urllib.error.HTTPError) as caught:urllib.request.urlopen(url)
                self.assertEqual(caught.exception.code,403)
                request=urllib.request.Request(url,headers={'Origin':'https://portal.test','Authorization':'Bearer OWNER'})
                with urllib.request.urlopen(request) as response:self.assertEqual(response.status,200)
            request=urllib.request.Request(origin+'/v1/science/jobs',encode({**self.request,'requestId':'5'*32}),
                headers={'Origin':'https://portal.test','Authorization':'Bearer OWNER','Content-Type':'application/json'})
            with urllib.request.urlopen(request) as response:self.assertEqual(decode(response.read())['state'],'QUEUED')
            self.assertEqual(len(self.portal.jobs()),2)
        finally:
            server.shutdown();thread.join();server.server_close()


if __name__=='__main__':unittest.main()
