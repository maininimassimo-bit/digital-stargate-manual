"""Unidentified-object preview contract, synthetic measurements only; no send."""
import copy
import unittest
import xml.etree.ElementTree as ET
from tools.scientific_transients import test_mpc_export as fixtures
from tools.scientific_transients import mpc_export as mpc
from tools.scientific_transients.attempt_journal import read_json
from tools.scientific_transients.preview_review_ledger import PreviewReviewLedger
from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.pixinsight.local_pilot.broker import encode
from tools.scientific_transients.local_registry import fingerprint

class TrackletExportTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.MPCExportTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
        self.f.request['protocol']=mpc.REQUEST_V2
        self.row=self.f.request['observations'][0]
        del self.row['permID'];self.row['objectID']={'kind':'TRKSUB','value':'SYN-0001'}
    def test_unidentified_object_has_only_local_id_and_no_number_or_discovery(self):
        d=self.f.export();xml=ET.parse(d/'preview.xml')
        self.assertEqual(xml.findtext('.//trkSub'),'SYN-0001');self.assertIsNone(xml.find('.//permID'))
        v,_=read_json(d/'preview.json');self.assertFalse(v['submissionAuthorized']);self.assertFalse(v['observingNightOrAssociationValidated'])
        self.assertEqual(v['scienceValidation'],'NOT_VALIDATED')
    def test_numbered_v2_preserves_number_without_local_tracklet(self):
        self.row['objectID']={'kind':'PERMID','value':'433'}
        xml=ET.parse(self.f.export()/'preview.xml');self.assertEqual(xml.findtext('.//permID'),'433');self.assertIsNone(xml.find('.//trkSub'))
    def test_invalid_local_ids_rejected(self):
        for value in ('','123456789','a b','a/b','a.b','a+','è','x\n','<x>',None,True):
            self.row['objectID']['value']=value
            with self.subTest(value=value),self.assertRaises(ProtocolError):self.f.export()
    def test_identity_must_be_explicit_and_exclusive(self):
        for identity in ({'kind':'PROVID','value':'2026 AA'},{'kind':'TRKSUB','value':'x','permID':'433'},None):
            self.row['objectID']=identity
            with self.assertRaises((ProtocolError,TypeError)):self.f.export()
    def test_duplicate_local_id_same_instant_rejected_despite_decimal_text(self):
        duplicate=copy.deepcopy(self.row);duplicate['obsTime']='2026-10-09T01:02:03.12Z';self.f.request['observations'].append(duplicate)
        with self.assertRaisesRegex(ProtocolError,'MPC_DUPLICATE_OBJECT_TIME'):self.f.export()
    def test_different_local_ids_same_time_not_collapsed(self):
        duplicate=copy.deepcopy(self.row);duplicate['objectID']['value']='SYN-0002';self.f.request['observations'].append(duplicate)
        self.assertEqual(len(ET.parse(self.f.export()/'preview.xml').findall('.//optical')),2)
    def test_local_id_and_number_with_same_text_are_different_declared_namespaces(self):
        self.row['objectID']['value']='433';duplicate=copy.deepcopy(self.row);duplicate['objectID']['kind']='PERMID'
        self.f.request['observations'].append(duplicate)
        self.assertEqual(len(ET.parse(self.f.export()/'preview.xml').findall('.//optical')),2)
    def test_mixing_old_and_new_identity_fields_rejected(self):
        self.row['permID']='433'
        with self.assertRaises(ProtocolError):self.f.export()
    def test_unknown_uncertainty_is_not_replaced_with_zero(self):
        for k in ('rmsRA','rmsDec','rmsCorr','rmsTime'):self.row[k]=None
        d=self.f.export();xml=ET.parse(d/'preview.xml');self.assertIsNone(xml.find('.//rmsRA'))
        v,_=read_json(d/'preview.json');self.assertEqual(v['unknownFieldsByObservation'][0]['objectID'],self.row['objectID'])
    def test_preview_can_enter_existing_review_ledger_without_send_authority(self):
        d=self.f.export();_,sha=read_json(d/'export.json');root=self.f.root/'ledgers';root.mkdir()
        ledger=PreviewReviewLedger.prepare(d,sha,'MPC',root,'c'*32)
        v=ledger.inspect(ledger.anchor_sha);self.assertFalse(v['submissionAuthorized'])
    def test_bad_protocol_types_rejected_as_protocol_errors(self):
        for protocol in ([],{},None,True,'unknown'):
            self.f.request['protocol']=protocol
            with self.assertRaises(ProtocolError):self.f.export()
    def test_eight_character_identity_preserved_without_case_folding(self):
        self.row['objectID']['value']='aB_09-zZ'
        self.assertEqual(ET.parse(self.f.export()/'preview.xml').findtext('.//trkSub'),'aB_09-zZ')
    def test_same_object_same_image_different_time_rejected(self):
        other=copy.deepcopy(self.row);other['obsTime']='2026-10-09T01:03:03.12Z';self.f.request['observations'].append(other)
        with self.assertRaisesRegex(ProtocolError,'MPC_REUSED_IMAGE_FOR_OBJECT'):self.f.export()
    def add_image(self,name,content):
        path=self.f.artifacts/name;path.write_bytes(content)
        manifest=self.f.local.verify(self.f.request['bindingRef'],self.f.request['manifestSha256'])
        # New registry binding, preserving the old registered snapshot.
        manifest['binding']['bindingRef']='e'*32
        manifest['files'].append({'role':'INPUT','path':name,**fingerprint(path)})
        receipt=self.f.local.register(encode(manifest))
        self.f.request['bindingRef']=manifest['binding']['bindingRef'];self.f.request['manifestSha256']=receipt['manifestSha256']
    def test_alias_with_identical_image_bytes_is_not_another_observation(self):
        self.add_image('alias.dat',(self.f.artifacts/'INPUT.dat').read_bytes())
        other=copy.deepcopy(self.row);other.update(obsTime='2026-10-09T01:03:03.12Z',imagePath='alias.dat')
        self.f.request['observations'].append(other)
        with self.assertRaisesRegex(ProtocolError,'MPC_REUSED_IMAGE_FOR_OBJECT'):self.f.export()
    def test_distinct_images_for_same_object_are_supported(self):
        self.add_image('second.dat',b'SYNTHETIC distinct image, not real science data')
        other=copy.deepcopy(self.row);other.update(obsTime='2026-10-09T01:03:03.12Z',imagePath='second.dat')
        self.f.request['observations'].append(other)
        self.assertEqual(len(ET.parse(self.f.export()/'preview.xml').findall('.//optical')),2)

if __name__=='__main__':unittest.main()
