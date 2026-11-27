import hashlib
from io import BytesIO
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
COHORT=HERE/'inputs/cohort'
SAT=HERE/'inputs/targets'
sys.path.insert(0,'O:/BKL046-ACS-WFC-runtime-7.2.0')
import numpy as np
from astropy.io import fits


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def pinned(path, expected):
    raw=path.read_bytes()
    if digest(raw)!=expected:
        raise ValueError('SHA256 drift: '+path.name)
    return raw


def read_frame(path, sha):
    with fits.open(BytesIO(pinned(path,sha)),memmap=False) as hdus:
        image=hdus[0].data
    if image.shape!=(1024,1024) or image.dtype.kind not in 'iu':
        raise ValueError('Detector frame')
    return image


def bias(image):
    rows=(slice(2,6),slice(1018,1022))
    cols=(slice(64,448),slice(576,960))
    return np.array([[np.median(image[y,x]) for x in cols] for y in rows])


def extract(image, box, corrected):
    x0,y0,x1,y1=box
    pixels=image[y0:y1,x0:x1].astype(np.float64)
    if corrected:
        q=bias(image)
        yq=(np.arange(y0,y1)>=512).astype(np.intp)
        xq=(np.arange(x0,x1)>=512).astype(np.intp)
        pixels-=q[yq[:,None],xq[None,:]]
    return pixels


def measure(pred, raw, ceiling):
    expected=pred>=ceiling
    actual=raw==ceiling
    clean=~actual
    residual=(pred-raw)[clean]
    return dict(tp=int(np.count_nonzero(expected&actual)), fp=int(np.count_nonzero(expected&~actual)),
                tn=int(np.count_nonzero(~expected&~actual)), fn=int(np.count_nonzero(~expected&actual)),
                unclippedPixels=int(residual.size),
                unclippedMedianErrorDn=float(np.median(residual)) if residual.size else None,
                unclippedMaeDn=float(np.mean(np.abs(residual))) if residual.size else None)


def main(out):
    design=(HERE/'protocollo.json').read_bytes()
    p=json.loads(design)
    cohort=json.loads(pinned(COHORT/'riscontro.json',p['cohortSha256']))
    sat=json.loads(pinned(SAT/'protocollo.json',p['saturationPlanSha256']))
    acquisition=json.loads(pinned(SAT/'acquisizione.json',p['saturationAcquisitionSha256']))
    assert acquisition['designSha256']==p['saturationPlanSha256'] and acquisition['verified']==48
    sat_pins={row['name']:row['sha256'] for row in acquisition['files']}
    boxes=dict(center=sat['centralRoi'],**sat['regions'])
    ceiling=p['thresholdDn']
    records=[]
    train={}
    for stage, groups in p['training'].items():
        train[stage]=[]
        for group in groups:
            candidates=sorted((r for r in cohort['identities'] if r['run']==group),key=lambda r:r['start'])
            assert len(candidates)==10
            chosen=candidates[:p['trainingFramesPerLevel']]
            assert len({row['exposureMs'] for row in chosen})==1
            train[stage].append((chosen[0]['exposureMs'],chosen))
    target_names={row['name'] for group in p['heldOutGroups'] for row in sat['selected'][group]}
    assert len(target_names)==12 and not target_names.intersection(row['fit'] for levels in train.values() for _,rows in levels for row in rows)
    for stage,levels in train.items():
        trained=[(time,[read_frame(COHORT/'source'/row['fit'],row['fitsSha256']) for row in rows])
                 for time,rows in levels]
        for model in p['models']:
            corrected=model=='parallelOverscan'
            summaries=[]
            for time, frames in trained:
                arrays={}
                for region,box in boxes.items():
                    assert all(np.max(extract(frame,box,False))<ceiling for frame in frames)
                    arrays[region]=np.median([extract(frame,box,corrected) for frame in frames],axis=0)
                summaries.append((time,arrays))
            (t0,low),(t1,high)=summaries
            assert t0<t1
            for group in p['heldOutGroups']:
                for row in sat['selected'][group]:
                    name=row['name']
                    frame=read_frame(SAT/'source'/name,sat_pins[name])
                    weight=(row['integrationMs']-t0)/(t1-t0)
                    assert weight>1
                    by_region={}
                    for region,box in boxes.items():
                        raw=extract(frame,box,False)
                        target_bias=raw-extract(frame,box,True) if corrected else 0
                        pred=low[region]+weight*(high[region]-low[region])+target_bias
                        by_region[region]=measure(pred,raw,ceiling)
                    records.append(dict(training=stage,model=model,group=group,frame=name,results=by_region))
    assert len(records)==48
    result=dict(protocol='BKL046_TV4_SATURATION_PREDICTION_RESULT_V1',designSha256=digest(design),
                evaluatedFrames=len(target_names),records=records, fit= 'two-level medians',
                sameSession=True,censoredValuesRecovered=False,nativeExecutions=0,scientificClosures=0)
    with out.open('xb') as stream:
        stream.write(json.dumps(result,indent=2,sort_keys=True,allow_nan=False).encode()+b'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))