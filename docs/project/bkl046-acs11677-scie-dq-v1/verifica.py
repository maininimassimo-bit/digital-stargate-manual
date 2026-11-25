from contextlib import ExitStack
from hashlib import file_digest,sha256
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
STORE=Path('O:/')
sys.path.insert(0,str(STORE/'BKL046-ACS-WFC-runtime-7.2.0'))
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np


def digest(raw):return sha256(raw).hexdigest()


def components(mask):
    points={tuple(map(int,p)) for p in np.argwhere(mask)}
    while points:
        seed=min(points)
        points.remove(seed)
        pending=[seed]
        cluster=[]
        while pending:
            y,x=pending.pop()
            cluster.append((y,x))
            for i in range(y-1,y+2):
                for j in range(x-1,x+2):
                    q=(i,j)
                    if q in points:
                        points.remove(q)
                        pending.append(q)
        yield np.array(cluster)


def dq_counts(values):
    codes,counts=np.unique(values.astype(np.uint16),return_counts=True)
    return {str(int(k)):int(v) for k,v in zip(codes,counts)}


def short_masks(values, state, plan):
    # Reuse the original geometric, signal, and finite support checks.
    if state not in ('CANDIDATE_UNSATURATED_REFERENCE','SHORT_OTHER_DQ'):
        return {str(mask):False for mask in plan['dqDiagnostics']['masks']}
    values=values.astype(np.uint16)
    return {str(mask):bool(np.all((values&(65535^mask))==0))
            for mask in plan['dqDiagnostics']['masks']}


def screen(hdu, flags, projection, plan):
    x,y=map(float,projection)
    if not np.isfinite([x,y]).all():
        return dict(state='WCS_INVALID')
    i,j=round(x),round(y)
    if not (20<=i<hdu.shape[1]-20 and 20<=j<hdu.shape[0]-20):
        return dict(state='EDGE')
    ys,xs=np.mgrid[j-20:j+21,i-20:i+21]
    sig=hdu[j-20:j+21,i-20:i+21].astype(float)
    q=flags[j-20:j+21,i-20:i+21]
    r2=(xs-x)**2+(ys-y)**2
    near=r2<=plan['shortLocalSearchPx']**2
    ann=(r2>=14**2)&(r2<=19**2)&(q==0)&np.isfinite(sig)
    if ann.sum()<100 or not np.isfinite(sig[near]).all():
        return dict(state='BACKGROUND_OR_PEAK_SUPPORT')
    index=int(np.argmax(np.where(near,sig,-np.inf)))
    px,py=int(xs.flat[index]),int(ys.flat[index])
    peak=float(sig.flat[index]-np.median(sig[ann]))
    shift=float(np.hypot(px-x,py-y))
    area=(xs-px)**2+(ys-py)**2<=plan['baseRadiusPx']**2
    bad=area&(q!=0)
    n_full=int(np.count_nonzero(area&((q&plan['longBit'])!=0)))
    state='CANDIDATE_UNSATURATED_REFERENCE'
    if shift>plan['shortMaxPeakShiftPx'] or peak<plan['shortMinPeakAboveBackgroundElectrons']:
        state='PEAK_SUPPORT_OR_RELOCATION'
    elif n_full:
        state='SHORT_FULL_WELL'
    elif np.any(bad):
        state='SHORT_OTHER_DQ'
    elif not np.isfinite(sig[area]).all():
        state='SHORT_NONFINITE'
    return dict(state=state,peakAboveBackground=peak,peakShiftPx=shift,
                apertureNonzeroDQ=int(bad.sum()),apertureFullWell=n_full,projectedXY=[x,y],peakXY=[px,py],
                apertureDqCounts=dq_counts(q[area]),maskSensitivity=short_masks(q[area],state,plan))


def analyze(plan, files):
    cases=[]
    with ExitStack() as stack:
        images={}
        for role in plan['roles']:
            entry=plan['fits'][role]
            name,seconds,pin=entry['file'],entry['seconds'],entry['sha256']
            path=STORE/entry['sourceFolder']/'source'/name
            with path.open('rb') as stream:
                if file_digest(stream,'sha256').hexdigest()!=pin:
                    raise ValueError('Input changed '+name)
            h=stack.enter_context(fits.open(path,mode='readonly',memmap=True))
            assert h[0].header['EXPTIME']==seconds
            images[role]=h
            files.append(dict(name=name,sha256=pin,exposureSeconds=seconds))
        for ext in (1,2):
            geometry={k:WCS(h['SCI',ext].header,h) for k,h in images.items()}
            chip=images['L1457']['SCI',ext].header['CCDCHIP']
            assert all(h['SCI',ext].header['CCDCHIP']==chip and
                h['SCI',ext].header['BUNIT'].strip().upper()=='ELECTRONS' for h in images.values())
            long_dq=images['L1457']['DQ',ext].data
            for group in components((long_dq&plan['longBit'])!=0):
                ys,xs=group.T
                height=int(ys.max()-ys.min()+1)
                if height<plan['minVerticalSpanPx']:
                    continue
                xc=float(np.median(xs))
                yc=float((ys.min()+ys.max())/2)
                coord=geometry['L1457'].all_pix2world([[xc,yc]],0,ra_dec_order=True)
                short={}
                for name in ('A1',):
                    h=images[name]
                    projection=geometry[name].all_world2pix(coord,0,tolerance=1e-8,maxiter=70,quiet=False,ra_dec_order=True)[0]
                    short[name]=screen(h['SCI',ext].data,h['DQ',ext].data,projection,plan)
                dq=long_dq[ys,xs]
                cases.append(dict(chip=int(chip),centerXY=[xc,yc],verticalSpan=height,
                    fullWellPixels=len(ys),mixedLongPixels=int(np.count_nonzero(dq!=plan['longBit'])),
                    longDqCounts=dq_counts(dq),
                    longMaskSensitivity={str(bits):bool(np.all((dq.astype(np.uint16)&
                         (65535^(bits|plan['longBit'])))==0)) for bits in plan['dqDiagnostics']['masks']},
                    pixelsOutsideStandard=int(np.count_nonzero((xs-xc)**2+(ys-yc)**2>plan['baseRadiusPx']**2)),
                    short=short))
    return cases


def main(output):
    raw=(ROOT/'protocollo.json').read_bytes()
    p=json.loads(raw)
    files=[]
    results=analyze(p,files)
    parent=(STORE/'BKL046-ACS-11677-scie-riferimento-breve-v1/riscontro.json').read_bytes()
    assert digest(parent)==p['parentReportSha256']
    previous=json.loads(parent)['cases']
    assert len(previous)==len(results)
    for source,updated in zip(previous,results):
        assert all(updated[k]==v for k,v in source.items() if k!='short')
        assert all(updated['short']['A1'][k]==v for k,v in source['short']['A1'].items())
    report=dict(protocol='BKL046_ACS11677_TRAIL_DQ_ATTRITION_RESULT_V1', designSha256=digest(raw),
                inputs=files,cases=results,photometryPerformed=False,
                geometricQualification=False,nativeExecutions=0,scientificClosures=0)
    with output.open('xb') as out:
        out.write(json.dumps(report,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))