"""Synthetic byte fixtures only; no native parsing or real scientific qualification."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError,encode,decode
from tools.scientific_transients.campaign_input_archive import CampaignInputArchive,payload
from tools.scientific_transients.local_registry import fingerprint
from tools.scientific_transients.confirmatory_campaign import input_blockers,ConfirmatoryCampaigns
from tools.scientific_registry.ingestion_storage import MemoryStore

def ref(n):return format(n,'032x')
def sha(raw):return hashlib.sha256(raw).hexdigest()

class CampaignArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.source=self.root/'source';self.archive=self.root/'archive'
        self.source.mkdir();self.archive.mkdir();frames=[];files=[]
        shared_bandpass=b'SYNTHETIC bandpass metadata'
        for i in range(3):
            hashes={}
            for role in ('IMAGE','METADATA','BANDPASS'):
                raw=shared_bandpass if role=='BANDPASS' else ('SYNTHETIC '+role+' '+str(i)).encode()
                name=str(i)+'-'+role.lower()+('.xisf' if role=='IMAGE' else '.json')
                (self.source/name).write_bytes(raw);hashes[role]=sha(raw)
                files.append({'role':role,'frameRef':ref(10+i),'path':name,'sha256':sha(raw),'bytes':len(raw)})
            frames.append({'frameRef':ref(10+i),'exposureRef':ref(20+i),'sha256':hashes['IMAGE'],
                'metadataSha256':hashes['METADATA'],'bandpassSha256':hashes['BANDPASS'],'role':'SCIENCE',
                'acquiredUTC':None,'timeStatus':'UNKNOWN','calibration':'UNKNOWN','uncertainty':'UNKNOWN'})
        self.value={'protocol':'DSG_CAMPAIGN_INPUT_SOURCE_V1','witness':{'witnessRef':ref(1),'purpose':'SYNTHETIC',
                    'correlationRef':ref(2),'frames':frames},'files':files}
        self.manifest=self.root/'manifest.json';self.pin()

    def pin(self):
        self.manifest.write_bytes(encode(self.value));self.expected=sha(self.manifest.read_bytes())

    def prepare(self):return CampaignInputArchive.prepare(self.source,self.manifest,self.expected,self.archive)

    def test_all_bytes_retained_and_minimized_payload_binds_actual_private_manifest(self):
        archive=self.prepare();inspected=archive.inspect();witness=inspected['witness']
        self.assertEqual(witness['reportSha256'],self.expected);self.assertEqual(inspected['qualifiedControls'],0)
        self.assertFalse(inspected['executionAuthorized']);self.assertEqual(inspected['scienceValidation'],'NOT_VALIDATED')
        index=decode((archive.directory/'archive.json').read_bytes())
        for record in index['files']:
            self.assertEqual((archive.directory/record['snapshot']).read_bytes(),(self.source/record['path']).read_bytes())
        output=self.root/'worker-payload.json';actual=archive.export(output)
        self.assertEqual(actual,sha(output.read_bytes()));self.assertEqual(decode(output.read_bytes()),witness)
        self.assertNotIn('path',str(witness));self.assertNotIn('authority',str(witness));self.assertNotIn(str(self.root),str(witness))

    def test_later_original_change_preserves_retained_snapshot_and_original_proof(self):
        archive=self.prepare();before=archive.verify()
        (self.source/self.value['files'][0]['path']).write_bytes(b'Changed only in synthetic fixture')
        self.manifest.write_bytes(b'Changed original manifest')
        self.assertEqual(archive.verify(),before)

    def test_changed_source_prevents_archive_and_leaves_failure_receipt(self):
        (self.source/self.value['files'][0]['path']).write_bytes(b'Changed fixture')
        with self.assertRaisesRegex(ProtocolError,'SOURCE_CHANGED'):self.prepare()
        self.assertFalse((self.archive/ref(1)).exists());self.assertEqual(len(list(self.archive.glob('failed-*.json'))),1)

    def test_changed_snapshot_blocks_export_without_new_file(self):
        archive=self.prepare();index=decode((archive.directory/'archive.json').read_bytes())
        (archive.directory/index['files'][0]['snapshot']).write_bytes(b'Changed snapshot')
        output=self.root/'not-exported.json'
        with self.assertRaisesRegex(ProtocolError,'SNAPSHOT_CHANGED'):archive.export(output)
        self.assertFalse(output.exists())

    def test_changed_index_and_manifest_are_not_accepted_with_stale_pin(self):
        archive=self.prepare();path=archive.directory/'archive.json';path.write_bytes(path.read_bytes()+b' ')
        with self.assertRaisesRegex(ProtocolError,'INDEX_CHANGED'):archive.verify()

    def test_manifest_pin_mismatch_is_retained_failure(self):
        self.manifest.write_bytes(self.manifest.read_bytes()+b' ')
        with self.assertRaisesRegex(ProtocolError,'MANIFEST_CHANGED'):self.prepare()
        self.assertEqual(len(list(self.archive.glob('failed-*.json'))),1)

    def test_second_prepare_cannot_replace_existing_witness_directory(self):
        archive=self.prepare();before=fingerprint(archive.directory/'archive.json')
        with self.assertRaises(FileExistsError):self.prepare()
        self.assertEqual(fingerprint(archive.directory/'archive.json'),before);self.assertEqual(len(list(self.archive.glob('failed-*.json'))),1)

    def test_reported_complete_flags_require_retained_proof_files_not_merely_boolean_claims(self):
        self.value['witness']['frames'][0]['calibration']='VERIFIED_FOR_DECLARED_MODEL';self.pin()
        with self.assertRaisesRegex(ProtocolError,'PROOF_MISSING'):self.prepare()

    def test_retained_proofs_never_become_scientific_attestation_or_owner_review(self):
        for i,frame in enumerate(self.value['witness']['frames']):
            for state,complete,role in (
                    ('calibration','VERIFIED_FOR_DECLARED_MODEL','CALIBRATION_PROOF'),
                    ('uncertainty','COMPLETE_FOR_DECLARED_MODEL','UNCERTAINTY_PROOF')):
                frame[state]=complete
                raw=b'SYNTHETIC unvalidated proof';name=str(i)+'-'+role+'.txt'
                (self.source/name).write_bytes(raw)
                self.value['files'].append({'role':role,'frameRef':frame['frameRef'],
                    'path':name,'sha256':sha(raw),'bytes':len(raw)})
        self.pin();result=self.prepare().inspect()
        self.assertEqual(result['scienceStatements'],'WORKER_REPORTED_NOT_ATTESTED')
        self.assertEqual(result['scienceValidation'],'NOT_VALIDATED')
        self.assertEqual(result['qualifiedControls'],0)
        self.assertFalse(result['executionAuthorized'])
        service=ConfirmatoryCampaigns(MemoryStore(),ref(30),ref(31),ref(32),lambda _:None)
        service.register_inputs(result['witness'])
        self.assertIsNone(service.input_view(ref(1))['review'])

    def test_missing_input_role_duplicate_role_and_unrelated_digest_rejected(self):
        for kind in ('missing','duplicate','digest'):
            value=copy.deepcopy(self.value)
            if kind=='missing':value['files'][0]['role']='CALIBRATION_PROOF'
            if kind=='duplicate':value['files'][1]['role']='IMAGE'
            if kind=='digest':value['witness']['frames'][0]['sha256']='f'*64
            with self.subTest(kind=kind),self.assertRaises(ProtocolError):payload(value,self.expected)

    def test_traversal_and_overlapping_roots_rejected(self):
        self.value['files'][0]['path']='../outside.xisf';self.pin()
        with self.assertRaisesRegex(ProtocolError,'RELATIVE_PATH'):self.prepare()
        with self.assertRaisesRegex(ProtocolError,'ROOT_OVERLAP'):
            CampaignInputArchive.prepare(self.source,self.manifest,self.expected,self.source)

    def test_local_reserved_real_declaration_does_not_fill_unknown_science_or_authorize(self):
        self.value['witness']['purpose']='CONFIRMATORY_RESERVED_REAL';self.pin();archive=self.prepare()
        result=archive.inspect();self.assertEqual(result['qualifiedControls'],0)
        self.assertIn('CALIBRATION_OR_FULL_MODEL_UNCERTAINTY_MISSING',input_blockers(result['witness']))
        self.assertIn('ACQUISITION_TIME_NOT_VERIFIED',input_blockers(result['witness']))
        service=ConfirmatoryCampaigns(MemoryStore(),ref(30),ref(31),ref(32),lambda _:None)
        service.register_inputs(result['witness']);self.assertIsNone(service.input_view(ref(1))['review'])

    def test_copy_failure_retains_partial_directory_and_never_restarts_implicitly(self):
        from tools.scientific_transients import campaign_input_archive as module
        original=module.copy_verified;calls=0
        def interrupted(*args,**kwargs):
            nonlocal calls
            calls+=1
            if calls==3:raise OSError('Synthetic interruption')
            return original(*args,**kwargs)
        with patch.object(module,'copy_verified',interrupted),self.assertRaises(OSError):self.prepare()
        directory=self.archive/ref(1);self.assertTrue((directory/'manifest.json').exists())
        self.assertFalse((directory/'archive.json').exists())
        with self.assertRaises(FileExistsError):self.prepare()

if __name__=='__main__':unittest.main()
