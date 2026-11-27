
from hashlib import file_digest
from pathlib import Path
from collections import Counter
import json,runpy,sys

here=Path(__file__).resolve().parent
base=Path('O:/')
sys.path.insert(0,str(base/'BKL046-ACS-WFC-runtime-7.2.0'))
from astropy.io import fits
import numpy as np

def sha(p):
    with p.open('rb') as f:return file_digest(f,'sha256').hexdigest()
def read(p):return json.loads(p.read_bytes())
def require(b,msg):
    if not b:raise ValueError(msg)

geo=read(here/'riscontro-epsf.json')
dq=read(here/'riscontro-epsf-dq.json')
require(dq['geometryReportSha256']==sha(here/'riscontro-epsf.json') and dq['eligibleSourceIds']==[208],
        'Unexpected admitted source screening list')
candidate=next(r for r in dq['rows'] if r['sourceId']==208)
cohort=base/'BKL046-ACS-11677-scie-DQ-v1'
require(sha(cohort/'riscontro.json')=='c7ab445f872054b6c4261c1250a733443c8b0d2316a8f0126e102f976235e43d','Frozen cohort changed')
component=read(cohort/'riscontro.json')['cases'][207]
source=base/'BKL046-ACS11677-drizzle-ingressi-v1'/'flc'/'jb6v01e0q_flc.fits'
target=here/'jbbf01i3q_flc.fits'
require(sha(source)==geo['sourceSha256'] and sha(target)==geo['targetSha256'],'Geometry input FLC changed')
sys.argv[:]=[sys.argv[0],'jbbf01i1q']
helpers=runpy.run_path(str(base/'BKL046-ACS11677-riferimento-esterno-v1'/'verifica-candidato-frame-v2.py'))
evaluate=runpy.run_path(str(here/'verifica-epsf.py'))
components=runpy.run_path(str(cohort/'verifica.py'))['components']
gdir=base/'BKL046-ACS-11677-geometria-lunghe-v1'
models=runpy.run_path(str(gdir/'verifica.py'))
params=read(gdir/'protocollo.json')
centroid=models['load_fn'](base/'BKL046-GO14949-registrazione-profondita-v1'/'transfer.py',params['centroidSourceSha256'],'centroid')
cal=read(here/'protocollo-epsf.json')
require(sha(here/'protocollo-epsf.json')==geo['protocolSha256'] and sha(gdir/'protocollo.json')==cal['geometryProtocolSha256'],
        'Measurement method changed')
psfdir=Path(r'U:\coordinatore-r4-bkl046\DSG-Shared-BKL046-GO14949-ePSF-6f208aaeadf3')
psffile=psfdir/'STDPSF_ACSWFC_F606W_SM4.fits'
psfcode=psfdir/'compare_epsf.py'
require(sha(psffile)==cal['standardPsfSha256'] and sha(psfcode)==cal['psfFunctionsSha256'],'PSF model changed')
psf=runpy.run_path(str(psfcode))
cube=fits.getdata(psffile)
pairs=geo['chipPairs']['1->2']['pairs']
train=np.asarray([sum(r['tile'])%2==0 for r in pairs])
xy=np.asarray([r['sourceMoment'] for r in pairs])
design=np.column_stack((np.ones(len(xy)),xy/np.array([4096.,2048.])-.5))
residual=np.asarray([r['targetPsf'] for r in pairs])-np.asarray([r['predictPsf'] for r in pairs])
coeff,_,rank,_=np.linalg.lstsq(design[train],residual[train],rcond=None)
p90=float(np.quantile(np.linalg.norm((residual-design@coeff)[~train],axis=1),.9))
require(rank==3 and abs(p90-geo['chipPairs']['1->2']['methods']['standardEPSF']['models']['affine']['p90Px'])<1e-12,
        'Did not recover the inherited affine transform')
with fits.open(source,memmap=True) as a,fits.open(target,memmap=True) as b:
    src=helpers['inputs'](a)[1]
    dst=helpers['inputs'](b)[2]
    center=np.asarray(component['centerXY'])
    x,y=np.rint(center).astype(int)
    window=40
    flags=src['dq'][y-window:y+window+1,x-window:x+window+1]
    group_matches=[]
    for group in components((flags&256)!=0):
        ys,xs=group.T+np.array([[y-window],[x-window]])
        ys0,xs0=group.T
        vals=Counter(int(i) for i in flags[ys0,xs0])
        if ([float(np.median(xs)),float((min(ys)+max(ys))/2)]==component['centerXY'] and
            len(group)==component['fullWellPixels'] and int(max(ys)-min(ys)+1)==component['verticalSpan'] and
            vals==Counter({int(k):v for k,v in component['longDqCounts'].items()})):
            group_matches.append(np.column_stack((xs,ys)))
    require(len(group_matches)==1,'Frozen saturated component was not recovered uniquely')
    group=group_matches[0]
    peak=np.asarray(candidate['screen']['peakXY'],dtype=float)
    moment,error=centroid(np,dst['data'],dst['dq'],peak)
    refined=evaluate['profile'](dst,2,peak,moment,cube,psf) if error is None else None
    chosen=peak if refined is None else refined
    project=helpers['project']
    guess=project(dst['wcs'],src['wcs'],chosen[None,:])[0]
    for _ in range(8):
        delta=np.r_[1.,guess/np.array([4096.,2048.])-.5]@coeff
        guess=project(dst['wcs'],src['wcs'],(chosen-delta)[None,:])[0]
    roundtrip=project(src['wcs'],dst['wcs'],guess[None,:])[0]+np.r_[1.,guess/np.array([4096.,2048.])-.5]@coeff
    require(np.linalg.norm(roundtrip-chosen)<1e-6,'Reverse projection closure failed')
doc=dict(protocol='BKL046_ACS11677_SOURCE208_SPATIAL_ASSOCIATION_V1',sourceId=208,sourceComponent=center.tolist(),
    targetPeak=peak.tolist(),targetEPSFFit=None if refined is None else refined.tolist(),
    targetMomentStatus=error or 'OK',sourceBackprojection=guess.tolist(),sourceOffsetPx=(guess-center).tolist(),
    distanceToNearestComponentPixel=float(np.linalg.norm(group-guess,axis=1).min()),
    roundedBackprojectionHitsComponent=bool((group==np.rint(guess).astype(int)).all(axis=1).any()),
    sourceFullWellPixels=len(group),forwardReverseResidualPx=float(np.linalg.norm(roundtrip-chosen)),
    geometrySha256=sha(here/'riscontro-epsf.json'),qualificationSha256=sha(here/'riscontro-epsf-dq.json'),
    resultScope='Spatial consistency with the source full-well component. No flux or source deblending measured.',
    stellarFluxMeasured=False,scientificClosure=False)
with (here/'riscontro-identita-208.json').open('x',encoding='utf-8',newline='\n') as f:
 json.dump(doc,f,indent=2,allow_nan=False)
 f.write('\n')
print(json.dumps(doc))
