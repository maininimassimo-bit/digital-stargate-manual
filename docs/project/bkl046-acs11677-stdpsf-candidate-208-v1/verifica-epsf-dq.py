
from collections import Counter
from hashlib import file_digest
from pathlib import Path
import json,runpy,sys

p=Path(__file__).resolve().parent
o=Path('O:/')
sys.path.insert(0,str(o/'BKL046-ACS-WFC-runtime-7.2.0'))
from astropy.io import fits
import numpy as np
def sha(v):
 with v.open('rb') as f:return file_digest(f,'sha256').hexdigest()
def check(path,pin):
 if sha(path)!=pin:raise ValueError('Changed input '+path.name)
 return path
def read(f):return json.loads(f.read_bytes())
raw=check(p/'riscontro-epsf.json','9dbc517a3f6b5095e46adabc3e21c370b4e77faf3bbb0407bd2365c2b3e8216a')
r=read(raw)
recipe=read(check(p/'protocollo-epsf.json',r['protocolSha256']))
src=check(o/'BKL046-ACS11677-drizzle-ingressi-v1'/'flc'/'jb6v01e0q_flc.fits',r['sourceSha256'])
dst=check(p/(r['target']+'_flc.fits'),r['targetSha256'])
cdir=o/'BKL046-ACS-11677-scie-DQ-v1'
cohort=read(check(cdir/'riscontro.json','c7ab445f872054b6c4261c1250a733443c8b0d2316a8f0126e102f976235e43d'))
design=read(check(cdir/'protocollo.json',cohort['designSha256']))
screen=runpy.run_path(str(cdir/'verifica.py'))['screen']
sys.argv[:]=[sys.argv[0],'jbbf01i1q']
tool=runpy.run_path(str(check(o/'BKL046-ACS11677-riferimento-esterno-v1'/'verifica-candidato-frame-v2.py',
 '2f72a51e7a9a28c44a81f41d9fb8bff2d62ffb495a7fe513ffb1a79637b1a98a')))
models={}
for k,v in r['chipPairs'].items():
 d=v.get('methods',{}).get('standardEPSF',{})
 if not d.get('meetsFrozenGeometry'):continue
 rows=v['pairs']
 xy=np.asarray([x['sourceMoment'] for x in rows])
 train=np.asarray([sum(x['tile'])%2==0 for x in rows])
 data=np.column_stack((np.ones(len(xy)),xy/np.array([4096.,2048.])-.5))
 residual=np.asarray([x['targetPsf'] for x in rows])-np.asarray([x['predictPsf'] for x in rows])
 coeff,_,rank,_=np.linalg.lstsq(data[train],residual[train],rcond=None)
 p90=float(np.quantile(np.linalg.norm((residual-data@coeff)[~train],axis=1),.9))
 if rank!=3 or abs(p90-d['models']['affine']['p90Px'])>1e-12 or p90>recipe['qualification']['heldoutRadialP90Px']:
    raise ValueError('Reconstructed geometry does not match the held-out receipt')
 models[k]=coeff
rows=[]
with fits.open(src,memmap=True) as a,fits.open(dst,memmap=True) as b:
 source,target=(tool['inputs'](h) for h in (a,b))
 for k,c in enumerate(cohort['cases'],1):
    i=c['chip']
    xy=np.asarray(c['centerXY'])
    positions={j:tool['project'](source[i]['wcs'],t['wcs'],xy[None,:])[0] for j,t in target.items()}
    within=[j for j,(x,y) in positions.items() if 20<=x<4076 and 20<=y<2028]
    rec=dict(sourceId=k,sourceChip=i,footprint=within)
    if len(within)!=1:
        rows.append(dict(rec,state='NO_UNIQUE_FOOTPRINT'))
        continue
    j=within[0]
    m=models.get(f'{i}->{j}')
    if m is None:
        rows.append(dict(rec,state='NO_QUALIFIED_GEOMETRY'))
        continue
    point=positions[j]+np.r_[1.,xy/np.array([4096.,2048.])-.5]@m
    quality=screen(target[j]['data'],target[j]['dq'],point,design)
    rows.append(dict(rec,state=quality['state'],targetChip=j,screen=quality))
if len(rows)!=340:raise ValueError('Frozen cohort changed')
note=dict(method='BKL046_ACS11677_FRESH_STDPSF_DQ_V1',geometryReportSha256=sha(raw),target=r['target'],
           targetSha256=r['targetSha256'],screenPlanSha256=cohort['designSha256'],
           acceptedGeometry=sorted(models),states=dict(Counter(v['state'] for v in rows)),
           eligibleSourceIds=[v['sourceId'] for v in rows if v['state']=='CANDIDATE_UNSATURATED_REFERENCE'],
           fluxMeasured=False,scientificClosure=False,rows=rows)
with (p/'riscontro-epsf-dq.json').open('x',encoding='utf-8',newline='\n') as f:
 json.dump(note,f,indent=2,allow_nan=False)
 f.write('\n')
print(note['states'],note['eligibleSourceIds'])
