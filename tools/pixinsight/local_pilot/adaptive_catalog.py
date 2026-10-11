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
PROCESS_ORDER = ('BACKGROUND', 'OPTICAL_CORRECT', 'COLOR', 'DECONVOLVE', 'DENOISE', 'SEPARATE',
                 'STRETCH', 'MASK_BUILD', 'LOCAL_CONTRAST', 'COMBINE', 'RECOMBINE')
# Bounds are inherited from the reviewed V1 native implementation, not claimed
# to be scientifically optimal thresholds. The V2 executor is a separate gate.
PARAMETERS = {
    'BACKGROUND': {'polyDegree': (0, 2, int), 'boxSize': (5, 32, int), 'boxSeparation': (5, 64, int)},
    'OPTICAL_CORRECT': {},
    'COLOR': {},
    'DECONVOLVE': {'sharpenL': (0, .6, float), 'sharpenRGB': (0, .55, float)},
    'DENOISE': {'denoiseL': (.3, .85, float), 'denoiseRGB': (.3, .85, float)},
    'SEPARATE': {},
    'STRETCH': {'targetBackground': (.03, .12, float)},
    'MASK_BUILD': {'maskLow': (0, .5, float), 'maskHigh': (.05, 1, float)},
    'LOCAL_CONTRAST': {'contrastLarge': (0, .4, float), 'contrastSmall': (0, .4, float)},
    'COMBINE': {}, 'RECOMBINE': {},
}
ATTESTED_DOMAINS = ('LINEAR_ATTESTED', 'NONLINEAR_ATTESTED')
DOMAIN_RULES = {k: ('LINEAR_ATTESTED',) for k in ('BACKGROUND', 'OPTICAL_CORRECT', 'COLOR', 'DECONVOLVE', 'STRETCH')}
DOMAIN_RULES.update({k: ('NONLINEAR_ATTESTED',) for k in ('MASK_BUILD', 'LOCAL_CONTRAST', 'COMBINE', 'RECOMBINE')})
DOMAIN_RULES.update({k: ATTESTED_DOMAINS for k in ('DENOISE', 'SEPARATE')})
FACT_RULES = {'BACKGROUND': 'backgroundROI', 'COLOR': 'backgroundROI',
              'OPTICAL_CORRECT': 'stellarPSF', 'DECONVOLVE': 'stellarPSF', 'LOCAL_CONTRAST': 'mask'}


def fingerprint():
    return sha({'version': VERSION, 'order': PROCESS_ORDER,
                'initialDomains': ATTESTED_DOMAINS, 'domainRules': DOMAIN_RULES, 'factRules': FACT_RULES,
                'commonFacts': ['registration', 'runtime'], 'colorModes': ['LRGB', 'OSC'],
                'colorMeaning': 'EMPIRICAL_NATIVE_COLORCALIBRATION_NOT_SPCC',
                'opticalMeaning': 'BLURX_CORRECT_ONLY_LINEAR',
                'transition': {'STRETCH': 'NONLINEAR_ATTESTED'},
                'maskPlanning': 'MASK_BUILD_CONDITIONAL_NATIVE_VERIFICATION_BEFORE_LOCAL_CONTRAST',
                'checkpointScope': 'NEXT_STEP_PARAMETERS_ONLY',
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
    require(facts['domain'] in ATTESTED_DOMAINS, 'ADAPTIVE_ATTESTED_DOMAIN_REQUIRED')
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
        validate_step(step)
        process = step['process']
        ids.append(process)
    require(len(set(ids)) == len(ids) and ids == sorted(ids, key=PROCESS_ORDER.index), 'ADAPTIVE_GRAPH_ORDER')
    require(facts['runtime'] == 'VERIFIED' and facts['registration'] == 'VERIFIED', 'ADAPTIVE_RUNTIME_OR_REGISTRATION')
    domain = facts['domain']
    mask_planned = False
    for process in ids:
        if process in DOMAIN_RULES:
            allowed = DOMAIN_RULES[process]
            code = 'ADAPTIVE_LINEAR_REQUIRED' if allowed == ('LINEAR_ATTESTED',) else (
                'ADAPTIVE_NONLINEAR_REQUIRED' if allowed == ('NONLINEAR_ATTESTED',) else 'ADAPTIVE_ATTESTED_DOMAIN_REQUIRED')
            require(domain in allowed, code)
        if process in FACT_RULES:
            key = FACT_RULES[process]
            require(facts[key] == 'VERIFIED' or (key == 'mask' and mask_planned), {'backgroundROI': 'ADAPTIVE_BACKGROUND_REQUIRED',
                    'stellarPSF': 'ADAPTIVE_PSF_REQUIRED', 'mask': 'ADAPTIVE_MASK_REQUIRED'}[key])
        if process == 'COLOR':
            require(mode in {'LRGB', 'OSC'}, 'ADAPTIVE_PALETTE_NOT_PHOTOMETRY')
        if process == 'STRETCH':
            domain = 'NONLINEAR_ATTESTED'
        if process == 'MASK_BUILD':
            # Planning dependency only. Never changes the caller's facts.
            mask_planned = True
    if value['branch'] == 'STARLESS':
        require(all(process in ids for process in ('SEPARATE', 'STRETCH', 'RECOMBINE')) and
                ids.index('SEPARATE') < ids.index('STRETCH'), 'ADAPTIVE_STARLESS_DEPENDENCIES')
    else:
        require('SEPARATE' not in ids and 'RECOMBINE' not in ids, 'ADAPTIVE_DIRECT_DEPENDENCIES')
    # Canonical JSON also rejects NaN/Infinity. This graph is still not a receipt.
    encode(value)
    return copy.deepcopy(value)


def validate_step(value):
    require(isinstance(value, dict) and set(value) == {'process', 'parameters'}, 'ADAPTIVE_STEP_FIELDS')
    process = value['process']
    require(isinstance(process, str) and process in PARAMETERS, 'ADAPTIVE_PROCESS')
    bounds = PARAMETERS[process]
    require(isinstance(value['parameters'], dict) and set(value['parameters']) == set(bounds), 'ADAPTIVE_PARAMETERS')
    for name, (lo, hi, kind) in bounds.items():
        number = value['parameters'][name]
        require(type(number) is int if kind is int else type(number) in (int, float), 'ADAPTIVE_PARAMETER_TYPE')
        require(lo <= number <= hi, 'ADAPTIVE_PARAMETER_BOUND')
    if process == 'MASK_BUILD':
        require(value['parameters']['maskHigh']-value['parameters']['maskLow'] >= .05, 'ADAPTIVE_MASK_RANGE')
    encode(value)
    return copy.deepcopy(value)


def validate_dispatch(value, mode, current_facts):
    """Actual execution gate: a planned future mask never satisfies it."""
    step = validate_step(value); facts = provenance(current_facts)
    require(isinstance(mode, str) and mode in MODES, 'ADAPTIVE_MODE')
    require(facts['domain'] in ATTESTED_DOMAINS and facts['runtime'] == 'VERIFIED' and
            facts['registration'] == 'VERIFIED', 'ADAPTIVE_DISPATCH_ATTESTATIONS')
    process = step['process']
    require(facts['domain'] in DOMAIN_RULES[process], 'ADAPTIVE_DISPATCH_DOMAIN')
    if process in FACT_RULES:
        require(facts[FACT_RULES[process]] == 'VERIFIED', 'ADAPTIVE_DISPATCH_PHYSICAL_FACT_REQUIRED')
    if process == 'COLOR':
        require(mode in {'LRGB', 'OSC'}, 'ADAPTIVE_PALETTE_NOT_PHOTOMETRY')
    return step


def validate_next_decision(value, binding, graph, mode, initial_facts, current_facts, completed):
    """Only next-step parameters may change. Caller verifies native receipts."""
    graph = validate_graph(graph, mode, initial_facts)
    initial_facts = provenance(initial_facts); current_facts = provenance(current_facts)
    require(current_facts['sourceSha256'] == initial_facts['sourceSha256'], 'ADAPTIVE_SOURCE_SET_CHANGED')
    require(type(completed) is int and 1 <= completed <= len(graph['steps']), 'ADAPTIVE_COMPLETED_PREFIX')
    fields = {'action', 'bindingSha256', 'nextStep', 'rationale', 'limitations'}
    require(isinstance(value, dict) and set(value) == fields and isinstance(binding, str) and
            re.fullmatch('[a-f0-9]{64}', binding) and value['bindingSha256'] == binding, 'ADAPTIVE_NEXT_DECISION_BINDING')
    safe_text(value['rationale']); safe_text(value['limitations'])
    action = value['action']
    if action == 'CONTINUE':
        require(completed < len(graph['steps']) and isinstance(value['nextStep'], dict) and
                value['nextStep'].get('process') == graph['steps'][completed]['process'], 'ADAPTIVE_NEXT_STEP_ONLY')
        validate_dispatch(value['nextStep'], mode, current_facts)
    elif action == 'COMPLETE_FOR_REVIEW':
        require(completed == len(graph['steps']) and value['nextStep'] is None, 'ADAPTIVE_COMPLETE_PREFIX_REQUIRED')
        require(current_facts['runtime'] == 'VERIFIED' and current_facts['registration'] == 'VERIFIED',
                'ADAPTIVE_COMPLETION_ATTESTATIONS')
    else:
        require(action == 'STOP_FOR_REVIEW' and value['nextStep'] is None, 'ADAPTIVE_NEXT_ACTION')
    if action in ('CONTINUE', 'COMPLETE_FOR_REVIEW'):
        expected_domain = initial_facts['domain']
        if any(step['process'] == 'STRETCH' for step in graph['steps'][:completed]):
            expected_domain = 'NONLINEAR_ATTESTED'
        require(current_facts['domain'] == expected_domain, 'ADAPTIVE_PREFIX_DOMAIN_MISMATCH')
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
