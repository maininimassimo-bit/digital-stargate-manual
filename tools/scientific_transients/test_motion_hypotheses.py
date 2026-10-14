"""All combinations retained, synthetic trajectories not accepted tracklets."""
import hashlib
import json
import math
import tempfile
from decimal import Decimal
from pathlib import Path
import unittest
from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients.attempt_journal import write_new
from tools.scientific_transients.local_registry import fingerprint
from tools.scientific_transients.motion_hypotheses import inspect,tangent_plane,validate_pool

ref=lambda n:format(n,'032x')
class MotionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        records=[];frames=[]
        for i in range(3):
            image=self.root/f'image{i}';image.write_bytes(b'SYNTHETIC_NOT_IMAGE'+bytes([i]))
            catalog=self.root/f'catalog{i}';catalog.write_bytes(b'SYNTHETIC_NOT_DETECTOR'+bytes([i]))
            sha=fingerprint(image)['sha256'];cat=fingerprint(catalog)['sha256']
            records.extend([{'path':str(image),'sha256':sha},{'path':str(catalog),'sha256':cat}])
            frames.append({'frameRef':ref(i+1),'imageSha256':sha,'catalogSha256':cat,'elapsedSeconds':3600*i,
                'recordedJD':str(Decimal(2450000)+Decimal(i)/24),'band':'zg','retainedCatalogSourceCount':2,
                'candidates':[{'detectionRef':ref(10*i+j+10),'positionArcsec':[2*i+5*j,-3*i+7*j],
                    'positionCovariance':None} for j in range(2)]})
        self.evidence=self.root/'private.json';self.evidence_sha=write_new(self.evidence,{'schema':'BKL051_MOTION_PRIVATE_EVIDENCE_V1','files':records})
        self.pool={'schema':'BKL051_MOTION_POOL_V1','origin':'SYNTHETIC_TEST','selectionBasis':'SYNTHETIC_CANDIDATES',
            'sourceEvidenceSha256':self.evidence_sha,'coordinateMeaning':'RETAINED_TANGENT_PLANE_ARCSEC_ASTROMETRY_UNVALIDATED',
            'timeMeaning':'NOMINAL_RELATIVE_SECONDS_CLOCK_UNVALIDATED','frames':frames}
        self.path=self.root/'pool.json';self.persist()
    def persist(self):
        self.path.write_text(json.dumps(self.pool));self.sha=fingerprint(self.path)['sha256']
    def inspect(self):return inspect(self.path,self.sha,self.evidence,self.evidence_sha)

    def test_all_eight_hypotheses_retained_no_automatic_choice(self):
        v=self.inspect();self.assertEqual(len(v['hypotheses']),8);self.assertEqual(v['expectedHypotheses'],8)
        h=v['hypotheses'][0];self.assertEqual(h['velocityArcsecPerHour'],[2,-3]);self.assertEqual(h['radialRMSArcsec'],0)
        self.assertIsNone(v['selectedHypothesis']);self.assertFalse(v['trackletAccepted'])
        self.assertEqual(v['qualifiedControls'],0);self.assertNotIn(str(self.root),json.dumps(v))
        self.assertTrue(all(h['velocityCovariance'] is None and h['significance'] is None for h in v['hypotheses']))
    def test_ambiguous_crossing_and_stationary_sequences_not_classified(self):
        for i,f in enumerate(self.pool['frames']):
            f['candidates'][0]['positionArcsec']=[i-1,0]
            f['candidates'][1]['positionArcsec']=[1-i,0]
        self.persist();v=self.inspect();self.assertEqual(len(v['hypotheses']),8)
        self.assertGreaterEqual(sum(h['radialRMSArcsec']==0 for h in v['hypotheses']),2)
        self.assertEqual(v['movingObjectClassification'],'NOT_EVALUATED')
        for f in self.pool['frames']:
            for c in f['candidates']:c['positionArcsec']=[1,1]
        self.persist();v=self.inspect();self.assertTrue(all(h['velocityArcsecPerHour']==[0,0] for h in v['hypotheses']))
        self.assertFalse(v['trackletAccepted'])
    def test_missing_epoch_or_reused_input_rejected(self):
        self.pool['frames'][1]['elapsedSeconds']=0;self.persist()
        with self.assertRaises(ProtocolError):self.inspect()
        self.pool['frames'][1]['elapsedSeconds']=3600
        self.pool['frames'][1]['imageSha256']=self.pool['frames'][0]['imageSha256'];self.persist()
        with self.assertRaises(ProtocolError):self.inspect()
    def test_empty_pool_not_absence_of_moving_objects(self):
        self.pool['frames'][1]['candidates']=[];self.persist();v=self.inspect()
        self.assertEqual(v['status'],'EMPTY_POOL_NOT_NONDETECTION');self.assertEqual(v['hypotheses'],[])
    def test_capacity_exceeded_no_top_subset_disguised_as_complete(self):
        for i,f in enumerate(self.pool['frames']):
            f['retainedCatalogSourceCount']=17
            f['candidates']=[{'detectionRef':ref(1000+100*i+j),'positionArcsec':[j,i],'positionCovariance':None} for j in range(17)]
        self.persist();v=self.inspect();self.assertEqual(v['expectedHypotheses'],4913)
        self.assertEqual(v['status'],'RESOURCE_LIMIT_NO_PARTIAL_SELECTION');self.assertEqual(v['hypotheses'],[])
    def test_changed_evidence_or_pool_pin_rejected(self):
        (self.root/'image1').write_bytes(b'changed')
        with self.assertRaises(ProtocolError):self.inspect()
        self.sha='f'*64
        with self.assertRaises(ProtocolError):self.inspect()
    def test_duplicate_detection_and_invented_covariance_rejected(self):
        self.pool['frames'][1]['candidates'][0]['detectionRef']=self.pool['frames'][0]['candidates'][0]['detectionRef'];self.persist()
        with self.assertRaises(ProtocolError):self.inspect()
        self.pool['frames'][1]['candidates'][0]['detectionRef']=ref(999)
        self.pool['frames'][1]['candidates'][0]['positionCovariance']=0;self.persist()
        with self.assertRaises(ProtocolError):self.inspect()
    def test_tangent_projection_wrap_and_hemisphere(self):
        x,y=tangent_plane(359.999,0,.001,0);self.assertAlmostEqual(x,-7.2,places=6);self.assertEqual(y,0)
        x,y=tangent_plane(1,0,0,0);self.assertAlmostEqual(x,math.tan(math.pi/180)*180/math.pi*3600,places=9)
        with self.assertRaises(ProtocolError):tangent_plane(180,0,0,0)
    def test_retained_reference_distance_optional_not_matching_policy(self):
        self.pool['frames'][1]['candidates'][0]['referenceDistanceArcsec']=15.;self.persist()
        self.assertEqual(len(self.inspect()['hypotheses']),8)
        self.pool['frames'][1]['candidates'][0]['referenceDistanceArcsec']=-1;self.persist()
        with self.assertRaises(ProtocolError):self.inspect()

if __name__=='__main__':unittest.main()
