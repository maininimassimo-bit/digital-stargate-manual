"""Synthetic receipt collection and real file copies. Native proof kept separately."""
import copy
import tempfile
import unittest
from pathlib import Path

from tools.pixinsight.local_pilot.broker import ProtocolError, encode, decode
from tools.scientific_transients.native_aperture import prepare_run, collect_run
from tools.scientific_transients.local_registry import fingerprint


class NativeReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.runs=self.root/'runs';self.runs.mkdir()
        self.input=self.root/'input.xisf';self.input.write_bytes(b'synthetic bytes, not an XISF')
        self.engine=self.root/'engine.js';self.engine.write_bytes(b'synthetic engine fixture')
        self.catalog=self.root/'catalog.js';self.catalog.write_bytes(b'synthetic catalog fixture')
        self.operation='b'*32
        self.image={'imageIndex':0,'width':64,'height':64,'channels':1,'linearity':'DECLARED_LINEAR_NOT_ATTESTED'}
        self.parameters={'coordinateConvention':'PI_NATIVE_GEOMETRIC','apertureRadius':4,'annulusInner':2,'annulusOuter':3}
        self.targets=[{'sourceRef':'c'*32,'x':32.5,'y':32.5}]

    def prepare(self):
        return prepare_run(self.input,self.runs,self.operation,self.image,self.parameters,self.targets,'1.9.5 build 1706',engine=self.engine,catalog=self.catalog)

    def terminal(self, directory):
        manifest=decode((directory/'parameters.json').read_bytes())
        for name in ['input-initial.js','input-current.js','checkpoint-initial.js','checkpoint-current.js']:(directory/name).write_text('synthetic native History declaration',encoding='utf-8')
        (directory/'checkpoint.xisf').write_bytes(b'synthetic checkpoint')
        row={'sourceRef':'c'*32,'x':32.5,'y':32.5,'clipped':False,'backgroundAvailable':True,'fluxNormalizedSampleSum':.3,'area':50.,'background':.01,'skyNoiseDiagnostic':0.,'skySampleCount':248,'fullVariance':None,'significance':None,'scienceValidation':'NOT_VALIDATED'}
        (directory/'measurement-00001.json').write_bytes(encode(row))
        terminal={'protocol':manifest['protocol'],'operationRef':self.operation,'state':'COMPLETED','runtime':manifest['runtime'],'inputSha256':manifest['input']['sha256'],'imageIndex':0,'rows':[row],'changedPixels':0,'checkpointSha256':fingerprint(directory/'checkpoint.xisf')['sha256'],'historySha256':fingerprint(directory/'checkpoint-current.js')['sha256'],'parametersSha256':fingerprint(directory/'parameters.json')['sha256'],'scienceValidation':'NOT_VALIDATED','unit':'NORMALIZED_SAMPLE_SUM','fullAperturePhotometryWorkflowExecuted':False,'providerRequestsInvoked':0}
        (directory/'terminal.json').write_bytes(encode(terminal));return terminal

    def collect(self,directory): return collect_run(directory,self.operation,engine=self.engine,catalog=self.catalog)

    def test_exact_copies_no_launch_and_new_directory_blocks_replay(self):
        d=self.prepare();self.assertEqual((d/'input.xisf').read_bytes(),self.input.read_bytes());self.assertFalse((d/'terminal.json').exists())
        with self.assertRaises(FileExistsError):self.prepare()
        self.assertIn(b'\r\n',(d/'entry.js').read_bytes())

    def test_synthetic_collection_preserves_unknowns_and_all_four_exports(self):
        d=self.prepare();self.terminal(d);result=self.collect(d)
        self.assertEqual(result['qualityCounts'],{'measured':0,'excluded':0,'incomplete':1})
        history=decode((d/'history-bundle.json').read_bytes());self.assertEqual(len(history['exports']),4)
        self.assertEqual(history['upstreamAcquisitionHistory'],'NOT_ATTESTED')
        self.assertIsNone(result['nativeRows'][0]['significance']);self.assertEqual(self.collect(d),result)

    def test_mutated_source_snapshot_params_or_runtime_rejected(self):
        for name in ['input.xisf','parameters.json','entry.js','native_aperture.jsh']:
            with self.subTest(name=name):
                d=self.prepare();self.terminal(d);p=d/name;p.write_bytes(p.read_bytes()+b' ')
                with self.assertRaises(ProtocolError):self.collect(d)
                self.operation=hex(int(self.operation,16)+1)[2:].zfill(32)
        d=self.prepare();self.terminal(d);self.engine.write_bytes(b'changed')
        with self.assertRaisesRegex(ProtocolError,'RUNTIME_CHANGED'):self.collect(d)

    def test_output_digest_and_row_copy_mutation_block_success(self):
        d=self.prepare();self.terminal(d);(d/'checkpoint.xisf').write_bytes(b'changed')
        with self.assertRaisesRegex(ProtocolError,'OUTPUT_CHANGED'):self.collect(d)
        self.operation='d'*32;d=self.prepare();self.terminal(d);(d/'measurement-00001.json').write_bytes(encode({}))
        with self.assertRaisesRegex(ProtocolError,'ROW_CHANGED'):self.collect(d)

    def test_bad_row_units_authority_and_forged_variance_rejected(self):
        for key,value in [('unit','ADU'),('scienceValidation','ACCEPTED'),('providerRequestsInvoked',1),('changedPixels',1)]:
            d=self.prepare();t=self.terminal(d);t[key]=value;(d/'terminal.json').write_bytes(encode(t))
            with self.assertRaises(ProtocolError):self.collect(d)
            self.operation=hex(int(self.operation,16)+1)[2:].zfill(32)
        d=self.prepare();t=self.terminal(d);t['rows'][0]['fullVariance']=.1;(d/'terminal.json').write_bytes(encode(t))
        with self.assertRaises(ProtocolError):self.collect(d)

    def test_native_failure_is_not_success_or_recovery_authority(self):
        d=self.prepare();(d/'terminal.json').write_bytes(encode({'state':'FAILED'}))
        with self.assertRaisesRegex(ProtocolError,'NOT_COMPLETED'):self.collect(d)
        self.assertFalse((d/'history-bundle.json').exists())

    def test_malformed_targets_coordinates_and_input_rejected_before_copy(self):
        for modify in [lambda:self.image.update(channels=3),lambda:self.parameters.update(coordinateConvention='UNKNOWN'),lambda:self.targets[0].update(x=float('nan'))]:
            old=(copy.deepcopy(self.image),copy.deepcopy(self.parameters),copy.deepcopy(self.targets));modify()
            with self.assertRaises(ProtocolError):self.prepare()
            self.image,self.parameters,self.targets=old
        self.assertEqual(list(self.runs.iterdir()),[])

    def test_modified_history_bundle_never_overwritten(self):
        d=self.prepare();self.terminal(d);self.collect(d);p=d/'history-bundle.json';p.write_bytes(b'keep failure')
        with self.assertRaisesRegex(ProtocolError,'HISTORY_CHANGED'):self.collect(d)
        self.assertEqual(p.read_bytes(),b'keep failure')


if __name__=='__main__':unittest.main()
