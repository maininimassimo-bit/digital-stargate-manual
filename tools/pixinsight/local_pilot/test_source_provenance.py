import copy
from pathlib import Path
import struct
import tempfile
import unittest
import xml.etree.ElementTree as ET

from .image_analysis import fingerprint
from .source_provenance import inspect,verify_crop,match_drizzle_container

HISTORY='<ProcessingHistory version="1.0"><instance class="DrizzleIntegration"><table id="inputData"><row><item>/private/input.xdrz</item></row></table><parameter id="scale">2</parameter><parameter id="showImages">false</parameter></instance></ProcessingHistory>'

def write(path,values,width,height,*,crop=None,history=HISTORY,padding=0):
    offset=4096 if padding==0 else 2*1024*1024
    root=ET.Element('xisf');image=ET.SubElement(root,'Image',geometry=f'{width}:{height}:1',sampleFormat='Float32',colorSpace='Gray',location=f'attachment:{offset}:{len(values)*4}')
    ET.SubElement(image,'Property',id='PixInsight:ProcessingHistory',type='String').text=history
    if crop is not None:ET.SubElement(image,'FITSKeyword',name='WBPPCROP',value=crop)
    if padding:ET.SubElement(image,'Property',id='Padding',type='String').text='x'*padding
    header=ET.tostring(root);assert len(header)<offset-16
    data=b'XISF0100'+struct.pack('<II',len(header),0)+header
    path.write_bytes(data+bytes(offset-len(data))+struct.pack('<'+'f'*len(values),*values))

class SourceProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();root=Path(self.tmp.name)
        self.child=root/'child.xisf';self.parent=root/'parent.xisf';self.container=root/'container.xpsm'
        write(self.parent,[.1,.2,.3,.4],2,2)
        write(self.child,[.2,.4],1,2,crop="'(1,0)x(2,2)'")
        root=ET.Element('{http://www.pixinsight.com/xpsm}xpsm')
        instance=copy.deepcopy(ET.fromstring(HISTORY)[0]);instance.find("parameter[@id='showImages']").text='true'
        root.append(instance);self.container.write_bytes(ET.tostring(root))
    def tearDown(self):self.tmp.cleanup()
    def crop(self):
        return verify_crop(self.child,self.parent,child_sha256=fingerprint(self.child),parent_sha256=fingerprint(self.parent),child_index=0,parent_index=0)
    def match(self):
        return match_drizzle_container(self.child,self.container,source_sha256=fingerprint(self.child),container_sha256=fingerprint(self.container),image_index=0)
    def test_crop_proves_all_selected_pixels_without_promoting_science(self):
        r=self.crop();self.assertEqual(r['crop'],[1,0,2,2]);self.assertTrue(r['historyPreserved'])
        self.assertEqual(r['relationship'],'PIXELS_BIT_IDENTICAL_RECTANGULAR_SUBSET')
        self.assertEqual(r['linearity'],'NOT_ESTABLISHED')
    def test_pixel_difference_rejected_even_when_updated_digest_matches(self):
        write(self.child,[.2,.41],1,2,crop="'(1,0)x(2,2)'")
        with self.assertRaisesRegex(ValueError,'PIXELS_DIFFER'):self.crop()
    def test_changed_crop_bounds_and_history_rejected(self):
        for crop,history in (("'(0,0)x(2,2)'",HISTORY),("'(1,0)x(2,2)'",HISTORY.replace('>2<','>3<'))):
            write(self.child,[.2,.4],1,2,crop=crop,history=history)
            with self.assertRaises(ValueError):self.crop()
    def test_hash_change_and_auxiliary_index_rejected(self):
        with self.assertRaisesRegex(ValueError,'CHANGED'):inspect(self.child,expected_sha256='a'*64,image_index=0)
        with self.assertRaisesRegex(ValueError,'INDEX'):inspect(self.child,expected_sha256=fingerprint(self.child),image_index=1)
    def test_history_is_reported_with_coverage_limit(self):
        r=inspect(self.child,expected_sha256=fingerprint(self.child),image_index=0)
        self.assertEqual(r['recordedProcesses'],['DrizzleIntegration'])
        self.assertEqual(r['upstreamHistory'],'NOT_ESTABLISHED');self.assertEqual(r['registration'],'NOT_ESTABLISHED')
        self.assertNotIn('/private',str(r))
    def test_history_entity_and_unknown_version_rejected(self):
        for h in ('<!DOCTYPE ProcessingHistory>'+HISTORY,HISTORY.replace('version="1.0"','version="2.0"')):
            write(self.child,[.2,.4],1,2,crop="'(1,0)x(2,2)'",history=h)
            with self.assertRaises(ValueError):inspect(self.child,expected_sha256=fingerprint(self.child),image_index=0)
    def test_bounded_large_source_header_supported_without_v1_change(self):
        write(self.child,[.2,.4],1,2,crop="'(1,0)x(2,2)'",padding=1100000)
        r=inspect(self.child,expected_sha256=fingerprint(self.child),image_index=0)
        self.assertEqual(r['recordedProcesses'],['DrizzleIntegration'])
        from .image_analysis import selected_header
        with self.assertRaisesRegex(ValueError,'HEADER_LIMIT'):selected_header(self.child,0)
    def test_header_over_four_mib_rejected_before_xml_or_attachment_read(self):
        self.child.write_bytes(b'XISF0100'+struct.pack('<II',4*1024*1024+1,0))
        with self.assertRaisesRegex(ValueError,'HEADER_LIMIT'):inspect(self.child,expected_sha256=fingerprint(self.child),image_index=0)
    def test_utf16_container_entities_rejected_before_parser_resolution(self):
        text=self.container.read_bytes().decode().replace('>2<','>&scale;<')
        text='<!DOCTYPE xpsm [<!ENTITY scale "2">]>'+text
        for encoding in ('utf-16','utf-16-le','utf-16-be'):
            self.container.write_bytes(text.encode(encoding))
            with self.subTest(encoding=encoding),self.assertRaisesRegex(ValueError,'CONTAINER_XML'):self.match()
    def test_utf16_header_entities_rejected_before_parser_resolution(self):
        text='<xisf><Image geometry="1:2:1" sampleFormat="Float32" colorSpace="Gray" location="attachment:4096:8"/></xisf>'
        for encoding in ('utf-16','utf-16-le','utf-16-be'):
            raw=('<!DOCTYPE xisf [<!ENTITY value "2">]>'+text).encode(encoding)
            self.child.write_bytes(b'XISF0100'+struct.pack('<II',len(raw),0)+raw+bytes(4096-16-len(raw))+bytes(8))
            with self.subTest(encoding=encoding),self.assertRaisesRegex(ValueError,'PROVENANCE_XML'):
                inspect(self.child,expected_sha256=fingerprint(self.child),image_index=0)
    def test_matches_pixel_parameters_and_exposes_ui_difference(self):
        r=self.match();self.assertEqual(r['containerIndex'],0);self.assertEqual(r['uiDifferences'],['showImages'])
        self.assertEqual(r['executionReceipt'],'NOT_ESTABLISHED');self.assertEqual(r['linearity'],'NOT_ESTABLISHED')
    def test_modified_parameter_missing_input_and_ambiguous_container_rejected(self):
        initial=self.container.read_bytes()
        for variant in ('changed','missing','duplicate'):
            tree=ET.fromstring(initial)
            if variant=='changed':tree[0].find("parameter[@id='scale']").text='3'
            if variant=='missing':tree[0].remove(tree[0].find('table'))
            if variant=='duplicate':tree.append(copy.deepcopy(tree[0]))
            self.container.write_bytes(ET.tostring(tree))
            with self.subTest(variant=variant),self.assertRaisesRegex(ValueError,'MATCH_REQUIRED'):self.match()
