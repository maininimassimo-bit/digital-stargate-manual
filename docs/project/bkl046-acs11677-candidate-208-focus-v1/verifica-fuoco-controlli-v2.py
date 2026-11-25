
from hashlib import file_digest
from pathlib import Path
import json
import runpy
import sys

root=Path(__file__).resolve().parent
sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
import numpy as np
from astropy.io import fits

def sha(p):
    with p.open('rb') as f:return file_digest(f,'sha256').hexdigest()
def pin(p,s):
    if sha(p)!=s:raise ValueError('Input hash changed: '+p.name)
    return p
def read(p):return json.loads(p.read_bytes())

def score(sci,err,xy,centroid,model,sample,limit):
    w=1/err
    background=np.column_stack((np.ones(len(xy)),xy-centroid))*w[:,None]
    q,_=np.linalg.qr(background,mode='reduced')
    v=sci*w
    residual=v-q@(q.T@v)
    energy=float(residual@residual)
    best=centroid.copy()
    minimum=float('inf')
    for step,count in ((.2,4),(.04,4),(.005,5)):
        ax=np.arange(-count,count+1)*step
        x,y=np.meshgrid(ax,ax)
        loc=best+np.column_stack((x.ravel(),y.ravel()))
        loc=loc[np.linalg.norm(loc-centroid,axis=1)<=limit]
        values=sample(np,model,xy[:,0,None]-loc[:,0],xy[:,1,None]-loc[:,1])*w[:,None]
        projected=values-q@(q.T@values)
        den=np.sum(projected*projected,axis=0)
        numerator=projected.T@residual
        errors=np.where((den>0)&(numerator>0),energy-numerator**2/den,np.inf)
        index=np.argmin(errors)
        if errors[index]<minimum:
            best=loc[index]
            minimum=float(errors[index])
    return minimum/(len(sci)-6)

def main():
    expected='8885229a54f94224e65089500b158d134582456eec2aa8b5aaae8234e90090da'
    plan=read(pin(root/'protocollo-fuoco-v2.json',expected))
    origin=Path(r'O:\BKL046-ACS11677-epsf-cross-visit-30s-v1')
    geom=read(pin(origin/'riscontro-epsf.json',plan['geometrySha256']))
    context=read(pin(origin/'contesto-picco-208.json',plan['candidateContextSha256']))
    star=np.asarray(context['windowMaxima'][1]['peakDetectorXY'])
    stock=Path(r'U:\coordinatore-r4-bkl046\DSG-Shared-BKL046-GO14949-ePSF-6f208aaeadf3')
    psf=runpy.run_path(str(pin(stock/'compare_epsf.py',plan['psfSourceSha256'])))
    reference=fits.getdata(pin(stock/'STDPSF_ACSWFC_F606W_SM4.fits',plan['standardModelSha256']))
    header=read(pin(root/'libreria-testata.json',plan['focusPrimaryHeaderReceiptSha256']))
    archive=read(root/'acquisizione-libreria.json')
    if archive['etag']!=header['etag']:raise ValueError('Focus library changed from the inspectable header')
    library=pin(root/'STDPBF_ACSWFC_F606W_SM4.fits',archive['sha256'])
    science=pin(origin/'jbbf01i3q_flc.fits',plan['flcSha256'])
    records=[]
    reasons={}
    with fits.open(library,memmap=True) as model,fits.open(science,mode='readonly',memmap=True) as target:
        with library.open('rb') as stream:
            from hashlib import sha256
            if sha256(stream.read(header['headerBytes'])).hexdigest()!=header['headerPrefixSha256']:
                raise ValueError('Library FITS header does not match the bounded acquisition')
        cubes=model[0].data
        cards=model[0].header
        xs=np.asarray([cards[f'IPSFX{i:02d}'] for i in range(1,10)])
        ys=np.asarray([cards[f'JPSFY{i:02d}'] for i in range(1,6)])
        if plan['physicalChip']!=2 or list(ys)!=[0,512,1024,1536,2049]:
            raise ValueError('Unexpected target chip focus grid')
        def interpolate(cube,xy):
            x,y=xy+1
            i=int(np.clip(np.searchsorted(xs,x)-1,0,7))
            j=int(np.clip(np.searchsorted(ys,y)-1,0,3))
            u=(x-xs[i])/(xs[i+1]-xs[i])
            v=(y-ys[j])/(ys[j+1]-ys[j])
            k=9*j+i
            return (1-v)*((1-u)*cube[k]+u*cube[k+1])+v*((1-u)*cube[k+9]+u*cube[k+10])
        if len(cubes.shape)!=4 or cubes.shape[1:]!=reference.shape:
            raise ValueError('Focus planes differ from archived standard shape')
        ext=plan['scienceExtension']
        if target['SCI',ext].header['CCDCHIP']!=plan['physicalChip']:
            raise ValueError('Physical chip binding changed')
        sci,err,dq=(target[k,ext].data for k in ('SCI','ERR','DQ'))
        dy,dx=np.mgrid[-3:4,-3:4]
        core=dx*dx+dy*dy<=plan['stampRadiusPx']**2
        for row in geom['chipPairs']['1->2']['pairs']:
            spot=np.asarray(row['targetMoment'])
            if np.linalg.norm(spot-star)<=plan['excludedCandidateRadiusPx']:
                reasons['candidateNeighborhood']=reasons.get('candidateNeighborhood',0)+1
                continue
            x,y=np.rint(spot).astype(int)
            box=(slice(y-3,y+4),slice(x-3,x+4))
            pixels=sci[box][core].astype(float)
            errors=err[box][core].astype(float)
            if np.any(dq[box][core]) or not np.isfinite(pixels).all() or not np.isfinite(errors).all() or np.any(errors<=0):
                reasons['quality']=reasons.get('quality',0)+1
                continue
            xy=np.column_stack(((x+dx)[core],(y+dy)[core]))
            def metric(cube,focus):
                patch=interpolate(cube,spot) if focus else psf['psf_at'](np,cube,spot,plan['physicalChip'])
                return score(pixels,errors,xy,spot,patch,psf['sample'],plan['fitShiftLimitPx'])
            values=[metric(c,True) for c in cubes]
            baseline=metric(reference,False)
            if not np.isfinite(values+[baseline]).all():
                reasons['incompleteAcrossModels']=reasons.get('incompleteAcrossModels',0)+1
                continue
            records.append(dict(targetMoment=spot.tolist(),sourceTile=row['tile'],distanceFromCandidatePx=float(np.linalg.norm(spot-star)),
                                standard=baseline, focusPlanes=values))
        labels={k:model[0].header[k] for k in model[0].header if k.startswith(('FOC','KPSF','NF'))}
    train=[r for r in records if sum(r['sourceTile'])%2==0]
    held=[r for r in records if sum(r['sourceTile'])%2==1]
    footprint=lambda rows:len({tuple(r['sourceTile']) for r in rows})
    enough=(min(len(train),len(held))>=plan['minStarsPerPartition'] and
            min(footprint(train),footprint(held))>=plan['minTilesPerPartition'])
    result=dict(protocolSha256=expected,librarySha256=archive['sha256'],flcSha256=plan['flcSha256'],
                controlStarsFit=len(train),controlStarsHeldOut=len(held),fitTiles=footprint(train),heldOutTiles=footprint(held),
                libraryFocusHeader=labels,discards=reasons,controlRows=records,scientificClosure=False,stellarFluxMeasured=False)
    if enough:
        f=np.median([r['focusPlanes'] for r in train],axis=0)
        i=int(np.argmin(f))
        v=np.median([r['focusPlanes'] for r in held],axis=0)
        train0=float(np.median([r['standard'] for r in train]))
        held0=float(np.median([r['standard'] for r in held]))
        result.update(selectedPlaneIndexZeroBased=i,fitMedianByPlane=f.tolist(),fitMedianStandard=train0,
            selectedPlaneHeldOutMedian=float(v[i]),standardHeldOutMedian=held0,
            heldOutImproved=bool(v[i]<held0),candidateEvaluated=False)
    else:
        result.update(heldOutImproved=False,candidateEvaluated=False)
    path=root/'riscontro-fuoco-controlli-v2.json'
    with path.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(result,f,indent=2,allow_nan=False)
        f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('controlRows','libraryFocusHeader')}),flush=True)

if __name__=='__main__':
    main()
