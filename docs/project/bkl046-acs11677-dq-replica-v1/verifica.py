from contextlib import ExitStack
from hashlib import file_digest, sha256
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


def extended_support(dq,bit,span):
    coords=[tuple(map(int,p)) for p in np.argwhere((dq&bit)!=0)]
    available=set(coords)
    retained=[]
    components=0
    for seed in coords:
        if seed not in available:continue
        available.remove(seed)
        pending=[seed]
        group=[]
        while pending:
            y,x=pending.pop()
            group.append((y,x))
            for i in range(y-1,y+2):
                for j in range(x-1,x+2):
                    if (i,j) in available:
                        available.remove((i,j))
                        pending.append((i,j))
        if max(y for y,x in group)-min(y for y,x in group)+1>=span:
            components+=1
            retained.extend(group)
    return np.array(retained,dtype=int),components


def projected_counts(reference, successor, world, coords, bit_cosmic, bit_full):
    n=len(coords)
    in_view=0
    hits=0
    nearby=0
    flag_stats={'referenceFlagged':0,'repeatFlagged':0,'commonFlagged':0,
                'baselineOnly':0,'repeatOnly':0,'neitherFlagged':0}
    dist=[]
    for low in range(0,n,8192):
        y,x=coords[low:low+8192].T
        px=world(np.column_stack((x,y)))
        have=np.isfinite(px).all(axis=1)
        i,j=np.rint(np.where(have[:,None],px,0)).astype(int).T
        ok=have&(i>0)&(j>0)&(i<successor.shape[1]-1)&(j<successor.shape[0]-1)
        old=reference[y[ok],x[ok]]
        qx,qy=i[ok],j[ok]
        target=successor[qy,qx]
        in_view+=len(target)
        current=(target&bit_full)!=0
        seen=np.zeros(len(qx),dtype=bool)
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                seen|=(successor[qy+dy,qx+dx]&bit_full)!=0
        hits+=int(current.sum())
        nearby+=int(seen.sum())
        a=((old&bit_cosmic)!=0)[current]
        b=((target&bit_cosmic)!=0)[current]
        for key,mask in [('referenceFlagged',a),('repeatFlagged',b),('commonFlagged',a&b),
                         ('baselineOnly',a&~b),('repeatOnly',~a&b),('neitherFlagged',~a&~b)]:
            flag_stats[key]+=int(mask.sum())
        dist.extend(np.linalg.norm(px[ok]-np.column_stack((x[ok],y[ok])),axis=1).tolist())
    assert hits==sum(flag_stats[k] for k in ('commonFlagged','baselineOnly','repeatOnly','neitherFlagged'))
    return dict(sourceSupport=n,inView=in_view,fullWellNearest=hits,fullWellWithinOnePixel=nearby,
                targetDetectorDisplacementMedianPx=float(np.median(dist)) if dist else None,
                cosmicFlagsOnNearestCommonFullWell=flag_stats)


def main(out):
    p=(ROOT/'protocollo.json').read_bytes()
    plan=json.loads(p)
    receipt=json.loads((ROOT/'acquisizione.json').read_bytes())
    assert receipt['planSha256']==sha256(p).hexdigest()
    orig,repeat=plan['exposures']
    files=[BASE/'BKL046-ACS-11677-fotometria-v2/source'/orig['file'],ROOT/repeat['file']]
    known=['e6011691a50b2608a3cb91e5f9ceb0957aa4a17e46aa04f8e00bee30df5fdd4d',receipt['sha256']]
    result=[]
    with ExitStack() as stack:
        sources=[]
        for path,exp,expected in zip(files,(orig,repeat),known):
            assert pin(path)==expected and path.stat().st_size==exp['bytes']
            archived=BASE/'BKL046-ACS-11677-fotometria-v2/testate'/(exp['root']+'.header')
            assert pin(archived)==exp['archivedFltHeaderSha256']
            h=stack.enter_context(fits.open(path,mode='readonly',memmap=True))
            cal=h[0].header
            for field,wanted in [('ROOTNAME',exp['root']),('ASN_ID',plan['association'])]:
                assert cal[field].strip().lower()==wanted
            assert cal['EXPTIME']==exp['seconds'] and 'F606W' in [cal['FILTER1'],cal['FILTER2']]
            sources.append(h)
        a,b=sources
        assert a[0].header['EXPSTART']!=b[0].header['EXPSTART']
        for ext in (1,2):
            sa,sb=a['SCI',ext],b['SCI',ext]
            assert sa.header['CCDCHIP']==sb.header['CCDCHIP']
            dq_a,dq_b=a['DQ',ext].data,b['DQ',ext].data
            assert dq_a.shape==dq_b.shape
            coords,components=extended_support(dq_a,plan['fullWellBit'],plan['minimumTrailSpan'])
            awcs,bwcs=WCS(sa.header,a),WCS(sb.header,b)
            def project(pixels):
                world=awcs.all_pix2world(pixels,0,ra_dec_order=True)
                return bwcs.all_world2pix(world,0,tolerance=1e-8,maxiter=70,quiet=False,ra_dec_order=True)
            stats=projected_counts(dq_a,dq_b,project,coords,plan['cosmicRayRejectionBit'],plan['fullWellBit'])
            result.append(dict(chip=int(sa.header['CCDCHIP']),longComponents=components,**stats))
    assert sum(r['longComponents'] for r in result)==340 and sum(r['sourceSupport'] for r in result)==82560
    report=dict(protocol='BKL046_ACS11677_INDEPENDENT_LONG_DQ_SUPPORT_RESULT_V1',
                planSha256=receipt['planSha256'],inputSha256=known,chips=result,
                primaryWcsOnly=True,sameVisit=True,cosmicTruthAssigned=False,
                photometryPerformed=False,nativeExecutions=0,scientificClosures=0)
    with out.open('xb') as f:
        f.write(json.dumps(report,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))