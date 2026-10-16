"""Synthetic plans/authorization records, fake bootstrap/locks; never native consent."""
import datetime as dt
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import encode
from tools.scientific_transients import native_linear_preparation as preparation
from tools.scientific_transients import test_native_publication as fixture
from tools.scientific_transients import test_native_held_process as held_fixture
from tools.scientific_transients import native_linear_supervisor as lifecycle
from tools.scientific_transients import native_owned_closure as owned
from tools.scientific_transients.native_read_locks import NativeReadLocks


def sha(raw): return hashlib.sha256(raw).hexdigest()


class LinearPreparationTests(unittest.TestCase):
    def setUp(self):
        self.f=fixture.NativePublicationTests(); self.f.setUp(); self.addCleanup(self.f.doCleanups)
        f=self.f; self.base=f.root/'prepared'; self.base.mkdir(); self.mono=1
        self.input=f.root/'synthetic-inputs'; self.input.mkdir()
        raw=bytearray(b' '*2880+bytes(2880))
        for i,text in enumerate(['SIMPLE  =                    T','BITPIX  =                  -32',
                'NAXIS   =                    2','NAXIS1  =                    2','NAXIS2  =                    1','END']):
            raw[i*80:(i+1)*80]=text.ljust(80).encode('ascii')
        raw[2880:2888]=bytes.fromhex('40000000bf800000')  # Explicitly synthetic +2 and -1.
        self.source=bytes(raw); (self.input/'source.fits').write_bytes(self.source)
        (self.input/'kernel-spec.json').write_bytes(b'{"synthetic":"opaque model not evaluated by Python"}')
        lineage=dict(protocol='DSG_NATIVE_SOURCE_LINEAGE_V1',sourceSha256=sha(self.source),parentManifestSha256='8'*64,
            providerProductCardSha256='9'*64,upstreamPixInsightHistory='NOT_PRESENT_IN_SOURCE_FITS',
            interpretation='SOURCE_PROVENANCE_NOT_PHYSICAL_ACCEPTANCE')
        (self.input/'source-lineage.json').write_bytes(encode(lineage))
        def descriptor(path):
            raw=path.read_bytes(); return dict(path=path.as_posix(),sha256=sha(raw),byteLength=len(raw))
        self.descriptor=descriptor
        inputs=[dict(name=name,**descriptor(self.input/name)) for name in ['source.fits','kernel-spec.json','source-lineage.json']]
        for role,name in preparation.LIBRARIES.items():
            inputs.append(dict(name=name,**{k:f.fixed[role][k] for k in ['path','sha256','byteLength']}))
        files={row['name']:row for row in inputs}
        self.parameters=dict(protocol='DSG_NATIVE_LINEAR_MEASUREMENT_V2',operationRef=f.operation,purpose='DEVELOPMENT',
            expectedPixInsightVersion=f.control['expectedPixInsightVersion'],kernelSpecSha256=files['kernel-spec.json']['sha256'],
            lineageSha256=files['source-lineage.json']['sha256'],source=dict(sha256=sha(self.source),byteLength=len(self.source),
                primaryHeaderSha256=sha(self.source[:2880]),dataOffset=2880,width=2,height=1,sampleFormat='FLOAT32_BE',
                orientation='FITS_AXIS1_FAST_NO_FLIP',bscale=1,bzero=0),
            dependencies={key:f.fixed[role]['sha256'] for role,key in [('CORE','coreSha256'),('PARSER','parserSha256'),
                ('PRIMARY','primarySha256'),('WRAPPER','wrapperSha256')]},maxRuntimeSeconds=180,bindings=[],
            ownerNonce=f.control['ownerNonce'],processSessionRef=f.control['processSessionRef'])
        self.plan=dict(protocol='DSG_NATIVE_LINEAR_PREPARATION_V1',root=self.base.as_posix(),parameters=self.parameters,
            workFiles=inputs,resources=[{k:f.fixed[role][k] for k in ['role','path','sha256','byteLength']}
                                      for role in sorted(preparation.RESOURCES)])
        self.plan_path=f.root/'approved-plan.json'; self.approval_path=f.root/'synthetic-approval.json'
        self.approval=dict(protocol='DSG_NATIVE_LINEAR_HUMAN_SCOPE_V1',operationRef=f.operation,planSha256='0'*64,
            proposalSha256='7'*64,decisionRef='d'*32,permission='SINGLE_PREPARATION_SINGLE_START_WITH_OWNED_CLEANUP',
            authorizedUTC='2026-10-16T09:59:00Z',expiresUTC='2026-10-16T10:30:00Z',maxStarts=1,maxRuntimeSeconds=180,
            cloudAuthorized=False)
        sources=f.control_case.sources
        sources['tools.scientific_transients.native_linear_supervisor']={k:f.fixed['SUPERVISOR'][k] for k in ['path','sha256','byteLength']}
        prep_source=f.control_case.root/'preparation-source.py'; prep_source.write_bytes(b'# synthetic declared source, never executed\n')
        sources['tools.scientific_transients.native_linear_preparation']=descriptor(prep_source)
        self.save()
        # Portable metadata integration deliberately replaces native path rendering
        # and file-lock acquisition; the actual renderer has independent pure tests.
        self.renderer=patch.object(preparation,'render_entry',return_value=b'// SYNTHETIC_ENTRY_NOT_EXECUTED\r\n')
        self.renderer.start(); self.addCleanup(self.renderer.stop)
        def locks(rows,guard):
            group=object.__new__(NativeReadLocks); group._released=False
            group._held=[(object(),Path(row['path']),dict(row),()) for row in rows]
            return group
        self.lock_patch=patch.object(preparation,'NativeReadLocks',side_effect=locks)
        self.lock_patch.start(); self.addCleanup(self.lock_patch.stop)
        verify=patch.object(NativeReadLocks,'verify',return_value=None); verify.start(); self.addCleanup(verify.stop)
        spawn=patch('tools.scientific_transients.native_linear_supervisor._spawn_native',side_effect=AssertionError('NO_SPAWN'))
        self.spawn=spawn.start(); self.addCleanup(spawn.stop)

    def save(self):
        raw=encode(self.plan); self.plan_path.write_bytes(raw); self.plan_sha=sha(raw)
        self.approval['planSha256']=self.plan_sha; self.approval_path.write_bytes(encode(self.approval))
        self.approval_sha=sha(encode(self.approval))

    def context(self):
        return preparation.LinearAttemptPreparation(self.f.session,self.plan_path.as_posix(),self.plan_sha,
            monotonic=lambda:self.mono,wall=lambda:dt.datetime(2026,10,16,10,0,tzinfo=dt.timezone.utc))

    def prepare(self,context): return context.prepare(self.approval_path.as_posix(),self.approval_sha)

    def test_preparation_copies_only_opaque_bytes_and_returns_original_unstarted_supervisor(self):
        context=self.context(); supervisor=self.prepare(context)
        self.assertEqual(supervisor.diagnostic()['state'],'PREPARED_LIVE')
        self.assertEqual(context.diagnostic()['state'],'PREPARED_LIVE')
        self.assertFalse(supervisor.diagnostic()['startAttemptConsumed'])
        self.spawn.assert_not_called()
        work=self.base/'native-work'/self.f.operation
        self.assertEqual((work/'source.fits').read_bytes(),self.source)
        params=json.loads((work/'parameters.json').read_bytes())
        self.assertEqual(params,self.parameters)
        self.assertTrue(context.diagnostic()['grantCommitted'])
        self.assertEqual(context._records._budget,context._budget)
        self.assertIs(supervisor._records,context._records)
        self.assertTrue(any(path.name=='preparation-plan.json' for path,_,_ in context._records._pins))

    def test_constructor_does_no_preparation_io(self):
        context=self.context(); self.assertEqual(list(self.base.iterdir()),[])
        self.assertFalse(context.diagnostic()['attemptConsumed']); self.spawn.assert_not_called()

    def test_same_object_and_existing_directory_cannot_rearm_or_overwrite(self):
        context=self.context(); self.prepare(context)
        with self.assertRaisesRegex(Exception,'PREPARATION_REPLAY'): self.prepare(context)
        with self.assertRaisesRegex(Exception,'PREPARATION_SESSION_REPLAY'): self.prepare(self.context())
        fresh=preparation.LinearAttemptPreparation(type(self.f.session)(),self.plan_path.as_posix(),self.plan_sha,
            monotonic=lambda:self.mono,wall=lambda:dt.datetime(2026,10,16,10,0,tzinfo=dt.timezone.utc))
        with self.assertRaises(FileExistsError): self.prepare(fresh)
        self.spawn.assert_not_called()

    def test_changed_source_retains_partial_copy_and_no_grant(self):
        context=self.context(); path=self.input/'source.fits'; path.write_bytes(b'X'*len(self.source))
        with self.assertRaisesRegex(Exception,'PREPARATION_SOURCE_CHANGED'): self.prepare(context)
        work=self.base/'native-work'/self.f.operation
        self.assertTrue((work/'source.fits').exists())
        self.assertFalse((work/'launch-grant.json').exists())
        with self.assertRaisesRegex(Exception,'PREPARATION_REPLAY'): self.prepare(context)

    def test_scope_mismatch_blocks_before_private_directories(self):
        self.approval['operationRef']='f'*32; self.save(); context=self.context()
        with self.assertRaisesRegex(Exception,'PREPARATION_APPROVAL_SCOPE'): self.prepare(context)
        self.assertEqual(list(self.base.iterdir()),[])

    def test_failure_before_any_directory_still_consumes_original_bootstrap_session(self):
        self.approval['operationRef']='f'*32; self.save(); context=self.context()
        with self.assertRaisesRegex(Exception,'PREPARATION_APPROVAL_SCOPE'): self.prepare(context)
        self.assertEqual(list(self.base.iterdir()),[])
        self.approval['operationRef']=self.f.operation; self.save()
        with self.assertRaisesRegex(Exception,'PREPARATION_SESSION_REPLAY'): self.prepare(self.context())
        self.assertEqual(list(self.base.iterdir()),[])

    def test_expired_approval_cannot_create_a_fresh_grant(self):
        self.approval['expiresUTC']='2026-10-16T10:01:00Z'; self.save(); context=self.context()
        with self.assertRaisesRegex(Exception,'PREPARATION_APPROVAL_TIME'): self.prepare(context)
        self.assertFalse(context.diagnostic()['grantAttemptConsumed'])

    def test_low_free_space_stops_before_grant_without_cleanup(self):
        context=self.context()
        with patch.object(preparation.shutil,'disk_usage',return_value=SimpleNamespace(free=1024**3-1)):
            with self.assertRaisesRegex(Exception,'PREPARATION_FREE_SPACE'): self.prepare(context)
        work=self.base/'native-work'/self.f.operation
        self.assertTrue((work/'launch-seal.json').exists())
        self.assertFalse((work/'launch-grant.json').exists())

    def test_bad_resource_hash_rejected_before_private_directories(self):
        self.plan['resources'][0]['sha256']='0'*64; self.save(); context=self.context()
        with self.assertRaises(Exception): self.prepare(context)
        self.assertEqual(list(self.base.iterdir()),[])

    def test_boolean_geometry_cannot_become_integer_metadata(self):
        self.parameters['source']['width']=True; self.save(); context=self.context()
        with self.assertRaisesRegex(Exception,'PREPARATION_GEOMETRY_METADATA'): self.prepare(context)
        self.assertFalse(context.diagnostic()['grantAttemptConsumed'])

    def test_original_budget_expiry_cannot_be_reset_by_prepare(self):
        context=self.context(); self.mono=181
        with self.assertRaisesRegex(Exception,'NATIVE_BUDGET_EXPIRED'): self.prepare(context)
        self.assertEqual(list(self.base.iterdir()),[])

    def test_changed_plan_raw_pin_is_rejected_before_directories(self):
        context=self.context(); self.plan_path.write_bytes(self.plan_path.read_bytes()+b'\n')
        with self.assertRaisesRegex(Exception,'PREPARATION_PLAN_PIN'): self.prepare(context)
        self.assertEqual(list(self.base.iterdir()),[])

    def test_bad_declaration_card_stops_before_grant(self):
        card=dict(protocol='DSG_NATIVE_LINEAR_BINDING_CARD_V1',role='identity.gridSha256',referenceSha256='5'*64,
            sourceSha256=sha(self.source),kernelSpecSha256=self.parameters['kernelSpecSha256'],scope='WRONG_SCOPE')
        raw=encode(card); name='source-card-'+sha(raw)+'.json'; path=self.input/name; path.write_bytes(raw)
        self.plan['workFiles'].append(dict(name=name,**self.descriptor(path)))
        self.parameters['bindings']=[dict(role=card['role'],referenceSha256=card['referenceSha256'],cardSha256=sha(raw))]
        self.save(); context=self.context()
        with self.assertRaisesRegex(Exception,'PREPARATION_CARD_METADATA'): self.prepare(context)
        self.assertFalse(context.diagnostic()['grantAttemptConsumed'])

    def test_post_grant_write_failure_preserves_file_and_consumed_attempt_truthfully(self):
        context=self.context(); original=context._write_json
        def write(path,value):
            result=original(path,value)
            if path.name=='launch-grant.json': raise OSError('SYNTHETIC_AFTER_GRANT_WRITE')
            return result
        with patch.object(context,'_write_json',side_effect=write):
            with self.assertRaises(OSError): self.prepare(context)
        self.assertTrue((self.base/'native-work'/self.f.operation/'launch-grant.json').exists())
        self.assertTrue(context.diagnostic()['grantAttemptConsumed'])
        self.assertFalse(context.diagnostic()['grantCommitted'])
        with self.assertRaisesRegex(Exception,'PREPARATION_REPLAY'): self.prepare(context)

    def test_preparation_through_retained_before_image_failure_uses_only_fake_process(self):
        context=self.context(); supervisor=self.prepare(context)
        holder=held_fixture.HeldNativeProcessTests(); holder.setUp(); self.addCleanup(holder.doCleanups)
        def locks(rows,guard):
            group=object.__new__(NativeReadLocks); group._released=False
            group._held=[(object(),Path(row['path']),dict(row),()) for row in rows]; return group
        with patch.object(lifecycle,'_spawn_native',return_value=holder.process), patch.object(
                lifecycle,'_acquire_owner_locks',side_effect=locks): supervisor.start()
        r=context._records; work=r._work
        from tools.scientific_transients import native_publication as pub
        pin={path.name:row for path,row,_ in r._pins if path.parent==work}
        started=dict(protocol='DSG_NATIVE_LINEAR_STARTED_V1',operationRef=self.f.operation,
            parametersSha256=pin['parameters.json']['sha256'],sealSha256=r._binding['sealSha256'],
            pixInsightVersion=self.parameters['expectedPixInsightVersion'],maxStarts=1)
        (work/'started-native.json').write_bytes(encode(started)); (work/'native.log').write_bytes(b'SYNTHETIC_FAILURE_LOG')
        terminal=dict(protocol='DSG_NATIVE_LINEAR_TERMINAL_V1',operationRef=self.f.operation,state='FAILED_RETAINED',
            errorCode='SYNTHETIC_INVALID_MODEL_BEFORE_IMAGE',retentionErrorCode=None,
            products=[dict(role=name,name=name,**{k:self.descriptor(work/name)[k] for k in ['sha256','byteLength']})
                      for name in ['started-native.json','native.log']],unclosedOwnedViews=0,cooperativeDeadlineExceeded=False,
            fullPhysicalVariance=None,significance=None,scientificValidation='NOT_VALIDATED',qualifiedControls=0,
            provenanceVerified=False,physicalApplicabilityVerified=False)
        pub._write_control(work/'terminal.json',terminal)
        _,tr,_=pub._read_control(work/'terminal.json')
        pub._write_control(work/'terminal-ready.json',dict(protocol='DSG_NATIVE_LINEAR_TERMINAL_READY_V1',
            operationRef=self.f.operation,terminalSha256=tr['sha256']))
        _,rr,_=pub._read_control(work/'terminal-ready.json')
        pub._write_control(work/'native-return.json',dict(protocol='DSG_NATIVE_LINEAR_RETURNED_V1',
            operationRef=self.f.operation,sealSha256=r._binding['sealSha256'],wrapperSha256=self.parameters['dependencies']['wrapperSha256'],
            terminalSha256=tr['sha256'],readySha256=rr['sha256'],state='FAILED_RETAINED',unclosedOwnedViews=0,
            fullPhysicalVariance=None,significance=None,scientificValidation='NOT_VALIDATED',qualifiedControls=0,
            nativeProcessId='4242',processSessionRef=self.parameters['processSessionRef'],
            ownerSha256=pin['native-owner.json']['sha256'],ownerReadySha256=pin['native-owner-ready.json']['sha256']))
        with patch.object(holder.Queries,'poll',return_value=0), patch.object(
                owned,'_WindowsOwnedExit',side_effect=AssertionError('NO_REAL_WAIT_OR_TERMINATION')):
            result=supervisor.tick()
        self.assertEqual(result['state'],'CLOSED_RETAINED')
        self.assertFalse(supervisor._closure['technicalComputationAccepted'])
        self.assertEqual(result['scientificValidation'],'NOT_VALIDATED')
        self.assertEqual(result['qualifiedControls'],0)


class NativeEntryTests(unittest.TestCase):
    def setUp(self):
        self.expected=dict(operationRef='a'*32,ownerNonce='b'*32,processSessionRef='c'*32,
            sealSha256='1'*64,grantSha256='2'*64,wrapperSha256='3'*64,parentDeadlineUTC='2026-10-16T10:03:00Z')

    def test_literal_entry_has_exact_include_order_crlf_and_one_call(self):
        root='F:/Synthetic/native-work/'+'a'*32
        raw=preparation.render_entry(root,'F:/Synthetic/native-supervision/launcher.jsh',self.expected)
        self.assertNotIn(b'\n',raw.replace(b'\r\n',b''))
        lines=raw.decode('ascii').splitlines()
        self.assertEqual(len(lines),6)
        self.assertEqual(lines[:4],['#include "'+root+'/'+name+'"' for name in preparation.LIBRARIES.values()])
        self.assertEqual(raw.count(b'DSGNativeLinearLaunch('),1)

    def test_native_paths_reject_quote_traversal_and_unicode(self):
        for path in ['F:/bad"/native-work/'+'a'*32,'F:/../native-work/'+'a'*32,'F:/caffè/'+'a'*32]:
            with self.assertRaises(Exception): preparation.render_entry(path,'F:/safe/launcher.jsh',self.expected)


if __name__=='__main__': unittest.main()
