"""Offline provider, persistence, consent and local input binding regressions."""
import copy
from concurrent.futures import ThreadPoolExecutor
from http.server import HTTPServer
from pathlib import Path
import threading
import urllib.error
import urllib.request
import unittest
from unittest.mock import patch

from .broker import ProtocolError, decode, encode
from .intake import sha
from .openai_planner import OpenAIPlanner, validate_evidence, VERSION
from . import test_intake as intake_fixtures
from .test_scientific_portal import WORKER, TOKEN
from .transport_http import handler_for
from . import worker
from .planning_agent import cycle, scope


def tuning():
    return {'background': {'polyDegree': 1, 'boxSize': 16, 'boxSeparation': 32},
            'processing': copy.deepcopy(worker.PROCESSING_DEFAULTS),
            'rationale': 'Dettaglio moderato entro i limiti della ricetta.',
            'limitations': 'Metadati soltanto; qualità scientifica e risultato da valutare.'}


def response(value=None):
    return {'id': 'resp_offline_test', 'model': 'test-model-snapshot', 'status': 'completed',
            'output': [{'type': 'message', 'role': 'assistant', 'status': 'completed',
                        'content': [{'type': 'output_text', 'text': encode(value or tuning()).decode()}]}],
            'usage': {'input_tokens': 40, 'output_tokens': 60, 'total_tokens': 100}}


class ProviderTests(unittest.TestCase):
    def evidence(self):
        return {'recipe': worker.NONLINEAR_RECIPE, 'field': None, 'inputSetSha256': 'e' * 64,
                'masters': [{'role': r, 'width': 1000, 'height': 800, 'imageIndex': 0} for r in worker.ROLES]}

    def test_minimized_payload_no_tools_store_or_private_hash_and_actual_model(self):
        sent = []
        planner = OpenAIPlanner('private-test-key', 'test-model', 2, send=lambda p: sent.append(p) or response())
        value, receipt = planner.generate('Dettaglio naturale', 'M27', self.evidence())
        self.assertEqual(value, tuning())
        self.assertEqual(receipt['model'], 'test-model-snapshot')
        self.assertEqual(receipt['requestedModel'], 'test-model')
        self.assertFalse(sent[0]['store'])
        self.assertNotIn('tools', sent[0])
        self.assertNotIn('inputSetSha256', sent[0]['input'])
        self.assertNotIn('private-test-key', encode(sent).decode())
        self.assertEqual(sent[0]['text']['format']['schema']['additionalProperties'], False)

    def test_paths_urls_secrets_rejected_before_send(self):
        for prompt in [r'Leggi F:\Astro', 'https://private.test', 'sk-example', 'api_key=secret']:
            calls = []
            planner = OpenAIPlanner('test-key', 'test-model', 1, send=lambda p: calls.append(p))
            with self.assertRaises(ProtocolError):
                planner.generate(prompt, 'M27', self.evidence())
            self.assertEqual(calls, [])

    def test_refusal_incomplete_tool_and_unbounded_results_rejected(self):
        bad = []
        item = response(); item['status'] = 'incomplete'; bad.append(item)
        item = response(); item['output'][0]['content'] = [{'type': 'refusal', 'refusal': 'No'}]; bad.append(item)
        item = response(); item['output'] = [{'type': 'function_call', 'name': 'shell'}]; bad.append(item)
        item = tuning(); item['processing']['sharpenL'] = 9; bad.append(response(item))
        item = tuning(); item['script'] = 'arbitrary()'; bad.append(response(item))
        item = tuning(); item['rationale'] = 'Bearer secret'; bad.append(response(item))
        item = response(); item['output'][0]['content'][0]['text'] = '{"a":1,"a":2}'; bad.append(item)
        for item in bad:
            with self.subTest(item=item), self.assertRaisesRegex(ProtocolError, 'AI_PROVIDER_FAILED_NO_RETRY'):
                OpenAIPlanner('key', 'test-model', 1, send=lambda p: item).generate('Test', 'M27', self.evidence())

    def test_evidence_cannot_contain_paths_or_invent_field_for_other_target(self):
        for change in [{'path': 'private'}, {'recipe': 'shell'}, {'field': {}},
                       {'masters': [{'role': 'RGB', 'width': 1, 'height': 1, 'imageIndex': 0}]}]:
            with self.assertRaises(ProtocolError):
                validate_evidence({**self.evidence(), **change}, 'M27', 'LRGB')
        with self.assertRaises(ProtocolError):
            validate_evidence(self.evidence(), 'M42', 'LRGB')


class FlowTests(unittest.TestCase):
    setUp = intake_fixtures.IntakeTests.setUp
    selection = intake_fixtures.IntakeTests.selection
    plan = intake_fixtures.IntakeTests.plan

    def enable(self, send=None, daily_limit=2):
        self.calls = []
        self.portal.planner = OpenAIPlanner('test-key', 'test-model', daily_limit,
                    send=send or (lambda p: self.calls.append(p) or response()))
        selected = {**self.selection(), 'openaiPlanning': {'dataTransferConfirmed': True}}
        self.portal.create_intake(selected)
        evidence = {'recipe': worker.NONLINEAR_RECIPE, 'field': None, 'inputSetSha256': 'e' * 64,
                    'masters': self.plan()['masters']}
        return selected['requestId'], {'workerId': WORKER, 'evidence': evidence}

    def test_disabled_and_missing_consent_never_send(self):
        with self.assertRaisesRegex(ProtocolError, 'AI_PROVIDER_DISABLED'):
            self.portal.create_intake({**self.selection(), 'openaiPlanning': {'dataTransferConfirmed': True}})
        with self.assertRaisesRegex(ProtocolError, 'CONSENT'):
            self.portal.create_intake({**self.selection(), 'openaiPlanning': {'dataTransferConfirmed': False}})
        with self.assertRaisesRegex(ProtocolError, 'CONSENT'):
            self.portal.create_intake({**self.selection(), 'openaiPlanning': {'dataTransferConfirmed': 1}})
        self.assertEqual(self.portal.jobs(), [])

    def test_cached_replay_exact_draft_and_owner_confirmation(self):
        request_id, payload = self.enable()
        draft = self.portal.generate_openai(request_id, payload)
        self.assertEqual(self.portal.generate_openai(request_id, payload), draft)
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.portal.jobs(), [])
        plan = {**self.plan(), **draft['plan']}
        with self.assertRaisesRegex(ProtocolError, 'AI_DRAFT_BINDING'):
            self.portal.propose(request_id, {**plan, 'rationale': 'Changed'})
        ready = self.portal.propose(request_id, plan)
        job = self.portal.approve_plan(request_id, {'proposalSha256': ready['proposalSha256']})
        context = self.portal.context(job['jobId'])
        self.assertEqual(context['intent']['plan']['aiProvenance']['method'], VERSION)
        self.assertEqual(context['intent']['intake']['aiMode'], 'OPENAI_API_PLANNING')
        self.assertEqual(len(self.portal.jobs()), 1)

    def test_failure_timeout_and_restart_never_resend(self):
        sends = []
        def failed(p):
            sends.append(p)
            raise TimeoutError('private provider payload')
        request_id, payload = self.enable(failed)
        self.assertEqual(self.portal.generate_openai(request_id, payload)['state'], 'AI_FAILED_NO_RETRY')
        self.assertEqual(self.portal.generate_openai(request_id, payload)['state'], 'AI_FAILED_NO_RETRY')
        self.assertEqual(len(sends), 1)
        self.assertNotIn('private provider', encode(self.portal.openai_state(request_id)).decode())

    def test_concurrent_same_request_one_send_and_ambiguous_crash_reserved(self):
        entered, release = threading.Event(), threading.Event()
        sends = []
        def slow(p):
            sends.append(p); entered.set(); release.wait(5)
            return response()
        request_id, payload = self.enable(slow)
        with ThreadPoolExecutor(max_workers=2) as pool:
            first = pool.submit(self.portal.generate_openai, request_id, payload)
            self.assertTrue(entered.wait(5))
            second = self.portal.generate_openai(request_id, payload)
            self.assertEqual(second['state'], 'AI_REQUEST_RESERVED_NO_RETRY')
            release.set(); self.assertEqual(first.result()['state'], 'AI_DRAFT_READY')
        self.assertEqual(len(sends), 1)

    def test_daily_cap_and_changed_evidence(self):
        request_id, payload = self.enable(daily_limit=1)
        self.portal.generate_openai(request_id, payload)
        changed = copy.deepcopy(payload); changed['evidence']['inputSetSha256'] = 'd' * 64
        with self.assertRaisesRegex(ProtocolError, 'AI_EVIDENCE_CHANGED'):
            self.portal.generate_openai(request_id, changed)
        self.portal.create_intake({**self.selection(), 'requestId': '2' * 32, 'openaiPlanning': {'dataTransferConfirmed': True}})
        with self.assertRaisesRegex(ProtocolError, 'AI_DAILY_LIMIT'):
            self.portal.generate_openai('2' * 32, payload)
        self.assertEqual(len(self.calls), 1)

    def test_withdrawal_prevents_provider_send(self):
        request_id, payload = self.enable()
        self.portal.withdraw_intake(request_id, {})
        with self.assertRaisesRegex(ProtocolError, 'WITHDRAWN'):
            self.portal.generate_openai(request_id, payload)
        self.assertEqual(self.calls, [])

    def test_http_owner_cannot_use_worker_provider_route(self):
        request_id, payload = self.enable()
        server = HTTPServer(('127.0.0.1', 0), handler_for(self.broker, lambda token: None,
                        'https://portal.test', __import__('hashlib').sha256(TOKEN.encode()).hexdigest(), self.portal))
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        try:
            path = '/v1/worker/science/intakes/' + request_id + '/openai-plan'
            request = urllib.request.Request('http://127.0.0.1:' + str(server.server_port) + path,
                encode(payload), headers={'Content-Type': 'application/json', 'Origin': 'https://portal.test', 'Authorization': 'Bearer ' + TOKEN})
            with self.assertRaises(urllib.error.HTTPError) as raised:
                urllib.request.urlopen(request)
            self.assertEqual(raised.exception.code, 403)
            self.assertEqual(self.calls, [])
            request.remove_header('Origin')
            with urllib.request.urlopen(request) as reply:
                self.assertEqual(decode(reply.read())['state'], 'AI_DRAFT_READY')
        finally:
            server.shutdown(); thread.join(); server.server_close()


class LocalAgentTests(unittest.TestCase):
    setUp = intake_fixtures.LocalInspectionTests.setUp
    write = intake_fixtures.LocalInspectionTests.write

    def test_pc_cycle_real_synthetic_headers_proposes_once_never_launches(self):
        intake = {**self.intake, 'target': 'M27', 'state': 'AWAITING_ASSISTANT_PLAN',
                  'openai': {'state': 'AWAITING_LOCAL_EVIDENCE'}}
        intake['selection']['openaiPlanning'] = {'dataTransferConfirmed': True}
        config = self.folder / 'config.json'
        config.write_bytes(encode({'serviceOrigin': 'https://test.run.app', 'workerId': WORKER,
                                  'workerRoot': str(self.folder), 'registry': {}}))
        settings = {'allowedMasterRoots': [str(self.folder)], 'targets': {'M27': {
            'recipe': worker.NONLINEAR_RECIPE, 'field': None, 'mapping': None}}}
        posts = []
        class FakeTransport:
            def request(self, path): return {'intakes': [intake]}
            def post(self, path, value):
                posts.append((path, value))
                if path.endswith('/openai-plan'):
                    return {'state': 'AI_DRAFT_READY', 'evidence': value['evidence'],
                            'plan': {**tuning(), 'recipe': worker.NONLINEAR_RECIPE}}
                return {'state': 'PLAN_READY'}
        with patch('tools.pixinsight.local_pilot.planning_agent.local_directory', side_effect=lambda v: str(self.folder)), \
             patch('tools.pixinsight.local_pilot.intake_assistant.local_directory', side_effect=lambda v: str(self.folder)):
            result = cycle(config, settings, FakeTransport())
        self.assertEqual(result['requests'][0]['state'], 'PLAN_READY')
        self.assertFalse(result['nativeStarted'])
        self.assertEqual(len(posts), 3)
        self.assertEqual(len(decode(config.read_bytes())['registry']), 1)
        self.assertNotIn('path', posts[0][1]['evidence']['masters'][0])
        with self.assertRaisesRegex(ProtocolError, 'REVIEWED_TARGET_REQUIRED'), \
             patch('tools.pixinsight.local_pilot.planning_agent.local_directory', return_value=str(self.folder)):
            scope({**intake, 'target': 'M42'}, settings)
