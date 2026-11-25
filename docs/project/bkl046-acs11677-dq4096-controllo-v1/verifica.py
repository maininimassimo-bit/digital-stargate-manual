from contextlib import ExitStack
from hashlib import file_digest,sha256
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
BASE=Path('O:/')
sys.path.insert(0,str(BASE/'BKL046-ACS-WFC-runtime-7.2.0'))
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np


def pin(path):
    with path.open('rb') as f:return file_digest(f,'sha256').hexdigest()


def read_json(path,expected):
    raw=path.read_bytes()
    assert sha256(raw).hexdigest()==expected
    return json.loads(raw)


def trails(mask,span):
    coords=[tuple(map(int,row)) for row in np.argwhere(mask)]
    remaining=set(coords)
    for seed in coords:
        if seed not in remaining:continue
        remaining.remove(seed)
        group=[]
        stack=[seed]
        while stack:
            y,x=stack.pop()
            group.append((y,x))
            for i in range(y-1,y+2):
                for j in range(x-1,x+2):
                    if (i,j) in remaining:
                        remaining.remove((i,j))
                        stack.append((i,j))
        if max(y for y,x in group)-min(y for y,x in group)+1>=span:
            yield np.asarray(sorted(group),dtype=int)


def distribution(records,plan):
    groups={}
    for ident,_,_,_,a,b in records:
        groups.setdefault(ident,[]).append((a,b))
    rng=np.random.default_rng(plan['seed'])
    ref=0
    repeated=0
    overlap=0
    expected=0
    shuffled=np.zeros(plan['iterations'],dtype=np.int64)
    for rows in groups.values():
        a,b=np.asarray(rows,dtype=bool).T
        n=len(a)
        ref+=int(a.sum())
        repeated+=int(b.sum())
        overlap+=int((a&b).sum())
        expected+=int(a.sum())*int(b.sum())/n
        shifts=rng.integers(0,n,size=len(shuffled))
        for j,shift in enumerate(shifts):
            shuffled[j]+=int(np.count_nonzero(a&np.roll(b,int(shift))))
    return dict(nearestCommonFullWell=len(records),trails=len(groups),referenceFlag4096=ref,
                repeatFlag4096=repeated,observedBoth=overlap,
                expectedBothGivenTrailCounts=expected,
                cyclicNullMedian=float(np.median(shuffled)),
                cyclicNullCentral95=np.quantile(shuffled,[.025,.975]).tolist(),
                cyclicNullMaximum=int(shuffled.max()),
                cyclesAtOrAboveObserved=int(np.count_nonzero(shuffled>=overlap)))


def main(out):
    raw=(ROOT/'protocollo.json').read_bytes()
    p=json.loads(raw)
    folder=BASE/'BKL046-ACS-11677-geometria-lunghe-v1'
    geo=read_json(folder/'riscontro.json',p['geometrySha256'])
    prior=read_json(folder/'sensibilita-dq.json',p['previousMapperReportSha256'])
    replica=BASE/'BKL046-ACS-11677-DQ-replique-v1'
    base=read_json(replica/'riscontro.json',p['replicaResultSha256'])
    fit=next(c for c in geo['chips'] if c['chip']==p['chip'])
    assert fit['models']['affine']['passes']
    files=[BASE/'BKL046-ACS-11677-fotometria-v2/source/jb6v01e0q_flc.fits',replica/'jb6v01e5q_flc.fits']
    assert [pin(f) for f in files]==base['inputSha256']
    with ExitStack() as stack:
        a,b=[stack.enter_context(fits.open(f,mode='readonly',memmap=True)) for f in files]
        assert a['SCI',1].header['CCDCHIP']==b['SCI',1].header['CCDCHIP']==p['chip']
        qa,qb=a['DQ',1].data,b['DQ',1].data
        ax,bx=WCS(a['SCI',1].header,a),WCS(b['SCI',1].header,b)
        points=np.asarray([r['source'] for r in fit['anchors']])
        fit_rows=np.asarray([sum(r['tile'])%2==0 for r in fit['anchors']])
        measured=np.asarray([r['observed'] for r in fit['anchors']])
        estimate=np.asarray([r['estimate'] for r in fit['anchors']])
        size=np.array([qa.shape[1],qa.shape[0]],dtype=float)
        basis=lambda c:np.column_stack((np.ones(len(c)),c/size-.5))
        coef,_,rank,_=np.linalg.lstsq(basis(points)[fit_rows],(measured-estimate)[fit_rows],rcond=None)
        assert rank==3
        records=[]
        for ident,group in enumerate(trails((qa&256)!=0,p['minimumVerticalSpanPx'])):
            y,x=group.T
            pts=np.column_stack((x,y))
            proj=bx.all_world2pix(ax.all_pix2world(pts,0,ra_dec_order=True),0,tolerance=1e-8,
                                 maxiter=70,quiet=False,ra_dec_order=True)+basis(pts)@coef
            near=np.rint(proj).astype(int)
            for index,(qx,qy) in enumerate(near):
                if not (0<qx<qb.shape[1]-1 and 0<qy<qb.shape[0]-1 and qb[qy,qx]&256):
                    continue
                dist=float(np.linalg.norm(proj[index]-near[index]))
                records.append((ident,int(qx),int(qy),dist,
                                bool(qa[y[index],x[index]]&4096),bool(qb[qy,qx]&4096)))
    chosen={}
    for idx,(_,x,y,dist,_,_) in enumerate(records):
        key=(x,y)
        if key not in chosen or dist<records[chosen[key]][3]:
            chosen[key]=idx
    uniq=[records[j] for j in sorted(chosen.values())]
    observed=distribution(records,p)
    assert observed['observedBoth']==prior['chips'][0]['stats']['cosmicFlagsOnNearestCommonFullWell']['commonFlagged']
    unique=distribution(uniq,p)
    result=dict(protocol='BKL046_ACS11677_DQ4096_WITHIN_TRAIL_REPEAT_RESULT_V1',
        planSha256=sha256(raw).hexdigest(),projections=observed,distinctTargets=unique,
        duplicatedTargetProjections=len(records)-len(uniq),nullIsDescriptive=True,
        doesNotIdentifyCosmicTruth=True,nativeExecutions=0,scientificClosures=0)
    with out.open('xb') as f:
        f.write(json.dumps(result,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))