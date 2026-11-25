"""Exercise the custody with real NTFS handles and fabricated R4/result receipts."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0,sys.argv.pop(1))
sys.path.insert(1,str(Path(__file__).resolve().parent))
from imageanalysis_custody import ImageAnalysisFiles, _IDS, _METRICS, _pin, _encode, digest

BASE=Path(__file__).resolve().parent
FIXTURE=Path('O:/BKL046-ImageAnalysis-controlli-v1/fixture')
RUNNER=Path('O:/BKL046-ImageAnalysis-runner-v1/ImageAnalysis-controls.jsh')
ADAPTER=Path('O:/BKL046-ImageAnalysis-PJSR-v1/ImageAnalysis-adapter.jsh')
PARSER=Path(sys.path[0])/ 'tools/scientific_transients/strict_passive_json.jsh'
OP='a'*32
NONCE='b'*32
RES='fd211b22-eace-482b-b353-c88ed80ba6b3'


class CustodyTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory(dir=BASE)
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)/OP
        self.inputs=self.root/'inputs'
        self.inputs.mkdir(parents=True)
        rows=[]
        expected=json.loads((FIXTURE/'riscontro.json').read_bytes())
        for name in _IDS:
            copied=Path(shutil.copyfile(FIXTURE/(name+'.fits'),self.inputs/(name+'.fits')))
            row=_pin(copied,copied.read_bytes())
            self.assertEqual(row['sha256'],next(r['sha256'] for r in expected['files'] if r['name']==copied.name))
            rows.append(row)
        config=dict(protocol='BKL046_IMAGEANALYSIS_PJSR_CONFIG_V1',operationRef=OP,requestNonce=NONCE,
                    deadlineUTC='2026-11-25T12:00:00.000Z',plan=dict(operationRef=OP,
                        version='1.9.6 build 1719',inputRoot=self.inputs.as_posix(),
                        inputs=[dict(row,id=name) for row,name in zip(rows,_IDS)]))
        (self.root/'runtime-config.json').write_bytes(_encode(config))
        (self.root/'entry.js').write_bytes(b'/* fixture never executes */')
        for s in (RUNNER,ADAPTER,PARSER):
            shutil.copyfile(s,self.root/s.name)
        self.files=rows+[_pin(p,p.read_bytes()) for p in self.root.glob('*') if p.is_file()]
        self.live=True
        self.guard=ImageAnalysisFiles(self.root,operation=OP,request_nonce=NONCE,files=self.files,
                                     assert_live=lambda:self.live)
        self.addCleanup(self.guard._dirs.close)
        self.addCleanup(self.guard._static.release)
        self.addCleanup(lambda:[group.release() for group in reversed(self.guard._messages)])
        self.cfg_sha=digest((self.root/'runtime-config.json').read_bytes())
        self.entry_sha=digest((self.root/'entry.js').read_bytes())
        self.request=dict(protocol='BKL046_IMAGEANALYSIS_START_REQUEST_V1',operationRef=OP,requestNonce=NONCE,
                          configSha256=self.cfg_sha,entrySha256=self.entry_sha)
        self.ack_path=self.root/'start-ack.json'
        self.result_path=self.root/'measurements.json'

    def reservation(self,op):
        self.assertEqual(op,OP)
        return RES

    def acknowledge(self):
        self.request_path=self.root/'start-request.json'
        self.request_path.write_bytes(_encode(self.request))
        return self.guard.acknowledge(self.reservation)

    def publish_result(self,ack_hash,mode=None):
        rows=[dict(id=name,values={metric:1 for metric in _METRICS}) for name in _IDS]
        deltas=[dict(id=name,byMetric={metric:0 for metric in _METRICS}) for name in _IDS]
        if mode=='delta':
            deltas[0]['byMetric']['measurementSigma']=5
        result=dict(protocol='BKL046_IMAGEANALYSIS_CONTROL_RESULT_V1',operationRef=OP,
                    cache=False,extendedMeasurements=False,scientificAcceptance=False,version='1.9.6 build 1719',
                    forward=dict(inputOrder=list(_IDS),records=rows),
                    reverse=dict(inputOrder=list(_IDS[::-1]),records=rows),deltas=deltas)
        result_raw=_encode(result)
        receipt=dict(protocol='BKL046_IMAGEANALYSIS_RETURN_V1',operationRef=OP,requestNonce=NONCE,
                     reservation=RES,entrySha256=self.entry_sha,configSha256=self.cfg_sha,
                     startAckSha256=ack_hash,resultSha256=digest(result_raw),producerReturned=True,
                     scientificAcceptance=(mode=='science'))
        self.result_path.write_bytes(result_raw)
        (self.root/'return.json').write_bytes(_encode(receipt))

    def test_files_protected_through_outcome_until_original_exit(self):
        with self.assertRaises(PermissionError):
            (self.inputs/'compact-zones.fits').open('r+b').close()
        with self.assertRaises(OSError):
            self.inputs.rename(self.root/'input-replacement')
        ack=self.acknowledge()
        self.assertEqual(digest(self.ack_path.read_bytes()),ack)
        self.assertFalse((self.root/'start-ack.pending').exists())
        self.publish_result(ack)
        result_sha,receipt_sha=self.guard.retain(self.reservation)
        self.assertEqual(digest(self.result_path.read_bytes()),result_sha)
        self.assertRegex(receipt_sha,'^[a-f0-9]{64}$')
        with self.assertRaises(PermissionError):
            self.result_path.open('r+b').close()
        with self.assertRaisesRegex(ValueError,'ORIGINAL_EXIT_NOT_PROVEN'):
            self.guard.release_after_proven_exit(lambda:False)
        self.guard.release_after_proven_exit(lambda:True)
        self.result_path.open('r+b').close()

    def test_pinned_entry_mismatch_fences_ack_without_overwriting(self):
        self.request['entrySha256']='0'*64
        with self.assertRaisesRegex(ValueError,'REQUEST_BINDING'):
            self.acknowledge()
        self.assertFalse(self.ack_path.exists())
        with self.assertRaisesRegex(ValueError,'ACK_REPLAY'):
            self.guard.acknowledge(self.reservation)

    def test_ack_file_created_elsewhere_is_not_overwritten(self):
        self.ack_path.write_bytes(b'previous')
        with self.assertRaises(FileExistsError):
            self.acknowledge()
        self.assertEqual(self.ack_path.read_bytes(),b'previous')

    def test_wrong_return_delta_blocks_release(self):
        ack=self.acknowledge()
        self.publish_result(ack,mode='delta')
        with self.assertRaisesRegex(ValueError,'DELTA_MISMATCH'):
            self.guard.retain(self.reservation)
        with self.assertRaisesRegex(ValueError,'ORIGINAL_EXIT_NOT_PROVEN'):
            self.guard.release_after_proven_exit(lambda:True)

    def test_parent_must_reread_same_reservation_after_request(self):
        self.request_path=self.root/'start-request.json'
        self.request_path.write_bytes(_encode(self.request))
        ids=iter([RES,'3a0684c6-e636-470b-8c56-bd1ae7645c76'])
        with self.assertRaisesRegex(ValueError,'RESERVATION_CHANGED'):
            self.guard.acknowledge(lambda _:next(ids))
        self.assertFalse(self.ack_path.exists())


if __name__=='__main__':
    unittest.main()
