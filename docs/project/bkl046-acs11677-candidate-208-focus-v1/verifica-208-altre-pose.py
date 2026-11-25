
from collections import Counter
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
cross=Path(r'O:\BKL046-ACS11677-epsf-cross-visit-30s-v1')
loc=cross/'riscontro-proiezione-picco-dominante-208.json'
anchor=read(loc)
if not anchor['roundedBackprojectionHitsComponent'] or anchor['targetMomentStatus']!='MODEL_EXCEEDS_RESIDUAL_LIMIT':
    raise ValueError('Unexpected exploratory position status')
ref=np.asarray(anchor['sourceBackprojection'])
root=Path('O:/')
cohort=root/'BKL046-ACS-11677-scie-DQ-v1'
doc=read(cohort/'riscontro.json')
plan_path=cohort/'protocollo.json'
if sha(plan_path)!=doc['designSha256'] or sha(cohort/'riscontro.json')!='c7ab445f872054b6c4261c1250a733443c8b0d2316a8f0126e102f976235e43d':
    raise ValueError('Frozen cohort or screen changed')
plan=read(plan_path)
screen=runpy.run_path(str(cohort/'verifica.py'))['screen']
sys.argv[:]=[sys.argv[0],'jbbf01i1q']
wcs=runpy.run_path(str(root/'BKL046-ACS11677-riferimento-esterno-v1'/'verifica-candidato-frame-v2.py'))
primary=root/'BKL046-ACS11677-drizzle-ingressi-v1'/'flc'/'jb6v01e0q_flc.fits'
if sha(primary)!='e6011691a50b2608a3cb91e5f9ceb0957aa4a17e46aa04f8e00bee30df5fdd4d':
    raise ValueError('Saturated exposure changed')
results=[]
old_source=np.asarray(doc['cases'][207]['centerXY'])
with fits.open(primary,memmap=True) as a:
    iw=wcs['inputs'](a)[1]['wcs']
    for target_dir in ('BKL046-ACS11677-epsf-fresh-v1','BKL046-ACS11677-epsf-repeat-40s-v1'):
        folder=root/target_dir
        pin=folder/'riscontro-epsf.json'
        geo=read(pin)
        d=geo['chipPairs']['1->2']
        if not d['methods']['standardEPSF']['meetsFrozenGeometry'] or geo['independentFluxMeasured']:
            raise ValueError('No accepted geometry for 40-second comparison')
        rows=d['pairs']
        xy=np.asarray([p['sourceMoment'] for p in rows])
        train=np.asarray([sum(p['tile'])%2==0 for p in rows])
        design=np.column_stack((np.ones(len(xy)),xy/np.array([4096.,2048.])-.5))
        shifts=np.asarray([p['targetPsf'] for p in rows])-np.asarray([p['predictPsf'] for p in rows])
        coef,_,rank,_=np.linalg.lstsq(design[train],shifts[train],rcond=None)
        err=float(np.quantile(np.linalg.norm((shifts-design@coef)[~train],axis=1),.9))
        if rank!=3 or abs(err-d['methods']['standardEPSF']['models']['affine']['p90Px'])>1e-12:
            raise ValueError('Could not reproduce held-out geometry')
        f=folder/(geo['target']+'_flc.fits')
        if sha(f)!=geo['targetSha256']:
            raise ValueError('Exposure differs from geometry evidence')
        with fits.open(f,memmap=True) as h:
            frame=wcs['inputs'](h)[2]
            recs={}
            for key,pos in (('frozenCenter',old_source),('exploratoryBrightPeak',ref)):
                target=wcs['project'](iw,frame['wcs'],pos[None,:])[0]+np.r_[1.,pos/np.array([4096.,2048.])-.5]@coef
                if not (20<=target[0]<4076 and 20<=target[1]<2028):
                    recs[key]=dict(state='OUTSIDE_PINNED_CHIP',predictedXY=target.tolist())
                else:
                    recs[key]=screen(frame['data'],frame['dq'],target,plan)
            results.append(dict(target=geo['target'],geometrySha256=sha(pin),fitsSha256=geo['targetSha256'],locations=recs))
record=dict(method='BKL046_ACS11677_SOURCE208_CROSS_VISIT_LOCALIZATION_V1',
            sourceId=208,sourcePositionSha256=sha(loc),temperatureModelPassed=False,
            crossVisitScreen=results,stellarFluxMeasured=False,qualificationChanged=False,scientificClosure=False)
with (b/'riscontro-208-altre-pose.json').open('x',encoding='utf-8',newline='\n') as f:
    json.dump(record,f,indent=2,allow_nan=False)
    f.write('\n')
for row in results:
    print(row['target'],{k:(v['state'],v.get('peakShiftPx'),v.get('peakAboveBackground'),v.get('apertureNonzeroDQ'),
        v.get('apertureFullWell'),v.get('peakXY')) for k,v in row['locations'].items()})
