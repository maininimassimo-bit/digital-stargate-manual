"""Pinned literal entry tests with synthetic project sources, no native driver."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.scientific_transients.native_verified_bootstrap import ENTRY, _pin, _bytes

HERE = Path(__file__).parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class BootstrapTests(unittest.TestCase):
    def scenario(self, *, change=None, source=b"def main(session):\n    assert session.assert_intact()\n    print('SYNTHETIC_ENTRY_REACHED')\n",
                 flags=('-I', '-S', '-B'), success=True, error=None):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            bootstrap, loader = root/'bootstrap.py', root/'loader.py'
            bootstrap.write_bytes((HERE/'native_verified_bootstrap.py').read_bytes())
            loader.write_bytes((HERE/'native_verified_loader.py').read_bytes())
            (root/'tools').mkdir()
            module = root/'tools/synthetic.py'; module.write_bytes(source)
            sources = dict(protocol='DSG_NATIVE_VERIFIED_SOURCES_V1', root=str(root), modules=[
                dict(name='tools.synthetic', path=str(Path('tools/synthetic.py')), sha256=sha(source),
                     byteLength=len(source), isPackage=False)])
            source_path = root/'sources.json'; source_path.write_bytes(json.dumps(sources).encode('ascii'))
            executable = str(Path(sys.executable).resolve())
            manifest = dict(protocol='DSG_NATIVE_BOOTSTRAP_MANIFEST_V1', bootstrapSha256=sha(bootstrap.read_bytes()),
                            entrySha256=sha(ENTRY.encode('ascii')), pythonVersion=sys.version,
                            pythonExecutable=executable, pythonExecutableSha256=sha(Path(executable).read_bytes()),
                            loaderPath=str(loader), loaderSha256=sha(loader.read_bytes()),
                            sourcesManifestPath=str(source_path), sourcesManifestSha256=sha(source_path.read_bytes()),
                            entryModule='tools.synthetic', entryCallable='main')
            if change:
                change(root, manifest)
            manifest_path=root/'bootstrap-manifest.json'
            raw=json.dumps(manifest).encode('ascii'); manifest_path.write_bytes(raw)
            result = subprocess.run([executable, *flags, '-c', ENTRY, str(bootstrap),
                                     manifest['bootstrapSha256'], str(manifest_path), sha(raw)],
                                    capture_output=True, text=True, timeout=20,
                                    env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1'})
            if success:
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn('SYNTHETIC_ENTRY_REACHED', result.stdout)
            else:
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertNotIn('SYNTHETIC_ENTRY_REACHED', result.stdout)
                if error is not None:
                    self.assertIn(error, result.stderr)
            return result

    def test_exact_pinned_literal_entry(self):
        self.scenario()

    def test_bootstrap_changed_before_verification(self):
        self.scenario(change=lambda root, m: (root/'bootstrap.py').write_bytes(b"print('SYNTHETIC_ENTRY_REACHED')"), success=False, error='BOOTSTRAP_SOURCE_HASH')

    def test_loader_changed_before_verification(self):
        self.scenario(change=lambda root, m: (root/'loader.py').write_bytes(b"print('SYNTHETIC_ENTRY_REACHED')"), success=False, error='BOOTSTRAP_PIN_MISMATCH')

    def test_source_changed_before_verification(self):
        self.scenario(change=lambda root, m: (root/'tools/synthetic.py').write_bytes(b"print('SYNTHETIC_ENTRY_REACHED')"), success=False, error='SOURCE_HASH')

    def test_wrong_literal_entry_pin(self):
        self.scenario(change=lambda root, m: m.update(entrySha256='0'*64), success=False, error='BOOTSTRAP_ENTRY_PIN')

    def test_wrong_runtime_version(self):
        self.scenario(change=lambda root, m: m.update(pythonVersion='unapproved runtime'), success=False, error='BOOTSTRAP_RUNTIME')

    def test_wrong_runtime_executable_pin(self):
        self.scenario(change=lambda root, m: m.update(pythonExecutableSha256='0'*64), success=False, error='BOOTSTRAP_PIN_MISMATCH')

    def test_unpinned_entry_module(self):
        self.scenario(change=lambda root, m: m.update(entryModule='tools.unknown'), success=False, error='BOOTSTRAP_ENTRY_NOT_PINNED')

    def test_unknown_manifest_field(self):
        self.scenario(change=lambda root, m: m.update(extra=True), success=False, error='BOOTSTRAP_SCHEMA')

    def test_nonisolated_interpreter_rejected(self):
        self.scenario(flags=('-S', '-B'), success=False, error='BOOTSTRAP_ISOLATION')

    def test_manifest_source_closure_changed_during_entry(self):
        self.scenario(source=b"def main(session):\n    from pathlib import Path\n    p=Path(__file__).parent.parent/'sources.json'\n    p.write_bytes(b'{}')\n    session.assert_intact()\n    print('SYNTHETIC_ENTRY_REACHED')\n", success=False, error='BOOTSTRAP_CLOSURE_CHANGED')

    def test_loader_source_closure_changed_during_entry(self):
        self.scenario(source=b"def main(session):\n    from pathlib import Path\n    p=Path(__file__).parent.parent/'loader.py'\n    p.write_bytes(p.read_bytes()+b'\\n')\n    session.assert_intact()\n    print('SYNTHETIC_ENTRY_REACHED')\n", success=False, error='BOOTSTRAP_CLOSURE_CHANGED')

    def test_same_byte_bootstrap_replacement_rejected_by_live_gate(self):
        self.scenario(source=b"def main(session):\n    from pathlib import Path\n    p=Path(__file__).parent.parent/'bootstrap.py'\n    q=p.with_name('replacement.py')\n    q.write_bytes(p.read_bytes())\n    q.replace(p)\n    session.assert_intact()\n    print('SYNTHETIC_ENTRY_REACHED')\n", success=False, error='BOOTSTRAP_CLOSURE_CHANGED')

    def test_entry_exception_propagates(self):
        self.scenario(source=b"def main(session):\n    raise RuntimeError('synthetic failure')\n", success=False, error='synthetic failure')

    def test_same_bytes_replacement_between_pin_and_snapshot_rejected(self):
        for name in ['loader.py', 'sources.json', 'bootstrap-manifest.json']:
            with self.subTest(role=name):
                def change(root, manifest):
                    # Explicit synthetic fault hook in the private fixture only.
                    # The production _pin result is captured, then its file is replaced.
                    hook = f'''
_original_pin = _pin
_injected = False
def _pin(path, expected, limit):
    global _injected
    result = _original_pin(path, expected, limit)
    if Path(path).name == {name!r} and not _injected:
        _injected = True
        target = Path(path)
        replacement = target.with_name('same-byte-replacement')
        replacement.write_bytes(target.read_bytes())
        replacement.replace(target)
    return result
'''
                    path = root/'bootstrap.py'
                    path.write_bytes(path.read_bytes() + hook.encode('ascii'))
                    manifest['bootstrapSha256'] = sha(path.read_bytes())
                result = self.scenario(change=change, success=False)
                self.assertIn('BOOTSTRAP_CLOSURE_CHANGED', result.stderr)

    def test_descriptor_identity_returned_for_synthetic_executable_copy(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary).resolve()/'python-copy.exe'
            raw = Path(sys.executable).read_bytes()
            path.write_bytes(raw)
            original, original_identity = _pin(path, sha(raw), 16777216)
            replacement = path.with_name('replacement.exe')
            replacement.write_bytes(raw)
            replacement.replace(path)
            current, current_identity = _bytes(path, 16777216)
            self.assertEqual(original, current)
            self.assertNotEqual(original_identity, current_identity)

    def test_live_source_attestation_includes_verified_bootstrap_buffers(self):
        self.scenario(source=b"def main(session):\n    from pathlib import Path\n    import hashlib\n    rows=session.attest_sources()\n    assert set(rows)=={'tools.synthetic','_dsg_verified_bootstrap','_dsg_pinned_source_loader'}\n    for row in rows.values():\n        raw=Path(row['path']).read_bytes()\n        assert hashlib.sha256(raw).hexdigest()==row['sha256']\n        assert len(raw)==row['byteLength']\n    rows['tools.synthetic']['sha256']='0'*64\n    assert session.attest_sources()['tools.synthetic']['sha256']!='0'*64\n    print('SYNTHETIC_ENTRY_REACHED')\n")

    def test_bootstrap_attestation_is_a_copy_and_matches_live_runtime(self):
        self.scenario(source=b"def main(session):\n    import sys,hashlib\n    from pathlib import Path\n    b=session.attest_bootstrap()\n    assert b['expectedPythonVersion']==sys.version\n    assert b['pythonExecutable']==Path(sys.executable).as_posix()\n    assert b['pythonExecutableSha256']==hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest()\n    b['bootstrapManifestSha256']='0'*64\n    assert session.attest_bootstrap()['bootstrapManifestSha256']!='0'*64\n    print('SYNTHETIC_ENTRY_REACHED')\n")

    def test_source_attestation_refuses_changed_source_instead_of_hashing_it_as_executed(self):
        self.scenario(source=b"def main(session):\n    from pathlib import Path\n    Path(__file__).write_bytes(b'# altered source')\n    session.attest_sources()\n    print('SYNTHETIC_ENTRY_REACHED')\n",success=False,error='SOURCE_IDENTITY_CHANGED')


if __name__ == '__main__':
    unittest.main()
