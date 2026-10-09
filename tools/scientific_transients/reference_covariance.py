"""Catalog-only formal covariance; no association or absolute-astrometry acceptance."""
import math

AXES=('raCosDec','dec','parallax','pmRaCosDec','pmDec')
UNITS=('mas','mas','mas','mas/yr','mas/yr')
ERRORS=('ra_error','dec_error','parallax_error','pmra_error','pmdec_error')
CORRELATIONS=((0,1,'ra_dec_corr'),(0,2,'ra_parallax_corr'),(0,3,'ra_pmra_corr'),(0,4,'ra_pmdec_corr'),(1,2,'dec_parallax_corr'),(1,3,'dec_pmra_corr'),(1,4,'dec_pmdec_corr'),(2,3,'parallax_pmra_corr'),(2,4,'parallax_pmdec_corr'),(3,4,'pmra_pmdec_corr'))

def number(value):
 if value is None or value=='':return None
 if isinstance(value,bool):raise ValueError('NONNUMERIC_CATALOG_FIELD')
 result=float(value)
 if not math.isfinite(result):raise ValueError('NONFINITE_CATALOG_FIELD')
 return result

def positive_correlation(matrix):
 """Strict mathematical consistency, not a source-quality or significance cut."""
 lower=[[0.0]*5 for _ in range(5)]
 for i in range(5):
  for j in range(i+1):
   value=matrix[i][j]-sum(lower[i][k]*lower[j][k] for k in range(j))
   if i==j:
    if value<=0:raise ValueError('CORRELATION_NOT_POSITIVE_DEFINITE')
    lower[i][j]=math.sqrt(value)
   else:lower[i][j]=value/lower[j][j]

def catalog_covariance(row):
 fields=ERRORS+tuple(name for _,_,name in CORRELATIONS)
 missing=[name for name in fields if row.get(name) in (None,'')]
 if missing:return {'status':'UNAVAILABLE_MISSING_CATALOG_FIELDS','missingFields':missing,'matrix':None,'missingCorrelationsFilledWithZero':False}
 errors=[number(row[name]) for name in ERRORS]
 if any(value<=0 for value in errors):raise ValueError('NONPOSITIVE_FORMAL_ERROR')
 matrix=[[0.0]*5 for _ in range(5)];rho=[[float(i==j) for j in range(5)] for i in range(5)]
 for i,error in enumerate(errors):matrix[i][i]=error*error
 for i,j,name in CORRELATIONS:
  correlation=number(row[name])
  if not -1<=correlation<=1:raise ValueError('CORRELATION_OUT_OF_RANGE')
  rho[i][j]=rho[j][i]=correlation
  matrix[i][j]=matrix[j][i]=correlation*errors[i]*errors[j]
 positive_correlation(rho)
 if any(not math.isfinite(value) for row in matrix for value in row):raise ValueError('NONFINITE_RECONSTRUCTED_COVARIANCE')
 if any(matrix[i][i]<=0 for i in range(5)):raise ValueError('NONPOSITIVE_RECONSTRUCTED_COVARIANCE_DIAGONAL')
 return {'status':'CATALOG_FORMAL_COVARIANCE_RECONSTRUCTED','axes':list(AXES),'axisUnits':list(UNITS),'elementUnits':'product of row and column axis units','matrix':matrix,'positiveDefiniteCorrelationVerified':True,'gaiaRaErrorAlreadyCosDecScaled':True,'scientificValidation':'NOT_VALIDATED','nativeCentroidCovarianceIncluded':False,'radialVelocityCovarianceIncluded':False,'catalogSystematicsIncluded':False,'associationAccepted':False}

def validate_matrix(matrix):
 if len(matrix)!=5 or any(len(row)!=5 for row in matrix):raise ValueError('INVALID_COVARIANCE_SHAPE')
 if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for row in matrix for v in row):raise ValueError('NONFINITE_COVARIANCE')
 if any(matrix[i][j]!=matrix[j][i] for i in range(5) for j in range(5)):raise ValueError('ASYMMETRIC_COVARIANCE')
 if any(matrix[i][i]<=0 for i in range(5)):raise ValueError('NONPOSITIVE_COVARIANCE_DIAGONAL')
 errors=[math.sqrt(matrix[i][i]) for i in range(5)]
 positive_correlation([[matrix[i][j]/(errors[i]*errors[j]) for j in range(5)] for i in range(5)])

def conditional_linear_position(matrix, years):
 """Fixed tangent-plane linear PM model only, not six-dimensional propagation."""
 if not isinstance(years,(int,float)) or isinstance(years,bool) or not math.isfinite(years):raise ValueError('INVALID_EPOCH_DIFFERENCE')
 validate_matrix(matrix)
 # Cpos = J C J^T, J=[[1,0,0,dt,0],[0,1,0,0,dt]].
 a=matrix[0][0]+2*years*matrix[0][3]+years*years*matrix[3][3]
 b=matrix[0][1]+years*(matrix[0][4]+matrix[3][1])+years*years*matrix[3][4]
 d=matrix[1][1]+2*years*matrix[1][4]+years*years*matrix[4][4]
 if not all(math.isfinite(value) for value in (a,b,d)):raise ValueError('NONFINITE_PROJECTED_COVARIANCE')
 return {'model':'CONDITIONAL_FIXED_TANGENT_PLANE_LINEAR_PM','axes':['raCosDec','dec'],'matrixMasSquared':[[a,b],[b,d]],'deltaJulianYearsTCB':years,'sixDimensionalPropagation':False,'apparentPlace':False,'observerParallax':False,'radialPerspective':False,'scientificValidation':'NOT_VALIDATED','associationAccepted':False}

def conditional_cross_epoch_position(matrix, years_a, years_b):
 """J_a C J_b^T for one shared catalog source; not independent epochs."""
 for years in (years_a,years_b):
  if not isinstance(years,(int,float)) or isinstance(years,bool) or not math.isfinite(years):raise ValueError('INVALID_EPOCH_DIFFERENCE')
 validate_matrix(matrix)
 a=matrix[0][0]+(years_a+years_b)*matrix[0][3]+years_a*years_b*matrix[3][3]
 b=matrix[0][1]+years_b*matrix[0][4]+years_a*matrix[3][1]+years_a*years_b*matrix[3][4]
 c=matrix[1][0]+years_b*matrix[1][3]+years_a*matrix[4][0]+years_a*years_b*matrix[4][3]
 d=matrix[1][1]+(years_a+years_b)*matrix[1][4]+years_a*years_b*matrix[4][4]
 if not all(math.isfinite(value) for value in (a,b,c,d)):raise ValueError('NONFINITE_PROJECTED_COVARIANCE')
 return {'model':'CONDITIONAL_FIXED_TANGENT_PLANE_LINEAR_PM_SHARED_REFERENCE','matrixMasSquared':[[a,b],[c,d]],'deltaJulianYearsTCB':[years_a,years_b],'sameCatalogSourceRequired':True,'epochsAssumedIndependent':False,'scientificValidation':'NOT_VALIDATED','associationAccepted':False}
