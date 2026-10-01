"""Synthetic public boundary checks; no real approval, gallery or cloud writes."""
from copy import deepcopy
import json
import unittest

from .archive import ArchiveError, build_packet, digest, encode
from .public_projection import build_public_projection, SCHEMA
from .provenance import validate_emitted_profile
from .test_delivery import candidate
from .test_binding import fixture
from .test_provenance import SOURCE, STAMP


def selection_for(bundle):
    value = bundle['packet']['archive']['instances']['A']['parameters']['n']
    return {'kind': 'BKL049_PRIVATE_PUBLIC_SELECTION_V1', 'scope': 'EXACT_WORKFLOW_FIELDS_ONLY',
            'deliverySha256': digest(encode(bundle)), 'approvedBy': 'SYNTHETIC_PRIVATE_APPROVER',
            'approvedAt': '2026-10-01T08:00:00Z', 'imageId': 'IMG-synthetic',
            'imageVersionId': 'VER-synthetic-1', 'workflowId': 'WF-synthetic-1',
            'steps': [{'stepId': 'step-0001', 'processId': 'PixelMath',
                       'parameters': [{'name': 'n', 'valueSha256': digest(encode(value))}]}]}


def project(bundle, selection, **changes):
    args = dict(delivery_bytes=encode(bundle), delivery_digest=digest(encode(bundle)),
                current_snapshot_digest=bundle['snapshotSha256'], selection_bytes=encode(selection),
                selection_digest=digest(encode(selection)), current_selection_digest=digest(encode(selection)))
    args.update(changes)
    return build_public_projection(**args)


class PublicProjectionTests(unittest.TestCase):
    def setUp(self):
        self.bundle = candidate()
        self.selection = selection_for(self.bundle)

    def test_explicit_fields_only_and_exact_lexical_value(self):
        before = deepcopy((self.bundle, self.selection))
        result = project(self.bundle, self.selection)
        self.assertEqual(before, (self.bundle, self.selection))
        self.assertEqual(result['steps'][0]['parameters'][0]['lexicalJson'],
                         encode(self.bundle['packet']['archive']['instances']['A']['parameters']['n']).decode())
        self.assertEqual(result['omittedStepCount'], 1)
        self.assertEqual(result['steps'][0]['omittedParameterCount'], 3)
        self.assertEqual(result['captureCompleteness'], 'PARTIAL')
        raw = encode(result)
        for private in [b'neverExecute', b'SYNTHETIC_OPERATOR', b'SYNTHETIC_PRIVATE_APPROVER',
                        b'SYNTHETIC_SESSION', b'SYNTHETIC_TARGET', b'SYNTHETIC_MASK', b'originalBase64',
                        self.bundle['packetSha256'].encode(), self.bundle['snapshotSha256'].encode(),
                        self.bundle['association']['original']['sha256'].encode()]:
            self.assertNotIn(private, raw)

    def test_schema_identifier_patterns_require_the_absolute_end(self):
        schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
        for suffix in ['\n', '\r', '\u2028', '/', '?secret', '<tag>']:
            value = project(self.bundle, self.selection)
            value['imageId'] += suffix
            with self.subTest(suffix=suffix), self.assertRaises(ArchiveError):
                validate_emitted_profile(value, schema)

    def test_no_selection_is_unavailable_not_complete(self):
        self.selection['steps'] = []
        result = project(self.bundle, self.selection)
        self.assertEqual(result['captureCompleteness'], 'UNAVAILABLE')
        self.assertEqual(result['steps'], [])
        self.assertEqual(result['omittedStepCount'], 2)

    def test_source_order_survives_reversed_selection(self):
        self.selection['steps'].insert(0, {'stepId': 'step-0002', 'processId': 'StarXTerminator', 'parameters': []})
        result = project(self.bundle, self.selection)
        self.assertEqual([s['sourceOrdinal'] for s in result['steps']], [1, 2])
        self.assertEqual(result['orderSemantics'], 'EXPORTED_CONFIGURATION_ORDER')
        self.assertEqual(result['executionEvidence'], 'NOT_ESTABLISHED')

    def test_external_trust_and_freshness_required(self):
        for override in [{'delivery_digest': '0'*64}, {'selection_digest': '0'*64},
                         {'current_snapshot_digest': '0'*64}, {'current_selection_digest': None}]:
            with self.subTest(override=override), self.assertRaises(ArchiveError):
                project(self.bundle, self.selection, **override)

    def test_changed_delivery_invalidates_old_selection(self):
        self.selection['deliverySha256'] = '0'*64
        with self.assertRaisesRegex(ArchiveError, 'PUBLIC_SELECTION_SOURCE'):
            project(self.bundle, self.selection)

    def test_parameters_need_exact_value_approval(self):
        self.selection['steps'][0]['parameters'][0]['valueSha256'] = '0'*64
        with self.assertRaisesRegex(ArchiveError, 'PUBLIC_PARAMETER_CHANGED'):
            project(self.bundle, self.selection)

    def test_unknown_and_duplicate_fields_fail_closed(self):
        mutations = [lambda s: s.update(note='DO NOT PUBLISH'),
                     lambda s: s['steps'].append(deepcopy(s['steps'][0])),
                     lambda s: s['steps'][0]['parameters'].append(deepcopy(s['steps'][0]['parameters'][0])),
                     lambda s: s['steps'][0].update(stepId='step-9999'),
                     lambda s: s['steps'][0].update(processId='OtherProcess'),
                     lambda s: s['steps'][0]['parameters'][0].update(name='absent'),
                     lambda s: s.update(approvedBy=''),
                     lambda s: s.update(approvedAt='2026-09-01T00:00:00Z'),
                     lambda s: s.update(scope='ALL_PRIVATE_FIELDS')]
        for mutate in mutations:
            selected = deepcopy(self.selection); mutate(selected)
            with self.subTest(mutate=mutate), self.assertRaises(ArchiveError):
                project(self.bundle, selected)

    def test_urls_paths_markup_and_fragments_are_not_public_ids(self):
        for bad in ['https://example.test', '//example.test', '../private', 'IMG-../private',
                    'IMG-x?token=secret', 'IMG-x#fragment', 'IMG-%2e%2e', 'IMG-<script>',
                    'IMG-'+'x'*65, 'IMG-a\n', 'C:\\private']:
            for field in ['imageId', 'imageVersionId', 'workflowId']:
                selected = deepcopy(self.selection); selected[field] = bad
                with self.subTest(value=bad, field=field), self.assertRaises(ArchiveError):
                    project(self.bundle, selected)

    def test_arbitrary_routes_and_private_notes_are_not_supported(self):
        for key in ['methodCitation', 'previewUrl', 'notes', 'sourcePath', 'html']:
            selected = deepcopy(self.selection); selected[key] = 'unreviewed'
            with self.subTest(key=key), self.assertRaises(ArchiveError):
                project(self.bundle, selected)

    def test_explicitly_approved_expression_is_inert_lexical_data(self):
        value = self.bundle['packet']['archive']['instances']['A']['parameters']['expression']
        self.selection['steps'][0]['parameters'] = [{'name': 'expression', 'valueSha256': digest(encode(value))}]
        result = project(self.bundle, self.selection)
        self.assertIn('neverExecute();', result['steps'][0]['parameters'][0]['lexicalJson'])
        self.assertEqual(result['actionAuthority'], 'NONE')

    def test_step_and_parameter_count_bounds(self):
        for field in ['steps', 'parameters']:
            selected = deepcopy(self.selection)
            if field == 'steps':
                selected['steps'] *= 513
            else:
                selected['steps'][0]['parameters'] *= 129
            with self.subTest(field=field), self.assertRaises(ArchiveError):
                project(self.bundle, selected)

    def test_noncanonical_selection_and_missing_anchor_reject(self):
        raw = encode(self.selection)
        for invalid in [raw+b' ', b'{"kind":"duplicate",'+raw[1:], b'null', b'[]', b'{']:
            with self.subTest(raw=invalid[:30]), self.assertRaises(ArchiveError):
                project(self.bundle, self.selection, selection_bytes=invalid,
                        selection_digest=digest(invalid), current_selection_digest=digest(invalid))
        with self.assertRaises(ArchiveError):
            project(self.bundle, self.selection, selection_digest=None, current_selection_digest=None)

    def test_large_approved_value_rejects_without_silent_truncation(self):
        parts = list(fixture())
        source = SOURCE.replace(b'neverExecute();', b'x'*5000)
        parts[0] = build_packet(source, parts[0]['receiptId'], STAMP)
        parts[1]['sourceSha256'] = digest(source)
        parts[4]['packetSha256'] = digest(encode(parts[0]))
        parts[4]['sourceSha256'] = digest(source)
        bundle = candidate(parts)
        selected = selection_for(bundle)
        value = bundle['packet']['archive']['instances']['A']['parameters']['expression']
        selected['steps'][0]['parameters'] = [{'name': 'expression', 'valueSha256': digest(encode(value))}]
        with self.assertRaisesRegex(ArchiveError, 'PUBLIC_VALUE_LIMIT'):
            project(bundle, selected)
        # Omitting that field preserves the complete private original.
        selected['steps'][0]['parameters'] = []
        self.assertEqual(project(bundle, selected)['steps'][0]['omittedParameterCount'], 4)

    def test_total_output_limit_rejects_many_individually_valid_values(self):
        parts = list(fixture())
        source = SOURCE.replace(b'Group.add(A);', b''.join(b'A.p%d="'%i + b'x'*4000 + b'";' for i in range(80)) + b'Group.add(A);')
        parts[0] = build_packet(source, parts[0]['receiptId'], STAMP)
        parts[1]['sourceSha256'] = digest(source)
        parts[4]['packetSha256'] = digest(encode(parts[0]))
        parts[4]['sourceSha256'] = digest(source)
        bundle = candidate(parts); selected = selection_for(bundle)
        values = bundle['packet']['archive']['instances']['A']['parameters']
        selected['steps'][0]['parameters'] = [
            {'name': 'p%d'%i, 'valueSha256': digest(encode(values['p%d'%i]))} for i in range(80)]
        with self.assertRaisesRegex(ArchiveError, 'PUBLIC_OUTPUT_LIMIT'):
            project(bundle, selected)


if __name__ == '__main__':
    unittest.main()
