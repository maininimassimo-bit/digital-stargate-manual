
from hashlib import file_digest
from pathlib import Path
import json,runpy,sys
b=Path(__file__).resolve().parent
sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
from astropy.io import fits
import numpy as np

def sha(p):
    with p.open('rb') as f:return file_digest(f,'sha256').hexdigest()
def read(p):return json.loads(p.read_bytes())
def pin(p,v):
    if sha(p)!=v:raise ValueError('Unexpected input hash: '+p.name)
    return p

id=sys.argv[1]
if id not in ('j8hw23ggq','jd1y02pgq'):raise ValueError('Unknown shifted trial')
root=Path('O:/')
selection=read(b/'selezione-regioni.json')
cross=root/'BKL046-ACS11677-epsf-cross-visit-30s-v1'
origin=read(pin(cross/'riscontro-proiezione-picco-dominante-208.json',selection['pinnedSourceLocationSha256']))
geo_path=b/f'riscontro-epsf-{id}.json'
geo=read(geo_path)
recipe=read(pin(b/f'protocollo-epsf-{id}.json',geo['protocolSha256']))
if recipe['selectionSha256']!=sha(b/'selezione-regioni.json') or geo['target']!=id:
    raise ValueError('Trial selection lineage changed')
old=root/'BKL046-ACS-11677-scie-DQ-v1'
cases=read(pin(old/'riscontro.json','c7ab445f872054b6c4261c1250a733443c8b0d2316a8f0126e102f976235e43d'))
criteria=read(pin(old/'protocollo.json',cases['designSha256']))
screen=runpy.run_path(str(old/'verifica.py'))['screen']
sys.argv[:]=[sys.argv[0],'jbbf01i1q']
projection=runpy.run_path(str(root/'BKL046-ACS11677-riferimento-esterno-v1'/'verifica-candidato-frame-v2.py'))
a=root/'BKL046-ACS11677-drizzle-ingressi-v1'/'flc'/'jb6v01e0q_flc.fits'
f=b/(id+'_flc.fits')
pin(a,geo['sourceSha256'])
pin(f,geo['targetSha256'])
pair=geo['chipPairs']['1->2']
model=pair['methods']['standardEPSF']
p90=model['models'].get('affine',{}).get('p90Px')
results={}
with fits.open(a,memmap=True) as g,fits.open(f,memmap=True) as h:
    fr=projection['inputs'](g)[1]
    dst=projection['inputs'](h)[2]
    coef=np.zeros((3,2))
    if p90 is not None:
        rows=pair['pairs']
        xy=np.asarray([x['sourceMoment'] for x in rows])
        train=np.asarray([sum(x['tile'])%2==0 for x in rows])
        design=np.column_stack((np.ones(len(xy)),xy/np.array([4096.,2048.])-.5))
        res=np.asarray([x['targetPsf'] for x in rows])-np.asarray([x['predictPsf'] for x in rows])
        coef,_,rank,_=np.linalg.lstsq(design[train],res[train],rcond=None)
        measured=float(np.quantile(np.linalg.norm((res-design@coef)[~train],axis=1),.9))
        if rank!=3 or abs(measured-p90)>1e-12:raise ValueError('Heldout geometry differs')
    for key,pos in (('frozenCenter',cases['cases'][207]['centerXY']),('exploratoryBrightPeak',origin['sourceBackprojection'])):
        xy=np.asarray(pos)
        forecast=projection['project'](fr['wcs'],dst['wcs'],xy[None,:])[0]+np.r_[1.,xy/np.array([4096.,2048.])-.5]@coef
        results[key]=screen(dst['data'],dst['dq'],forecast,criteria)
report=dict(protocol='BKL046_ACS11677_208_SHIFTED_DETECTOR_DIAGNOSTIC_V1',trial=id,
        reportSha256=sha(geo_path),sourcePositionSha256=selection['pinnedSourceLocationSha256'],
        predictedLocationsUseAffineInDiagnostic=p90 is not None,geometryPassed=model['meetsFrozenGeometry'],
        heldOutAffineP90Px=p90,targetSha256=geo['targetSha256'],screen=results,
        candidateQualified=bool(model['meetsFrozenGeometry'] and results['exploratoryBrightPeak']['state']=='CANDIDATE_UNSATURATED_REFERENCE'),
        stellarFluxMeasured=False,scientificClosure=False)
with (b/f'riscontro-208-{id}.json').open('x',encoding='utf-8',newline='\n') as out:
    json.dump(report,out,indent=2,allow_nan=False)
    out.write('\n')
print({k:(v['state'],v.get('apertureDqCounts'),v.get('peakAboveBackground'),v.get('peakShiftPx')) for k,v in results.items()})
print(report['geometryPassed'],p90,report['candidateQualified'])
