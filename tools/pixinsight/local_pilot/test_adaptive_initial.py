"""Synthetic read-only receipts; these fixtures do not attest native execution."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from .adaptive_initial import build
from .native_analysis import prepare,verify,VERSION
from .test_source_provenance import write
from .test_native_measurements import fixture
from .image_analysis import fingerprint
from .broker import encode
from .intake import sha


class InitialPayloadTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.pi=self.root/'pi'
        (self.pi/'include/pjsr').mkdir(parents=True);(self.pi/'bin').mkdir()
        detector=self.pi/'include/pjsr/StarDetector.jsh';detector.write_text('// synthetic dependency')
        inputs=[]
        for i,role in enumerate(('R','G','B','L')):
            path=self.root/(role+'.xisf');write(path,[.05+i*.001]*4096,64,64)
            inputs.append({'role':role,'path':str(path),'sha256':fingerprint(path),'imageIndex':0,
                           'width':64,'height':64,'channels':1,'regions':[[0,0,64,64]]})
        for module in ('native_analysis','adaptive_native_adapter','intake'):
            guard=patch('tools.pixinsight.local_pilot.'+module+'.local_directory',lambda p:p)
            guard.start();self.addCleanup(guard.stop)
        directory=self.root/'analysis';manifest=prepare(directory,inputs,allowed_roots=[self.root],pixinsight_root=self.pi)
        measurements=[]
        for row in inputs:
            measured,_=fixture();measured.update(sourceSha256=row['sha256'],adapterSha256=manifest['measurementSha256'],
                                                 starDetectorSha256=manifest['starDetectorSha256'])
            measurements.append({'role':row['role'],'report':measured})
        (directory/'report.json').write_bytes(encode({'version':VERSION,'status':'READ_ONLY_MEASURED',
            'measurements':measurements,'originalUnchanged':True,'historyUnchanged':True,'scientificAcceptance':'NOT_ESTABLISHED'}))
        verify(directory,expected_manifest_sha256=fingerprint(directory/'manifest.json'))
        files=[]
        for name in ('suite','blur','noise','star','PixInsight.exe'):
            path=self.pi/'bin'/name;path.write_text(name)
            files.append({'path':str(path),'sha256':fingerprint(path)})
        files.append({'path':str(detector),'sha256':fingerprint(detector)})
        library=Path(__file__).parent
        runtime={'version':'DSG_PIAI_ADAPTIVE_RUNTIME_V2','coreVersion':measurements[0]['report']['coreVersion'],
                 'executorSha256':sha({'controller':fingerprint(library/'adaptive_executor.jsh'),
                                       'factory':fingerprint(library/'adaptive_native.jsh')}),
                 'measurementSha256':manifest['measurementSha256'],'starDetectorSha256':manifest['starDetectorSha256'],
                 'suiteSha256':files[0]['sha256'],'dependenciesSha256':sha(sorted(files[4:],key=lambda r:r['path'])),
                 'models':{k:{'selectedVersion':v,'fileSha256':files[i]['sha256']}
                           for i,(k,v) in enumerate((('BLURX',4),('NOISEX',3.1),('STARX',11)),1)}}
        descriptors=[{k:r[k] for k in ('role','sha256','imageIndex','width','height','channels')} for r in inputs]
        facts={'sourceSha256':sha(descriptors),'recordSha256':'a'*64,'domain':'LINEAR_ATTESTED',
               'registration':'VERIFIED','backgroundROI':'NOT_ESTABLISHED','stellarPSF':'NOT_ESTABLISHED',
               'runtime':'VERIFIED','mask':'NOT_ESTABLISHED'}
        record=self.root/'provenance.json';record.write_bytes(encode({'inputs':descriptors,'facts':facts,'scope':'SYNTHETIC_FIXTURE'}))
        self.settings={'analysisDirectory':str(directory),'analysisManifestSha256':fingerprint(directory/'manifest.json'),
                       'provenanceRecord':str(record),'provenanceRecordSha256':fingerprint(record),
                       'runtime':runtime,'runtimeFiles':files,'pixinsightRoot':str(self.pi),'allowedMasterRoots':[str(self.root)],'mode':'LRGB'}
        self.intake={'selection':{'prompt':'Piano fixture conservativo','masterDirectory':str(self.root),'sourceProfile':
                     {'mode':'LRGB','layout':'SINGLE','bayerPattern':None,'panels':[],'additionalDirectories':[]}}}

    def test_builds_exact_bound_previews_without_promoting_unknown_facts(self):
        value=build(self.intake,self.settings,'fixture-worker')
        self.assertEqual(len(value['assetsBase64']),4)
        self.assertEqual(value['evidence']['provenance']['backgroundROI'],'NOT_ESTABLISHED')
        self.assertEqual(value['evidence']['provenance']['recordSha256'],self.settings['provenanceRecordSha256'])
        self.assertEqual(value['evidence']['intent'],self.intake['selection']['prompt'])
        self.assertEqual(len({sha(r['displayCurve']) for r in value['evidence']['previews']}),1)

    def test_changed_record_runtime_or_original_prevents_payload(self):
        for change in ('record','runtime','source'):
            with self.subTest(change=change):
                self.setUp()
                if change=='record':Path(self.settings['provenanceRecord']).write_text('changed')
                elif change=='runtime':Path(self.settings['runtimeFiles'][1]['path']).write_text('changed')
                else:(self.root/'R.xisf').write_text('changed')
                with self.assertRaises(ValueError):build(self.intake,self.settings,'fixture-worker')


if __name__=='__main__':unittest.main()
