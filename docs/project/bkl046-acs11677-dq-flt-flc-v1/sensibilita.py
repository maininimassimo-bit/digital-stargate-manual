"""Change only the DQ source on the frozen 11677 support coordinates."""
from contextlib import ExitStack
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
BASE=Path('O:/')
sys.path[:0]=[str(ROOT),str(BASE/'BKL046-ACS-WFC-runtime-7.2.0')]
from verifica import pin
from astropy.io import fits
import numpy as np


def groups(mask):
    rest={tuple(map(int,point)) for point in np.argwhere(mask)}
    while rest:
        seed=min(rest)
        rest.remove(seed)
        queue=[seed]
        group=[]
        while queue:
            y,x=queue.pop()
            group.append((y,x))
            for i in range(y-1,y+2):
                for j in range(x-1,x+2):
                    if (i,j) in rest:
                        rest.remove((i,j))
                        queue.append((i,j))
        yield np.array(group)


def main(out):
    source=BASE/'BKL046-ACS-11677-scie-DQ-v1/riscontro.json'
    parent_sha='c7ab445f872054b6c4261c1250a733443c8b0d2316a8f0126e102f976235e43d'
    assert pin(source)==parent_sha
    rows=json.loads(source.read_bytes())['cases']
    plan=json.loads((ROOT/'protocollo.json').read_bytes())
    report=[]
    with ExitStack() as stack:
        dq={}
        for phase,program in plan['images'].items():
            dq[phase]={}
            for kind,meta in program.items():
                path=BASE/meta['folder']/'source'/meta['file']
                assert pin(path)==meta['sha256']
                filename=stack.enter_context(fits.open(path,mode='readonly',memmap=True))
                dq[phase][kind]=filename
        actual=[]
        for ext in (1,2):
            image=dq['long']['FLC']
            long_flt=dq['long']['FLT']['DQ',ext].data
            long_flc=image['DQ',ext].data
            chip=image['SCI',ext].header['CCDCHIP']
            short_flt=dq['short']['FLT']['DQ',ext].data
            short_flc=dq['short']['FLC']['DQ',ext].data
            for group in groups((long_flc&256)!=0):
                ys,xs=group.T
                height=int(ys.max()-ys.min()+1)
                if height<21:continue
                x=float(np.median(xs))
                y=float((ys.min()+ys.max())/2)
                actual.append((chip,[x,y],height,ys,xs,long_flt,long_flc,short_flt,short_flc))
        assert len(actual)==len(rows)==340
        for (chip,center,height,ys,xs,long_flt,long_flc,short_flt,short_flc),row in zip(actual,rows):
            assert chip==row['chip'] and center==row['centerXY'] and height==row['verticalSpan']
            flc,long_flags=long_flc[ys,xs],long_flt[ys,xs]
            assert int(np.count_nonzero(flc!=256))==row['mixedLongPixels']
            flags4096=lambda q:int(np.count_nonzero(q&4096))
            short=row['short']['A1']
            known=short['state'] in ('SHORT_OTHER_DQ','CANDIDATE_UNSATURATED_REFERENCE')
            short_counts=None
            if known:
                x,y=short['peakXY']
                yy,xx=np.mgrid[y-10:y+11,x-10:x+11]
                sel=(xx-x)**2+(yy-y)**2<=100
                q=short_flc[yy[sel],xx[sel]]
                alt=short_flt[yy[sel],xx[sel]]
                assert int(np.count_nonzero(q))==short['apertureNonzeroDQ']
                short_counts=dict(flc=flags4096(q),flt=flags4096(alt),
                                  alternativeClean=bool(np.all(alt==0)))
            report.append(dict(chip=int(chip),centerXY=center,long4096=dict(flc=flags4096(flc),
                    flt=flags4096(long_flags)),bothPreservedFullWell=bool(np.all((long_flags&256)!=0)),
                    alternativePureLong=bool(np.all(long_flags==256)),short=short_counts))
    result=dict(protocol='BKL046_ACS11677_FROZEN_SUPPORT_DQ_SENSITIVITY_V1',
                priorSha256=parent_sha,mode='Fixed FLC coordinates and support; substitute FLT DQ for comparison only.',
                cases=report,photometryPerformed=False,scientificClosures=0,nativeExecutions=0)
    with out.open('xb') as stream:
        stream.write(json.dumps(result,indent=2,sort_keys=True,allow_nan=False).encode()+b'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))