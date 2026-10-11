"""One reserved Responses function call; no provider/native retries."""
import re
from .broker import require, encode, decode
from .intake import sha
from .openai_planner import safe_text
from .image_previews import provider_image
from .research_knowledge import instructions
from . import research_contract as contract


def generate(provider, state, projection, assets, *, owner, knowledge_sha256):
    require(isinstance(owner, str) and contract.digest(owner) and owner not in provider._sent,
            'RESEARCH_SINGLE_RESERVED_SEND')
    require(state['apiCalls'] <= contract.MAX_CALLS and state['status'] == 'API_RESERVED',
            'RESEARCH_API_RESERVATION_REQUIRED')
    require(isinstance(projection, dict) and set(projection) ==
            {'intent', 'stage', 'selectedId', 'checkpoints', 'instrument', 'comparisonLimitations'},
            'RESEARCH_PROJECTION_FIELDS')
    safe_text(projection['intent'])
    require(projection['stage'] == state['stage'] and projection['selectedId'] == state['selectedId'] and
            len(encode(projection)) <= 32768, 'RESEARCH_PROJECTION_BINDING')
    guide, digest = instructions(knowledge_sha256)
    content = [{'type': 'input_text', 'text': encode(projection).decode()}]
    require(isinstance(assets, list) and len(assets) <= 16, 'RESEARCH_PREVIEW_COUNT')
    for row in assets:
        require(set(row) == {'raw', 'sha256', 'geometry', 'channels', 'label'}, 'RESEARCH_PREVIEW_FIELDS')
        require(re.fullmatch(r'(?:INITIAL_[RGBL]|(?:CONTROL|CANDIDATE)_CP[0-9]{3}_(?:RGB|L)(?:_CROP)?)',row['label']),
                'RESEARCH_PREVIEW_LABEL')
        content.append({'type': 'input_text', 'text': row['label']})
        content.append(provider_image(row['raw'], row['sha256'], expected_geometry=row['geometry'],
                                      expected_channels=row['channels']))
    payload = {'model': provider.model, 'store': False, 'max_output_tokens': 4000,
               'parallel_tool_calls': False,
               'instructions': 'Choose one bounded PixInsight experiment or selection. '
               'TEST creates a sibling of the exact selected parent, never a cumulative trial. '
               'SELECT advances the stage and may omit only optional stages. '
               'Use supplied native evidence and common-display previews; do not assert missing '
               'paired fits, photometric validity or scientific acceptance. '
               'Check SPCC fit evidence before selecting calibration. Preserve the control if '
               'a stronger setting has no supported benefit. Stop when evidence is inadequate.\n'+guide,
               'input': [{'role': 'user', 'content': content}],
               'tools': [{'type': 'function', 'name': 'choose_pixinsight_action',
                          'description': 'Request one admitted trial, select a verified sibling, finish for Owner review, or stop.',
                          'strict': True, 'parameters': contract.schema(sha(state), state['stage'])}],
               'tool_choice': {'type': 'function', 'name': 'choose_pixinsight_action'}}
    provider._sent.add(owner)
    try:
        response = provider._send(payload)
        require(isinstance(response, dict) and response.get('status') == 'completed' and
                isinstance(response.get('id'), str) and
                re.fullmatch('resp_[A-Za-z0-9_-]{1,160}', response['id']), 'RESEARCH_PROVIDER_RESPONSE')
        calls = []
        for item in response.get('output', []):
            require(isinstance(item, dict) and item.get('type') in ('reasoning', 'function_call'),
                    'RESEARCH_PROVIDER_TOOL_REQUIRED')
            if item['type'] == 'function_call':
                require(item.get('name') == 'choose_pixinsight_action' and item.get('status') == 'completed' and
                        isinstance(item.get('arguments'), str) and len(item['arguments']) <= 16384,
                        'RESEARCH_PROVIDER_TOOL')
                calls.append(item)
        require(len(calls) == 1, 'RESEARCH_PROVIDER_SINGLE_TOOL')
        decision = contract.decide(decode(calls[0]['arguments']), state)
        usage = response.get('usage')
        require(isinstance(usage, dict) and all(type(usage.get(k)) is int and usage[k] >= 0 for k in
                ('input_tokens', 'output_tokens', 'total_tokens')) and
                usage['input_tokens']+usage['output_tokens'] == usage['total_tokens'], 'RESEARCH_USAGE')
        actual_model = response.get('model')
        require(isinstance(actual_model, str) and re.fullmatch('[A-Za-z0-9][A-Za-z0-9._-]{1,119}', actual_model),
                'RESEARCH_PROVIDER_MODEL')
        return {'decision': decision, 'provider': {'responseId': response['id'], 'model': actual_model,
                'requestedModel': provider.model, 'knowledgeSha256': digest,
                'usage': {k: usage[k] for k in ('input_tokens', 'output_tokens', 'total_tokens')}}}
    except Exception:
        require(False, 'RESEARCH_PROVIDER_FAILED_NO_RETRY')
