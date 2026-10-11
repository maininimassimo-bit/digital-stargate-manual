"""Inspect the actual SPCC 1.9.5 CSV and console products, without inventing fits.

The exported CSV contains common RGB matches, not a fit-rejection flag. Robust
sigma is the process's value; residual statistics below describe exported rows.
No substitute regression is represented as the native repeated-median fit.
"""
import csv
import io
import math
import re
import statistics
from .broker import require
from .intake import sha

VERSION = 'DSG_SPCC_FIT_EVIDENCE_V1'
COLUMNS = ('x','y','alpha','delta','cat_0','cat_1','cat_2','img_0','img_1','img_2',
           'cat_01','cat_21','img_01','img_21')
NUMBER = r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?'


def inspect(csv_raw, log_raw, *, geometry, profile_sha256):
    require(isinstance(csv_raw,bytes) and 0 < len(csv_raw) <= 4194304 and
            isinstance(log_raw,bytes) and 0 < len(log_raw) <= 4194304,
            'SPCC_PRODUCTS_SIZE')
    require(isinstance(geometry,list) and len(geometry) == 2 and
            all(type(n) is int and 32 <= n <= 12000 for n in geometry) and
            isinstance(profile_sha256,str) and re.fullmatch('[a-f0-9]{64}',profile_sha256),
            'SPCC_PROFILE_GRID')
    reader = csv.DictReader(io.StringIO(csv_raw.decode('utf-8-sig')))
    require(tuple(reader.fieldnames or ()) == COLUMNS, 'SPCC_CSV_FORMAT_CHANGED')
    rows=[]
    for row in reader:
        require(set(row) == set(COLUMNS) and len(rows) < 24576, 'SPCC_CSV_ROWS')
        values={k:float(v) for k,v in row.items()}
        require(all(math.isfinite(v) for v in values.values()) and
                0 <= values['x'] < geometry[0] and 0 <= values['y'] < geometry[1] and
                all(values[k] > 0 for k in COLUMNS[4:]), 'SPCC_CSV_SAMPLE')
        rows.append(values)
    require(len(rows) >= 3, 'SPCC_COMMON_MATCHES_REQUIRED')
    log=log_raw.decode('utf-8-sig')
    fits={}
    for band,column in (('R','01'),('B','21')):
        pattern=r'f_'+band+r'\s*:\s*'+band+r'/G\s*=\s*('+NUMBER+r')\*F'+band+r'/FG\s*([+-])\s*('+NUMBER+r'),\s*sigma\s*=\s*('+NUMBER+r')'
        matches=re.findall(pattern,log)
        require(len(matches) == 1, 'SPCC_NATIVE_FIT_REQUIRED')
        slope,sign,intercept,sigma=matches[0]
        slope=float(slope);intercept=float(intercept)*(1 if sign == '+' else -1);sigma=float(sigma)
        require(all(math.isfinite(x) for x in (slope,intercept,sigma)) and slope > 0 and sigma >= 0,
                'SPCC_NATIVE_FIT_VALUES')
        xs=[r['cat_'+column] for r in rows]
        residuals=[r['img_'+column]-(slope*r['cat_'+column]+intercept) for r in rows]
        median=statistics.median(residuals)
        fits[band+'/G']={'nativeSlope':slope,'nativeIntercept':intercept,'nativeRobustSigma':sigma,
            'catalogRatioRange':[min(xs),max(xs)],'exportedResidualMedian':median,
            'exportedResidualMAD':statistics.median(abs(x-median) for x in residuals),
            'exportedResidualRMS':math.sqrt(sum(x*x for x in residuals)/len(rows))}
    gains=[]
    for band in ('R','G','B'):
        matches=re.findall(r'W_'+band+r'\s*:\s*('+NUMBER+r')',log)
        require(len(matches) == 1, 'SPCC_NATIVE_WHITE_BALANCE_REQUIRED')
        gain=float(matches[0]);require(math.isfinite(gain) and 0 < gain <= 1,'SPCC_NATIVE_GAIN')
        gains.append(gain)
    bins=[0]*16
    for row in rows:
        bins[min(3,int(row['y']*4/geometry[1]))*4+min(3,int(row['x']*4/geometry[0]))] += 1
    # Native gains are inverse white-reference image ratios, normalized together.
    # Reconstruct the native white abscissa with conservative printed rounding
    # intervals. This is not a replacement integration of the reference spectrum.
    for band,index in (('R',0),('B',2)):
        f=fits[band+'/G']; bounds=[]
        for green in (gains[1]-.00005,gains[1]+.00005):
            for gain in (gains[index]-.00005,gains[index]+.00005):
                for slope in (f['nativeSlope']-.0000005,f['nativeSlope']+.0000005):
                    for intercept in (f['nativeIntercept']-.0000005,f['nativeIntercept']+.0000005):
                        require(gain > 0 and slope > 0,'SPCC_WHITE_RECONSTRUCTION_UNCERTAIN')
                        bounds.append((green/gain-intercept)/slope)
        interval=[min(bounds),max(bounds)]
        f['reconstructedWhiteCatalogRatioInterval']=interval
        f['whiteInsideExportedRange']=f['catalogRatioRange'][0] <= interval[0] <= interval[1] <= f['catalogRatioRange'][1]
    return {'version':VERSION,'status':'NATIVE_FIT_INSPECTABLE','profileSha256':profile_sha256,
        'commonRGBMatches':len(rows),'coverage4x4':bins,'fits':fits,'nativeWhiteBalanceRGB':gains,
        'fitRejectionCount':'NOT_EXPORTED','whiteReferenceInsideFitRange':
            'INSIDE_EXPORTED_RANGE_FROM_ROUNDED_NATIVE_PRODUCTS' if all(f['whiteInsideExportedRange'] for f in fits.values()) else 'NOT_ESTABLISHED',
        'absolutePhotometry':'NOT_ESTABLISHED','scientificAcceptance':'NOT_ESTABLISHED',
        'productBindingSha256':sha({'csv':__import__('hashlib').sha256(csv_raw).hexdigest(),
                                   'log':__import__('hashlib').sha256(log_raw).hexdigest()}),
        'limitations':'Nominal filter curves and substitute QE; CSV common matches do not identify robust-fit inliers. '
                      'Native printed coefficients are rounded; exported residual statistics are descriptive. '
                      'White abscissae reconstructed from inverse normalized native gains and fit coefficients, with printed rounding intervals. '
                      'Range inclusion is not an uncertainty estimate or independent spectrum integration.'}
