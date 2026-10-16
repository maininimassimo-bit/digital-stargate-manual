"""Fresh Python subprocesses and synthetic source literals only; no native starts."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

LOADER = Path(__file__).with_name('native_verified_loader.py').resolve()


class VerifiedLoaderTests(unittest.TestCase):
    def scenario(self, body, *, sources=None, manifest_edit=''):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            rows = []
            for name, raw in (sources or {'tools.synthetic': b'VALUE = 17\n'}).items():
                package = name.endswith('.__init__')
                actual = name.removesuffix('.__init__')
                relative = Path(*actual.split('.')) / '__init__.py' if package else Path(*actual.split('.')).with_suffix('.py')
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
                rows.append(dict(name=actual, path=str(relative), sha256=hashlib.sha256(raw).hexdigest(),
                                 byteLength=len(raw), isPackage=package))
            value = dict(protocol='DSG_NATIVE_VERIFIED_SOURCES_V1', root=str(root), modules=rows)
            script = f'''import importlib.util, json, hashlib, sys, types, pathlib, importlib
spec = importlib.util.spec_from_file_location('_reviewed_loader_fixture', {str(LOADER)!r})
library = importlib.util.module_from_spec(spec)
spec.loader.exec_module(library)
value = json.loads({json.dumps(value)!r})
root = pathlib.Path(value['root'])
{manifest_edit}
raw = json.dumps(value).encode('ascii')
def construct():
    return library.VerifiedSources(raw, hashlib.sha256(raw).hexdigest())
def reject(action):
    try: action()
    except library.VerificationError: return
    raise AssertionError('expected rejection')
{body}
'''
            result = subprocess.run([sys.executable, '-I', '-S', '-B', '-c', script],
                                    capture_output=True, text=True, timeout=15,
                                    env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_verified_source_and_explicit_namespace(self):
        self.scenario('loader = construct().install()\nimport tools.synthetic\nassert tools.synthetic.VALUE == 17\nassert loader.assert_intact()')

    def test_changed_source_rejected_before_execution(self):
        self.scenario("(root/'tools/synthetic.py').write_bytes(b'raise RuntimeError()')\nreject(construct)")

    def test_same_verified_buffer_executes_after_disk_change_then_gate_rejects(self):
        self.scenario("loader = construct().install()\n(root/'tools/synthetic.py').write_bytes(b'VALUE = 99')\nimport tools.synthetic\nassert tools.synthetic.VALUE == 17\nreject(loader.assert_intact)")

    def test_prepopulated_project_namespace_rejected(self):
        self.scenario("sys.modules['tools'] = types.ModuleType('tools')\nreject(construct().install)")

    def test_replaced_module_identity_rejected(self):
        self.scenario("loader = construct().install()\nimport tools.synthetic\nsys.modules['tools.synthetic'] = types.ModuleType('tools.synthetic')\nreject(loader.assert_intact)")

    def test_unknown_project_import_blocks_filesystem_fallback(self):
        self.scenario("loader = construct().install()\n(root/'tools/unknown.py').write_bytes(b'raise RuntimeError(123)')\nsys.path.insert(0, str(root))\nreject(lambda: importlib.import_module('tools.unknown'))")

    def test_reload_refused(self):
        self.scenario("loader = construct().install()\nimport tools.synthetic\nreject(lambda: importlib.reload(tools.synthetic))")

    def test_modified_loader_identity_rejected(self):
        self.scenario("loader = construct().install()\nimport tools.synthetic\ntools.synthetic.__loader__ = None\nreject(loader.assert_intact)")

    def test_manifest_duplicate_module_rejected(self):
        self.scenario('reject(construct)', manifest_edit="value['modules'].append(value['modules'][0].copy())")

    def test_manifest_unknown_field_rejected(self):
        self.scenario('reject(construct)', manifest_edit="value['extra'] = True")

    def test_manifest_duplicate_json_key_rejected(self):
        self.scenario("raw = b'{\"protocol\":1,\"protocol\":2}'\nreject(construct)")

    def test_empty_package_initializer_verified(self):
        self.scenario('loader = construct().install()\nimport tools.synthetic\nassert tools.synthetic.VALUE == 17\nassert loader.assert_intact()',
                      sources={'tools.__init__': b'', 'tools.synthetic': b'VALUE = 17\n'})

    def test_parent_plain_module_cannot_be_package(self):
        self.scenario('reject(construct)', sources={'tools.synthetic': b'VALUE=1', 'tools.synthetic.child': b'VALUE=2'})

    def test_module_path_escape_rejected(self):
        self.scenario('reject(construct)', manifest_edit="value['modules'][0]['path'] = '../outside.py'")

    def test_source_and_module_count_limits(self):
        self.scenario('reject(construct)', manifest_edit="value['modules'] *= 129")
        self.scenario('reject(construct)', sources={'tools.synthetic': b' ' * 1048577})

    def test_hardlinked_source_rejected(self):
        self.scenario("os = importlib.import_module('os')\nos.link(root/'tools/synthetic.py', root/'duplicate.py')\nreject(construct)")

    def test_unknown_module_injected_after_load_rejected(self):
        self.scenario("loader = construct().install()\nimport tools.synthetic\nsys.modules['tools.unknown'] = types.ModuleType('tools.unknown')\nreject(loader.assert_intact)")

    def test_unpinned_pyc_not_executed(self):
        self.scenario("loader = construct().install()\n(root/'tools/synthetic.pyc').write_bytes(b'not approved bytecode')\nimport tools.synthetic\nassert tools.synthetic.VALUE == 17\nassert loader.assert_intact()")

    def test_identical_bytes_replacement_rejected(self):
        self.scenario("loader = construct().install()\nimport tools.synthetic\np = root/'tools/synthetic.py'\nq = root/'new.py'\nq.write_bytes(p.read_bytes())\nq.replace(p)\nreject(loader.assert_intact)")

    def test_direct_exec_without_install_rejected(self):
        self.scenario("loader = construct()\nspec = importlib.machinery.ModuleSpec('tools.synthetic', loader)\nmodule = importlib.util.module_from_spec(spec)\nsys.modules['tools.synthetic'] = module\nreject(lambda: loader.exec_module(module))\nassert not hasattr(module, 'VALUE')")

    def test_fabricated_spec_after_install_rejected(self):
        self.scenario("loader = construct().install()\nspec = importlib.machinery.ModuleSpec('tools.synthetic', loader)\nmodule = importlib.util.module_from_spec(spec)\nsys.modules['tools.synthetic'] = module\nreject(lambda: loader.exec_module(module))\nassert not hasattr(module, 'VALUE')")


if __name__ == '__main__':
    unittest.main()
