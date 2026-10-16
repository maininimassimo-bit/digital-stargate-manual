"""Pinned bootstrap source and literal entry; no native driver or authorization.

The reviewed invocation must pin ENTRY and the two expected hashes externally.
Reading hashes from mutable files to generate a new invocation is not approval.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import types

# This literal is the complete source passed to Python -I -S -B -c. It verifies
# this module's source buffer before executing any of its project code.
ENTRY = '''import sys, hashlib, pathlib, stat, os
if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
    raise RuntimeError('BOOTSTRAP_ISOLATION')
if len(sys.argv) != 5:
    raise RuntimeError('BOOTSTRAP_ARGUMENTS')
path = pathlib.Path(sys.argv[1])
if not path.is_absolute():
    raise RuntimeError('BOOTSTRAP_PATH')
for item in [path, *path.parents]:
    info = item.lstat()
    if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
        raise RuntimeError('BOOTSTRAP_ALIAS')
with path.open('rb') as stream:
    info = os.fstat(stream.fileno())
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > 1048576 or info.st_ino <= 0 or info.st_dev < 0:
        raise RuntimeError('BOOTSTRAP_SIZE')
    raw = stream.read(1048577)
if len(raw) != info.st_size or hashlib.sha256(raw).hexdigest() != sys.argv[2]:
    raise RuntimeError('BOOTSTRAP_SOURCE_HASH')
scope = {'__name__': '_dsg_verified_bootstrap', '__verified_bootstrap_sha256__': sys.argv[2],
         '__verified_bootstrap_path__': str(path), '__verified_bootstrap_bytes__': raw,
         '__verified_bootstrap_identity__': (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)}
exec(compile(raw, str(path), 'exec', dont_inherit=True), scope)
scope['_bootstrap_main'](sys.argv[3], sys.argv[4])
'''


def _require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def _pairs(rows):
    value = {}
    for key, item in rows:
        _require(key not in value, 'BOOTSTRAP_DUPLICATE_FIELD')
        value[key] = item
    return value


def _bytes(path, limit):
    path = Path(path)
    _require(path.is_absolute() and str(path.resolve()) == str(path), 'BOOTSTRAP_CANONICAL_PATH')
    for item in [path, *path.parents]:
        info = item.lstat()
        _require(not stat.S_ISLNK(info.st_mode) and
                 not getattr(info, 'st_file_attributes', 0) & 0x400, 'BOOTSTRAP_ALIAS')
    with path.open('rb') as stream:
        before = os.fstat(stream.fileno())
        _require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                 0 <= before.st_size <= limit and before.st_ino > 0 and
                 before.st_dev >= 0, 'BOOTSTRAP_FILE_SIZE')
        raw = stream.read(limit + 1)
        after = os.fstat(stream.fileno())
    identity = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns)
    _require(len(raw) == before.st_size and identity(before) == identity(after) ==
             identity(path.stat()), 'BOOTSTRAP_FILE_CHANGED')
    return raw, identity(after)


def _pin(path, expected, limit):
    _require(type(expected) is str and re.fullmatch('[0-9a-f]{64}', expected) is not None,
             'BOOTSTRAP_PIN_FORMAT')
    raw, identity = _bytes(path, limit)
    _require(hashlib.sha256(raw).hexdigest() == expected, 'BOOTSTRAP_PIN_MISMATCH')
    return raw, identity


class BootstrapSession:
    """Live gates for verified loader plus the bootstrap's own pinned closure."""
    def __init__(self, loader, snapshots):
        self.loader, self.snapshots = loader, tuple(snapshots)

    def assert_intact(self):
        self.loader.assert_intact()
        for path, raw, identity, limit in self.snapshots:
            current, current_identity = _bytes(path, limit)
            _require(current == raw and current_identity == identity, 'BOOTSTRAP_CLOSURE_CHANGED')
        return True


def _bootstrap_main(manifest_path, expected_manifest_sha256):
    _require(sys.flags.isolated == 1 and sys.flags.no_site == 1 and
             sys.flags.dont_write_bytecode == 1, 'BOOTSTRAP_ISOLATION')
    _require('__verified_bootstrap_sha256__' in globals(), 'BOOTSTRAP_UNVERIFIED_ENTRY')
    _require(not any(n == 'tools' or n.startswith('tools.') for n in sys.modules), 'BOOTSTRAP_PREPOPULATED')
    raw, manifest_identity = _pin(manifest_path, expected_manifest_sha256, 1048576)
    manifest = json.loads(raw.decode('ascii'), object_pairs_hook=_pairs)
    fields = {'protocol', 'bootstrapSha256', 'entrySha256', 'pythonVersion',
              'pythonExecutable', 'pythonExecutableSha256', 'loaderPath', 'loaderSha256',
              'sourcesManifestPath', 'sourcesManifestSha256', 'entryModule', 'entryCallable'}
    _require(type(manifest) is dict and set(manifest) == fields and
             manifest['protocol'] == 'DSG_NATIVE_BOOTSTRAP_MANIFEST_V1', 'BOOTSTRAP_SCHEMA')
    _require(manifest['bootstrapSha256'] == __verified_bootstrap_sha256__ and
             manifest['entrySha256'] == hashlib.sha256(ENTRY.encode('ascii')).hexdigest(), 'BOOTSTRAP_ENTRY_PIN')
    _require(type(manifest['pythonVersion']) is str and manifest['pythonVersion'] == sys.version and
             type(manifest['pythonExecutable']) is str and
             Path(manifest['pythonExecutable']) == Path(sys.executable), 'BOOTSTRAP_RUNTIME')
    # Python runtime is trusted, but its actual executable/version must be pinned.
    executable_raw, executable_identity = _pin(sys.executable, manifest['pythonExecutableSha256'], 16777216)
    for field in ['loaderPath', 'sourcesManifestPath', 'entryModule', 'entryCallable']:
        _require(type(manifest[field]) is str and len(manifest[field]) <= 4096, 'BOOTSTRAP_FIELD')
    _require(re.fullmatch(r'tools(?:\.[A-Za-z_][A-Za-z_0-9]*)+', manifest['entryModule']) is not None and
             re.fullmatch('[A-Za-z_][A-Za-z_0-9]*', manifest['entryCallable']) is not None,
             'BOOTSTRAP_ENTRY_NAME')
    loader_raw, loader_identity = _pin(manifest['loaderPath'], manifest['loaderSha256'], 1048576)
    sources_raw, sources_identity = _pin(manifest['sourcesManifestPath'], manifest['sourcesManifestSha256'], 1048576)
    snapshots = [(__verified_bootstrap_path__, __verified_bootstrap_bytes__,
                  __verified_bootstrap_identity__, 1048576)]
    snapshots.extend([(manifest_path, raw, manifest_identity, 1048576),
                      (sys.executable, executable_raw, executable_identity, 16777216),
                      (manifest['loaderPath'], loader_raw, loader_identity, 1048576),
                      (manifest['sourcesManifestPath'], sources_raw, sources_identity, 1048576)])
    library = types.ModuleType('_dsg_pinned_source_loader')
    exec(compile(loader_raw, manifest['loaderPath'], 'exec', dont_inherit=True), library.__dict__)
    loader = library.VerifiedSources(sources_raw, manifest['sourcesManifestSha256']).install()
    session = BootstrapSession(loader, snapshots)
    session.assert_intact()
    _require(manifest['entryModule'] in loader.sources, 'BOOTSTRAP_ENTRY_NOT_PINNED')
    module = __import__(manifest['entryModule'], fromlist=[manifest['entryCallable']])
    session.assert_intact()
    function = getattr(module, manifest['entryCallable'], None)
    _require(type(function) is types.FunctionType and function.__module__ == module.__name__ and
             function.__globals__ is module.__dict__, 'BOOTSTRAP_ENTRY_FUNCTION')
    # Future reviewed driver receives the live loader and must gate every sensitive
    # decision. This bootstrap does not create grants, processes or an attempt.
    result = function(session)
    session.assert_intact()
    return result
