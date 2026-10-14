"""Plan/journal integration with three MOCK jobs; no native image execution."""
import json
import math
import struct
import unittest
from unittest.mock import patch
from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients import test_triplet_report as fixtures
from tools.scientific_transients import test_native_aperture as native_fixtures
from tools.scientific_transients.test_test_plan import ref
from tools.scientific_transients.local_registry import fingerprint
from tools.scientific_transients.multi_epoch import compare,conditional_sigma


class MultiEpochTests(unittest.TestCase):
    def setUp(self):
        original=native_fixtures.NativeReceiptTests.prepare
        def with_headers(instance):
            marker=instance.input.read_bytes();index=int(marker[-1:])
            xml=('<xisf><Image geometry="64:64:1"><FITSKeyword name="FILTER" value="Green"/>'
                f'<FITSKeyword name="DATE-OBS" value="2026-10-14T00:{index*10:02d}:00.1234567"/>'
                '<FITSKeyword name="EXPTIME" value="600.0"/></Image></xisf>').encode()
            instance.input.write_bytes(b'XISF0100'+struct.pack('<II',len(xml),0)+xml+marker)
            return original(instance)
        with patch.object(native_fixtures.NativeReceiptTests,'prepare',with_headers):
            self.f=fixtures.TripletTests();self.f.setUp()
        self.addCleanup(self.f.doCleanups)
        for i in range(3):self.f.execute(i)
        self.budget={'schema':'BKL051_MULTI_EPOCH_BUDGET_V1','planSha256':self.f.plan.sha,
            'headSha256':self.f.plan.events()[1],'caseRef':ref(2),'sourceRef':'c'*32,
            'referenceFrameRef':ref(4),'origin':'SYNTHETIC_TEST',
            'pairs':[{'frameRef':ref(i),'rightToReferenceScale':2.,'variances':[4.,9.,.04],
                      'covariances':[1.,.1,.2]} for i in (5,6)],
            'omittedComponents':['MASTER_CALIBRATION','SKY_ESTIMATOR','PASSBAND_RESPONSE'],
            'skyIncludesReadNoise':None,'readNoiseAddedSeparately':None}
        self.path=self.f.root/'comparison-budget.json';self.persist()

    def persist(self):
        self.path.write_text(json.dumps(self.budget));self.sha=fingerprint(self.path)['sha256']

    def inspect(self):return compare(self.f.plan,ref(2),self.f.journals,self.path,self.sha)

    def test_actual_reports_join_case_and_keep_diagnostic_units(self):
        v=self.inspect();self.assertEqual(v['technicalCoverage'],'TECHNICAL_COVERAGE_COMPLETE')
        self.assertEqual(len(v['attempts']),3);self.assertEqual(v['unit'],'NORMALIZED_SAMPLE_SUM')
        for p in v['pairs']:
            self.assertAlmostEqual(p['algebraicDifference'],-.3)
            self.assertAlmostEqual(p['conditionalSigma'],math.sqrt(4+4*9+.09*.04-4*1-.6*.1+1.2*.2))
        self.assertEqual(v['qualifiedControls'],0);self.assertIsNone(v['significance'])
        self.assertNotIn(str(self.f.root),json.dumps(v))

    def test_unknown_scale_and_covariance_are_not_one_or_zero(self):
        self.budget['pairs'][0]['rightToReferenceScale']=None
        self.budget['pairs'][1]['covariances'][0]=None;self.persist();v=self.inspect()
        self.assertIsNone(v['pairs'][0]['algebraicDifference'])
        self.assertAlmostEqual(v['pairs'][1]['algebraicDifference'],-.3)
        self.assertIsNone(v['pairs'][1]['conditionalSigma'])

    def test_missing_or_ambiguous_source_never_success(self):
        self.budget['sourceRef']=ref(90);self.persist();v=self.inspect()
        self.assertTrue(all(r['selection']=='SOURCE_MISSING_OR_AMBIGUOUS' for r in v['attempts']))
        self.assertTrue(all(r['algebraicDifference'] is None for r in v['pairs']))

    def test_incompatible_header_band_and_unknown_metadata_block_difference(self):
        from tools.scientific_transients import multi_epoch
        original=multi_epoch.header
        target=next(r['sha256'] for r in self.f.manifests[1]['files'] if r['role']=='INPUT')
        def incompatible(path):
            v=original(path)
            if v['sha256']==target:v['keywords']['FILTER']='Red'
            return v
        with patch.object(multi_epoch,'header',incompatible):
            v=self.inspect();self.assertIsNone(v['pairs'][0]['algebraicDifference'])
            self.assertIn('FILTERS_INCOMPATIBLE',v['pairs'][0]['blockers'])
        with patch.object(multi_epoch,'header',side_effect=ProtocolError('MISSING_HEADER')):
            v=self.inspect();self.assertTrue(all(p['algebraicDifference'] is None for p in v['pairs']))

    def test_stale_plan_or_budget_pin_rejected(self):
        self.path.write_bytes(self.path.read_bytes()+b' ')
        with self.assertRaisesRegex(ProtocolError,'BUDGET_CHANGED'):self.inspect()
        self.persist();self.budget['headSha256']='f'*64;self.persist()
        with self.assertRaisesRegex(ProtocolError,'PLAN_BINDING'):self.inspect()

    def test_missing_journal_and_altered_report_do_not_hide_attempts(self):
        saved=dict(self.f.journals);self.f.journals.pop(next(iter(self.f.journals)));v=self.inspect()
        self.assertEqual(len(v['attempts']),3);self.assertEqual(v['technicalCoverage'],'INCOMPLETE')
        self.assertTrue(all(p['algebraicDifference'] is None for p in v['pairs']))
        self.f.journals=saved
        (next(iter(saved.values()))/'report.json').write_bytes(b'changed report')
        v=self.inspect();self.assertEqual(len(v['attempts']),3)
        self.assertEqual(v['technicalCoverage'],'INCOMPLETE')
        self.assertTrue(all(p['algebraicDifference'] is None for p in v['pairs']))

    def test_double_read_noise_and_cherry_picked_pair_rejected(self):
        self.budget.update(skyIncludesReadNoise=True,readNoiseAddedSeparately=True);self.persist()
        with self.assertRaisesRegex(ProtocolError,'DOUBLE_READ_NOISE'):self.inspect()
        self.budget['readNoiseAddedSeparately']=False;self.budget['pairs'].pop();self.persist()
        with self.assertRaisesRegex(ProtocolError,'PAIR_COVERAGE'):self.inspect()


class PropagationTests(unittest.TestCase):
    def test_malformed_gradient_refused_even_with_unknown_variance(self):
        for gradient in ([1,2],[True,0,0],[math.inf,0,0]):
            with self.assertRaises(ProtocolError):conditional_sigma([None]*3,[None]*3,gradient)

    def test_shared_scale_and_cross_terms_keep_correct_sign(self):
        self.assertAlmostEqual(conditional_sigma([4,9,.04],[1,.1,.2],[1,-2,-.3]),math.sqrt(36.1836))
        self.assertIsNone(conditional_sigma([4,9,.04],[None,0,0],[1,-2,-.3]))

    def test_non_psd_and_zero_variance_covariance_refused_even_without_flux(self):
        for variances,cov in (([1,1,1],[.9,.9,-.9]),([0,1,1],[.1,0,0])):
            with self.assertRaises(ProtocolError):conditional_sigma(variances,cov,[0,0,0])
        self.assertEqual(conditional_sigma([1,1,0],[1,0,0],[1,-1,0]),0)

    def test_generated_psd_matrices_agree_with_direct_quadratic_form(self):
        import random
        rng=random.Random(51007)
        for _ in range(100):
            a=[[rng.uniform(-2,2) for _ in range(3)] for _ in range(3)]
            c=[[math.fsum(a[i][k]*a[j][k] for k in range(3)) for j in range(3)] for i in range(3)]
            g=[1,-rng.uniform(.1,3),rng.uniform(-4,4)]
            sigma=conditional_sigma([c[i][i] for i in range(3)],[c[0][1],c[0][2],c[1][2]],g)
            expected=math.sqrt(math.fsum(g[i]*c[i][j]*g[j] for i in range(3) for j in range(3)))
            self.assertAlmostEqual(sigma,expected,places=11)


if __name__=='__main__':unittest.main()
