"""Closed source-buffer loader; no native launch, grant creation or image processing.

The caller must itself be a fresh, independently pinned bootstrap. Importing this
module normally does not establish that prerequisite or authorize any operation.
"""
import hashlib
import importlib.abc
import importlib.machinery
import json
import os
from pathlib import Path
import re
import stat
import sys

MAX_MANIFEST = 1048576
MAX_SOURCE = 1048576
MAX_TOTAL = 16777216


class VerificationError(ValueError):
    pass


def _require(condition, reason):
    if not condition:
        raise VerificationError(reason)


def _pairs(rows):
    result = {}
    for key, value in rows:
        _require(key not in result, 'DUPLICATE_FIELD')
        result[key] = value
    return result


def _read(path, limit):
    # Reject aliases at every component, including Windows redirection points.
    _require(path.is_absolute(), 'ABSOLUTE_PATH_REQUIRED')
    for item in [path, *path.parents]:
        info = item.lstat()
        _require(not stat.S_ISLNK(info.st_mode) and
                 not (getattr(info, 'st_file_attributes', 0) & 0x400), 'PATH_ALIAS')
    with path.open('rb') as stream:
        before = os.fstat(stream.fileno())
        _require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, 'SOURCE_NOT_PRIVATE_FILE')
        _require(0 <= before.st_size <= limit, 'SOURCE_SIZE')
        raw = stream.read(limit + 1)
        after = os.fstat(stream.fileno())
        _require(len(raw) == before.st_size and
                 (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
                 (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), 'SOURCE_CHANGED')
    current = path.stat()
    _require((current.st_dev, current.st_ino, current.st_size, current.st_mtime_ns) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), 'SOURCE_REPLACED')
    return raw, (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
                 after.st_ctime_ns, after.st_nlink)


class VerifiedSources(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Single-install loader for explicitly pinned tools.* sources and prefixes.

    Construct only in a fresh isolated interpreter. Disk changes after validation
    cannot change executed bytes: exec_module compiles the retained verified bytes.
    assert_intact also rechecks disk at each later supervisor decision boundary.
    """
    def __init__(self, manifest_raw, expected_sha256):
        _require(type(manifest_raw) is bytes and len(manifest_raw) <= MAX_MANIFEST,
                 'MANIFEST_SIZE')
        _require(type(expected_sha256) is str and
                 re.fullmatch('[0-9a-f]{64}', expected_sha256) is not None and
                 hashlib.sha256(manifest_raw).hexdigest() == expected_sha256, 'MANIFEST_HASH')
        try:
            value = json.loads(manifest_raw.decode('ascii'), object_pairs_hook=_pairs)
        except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
            raise VerificationError('MANIFEST_JSON') from error
        _require(type(value) is dict and set(value) == {'protocol', 'root', 'modules'} and
                 value['protocol'] == 'DSG_NATIVE_VERIFIED_SOURCES_V1', 'MANIFEST_SCHEMA')
        _require(type(value['root']) is str, 'ROOT_TYPE')
        self.root = Path(value['root'])
        _require(self.root.is_absolute() and str(self.root.resolve()) == str(self.root), 'ROOT_CANONICAL')
        _require(type(value['modules']) is list and 1 <= len(value['modules']) <= 128, 'MODULE_COUNT')
        self.sources, self.namespaces, self.loaded = {}, set(), {}
        self.identities, self.pending = {}, {}
        total, paths = 0, set()
        for row in value['modules']:
            _require(type(row) is dict and set(row) ==
                     {'name', 'path', 'sha256', 'byteLength', 'isPackage'}, 'MODULE_SCHEMA')
            name = row['name']
            _require(type(name) is str and len(name) <= 192 and
                     re.fullmatch(r'tools(?:\.[A-Za-z_][A-Za-z_0-9]*)*', name) is not None,
                     'MODULE_NAME')
            _require(name not in self.sources and type(row['isPackage']) is bool, 'MODULE_DUPLICATE')
            _require(type(row['path']) is str and type(row['byteLength']) is int and
                     0 <= row['byteLength'] <= MAX_SOURCE and type(row['sha256']) is str and
                     re.fullmatch('[0-9a-f]{64}', row['sha256']) is not None, 'MODULE_PIN')
            relative = Path(row['path'])
            expected = Path(*name.split('.')) / '__init__.py' if row['isPackage'] else Path(*name.split('.')).with_suffix('.py')
            _require(relative == expected and not relative.is_absolute(), 'MODULE_PATH')
            path = self.root / relative
            key = os.path.normcase(str(path))
            _require(key not in paths, 'SOURCE_PATH_DUPLICATE')
            paths.add(key)
            raw, identity = _read(path, MAX_SOURCE)
            _require(len(raw) == row['byteLength'] and hashlib.sha256(raw).hexdigest() == row['sha256'], 'SOURCE_HASH')
            total += len(raw)
            _require(total <= MAX_TOTAL, 'SOURCE_TOTAL')
            self.sources[name] = (path, raw, row['sha256'], row['isPackage'])
            self.identities[name] = identity
            parts = name.split('.')
            self.namespaces.update('.'.join(parts[:i]) for i in range(1, len(parts)))
        for prefix in self.namespaces & self.sources.keys():
            _require(self.sources[prefix][3], 'PARENT_NOT_PACKAGE')
        self.namespaces.difference_update(self.sources)
        self.installed = False

    def install(self):
        _require(sys.flags.isolated == 1 and sys.flags.no_site == 1 and
                 sys.flags.dont_write_bytecode == 1, 'ISOLATED_INTERPRETER_REQUIRED')
        _require(not self.installed and not any(n == 'tools' or n.startswith('tools.') for n in sys.modules),
                 'PREPOPULATED_PROJECT_MODULE')
        sys.meta_path.insert(0, self)
        self.installed = True
        return self

    def find_spec(self, fullname, path=None, target=None):
        if fullname != 'tools' and not fullname.startswith('tools.'):
            return None
        _require(self.installed and target is None and fullname not in self.loaded, 'RELOAD_REFUSED')
        _require(fullname in self.sources or fullname in self.namespaces, 'UNPINNED_PROJECT_IMPORT')
        package = fullname in self.namespaces or self.sources[fullname][3]
        _require(fullname not in self.pending, 'MODULE_LOAD_PENDING')
        spec = importlib.machinery.ModuleSpec(fullname, self, is_package=package)
        self.pending[fullname] = spec
        return spec

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        name = module.__name__
        _require(self.installed and sys.meta_path and sys.meta_path[0] is self and
                 sys.modules.get(name) is module and
                 self.pending.get(name) is module.__spec__ and
                 name not in self.loaded and module.__spec__.loader is self and
                 (name in self.sources or name in self.namespaces), 'UNVERIFIED_MODULE_EXEC')
        spec = module.__spec__
        del self.pending[name]
        if name in self.sources:
            path, raw, digest, package = self.sources[name]
            # No SourceFileLoader, pyc lookup, runpy or second pathname read.
            code = compile(raw, str(path), 'exec', dont_inherit=True)
            module.__file__ = str(path)
        else:
            digest, code = None, None
        self.loaded[name] = (module, spec, digest)
        if code is not None:
            exec(code, module.__dict__)

    def assert_intact(self):
        _require(self.installed and sys.meta_path and sys.meta_path[0] is self, 'LOADER_REPLACED')
        actual = {n for n in sys.modules if n == 'tools' or n.startswith('tools.')}
        _require(actual == set(self.loaded), 'MODULE_SET_CHANGED')
        for name, (module, spec, digest) in self.loaded.items():
            _require(sys.modules.get(name) is module and module.__spec__ is spec and
                     module.__loader__ is self and spec.loader is self, 'MODULE_IDENTITY_CHANGED')
            _require(digest == (self.sources[name][2] if name in self.sources else None), 'COMPILED_PIN_CHANGED')
        for name, (path, raw, digest, package) in self.sources.items():
            current, identity = _read(path, MAX_SOURCE)
            _require(identity == self.identities[name], 'SOURCE_IDENTITY_CHANGED')
            _require(current == raw and hashlib.sha256(current).hexdigest() == digest, 'SOURCE_HASH')
        return True
