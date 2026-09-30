"""F0 research only: bounded inline XISF history inspection, never execution."""
import argparse
import json
import struct
import xml.etree.ElementTree as ET

LIMIT = 2 * 1024 * 1024


def local(tag):
    return tag.rsplit('}', 1)[-1]


def xml(data):
    if len(data) > LIMIT or b'\x00' in data:
        raise ValueError('XML_BOUND_OR_ENCODING')
    text = data.decode('utf-8-sig')
    if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
        raise ValueError('XML_DECLARATION_UNSUPPORTED')
    root = ET.fromstring(text)
    pending = [(root, 0)]
    count = 0
    while pending:
        node, depth = pending.pop()
        count += 1
        if depth > 32 or count > 20000:
            raise ValueError('XML_TREE_BOUND')
        pending.extend((child, depth + 1) for child in node)
    return root


def inspect(stream):
    signature = stream.read(16)
    if len(signature) != 16 or signature[:8] != b'XISF0100':
        raise ValueError('SIGNATURE')
    length, reserved = struct.unpack('<II', signature[8:])
    if reserved or not 0 < length <= LIMIT:
        raise ValueError('HEADER_BOUND_OR_RESERVED')
    header = stream.read(length)
    if len(header) != length:
        raise ValueError('TRUNCATED_HEADER')
    root = xml(header)
    if local(root.tag) != 'xisf' or root.get('version') != '1.0':
        raise ValueError('XISF_VERSION')
    images = [n for n in root if local(n.tag) == 'Image']
    summaries = []
    for image in images:
        properties = [n for n in image if local(n.tag) == 'Property']
        history = [p for p in properties if p.get('id') == 'PixInsight:ProcessingHistory']
        item = {'propertyCount': len(properties), 'historyStatus': 'UNAVAILABLE'}
        if len(history) > 1:
            raise ValueError('AMBIGUOUS_HISTORY')
        if history:
            p = history[0]
            if p.get('type') != 'String' or len(p) or any(k in p.attrib for k in ('location', 'compression', 'encoding')):
                item['historyStatus'] = 'UNSUPPORTED_REPRESENTATION'
            else:
                h = xml((p.text or '').encode('utf-8'))
                if local(h.tag) != 'ProcessingHistory' or h.get('version') != '1.0':
                    raise ValueError('HISTORY_VERSION')
                instances = [n for n in h if local(n.tag) == 'instance']
                if len(instances) != len(h):
                    raise ValueError('HISTORY_STRUCTURE')
                # Only counts leave this function: arbitrary IDs and values remain private.
                item.update(historyStatus='PARSED_INLINE_SUBSET', instanceCount=len(instances),
                            instances=[{'parameterCount': sum(local(c.tag) == 'parameter' for c in n),
                                        'tableCount': sum(local(c.tag) == 'table' for c in n),
                                        'timeCount': sum(local(c.tag) == 'time' for c in n)} for n in instances])
        summaries.append(item)
    return {'headerBytes': length, 'imageCount': len(images), 'images': summaries,
            'executionEvidence': 'NOT_ESTABLISHED', 'workflowCompleteness': 'UNAVAILABLE'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file')
    args = parser.parse_args()
    try:
        with open(args.file, 'rb') as stream:
            report = inspect(stream)
        print(json.dumps(report, indent=2))
        return 0
    except (OSError, ValueError, ET.ParseError):
        # Do not leak paths, header excerpts or arbitrary XML values in diagnostics.
        print(json.dumps({'status': 'REJECTED_OR_UNREADABLE'}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
