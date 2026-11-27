"""Check the published ACS example on pinned original FITS and connected DQ trails."""
from contextlib import ExitStack
from hashlib import file_digest, sha256
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
BASE=Path('O:/')
sys.path[:0]=[str(ROOT),str(BASE/'BKL046-ACS-WFC-runtime-7.2.0')]
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
from connected import connected


def pin(path):
    with path.open('rb') as stream:return file_digest(stream,'sha256').hexdigest()


def load(stack,path,expected):
    if pin(path)!=expected:raise ValueError('Pinned source mismatch: '+path.name)
    return stack.enter_context(fits.open(path,mode='readonly',memmap=True))


def metrics(science,dq,pam, center, seconds, plan):
    x,y=center
    i,j=round(x),round(y)
    w=plan['halfWidthPx']
    if not (w<=i<science.shape[1]-w and w<=j<science.shape[0]-w):
        raise ValueError('Crop touches array edge')
    cut=np.s_[j-w:j+w+1,i-w:i+w+1]
    values=science[cut].astype(float)
    dq=dq[cut]
    area=pam[cut]
    ys,xs=np.mgrid[j-w:j+w+1,i-w:i+w+1]
    r2=(xs-x)**2+(ys-y)**2
    aperture=r2<=plan['radiusPx']**2
    saturation=(dq&256)!=0
    trail=connected(saturation,saturation&aperture)
    if np.any(trail[[0,-1],:]) or np.any(trail[:,[0,-1]]):
        raise ValueError('Trail not bounded')
    selected=aperture|trail
    sky=(r2>=plan['backgroundPx'][0]**2)&(r2<=plan['backgroundPx'][1]**2)&(dq==0)&np.isfinite(values)
    if sky.sum()<300:
        raise ValueError('Insufficient background')
    median=np.median(values[sky])
    report=dict(connectedFullWellPixels=int(trail.sum()), addedFullWellPixels=int((trail&~aperture).sum()),
                exact256Added=int(np.count_nonzero(trail&~aperture&(dq==256))),
                mixedDQAdded=int(np.count_nonzero(trail&~aperture&(dq!=256))),
                center=list(center))
    for name,mask in [('standard',aperture),('extended',selected)]:
        excluded=mask&~np.isin(dq,[0,256])
        if not np.isfinite(values[mask]).all():
            raise ValueError('Nonfinite pixels')
        report[name]=dict(aperturePixels=int(mask.sum()),otherDQPixels=int(excluded.sum()),
                          apertureRateDiagnostic=float(np.sum((values[mask]-median)*area[mask])/seconds),
                          qualityAccepted=not bool(excluded.any()))
        vals,counts=np.unique(dq[excluded],return_counts=True)
        report[name]['otherDQCodes']={str(int(k)):int(v) for k,v in zip(vals,counts)}
    return report


def main(out):
    raw=(ROOT/'protocollo.json').read_bytes()
    p=json.loads(raw)
    base=BASE/'BKL046-GO14949-nuovo-puntamento-v1'
    results={}
    with ExitStack() as stack:
        pam=load(stack,BASE/'BKL046-ACS-GitHub-MAST-d6df7a4fbfeb/wfc2_newpam.fits',p['pamSha256'])[0].data
        images={key:(load(stack,base/row['name'],row['sha256']),row['seconds'])
                for key,row in p['images'].items()}
        s=images['short'][0]
        swcs=WCS(s['SCI',1].header,s)
        world=swcs.all_pix2world([p['notebookXY']],0)[0]
        l=images['long'][0]
        lwcs=WCS(l['SCI',1].header,l)
        projected=lwcs.all_world2pix([world],0,tolerance=1e-9,maxiter=40)[0]
        displacement=float(np.linalg.norm(projected-np.array(p['notebookXY'])))
        for key,(hdus,seconds) in images.items():
            h=hdus['SCI',1]
            q=hdus['DQ',1].data
            assert h.header['CCDCHIP']==2 and hdus[0].header['EXPTIME']==seconds
            assert h.header['BUNIT'].strip().upper()=='ELECTRONS'
            assert all(float(h.header[c])==0 for c in ('LTV1','LTV2')) and h.data.shape==q.shape==pam.shape
            results[key]={'notebookFixed':metrics(h.data,q,pam,p['notebookXY'],seconds,p)}
            if key=='long':
                results[key]['projectedPrimaryWcs']=metrics(h.data,q,pam,projected,seconds,p)
    result=dict(protocol='BKL046_GO14949_NOTEBOOK_TRAIL_DIAGNOSTIC_V1',designSha256=sha256(raw).hexdigest(),
        longProjectionDisplacementPx=displacement,rates=results,independentCalibrationQualified=False,
        matchedAstrometryQualified=False,sciencePixelsReplaced=False,nativeExecutions=0,scientificClosures=0)
    with out.open('xb') as sink:
        sink.write(json.dumps(result,indent=2,sort_keys=True,allow_nan=False).encode()+b'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))