"""Read-only launch-code closure checks; never authorizes a start or process close.

loaded_sources must come from the live verified bootstrap, never a JSON assertion
or an ordinary scan of already imported modules. The future supervisor supplies it.
"""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import stat

from tools.pixinsight.local_pilot.broker import ProtocolError, require
from tools.scientific_transients.local_registry import safe_path, signature

MIB = 1048576
FIXED = frozenset({'ENTRY', 'LAUNCHER', 'SUPERVISOR', 'EXECUTABLE', 'PYTHON_EXECUTABLE',
    'CORE', 'PARSER', 'PRIMARY', 'WRAPPER', 'ARB_REPORT', 'RQ_REPORT', 'APPROVAL',
    'BOOTSTRAP_ENTRY', 'BOOTSTRAP_MANIFEST'})
HASH_ROLES = {'entrySha256':'ENTRY', 'launcherTemplateSha256':'LAUNCHER',
    'supervisorSha256':'SUPERVISOR', 'executableSha256':'EXECUTABLE', 'arbSha256':'ARB_REPORT',
    'rqSha256':'RQ_REPORT', 'approvalSha256':'APPROVAL', 'bootstrapEntrySha256':'BOOTSTRAP_ENTRY',
    'bootstrapManifestSha256':'BOOTSTRAP_MANIFEST'}
FIELDS = {'protocol', 'operationRef', 'sealSha256', 'grantSha256', 'expectedPixInsightVersion',
    'files', 'ownerNonce', 'processSessionRef', 'expectedPythonVersion', 'parentDeadlineUTC', *HASH_ROLES}


def _fields(value, fields):
    require(type(value) is dict and set(value) == set(fields), 'LAUNCH_CONTROL_FIELDS')


def _hex(value, count):
    return type(value) is str and re.fullmatch('[a-f0-9]{' + str(count) + '}', value) is not None


def _path(value):
    require(type(value) is str and 1 <= len(value) <= 512 and value.isascii()
            and not any(ord(c) < 32 for c in value), 'LAUNCH_CONTROL_PATH')
    path = Path(value)
    require(path.is_absolute() and path.as_posix() == value, 'LAUNCH_CONTROL_PATH')
    actual = safe_path(path)
    require(actual == path and actual.resolve() == path, 'LAUNCH_CONTROL_PATH')
    return path


def _pin(path, expected_sha, cap, guard, *, size=None, identity=None, capture=False, progress_guard=None):
    require(callable(guard) and (progress_guard is None or callable(progress_guard)), 'LAUNCH_CONTROL_GUARD')
    progress = guard if progress_guard is None else progress_guard
    path = _path(path)
    guard()
    digest, count, raw = hashlib.sha256(), 0, bytearray()
    with path.open('rb') as stream:
        before = os.fstat(stream.fileno())
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_ino != 0
                and 0 <= before.st_size <= cap and (size is None or before.st_size == size),
                'LAUNCH_CONTROL_FILE')
        if identity is not None:
            require(signature(before) == signature(identity), 'LAUNCH_CONTROL_IDENTITY')
        while chunk := stream.read(min(65536, before.st_size - count + 1)):
            progress(); count += len(chunk)
            require(count <= before.st_size, 'LAUNCH_CONTROL_FILE_CHANGED')
            digest.update(chunk)
            if capture: raw.extend(chunk)
        after = os.fstat(stream.fileno())
    require(count == before.st_size and signature(before) == signature(after)
            and signature(after)[:4] == signature(safe_path(path).lstat())[:4], 'LAUNCH_CONTROL_FILE_CHANGED')
    require(digest.hexdigest() == expected_sha, 'LAUNCH_CONTROL_HASH')
    guard()
    return (path, expected_sha, before.st_size, before, cap), bytes(raw)


def _tree(value, depth=1):
    require(depth <= 8, 'LAUNCH_CONTROL_JSON_DEPTH')
    if value is None or type(value) is bool: return
    if type(value) is int:
        require(abs(value) <= 2**128 - 1, 'LAUNCH_CONTROL_JSON_INTEGER')
    elif type(value) is str:
        require(value.isascii() and len(value) <= 512, 'LAUNCH_CONTROL_JSON_STRING')
    elif type(value) is list:
        require(len(value) <= 128, 'LAUNCH_CONTROL_JSON_ARRAY')
        for item in value: _tree(item, depth + 1)
    elif type(value) is dict:
        require(len(value) <= 32, 'LAUNCH_CONTROL_JSON_MEMBERS')
        for key, item in value.items():
            require(key not in {'__proto__', 'prototype', 'constructor'}, 'LAUNCH_CONTROL_JSON_KEY')
            _tree(key, depth + 1); _tree(item, depth + 1)
    else: raise ProtocolError('LAUNCH_CONTROL_JSON_TYPE')


def _json(raw):
    def pairs(rows):
        value = {}
        for key, item in rows:
            require(key not in value, 'LAUNCH_CONTROL_JSON_DUPLICATE')
            value[key] = item
        return value
    def integer(token):
        require(len(token) <= 40, 'LAUNCH_CONTROL_JSON_INTEGER')
        return int(token)
    def invalid(_): raise ProtocolError('LAUNCH_CONTROL_JSON_NUMBER')
    try:
        value = json.loads(raw.decode('ascii'), object_pairs_hook=pairs,
            parse_int=integer, parse_float=invalid, parse_constant=invalid)
    except ProtocolError:
        raise
    except (ValueError, UnicodeError, RecursionError) as error:
        raise ProtocolError('LAUNCH_CONTROL_JSON') from error
    _tree(value)
    return value


def _loaded(value):
    require(type(value) is dict and 1 <= len(value) <= 128, 'LAUNCH_CONTROL_LOADED_SET')
    result = {}
    for name, row in value.items():
        require(type(name) is str and len(name) <= 192 and
                re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*', name) is not None,
                'LAUNCH_CONTROL_MODULE_NAME')
        _fields(row, {'path', 'sha256', 'byteLength'})
        require(_hex(row['sha256'],64) and type(row['byteLength']) is int
                and 0 <= row['byteLength'] <= MIB, 'LAUNCH_CONTROL_LOADED_PIN')
        result[name] = {'path': _path(row['path']).as_posix(), 'sha256': row['sha256'],
                        'byteLength': row['byteLength']}
    return result


class LaunchControlSnapshot:
    """Immutable-by-convention metadata snapshot, not an ownership capability.

    The trusted caller retains the object in the same session, verifies it at
    publication/closure boundaries and still supplies independent live ownership.
    """
    def __init__(self, control, pins, sources, loaded_sources, guard, *, progress_guard=None):
        require(progress_guard is None or callable(progress_guard), 'LAUNCH_CONTROL_GUARD')
        self._control_raw, self._pins = json.dumps(control).encode('ascii'), tuple(pins)
        self._sources, self._loaded_sources, self._guard = sources, loaded_sources, guard
        self._progress_guard = progress_guard

    @property
    def control(self):
        return _json(self._control_raw)

    def verify(self):
        self._guard()
        require(_loaded(self._loaded_sources()) == self._sources, 'LAUNCH_CONTROL_LOADED_CHANGED')
        for path, digest, size, info, cap in self._pins:
            _pin(path.as_posix(), digest, cap, self._guard, size=size, identity=info,
                 progress_guard=self._progress_guard)
        require(_loaded(self._loaded_sources()) == self._sources, 'LAUNCH_CONTROL_LOADED_CHANGED')
        self._guard()
        return True


def inspect_launch_control(path, expected_sha256, *, loaded_sources, guard, progress_guard=None):
    """Validate every declared code pin and exact live-attested local source set.

    Raw approval/review hashes bind provenance only. This does not authenticate
    human consent, infer executing code from disk, create an attempt or close it.
    """
    require(_hex(expected_sha256,64) and callable(loaded_sources) and callable(guard), 'LAUNCH_CONTROL_ARGUMENTS')
    require(progress_guard is None or callable(progress_guard), 'LAUNCH_CONTROL_GUARD')
    control_pin, raw = _pin(path, expected_sha256, MIB, guard, capture=True, progress_guard=progress_guard)
    value = _json(raw)
    _fields(value, FIELDS)
    require(value['protocol'] == 'DSG_NATIVE_LINEAR_LAUNCH_CONTROL_V1', 'LAUNCH_CONTROL_PROTOCOL')
    for key in ['operationRef','ownerNonce','processSessionRef']:
        require(_hex(value[key],32), 'LAUNCH_CONTROL_SESSION')
    for key in [*HASH_ROLES,'sealSha256','grantSha256']:
        require(_hex(value[key],64), 'LAUNCH_CONTROL_PIN')
    for key in ['expectedPixInsightVersion','expectedPythonVersion']:
        require(type(value[key]) is str and 1 <= len(value[key]) <= 192 and value[key].isascii(), 'LAUNCH_CONTROL_VERSION')
    text = value['parentDeadlineUTC']
    require(type(text) is str and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ',text) is not None, 'LAUNCH_CONTROL_TIME')
    try: dt.datetime.strptime(text,'%Y-%m-%dT%H:%M:%SZ')
    except ValueError as error: raise ProtocolError('LAUNCH_CONTROL_TIME') from error
    require(type(value['files']) is list and len(FIXED) <= len(value['files']) <= 128, 'LAUNCH_CONTROL_FILES')
    fixed, sources, pins, total = {}, {}, [control_pin], 0
    for row in value['files']:
        _fields(row, {'role','name','path','sha256','byteLength'})
        role, name = row['role'], row['name']
        require(type(role) is str and role in FIXED | {'PARENT_SOURCE'} and type(name) is str
                and 1 <= len(name) <= 192 and name.isascii(), 'LAUNCH_CONTROL_ROLE')
        file = _path(row['path'])
        cap = 512*MIB if role == 'EXECUTABLE' else 16*MIB if role == 'PYTHON_EXECUTABLE' else MIB
        require(_hex(row['sha256'],64) and type(row['byteLength']) is int and
                0 <= row['byteLength'] <= cap and (row['byteLength'] > 0 or
                role == 'PARENT_SOURCE' and file.name == '__init__.py'), 'LAUNCH_CONTROL_SIZE')
        total += row['byteLength']; require(total <= 544*MIB, 'LAUNCH_CONTROL_AGGREGATE')
        if role == 'PARENT_SOURCE':
            require(name not in sources, 'LAUNCH_CONTROL_DUPLICATE_SOURCE')
            sources[name] = {key:row[key] for key in ['path','sha256','byteLength']}
        else:
            require(role not in fixed and name == file.name, 'LAUNCH_CONTROL_DUPLICATE_ROLE')
            fixed[role] = row
        pin, _ = _pin(row['path'], row['sha256'], cap, guard, size=row['byteLength'], progress_guard=progress_guard)
        pins.append(pin)
    require(set(fixed) == FIXED, 'LAUNCH_CONTROL_REQUIRED_ROLES')
    for key, role in HASH_ROLES.items():
        require(value[key] == fixed[role]['sha256'], 'LAUNCH_CONTROL_ROLE_BINDING')
    require(_loaded(loaded_sources()) == _loaded(sources), 'LAUNCH_CONTROL_LOADED_MISMATCH')
    snapshot = LaunchControlSnapshot(value, pins, sources, loaded_sources, guard, progress_guard=progress_guard)
    snapshot.verify()
    return snapshot
