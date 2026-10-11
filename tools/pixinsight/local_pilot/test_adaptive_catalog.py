"""Candidate graph regressions: scientific prerequisites and hostile outputs."""
import copy
import unittest

from .adaptive_catalog import VERSION, fingerprint, validate_graph, validate_checkpoint_decision
from .broker import ProtocolError


def facts():
    return {'domain': 'LINEAR_ATTESTED', 'sourceSha256': 'a' * 64, 'recordSha256': 'b' * 64,
            'registration': 'VERIFIED', 'backgroundROI': 'VERIFIED', 'stellarPSF': 'VERIFIED',
            'runtime': 'VERIFIED', 'mask': 'VERIFIED'}


def graph():
    return {'catalog': VERSION, 'catalogSha256': fingerprint(), 'branch': 'DIRECT',
            'steps': [{'process': 'DECONVOLVE', 'parameters': {'sharpenL': .18, 'sharpenRGB': .08}},
                      {'process': 'DENOISE', 'parameters': {'denoiseL': .4, 'denoiseRGB': .3}},
                      {'process': 'STRETCH', 'parameters': {'targetBackground': .08}}],
            'rationale': 'Ipotesi da confrontare sui checkpoint.',
            'limitations': 'La resa non dimostra recupero di dettaglio reale.'}


class CatalogTests(unittest.TestCase):
    def test_two_graphs_are_distinct_and_inputs_are_not_mutated(self):
        direct = graph()
        starless = copy.deepcopy(direct)
        starless['branch'] = 'STARLESS'
        starless['steps'].insert(2, {'process': 'SEPARATE', 'parameters': {}})
        starless['steps'].append({'process': 'RECOMBINE', 'parameters': {}})
        for mode in ('LRGB', 'OSC', 'SHO', 'HOO'):
            self.assertEqual(validate_graph(direct, mode, facts()), direct)
            self.assertEqual(validate_graph(starless, mode, facts()), starless)
        detached = validate_graph(direct, 'LRGB', facts())
        detached['steps'].clear()
        self.assertEqual(len(direct['steps']), 3)

    def test_whole_field_statistics_cannot_attest_linearity_or_psf(self):
        for key, missing in [('domain', 'NOT_ESTABLISHED'), ('domain', 'NONLINEAR_ATTESTED'),
                             ('stellarPSF', 'NOT_ESTABLISHED'), ('registration', 'NOT_ESTABLISHED'),
                             ('runtime', 'NOT_ESTABLISHED')]:
            value = facts()
            value[key] = missing
            with self.subTest(key=key, missing=missing), self.assertRaises(ProtocolError):
                validate_graph(graph(), 'LRGB', value)

    def test_isolated_denoise_requires_an_explicit_supported_domain(self):
        value = graph()
        value['steps'] = [value['steps'][1]]
        unknown = facts()
        unknown['domain'] = 'NOT_ESTABLISHED'
        with self.assertRaisesRegex(ProtocolError, 'ATTESTED_DOMAIN_REQUIRED'):
            validate_graph(value, 'LRGB', unknown)
        for domain in ('LINEAR_ATTESTED', 'NONLINEAR_ATTESTED'):
            known = facts()
            known['domain'] = domain
            self.assertEqual(validate_graph(value, 'LRGB', known), value)

    def test_order_duplicates_unknown_processes_and_code_are_rejected(self):
        values = []
        reordered = graph()
        reordered['steps'][0:2] = reversed(reordered['steps'][0:2])
        values.append(reordered)
        duplicated = graph()
        duplicated['steps'].insert(0, copy.deepcopy(duplicated['steps'][0]))
        values.append(duplicated)
        injected = graph()
        injected['steps'][0]['expression'] = '$T'
        values.append(injected)
        unknown = graph()
        unknown['steps'][0]['process'] = 'ExecuteScript'
        values.append(unknown)
        for value in values:
            with self.assertRaises(ProtocolError):
                validate_graph(value, 'LRGB', facts())

    def test_palette_and_mask_domain_are_not_guessed(self):
        color = graph()
        color['steps'].insert(0, {'process': 'COLOR', 'parameters': {}})
        for mode in ('SHO', 'HOO'):
            with self.assertRaisesRegex(ProtocolError, 'PALETTE'):
                validate_graph(color, mode, facts())
        contrast = graph()
        contrast['steps'].append({'process': 'LOCAL_CONTRAST', 'parameters': {'contrastLarge': .2, 'contrastSmall': .1}})
        missing = facts()
        missing['mask'] = 'NOT_ESTABLISHED'
        with self.assertRaisesRegex(ProtocolError, 'MASK'):
            validate_graph(contrast, 'LRGB', missing)
        contrast['steps'].pop(2)
        with self.assertRaisesRegex(ProtocolError, 'NONLINEAR'):
            validate_graph(contrast, 'LRGB', facts())

    def test_nonfinite_boolean_and_outside_parameters_are_rejected(self):
        for bad in (True, float('nan'), float('inf'), -.01, .61, '0.18'):
            value = graph()
            value['steps'][0]['parameters']['sharpenL'] = bad
            with self.subTest(bad=bad), self.assertRaises(ProtocolError):
                validate_graph(value, 'LRGB', facts())

    def test_branch_and_catalog_cannot_be_substituted(self):
        value = graph()
        value['branch'] = 'STARLESS'
        with self.assertRaisesRegex(ProtocolError, 'DEPENDENCIES'):
            validate_graph(value, 'LRGB', facts())
        value = graph()
        value['catalogSha256'] = 'c' * 64
        with self.assertRaisesRegex(ProtocolError, 'CATALOG_BINDING'):
            validate_graph(value, 'LRGB', facts())

    def test_checkpoint_decision_cannot_rebind_or_revise_graph(self):
        decision = {'action': 'CONTINUE', 'bindingSha256': 'a' * 64,
                    'rationale': 'Confronto limitato al checkpoint.', 'limitations': 'Nessuna accettazione automatica.'}
        self.assertEqual(validate_checkpoint_decision(decision, 'a' * 64), decision)
        for changed in ({**decision, 'bindingSha256': 'b' * 64}, {**decision, 'steps': []},
                        {**decision, 'action': 'EXECUTE'}, {**decision, 'rationale': 'https://unsafe.example'}):
            with self.assertRaises(ProtocolError):
                validate_checkpoint_decision(changed, 'a' * 64)


if __name__ == '__main__':
    unittest.main()
