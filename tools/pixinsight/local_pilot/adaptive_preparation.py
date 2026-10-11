"""Candidate explicit preparation contract; does not execute or approve pixels.

Sampling is an Owner-reviewed choice, never an inferred consequence of FWHM.
The prepared baseline must be measured before any graph step comparison.
"""
from .broker import require
from .intake import sha

VERSION = 'DSG_PIAI_ADAPTIVE_PREPARATION_V2'
ROLES = {'LRGB': ('R', 'G', 'B', 'L'), 'OSC': ('RGB',),
         'SHO': ('SII', 'Ha', 'OIII'), 'HOO': ('Ha', 'OIII')}


def preparation(mode, inputs, sampling):
    require(isinstance(mode, str) and mode in ROLES, 'ADAPTIVE_PREPARATION_MODE')
    require(isinstance(sampling, str) and sampling in {'ORIGINAL', 'BIN2_AVERAGE'},
            'ADAPTIVE_PREPARATION_SAMPLING')
    require(isinstance(inputs, list) and len(inputs) == len(ROLES[mode]),
            'ADAPTIVE_PREPARATION_INPUTS')
    fields = {'role', 'sha256', 'imageIndex', 'width', 'height', 'channels'}
    for item, role in zip(inputs, ROLES[mode]):
        require(isinstance(item, dict) and set(item) == fields and item['role'] == role,
                'ADAPTIVE_PREPARATION_INPUT_FIELDS')
        require(isinstance(item['sha256'], str) and len(item['sha256']) == 64 and
                all(c in '0123456789abcdef' for c in item['sha256']), 'ADAPTIVE_PREPARATION_HASH')
        require(type(item['imageIndex']) is int and 0 <= item['imageIndex'] <= 15,
                'ADAPTIVE_PREPARATION_INDEX')
        require(all(type(item[k]) is int and 32 <= item[k] <= 12000 for k in ('width', 'height'))
                and type(item['channels']) is int and item['channels'] == (3 if mode == 'OSC' else 1),
                'ADAPTIVE_PREPARATION_GEOMETRY')
    require(len({(i['sha256'], i['imageIndex']) for i in inputs}) == len(inputs),
            'ADAPTIVE_PREPARATION_DUPLICATE')
    geometry = inputs[0]['width'], inputs[0]['height']
    require(all((i['width'], i['height']) == geometry for i in inputs),
            'ADAPTIVE_PREPARATION_COMMON_GRID')
    factor = 2 if sampling == 'BIN2_AVERAGE' else 1
    # No unverified edge-trimming semantics: unsupported odd dimensions stop.
    require(all(n % factor == 0 and n // factor >= 32 for n in geometry),
            'ADAPTIVE_PREPARATION_EXACT_BINNING_GRID')
    mappings = {'LRGB': ['R', 'G', 'B'], 'OSC': ['RGB'],
                'SHO': ['SII', 'Ha', 'OIII'], 'HOO': ['Ha', 'OIII', 'OIII']}
    luminance = ({'kind': 'SOURCE', 'role': 'L'} if mode == 'LRGB' else
                 {'kind': 'RGB_WEIGHTED_PSEUDO_L', 'weights': [.2126, .7152, .0722]}
                 if mode == 'OSC' else {'kind': 'SOURCE', 'role': 'Ha'})
    return {'version': VERSION, 'mode': mode, 'inputSetSha256': sha(inputs),
            'sampling': sampling, 'factor': factor,
            'sourceGeometry': list(geometry), 'workingGeometry': [n // factor for n in geometry],
            'sourceEdgeFromWorkingEdgeScale': factor, 'coordinateConvention': 'PIXEL_EDGES',
            'rgbMapping': mappings[mode], 'luminance': luminance,
            'colorMeaning': 'ASSIGNED_PALETTE' if mode in {'SHO', 'HOO'} else 'UNCALIBRATED_CHANNELS',
            'binningMeaning': 'AVERAGE_LOW_PASS' if factor == 2 else 'NO_RESAMPLING',
            'baselineRequired': 'NATIVE_SAVED_AND_MEASURED_BEFORE_GRAPH',
            'scientificAcceptance': 'NOT_ESTABLISHED'}
