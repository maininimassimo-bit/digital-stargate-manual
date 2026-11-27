"""Compare ACS photometric rates on the archived held-out stellar associations."""
from contextlib import ExitStack
from hashlib import file_digest, sha256
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
BASE=Path('O:/')
DEPTH=BASE/'BKL046-GO14949-registrazione-profondita-v1'
GEOMETRY=BASE/'BKL046-GO14949-guida-fullwell-primary-v1'
sys.path.insert(0,str(BASE/'BKL046-ACS-WFC-runtime-7.2.0'))
import numpy as np
from astropy.io import fits


def ensure(valid, why):
    if not valid:
        raise ValueError(why)


def read_json(path, pin):
    raw=path.read_bytes()
    ensure(sha256(raw).hexdigest()==pin,path.name)
    return json.loads(raw)


def open_pinned(stack, path, expected):
    with path.open('rb') as stream:
        ensure(file_digest(stream,'sha256').hexdigest()==expected,path.name)
    return stack.enter_context(fits.open(path,mode='readonly',memmap=True))


def aperture(image, dq, pam, center, seconds, radius):
    x,y=center
    i,j=int(round(x)),int(round(y))
    if i<13 or j<13 or j+13>=image.shape[0] or i+13>=image.shape[1]:
        return 'EDGE',None
    area=np.s_[j-13:j+14,i-13:i+14]
    yy,xx=np.mgrid[j-13:j+14,i-13:i+14]
    weights=np.zeros(xx.shape)
    offsets=(np.arange(8)+.5)/8-.5
    for v in offsets:
        for u in offsets:
            weights+=((xx+u-x)**2+(yy+v-y)**2)<=radius**2
    weights/=64
    source=weights>0
    r2=(xx-x)**2+(yy-y)**2
    annulus=(r2>=8**2)&(r2<=12**2)
    pixels=image[area]
    quality=dq[area]
    if np.any(quality[source]!=0) or not np.isfinite(pixels[source]).all():
        return 'APERTURE_DQ_OR_NONFINITE',None
    usable=annulus&(quality==0)&np.isfinite(pixels)
    if np.count_nonzero(usable)<120:
        return 'BACKGROUND_SUPPORT',None
    background=np.median(pixels[usable])
    rates=[np.sum(weights[source]*(pixels[source]-background)*m)/seconds for m in (1,pam[area][source])]
    if not all(np.isfinite(v) and v>0 for v in rates):
        return 'NONPOSITIVE',None
    return 'MEASURED',dict(raw=float(rates[0]),pam=float(rates[1]))


def main(out):
    design=(ROOT/'protocollo.json').read_bytes()
    plan=json.loads(design)
    depth=read_json(DEPTH/'riscontro.json',plan['crossDepthSha256'])
    geo=read_json(GEOMETRY/'riscontro.json',plan['geometrySha256'])
    paths=read_json(DEPTH/'protocollo.json',plan['crossDepthProtocolSha256'])
    long=read_json(GEOMETRY/'protocollo.json',plan['geometryProtocolSha256'])['long']
    g={r['index']:r for r in geo['rows']}
    eligible=[r for r in depth['rows'] if r['heldout'] and r['commonValid']]
    ensure(len(eligible)==105 and len(g)==677,'Cohort')
    report=[]
    with ExitStack() as stack:
        images={}
        for role,name,seconds,expected in paths['roles']:
            parent=BASE/'BKL046-GO14949-quadrupoli-v1' if seconds==40 else DEPTH
            images[role]=(open_pinned(stack,parent/name,expected),seconds)
        images['L400']=(open_pinned(stack,BASE/'BKL046-GO14949-guida-fullwell-v1'/long['name'],long['sha256']),400)
        maps={int(chip):open_pinned(stack,BASE/'BKL046-ACS-GitHub-MAST-d6df7a4fbfeb'/f'wfc{chip}_newpam.fits',pin)[0].data
              for chip,pin in plan['pamSha256'].items()}
        for row in eligible:
            k=row['index']
            geometry=g[k]
            chip=row['chip']
            ensure(chip==geometry['chip'],'Chip')
            centers=dict(row['measured'],L400=geometry['affinePredictedCenter'])
            ext=1 if chip==2 else 2
            for radius in plan['apertureRadii']:
                states={}
                rates={}
                for role,(hdus,seconds) in images.items():
                    h=hdus['SCI',ext]
                    q=hdus['DQ',ext].data
                    ensure(h.header['CCDCHIP']==chip and float(hdus[0].header['EXPTIME'])==seconds,'FITS metadata')
                    ensure(h.header['BUNIT'].strip().upper()=='ELECTRONS' and
                           all(float(h.header[tag])==0 for tag in ('LTV1','LTV2')) and
                           maps[chip].shape==h.data.shape==q.shape,'Photometry grid and units')
                    if centers[role] is None:
                        states[role]='NO_PRIOR_CENTER'
                        continue
                    states[role],rate=aperture(h.data,q,maps[chip],centers[role],seconds,radius)
                    if rate is not None:
                        rates[role]=rate
                report.append(dict(index=k,chip=chip,radius=radius,longDQ=geometry['dqScreen'],
                                   tile=row['archivedTile'],states=states,rates=rates,
                                   geometricPrescreenPassed=geometry['geometricPrescreenOnly']))
    result=dict(protocol='BKL046_GO14949_APERTURE_CROSS_DEPTH_DIAGNOSTIC_V1',
                designSha256=sha256(design).hexdigest(),sources=len(eligible),measurements=report,
                syntheticSaturationRecoveryApplied=False,scientificClosures=0,nativeExecutions=0)
    with out.open('xb') as sink:
        sink.write(json.dumps(result,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))