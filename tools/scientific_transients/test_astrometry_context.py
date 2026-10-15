"""Synthetic XISF headers and retained declarations; no scientific image run."""
import copy
import json
import math
import struct
import unittest
from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients import test_input_lineage as fixtures
from tools.scientific_transients.local_registry import fingerprint
from tools.scientific_transients.astrometry_context import inspect_context, header, residuals, timestamp_seconds


def xisf(marker,start='2026-08-16T01:00:00.1234567',end=False):
    xml=('<xisf><Image geometry="64:64:1"><FITSKeyword name="DATE-OBS" value="'+start+'"/>'
        '<FITSKeyword name="DATE-AVG" value="2026-08-16T01:05:00.1200000"/>'
        '<FITSKeyword name="EXPTIME" value="600.0"/><FITSKeyword name="FILTER" value="Green"/>'
        +('<Property id="Observation:Time:End"/>' if end else '')+'</Image></xisf>').encode()
    return b'XISF0100'+struct.pack('<II',len(xml),0)+xml+marker


class AstrometryContextTests(unittest.TestCase):
    def setUp(self):
        self.l=fixtures.LineageTests();self.l.setUp();self.addCleanup(self.l.doCleanups)
        l=self.l;l.raw.write_bytes(xisf(b'SYNTHETIC_RAW'));l.output.write_bytes(xisf(b'SYNTHETIC_COPY'))
        for r in l.manifest['parents']:r['sha256']=fingerprint(r['path'])['sha256']
        l.receipt['products']['manifest.json']=self.save(l.directory/'manifest.json',l.manifest)
        l.receipt['products']['out.xisf']=fingerprint(l.output)['sha256']
        l.receipt_sha=self.save(l.directory/'receipt.json',l.receipt)
        l.draft['cases'][0]['frames'][0]['sha256']=fingerprint(l.raw)['sha256']
        l.draft_sha=self.save(l.draft_path,l.draft)
        self.solver=l.root/'solver';self.solver.mkdir();self.wcs=l.root/'wcs';self.wcs.mkdir()
        self.solver_output=self.solver/'candidate.xisf';self.solver_output.write_bytes(xisf(b'SYNTHETIC_SOLVER'))
        self.wcs_output=self.wcs/'derived.xisf';self.wcs_output.write_bytes(xisf(b'SYNTHETIC_WCS','2026-08-16T01:00:00.123',True))
        for d in (self.solver,self.wcs):(d/'entry.js').write_bytes(b'SYNTHETIC_NEVER_EXECUTED')
        self.sm={'input':str(l.raw),'inputSHA256':fingerprint(l.raw)['sha256'],
            'entrySHA256':fingerprint(self.solver/'entry.js')['sha256'],
            'source':'CDS VizieR Gaia DR3 I/355/gaiadr3; SYNTHETIC'}
        self.wm={'parents':[{'path':str(p),'sha256':fingerprint(p)['sha256']} for p in (l.output,self.solver_output)],
            'scriptSHA256':fingerprint(self.wcs/'entry.js')['sha256']}
        self.split={'training':[{'SourceID':'1'}],'heldOut':[{'SourceID':str(i)} for i in (2,3,4)]}
        self.centers=[{'x':1.2,'y':1.3},{'x':50.5,'y':50.4}]
        self.st={'status':'COMPLETED_CANDIDATE_WCS_WITH_HELD_OUT_REFERENCES','scienceValidation':'NOT_VALIDATED',
            'output':str(self.solver_output),'pixelDifference':0,'solutionSummary':'Reference catalog ........ Gaia DR3\n',
            'holdout':[{'sourceId':'2','status':'UNIQUE_DIAGNOSTIC_MATCH','predicted':[1,1],'measured':[1.2,1.3],'dx':.2,'dy':.3},
                {'sourceId':'3','status':'UNIQUE_DIAGNOSTIC_MATCH','predicted':[50,50],'measured':[50.5,50.4],'dx':.5,'dy':.4},
                {'sourceId':'4','status':'NO_MATCH'}]}
        self.wt={'status':'COMPLETED_SIGNED_GREEN_WITH_CANDIDATE_WCS','scienceValidation':'NOT_VALIDATED',
            'output':str(self.wcs_output),'pixelDifference':0,
            'coordinateChecks':[{'pixel':p,'reference':[299.9,22.7],'derived':[299.9,22.7]}
                for p in ([0.5,0.5],[32,32],[63.5,63.5])]}
        self.persist()

    def save(self,path,value):
        path.write_text(json.dumps(value));return fingerprint(path)['sha256']

    def persist(self):
        for d,m,t,flag in ((self.solver,self.sm,self.st,'inputHashUnchanged'),(self.wcs,self.wm,self.wt,'parentHashesUnchanged')):
            self.save(d/'manifest.json',m);self.save(d/'terminal.json',t)
            if d==self.solver:
                self.save(d/'catalog-split.json',self.split);self.save(d/'retained-centroids.json',self.centers)
            receipt={'terminal':t,flag:True,'products':{p.name:fingerprint(p)['sha256'] for p in d.iterdir() if p.name!='receipt.json'}}
            sha=self.save(d/'receipt.json',receipt)
            if d==self.solver:self.solver_sha=sha
            else:self.wcs_sha=sha

    def inspect(self):
        l=self.l
        return inspect_context(l.directory,l.receipt_sha,l.draft_path,l.draft_sha,
            self.solver,self.solver_sha,self.wcs,self.wcs_sha)

    def test_context_recomputes_residuals_and_preserves_exact_subseconds(self):
        v=self.inspect();self.assertEqual(v['holdout']['matched'],2)
        self.assertAlmostEqual(v['holdout']['radialRMSPixel'],(.54/2)**.5)
        self.assertEqual(v['timing']['derivedStartMinusSourceSeconds'],'-0.0004567')
        self.assertEqual(v['timing']['averageMinusStartHalfExposureSeconds'],'-0.0034567')
        self.assertTrue(v['timing']['averagePreserved'])
        self.assertEqual(v['timing']['endTimeOrigin'],'DERIVED_METADATA_NOT_IN_SOURCE')
        self.assertIsNone(v['holdout']['fullCovariance']);self.assertEqual(v['qualifiedControls'],0)
        self.assertNotIn(str(self.l.root),json.dumps(v));self.assertNotIn('sourceId',json.dumps(v))

    def test_changed_output_or_retained_centroids_rejected(self):
        for p in (self.wcs_output,self.solver/'retained-centroids.json',self.l.raw):
            raw=p.read_bytes();p.write_bytes(b'changed')
            with self.assertRaises(ProtocolError):self.inspect()
            p.write_bytes(raw)

    def test_missing_or_empty_native_coordinate_copy_evidence_rejected(self):
        valid=copy.deepcopy(self.wt)
        for checks in (None,[],[{'pixel':p,'reference':{},'derived':{}}
                for p in ([0.5,0.5],[32,32],[63.5,63.5])]):
            with self.subTest(checks=checks):
                self.wt=copy.deepcopy(valid)
                if checks is None:self.wt.pop('coordinateChecks')
                else:self.wt['coordinateChecks']=checks
                self.persist()
                with self.assertRaisesRegex(ProtocolError,'ASTROMETRY_COORDINATE_COPY_'):self.inspect()

    def test_mismatched_nonfinite_or_wrong_coordinate_probes_rejected(self):
        valid=copy.deepcopy(self.wt)
        for key,value in (('reference',[True,22.7]),('reference',[None,None]),
                ('reference',[float('nan'),22.7]),('derived',[299.9,float('inf')]),
                ('derived',[299.91,22.7]),('pixel',[1,1]),('pixel',[True,0.5])):
            with self.subTest(key=key,value=value):
                self.wt=copy.deepcopy(valid);self.wt['coordinateChecks'][0][key]=value;self.persist()
                # Nonfinite JSON is rejected by the retained-file reader before
                # the native-coordinate evidence check is reached.
                expected=('JSON_INVALID' if any(type(n) is float and not math.isfinite(n)
                    for n in value) else 'ASTROMETRY_COORDINATE_COPY_')
                with self.assertRaisesRegex(ProtocolError,expected):self.inspect()
        for value in ([360,22.7],[299.9,91]):
            self.wt=copy.deepcopy(valid)
            self.wt['coordinateChecks'][0].update(reference=value,derived=value);self.persist()
            with self.assertRaisesRegex(ProtocolError,'ASTROMETRY_COORDINATE_COPY_MISMATCH'):self.inspect()

    def test_overlapping_partition_and_centroid_reuse_rejected(self):
        self.split['training'][0]['SourceID']='2';self.persist()
        with self.assertRaisesRegex(ProtocolError,'PARTITION_OVERLAP'):self.inspect()
        self.split['training'][0]['SourceID']='1'
        self.st['holdout'][1]=copy.deepcopy(self.st['holdout'][0]);self.st['holdout'][1]['sourceId']='3';self.persist()
        with self.assertRaisesRegex(ProtocolError,'MATCH_CHANGED'):self.inspect()

    def test_missing_reference_and_wrong_parent_binding_rejected(self):
        self.st['holdout'].pop();self.persist()
        with self.assertRaises(ProtocolError):self.inspect()
        self.wm['parents'].pop();self.persist()
        with self.assertRaises(ProtocolError):self.inspect()

    def test_radius_is_square_and_descriptive_not_acceptance_threshold(self):
        self.centers[0]={'x':3.9,'y':3.9};self.st['holdout'][0].update(measured=[3.9,3.9],dx=2.9,dy=2.9)
        self.persist();v=self.inspect()
        self.assertEqual(v['holdout']['matched'],2)
        self.assertGreater(v['holdout']['largestResidualPixel'],3)
        self.assertEqual(v['solutionState'],'CANDIDATE_NOT_VALIDATED')

    def test_false_stored_residual_and_missing_catalog_identity_rejected(self):
        self.st['holdout'][0]['dx']=9;self.persist()
        with self.assertRaisesRegex(ProtocolError,'RESIDUAL_CHANGED'):self.inspect()
        self.sm['source']='OTHER';self.persist()
        with self.assertRaisesRegex(ProtocolError,'CATALOG_VERSION'):self.inspect()

    def test_xml_entities_oversize_headers_and_bad_dates_rejected(self):
        for raw in (b'<!DOCTYPE xisf [<!ENTITY x "bad">]><xisf/>',b'<xisf>\x00</xisf>'):
            self.l.raw.write_bytes(b'XISF0100'+struct.pack('<II',len(raw),0)+raw)
            with self.assertRaises(ProtocolError):header(self.l.raw)
        self.l.raw.write_bytes(b'XISF0100'+struct.pack('<II',32*1024*1024,0))
        with self.assertRaises(ProtocolError):header(self.l.raw)
        for value in ('2026-08-16T01:00:60','2026-08-16T01:00:01+02:00','2026-08-16T01:00:01.1234567890123'):
            with self.assertRaises(ProtocolError):timestamp_seconds(value)


if __name__=='__main__':unittest.main()
