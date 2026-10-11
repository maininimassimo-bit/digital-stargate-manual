import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from .native_analysis import prepare,verify,local_file,VERSION
from .test_source_provenance import write
from .test_native_measurements import fixture
from .image_analysis import fingerprint
from .broker import encode


class NativeAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.source=self.root/'source.xisf'
        write(self.source,[.05]*4096,64,64)
        self.pi=self.root/'pi';(self.pi/'include/pjsr').mkdir(parents=True)
        (self.pi/'include/pjsr/StarDetector.jsh').write_text('// simulated installed dependency')
        self.inputs=[{'role':'L','path':str(self.source),'sha256':fingerprint(self.source),'imageIndex':0,
                     'width':64,'height':64,'channels':1,'regions':[[0,0,64,64]]}]
        # Test filesystem guards on both CI hosts with synthetic paths; the
        # Windows lexical/UNC rejection is tested separately without this patch.
        self.lexical=patch('tools.pixinsight.local_pilot.native_analysis.local_directory',lambda p:p)
        self.lexical.start();self.addCleanup(self.lexical.stop)

    def prepared(self):
        self.directory=self.root/'analysis'
        manifest=prepare(self.directory,self.inputs,allowed_roots=[self.root],pixinsight_root=self.pi)
        report,_=fixture();report.update(sourceSha256=self.inputs[0]['sha256'],adapterSha256=manifest['measurementSha256'],
                                        starDetectorSha256=manifest['starDetectorSha256'])
        value={'version':VERSION,'status':'READ_ONLY_MEASURED','measurements':[{'role':'L','report':report}],
               'originalUnchanged':True,'historyUnchanged':True,'scientificAcceptance':'NOT_ESTABLISHED'}
        (self.directory/'report.json').write_bytes(encode(value))
        return manifest,value,fingerprint(self.directory/'manifest.json')

    def test_copies_exact_selected_source_and_verifies_independent_bindings(self):
        _,_,expected=self.prepared();original=fingerprint(self.source)
        report,bindings,receipt=verify(self.directory,expected_manifest_sha256=expected)
        self.assertEqual(receipt['status'],'READ_ONLY_VERIFIED');self.assertEqual(bindings['L']['sourceSha256'],original)
        self.assertEqual(fingerprint(self.source),original)
        self.assertIn(b'\r\n',(self.directory/'run.js').read_bytes())
        with self.assertRaises(FileExistsError):verify(self.directory,expected_manifest_sha256=expected)

    def test_manifest_source_and_region_substitution_fail_verification(self):
        for changed in ('manifest','source','region','component'):
            with self.subTest(changed=changed):
                self.setUp();manifest,value,expected=self.prepared()
                if changed=='manifest':(self.directory/'manifest.json').write_bytes(encode({**manifest,'report':'elsewhere'}))
                elif changed=='source':self.source.write_bytes(b'changed')
                elif changed=='component':(self.directory/'analysis.jsh').write_text('// changed')
                else:
                    value['measurements'][0]['report']['regions']=[[0,0,32,32]]
                    (self.directory/'report.json').write_bytes(encode(value))
                with self.assertRaises(ValueError):verify(self.directory,expected_manifest_sha256=expected)

    def test_outside_scope_and_boolean_geometry_are_rejected(self):
        with self.assertRaises(ValueError):prepare(self.root/'outside',self.inputs,allowed_roots=[self.pi],pixinsight_root=self.pi)
        changed=copy.deepcopy(self.inputs);changed[0]['channels']=True
        with self.assertRaises(ValueError):prepare(self.root/'boolean',changed,allowed_roots=[self.root],pixinsight_root=self.pi)

    def test_unc_is_rejected_before_any_resolve(self):
        self.lexical.stop()
        with patch.object(Path,'resolve',side_effect=AssertionError('Must not resolve UNC')):
            with self.assertRaises(ValueError):local_file('//server/private/master.xisf',[str(self.root)])

if __name__=='__main__':unittest.main()
