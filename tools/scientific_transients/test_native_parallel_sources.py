"""Adversarial source-only gates; no native operations or astronomical data."""
import unittest

from tools.scientific_transients import test_native_verified_loader as fixture


class ParallelSourceTests(unittest.TestCase):
    scenario = fixture.VerifiedLoaderTests.scenario

    @staticmethod
    def sources(count=22):
        return {f'tools.source_{i}': b'VALUE = 17\n' for i in range(count)}

    def test_every_source_rechecked_with_four_workers_and_no_surviving_threads(self):
        for count in (22, 128):
            with self.subTest(count=count):
                self.scenario('''
import threading
loader = construct().install()
original = library._read
lock = threading.Lock()
barrier = threading.Barrier(4, timeout=5)
seen = []
active = [0, 0]
def read(path, limit):
    with lock:
        index = len(seen)
        seen.append(str(path))
        active[0] += 1
        active[1] = max(active)
    try:
        if index < 4: barrier.wait()
        return original(path, limit)
    finally:
        with lock: active[0] -= 1
library._read = read
for attempt in range(2):
    seen.clear()
    assert loader.assert_intact()
    assert len(seen) == len(set(seen)) == len(loader.sources)
    assert active == [0, 4]
    assert not any(t.name.startswith('dsg_verified_source') for t in threading.enumerate())
''', sources=self.sources(count))

    def test_failure_precedence_is_manifest_order_and_workers_join(self):
        self.scenario('''
import threading, errno
loader = construct().install()
original = library._read
later = threading.Event()
done = []
def read(path, limit):
    try:
        if path.stem == 'source_0':
            assert later.wait(5)
            raise PermissionError(errno.EACCES, 'synthetic denied', str(path))
        if path.stem == 'source_1':
            later.set()
            raise FileNotFoundError(errno.ENOENT, 'synthetic missing', str(path))
        return original(path, limit)
    finally: done.append(path.stem)
library._read = read
try: loader.assert_intact()
except PermissionError as error:
    assert error.errno == errno.EACCES
    assert error.filename.endswith('source_0.py')
else: raise AssertionError('missing access rejection')
assert len(done) == 22
assert not any(t.name.startswith('dsg_verified_source') for t in threading.enumerate())
''', sources=self.sources())

    def test_coherence_rechecked_after_reads(self):
        mutations = [
            'loader.sources = dict(loader.sources)',
            'loader.identities = dict(loader.identities)',
            'loader.loaded = dict(loader.loaded)',
            "loader.identities['tools.source_0'] = (0, 0, 0, 0, 0, 0)",
            "loader.sources['tools.source_0'] = (root / 'other.py', b'other', '0' * 64, False)",
            "sys.modules['tools.source_0'] = types.ModuleType('tools.source_0')",
            "sys.modules['tools.source_0'].__loader__ = None",
            "sys.modules['tools.source_0'].__spec__ = None",
            "sys.modules['tools.unpinned'] = types.ModuleType('tools.unpinned')",
            'sys.meta_path.insert(0, object())',
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.scenario('''
loader = construct().install()
import tools.source_0
original = library._read
def read(path, limit):
    result = original(path, limit)
    if path.stem == 'source_21':
        ''' + mutation + '''
    return result
library._read = read
reject(loader.assert_intact)
''', sources=self.sources())

    def test_original_short_read_rejected_and_stream_closed(self):
        self.scenario('''
loader = construct().install()
original_open = pathlib.Path.open
closed = []
class ShortStream:
    def __init__(self, stream): self.stream = stream
    def __enter__(self): return self
    def __exit__(self, *args):
        self.stream.close()
        closed.append(self.stream.closed)
    def fileno(self): return self.stream.fileno()
    def read(self, size): return self.stream.read(size)[:-1]
def open_file(path, *args, **kwargs):
    stream = original_open(path, *args, **kwargs)
    return ShortStream(stream) if path.stem == 'source_21' else stream
pathlib.Path.open = open_file
try: loader.assert_intact()
except library.VerificationError as error: assert str(error) == 'SOURCE_CHANGED'
else: raise AssertionError('short read accepted')
assert closed == [True]
''', sources=self.sources())

    def test_partial_submission_interruption_joins_started_workers(self):
        for exception in ('RuntimeError', 'KeyboardInterrupt'):
            with self.subTest(exception=exception):
                self.scenario('''
import threading
loader = construct().install()
original = library._read
pool_class = library.ThreadPoolExecutor
fault = threading.Event()
done = []
def read(path, limit):
    assert fault.wait(5)
    try: return original(path, limit)
    finally: done.append(path.stem)
class BrokenPool(pool_class):
    count = 0
    def submit(self, *args, **kwargs):
        self.count += 1
        if self.count == 3:
            fault.set()
            raise ''' + exception + '''('synthetic submission interruption')
        return super().submit(*args, **kwargs)
library._read = read
library.ThreadPoolExecutor = BrokenPool
try: loader.assert_intact()
except ''' + exception + ''': pass
else: raise AssertionError('interruption swallowed')
assert len(done) == 2
assert not any(t.name.startswith('dsg_verified_source') for t in threading.enumerate())
''', sources=self.sources())

    def test_failed_futures_do_not_retain_read_frames(self):
        self.scenario('''
import gc, weakref, threading
loader = construct().install()
refs = []
class Buffer:
    def __init__(self): self.data = bytearray(1048576)
def read(path, limit):
    buffer = Buffer()
    refs.append(weakref.ref(buffer))
    raise library.VerificationError('SYNTHETIC_READ_FAILURE')
library._read = read
kept = None
try: loader.assert_intact()
except library.VerificationError as error: kept = error
assert kept is not None and str(kept) == 'SYNTHETIC_READ_FAILURE'
gc.collect()
assert len(refs) == 22 and all(ref() is None for ref in refs)
assert not any(t.name.startswith('dsg_verified_source') for t in threading.enumerate())
''', sources=self.sources())

    def test_original_ancestor_checks_remain_ordered_for_every_file(self):
        self.scenario('''
import threading
loader = construct().install()
original = library._read
original_lstat = pathlib.Path.lstat
local = threading.local()
observations = {}
def lstat(path, *args, **kwargs):
    observations.setdefault(local.name, []).append(str(path))
    return original_lstat(path, *args, **kwargs)
def read(path, limit):
    local.name = path.stem
    return original(path, limit)
library._read = read
pathlib.Path.lstat = lstat
assert loader.assert_intact()
for path, _, _, _ in loader.sources.values():
    assert observations[path.stem] == [str(path), *map(str, path.parents)]
''', sources=self.sources())

    def test_retrieval_interrupt_joins_workers_before_propagation(self):
        self.scenario('''
import threading
loader = construct().install()
original = library._read
pool_class = library.ThreadPoolExecutor
release = threading.Event()
done = []
def read(path, limit):
    assert release.wait(5)
    try: return original(path, limit)
    finally: done.append(path.stem)
class BrokenRetrieval(pool_class):
    def map(self, fn, jobs):
        futures = [self.submit(fn, job) for job in tuple(jobs)[:2]]
        def results():
            release.set()
            raise KeyboardInterrupt('synthetic retrieval interruption')
            yield None
        return results()
library._read = read
library.ThreadPoolExecutor = BrokenRetrieval
try: loader.assert_intact()
except KeyboardInterrupt: pass
else: raise AssertionError('retrieval interrupt swallowed')
assert len(done) == 2
assert not any(t.name.startswith('dsg_verified_source') for t in threading.enumerate())
''', sources=self.sources())

    def test_original_budget_still_expires_when_last_read_advances_clock(self):
        repo = fixture.LOADER.parents[2]
        names = [
            'tools.scientific_transients.native_run_budget',
            'tools.pixinsight.local_pilot.broker',
            'tools.pixinsight.local_pilot.worker',
            'tools.pixinsight.workflow_archive.__init__',
            'tools.pixinsight.workflow_archive.export_parser',
            'tools.scientific_registry.__init__',
            'tools.scientific_registry.ingestion_storage',
        ]
        sources = {name: repo.joinpath(*name.split('.')).with_suffix('.py').read_bytes()
                   for name in names}
        sources.update(self.sources())
        self.scenario('''
import datetime as dt
loader = construct().install()
from tools.scientific_transients.native_run_budget import LiveNativeBudget
clock = [10.0]
wall = dt.datetime(2026, 10, 16, tzinfo=dt.timezone.utc)
budget = LiveNativeBudget(monotonic=lambda: clock[0], wall=lambda: wall)
budget.require_running()
original = library._read
def read(path, limit):
    result = original(path, limit)
    if path.stem == 'source_21': clock[0] = 190.0
    return result
library._read = read
assert loader.assert_intact()
try: budget.require_running()
except Exception as error: assert str(error) == 'NATIVE_BUDGET_EXPIRED'
else: raise AssertionError('expired original budget accepted')
assert budget.origin_monotonic == 10 and budget.deadline_monotonic == 190
''', sources=sources)

    def test_later_source_ancestor_alias_still_rejected(self):
        self.scenario('''
import threading, stat
loader = construct().install()
original = library._read
original_lstat = pathlib.Path.lstat
local = threading.local()
def lstat(path, *args, **kwargs):
    if local.name == 'source_21' and path == root / 'tools':
        return types.SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0x400)
    return original_lstat(path, *args, **kwargs)
def read(path, limit):
    local.name = path.stem
    return original(path, limit)
library._read = read
pathlib.Path.lstat = lstat
try: loader.assert_intact()
except library.VerificationError as error: assert str(error) == 'PATH_ALIAS'
else: raise AssertionError('alias accepted')
''', sources=self.sources())

    def test_actual_changed_missing_oversized_and_hardlinked_sources(self):
        mutations = [
            "target.write_bytes(b'VALUE = 99\\n')",
            'target.unlink()',
            "target.write_bytes(b'x' * (library.MAX_SOURCE + 1))",
            "import os; os.link(target, root / 'synthetic-hardlink')",
            "copy = root / 'replacement'; copy.write_bytes(target.read_bytes()); copy.replace(target)",
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.scenario('''
loader = construct().install()
target = root / 'tools/source_21.py'
''' + mutation + '''
try: loader.assert_intact()
except (library.VerificationError, FileNotFoundError): pass
else: raise AssertionError('changed source accepted')
''', sources=self.sources())


if __name__ == '__main__':
    unittest.main()
