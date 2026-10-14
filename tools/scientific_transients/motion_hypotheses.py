"""Enumerate all three-exposure association hypotheses in an explicit pool.

Unweighted tangent-plane linear fits are descriptive, not orbits, validated
tracklets, significance tests, a blind search or an automatic association.
"""
import hashlib
import itertools
import math
import re
from decimal import Decimal
from pathlib import Path
from tools.pixinsight.local_pilot.broker import require,opaque
from tools.scientific_transients.attempt_journal import read_json,write_new
from tools.scientific_transients.local_registry import safe_path,fingerprint
from tools.scientific_transients.queue import fields,digest

LIMIT=4096  # Resource ceiling; no astrophysical or acceptance meaning.
def finite(x):return type(x) in {int,float} and math.isfinite(x)


def tangent_plane(ra,dec,anchor_ra,anchor_dec):
    require(all(finite(x) for x in (ra,dec,anchor_ra,anchor_dec))
        and 0<=ra<360 and 0<=anchor_ra<360 and abs(dec)<=90 and abs(anchor_dec)<=90,'MOTION_SKY_COORDINATE')
    a,d,a0,d0=map(math.radians,(ra,dec,anchor_ra,anchor_dec))
    u=(math.cos(d)*math.cos(a),math.cos(d)*math.sin(a),math.sin(d))
    c=(math.cos(d0)*math.cos(a0),math.cos(d0)*math.sin(a0),math.sin(d0))
    e=(-math.sin(a0),math.cos(a0),0);n=(-math.sin(d0)*math.cos(a0),-math.sin(d0)*math.sin(a0),math.cos(d0))
    dot=lambda x:math.fsum(v*w for v,w in zip(u,x))
    denominator=dot(c);require(denominator>0,'MOTION_TANGENT_HEMISPHERE')
    result=[dot(b)/denominator*180/math.pi*3600 for b in (e,n)]
    require(all(finite(x) for x in result),'MOTION_PROJECTION_OVERFLOW');return result


def validate_pool(pool):
    fields(pool,{'schema','origin','selectionBasis','sourceEvidenceSha256','coordinateMeaning','timeMeaning','frames'})
    require(pool['schema']=='BKL051_MOTION_POOL_V1' and pool['origin'] in {'SYNTHETIC_TEST','PUBLIC_KNOWN_OBJECT_CONTROL'}
        and pool['selectionBasis'] in {'SYNTHETIC_CANDIDATES','RETAINED_EPHEMERIS_NEAREST_THREE_NOT_BLIND'}
        and digest(pool['sourceEvidenceSha256'])
        and pool['coordinateMeaning']=='RETAINED_TANGENT_PLANE_ARCSEC_ASTROMETRY_UNVALIDATED'
        and pool['timeMeaning']=='NOMINAL_RELATIVE_SECONDS_CLOCK_UNVALIDATED'
        and type(pool['frames']) is list and len(pool['frames'])==3,'MOTION_POOL')
    frame_refs=set();detection_refs=set();times=[]
    for frame in pool['frames']:
        fields(frame,{'frameRef','imageSha256','catalogSha256','elapsedSeconds','recordedJD','band','retainedCatalogSourceCount','candidates'})
        require(opaque(frame['frameRef']) and frame['frameRef'] not in frame_refs
            and digest(frame['imageSha256']) and digest(frame['catalogSha256'])
            and finite(frame['elapsedSeconds']) and 0<=frame['elapsedSeconds']<=1e9
            and type(frame['recordedJD']) is str and re.fullmatch(r'\d{1,7}(?:\.\d{1,24})?',frame['recordedJD'])
            and frame['band'] in {'zg','Green','Red','Blu','L-Pro'}
            and type(frame['retainedCatalogSourceCount']) is int and 0<=frame['retainedCatalogSourceCount']<=100000
            and type(frame['candidates']) is list and len(frame['candidates'])<=min(256,frame['retainedCatalogSourceCount']),'MOTION_FRAME')
        frame_refs.add(frame['frameRef']);times.append(frame['elapsedSeconds'])
        for candidate in frame['candidates']:
            fields(candidate,{'detectionRef','positionArcsec','positionCovariance'}
                   | ({'referenceDistanceArcsec'} if 'referenceDistanceArcsec' in candidate else set()))
            require('referenceDistanceArcsec' not in candidate or candidate['referenceDistanceArcsec'] is None
                or finite(candidate['referenceDistanceArcsec']) and candidate['referenceDistanceArcsec']>=0,
                'MOTION_REFERENCE_DISTANCE')
            require(opaque(candidate['detectionRef']) and candidate['detectionRef'] not in detection_refs
                and type(candidate['positionArcsec']) is list and len(candidate['positionArcsec'])==2
                and all(finite(v) and abs(v)<=1e7 for v in candidate['positionArcsec'])
                and candidate['positionCovariance'] is None,'MOTION_DETECTION')
            detection_refs.add(candidate['detectionRef'])
    require(times[0]==0 and times[0]<times[1]<times[2]
        and len({f['imageSha256'] for f in pool['frames']})==3,'MOTION_TIME_OR_REUSED_IMAGE')
    jd0=Decimal(pool['frames'][0]['recordedJD'])
    require(all(abs(float((Decimal(f['recordedJD'])-jd0)*86400)-f['elapsedSeconds'])<=1e-6
                for f in pool['frames']),'MOTION_TIME_REPRESENTATION')
    return math.prod(len(f['candidates']) for f in pool['frames'])


def fit(times,positions):
    hours=[t/3600 for t in times];mean=math.fsum(hours)/3
    dt=[t-mean for t in hours];den=math.fsum(t*t for t in dt)
    require(den>0,'MOTION_TIME_BASELINE')
    center=[math.fsum(p[k] for p in positions)/3 for k in (0,1)]
    velocity=[math.fsum(t*(p[k]-center[k]) for t,p in zip(dt,positions))/den for k in (0,1)]
    intercept=[center[k]-velocity[k]*mean for k in (0,1)]
    residuals=[[p[k]-intercept[k]-velocity[k]*h for k in (0,1)] for p,h in zip(positions,hours)]
    distances=[math.hypot(*r) for r in residuals]
    result={'interceptArcsec':intercept,'velocityArcsecPerHour':velocity,
        'residualVectorsArcsec':residuals,'radialRMSArcsec':math.hypot(*distances)/math.sqrt(3),
        'maximumResidualArcsec':max(distances)}
    require(all(finite(x) for x in intercept+velocity+distances),'MOTION_FIT_OVERFLOW');return result


def inspect(pool_path,pool_sha,evidence_path,evidence_sha):
    pool,actual=read_json(safe_path(pool_path));evidence,actual_evidence=read_json(safe_path(evidence_path))
    require(digest(pool_sha) and digest(evidence_sha) and actual==pool_sha and actual_evidence==evidence_sha
        and pool['sourceEvidenceSha256']==evidence_sha,'MOTION_INPUT_PIN')
    count=validate_pool(pool)
    fields(evidence,{'schema','files'})
    require(evidence['schema']=='BKL051_MOTION_PRIVATE_EVIDENCE_V1'
        and type(evidence['files']) is list and 1<=len(evidence['files'])<=128,'MOTION_EVIDENCE')
    hashes=set();paths=set()
    for r in evidence['files']:
        fields(r,{'path','sha256'})
        require(type(r['path']) is str and Path(r['path']).is_absolute() and r['path'] not in paths
            and digest(r['sha256']) and fingerprint(r['path'])['sha256']==r['sha256'],'MOTION_EVIDENCE_CHANGED')
        hashes.add(r['sha256']);paths.add(r['path'])
    require(all(f[k] in hashes for f in pool['frames'] for k in ('imageSha256','catalogSha256')),'MOTION_FRAME_EVIDENCE')
    hypotheses=[]
    if 0<count<=LIMIT:
        times=[f['elapsedSeconds'] for f in pool['frames']]
        for selection in itertools.product(*(f['candidates'] for f in pool['frames'])):
            ids=[d['detectionRef'] for d in selection]
            hypotheses.append({'hypothesisRef':hashlib.sha256((pool_sha+''.join(ids)).encode()).hexdigest()[:32],
                'detectionRefs':ids,**fit(times,[d['positionArcsec'] for d in selection]),
                'associationState':'UNREVIEWED_HYPOTHESIS','velocityCovariance':None,'significance':None})
    require(read_json(safe_path(pool_path))[1]==pool_sha and read_json(safe_path(evidence_path))[1]==evidence_sha
        and all(fingerprint(r['path'])['sha256']==r['sha256'] for r in evidence['files']),'MOTION_SOURCE_CHANGED')
    return {'schema':'BKL051_MOTION_HYPOTHESES_V1','poolSha256':pool_sha,'pool':pool,
        'expectedHypotheses':count,'hypotheses':hypotheses,
        'status':'RESOURCE_LIMIT_NO_PARTIAL_SELECTION' if count>LIMIT else 'EMPTY_POOL_NOT_NONDETECTION' if count==0 else 'ALL_POOL_HYPOTHESES_ENUMERATED',
        'resourceLimit':LIMIT,'selectedHypothesis':None,'model':'UNWEIGHTED_LINEAR_TANGENT_PLANE_DESCRIPTIVE_NOT_ORBIT',
        'crossEpochCovariance':None,'scienceValidation':'NOT_VALIDATED','trackletAccepted':False,
        'movingObjectClassification':'NOT_EVALUATED','blindRecovery':False,'qualifiedControls':0,'submissionAuthorized':False}


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('pool','pool-sha','evidence','evidence-sha','output'):p.add_argument('--'+n,required=True)
    a=p.parse_args();print(write_new(Path(a.output),inspect(a.pool,a.pool_sha,a.evidence,a.evidence_sha)))


if __name__=='__main__':main()
