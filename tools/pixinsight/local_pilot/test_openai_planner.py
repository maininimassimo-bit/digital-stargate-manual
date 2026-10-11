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
from .scientific_portal import ScientificPortal
from tools.scientific_registry.ingestion_storage import Conflict
from . import worker
from .planning_agent import cycle, scope, evidence_for
from .planning_diagnostics import LIMITATIONS
from .image_analysis import METHOD


def pixel_evidence(evidence):
    value = copy.deepcopy(evidence)
    value['pixelDiagnostics'] = []
    for master in value['masters']:
        count = master['width'] * master['height']
        row = {'channelIndex': 0, 'sampleCount': count, 'minimum': -1., 'maximum': 2.,
               'mean': .5, 'populationVariance': 1., 'zeroSamples': 0, 'oneSamples': 0,
               'belowZeroSamples': 1, 'aboveOneSamples': 1, 'constant': False,
               'sampledDistribution': {'gridWidth': 64, 'gridHeight': 64, 'count': 4096,
                  'method': 'UNIFORM_CELL_CENTERS_NO_INTERPOLATION', 'median': .5, 'mad': .1,
                  'quantiles': [-.1, .1, .5, .8, 1.1]}}
        value['pixelDiagnostics'].append({'role': master['role'], 'report': {
            'method': METHOD, 'sourceSha256': 'a' * 64, 'imageIndex': master['imageIndex'], 'width': master['width'], 'height': master['height'],
            'channels': [row], 'allFinite': True, 'linearity': 'NOT_ESTABLISHED',
            'calibration': 'NOT_ESTABLISHED', 'psf': {'status': 'UNAVAILABLE', 'reason': 'NATIVE_FIT_REQUIRED'},
            'backgroundNoise': {'status': 'UNAVAILABLE', 'reason': 'VALIDATED_BACKGROUND_MASK_REQUIRED'},
            'acceptance': 'DIAGNOSTIC_ONLY', 'limitations': copy.deepcopy(LIMITATIONS)}})
    return value


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

    def test_numeric_diagnostics_are_sent_without_source_hashes(self):
        evidence = pixel_evidence(self.evidence())
        validate_evidence(evidence, 'M27', 'LRGB')
        sent = []
        OpenAIPlanner('key', 'test-model', 0, send=lambda p: sent.append(p) or response()).generate('Test', 'M27', evidence)
        self.assertNotIn('sourceSha256', sent[0]['input'])
        self.assertNotIn('inputSetSha256', sent[0]['input'])
        self.assertIn('populationVariance', sent[0]['input'])
        self.assertEqual(evidence['pixelDiagnostics'][0]['report']['sourceSha256'], 'a' * 64)

    def test_invalid_diagnostics_cannot_inject_strings_or_claim_scientific_evidence(self):
        for mutate in [lambda r: r.update(path='private'), lambda r: r.update(linearity='LINEAR'),
                       lambda r: r.update(allFinite=False), lambda r: r.update(width=999), lambda r: r.update(imageIndex=1),
                       lambda r: r['channels'][0].update(mean=float('nan')),
                       lambda r: r['channels'][0].update(zeroSamples=800001),
                       lambda r: r['channels'][0]['sampledDistribution'].update(method='instructions')]:
            value = pixel_evidence(self.evidence())
            mutate(value['pixelDiagnostics'][0]['report'])
            with self.assertRaises(ProtocolError):
                validate_evidence(value, 'M27', 'LRGB')

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

    def enable(self, send=None, daily_limit=2, pixel_statistics=False):
        self.calls = []
        self.portal.planner = OpenAIPlanner('test-key', 'test-model', daily_limit,
                    send=send or (lambda p: self.calls.append(p) or response()))
        selected = {**self.selection(), 'openaiPlanning': {'dataTransferConfirmed': True}}
        if pixel_statistics:
            selected['openaiPlanning']['pixelStatisticsConfirmed'] = True
        self.portal.create_intake(selected)
        evidence = {'recipe': worker.NONLINEAR_RECIPE, 'field': None, 'inputSetSha256': 'e' * 64,
                    'masters': self.plan()['masters']}
        return selected['requestId'], {'workerId': WORKER, 'evidence': evidence}

    def test_diagnostics_require_distinct_consent_before_paid_reservation(self):
        request_id, body = self.enable()
        body['evidence'] = pixel_evidence(body['evidence'])
        with self.assertRaisesRegex(ProtocolError, 'AI_PIXEL_STATISTICS_CONSENT_BINDING'):
            self.portal.generate_openai(request_id, body)
        self.assertEqual(self.calls, [])
        self.assertEqual(self.portal.openai_state(request_id)['state'], 'AWAITING_LOCAL_EVIDENCE')

    def test_consented_diagnostics_are_bound_and_replay_does_not_pay_again(self):
        with patch.dict('os.environ', {'DSG_PIAI_PIXEL_STATISTICS': 'LOCAL_WORKER_VERIFIED'}):
            request_id, body = self.enable(pixel_statistics=True)
        missing = copy.deepcopy(body)
        with self.assertRaisesRegex(ProtocolError, 'AI_PIXEL_STATISTICS_CONSENT_BINDING'):
            self.portal.generate_openai(request_id, missing)
        body['evidence'] = pixel_evidence(body['evidence'])
        first = self.portal.generate_openai(request_id, body)
        self.assertEqual(first['state'], 'AI_DRAFT_READY')
        self.assertEqual(self.portal.generate_openai(request_id, body), first)
        self.assertEqual(len(self.calls), 1)
        changed = copy.deepcopy(body)
        changed['evidence']['pixelDiagnostics'][0]['report']['sourceSha256'] = 'b' * 64
        with self.assertRaisesRegex(ProtocolError, 'AI_EVIDENCE_CHANGED'):
            self.portal.generate_openai(request_id, changed)
        self.assertEqual(len(self.calls), 1)

    def test_pixel_statistics_intake_is_disabled_until_worker_verified(self):
        with patch.dict('os.environ', {'DSG_PIAI_PIXEL_STATISTICS': ''}):
            with self.assertRaisesRegex(ProtocolError, 'AI_PIXEL_STATISTICS_DISABLED'):
                self.enable(pixel_statistics=True)

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

    def test_result_storage_failure_restart_keeps_paid_send_reserved(self):
        request_id, payload = self.enable()
        original = self.store.put
        def failing(key, raw, generation=0):
            if key.startswith('science/openai-results/'):
                raise Conflict('synthetic result write failure')
            return original(key, raw, generation)
        with patch.object(self.store, 'put', side_effect=failing), self.assertRaises(Conflict):
            self.portal.generate_openai(request_id, payload)
        restarted = ScientificPortal(self.broker, lambda: self.catalog, lambda: self.gallery, self.portal.planner)
        self.assertEqual(restarted.generate_openai(request_id, payload)['state'], 'AI_REQUEST_RESERVED_NO_RETRY')
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(restarted.jobs(), [])

    def test_reservation_storage_failure_sends_nothing(self):
        request_id, payload = self.enable()
        with patch.object(self.broker, '_mutate', side_effect=Conflict('synthetic reserve failure')), self.assertRaises(Conflict):
            self.portal.generate_openai(request_id, payload)
        self.assertEqual(self.calls, [])

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

    def test_disabled_daily_quota_allows_distinct_requests_and_keeps_idempotency(self):
        request_id, payload = self.enable(daily_limit=0)
        first = self.portal.generate_openai(request_id, payload)
        second_id = '2' * 32
        self.portal.create_intake({**self.selection(), 'requestId': second_id,
                                  'openaiPlanning': {'dataTransferConfirmed': True}})
        self.assertEqual(self.portal.generate_openai(second_id, payload)['state'], 'AI_DRAFT_READY')
        self.assertEqual(self.portal.generate_openai(request_id, payload), first)
        self.assertEqual(len(self.calls), 2)

    def test_disabled_daily_quota_does_not_disable_storage_capacity(self):
        request_id, payload = self.enable(daily_limit=0)
        def fill(state, now):
            state['openaiAttempts'] = {format(n, '032x'): {'day': now[:10]} for n in range(16)}
        self.broker._mutate(fill)
        with self.assertRaisesRegex(ProtocolError, 'AI_ATTEMPT_CAPACITY'):
            self.portal.generate_openai(request_id, payload)
        self.assertEqual(self.calls, [])

    def test_invalid_daily_configuration_rejected(self):
        for value in (-1, 17, True, 0.0, '0'):
            with self.subTest(value=value), self.assertRaisesRegex(ProtocolError, 'AI_DAILY_LIMIT'):
                OpenAIPlanner('test-key', 'test-model', value)

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

    def test_worker_reads_pixels_and_binds_digest_without_exporting_paths(self):
        import hashlib
        import struct
        rows = []
        for role in worker.ROLES:
            path = self.folder / (role + '.xisf')
            header = b'<xisf><Image geometry="1000:800:1" sampleFormat="Float32" colorSpace="Gray" location="attachment:4096:3200000"/></xisf>'
            prefix = b'XISF0100' + struct.pack('<II', len(header), 0) + header
            path.write_bytes(prefix + bytes(4096 - len(prefix)) + struct.pack('<f', .25) * 800000)
            rows.append({'role': role, 'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                         'imageIndex': 0, 'width': 1000, 'height': 800})
        intake = {**self.intake, 'target': 'M27'}
        intake['selection']['openaiPlanning'] = {'dataTransferConfirmed': True, 'pixelStatisticsConfirmed': True}
        preset = {'recipe': worker.NONLINEAR_RECIPE, 'field': None, 'mapping': None}
        with patch('tools.pixinsight.local_pilot.planning_agent.inspect', return_value=rows):
            evidence = evidence_for({}, intake, preset)
        self.assertEqual([r['report']['sourceSha256'] for r in evidence['pixelDiagnostics']], [r['sha256'] for r in rows])
        self.assertTrue(all(r['report']['channels'][0]['mean'] == .25 for r in evidence['pixelDiagnostics']))
        self.assertNotIn('path', encode(evidence).decode())
        rows[0]['sha256'] = 'f' * 64
        with patch('tools.pixinsight.local_pilot.planning_agent.inspect', return_value=rows):
            with self.assertRaisesRegex(ValueError, 'ANALYSIS_INPUT_CHANGED'):
                evidence_for({}, intake, preset)

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
