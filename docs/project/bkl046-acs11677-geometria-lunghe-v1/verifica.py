from collections import Counter
from contextlib import ExitStack
from hashlib import file_digest,sha256
import json
from pathlib import Path
import runpy
import sys

ROOT=Path(__file__).resolve().parent
BASE=Path('O:/')
sys.path.insert(0,str(BASE/'BKL046-ACS-WFC-runtime-7.2.0'))
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np


def digest(path):
    with path.open('rb') as stream:return file_digest(stream,'sha256').hexdigest()


def load_fn(path,pin,field):
    assert digest(path)==pin
    return runpy.run_path(str(path))[field]


def fit(points,resid,training,holdout,tile,plan,shape):
    records={}
    if min(training.sum(),holdout.sum())<plan['minFitAndHoldoutStars']:
        return 'INSUFFICIENT_STARS',records
    if min(len(np.unique(tile[no],axis=0)) for no in (training,holdout))<plan['minFitAndHoldoutTiles']:
        return 'INSUFFICIENT_TILES',records
    size=np.array([shape[1],shape[0]],dtype=float)
    design=np.column_stack((np.ones(len(points)),points/size-.5))
    coef,_,rank,_=np.linalg.lstsq(design[training],resid[training],rcond=None)
    assert rank==3
    shift=np.median(resid[training],axis=0)
    for name,corr in [('primaryWcs',0),('translation',shift),('affine',design@coef)]:
        radial=np.linalg.norm((resid-corr)[holdout],axis=1)
        median,p90=map(float,np.quantile(radial,[.5,.9]))
        records[name]=dict(medianPx=median,p90Px=p90,
                           countWithinLimit=int((radial<=plan['heldoutP90LimitPx']).sum()),
                           passes=p90<=plan['heldoutP90LimitPx'])
    return 'MEASURED',records


def main(out):
    raw=(ROOT/'protocollo.json').read_bytes()
    p=json.loads(raw)
    ancestor=BASE/'BKL046-ACS-11677-DQ-replique-v1/riscontro.json'
    assert digest(ancestor)==p['parentResultSha256']
    input_pins=json.loads(ancestor.read_bytes())['inputSha256']
    seeds=load_fn(BASE/'BKL046-GO14949-nuovo-puntamento-v1/check_new_pointing.py',p['seedSourceSha256'],'seeds')
    centroid=load_fn(BASE/'BKL046-GO14949-registrazione-profondita-v1/transfer.py',p['centroidSourceSha256'],'centroid')
    pair=[BASE/'BKL046-ACS-11677-fotometria-v2/source/jb6v01e0q_flc.fits',
          BASE/'BKL046-ACS-11677-DQ-replique-v1/jb6v01e5q_flc.fits']
    reports=[]
    with ExitStack() as stack:
        frames=[]
        for i,path in enumerate(pair):
            assert digest(path)==input_pins[i]
            frames.append(stack.enter_context(fits.open(path,mode='readonly',memmap=True)))
        a,b=frames
        for ext in (1,2):
            am,bm=a['SCI',ext],b['SCI',ext]
            aq,bq=a['DQ',ext].data,b['DQ',ext].data
            chip=am.header['CCDCHIP']
            assert bm.header['CCDCHIP']==chip
            aw,bw=WCS(am.header,a),WCS(bm.header,b)
            assert aw.wcs.radesys==bw.wcs.radesys=='ICRS'
            seed_image=np.where(aq==0,am.data,-np.inf)
            accepted=[]
            rejects=Counter()
            others=[]
            all_seeds=list(seeds(np,seed_image,p))
            for seed in all_seeds:
                xy,err=centroid(np,am.data,aq,np.array(seed))
                if err:
                    rejects['reference_'+err]+=1
                else:
                    others.append((seed,xy))
            coords=np.asarray([xy for _,xy in others])
            world=aw.all_pix2world(coords,0,ra_dec_order=True)
            forecasts=bw.all_world2pix(world,0,tolerance=1e-8,maxiter=60,ra_dec_order=True)
            used=set()
            rows=[]
            for (seed,xy),guess in zip(others,forecasts):
                measured,err=centroid(np,bm.data,bq,guess)
                if err:
                    rejects['repeat_'+err]+=1
                    continue
                match=tuple(np.rint(measured).astype(int))
                if match in used:
                    rejects['duplicate_repeat_peak']+=1
                    continue
                used.add(match)
                tile=np.array(seed)//p['tilePixels']
                accepted.append((xy,tile,measured-guess))
                rows.append(dict(source=xy.tolist(),estimate=guess.tolist(),observed=measured.tolist(),
                                 tile=tile.tolist()))
            points,tiles,resid=(np.array([row[i] for row in accepted]) for i in range(3))
            train=tiles.sum(axis=1)%2==0
            test=~train
            status,report=fit(points,resid,train,test,tiles,p,am.data.shape)
            reports.append(dict(chip=int(chip),candidates=len(all_seeds),accepted=len(accepted),
                rejected=dict(rejects),fitStars=int(train.sum()),heldoutStars=int(test.sum()),
                fitTiles=len(np.unique(tiles[train],axis=0)),heldoutTiles=len(np.unique(tiles[test],axis=0)),
                status=status,models=report,anchors=rows))
            assert len(all_seeds)==len(accepted)+sum(rejects.values())
    data=dict(protocol='BKL046_ACS11677_LONG_PAIR_GEOMETRY_RESULT_V1',
              designSha256=sha256(raw).hexdigest(),chips=reports,matchedSaturatedObjectsQualified=False,
              nativeExecutions=0,scientificClosures=0)
    with out.open('xb') as sink:
        sink.write(json.dumps(data,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))