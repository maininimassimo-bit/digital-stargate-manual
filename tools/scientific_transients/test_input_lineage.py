"""Synthetic metadata-copy receipts: real byte verification, no pixel processing."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients.attempt_journal import write_new
from tools.scientific_transients.input_lineage import inspect_lineage
from tools.scientific_transients.test_test_plan import draft


class LineageTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.directory=self.root/'native';self.directory.mkdir()
        self.raw=self.root/'raw.xisf';self.raw.write_bytes(b'SYNTHETIC RAW NOT IMAGE')
        self.cal=self.root/'cal.xisf';self.cal.write_bytes(b'SYNTHETIC SIGNED CALIBRATION NOT IMAGE')
        self.output=self.directory/'out.xisf';self.output.write_bytes(b'SYNTHETIC DERIVED NOT IMAGE')
        self.script=self.directory/'entry.js';self.script.write_bytes(b'SYNTHETIC SCRIPT NEVER EXECUTED')
        sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
        self.manifest={'parents':[{'path':str(p),'sha256':sha(p)} for p in (self.raw,self.cal)],
            'entrySHA256':sha(self.script),'purpose':'synthetic','metadataPolicy':'synthetic'}
        self.terminal={'status':'COMPLETED_METADATA_BOUND_SIGNED_PILOT','scienceValidation':'NOT_VALIDATED',
            'rows':[{'filter':'Green','parent':str(self.cal),'observationSource':str(self.raw),'path':str(self.output),
                'copiedProperties':[],'omittedProperties':[],'keywordCount':0,'maxAbsolutePixelDifference':0,
                'scienceValidation':'NOT_VALIDATED'}]}
        self.manifest_sha=write_new(self.directory/'manifest.json',self.manifest)
        self.terminal_sha=write_new(self.directory/'terminal.json',self.terminal)
        self.receipt={'terminal':self.terminal,'parentHashesUnchanged':True,
            'products':{'entry.js':sha(self.script),'manifest.json':self.manifest_sha,
                        'terminal.json':self.terminal_sha,'out.xisf':sha(self.output)}}
        self.receipt_sha=write_new(self.directory/'receipt.json',self.receipt)
        self.draft=draft();self.draft['cases'][0]['frames'][0]['sha256']=sha(self.raw)
        self.draft_path=self.root/'draft.json';self.draft_sha=write_new(self.draft_path,self.draft)

    def inspect(self):
        return inspect_lineage(self.directory,self.receipt_sha,self.draft_path,self.draft_sha)

    def test_byte_identity_does_not_validate_calibration_or_uncertainty(self):
        value=self.inspect();self.assertEqual(value['inputs'][0]['sampleMembership'],'IN_CANDIDATE_MANIFEST')
        self.assertEqual(value['calibrationSemantics'],'NOT_ATTESTED_BY_THIS_IMPORT')
        self.assertEqual(value['qualifiedControls'],0);self.assertIsNone(value['completeUncertainty'])
        self.assertFalse(value['executionAuthorized'])

    def test_outside_sample_stays_outside_and_paths_not_exported(self):
        self.draft['cases']=[];self.draft_path.write_text(json.dumps(self.draft))
        self.draft_sha=hashlib.sha256(self.draft_path.read_bytes()).hexdigest()
        value=self.inspect();self.assertEqual(value['inputs'][0]['sampleMembership'],'OUTSIDE_CANDIDATE_MANIFEST')
        raw=json.dumps(value)
        for token in (str(self.root),'raw.xisf','cal.xisf','out.xisf','Observation:Location'):
            self.assertNotIn(token,raw)

    def test_changed_raw_calibrated_or_derived_bytes_refused(self):
        for path in (self.raw,self.cal,self.output):
            old=path.read_bytes();path.write_bytes(b'changed')
            with self.assertRaises(ProtocolError):self.inspect()
            path.write_bytes(old)

    def test_wrong_receipt_and_candidate_manifest_hash_refused(self):
        old=self.receipt_sha;self.receipt_sha='f'*64
        with self.assertRaises(ProtocolError):self.inspect()
        self.receipt_sha=old;self.draft_sha='f'*64
        with self.assertRaises(ProtocolError):self.inspect()

    def test_changed_script_or_terminal_refused(self):
        self.script.write_bytes(b'changed')
        with self.assertRaises(ProtocolError):self.inspect()

    def test_receipt_terminal_semantics_cannot_promote_science(self):
        self.receipt['terminal']['scienceValidation']='VALIDATED'
        (self.directory/'receipt.json').write_text(json.dumps(self.receipt))
        self.receipt_sha=hashlib.sha256((self.directory/'receipt.json').read_bytes()).hexdigest()
        with self.assertRaises(ProtocolError):self.inspect()


if __name__=='__main__':unittest.main()
