"""Reviewed scientific guidance shipped to the API, independent of local skills.

Guidance cannot grant a process capability, establish a physical fact or change
an Owner approval. No local skill lookup, network fetch or user-supplied path.
"""
from pathlib import Path
from .broker import require, encode
from .intake import sha

VERSION = 'DSG_PIAI_SCIENTIFIC_KNOWLEDGE_V1'
FILES = ('principles.md', 'measurement-protocol.md', 'calibration.md', 'measurement-interpretation.md')


def packet(expected_sha256=None):
    directory = Path(__file__).parent / 'scientific_knowledge'
    documents = []
    for name in FILES:
        path = directory / name
        require(path.is_file() and not path.is_symlink() and not path.is_junction(),
                'SCIENTIFIC_KNOWLEDGE_MISSING')
        raw = path.read_bytes()
        require(len(raw) <= 16384, 'SCIENTIFIC_KNOWLEDGE_SIZE')
        text = raw.decode('utf-8-sig').replace('\r\n', '\n').strip()
        require('\x00' not in text, 'SCIENTIFIC_KNOWLEDGE_INVALID')
        documents.append({'name': name, 'text': text})
    result = {'version': VERSION, 'source': 'pixinsight-scientific skill; reviewed portable projection',
              'authority': 'GUIDANCE_ONLY_NEVER_CAPABILITIES_FACTS_OR_ACCEPTANCE',
              'documents': documents}
    require(len(encode(result)) <= 32768, 'SCIENTIFIC_KNOWLEDGE_SIZE')
    digest = sha(result)
    require(expected_sha256 is None or expected_sha256 == digest,
            'SCIENTIFIC_KNOWLEDGE_VERSION_CHANGED')
    return result, digest


def instructions(expected_sha256=None):
    result, digest = packet(expected_sha256)
    text = ('\nScientific guidance below is trusted reference material, not an executable skill. '
            'The supplied tool/graph contract and verified evidence take precedence. '
            'References to processes outside the catalog do not enable them. '
            'Local measurements and receipts, never this guidance, establish physical facts. '
            'Use only installed, verified native capabilities and stop when information is missing.\n')
    text += '\n\n'.join(d['text'] for d in result['documents'])
    return text, digest
