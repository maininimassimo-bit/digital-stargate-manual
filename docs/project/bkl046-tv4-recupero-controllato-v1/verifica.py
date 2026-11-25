"""Measure recovery against observed, deliberately censored raw TV4 values."""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from modello import bias,digest,extract,pinned,read_frame,np

COHORT=Path('O:/BKL046-TV4-CLEAR1-saturazione-predizione-v1/inputs/cohort')
COHORT_PIN='5cc3749b5b4337f62303ca8aba3889d08ecedcffcd1f84cd4f1843043653aea2'


def stats(prediction, pixels, cap):
    masked=pixels>cap
    truth=pixels[masked]
    if not truth.size:
        return dict(count=0)
    prediction=np.maximum(cap,prediction[masked])
    delta=prediction-truth
    return dict(count=truth.size,maeDn=float(np.abs(delta).mean()),
                signedFluxErrorFraction=float(delta.sum()/truth.sum()),
                trueSumDn=float(truth.sum()),estimatedSumDn=float(prediction.sum()))


def main(out):
    design=(ROOT/'protocollo.json').read_bytes()
    p=json.loads(design)
    source=json.loads((ROOT/'acquisizione.json').read_bytes())
    assert source['designSha256']==digest(design) and source['verified']==12
    input_pins={r['name']:r['sha256'] for r in source['files']}
    c=json.loads(pinned(COHORT/'riscontro.json',COHORT_PIN))
    boxes=dict(center=p['centralRoi'],**p['regions'])
    targets=p['selected']['DC']
    assert len(targets)==6 and all(t['integrationMs']==10003.5 for t in targets)
    fit={}
    for label,groups in p['training'].items():
        levels=[]
        for group in groups:
            rows=sorted((r for r in c['identities'] if r['run']==group),key=lambda r:r['start'])[:6]
            assert len(rows)==6 and len({r['exposureMs'] for r in rows})==1
            assert not {r['fit'] for r in rows}.intersection(t['name'] for t in targets)
            frames=[read_frame(COHORT/'source'/r['fit'],r['fitsSha256']) for r in rows]
            levels.append((rows[0]['exposureMs'],{
                reg:np.median([extract(frame,box,True) for frame in frames],axis=0)
                for reg,box in boxes.items()}))
        assert levels[0][0]<10003.5<levels[1][0]
        fit[label]=levels
    measures=[]
    for target in targets:
        name=target['name']
        frame=read_frame(ROOT/'source'/name,input_pins[name])
        exposure=target['integrationMs']
        for reg,box in boxes.items():
            raw=extract(frame,box,False)
            assert raw.max()<p['codeCeilingDn']
            offset=raw-extract(frame,box,True)
            preds={}
            for stage,((t0,low),(t1,high)) in fit.items():
                alpha=(exposure-t0)/(t1-t0)
                preds[stage+'TwoLevels']=low[reg]+alpha*(high[reg]-low[reg])+offset
                preds[stage+'ShortOnly']=low[reg]*(exposure/t0)+offset
            for cap in p['syntheticCapsDn']:
                result={'clippedLowerBound':stats(np.full_like(raw,cap),raw,cap)}
                result.update({m:stats(pred,raw,cap) for m,pred in preds.items()})
                assert all(r['count']==result['clippedLowerBound']['count'] for r in result.values())
                measures.append(dict(frame=name,region=reg,syntheticCapDn=cap,results=result))
    assert len(measures)==60
    result=dict(protocol='BKL046_TV4_CONTROLLED_CENSORING_RECOVERY_RESULT_V1',
                designSha256=digest(design),cohortSha256=COHORT_PIN,measures=measures,
                targetFrames=6,sameSession=True,hardwareSaturationRecoveryVerified=False,
                scientificClosures=0,nativeExecutions=0)
    with out.open('xb') as stream:
        stream.write(json.dumps(result,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))