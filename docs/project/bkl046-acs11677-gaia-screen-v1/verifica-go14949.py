
from collections import Counter
from hashlib import file_digest
from pathlib import Path
import json
import runpy
import sys

root=Path(__file__).resolve().parent
base=Path('O:/')
sys.path.insert(0,str(base/'BKL046-ACS-WFC-runtime-7.2.0'))
from astropy.io import fits
import numpy as np

def sha(path):
    with path.open('rb') as f:
        return file_digest(f,'sha256').hexdigest()
def pin(path,expected):
    if sha(path)!=expected:
        raise ValueError('Frozen input changed: '+path.name)
    return path
def read(p):
    return json.loads(p.read_bytes())
def write(name,data):
    with (root/name).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(data,f,sort_keys=True,indent=2,allow_nan=False)
        f.write('\n')
def inside(xy,m):
    return bool(np.isfinite(xy).all() and (m<=xy[0]<4096-m) and (m<=xy[1]<2048-m))

def evaluate(target, identity, exposure, cohort, geometry, old, helpers, source, source_anchors, screen):
    target_pin=identity['sha256']
    extension_map={1:2,2:1}
    blocks={}
    with fits.open(pin(exposure,target_pin),mode='readonly',memmap=True) as f:
        h=f[0].header
        if h['ROOTNAME'].lower()!=target or h['PROPOSID']!=14949 or h['EXPTIME']!=40. or not all(
                f['SCI',ext].header['WCSNAME']==identity['wcs'] and f['SCI',ext].header['RADESYS']=='ICRS'
                for ext in extension_map):
            raise ValueError('Detector/FITS identity differs from matched archival product')
        destination=helpers['inputs'](f)
        models={}
        for i in (1,2):
            for j in (1,2):
                key=f'{i}->{j}'
                blocks[key],models[key]=helpers['fit_pair'](source[i],destination[j],source_anchors[i],
                     old['centroid'],old['fit'],geometry)
        cases=[]
        for number,case in enumerate(cohort,1):
            chip=case['chip']
            spot=np.asarray([case['centerXY']])
            converted={j:helpers['project'](source[chip]['wcs'],destination[j]['wcs'],spot)[0] for j in (1,2)}
            covered=[j for j,xy in converted.items() if inside(xy,identity['margin'])]
            record=dict(sourceId=number,sourceChip=chip,footprint=covered)
            if len(covered)!=1:
                cases.append(dict(record,result='no_unique_footprint',candidate=False))
                continue
            j=covered[0]
            model=models[f'{chip}->{j}']
            xy=converted[j]
            if model is not None:
                xy=xy+np.r_[1.,spot[0]/np.array([4096.,2048.])-.5]@model
            measured=screen(destination[j]['data'],destination[j]['dq'],xy,old['screenPlan'])
            cases.append(dict(record,targetChip=j,predictedCenter=xy.tolist(),screen=measured,result=measured['state'],
                              geometryPassed=model is not None,
                              candidate=model is not None and measured['state']=='CANDIDATE_UNSATURATED_REFERENCE'))
    result=dict(planSha256=identity['planSha256'],root=target,wcs=identity['wcs'],fitsSha256=target_pin,
                coverage=sum(len(c['footprint'])==1 for c in cases),geometry=blocks,
                screening=dict(Counter(c['result'] for c in cases)),
                eligibleUnsaturated=sum(c['candidate'] for c in cases),scientificClosure=False,fluxMeasured=False)
    write(f'go14949-{target}.json',dict(result,rows=cases))
    return {**result,'geometry':{k:{n:v for n,v in value.items() if n!='anchors'} for k,value in blocks.items()}}

def main():
    plan_sha='76ffdf7138f75461886105ff0cde07ac76899c98500dbc627c85f6289f912a3d'
    plan=read(pin(root/'protocollo-go14949.json',plan_sha))
    historical=base/'BKL046-ACS-11677-geometria-lunghe-v1'
    geometry=read(pin(historical/'protocollo.json',plan['geometryPlanSha256']))
    case_root=base/'BKL046-ACS-11677-scie-DQ-v1'
    co=read(pin(case_root/'riscontro.json',plan['sourceCohortSha256']))
    screen_plan=read(pin(case_root/'protocollo.json',co['designSha256']))
    if len(co['cases'])!=340:
        raise ValueError('Frozen cohort size changed')
    earlier=base/'BKL046-GO14949-nuovo-puntamento-v1'
    archived=read(pin(earlier/'protocollo.json',plan['archiveSelectionProtocolSha256']))
    helpers=runpy.run_path(str(pin(base/'BKL046-ACS11677-riferimento-esterno-v1'/'verifica-candidato-frame-v2.py',
        '2f72a51e7a9a28c44a81f41d9fb8bff2d62ffb495a7fe513ffb1a79637b1a98a')),run_name='screen_helpers')
    frozen=runpy.run_path(str(historical/'verifica.py'))
    load=frozen['load_fn']
    centroid=load(base/'BKL046-GO14949-registrazione-profondita-v1'/'transfer.py',
                  geometry['centroidSourceSha256'],'centroid')
    seeds=load(earlier/'check_new_pointing.py',geometry['seedSourceSha256'],'seeds')
    screen=runpy.run_path(str(case_root/'verifica.py'))['screen']
    helper_doc=dict(centroid=centroid,fit=frozen['fit'],screenPlan=screen_plan)
    source_path=base/'BKL046-ACS11677-drizzle-ingressi-v1'/'flc'/'jb6v01e0q_flc.fits'
    result=[]
    with fits.open(pin(source_path,plan['sourceSha256']),mode='readonly',memmap=True) as f:
        source=helpers['inputs'](f)
        anchors={}
        for i in (1,2):
            frame=source[i]
            xy=np.where(frame['dq']==0,frame['data'],-np.inf)
            anchors[i]=[]
            for seed in seeds(np,xy,geometry):
                p,error=centroid(np,frame['data'],frame['dq'],np.asarray(seed))
                if error is None:
                    anchors[i].append((*seed,*p))
        for target,row in plan['targets'].items():
            name,seconds,digest=archived['frames'][row['archiveRole']]
            if name!=target+'_flc.fits' or seconds!=40:
                raise ValueError('Prior capture no longer binds the exact trial')
            identity=dict(wcs=row['wcs'],sha256=digest,margin=plan['edgeMarginPixels'],planSha256=plan_sha)
            result.append(evaluate(target,identity,earlier/name,co['cases'],geometry,helper_doc,helpers,source,anchors,screen))
    write('go14949-sintesi.json',dict(planSha256=plan_sha,targets=result,scientificClosure=False))
    for r in result:
        print(r['root'],r['coverage'],r['eligibleUnsaturated'],r['screening'],
          {k:(v['matched'],v['status'],v.get('models',{}).get('affine',{}).get('p90Px')) for k,v in r['geometry'].items()})

if __name__=='__main__':
    sys.argv[:]=[sys.argv[0],'jbbf01i1q']
    main()
