"""Private synthetic dossiers; no providers, native processing or scientific OAT."""
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError, encode, decode
from tools.scientific_transients.local_registry import LocalRegistry, ROLES, fingerprint
from tools.scientific_transients import reporting_draft as draft


class DraftTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.artifacts, self.registry, self.output = [self.root / n for n in ('artifacts', 'registry', 'output')]
        for path in (self.artifacts, self.registry, self.output): path.mkdir()
        self.local = LocalRegistry(self.artifacts, self.registry)
        binding = {k: str(i) * 32 for i, k in enumerate(
            ('bindingRef', 'inputRef', 'referenceRef', 'algorithmRef', 'contractRef'), 1)}
        manifest = {'protocol': 'DSG_TRANSIENT_LOCAL_BINDING_V1', 'binding': binding, 'files': []}
        for role in sorted(ROLES):
            path = self.artifacts / (role + '.dat'); path.write_bytes(b'fixture-not-real')
            manifest['files'].append({'role': role, 'path': path.name, **fingerprint(path)})
        receipt = self.local.register(encode(manifest))
        self.request = {'protocol': draft.PROTOCOL, 'dossierRef': 'a' * 32, 'bindingRef': binding['bindingRef'],
            'manifestSha256': receipt['manifestSha256'], 'categoryDeclared': 'GALACTIC_NOVA_CANDIDATE',
            'channelDeclared': 'CBAT', 'dataOriginDeclared': 'SYNTHETIC', 'note': 'fixture',
            'evidencePaths': ['INPUT.dat']}
        self.path = self.root / 'request.json'

    def pin(self):
        raw = encode(self.request); self.path.write_bytes(raw)
        return hashlib.sha256(raw).hexdigest()

    def export(self):
        return draft.export(self.local, self.path, self.pin(), self.output)

    def test_all_channels_are_declarations_only_and_offline(self):
        with patch('socket.socket', side_effect=AssertionError('network forbidden')):
            for i, (category, channel) in enumerate(draft.CHANNELS.items()):
                self.request.update(categoryDeclared=category, channelDeclared=channel, dossierRef=str(i + 1) * 32)
                directory = self.export(); value = decode((directory / 'dossier.json').read_bytes())
                self.assertEqual(value['state'], 'DRAFT')
                self.assertFalse(value['submissionAuthorized']); self.assertFalse(value['declarationsAttested'])
                self.assertEqual(value['scienceValidation'], 'NOT_VALIDATED')
                self.assertEqual(value['externalSubmission'], 'NONE')
                self.assertFalse(value['completeDependencyArchive'])
                receipt = decode((directory / 'export.json').read_bytes())
                for name, expected in receipt['files'].items(): self.assertEqual(fingerprint(directory / name), expected)

    def test_wrong_channel_or_unknown_category_rejected(self):
        for category, channel in [('GALACTIC_NOVA_CANDIDATE', 'TNS'), ('UNKNOWN', 'CBAT'), ('UNKNOWN', None)]:
            self.request.update(categoryDeclared=category, channelDeclared=channel)
            with self.assertRaises(ProtocolError): self.export()
        self.assertEqual(list(self.output.iterdir()), [])

    def test_authority_credentials_and_extra_fields_rejected(self):
        for key in ('scienceValidation', 'accepted', 'api_key', 'endpoint', 'submissionAuthorized'):
            self.request[key] = 'secret-or-claim'
            with self.assertRaises(ProtocolError): self.export()
            del self.request[key]
        self.assertEqual(list(self.output.iterdir()), [])

    def test_raw_duplicate_keys_rejected_even_when_pinned(self):
        raw = encode(self.request)[:-1] + b',"note":"override"}'
        self.path.write_bytes(raw)
        with self.assertRaises(ProtocolError):
            draft.export(self.local, self.path, hashlib.sha256(raw).hexdigest(), self.output)

    def test_request_changed_rejected(self):
        pinned = self.pin(); self.path.write_bytes(b'{}')
        with self.assertRaisesRegex(ProtocolError, 'DRAFT_REQUEST_CHANGED'):
            draft.export(self.local, self.path, pinned, self.output)

    def test_registered_evidence_tamper_rejected(self):
        (self.artifacts / 'INPUT.dat').write_bytes(b'changed')
        with self.assertRaisesRegex(ProtocolError, 'LOCAL_BYTES_MISMATCH'): self.export()
        self.assertEqual(list(self.output.iterdir()), [])

    def test_unregistered_duplicate_and_traversal_paths_rejected(self):
        for paths in (['missing.dat'], ['INPUT.dat', 'INPUT.dat'], ['../request.json'], ['/absolute'], [], ['INPUT.dat', {}]):
            self.request['evidencePaths'] = paths
            with self.assertRaises(ProtocolError): self.export()

    def test_root_overlap_and_source_in_output_rejected(self):
        pinned = self.pin()
        for root in (self.artifacts, self.registry, self.root):
            with self.assertRaises(ProtocolError): draft.export(self.local, self.path, pinned, root)
        self.path = self.output / 'request.json'; pinned = self.pin()
        with self.assertRaises(ProtocolError): draft.export(self.local, self.path, pinned, self.output)

    def test_hostile_text_passive_and_not_converted_to_measurements(self):
        self.request['note'] = '<script>alert(1)</script><img src="https://evil"> NORMALIZED_SAMPLE_SUM'
        directory = self.export(); rendered = (directory / 'dossier.html').read_text(encoding='utf-8')
        self.assertNotIn('<script>', rendered); self.assertNotIn('<img', rendered)
        self.assertIn('&lt;script&gt;', rendered); self.assertIn('default-src &#39;none&#39;', rendered)
        value = decode((directory / 'dossier.json').read_bytes())
        self.assertNotIn('measurements', value)

    def test_reused_ref_does_not_overwrite(self):
        directory = self.export(); before = {p.name: p.read_bytes() for p in directory.iterdir()}
        self.request['note'] = 'different'
        with self.assertRaises(FileExistsError): self.export()
        self.assertEqual(before, {p.name: p.read_bytes() for p in directory.iterdir()})

    def test_mid_export_mutation_keeps_partial_and_blocks_retry(self):
        original = draft.render
        def mutate(value):
            (self.artifacts / 'INPUT.dat').write_bytes(b'mutated-after-first-verification')
            return original(value)
        with patch.object(draft, 'render', side_effect=mutate):
            with self.assertRaises(ProtocolError): self.export()
        directory = self.output / self.request['dossierRef']
        self.assertTrue((directory / 'failed.json').is_file()); self.assertFalse((directory / 'export.json').exists())
        self.assertTrue((directory / 'dossier.json').is_file())
        (self.artifacts / 'INPUT.dat').write_bytes(b'fixture-not-real')
        with self.assertRaises(FileExistsError): self.export()

    def test_request_changed_during_export_preserves_failure(self):
        original = draft.render
        def mutate(value):
            self.path.write_bytes(b'{}'); return original(value)
        with patch.object(draft, 'render', side_effect=mutate):
            with self.assertRaises(ProtocolError): self.export()
        self.assertTrue((self.output / self.request['dossierRef'] / 'failed.json').exists())


    def test_long_note_and_dependency_paths_remain_passive_and_complete(self):
        self.request['note'] = 'identificativo_' * 60 + '<script>alert(1)</script>'
        directory = self.export()
        value = decode((directory / 'dossier.json').read_bytes())
        rendered = (directory / 'dossier.html').read_text(encoding='utf-8')
        self.assertEqual(value['declarations']['note'], self.request['note'])
        self.assertIn('identificativo_' * 60, rendered)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', rendered)
        self.assertNotIn('<script>', rendered)
        self.assertIn('NOT_VALIDATED', rendered)
        self.assertFalse(value['submissionAuthorized'])
        receipt = decode((directory / 'export.json').read_bytes())
        self.assertEqual(fingerprint(directory / 'dossier.html'), receipt['files']['dossier.html'])

    def test_dossier_structure_preserves_long_values_without_external_assets(self):
        from html.parser import HTMLParser
        class Parser(HTMLParser):
            def __init__(self):
                super().__init__(); self.tags = []; self.meta = []; self.text = []
            def handle_starttag(self, tag, attrs):
                self.tags.append(tag)
                if tag == 'meta': self.meta.append(dict(attrs))
            def handle_data(self, data): self.text.append(data)
        value = {'declarations': {'categoryDeclared': 'MOVING_OBJECT_CANDIDATE',
            'channelDeclared': 'MPC', 'dataOriginDeclared': 'SYNTHETIC', 'note': 'nota_' * 200},
            'selectedEvidence': [{'path': 'cartella/' + 'nome_' * 200, 'sha256': 'a' * 64}],
            'missingGates': list(draft.GAPS), 'artifactRoot': 'fixture/' + 'percorso_' * 200}
        rendered = draft.render(value); parser = Parser(); parser.feed(rendered)
        for tag in ('head', 'body', 'main'): self.assertEqual(parser.tags.count(tag), 1)
        for tag in ('script', 'img', 'link', 'iframe', 'a'): self.assertNotIn(tag, parser.tags)
        for text in (value['declarations']['note'], value['selectedEvidence'][0]['path'], value['artifactRoot']):
            self.assertIn(text, ''.join(parser.text))
        csp = next(m['content'] for m in parser.meta if m.get('http-equiv') == 'Content-Security-Policy')
        for rule in ("default-src 'none'", "base-uri 'none'", "form-action 'none'"):
            self.assertIn(rule, csp)

if __name__ == '__main__': unittest.main()
