"""Sealed synthetic native declarations; no PixInsight launch, cloud or science OAT."""
import copy
import unittest
from pathlib import Path

from tools.pixinsight.local_pilot.broker import ProtocolError, encode
from tools.scientific_transients.attempt_journal import AttemptJournal, read_json
from tools.scientific_transients.local_report import inspect, export, render, kernel_rows
from tools.scientific_transients import test_native_supervisor as fixtures


class LocalReportTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.SupervisorTests(); self.fixture.setUp(); self.addCleanup(self.fixture.doCleanups)
        f = self.fixture
        supervisor = f.supervisor(); self.assertEqual(supervisor.start()['state'], 'RUNNING')
        f.native('COMPLETED'); self.assertEqual(supervisor.tick()['state'], 'COMPLETED')
        self.journal = f.journal
        self.sha = read_json(self.journal.directory / 'report.json')[1]
        self.output = f.fixture.root / 'exports'; self.output.mkdir()

    def test_sealed_export_retains_nulls_units_history_and_distinct_digests(self):
        before = len(self.fixture.transport.posts)
        result = export(self.journal, self.sha, self.output)
        value, local_sha = read_json(result / 'report.json')
        receipt, _ = read_json(result / 'export.json')
        self.assertEqual(value['technicalReportSha256'], self.sha)
        self.assertEqual(receipt['localReportSha256'], local_sha)
        self.assertNotEqual(local_sha, self.sha)
        row = value['measurements'][0]['rows'][0]
        self.assertIsNone(row['fullVariance']); self.assertIsNone(row['significance'])
        self.assertEqual(value['qualityCountsDeclared'], {'measured': 0, 'excluded': 0, 'incomplete': 1})
        self.assertEqual(value['measurements'][0]['unit'], 'NORMALIZED_SAMPLE_SUM')
        self.assertEqual(value['scienceValidation'], 'NOT_VALIDATED')
        self.assertFalse(value['completeDependencyArchive'])
        self.assertEqual(len(self.fixture.transport.posts), before)
        for path in result.iterdir():
            self.assertNotIn(self.fixture.claim['leaseToken'].encode(), path.read_bytes())
        self.assertIn('sconosciuta', (result / 'report.html').read_text(encoding='utf-8'))

    def test_wrong_digest_or_changed_artifact_refuses_before_export(self):
        with self.assertRaisesRegex(ProtocolError, 'SEAL_MISMATCH'):
            export(self.journal, 'f'*64, self.output)
        self.assertEqual(list(self.output.iterdir()), [])
        path = self.journal.directory / self.journal._events()[-2]['data']['files'][0]['path']
        path.write_bytes(b'changed checkpoint')
        with self.assertRaisesRegex(ProtocolError, 'CHECKPOINT_CHANGED'):
            export(self.journal, self.sha, self.output)
        self.assertEqual(list(self.output.iterdir()), [])

    def test_restart_can_read_sealed_attempt_without_replay(self):
        reopened = AttemptJournal(self.journal.directory, self.journal.anchor['identity'])
        self.assertEqual(inspect(reopened, self.sha), inspect(self.journal, self.sha))
        self.assertEqual(self.fixture.starts, 1)

    def test_existing_export_is_not_overwritten(self):
        directory = export(self.journal, self.sha, self.output)
        original = (directory / 'report.json').read_bytes()
        with self.assertRaises(FileExistsError): export(self.journal, self.sha, self.output)
        self.assertEqual((directory / 'report.json').read_bytes(), original)

    def test_no_source_overlap_or_active_attempt_export(self):
        with self.assertRaisesRegex(ProtocolError, 'ROOT_OVERLAP'):
            export(self.journal, self.sha, self.journal.directory)
        with self.assertRaisesRegex(ProtocolError, 'NOT_COMPLETED'):
            with unittest.mock.patch.object(self.journal, '_events', return_value=[{'kind':'RUNNING'}]):
                inspect(self.journal, self.sha)

    def test_html_escapes_local_evidence_and_has_no_active_content(self):
        value = inspect(self.journal, self.sha)
        value['artifactRoot'] = '<script>alert(1)</script>'
        page = render(value)
        self.assertNotIn('<script>', page); self.assertIn('&lt;script&gt;', page)
        self.assertIn('Content-Security-Policy', page)
        self.assertIn(self.sha, page)

    def test_unit_variance_authority_or_input_binding_cannot_be_promoted(self):
        event = self.journal._events()[-2]
        files = {r['role']:r for r in event['data']['files']}
        bundle, _ = read_json(self.journal.directory / files['HISTORY']['path'])
        params = read_json(self.journal.directory / files['PARAMETERS']['path'])
        for mutate in [lambda b:b['terminal'].update(unit='ADU'),
                       lambda b:b['terminal']['rows'][0].update(significance=5.),
                       lambda b:b.update(inputSha256='f'*64),
                       lambda b:b['terminal'].update(scienceValidation='ACCEPTED')]:
            changed = copy.deepcopy(bundle); mutate(changed)
            with self.assertRaises(ProtocolError):kernel_rows(changed, params, files['CHECKPOINT'], event['data']['processRef'])

    def test_mid_export_mutation_retains_failure_and_blocks_retry(self):
        original = inspect
        calls = 0
        def changed(journal, sha):
            nonlocal calls
            calls += 1
            if calls == 2: raise ProtocolError('REPORT_SOURCE_CHANGED')
            return original(journal, sha)
        with unittest.mock.patch('tools.scientific_transients.local_report.inspect', side_effect=changed):
            with self.assertRaises(ProtocolError): export(self.journal, self.sha, self.output)
        directory = self.output / self.journal.anchor['identity']['attemptId']
        self.assertTrue((directory / 'failed.json').exists())
        self.assertFalse((directory / 'export.json').exists())
        with self.assertRaises(FileExistsError):export(self.journal, self.sha, self.output)


    def test_each_table_has_named_keyboard_region_and_caption(self):
        from html.parser import HTMLParser
        class Tables(HTMLParser):
            def __init__(self):
                super().__init__(); self.regions = []; self.captions = 0
            def handle_starttag(self, tag, attributes):
                attributes = dict(attributes)
                if tag == 'div' and attributes.get('class') == 'scroll':
                    self.regions.append(attributes)
                if tag == 'caption': self.captions += 1
        value = inspect(self.journal, self.sha)
        value['measurements'].append(copy.deepcopy(value['measurements'][0]))
        parser = Tables(); parser.feed(render(value))
        self.assertEqual(len(parser.regions), 2)
        self.assertEqual(parser.captions, 2)
        for region in parser.regions:
            self.assertEqual(region['tabindex'], '0')
            self.assertEqual(region['role'], 'region')
            self.assertTrue(region['aria-label'])

    def test_render_preserves_missing_uncertainty_and_report(self):
        value = inspect(self.journal, self.sha); before = copy.deepcopy(value)
        page = render(value)
        self.assertEqual(value, before)
        self.assertIn('NOT_VALIDATED', page)
        self.assertIn('sconosciuta', page)
        for measurement in value['measurements']:
            for row in measurement['rows']:
                self.assertIsNone(row['fullVariance'])
                self.assertIsNone(row['significance'])

    def test_scroll_and_long_identifier_focus_styles(self):
        page = render(inspect(self.journal, self.sha))
        self.assertIn('body{overflow-wrap:anywhere;', page)
        self.assertIn('.scroll{overflow:auto;max-width:100%}', page)
        self.assertIn('.scroll:focus-visible{outline:3px solid #ffd479;', page)

    def test_operation_identifier_remains_escaped_in_heading(self):
        value = inspect(self.journal, self.sha)
        value['measurements'][0]['operationRef'] = '<script>invalid</script>'
        page = render(value)
        self.assertNotIn('<script>', page)
        self.assertIn('&lt;script&gt;invalid&lt;/script&gt;', page)

if __name__ == '__main__': unittest.main()
