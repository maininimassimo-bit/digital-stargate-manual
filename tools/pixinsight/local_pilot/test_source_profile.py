"""Synthetic multi-profile/mosaic inventory; no scientific/native acceptance evidence."""
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from .broker import ProtocolError
from .source_profile import source_profile, inspect_sources, inventory_sources, image_metadata, MODES


class SourceProfileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.selection = {'masterDirectory':r'F:\Astro\Master','sessionIds':['SESSION-1','SESSION-2']}

    def tearDown(self):
        self.tmp.cleanup()

    def profile(self, mode='OSC', layout='SINGLE', panels=None):
        return {**self.selection,'sourceProfile':{'mode':mode,'layout':layout,'bayerPattern':None,'panels':panels or []}}

    def write(self, filename, channels=3, extra='', image_id='integration'):
        raw=f'<xisf><Image id="{image_id}" geometry="1000:800:{channels}" sampleFormat="Float32" colorSpace="{"RGB" if channels == 3 else "Gray"}"/>{extra}</xisf>'.encode()
        path=self.base/filename
        path.write_bytes(b'XISF0100'+struct.pack('<II',len(raw),0)+raw+b'synthetic pixels')
        return path

    def test_large_history_header_is_bounded_without_rejecting_real_master_envelope(self):
        path=self.write('history.xisf',extra='<!--'+('x'*(1100*1024))+'-->')
        self.assertEqual(image_metadata(path,'OSC',0)['channels'],3)
        path.write_bytes(b'XISF0100'+struct.pack('<II',4*1024*1024+1,0))
        with self.assertRaisesRegex(ProtocolError,'HEADER_LIMIT'):image_metadata(path,'OSC',0)

    def test_every_source_mode_has_physical_roles_and_rgb_is_not_treated_as_mono(self):
        for mode,roles in MODES.items():
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as task_dir:
                directory=Path(task_dir)
                mapping={}
                for role in roles:
                    path=self.write(mode+role+'.xisf',3 if mode=='OSC' else 1)
                    (directory/path.name).write_bytes(path.read_bytes())
                    mapping[role]={'filename':path.name,'imageIndex':0}
                selection=self.profile(mode)
                if mode=='OSC_CFA':selection['sourceProfile']['bayerPattern']='RGGB'
                with patch('tools.pixinsight.local_pilot.intake.local_directory',return_value=str(directory)):
                    report=inspect_sources({'selection':selection},[mapping])
                self.assertEqual([m['role'] for m in report['panels'][0]['masters']],list(roles))
                self.assertEqual(report['authority'],'PLANNING_ONLY')
        path=self.write('wrong-osc.xisf',1)
        with self.assertRaisesRegex(ProtocolError,'PROFILE_CHANNELS'):image_metadata(path,'OSC',0)

    def test_cfa_pattern_never_guessed_and_profile_shapes_are_closed(self):
        selection=self.profile('OSC_CFA')
        with self.assertRaisesRegex(ProtocolError,'BAYER'):source_profile(selection)
        selection['sourceProfile']['bayerPattern']='RGGB';source_profile(selection)
        selection['sourceProfile']['script']='bad()'
        with self.assertRaisesRegex(ProtocolError,'FIELDS'):source_profile(selection)

    def test_shared_folder_mosaic_retains_distinct_panel_selection_and_session_coverage(self):
        self.write('Panel_1.xisf');self.write('Panel_2.xisf')
        panels=[{'panelId':'P1','directory':self.selection['masterDirectory'],'sessionIds':['SESSION-1']},
                {'panelId':'P2','directory':self.selection['masterDirectory'],'sessionIds':['SESSION-2']}]
        selection=self.profile(layout='PANELS',panels=panels)
        mapping=[{'RGB':{'filename':f'Panel_{n}.xisf','imageIndex':0}} for n in (1,2)]
        with patch('tools.pixinsight.local_pilot.intake.local_directory',return_value=str(self.base)):
            report=inspect_sources({'selection':selection},mapping)
            self.assertEqual(len(report['panels']),2)
            self.assertEqual(report['mosaicOverlap'],'NATIVE_REVIEW_REQUIRED')
            mapping[1]['RGB']['filename']='Panel_1.xisf'
            with self.assertRaisesRegex(ProtocolError,'REUSED'):inspect_sources({'selection':selection},mapping)
        panels[1]['sessionIds']=['UNSELECTED']
        with self.assertRaisesRegex(ProtocolError,'PANEL_SESSIONS'):source_profile(selection)

    def test_mosaic_discovery_lists_auxiliary_images_without_selecting_or_assembling(self):
        self.write('masterLight_RGB_PANEL-1.xisf',extra='<Image id="rejection_high" geometry="1000:800:3" sampleFormat="Float32" colorSpace="RGB"/>')
        self.write('masterBias.xisf',1)
        selection=self.profile(layout='PANELS')
        with patch('tools.pixinsight.local_pilot.intake.local_directory',return_value=str(self.base)):
            report=inventory_sources({'selection':selection})
            self.assertEqual(len(report['files']),2)
            self.assertEqual(report['selection'],'EXPLICIT_SELECTION_REQUIRED')
            self.assertEqual(sum(len(row['images']) for row in report['files']),3)
            with self.assertRaisesRegex(ProtocolError,'MOSAIC_SELECTION_PLAN'):inspect_sources({'selection':selection})
        path=self.base/'masterLight_RGB_PANEL-1.xisf'
        with self.assertRaisesRegex(ProtocolError,'MULTI_IMAGE'):image_metadata(path,'OSC')
        with self.assertRaisesRegex(ProtocolError,'AUXILIARY'):image_metadata(path,'OSC',1)

    def test_duplicate_panel_identity_unknown_sessions_and_escape_are_rejected(self):
        panels=[{'panelId':'P1','directory':self.selection['masterDirectory'],'sessionIds':['SESSION-1']},
                {'panelId':'P1','directory':self.selection['masterDirectory'],'sessionIds':['SESSION-2']}]
        with self.assertRaisesRegex(ProtocolError,'PANEL_ID'):source_profile(self.profile(layout='PANELS',panels=panels))
        path=self.write('Master.xisf')
        with patch('tools.pixinsight.local_pilot.intake.local_directory',return_value=str(self.base)):
            with self.assertRaisesRegex(ProtocolError,'ROLE_FILENAME'):
                inspect_sources({'selection':self.profile()},[{'RGB':{'filename':'../Master.xisf','imageIndex':0}}])

    def test_xml_entity_oversize_and_truncation_are_rejected(self):
        path=self.base/'bad.xisf'
        for raw,size in [(b'<!DOCTYPE xisf><xisf/>',23),(b'',1048577),(b'<xisf>',100)]:
            path.write_bytes(b'XISF0100'+struct.pack('<II',size,0)+raw)
            with self.assertRaises(ProtocolError):image_metadata(path,'OSC',0)


if __name__=='__main__':unittest.main()
