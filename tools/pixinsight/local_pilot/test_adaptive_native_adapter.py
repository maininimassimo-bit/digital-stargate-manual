import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from .adaptive_native_adapter import validate_runtime_files
from .image_analysis import fingerprint
from .intake import sha


class RuntimeBindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.files=[]
        for name in ('suite','blur','noise','star','detector','core'):
            path=self.root/name;path.write_text(name)
            self.files.append({'path':str(path),'sha256':fingerprint(path)})
        self.runtime={'suiteSha256':self.files[0]['sha256'],
                      'models':{k:{'fileSha256':self.files[i]['sha256']} for i,k in enumerate(('BLURX','NOISEX','STARX'),1)},
                      'dependenciesSha256':sha(sorted(self.files[4:],key=lambda r:r['path']))}
        guard=patch('tools.pixinsight.local_pilot.adaptive_native_adapter.local_directory',lambda p:p)
        guard.start();self.addCleanup(guard.stop)

    def test_complete_pinned_runtime_accepts_only_actual_files(self):
        validate_runtime_files(self.runtime,self.files)
        Path(self.files[-1]['path']).write_text('substituted')
        with self.assertRaises(ValueError):validate_runtime_files(self.runtime,self.files)

    def test_missing_model_or_dependency_cannot_satisfy_runtime(self):
        for removed in (0,1,2,3,4,5):
            with self.subTest(removed=removed):
                with self.assertRaises(ValueError):validate_runtime_files(self.runtime,self.files[:removed]+self.files[removed+1:])

    def test_dependency_path_substitution_changes_binding(self):
        values=copy.deepcopy(self.files)
        duplicate=self.root/'other-detector';duplicate.write_text('detector')
        values[4]['path']=str(duplicate)
        with self.assertRaises(ValueError):validate_runtime_files(self.runtime,values)


if __name__=='__main__':unittest.main()
