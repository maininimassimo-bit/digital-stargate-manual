import copy,math,unittest
from tools.scientific_transients.reference_covariance import catalog_covariance,conditional_linear_position,conditional_cross_epoch_position,ERRORS,CORRELATIONS

def fixture():
 row={name:str(i+1) for i,name in enumerate(ERRORS)}
 row.update({name:'0' for _,_,name in CORRELATIONS})
 row.update(ra_dec_corr='0.1',ra_pmra_corr='0.25',ra_pmdec_corr='0.05',dec_pmra_corr='0.1',dec_pmdec_corr='-0.1',pmra_pmdec_corr='0.2')
 return row

class CovarianceTests(unittest.TestCase):
 def test_reconstruction_preserves_units_correlations_and_ra_cosdec_once(self):
  result=catalog_covariance(fixture());c=result['matrix']
  self.assertEqual(result['axisUnits'],['mas','mas','mas','mas/yr','mas/yr'])
  self.assertEqual([c[i][i] for i in range(5)],[1,4,9,16,25])
  self.assertEqual(c[0][3],1);self.assertEqual(c[1][4],-1)
  self.assertEqual(c[0][4],.25);self.assertEqual(c[3][1],.8)
  self.assertEqual(c[3][4],4);self.assertTrue(result['gaiaRaErrorAlreadyCosDecScaled'])
  self.assertFalse(result['associationAccepted']);self.assertFalse(result['nativeCentroidCovarianceIncluded'])

 def test_missing_correlation_is_unavailable_not_zero(self):
  row=fixture();row['ra_pmra_corr']=''
  result=catalog_covariance(row)
  self.assertIsNone(result['matrix']);self.assertEqual(result['missingFields'],['ra_pmra_corr'])
  self.assertFalse(result['missingCorrelationsFilledWithZero'])

 def test_bad_formal_errors_and_correlations_stop(self):
  for field,value in [('ra_error','0'),('dec_error','-1'),('pmra_error','nan'),('ra_pmra_corr','1.1'),('pmra_pmdec_corr','inf')]:
   with self.subTest(field=field,value=value):
    row=fixture();row[field]=value
    with self.assertRaises(ValueError):catalog_covariance(row)

 def test_inconsistent_correlations_inside_scalar_range_stop(self):
  row=fixture();row.update(ra_dec_corr='-0.9',ra_parallax_corr='-0.9',dec_parallax_corr='-0.9')
  with self.assertRaisesRegex(ValueError,'NOT_POSITIVE_DEFINITE'):catalog_covariance(row)

 def test_conditional_projection_includes_position_motion_cross_terms(self):
  c=catalog_covariance(fixture())['matrix'];result=conditional_linear_position(c,2)
  self.assertEqual(result['matrixMasSquared'][0][0],69)
  self.assertEqual(result['matrixMasSquared'][1][1],100)
  self.assertAlmostEqual(result['matrixMasSquared'][0][1],18.3)
  self.assertEqual(conditional_linear_position(c,0)['matrixMasSquared'],[[1,.2],[.2,4]])
  self.assertFalse(result['sixDimensionalPropagation']);self.assertFalse(result['associationAccepted'])

 def test_bad_epoch_shape_and_asymmetry_stop(self):
  c=catalog_covariance(fixture())['matrix']
  for years in [math.nan,math.inf,True]:
   with self.assertRaises(ValueError):conditional_linear_position(c,years)
  with self.assertRaises(ValueError):conditional_linear_position([[1]],2)
  wrong=copy.deepcopy(c);wrong[0][1]+=1
  with self.assertRaises(ValueError):conditional_linear_position(wrong,2)

 def test_shared_reference_cross_epoch_covariance_is_not_independent_or_symmetric(self):
  matrix=catalog_covariance(fixture())['matrix'];result=conditional_cross_epoch_position(matrix,1,2)
  expected=[[36,9.5],[10.05,51]]
  for i in range(2):
   for j in range(2):self.assertAlmostEqual(result['matrixMasSquared'][i][j],expected[i][j])
  reverse=conditional_cross_epoch_position(matrix,2,1)['matrixMasSquared']
  for i in range(2):
   for j in range(2):self.assertAlmostEqual(reverse[i][j],result['matrixMasSquared'][j][i])
  same=conditional_cross_epoch_position(matrix,2,2)['matrixMasSquared']
  self.assertEqual(same,conditional_linear_position(matrix,2)['matrixMasSquared'])
  self.assertFalse(result['epochsAssumedIndependent'])

 def test_overflow_does_not_create_infinite_covariance(self):
  row=fixture();row['ra_error']='1e308'
  with self.assertRaisesRegex(ValueError,'NONFINITE'):catalog_covariance(row)
  row['ra_error']='1e-300'
  with self.assertRaisesRegex(ValueError,'NONPOSITIVE_RECONSTRUCTED'):catalog_covariance(row)
  matrix=catalog_covariance(fixture())['matrix']
  with self.assertRaisesRegex(ValueError,'NONFINITE'):conditional_linear_position(matrix,1e308)
  with self.assertRaisesRegex(ValueError,'NONFINITE'):conditional_cross_epoch_position(matrix,1e308,1e308)

if __name__=='__main__':unittest.main(verbosity=2)
