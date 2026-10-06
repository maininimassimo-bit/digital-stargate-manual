"""Synthetic revision evidence; never a native execution or Owner acceptance."""
import base64
import copy
import unittest
from .broker import encode, decode, ProtocolError, STATE_KEY
from . import test_scientific_portal as fixtures
from .scientific_portal import digest
from tools.scientific_registry.ingestion_storage import Conflict


class RevisionTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.ScientificTests()
        self.fixture.setUp()
        self.portal = self.fixture.portal
        self.job,self.lease = self.fixture.complete()
        self.parent = self.portal.deliver(self.job,self.fixture.payload(self.lease))
        self.identity = '8'*32
        workflow = b'var Root = new ProcessContainer;\nvar P = new PixelMath;\nP.expression = "1";\nRoot.add(P);'
        self.value = {k:v for k,v in self.fixture.payload(self.lease).items() if k in {'original','previewBase64'}}
        self.value.update(parentReviewSha256=self.parent['reviewSha256'],label='M31 approved refinement',
                          processingDate='2026-10-06',workflowBase64=base64.b64encode(workflow).decode(),
                          correlationsBase64=base64.b64encode(encode({'jobId':self.job,'revisionId':self.identity,
                          'parentReviewSha256':self.parent['reviewSha256'],'upstreamHistoryCompleteness':'NOT_ESTABLISHED',
                          'instances':[{'ordinal':1,'variable':'P'}]})).decode())
        self.value['original'] = {**self.value['original'],'sha256':'9'*64}

    def submit(self):
        return self.portal.deliver_revision(self.job,self.identity,self.value)

    def test_parent_and_public_gallery_unchanged_on_retry(self):
        result=self.submit()
        self.assertEqual(self.submit(),result)
        self.assertEqual(self.portal.result(self.job)['reviewSha256'],self.parent['reviewSha256'])
        self.assertEqual(result['imageId'],self.parent['imageId'])
        self.assertEqual(result['context'],self.parent['context'])
        self.assertEqual(result['workflowCompleteness'],'INCREMENTAL_REFINEMENT_ONLY')
        self.assertEqual(result['scientificAcceptance'],'OWNER_REVIEW_REQUIRED')
        self.assertEqual(result['publication'],'NONE')
        self.assertEqual(len(self.portal.revisions(self.job)),1)
        self.assertEqual(self.fixture.gallery['records'][0]['imageVersionId'],'VER-'+'e'*32)

    def test_conflicting_retry_preserves_original_revision(self):
        expected=self.submit()
        self.value['label']='different'
        with self.assertRaises(Conflict):self.submit()
        self.assertEqual(self.portal.revision(self.job,self.identity)['reviewSha256'],expected['reviewSha256'])

    def test_stale_parent_and_extra_fields_rejected_before_write(self):
        for patch in [{'parentReviewSha256':'0'*64},{'path':'C:/private'},{'processingDate':'2026-02-30'},
                      {'label':'C:/private'},{'original':{**self.value['original'],'width':True}}]:
            original=copy.deepcopy(self.value)
            self.value.update(patch)
            with self.assertRaises(ProtocolError):self.submit()
            self.value=original
        self.assertEqual(self.portal.revisions(self.job),[])

    def test_mismatched_correlations_and_script_execution_rejected(self):
        original=copy.deepcopy(self.value)
        for raw in [b'{}',encode({'jobId':self.job,'revisionId':'0'*32})]:
            self.value['correlationsBase64']=base64.b64encode(raw).decode()
            with self.assertRaises(ProtocolError):self.submit()
        self.value=original
        self.value['workflowBase64']=base64.b64encode(b'File.writeTextFile("C:/private", "bad");').decode()
        with self.assertRaises(ProtocolError):self.submit()

    def test_decision_bound_to_revision_not_parent(self):
        result=self.submit()
        with self.assertRaises(ProtocolError):
            self.portal.decide_revision(self.job,self.identity,{'reviewSha256':self.parent['reviewSha256'],'decision':'ACCEPT_PRIVATE'})
        decision={'reviewSha256':result['reviewSha256'],'decision':'ACCEPT_PRIVATE'}
        self.portal.decide_revision(self.job,self.identity,decision)
        self.assertEqual(self.portal.revision(self.job,self.identity)['decision'],decision)
        self.assertIsNone(self.portal.result(self.job)['decision'])
        with self.assertRaises(Conflict):
            self.portal.decide_revision(self.job,self.identity,{**decision,'decision':'REJECT'})

    def test_only_existing_mutable_state_authority_used(self):
        original_put=self.fixture.store.put
        def put(key,raw,generation=0):
            if generation and key != STATE_KEY:raise AssertionError('new overwrite authority')
            return original_put(key,raw,generation)
        self.fixture.store.put=put
        self.submit();self.submit()
        self.assertEqual(len(self.portal.revisions(self.job)),1)

    def test_assets_hash_checked_and_wrong_ids_rejected(self):
        result=self.submit()
        for role in ('preview','workflow','correlations'):
            self.assertEqual(digest(self.portal.revision_asset(self.job,self.identity,role)),result[role+'Sha256'])
        with self.assertRaises(ProtocolError):self.portal.revision(self.job,'../private')
        with self.assertRaises(ProtocolError):self.portal.revision(self.job,'7'*32)

    def test_uncommitted_delivery_cannot_be_reviewed(self):
        from unittest.mock import patch
        with patch.object(self.fixture.broker,'_mutate',side_effect=Conflict('lost index commit')):
            with self.assertRaises(Conflict):self.submit()
        with self.assertRaisesRegex(ProtocolError,'REVISION_PENDING'):self.portal.revision(self.job,self.identity)
        self.assertEqual(self.portal.revisions(self.job),[])
        self.submit()
        self.assertEqual(len(self.portal.revisions(self.job)),1)

    def test_concurrent_distinct_deliveries_preserve_all_bindings(self):
        from concurrent.futures import ThreadPoolExecutor
        def deliver(number):
            identity=f'{number:032x}'
            value=copy.deepcopy(self.value)
            correlation=decode(base64.b64decode(value['correlationsBase64']))
            correlation['revisionId']=identity
            value['correlationsBase64']=base64.b64encode(encode(correlation)).decode()
            return self.portal.deliver_revision(self.job,identity,value)
        with ThreadPoolExecutor(max_workers=4) as pool:
            results=list(pool.map(deliver,range(100,104)))
        self.assertEqual({r['revisionId'] for r in results},{r['revisionId'] for r in self.portal.revisions(self.job)})
        self.assertEqual(len(self.portal.revisions(self.job)),4)
        self.assertEqual(self.portal.result(self.job)['reviewSha256'],self.parent['reviewSha256'])

    def test_full_index_rejects_before_asset_or_receipt_writes(self):
        raw,generation=self.fixture.store.get(STATE_KEY)
        state=decode(raw);state['scientificRevisions']={self.job:[f'{i:032x}' for i in range(16)]}
        self.fixture.store.put(STATE_KEY,encode(state),generation)
        with self.assertRaisesRegex(ProtocolError,'REVISION_CAPACITY'):self.submit()
        self.assertFalse(self.fixture.store.exists(f'science/revisions/{self.job}/{self.identity}'))

    def test_http_role_separation_and_exact_revision_routes(self):
        import hashlib
        import threading
        import urllib.request
        import urllib.error
        from http.server import HTTPServer
        from .transport_http import handler_for, AuthError
        def owner(token):
            if token != 'OWNER':raise AuthError()
        server=HTTPServer(('127.0.0.1',0),handler_for(self.fixture.broker,owner,'https://portal.test',
            hashlib.sha256(fixtures.TOKEN.encode()).hexdigest(),self.portal))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        origin=f'http://127.0.0.1:{server.server_port}'
        route=f'/science/{self.job}/revisions/{self.identity}'
        owner_headers={'Origin':'https://portal.test','Authorization':'Bearer OWNER','Content-Type':'application/json'}
        worker_headers={'Authorization':'Bearer '+fixtures.TOKEN,'Content-Type':'application/json'}
        def request(path,body=None,headers=None):
            return urllib.request.urlopen(urllib.request.Request(origin+path,
                encode(body) if body is not None else None,headers=headers or {}))
        try:
            with request('/v1/worker'+route+'/result',self.value,worker_headers) as response:
                self.assertEqual(decode(response.read())['revisionId'],self.identity)
            for role in ('result','preview','workflow','correlations'):
                with self.assertRaises(urllib.error.HTTPError) as caught:request('/v1'+route+'/'+role)
                self.assertEqual(caught.exception.code,403)
                with request('/v1'+route+'/'+role,headers=owner_headers) as response:self.assertEqual(response.status,200)
                with self.assertRaises(urllib.error.HTTPError) as caught:request('/v1/worker'+route+'/'+role,headers=worker_headers)
                self.assertEqual(caught.exception.code,404)
            decision={'reviewSha256':self.portal.revision(self.job,self.identity)['reviewSha256'],'decision':'ACCEPT_PRIVATE'}
            with self.assertRaises(urllib.error.HTTPError) as caught:
                request('/v1/worker'+route+'/decision',decision,worker_headers)
            self.assertEqual(caught.exception.code,404)
            with request('/v1'+route+'/decision',decision,owner_headers) as response:self.assertEqual(response.status,200)
            with self.assertRaises(urllib.error.HTTPError) as caught:request('/v1'+route+'/result',self.value,owner_headers)
            self.assertEqual(caught.exception.code,404)
        finally:
            server.shutdown();thread.join();server.server_close()


if __name__ == '__main__':unittest.main()
