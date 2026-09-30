"""Synthetic F3 lexical/evidence contract tests; never private scientific inputs."""
from copy import deepcopy
import json
import unittest

from .archive import ArchiveError, build_packet, digest, encode
from .provenance import build_sidecar, validate_emitted_profile

STAMP = '2026-09-30T18:00:00Z'
SOURCE = b'''var Root=new ProcessContainer;
var Group=new ProcessContainer;
var A=new PixelMath;A.expression="neverExecute();";A.n=+0.1200E-03;
A.mode=PixelMath.SameAsTarget;A.table=[[true,null],[0.25,false]];
Group.add(A);var B=new StarXTerminator;B.ml_version=0;
Group.add(B);Group.setMask(0,"SYNTHETIC_MASK");Group.invertMask(0);Root.add(Group);
'''


def sample():
    packet = build_packet(SOURCE, 'BKL049-SYNTHETIC-F3', STAMP)
    declaration = {'declaredBy': 'SYNTHETIC_OPERATOR', 'declaredAt': '2026-09-30T18:01:00Z',
                   'scope': 'EXPORTED_CONFIGURATIONS_ONLY', 'sourceSha256': digest(SOURCE)}
    return packet, declaration


def sidecar_for(packet, declaration):
    raw = encode(packet)
    return build_sidecar(raw, digest(raw), declaration, exported_at='2026-09-30T18:02:00Z')


class ProvenanceTests(unittest.TestCase):
    def test_order_lexical_values_and_distinct_clocks(self):
        packet, declaration = sample(); original = deepcopy(packet)
        sidecar = sidecar_for(packet, declaration)
        self.assertEqual(packet, original)
        steps = sidecar['workflow']['steps']
        self.assertEqual([s['processId'] for s in steps], ['PixelMath', 'StarXTerminator'])
        self.assertEqual([s['ordinal'] for s in steps], [1, 2])
        self.assertEqual(steps[0]['parameters']['bkl049LexicalV1']['exportParameters'], packet['archive']['instances']['A']['parameters'])
        self.assertEqual(steps[0]['parameters']['bkl049LexicalV1']['containerPath'], ['Root', 'Group'])
        self.assertEqual(sidecar['exportedAt'], '2026-09-30T18:02:00Z')
        self.assertEqual(steps[0]['declaredAt'], declaration['declaredAt'])
        self.assertIsNone(steps[0]['capturedAt'])
        self.assertIsNone(sidecar['workflow']['startedAt'])

    def test_no_observed_promotion_or_binding_inference(self):
        packet, declaration = sample(); s = sidecar_for(packet, declaration)
        self.assertEqual(s['capture']['completeness'], 'PARTIAL')
        self.assertEqual(s['capture']['observedStepCount'], 0)
        self.assertTrue(all(x['evidenceClass'] == 'DECLARED' for x in s['workflow']['steps']))
        self.assertTrue(all(x['maskRefs'] == [] for x in s['workflow']['steps']))
        self.assertEqual(s['workflow']['outputs'], [])
        self.assertEqual(s['observationContext'], {'sessionId': 'unknown', 'target': 'unknown'})
        self.assertEqual(len(packet['archive']['instances']['Group']['maskCommands']), 2)
        self.assertEqual(s['workflow']['steps'][1]['processVersion'], None)

    def test_declaration_is_bound_to_exact_source(self):
        packet, declaration = sample()
        for change in [{'scope':'OBSERVED'}, {'sourceSha256':'0'*64}, {'declaredBy':''},
                       {'declaredAt':'2026-09-30'}, {'declaredAt':'2026-02-30T00:00:00Z'}, {'extra':'private'}]:
            invalid = {**declaration, **change}
            with self.subTest(change=change), self.assertRaises(ArchiveError):
                sidecar_for(packet, invalid)
        for key in declaration:
            invalid = dict(declaration); del invalid[key]
            with self.subTest(missing=key), self.assertRaises(ArchiveError):
                sidecar_for(packet, invalid)

    def test_context_limits_and_no_truncation(self):
        packet, declaration = sample()
        for field, maximum in [('sessionId',128), ('target',256), ('productVersion',64), ('declaredBy',256)]:
            valid = {**declaration, field:'x'*maximum}
            self.assertTrue(validate_emitted_profile(sidecar_for(packet, valid)))
            with self.subTest(field=field), self.assertRaises(ArchiveError):
                sidecar_for(packet, {**valid, field:'x'*(maximum+1)})
        with self.assertRaises(ArchiveError):
            sidecar_for(packet, {**declaration,'productVersion':'😀'*64})

    def test_unsupported_source_and_wrong_packet_digest_rejected(self):
        packet, declaration = sample()
        bad = build_packet(SOURCE + b'Root.executeGlobal();', 'BKL049-BAD', STAMP)
        with self.assertRaisesRegex(ArchiveError,'SOURCE_UNSUPPORTED'):
            sidecar_for(bad, declaration)
        with self.assertRaisesRegex(ArchiveError,'PACKET_INTEGRITY'):
            build_sidecar(encode(packet), '0'*64, declaration, exported_at=STAMP)

    def test_empty_supported_export_is_unavailable(self):
        source=b'var P=new ProcessContainer;'
        p=build_packet(source, 'BKL049-EMPTY', STAMP)
        _, d=sample(); d['sourceSha256']=digest(source)
        s=sidecar_for(p,d)
        self.assertEqual(s['capture']['completeness'],'UNAVAILABLE')
        self.assertEqual(s['workflow']['steps'],[])

    def test_export_time_cannot_precede_import_or_attestation(self):
        packet, declaration=sample()
        with self.assertRaisesRegex(ArchiveError,'EXPORT_TIME_CONFLICT'):
            build_sidecar(encode(packet),digest(encode(packet)),declaration,exported_at=STAMP)

    def test_schema_constraints_reject_invalid_emitted_fields(self):
        packet, declaration=sample(); s=sidecar_for(packet,declaration)
        cases=[]
        x=deepcopy(s);x['source']['unexpected']='private';cases.append(x)
        x=deepcopy(s);x['workflow']['steps'][0]['ordinal']=True;cases.append(x)
        x=deepcopy(s);x['workflow']['steps'][0]['processId']='x'*257;cases.append(x)
        x=deepcopy(s);x['capture']['observedStepCount']=-1;cases.append(x)
        x=deepcopy(s);x['authority']='catalog';cases.append(x)
        x=deepcopy(s);x['workflow']['steps'][0]['evidenceClass']='SUGGESTED';cases.append(x)
        x=deepcopy(s);del x['source']['hostId'];cases.append(x)
        for index, value in enumerate(cases):
            with self.subTest(index=index),self.assertRaises(ArchiveError):
                validate_emitted_profile(value)
        with self.assertRaisesRegex(ArchiveError,'PROFILE_SCHEMA_UNSUPPORTED'):
            validate_emitted_profile(s, {'type':'object','futureKeyword':True})

    def test_repeat_is_deterministic(self):
        packet,declaration=sample()
        self.assertEqual(encode(sidecar_for(packet,declaration)),encode(sidecar_for(packet,declaration)))


if __name__ == '__main__':
    unittest.main()
