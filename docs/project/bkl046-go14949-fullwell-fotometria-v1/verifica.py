"""Compare isolated pure full-well trails using existing same-field repeats."""
from contextlib import ExitStack
from hashlib import file_digest, sha256
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
BASE=Path('O:/')
sys.path.insert(0,str(BASE/'BKL046-ACS-WFC-runtime-7.2.0'))
from astropy.io import fits
import numpy as np


def pin(path):
    with path.open('rb') as f:
        return file_digest(f,'sha256').hexdigest()


def read(path, expected):
    raw=path.read_bytes()
    assert sha256(raw).hexdigest()==expected
    return json.loads(raw)


def image(stack, path, expected, seconds):
    assert pin(path)==expected
    hdus=stack.enter_context(fits.open(path,mode='readonly',memmap=True))
    h=hdus['SCI',1]
    assert h.header['CCDCHIP']==2 and hdus[0].header['EXPTIME']==seconds
    assert h.header['BUNIT'].strip().upper()=='ELECTRONS'
    assert all(float(h.header[tag])==0 for tag in ('LTV1','LTV2'))
    return h.data,hdus['DQ',1].data


def connected(mask, seeds):
    result=np.zeros(mask.shape,dtype=bool)
    height,width=mask.shape
    pending=[tuple(map(int, point)) for point in np.argwhere(seeds)]
    for y,x in pending:
        result[y,x]=True
    while pending:
        y,x=pending.pop()
        for i in range(max(0,y-1),min(height,y+2)):
            for j in range(max(0,x-1),min(width,x+2)):
                if mask[i,j] and not result[i,j]:
                    result[i,j]=True
                    pending.append((i,j))
    return result


def observe(pair, offset, center, radius, seconds, include_trail, plan):
    data,flags=pair
    x,y=center
    i,j=round(x),round(y)
    w=plan['stampHalfWidthPx']
    if not (w<=i<data.shape[1]-w and w<=j<data.shape[0]-w):
        return dict(state='EDGE')
    s=np.s_[j-w:j+w+1,i-w:i+w+1]
    values=data[s].astype(np.float64)
    q=flags[s]
    pam=offset[s]
    yy,xx=np.mgrid[j-w:j+w+1,i-w:i+w+1]
    r2=(xx-x)**2+(yy-y)**2
    circle=r2<=radius**2
    bounded=~((q&256)!=0)
    # Use bitwise labels for finding connected bleed. Mixed bits are never photometrically allowed.
    extension=connected(~bounded,(r2<=9)&~bounded) if include_trail else np.zeros(q.shape,dtype=bool)
    if include_trail and (not np.any(extension) or np.any(extension[[0,-1],:]) or np.any(extension[:,[0,-1]])):
        return dict(state='BLEED_SUPPORT_UNCERTAIN')
    use=circle|extension
    lo,hi=plan['backgroundAnnulusPx']
    sky=(r2>=lo**2)&(r2<=hi**2)&(q==0)&np.isfinite(values)
    counts=dict(aperturePixels=int(use.sum()),linkedTrailPixels=int(extension.sum()),
                addedTrailPixels=int(np.count_nonzero(extension&~circle)),validBackgroundPixels=int(sky.sum()))
    allowed=np.isin(q,plan['allowedLongCodes']) if include_trail else q==0
    if np.any(~allowed[use]) or not np.isfinite(values[use]).all():
        return dict(state='APERTURE_DQ_OR_NONFINITE',**counts)
    if sky.sum()<180:
        return dict(state='INSUFFICIENT_BACKGROUND',**counts)
    background=np.median(values[sky])
    rate=float(np.sum((values[use]-background)*pam[use])/seconds)
    if not np.isfinite(rate) or rate<=0:
        return dict(state='INVALID_RATE',**counts)
    return dict(state='MEASURED',electronsPerSecond=rate,**counts)


def main(out):
    raw=(ROOT/'protocollo.json').read_bytes()
    plan=json.loads(raw)
    depth=BASE/'BKL046-GO14949-registrazione-profondita-v1'
    cross={r['index']:r for r in read(depth/'riscontro.json',plan['crossDepthPin'])['rows']}
    roles={role:(name,seconds,digest) for role,name,seconds,digest in
           read(depth/'protocollo.json',plan['crossDepthProtocolPin'])['roles']}
    geo={}
    for key,name in [('primary','BKL046-GO14949-guida-fullwell-primary-v1'),
                     ('repeat','BKL046-GO14949-guida-fullwell-replica-v1')]:
        rows=read(BASE/name/'riscontro.json',plan['geometryReceipts'][key])['rows']
        geo[key]={r['index']:r for r in rows if r['dqScreen']=='PURE_FULL_WELL'}
        assert sorted(geo[key])==plan['indices']
        assert all(r['chip']==2 and not r['geometricPrescreenOnly'] for r in geo[key].values())
    measures=[]
    with ExitStack() as stack:
        pam_path=BASE/'BKL046-ACS-GitHub-MAST-d6df7a4fbfeb/wfc2_newpam.fits'
        assert pin(pam_path)==plan['pamPin']
        pam=stack.enter_context(fits.open(pam_path,mode='readonly',memmap=True))[0].data
        images={}
        for role in ('A40','B40','C150','D150'):
            name,t,expected=roles[role]
            folder=BASE/'BKL046-GO14949-quadrupoli-v1' if t==40 else depth
            images[role]=(image(stack,folder/name,expected,t),t)
        for key,folder,name in [
            ('primary','BKL046-GO14949-guida-fullwell-v1','jdg301bwq_flc.fits'),
            ('repeat','BKL046-GO14949-guida-fullwell-replica-v1','jdg301byq_flc.fits')]:
            images[key]=(image(stack,BASE/folder/name,plan['longPins'][key],400),400)
        assert all(im.shape==dq.shape==pam.shape for (im,dq),_ in images.values())
        for k in plan['indices']:
            for radius in plan['radiiPx']:
                rates={}
                for role,(arrays,seconds) in images.items():
                    long=role in geo
                    center=geo[role][k]['affinePredictedCenter'] if long else cross[k]['measured'][role]
                    assert center is not None
                    rates[role]=observe(arrays,pam,center,radius,seconds,long,plan)
                measures.append(dict(index=k,radiusPx=radius,rates=rates,geometricPrescreenPassed=False))
    result=dict(protocol='BKL046_GO14949_PURE_FULLWELL_APERTURE_RESULT_V1',
                designSha256=sha256(raw).hexdigest(),measures=measures,sciencePixelsReplaced=False,
                validatedSaturatedFluxRecovery=False,nativeExecutions=0,scientificClosures=0)
    with out.open('xb') as sink:
        sink.write(json.dumps(result,indent=2,sort_keys=True,allow_nan=False).encode()+b'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))