"""Bounded sibling experiments; executable capabilities never come from prose.

The research controller is separate from the historical V2 graph contract.
An Owner approval binds the installed runtime, source set and initial evidence.
"""
import copy
import re
from .broker import require, encode
from .intake import sha
from .adaptive_catalog import validate_step
from .openai_planner import safe_text, object_schema

VERSION = 'DSG_PIAI_RESEARCH_V1'
STAGES = ('CALIBRATION', 'DETAIL', 'NOISE', 'STRETCH', 'COMBINE', 'PRESENTATION', 'FINAL')
PROCESSES = {'CALIBRATION': ('SPCC',), 'DETAIL': ('OPTICAL_CORRECT', 'DECONVOLVE'),
             'NOISE': ('DENOISE',), 'STRETCH': ('STRETCH',), 'COMBINE': ('COMBINE',),
             'PRESENTATION': ('VIVIDNESS',), 'FINAL': ()}
MAX_CALLS = 32
MAX_TRIALS = 16


def digest(value):
    return isinstance(value, str) and re.fullmatch('[a-f0-9]{64}', value) is not None


def checkpoint_id(value):
    return isinstance(value, str) and re.fullmatch('CP[0-9]{3}', value) is not None


def fingerprint():
    return sha({'version': VERSION, 'stages': STAGES, 'processes': PROCESSES,
                'calls': MAX_CALLS, 'trials': MAX_TRIALS,
                'trialsPerStage':3,
                'mode': 'LRGB', 'sampling': 'ORIGINAL',
                'comparison': 'EXACT_PARENT_CONTROL_SIBLINGS',
                'spcc': 'EXPLICIT_NOMINAL_FILTERS_QE_WHITE_AND_NATIVE_FIT',
                'selection': 'MODEL_CHOOSES_FROM_PHYSICALLY_VERIFIED_CHECKPOINTS',
                'acceptance': 'OWNER_PRIVATE_REVIEW_ONLY'})


def policy(analysis_sha, runtime_sha, knowledge_sha):
    require(all(digest(x) for x in (analysis_sha, runtime_sha, knowledge_sha)), 'RESEARCH_POLICY_HASHES')
    return {'version': VERSION, 'catalogSha256': fingerprint(), 'analysisSha256': analysis_sha,
            'runtimeSha256': runtime_sha, 'knowledgeSha256': knowledge_sha,
            'mode': 'LRGB', 'sampling': 'ORIGINAL', 'maxApiCalls': MAX_CALLS,
            'maxNativeTrials': MAX_TRIALS, 'processes': {k:list(v) for k,v in PROCESSES.items()},
            'maxTrialsPerStage':3,
            'adaptationScope': 'BOUNDED_SIBLING_TRIALS_AND_SELECTION',
            'finalAcceptance': 'OWNER_REQUIRED', 'publication': 'NONE'}


def step(value):
    require(isinstance(value, dict) and set(value) == {'process', 'parameters'}, 'RESEARCH_STEP_FIELDS')
    if value['process'] == 'SPCC':
        require(value['parameters'] == {}, 'RESEARCH_SPCC_PINNED_PROFILE')
    elif value['process'] == 'VIVIDNESS':
        p = value['parameters']
        require(isinstance(p, dict) and set(p) == {'saturation'} and
                type(p['saturation']) in (int, float) and 0 <= p['saturation'] <= .25,
                'RESEARCH_VIVIDNESS_BOUND')
    else:
        validate_step(value)
    encode(value)
    return copy.deepcopy(value)


def decide(value, state):
    require(isinstance(value, dict) and set(value) ==
            {'action', 'bindingSha256', 'parentId', 'checkpointId', 'step', 'rationale', 'limitations'},
            'RESEARCH_DECISION_FIELDS')
    require(value['bindingSha256'] == sha(state), 'RESEARCH_DECISION_CHANGED')
    safe_text(value['rationale']); safe_text(value['limitations'])
    require(len(value['rationale'].encode('utf-8')) <= 1500 and len(value['limitations'].encode('utf-8')) <= 1500,
            'RESEARCH_DECISION_TEXT_LIMIT')
    require(value['action'] in ('TEST', 'SELECT', 'FINISH', 'STOP'), 'RESEARCH_ACTION')
    stage = state['stage']; parent = state['selectedId']; nodes = state['checkpoints']
    require(stage in STAGES and parent in nodes, 'RESEARCH_STATE')
    if value['action'] == 'TEST':
        require(stage != 'FINAL' and value['parentId'] == parent and value['checkpointId'] is None,
                'RESEARCH_EXACT_PARENT_REQUIRED')
        candidate = step(value['step'])
        require(candidate['process'] in PROCESSES[stage], 'RESEARCH_STAGE_PROCESS')
        require(state['nativeTrials'] < MAX_TRIALS, 'RESEARCH_TRIAL_LIMIT')
        # The calibration and fusion stages are fixed operations, not repeated paid/native searches.
        siblings = [n for n in nodes.values() if n.get('parentId') == parent and n.get('stage') == stage]
        require(len(siblings) < 3, 'RESEARCH_STAGE_TRIAL_LIMIT')
        require(stage not in ('CALIBRATION', 'COMBINE') or not siblings, 'RESEARCH_FIXED_STAGE_ALREADY_TESTED')
        require(not any(n.get('step') == candidate for n in siblings), 'RESEARCH_IDENTICAL_TRIAL_REPLAY')
    elif value['action'] == 'SELECT':
        require(stage != 'FINAL' and value['parentId'] == parent and value['step'] is None,
                'RESEARCH_SELECTION_FIELDS')
        target = value['checkpointId']
        require(checkpoint_id(target) and target in nodes and nodes[target].get('verified') is True, 'RESEARCH_VERIFIED_SELECTION')
        if target == parent:
            require(stage in ('DETAIL', 'NOISE', 'PRESENTATION'), 'RESEARCH_REQUIRED_STAGE')
        else:
            require(nodes[target].get('parentId') == parent and nodes[target].get('stage') == stage,
                    'RESEARCH_SIBLING_REQUIRED')
            if stage == 'CALIBRATION':
                require(digest(nodes[target].get('photometricReceiptSha256')) and
                        nodes[target].get('photometry', {}).get('status') == 'NATIVE_FIT_INSPECTABLE' and
                        nodes[target].get('photometry', {}).get('whiteReferenceInsideFitRange') ==
                            'INSIDE_EXPORTED_RANGE_FROM_ROUNDED_NATIVE_PRODUCTS',
                        'RESEARCH_NATIVE_SPCC_RECEIPT_REQUIRED')
    else:
        require(value['parentId'] == parent and value['checkpointId'] is None and value['step'] is None,
                'RESEARCH_TERMINAL_FIELDS')
        if value['action'] == 'FINISH':
            require(stage == 'FINAL' and nodes[parent]['domain'] == 'NONLINEAR_ATTESTED',
                    'RESEARCH_FINAL_PREFIX_REQUIRED')
    return copy.deepcopy(value)


def schema(state):
    binding,stage,parent=sha(state),state['stage'],state['selectedId']
    require(digest(binding) and stage in STAGES, 'RESEARCH_SCHEMA_BINDING')
    require(checkpoint_id(parent) and parent in state['checkpoints'],'RESEARCH_SCHEMA_PARENT')
    from .adaptive_provider import graph_schema
    from .broker import ProtocolError
    targets=[]
    for target in state['checkpoints']:
        try:
            decide({'action':'SELECT','bindingSha256':binding,'parentId':parent,
                    'checkpointId':target,'step':None,'rationale':'Schema','limitations':'Schema'},state)
        except ProtocolError:continue
        targets.append(target)
    siblings=[n for n in state['checkpoints'].values() if n.get('parentId') == parent and n.get('stage') == stage]
    can_test=(stage != 'FINAL' and state['nativeTrials'] < MAX_TRIALS and len(siblings) < 3 and
              (stage not in ('CALIBRATION','COMBINE') or not siblings))
    actions=(['TEST'] if can_test else [])+(['SELECT'] if targets else [])
    if stage == 'FINAL' and state['checkpoints'][parent]['domain'] == 'NONLINEAR_ATTESTED':actions.append('FINISH')
    actions.append('STOP')
    variants = graph_schema()['properties']['steps']['items']['anyOf']
    selected = [v for v in variants if v['properties']['process']['enum'][0] in PROCESSES[stage]]
    if stage == 'CALIBRATION':
        selected.append(object_schema({'process': {'type': 'string', 'enum': ['SPCC']},
                                       'parameters': object_schema({})}))
    if stage == 'PRESENTATION':
        selected.append(object_schema({'process': {'type': 'string', 'enum': ['VIVIDNESS']},
                                       'parameters': object_schema({'saturation': {'type': 'number'}})}))
    return object_schema({'action': {'type': 'string', 'enum': actions},
                          'bindingSha256': {'type': 'string', 'enum': [binding]},
                          'parentId': {'type': 'string','enum':[parent],
                                       'description':'Exact existing parent. Never invent or replace this ID.'},
                          'checkpointId': {'type': ['string', 'null'],'enum':targets+[None],
                                           'description':'Null for TEST, STOP and FINISH. SELECT uses an admitted verified checkpoint.'},
                          'step': {'anyOf': (selected if can_test else []) + [{'type': 'null'}]},
                          'rationale': {'type': 'string'}, 'limitations': {'type': 'string'}})
