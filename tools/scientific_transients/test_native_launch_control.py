"""Synthetic code byte pins and attestation callbacks; no native process or pixels."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from tools.scientific_transients import native_launch_control as control


def sha(raw): return hashlib.sha256(raw).hexdigest()


class LaunchControlTests(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory(); self.addCleanup(self.temporary.cleanup)
        self.root=Path(self.temporary.name).resolve()
        self.path=self.root/'launch-control.json'
        self.rows=[]
        for role in sorted(control.FIXED):
            path=self.root/(role.lower()+'.synthetic')
            raw=('SYNTHETIC_CODE_OR_METADATA_'+role).encode('ascii');path.write_bytes(raw)
            self.rows.append(dict(role=role,name=path.name,path=path.as_posix(),sha256=sha(raw),byteLength=len(raw)))
        source=self.root/'parent_source.py';raw=b'# synthetic source bytes, never executed\n';source.write_bytes(raw)
        self.sources={'tools.synthetic':dict(path=source.as_posix(),sha256=sha(raw),byteLength=len(raw))}
        self.rows.append(dict(role='PARENT_SOURCE',name='tools.synthetic',**self.sources['tools.synthetic']))
        self.value=dict(protocol='DSG_NATIVE_LINEAR_LAUNCH_CONTROL_V1',operationRef='a'*32,
            sealSha256=sha(b'synthetic-seal'),grantSha256=sha(b'synthetic-grant'),files=self.rows,
            ownerNonce='b'*32,processSessionRef='c'*32,expectedPixInsightVersion='SYNTHETIC_PI',
            expectedPythonVersion='SYNTHETIC_PYTHON',parentDeadlineUTC='2026-10-16T10:03:00Z')
        for key,role in control.HASH_ROLES.items():
            self.value[key]=next(r['sha256'] for r in self.rows if r['role']==role)
        self.guard_calls=0

    def write(self):
        raw=json.dumps(self.value).encode('ascii');self.path.write_bytes(raw)
        return sha(raw)

    def guard(self): self.guard_calls+=1

    def inspect(self, *, loaded=None, guard=None, digest=None):
        digest=self.write() if digest is None else digest
        return control.inspect_launch_control(self.path.as_posix(),digest,
            loaded_sources=loaded or (lambda:copy.deepcopy(self.sources)),guard=guard or self.guard)

    def test_full_fixed_and_attested_source_closure_read_only(self):
        snapshot=self.inspect();self.assertTrue(snapshot.verify());self.assertGreater(self.guard_calls,20)
        self.assertEqual(snapshot.control,self.value)
        self.assertEqual(len(list(self.root.iterdir())),len(self.rows)+1)

    def test_unknown_and_missing_fields(self):
        self.value['extra']=True
        with self.assertRaisesRegex(control.ProtocolError,'FIELDS'):self.inspect()
        del self.value['extra'];del self.value['grantSha256']
        with self.assertRaisesRegex(control.ProtocolError,'FIELDS'):self.inspect()

    def test_duplicate_json_key_rejected(self):
        raw=b'{"protocol":1,"protocol":2}';self.path.write_bytes(raw)
        with self.assertRaisesRegex(control.ProtocolError,'JSON_DUPLICATE'):self.inspect(digest=sha(raw))

    def test_missing_fixed_role(self):
        self.rows.pop(0)
        with self.assertRaisesRegex(control.ProtocolError,'REQUIRED_ROLES'):self.inspect()

    def test_duplicate_fixed_role(self):
        self.rows.append(copy.deepcopy(self.rows[0]))
        with self.assertRaisesRegex(control.ProtocolError,'DUPLICATE_ROLE'):self.inspect()

    def test_unattested_or_missing_loaded_module(self):
        with self.assertRaisesRegex(control.ProtocolError,'LOADED_MISMATCH'):
            self.inspect(loaded=lambda:{'tools.unknown':copy.deepcopy(self.sources['tools.synthetic'])})

    def test_changed_attested_source_pin(self):
        source=copy.deepcopy(self.sources);source['tools.synthetic']['sha256']='0'*64
        with self.assertRaisesRegex(control.ProtocolError,'LOADED_MISMATCH'):self.inspect(loaded=lambda:source)

    def test_role_top_hash_binding(self):
        self.value['entrySha256']='0'*64
        with self.assertRaisesRegex(control.ProtocolError,'ROLE_BINDING'):self.inspect()

    def test_source_raw_hash_and_identity_remain_pinned(self):
        snapshot=self.inspect();row=self.rows[-1];path=Path(row['path'])
        replacement=path.with_name('replacement.py');replacement.write_bytes(path.read_bytes());replacement.replace(path)
        with self.assertRaisesRegex(control.ProtocolError,'IDENTITY'):snapshot.verify()

    def test_code_changed_after_snapshot(self):
        snapshot=self.inspect();Path(self.rows[0]['path']).write_bytes(b'SYNTHETIC_CHANGE')
        with self.assertRaises(control.ProtocolError):snapshot.verify()

    def test_live_attested_set_changed_after_snapshot(self):
        snapshot=self.inspect();self.sources['tools.unknown']=dict(self.sources['tools.synthetic'])
        with self.assertRaisesRegex(control.ProtocolError,'LOADED_CHANGED'):snapshot.verify()

    def test_control_object_mutation_does_not_change_snapshot(self):
        snapshot=self.inspect();value=snapshot.control;value['ownerNonce']='d'*32
        self.assertEqual(snapshot.control['ownerNonce'],'b'*32);self.assertTrue(snapshot.verify())

    def test_control_file_changed_after_snapshot(self):
        snapshot=self.inspect();self.value['ownerNonce']='d'*32;self.write()
        with self.assertRaises(control.ProtocolError):snapshot.verify()

    def test_bad_calendar_date_and_session(self):
        self.value['parentDeadlineUTC']='2026-02-30T10:03:00Z'
        with self.assertRaisesRegex(control.ProtocolError,'TIME'):self.inspect()
        self.value['parentDeadlineUTC']='2026-10-16T10:03:00Z';self.value['ownerNonce']='bad'
        with self.assertRaisesRegex(control.ProtocolError,'SESSION'):self.inspect()

    def test_size_bool_empty_nonpackage_and_oversized_code(self):
        for size in [True,0,control.MIB+1]:
            self.rows[0]['byteLength']=size
            with self.assertRaisesRegex(control.ProtocolError,'SIZE'):self.inspect()

    def test_empty_package_initializer_is_allowed(self):
        path=self.root/'__init__.py';path.write_bytes(b'')
        row=self.rows[-1];row.update(path=path.as_posix(),sha256=sha(b''),byteLength=0)
        self.sources['tools.synthetic']={k:row[k] for k in ['path','sha256','byteLength']}
        self.assertTrue(self.inspect().verify())

    def test_noncanonical_path(self):
        self.rows[-1]['path']=self.root.as_posix()+'/../outside.py'
        with self.assertRaises(control.ProtocolError):self.inspect()

    def test_duplicate_source(self):
        self.rows.append(copy.deepcopy(self.rows[-1]))
        with self.assertRaisesRegex(control.ProtocolError,'DUPLICATE_SOURCE'):self.inspect()

    def test_callback_failure_and_clock_guard_failure_propagate(self):
        def fail():raise RuntimeError('SYNTHETIC_LIVE_FAILURE')
        with self.assertRaisesRegex(RuntimeError,'SYNTHETIC_LIVE_FAILURE'):self.inspect(guard=fail)
        with self.assertRaisesRegex(RuntimeError,'SYNTHETIC_LIVE_FAILURE'):self.inspect(loaded=fail)

    def test_files_and_json_bounds(self):
        self.value['files']=self.rows*9
        with self.assertRaisesRegex(control.ProtocolError,'JSON_ARRAY'):self.inspect()

    def test_hardlinked_code_rejected(self):
        import os
        os.link(self.rows[0]['path'],self.root/'hardlink')
        with self.assertRaisesRegex(control.ProtocolError,'FILE'):self.inspect()

    def test_raw_control_hash_is_external(self):
        self.write()
        with self.assertRaisesRegex(control.ProtocolError,'HASH'):self.inspect(digest='0'*64)

    def test_multichunk_progress_keeps_full_boundary_guards_and_exact_bytes(self):
        path=self.root/'large.synthetic'; raw=b'SYNTHETIC_BYTE'*30000; path.write_bytes(raw)
        full=[]; progress=[]
        pin,captured=control._pin(path.as_posix(),sha(raw),control.MIB,lambda:full.append(True),
            capture=True,progress_guard=lambda:progress.append(True))
        self.assertEqual(captured,raw); self.assertEqual(pin[2],len(raw))
        self.assertEqual(len(full),2); self.assertEqual(len(progress),(len(raw)+65535)//65536)

    def test_midstream_source_failure_rejected_by_final_full_gate(self):
        path=self.root/'large.synthetic'; raw=b'SYNTHETIC'*20000; path.write_bytes(raw)
        changed=False
        def full():
            if changed: raise RuntimeError('SYNTHETIC_SOURCE_CLOSURE_CHANGED')
        def progress():
            nonlocal changed
            changed=True
        with self.assertRaisesRegex(RuntimeError,'SOURCE_CLOSURE_CHANGED'):
            control._pin(path.as_posix(),sha(raw),control.MIB,full,progress_guard=progress)

    def test_progress_failure_interrupts_stream_and_never_runs_final_positive_gate(self):
        path=self.root/'large.synthetic'; raw=b'SYNTHETIC'*20000; path.write_bytes(raw)
        full=[]; progress=[]
        def tick():
            progress.append(True)
            if len(progress)==2: raise RuntimeError('SYNTHETIC_ORIGINAL_DEADLINE')
        with self.assertRaisesRegex(RuntimeError,'ORIGINAL_DEADLINE'):
            control._pin(path.as_posix(),sha(raw),control.MIB,lambda:full.append(True),progress_guard=tick)
        self.assertEqual(len(full),1); self.assertEqual(len(progress),2)

    def test_empty_source_keeps_both_full_gates_with_no_chunk(self):
        path=self.root/'empty.synthetic'; path.write_bytes(b''); full=[]; progress=[]
        control._pin(path.as_posix(),sha(b''),control.MIB,lambda:full.append(True),
            progress_guard=lambda:progress.append(True))
        self.assertEqual(len(full),2); self.assertEqual(progress,[])

    def test_invalid_progress_callback_is_not_silently_defaulted(self):
        for invalid in [False,0,'',[],{}]:
            with self.subTest(value=invalid), self.assertRaisesRegex(control.ProtocolError,'GUARD'):
                control._pin(self.path.as_posix(),'a'*64,control.MIB,self.guard,progress_guard=invalid)

    def test_snapshot_retains_separate_callbacks_and_loaded_set_failure(self):
        calls=[]; digest=self.write()
        snapshot=control.inspect_launch_control(self.path.as_posix(),digest,
            loaded_sources=lambda:self.sources,guard=self.guard,progress_guard=lambda:calls.append(True))
        self.assertGreater(len(calls),0); before=len(calls)
        snapshot.verify(); self.assertGreater(len(calls),before)
        self.sources['tools.synthetic']['sha256']='0'*64
        with self.assertRaisesRegex(control.ProtocolError,'LOADED_CHANGED'): snapshot.verify()

    def test_midstream_same_byte_source_replacement_is_seen_at_full_end(self):
        source=self.root/'original-source.py'; source.write_bytes(b'# SYNTHETIC_CODE\n')
        original=source.stat(); target=self.root/'large.synthetic'; raw=b'SYNTHETIC'*20000; target.write_bytes(raw)
        replaced=False
        def full():
            if source.stat().st_ino!=original.st_ino: raise RuntimeError('SYNTHETIC_SOURCE_IDENTITY_CHANGED')
        def progress():
            nonlocal replaced
            if not replaced:
                other=source.with_name('replacement.py'); other.write_bytes(source.read_bytes()); other.replace(source)
                replaced=True
        with self.assertRaisesRegex(RuntimeError,'SOURCE_IDENTITY_CHANGED'):
            control._pin(target.as_posix(),sha(raw),control.MIB,full,progress_guard=progress)
        self.assertEqual(source.read_bytes(),b'# SYNTHETIC_CODE\n')

    def test_attested_module_change_during_snapshot_progress_blocks_result(self):
        changed=False
        def progress():
            if changed: self.sources['tools.synthetic']['sha256']='0'*64
        digest=self.write()
        snapshot=control.inspect_launch_control(self.path.as_posix(),digest,
            loaded_sources=lambda:self.sources,guard=self.guard,progress_guard=progress)
        changed=True
        with self.assertRaisesRegex(control.ProtocolError,'LOADED_CHANGED'): snapshot.verify()


if __name__=='__main__':unittest.main()
