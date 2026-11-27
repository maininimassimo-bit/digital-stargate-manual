from contextlib import ExitStack
from hashlib import file_digest
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
BASE=Path('O:/')
PREVIOUS=BASE/'BKL046-ACS-11677-DQ-replique-v1'
sys.path[:0]=[str(PREVIOUS),str(BASE/'BKL046-ACS-WFC-runtime-7.2.0')]
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
from verifica import extended_support, projected_counts


def pin(path):
    with path.open('rb') as stream:return file_digest(stream,'sha256').hexdigest()


def main(out):
    geometry=ROOT/'riscontro.json'
    sha=pin(geometry)
    assert sha==pin(ROOT/'replay.json')
    report=json.loads(geometry.read_bytes())['chips']
    predecessor=json.loads((PREVIOUS/'riscontro.json').read_bytes())
    pins=predecessor['inputSha256']
    files=[BASE/'BKL046-ACS-11677-fotometria-v2/source/jb6v01e0q_flc.fits',PREVIOUS/'jb6v01e5q_flc.fits']
    assert [pin(path) for path in files]==pins
    rows=[]
    with ExitStack() as stack:
        a,b=[stack.enter_context(fits.open(p,mode='readonly',memmap=True)) for p in files]
        for ext in (1,2):
            ah,bh=a['SCI',ext],b['SCI',ext]
            chip=ah.header['CCDCHIP']
            row=next(x for x in report if x['chip']==chip)
            if not row['models']['affine']['passes']:
                rows.append(dict(chip=int(chip),applied=False,reason='HELDOUT_P90_OUTSIDE_LIMIT'))
                continue
            qa,qb=a['DQ',ext].data,b['DQ',ext].data
            points=np.asarray([r['source'] for r in row['anchors']])
            train=np.asarray([sum(r['tile'])%2==0 for r in row['anchors']])
            resid=np.asarray([r['observed'] for r in row['anchors']])-np.asarray([r['estimate'] for r in row['anchors']])
            size=np.array([qa.shape[1],qa.shape[0]],dtype=float)
            cols=lambda p:np.column_stack((np.ones(len(p)),p/size-.5))
            fitted,_,rank,_=np.linalg.lstsq(cols(points)[train],resid[train],rcond=None)
            assert rank==3
            aw,bw=WCS(ah.header,a),WCS(bh.header,b)
            def project(px):
                world=aw.all_pix2world(px,0,ra_dec_order=True)
                return bw.all_world2pix(world,0,tolerance=1e-8,maxiter=70,quiet=False,
                                       ra_dec_order=True)+cols(px)@fitted
            coords,num=extended_support(qa,256,21)
            stats=projected_counts(qa,qb,project,coords,4096,256)
            rows.append(dict(chip=int(chip),applied=True,components=num,stats=stats))
    assert len(rows)==2 and sum(r['applied'] for r in rows)==1
    result=dict(protocol='BKL046_ACS11677_DQ_AFFINE_SENSITIVITY_V1',geometrySha256=sha,chips=rows,
                astrophysicalTruthReconstructed=False,nativeExecutions=0,scientificClosures=0)
    with out.open('xb') as stream:
        stream.write(json.dumps(result,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))