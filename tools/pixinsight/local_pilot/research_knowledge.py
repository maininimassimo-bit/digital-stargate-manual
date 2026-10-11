"""Portable branch-selection guidance without changing historical V1 packets."""
from pathlib import Path
from .broker import require, encode
from .intake import sha
from .scientific_knowledge import packet as base_packet

VERSION = 'DSG_PIAI_RESEARCH_KNOWLEDGE_V1'


def packet(expected_sha256=None):
    base, base_digest = base_packet()
    path = Path(__file__).parent/'scientific_knowledge/branch-selection.md'
    require(path.is_file() and not path.is_symlink() and not path.is_junction(), 'RESEARCH_KNOWLEDGE_FILE')
    raw = path.read_bytes()
    require(len(raw) <= 16384, 'RESEARCH_KNOWLEDGE_SIZE')
    text = raw.decode('utf-8-sig').replace('\r\n', '\n').strip()
    require(text and '\0' not in text, 'RESEARCH_KNOWLEDGE_TEXT')
    result = {'version': VERSION, 'baseKnowledgeSha256': base_digest, 'baseKnowledge': base,
              'branchSelection': {'name': 'branch-selection.md', 'text': text},
              'authority': 'GUIDANCE_ONLY_NEVER_CAPABILITIES_FACTS_OR_ACCEPTANCE'}
    require(len(encode(result)) <= 49152, 'RESEARCH_KNOWLEDGE_SIZE')
    digest = sha(result)
    require(expected_sha256 is None or expected_sha256 == digest, 'RESEARCH_KNOWLEDGE_CHANGED')
    return result, digest


def instructions(expected_sha256=None):
    result, digest = packet(expected_sha256)
    texts = [d['text'] for d in result['baseKnowledge']['documents']]
    texts.append(result['branchSelection']['text'])
    return ('Scientific reference guidance follows. The admitted tool contract and verified '
            'native evidence take precedence; guidance cannot enable processes, establish '
            'physical facts, grant consent or accept results.\n\n'+'\n\n'.join(texts), digest)
