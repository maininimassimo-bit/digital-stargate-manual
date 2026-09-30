"""Parse the versioned BKL-049 bounded export-shaped JS subset, never execute it.
The returned in-memory structure can contain private values. CLI emits counts only.
No PCL/PJSR/vendor source is incorporated. Not a general JavaScript parser.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

MAX_BYTES = 2 * 1024 * 1024
MAX_TOKENS = 200000
MAX_INSTANCES = 512
MAX_DEPTH = 32
MAX_PARAMETERS = 2048
MAX_STRING = 4096
STRING_LIMITS = {"1.0": MAX_STRING, "1.1": 16384}
MAX_ARRAY_ITEMS = 4096
MAX_IDENTIFIER = 128
MAX_MASK_COMMANDS = 128
TOKEN = re.compile(r'(?P<space>\s+)|(?P<line>//[^\r\n]*)|(?P<block>/\*[\s\S]*?\*/)|(?P<string>"(?:[^"\\\r\n]|\\[^\r\n])*")|(?P<number>(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)|(?P<id>[A-Za-z_$][A-Za-z0-9_$]*)|(?P<punct>[.=;(),\[\]+-])')

class Unsupported(ValueError):
    def __init__(self, code, offset):
        self.code, self.offset = code, offset
        super().__init__(f'{code} at character {offset}')

def parse_export(text, *, profile="1.0"):
    if not isinstance(profile, str) or profile not in STRING_LIMITS:
        raise Unsupported("PROFILE_UNSUPPORTED", 0)
    max_string = STRING_LIMITS[profile]
    if len(text.encode('utf-8')) > MAX_BYTES:
        raise Unsupported('SIZE_LIMIT', 0)
    tokens, comments = [], []
    pos = 0
    while pos < len(text):
        match = TOKEN.match(text, pos)
        if not match:
            raise Unsupported('UNSUPPORTED_TOKEN', pos)
        kind = match.lastgroup
        if kind == 'id' and len(match.group()) > MAX_IDENTIFIER:
            raise Unsupported('IDENTIFIER_LIMIT', pos)
        if kind in ('line', 'block'):
            comments.append({'start': pos, 'end': match.end()})
        elif kind != 'space':
            tokens.append((kind, match.group(), pos, match.end()))
            if len(tokens) > MAX_TOKENS:
                raise Unsupported('TOKEN_LIMIT', pos)
        pos = match.end()
    tokens.append(('eof', '', pos, pos))
    index = 0
    instances, statements, parents = {}, [], {}

    def current():
        return tokens[index]

    def take(value=None, kind=None):
        nonlocal index
        token = current()
        if (value is not None and token[1] != value) or (kind is not None and token[0] != kind):
            raise Unsupported('UNEXPECTED_SYNTAX', token[2])
        index += 1
        return token

    def string():
        token = take(kind='string')
        try:
            value = json.loads(token[1])
            value.encode('utf-8')
            if len(value) > max_string:
                raise Unsupported('STRING_LIMIT', token[2])
            return value
        except Unsupported:
            raise
        except (ValueError, UnicodeError):
            raise Unsupported('UNSUPPORTED_STRING_ESCAPE', token[2]) from None

    def value(depth=0):
        if depth > MAX_DEPTH:
            raise Unsupported('VALUE_DEPTH_LIMIT', current()[2])
        token = current()
        if token[0] == 'string':
            result = string()
            while current()[1] == '+':
                take('+')
                result += string()  # Literal concatenation only.
                if len(result) > max_string:
                    raise Unsupported('STRING_LIMIT', token[2])
            return result
        if token[1] == '[':
            take('[')
            result = []
            if current()[1] != ']':
                while True:
                    if len(result) >= MAX_ARRAY_ITEMS:
                        raise Unsupported('ARRAY_LIMIT', current()[2])
                    result.append(value(depth + 1))
                    if current()[1] != ',':
                        break
                    take(',')
                    if current()[1] == ']':
                        break
            take(']')
            return result
        if token[0] == 'number' or token[1] in ('-', '+'):
            sign = ''
            if token[1] in ('-', '+'):
                sign = take()[1]
            number = take(kind='number')
            if len(number[1]) > 128:
                raise Unsupported('NUMBER_LITERAL_LIMIT', number[2])
            # Keep the lexical numeric representation, including precision, without float rounding.
            return {'kind': 'number', 'literal': sign + number[1]}
        if token[1] in ('true', 'false', 'null'):
            return {'true': True, 'false': False, 'null': None}[take()[1]]
        if token[0] == 'id':
            owner = take(kind='id')[1]
            take('.')
            member = take(kind='id')[1]
            return {'kind': 'enum', 'owner': owner, 'member': member}
        raise Unsupported('UNSUPPORTED_VALUE', token[2])

    def integer_index():
        token = take(kind='number')
        if len(token[1]) > 9 or not re.fullmatch(r'\d+', token[1]):
            raise Unsupported('INVALID_INDEX', token[2])
        return int(token[1])

    while current()[0] != 'eof':
        start = current()[2]
        if current()[1] == 'var':
            take('var')
            name = take(kind='id')[1]
            take('='); take('new')
            process = take(kind='id')[1]
            if current()[1] == '(':
                take('('); take(')')
            take(';')
            if name in instances:
                raise Unsupported('DUPLICATE_VARIABLE', start)
            if len(instances) >= MAX_INSTANCES:
                raise Unsupported('INSTANCE_LIMIT', start)
            instances[name] = {'process': process, 'parameters': {}, 'children': [], 'maskCommands': [], 'sourceSpan': [start, tokens[index-1][3]]}
            operation = 'declare'
        else:
            name = take(kind='id')[1]
            if name not in instances:
                raise Unsupported('UNKNOWN_INSTANCE', start)
            take('.')
            member = take(kind='id')[1]
            obj = instances[name]
            if name in parents:
                raise Unsupported('POST_ATTACHMENT_MUTATION', start)
            if current()[1] == '=':
                take('=')
                if member in obj['parameters']:
                    raise Unsupported('DUPLICATE_PROPERTY', start)
                if len(obj['parameters']) >= MAX_PARAMETERS:
                    raise Unsupported('PARAMETER_LIMIT', start)
                obj['parameters'][member] = value()
                take(';')
                operation = 'assign'
            else:
                if obj['process'] != 'ProcessContainer' or member not in ('add', 'setMask', 'invertMask'):
                    raise Unsupported('UNSUPPORTED_CALL', start)
                take('(')
                if member == 'add':
                    child = take(kind='id')[1]
                    if child not in instances:
                        raise Unsupported('UNKNOWN_CHILD', start)
                    if child in parents:
                        raise Unsupported('REUSED_INSTANCE', start)
                    ancestor = name
                    while True:
                        if ancestor == child:
                            raise Unsupported('CONTAINER_CYCLE', start)
                        if ancestor not in parents:
                            break
                        ancestor = parents[ancestor]
                    parents[child] = name
                    obj['children'].append(child)
                else:
                    child_index = integer_index()
                    if child_index >= len(obj['children']):
                        raise Unsupported('MASK_INDEX_RANGE', start)
                    command = {'operation': member, 'index': child_index}
                    if member == 'setMask':
                        take(',')
                        command['reference'] = string()
                    if len(obj['maskCommands']) >= MAX_MASK_COMMANDS:
                        raise Unsupported('MASK_COMMAND_LIMIT', start)
                    obj['maskCommands'].append(command)
                take(')'); take(';')
                operation = member
        statements.append({'instance': name, 'operation': operation, 'sourceSpan': [start, tokens[index-1][3]]})
    roots = [name for name in instances if name not in parents]
    if len(roots) != 1:
        raise Unsupported('ROOT_COUNT', 0)
    stack = [(roots[0], 0)]
    while stack:
        name, depth = stack.pop()
        if depth > MAX_DEPTH:
            raise Unsupported('CONTAINER_DEPTH_LIMIT', 0)
        stack.extend((child, depth + 1) for child in instances[name]['children'])
    return {'status': 'PARSED_SUBSET', 'root': roots[0], 'instances': instances,
            'statements': statements, 'commentSpans': comments,
            'sourceSha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
            'executionEvidence': 'NOT_ESTABLISHED', 'workflowCompleteness': 'UNAVAILABLE'}

def safe_summary(result):
    items = list(result['instances'].values())
    return {'status': result['status'], 'instanceCount': len(items),
            'containerCount': sum(x['process'] == 'ProcessContainer' for x in items),
            'processInstanceCount': sum(x['process'] != 'ProcessContainer' for x in items),
            'parameterCount': sum(len(x['parameters']) for x in items),
            'maskCommandCount': sum(len(x['maskCommands']) for x in items),
            'statementCount': len(result['statements']),
            'executionEvidence': result['executionEvidence'],
            'workflowCompleteness': result['workflowCompleteness']}

def main():
    try:
        with Path(sys.argv[1]).open('rb') as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise Unsupported('SIZE_LIMIT', 0)
        result = parse_export(raw.decode('utf-8-sig'))
        summary = safe_summary(result)
        summary['originalByteSha256'] = hashlib.sha256(raw).hexdigest()
        print(json.dumps(summary, indent=2))
    except Unsupported as exc:
        print(json.dumps({'status': 'UNSUPPORTED', 'code': exc.code, 'offset': exc.offset}))
        sys.exit(1)
    except (OSError, UnicodeError, IndexError):
        print(json.dumps({'status': 'UNAVAILABLE', 'code': 'INPUT_ERROR'}))
        sys.exit(1)


if __name__ == "__main__":
    main()
