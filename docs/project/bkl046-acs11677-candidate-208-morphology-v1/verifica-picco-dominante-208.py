
from hashlib import file_digest
from pathlib import Path
import json
import runpy
import sys

base=Path(__file__).resolve().parent
sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
import numpy as np
from astropy.io import fits

def sha(p):
    with p.open('rb') as f:return file_digest(f,'sha256').hexdigest()
def read(p):return json.loads(p.read_bytes())

def solve(xy, values, sigma, origin, model, sample, plan):
    weights=1/sigma
    xy0=xy-origin
    background=np.column_stack((np.ones(len(xy)),xy0))*weights[:,None]
    q,_=np.linalg.qr(background,mode='reduced')
    v=values*weights
    detrended=v-q@(q.T@v)
    v2=float(detrended@detrended)
    radius=plan['centerSearchRadiusPx']
    step=plan['coarseStepPx']
    axis=np.arange(-radius,radius+step/2,step)
    x,y=np.meshgrid(axis,axis)
    offsets=np.column_stack((x.ravel(),y.ravel()))
    positions=origin+offsets[np.linalg.norm(offsets,axis=1)<=radius]
    template=sample(np,model,xy[:,0,None]-positions[:,0],xy[:,1,None]-positions[:,1])*weights[:,None]
    residual_template=template-q@(q.T@template)
    gram=residual_template.T@residual_template
    diagonals=np.diag(gram)
    dot=residual_template.T@detrended
    choices=np.where(dot>0,v2-dot**2/diagonals,np.inf)
    initial=np.array([positions[np.argmin(choices)]])
    separation=np.linalg.norm(positions[:,None,:]-positions[None,:,:],axis=2)
    det=diagonals[:,None]*diagonals[None,:]-gram**2
    with np.errstate(divide='ignore',invalid='ignore'):
        amp_a=(dot[:,None]*diagonals[None,:]-dot[None,:]*gram)/det
        amp_b=(dot[None,:]*diagonals[:,None]-dot[:,None]*gram)/det
        two=np.where((separation>=plan['pairSeparationMinPx'])&(det>0)&(amp_a>0)&(amp_b>0),
                     v2-amp_a*dot[:,None]-amp_b*dot[None,:],np.inf)
    p,q0=np.unravel_index(np.argmin(two),two.shape)
    if not np.isfinite(two[p,q0]):raise ValueError('No positive separated two-component model')
    initial_two=positions[[p,q0]].copy()

    def evaluate(points):
        if np.any(np.linalg.norm(points-origin,axis=1)>radius):
            return np.inf,None,None
        if len(points)==2 and np.linalg.norm(points[1]-points[0])<plan['pairSeparationMinPx']:
            return np.inf,None,None
        fitted=sample(np,model,xy[:,0,None]-points[:,0],xy[:,1,None]-points[:,1])*weights[:,None]
        design=np.column_stack((background,fitted))
        coef,_,rank,_=np.linalg.lstsq(design,v,rcond=None)
        if rank!=design.shape[1] or np.any(coef[3:]<=0):
            return np.inf,None,None
        error=v-design@coef
        return float(error@error),coef,design

    def finish(points):
        points=points.copy()
        best,_,_=evaluate(points)
        for step in plan['refinementStepsPx']:
            d=np.arange(-3,4)*step
            for _ in range(2):
                for i in range(len(points)):
                    chosen=points[i].copy()
                    for x in d:
                        for y in d:
                            trial=points.copy()
                            trial[i]=points[i]+[x,y]
                            score,_,_=evaluate(trial)
                            if score<best:
                                best=score
                                chosen=trial[i]
                    points[i]=chosen
        score,coef,design=evaluate(points)
        error=np.sqrt(np.diag(np.linalg.inv(design.T@design)))[3:]
        pars=3+3*len(points)
        return dict(positionsPx=points.tolist(),conditionalAmplitudeSnr=(coef[3:]/error).tolist(),
                    chiSquare=score,reducedChiSquare=score/(len(xy)-pars),bic=score+pars*np.log(len(xy)))
    one=finish(initial)
    two_starts=[initial_two]
    anchor=np.asarray(one['positionsPx'][0])
    coarse_single_score=one['chiSquare']
    alternatives=[]
    for point in positions:
        pair=np.vstack((anchor,point))
        score,_,_=evaluate(pair)
        if np.isfinite(score):
            alternatives.append((score,pair))
    alternatives.sort(key=lambda x:x[0])
    two_starts.extend(pair for _,pair in alternatives[:8])
    results=[finish(pair) for pair in two_starts]
    two=min(results,key=lambda candidate:candidate['chiSquare'])
    if two['chiSquare']>coarse_single_score:
        k=9
        return one,dict(positionsPx=one['positionsPx'],conditionalAmplitudeSnr=one['conditionalAmplitudeSnr']+[0.0],
                        chiSquare=one['chiSquare'],reducedChiSquare=one['chiSquare']/(len(xy)-k),
                        bic=one['chiSquare']+k*np.log(len(xy)),secondComponentAtZeroBoundary=True)
    two['secondComponentAtZeroBoundary']=False
    return one,two

plan_path=base/'protocollo-picco-dominante-208.json'
plan_pin='5ac74b9acc1290f0ad10fae74b39bfeddf96d2029fb20d0b4898315c2f10d310'
if sha(plan_path)!=plan_pin:raise ValueError('Blend protocol changed')
plan=read(plan_path)
inputs={'riscontro-identita-208.json':plan['diagnosisSha256'],'riscontro-epsf-dq.json':plan['screenSha256'],
        'jbbf01i3q_flc.fits':plan['targetSha256']}
for n,d in inputs.items():
    if sha(base/n)!=d:raise ValueError('Input changed: '+n)
psfdir=Path(r'U:\coordinatore-r4-bkl046\DSG-Shared-BKL046-GO14949-ePSF-6f208aaeadf3')
cube=psfdir/'STDPSF_ACSWFC_F606W_SM4.fits'
code=psfdir/'compare_epsf.py'
if sha(cube)!=plan['modelSha256'] or sha(code)!=plan['psfCodeSha256']:
    raise ValueError('PSF model changed')
helpers=runpy.run_path(str(code))
dq=read(base/'riscontro-epsf-dq.json')
case=next(r for r in dq['rows'] if r['sourceId']==208)
if sha(base/'contesto-picco-208.json')!=plan['contextSha256']:
    raise ValueError('Bright-peak diagnosis changed')
origin=np.asarray(plan['brightPeak'],dtype=float)
half=plan['halfStampPx']
ix,iy=np.rint(origin).astype(int)
yy,xx=np.mgrid[iy-half:iy+half+1,ix-half:ix+half+1]
box=(slice(iy-half,iy+half+1),slice(ix-half,ix+half+1))
ext=plan['targetExtension']
with fits.open(base/'jbbf01i3q_flc.fits',memmap=True) as f:
    science=f['SCI',ext]
    if science.header['CCDCHIP']!=plan['physicalChip'] or science.header['BUNIT'].strip()!='ELECTRONS':
        raise ValueError('Unexpected physical chip or unit')
    sci=science.data[box]
    flag=f['DQ',ext].data[box]
    err=f['ERR',ext].data[box]
    keep=np.isfinite(sci)&np.isfinite(err)&(err>0)&(flag==0)
    if int(keep.sum())<120:raise ValueError('Insufficient valid data in frozen window')
    image=helpers['psf_at'](np,fits.getdata(cube,memmap=False),origin,plan['physicalChip'])
    one,two=solve(np.column_stack((xx[keep],yy[keep])),sci[keep],err[keep],origin,image,helpers['sample'],plan)
change=one['bic']-two['bic']
plausible={n:v['reducedChiSquare']<=plan['maxReducedChiSquare'] and min(v['conditionalAmplitudeSnr'])>=plan['minComponentSnr']
           for n,v in (('one',one),('two',two))}
report=dict(solverRevision='Starts anchored at the refined single-component optimum, nonnegative two-component boundary included',protocolSha256=plan_pin,sourceId=208,centeredAt=origin.tolist(),pixelsUsed=int(keep.sum()),onePsf=one,twoPsf=two,
            deltaBicForTwo=change,plausibleByFrozenDiagnostic=plausible,
            twoPreferredByBic=bool(change>=plan['minDeltaBicForSecondPsf']),
            stellarFluxMeasured=False,qualifiedReference=False,scientificClosure=False)
with (base/'riscontro-picco-dominante-208.json').open('x',encoding='utf-8',newline='\n') as f:
    json.dump(report,f,indent=2,allow_nan=False)
    f.write('\n')
print(json.dumps(report),flush=True)
