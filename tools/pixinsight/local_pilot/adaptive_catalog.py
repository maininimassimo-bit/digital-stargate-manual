"""Candidate V2 graph contract. Validation is not native execution or acceptance.

The caller supplies attested provenance, never a model's guess about linearity.
No code, expressions, filenames or new processes are accepted from the provider.
"""
import copy
import re

from .broker import require, encode
from .intake import sha
from .openai_planner import safe_text

VERSION = 'DSG_PIAI_ADAPTIVE_CATALOG_V2'
MODES = {'LRGB', 'OSC', 'SHO', 'HOO'}
PROCESS_ORDER = ('BACKGROUND', 'COLOR', 'DECONVOLVE', 'DENOISE', 'SEPARATE',
                 'STRETCH', 'LOCAL_CONTRAST', 'COMBINE', 'RECOMBINE')
# Bounds are inherited from the reviewed V1 native implementation, not claimed
# to be scientifically optimal thresholds. The V2 executor is a separate gate.
PARAMETERS = {
    'BACKGROUND': {'polyDegree': (0, 2, int), 'boxSize': (5, 32, int), 'boxSeparation': (5, 64, int)},
    'COLOR': {},
    'DECONVOLVE': {'sharpenL': (0, .6, float), 'sharpenRGB': (0, .55, float)},
    'DENOISE': {'denoiseL': (.3, .85, float), 'denoiseRGB': (.3, .85, float)},
    'SEPARATE': {},
    'STRETCH': {'targetBackground': (.03, .12, float)},
    'LOCAL_CONTRAST': {'contrastLarge': (0, .4, float), 'contrastSmall': (0, .4, float)},
    'COMBINE': {}, 'RECOMBINE': {},
}
DOMAIN_RULES = {k: 'LINEAR_ATTESTED' for k in ('BACKGROUND', 'COLOR', 'DECONVOLVE', 'STRETCH')}
DOMAIN_RULES.update({k: 'NONLINEAR_ATTESTED' for k in ('LOCAL_CONTRAST', 'COMBINE', 'RECOMBINE')})
FACT_RULES = {'BACKGROUND': 'backgroundROI', 'COLOR': 'backgroundROI',
              'DECONVOLVE': 'stellarPSF', 'LOCAL_CONTRAST': 'mask'}


def fingerprint():
    return sha({'version': VERSION, 'order': PROCESS_ORDER,
                'domainRules': DOMAIN_RULES, 'factRules': FACT_RULES,
                'commonFacts': ['registration', 'runtime'], 'colorModes': ['LRGB', 'OSC'],
                'transition': {'STRETCH': 'NONLINEAR_ATTESTED'},
                'branches': {'DIRECT': {'forbidden': ['SEPARATE', 'RECOMBINE']},
                             'STARLESS': {'required': ['SEPARATE', 'STRETCH', 'RECOMBINE']}},
                'parameters': {key: {p: [lo, hi, kind.__name__] for p, (lo, hi, kind) in bounds.items()}
                               for key, bounds in PARAMETERS.items()}})


def provenance(value):
    """Only the worker's bound, independently recorded facts can enable steps."""
    keys = {'domain', 'sourceSha256', 'recordSha256', 'registration', 'backgroundROI',
            'stellarPSF', 'runtime', 'mask'}
    require(isinstance(value, dict) and set(value) == keys, 'ADAPTIVE_PROVENANCE_FIELDS')
    for key in ('sourceSha256', 'recordSha256'):
        require(isinstance(value[key], str) and re.fullmatch('[a-f0-9]{64}', value[key]), 'ADAPTIVE_PROVENANCE_HASH')
    require(isinstance(value['domain'], str) and value['domain'] in {'LINEAR_ATTESTED', 'NONLINEAR_ATTESTED', 'NOT_ESTABLISHED'}, 'ADAPTIVE_DOMAIN')
    for key in ('registration', 'backgroundROI', 'stellarPSF', 'runtime', 'mask'):
        require(isinstance(value[key], str) and value[key] in {'VERIFIED', 'NOT_ESTABLISHED'}, 'ADAPTIVE_FACT')
    return copy.deepcopy(value)


def validate_graph(value, mode, facts):
    """A finite graph, with conservative prerequisites; no quality assertion."""
    facts = provenance(facts)
    require(isinstance(mode, str) and mode in MODES, 'ADAPTIVE_MODE')
    require(isinstance(value, dict) and set(value) == {'catalog', 'catalogSha256', 'branch', 'steps', 'rationale', 'limitations'},
            'ADAPTIVE_GRAPH_FIELDS')
    require(value['catalog'] == VERSION and value['catalogSha256'] == fingerprint(), 'ADAPTIVE_CATALOG_BINDING')
    require(isinstance(value['branch'], str) and value['branch'] in {'DIRECT', 'STARLESS'}, 'ADAPTIVE_BRANCH')
    safe_text(value['rationale'])
    safe_text(value['limitations'])
    steps = value['steps']
    require(isinstance(steps, list) and 1 <= len(steps) <= len(PROCESS_ORDER), 'ADAPTIVE_STEPS')
    ids = []
    for step in steps:
        require(isinstance(step, dict) and set(step) == {'process', 'parameters'}, 'ADAPTIVE_STEP_FIELDS')
        process = step['process']
        require(isinstance(process, str) and process in PARAMETERS, 'ADAPTIVE_PROCESS')
        bounds = PARAMETERS[process]
        params = step['parameters']
        require(isinstance(params, dict) and set(params) == set(bounds), 'ADAPTIVE_PARAMETERS')
        for key, (lo, hi, kind) in bounds.items():
            val = params[key]
            require(type(val) is int if kind is int else type(val) in (int, float), 'ADAPTIVE_PARAMETER_TYPE')
            require(lo <= val <= hi, 'ADAPTIVE_PARAMETER_BOUND')
        ids.append(process)
    require(len(set(ids)) == len(ids) and ids == sorted(ids, key=PROCESS_ORDER.index), 'ADAPTIVE_GRAPH_ORDER')
    require(facts['runtime'] == 'VERIFIED' and facts['registration'] == 'VERIFIED', 'ADAPTIVE_RUNTIME_OR_REGISTRATION')
    domain = facts['domain']
    for process in ids:
        if process in DOMAIN_RULES:
            require(domain == DOMAIN_RULES[process], 'ADAPTIVE_LINEAR_REQUIRED' if DOMAIN_RULES[process] ==
                    'LINEAR_ATTESTED' else 'ADAPTIVE_NONLINEAR_REQUIRED')
        if process in FACT_RULES:
            key = FACT_RULES[process]
            require(facts[key] == 'VERIFIED', {'backgroundROI': 'ADAPTIVE_BACKGROUND_REQUIRED',
                    'stellarPSF': 'ADAPTIVE_PSF_REQUIRED', 'mask': 'ADAPTIVE_MASK_REQUIRED'}[key])
        if process == 'COLOR':
            require(mode in {'LRGB', 'OSC'}, 'ADAPTIVE_PALETTE_NOT_PHOTOMETRY')
        if process == 'STRETCH':
            domain = 'NONLINEAR_ATTESTED'
    if value['branch'] == 'STARLESS':
        require(all(process in ids for process in ('SEPARATE', 'STRETCH', 'RECOMBINE')) and
                ids.index('SEPARATE') < ids.index('STRETCH'), 'ADAPTIVE_STARLESS_DEPENDENCIES')
    else:
        require('SEPARATE' not in ids and 'RECOMBINE' not in ids, 'ADAPTIVE_DIRECT_DEPENDENCIES')
    # Canonical JSON also rejects NaN/Infinity. This graph is still not a receipt.
    encode(value)
    return copy.deepcopy(value)


def validate_checkpoint_decision(value, binding):
    """Decision scope is exact; a continuation cannot silently revise a graph."""
    keys = {'action', 'bindingSha256', 'rationale', 'limitations'}
    require(isinstance(value, dict) and set(value) == keys, 'ADAPTIVE_DECISION_FIELDS')
    require(isinstance(binding, str) and re.fullmatch('[a-f0-9]{64}', binding) and
            value['bindingSha256'] == binding, 'ADAPTIVE_CHECKPOINT_BINDING')
    require(isinstance(value['action'], str) and value['action'] in {'CONTINUE', 'STOP_FOR_REVIEW'}, 'ADAPTIVE_DECISION_ACTION')
    safe_text(value['rationale'])
    safe_text(value['limitations'])
    return copy.deepcopy(value)
