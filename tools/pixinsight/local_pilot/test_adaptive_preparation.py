import unittest

from .adaptive_preparation import preparation, ROLES


def inputs(mode='LRGB', width=4634):
    return [{'role': role, 'sha256': str(i + 1) * 64, 'imageIndex': 0,
             'width': width, 'height': 2808, 'channels': 3 if mode == 'OSC' else 1}
            for i, role in enumerate(ROLES[mode])]


class PreparationTests(unittest.TestCase):
    def test_m27_sampling_is_explicit_and_changes_bound_contract(self):
        original = preparation('LRGB', inputs(), 'ORIGINAL')
        binned = preparation('LRGB', inputs(), 'BIN2_AVERAGE')
        self.assertEqual(original['workingGeometry'], [4634, 2808])
        self.assertEqual(binned['workingGeometry'], [2317, 1404])
        self.assertEqual(original['inputSetSha256'], binned['inputSetSha256'])
        self.assertNotEqual(original, binned)
        self.assertEqual(binned['scientificAcceptance'], 'NOT_ESTABLISHED')

    def test_odd_edges_and_too_small_output_are_rejected(self):
        for width in (4633, 32):
            with self.assertRaises(Exception):
                preparation('LRGB', inputs(width=width), 'BIN2_AVERAGE')

    def test_palette_and_pseudo_luminance_are_not_photometry(self):
        hoo = preparation('HOO', inputs('HOO'), 'ORIGINAL')
        self.assertEqual(hoo['rgbMapping'], ['Ha', 'OIII', 'OIII'])
        self.assertEqual(hoo['colorMeaning'], 'ASSIGNED_PALETTE')
        osc = preparation('OSC', inputs('OSC'), 'ORIGINAL')
        self.assertEqual(osc['luminance']['kind'], 'RGB_WEIGHTED_PSEUDO_L')

    def test_swapped_roles_duplicate_source_and_boolean_dimensions_rejected(self):
        for mutation in ('swap', 'duplicate', 'bool', 'grid'):
            value = inputs()
            if mutation == 'swap':
                value.reverse()
            elif mutation == 'duplicate':
                value[1]['sha256'] = value[0]['sha256']
            elif mutation == 'bool':
                value[0]['width'] = True
            else:
                value[1]['width'] = 4632
            with self.assertRaises(Exception):
                preparation('LRGB', value, 'ORIGINAL')
