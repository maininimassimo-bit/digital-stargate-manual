"""Synthetic contract tests; the native probe is separately identified in docs."""
import copy
import math
import unittest

from .native_measurements import validate

def fixture():
    value={'version':'DSG_PIAI_NATIVE_MEASUREMENTS_V2','width':64,'height':64,'channels':1,
        'regions':[[0,0,64,64]],'noise':[{'region':0,'channel':0,'estimates':[
            {'method':'MRS','layers':n,'sigma':.001,'support':100} for n in (4,3,2)]}],
        'starSelection':{'detected':10,'selected':1,'grid':16,'method':'BRIGHTEST_ISOLATED_PER_CELL'},
        'detector':{'version':2.01,'structureLayers':5,'hotPixelFilterRadius':1,
            'noiseReductionFilterRadius':0,'sensitivity':.5,'peakResponse':.5,'upperLimit':1},
        'fits':[{'star':0,'channel':0,'model':'GAUSSIAN','background':-.01,'amplitude':.2,
            'x':10,'y':10,'sx':2,'sy':1,'theta':0,'residual':.001}],
        'noiseUnits':'NORMALIZED_IMAGE_SAMPLES','noiseAssumption':'GAUSSIAN_COMPONENT_ESTIMATE',
        'backgroundValidity':'NOT_ESTABLISHED','linearity':'NOT_ESTABLISHED',
        'registration':'NOT_ESTABLISHED','acceptance':'NOT_ESTABLISHED',
        'sourceSha256':'a'*64,'imageIndex':0,'adapterSha256':'b'*64,'starDetectorSha256':'c'*64,
        'coreVersion':{'major':1,'minor':9,'release':5,'revision':0,'build':1706},
        'historyUnchanged':True,'originalUnchanged':True,'status':'MEASURED'}
    binding={k:value[k] for k in ('sourceSha256','imageIndex','adapterSha256','starDetectorSha256','width','height','channels')}
    return value,binding

class NativeMeasurementTests(unittest.TestCase):
    def test_derives_only_mathematical_gaussian_descriptors(self):
        v,b=fixture(); before=copy.deepcopy(v); r=validate(v,b)
        self.assertAlmostEqual(r['derivedGaussianFits'][0]['fwhmMajorPixels'],4*math.sqrt(2*math.log(2)))
        self.assertAlmostEqual(r['derivedGaussianFits'][0]['eccentricity'],math.sqrt(.75))
        self.assertEqual(r['acceptance'],'NOT_ESTABLISHED');self.assertEqual(v,before)
    def test_changed_scope_and_runtime_rejected(self):
        for key in ('sourceSha256','adapterSha256','starDetectorSha256','imageIndex','width','channels'):
            v,b=fixture();b[key]='d'*64 if key.endswith('Sha256') else b[key]+1
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'BINDING'):validate(v,b)
    def test_scientific_attestations_cannot_be_smuggled_in_measurements(self):
        for key in ('backgroundValidity','linearity','registration','acceptance'):
            v,b=fixture();v[key]='VERIFIED'
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'ATTESTATION'):validate(v,b)
    def test_invalid_support_duplicate_fit_and_nonfinite_rejected(self):
        for mutation in (lambda v:v['noise'][0]['estimates'][0].update(support=4097),
                         lambda v:v['fits'].append(copy.deepcopy(v['fits'][0])),
                         lambda v:v['fits'][0].update(sx=float('nan')),
                         lambda v:v['fits'][0].update(amplitude=True),
                         lambda v:v['detector'].update(upperLimit=True)):
            v,b=fixture();mutation(v)
            with self.assertRaises(ValueError):validate(v,b)
    def test_missing_fits_do_not_create_psf(self):
        v,b=fixture();v['fits']=[];r=validate(v,b);self.assertEqual(r['derivedGaussianFits'],[])
    def test_invalid_region_or_noise_scope_and_modified_history_rejected(self):
        for mutation in (lambda v:v['regions'][0].__setitem__(2,65),
                         lambda v:v['noise'][0].update(channel=1),
                         lambda v:v.update(historyUnchanged=False),
                         lambda v:v['coreVersion'].update(build=True)):
            v,b=fixture();mutation(v)
            with self.assertRaises(ValueError):validate(v,b)
