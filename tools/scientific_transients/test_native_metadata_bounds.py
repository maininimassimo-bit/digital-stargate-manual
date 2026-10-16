"""Synthetic metadata only; no native process, images or scientific claims."""
import os
from pathlib import Path
import stat
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools.scientific_transients import native_publication as pub


class NativeMetadataBoundsTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name).resolve(); self.root=self.base/'metadata'; self.root.mkdir()

    def file(self,name='synthetic.json',size=1):
        path=self.root/name
        with path.open('xb') as stream: stream.truncate(size)
        return path

    def test_flat_valid_tree_factors_ancestor_checks_without_caching_invocations(self):
        for i in range(64): self.file(str(i))
        with patch.object(pub,'safe_path',wraps=pub.safe_path) as checked:
            self.assertIsNone(pub._metadata_bound(self.root)); self.assertEqual(checked.call_count,2)
            pub._metadata_bound(self.root); self.assertEqual(checked.call_count,4)

    def test_global_entry_boundary_and_new_entry_on_next_scan(self):
        for i in range(256): self.file(str(i),0)
        pub._metadata_bound(self.root); self.file('excess',0)
        with self.assertRaisesRegex(Exception,'PUBLICATION_METADATA_ENTRIES'): pub._metadata_bound(self.root)

    def test_global_byte_boundary_not_reset_between_directories(self):
        self.file('first',8*pub.MIB); sub=self.root/'nested'; sub.mkdir()
        with (sub/'second').open('xb') as stream: stream.truncate(8*pub.MIB)
        pub._metadata_bound(self.root); self.file('excess',1)
        with self.assertRaisesRegex(Exception,'PUBLICATION_METADATA_AGGREGATE'): pub._metadata_bound(self.root)

    def test_directory_depth_eight_allowed_nine_rejected(self):
        path=self.root
        for i in range(8): path=path/str(i); path.mkdir()
        pub._metadata_bound(self.root); (path/'too-deep').mkdir()
        with self.assertRaisesRegex(Exception,'PUBLICATION_METADATA_DEPTH'): pub._metadata_bound(self.root)

    def test_hardlinked_metadata_rejected(self):
        path=self.file(); os.link(path,self.root/'alias')
        with self.assertRaisesRegex(Exception,'PUBLICATION_METADATA_FILE'): pub._metadata_bound(self.root)

    def test_child_reparse_rejected_before_directory_recursion(self):
        child=self.root/'reparse'; child.mkdir(); original=Path.lstat
        def info(path,*args,**kwargs):
            if path==child: return SimpleNamespace(st_mode=stat.S_IFDIR,st_file_attributes=0x400)
            return original(path,*args,**kwargs)
        with patch.object(Path,'lstat',info):
            with self.assertRaisesRegex(Exception,'LOCAL_LINK_OR_REPARSE'): pub._metadata_bound(self.root)

    def test_nonregular_entry_rejected_without_opening_it(self):
        child=self.file(); original=Path.lstat
        def info(path,*args,**kwargs):
            if path==child: return SimpleNamespace(st_mode=stat.S_IFIFO,st_file_attributes=0)
            return original(path,*args,**kwargs)
        with patch.object(Path,'lstat',info):
            with self.assertRaisesRegex(Exception,'PUBLICATION_METADATA_FILE'): pub._metadata_bound(self.root)

    def test_permission_and_vanished_child_errors_propagate(self):
        child=self.file(); original=Path.lstat
        for error in [PermissionError('SYNTHETIC'),FileNotFoundError('SYNTHETIC')]:
            def info(path,*args,**kwargs):
                if path==child: raise error
                return original(path,*args,**kwargs)
            with self.subTest(error=type(error)), patch.object(Path,'lstat',info):
                with self.assertRaises(type(error)): pub._metadata_bound(self.root)

    def test_empty_root_symlink_is_rejected(self):
        target=self.base/'outside-empty'; target.mkdir(); alias=self.base/'root-alias'
        try: os.symlink(target,alias,target_is_directory=True)
        except OSError as error: self.skipTest('Synthetic directory symlink privilege unavailable: '+type(error).__name__)
        with self.assertRaisesRegex(Exception,'LOCAL_LINK_OR_REPARSE'): pub._metadata_bound(alias)

    def test_identical_directory_replacement_during_enumeration_rejected(self):
        child=self.file('one',0); original=Path.iterdir; swapped=False
        displaced=self.base/'metadata-original'
        self.assertTrue(self.root.resolve().is_relative_to(self.base))
        self.assertTrue(displaced.resolve().is_relative_to(self.base))
        def rows(path):
            nonlocal swapped
            for item in list(original(path)):
                yield item
                if path==self.root and not swapped:
                    path.rename(displaced); path.mkdir(); (path/child.name).write_bytes(b''); swapped=True
        with patch.object(Path,'iterdir',rows):
            with self.assertRaisesRegex(Exception,'PUBLICATION_METADATA_DIRECTORY_CHANGED'): pub._metadata_bound(self.root)
        self.assertTrue(swapped)

    def test_queued_directory_replacement_cannot_adopt_new_identity(self):
        child=self.root/'nested'; child.mkdir(); original=pub.safe_path; swapped=False
        displaced=self.base/'nested-original'
        self.assertTrue(child.resolve().is_relative_to(self.base))
        self.assertTrue(displaced.resolve().is_relative_to(self.base))
        def checked(path):
            nonlocal swapped
            if path==child and not swapped:
                child.rename(displaced); child.mkdir(); swapped=True
            return original(path)
        with patch.object(pub,'safe_path',side_effect=checked):
            with self.assertRaisesRegex(Exception,'PUBLICATION_METADATA_DIRECTORY_CHANGED'): pub._metadata_bound(self.root)
        self.assertTrue(swapped)


if __name__=='__main__': unittest.main()
