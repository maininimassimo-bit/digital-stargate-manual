from collections import Counter
from hashlib import file_digest
import json
from pathlib import Path
import runpy
import sys

root=Path(__file__).resolve().parent
base=Path('O:/')
sys.path.insert(0,str(base/'BKL046-ACS-WFC-runtime-7.2.0'))
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.wcs.utils import wcs_to_celestial_frame

def project(source, target, xy):
    source_frame = wcs_to_celestial_frame(source)
    target_frame = wcs_to_celestial_frame(target)
    world = source.all_pix2world(xy, 0, ra_dec_order=True)
    if not source_frame.is_equivalent_frame(target_frame):
        position = SkyCoord(world[:, 0] * u.deg, world[:, 1] * u.deg, frame=source_frame)
        transformed = position.transform_to(target_frame)
        world = np.column_stack((transformed.spherical.lon.deg, transformed.spherical.lat.deg))
    return target.all_world2pix(world, 0, tolerance=1e-8, maxiter=70, quiet=False, ra_dec_order=True)

old=base/'BKL046-ACS-11677-geometria-lunghe-v1'
case_dir=base/'BKL046-ACS-11677-scie-DQ-v1'
target_root='jbbf01i1q'
footprint=root/f'copertura-frame-{target_root}.json'
projections={
    'j6mfa8v8q':'ec03f59536cf3d476951e18a29a54b6de0b2bc20aaa3dbd3eaac4fa56561df5f',
    'jbbf01i1q':'bd96193fb5612969b56fa0fef03604904efe31fab65c2816c509bb77902aac1f',
}
long=base/'BKL046-ACS11677-drizzle-ingressi-v1'/'flc'/'jb6v01e0q_flc.fits'
short=root/f'{target_root}_flc.fits'
def digest(path):
    with path.open('rb') as f:return file_digest(f,'sha256').hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)

def inputs(h):
    assert h[0].header['INSTRUME']=='ACS' and h[0].header['DETECTOR']=='WFC'
    assert 'F606W' in (h[0].header['FILTER1'],h[0].header['FILTER2'])
    data={}
    for ext,chip in ((1,2),(2,1)):
        sci=h['SCI',ext]
        assert sci.header['CCDCHIP']==chip and sci.header['BUNIT'].strip().upper()=='ELECTRONS'
        dq=h['DQ',ext].data
        w=WCS(sci.header,h)
        require((w.wcs.radesys=='ICRS' or (w.wcs.radesys=='FK5' and w.wcs.equinox==2000.0))
                and w.has_distortion and sci.data.shape==dq.shape==(2048,4096),
                'Chip geometry differs from frozen setup')
        data[chip]={'data':sci.data,'dq':dq,'wcs':w}
    return data

def fit_pair(source,target,stellar_seeds,centroid,fit,plan,shift):
    seeds=np.asarray(stellar_seeds)
    if not len(seeds):
        return dict(status='NO_SOURCE_ANCHORS',belongs=0,matched=0,passed=False,anchors=[]),None
    xy=seeds[:,2:4]
    forecasts=project(source['wcs'],target['wcs'],xy)+shift
    inside=(forecasts[:,0]>=20)&(forecasts[:,0]<4076)&(forecasts[:,1]>=20)&(forecasts[:,1]<2028)
    fitted=[]
    used=set()
    counts=Counter()
    for seed,guess in zip(seeds[inside],forecasts[inside],strict=True):
        observed,err=centroid(np,target['data'],target['dq'],guess)
        if err:
            counts[err]+=1
            continue
        match=tuple(np.rint(observed).astype(int))
        if match in used:
            counts['duplicate_peak']+=1
            continue
        used.add(match)
        tile=np.floor_divide(seed[:2].astype(int),plan['tilePixels'])
        fitted.append(dict(source=seed[2:4].tolist(),estimate=guess.tolist(),observed=observed.tolist(),tile=tile.tolist()))
    matched=len(fitted)
    summary=dict(belongs=int(inside.sum()),matched=matched,rejected=dict(counts),anchors=fitted,status='NO_MATCHED_ANCHORS',passed=False)
    if not matched:
        return summary,None
    pts,tiles,obs,forecasts=[np.asarray([v[key] for v in fitted]) for key in ('source','tile','observed','estimate')]
    train=tiles.sum(axis=1)%2==0
    test=~train
    delta=obs-forecasts
    state,models=fit(pts,delta,train,test,tiles,plan,source['data'].shape)
    ok=bool(models.get('affine',{}).get('passes',False))
    summary.update(status=state,models=models,passed=ok,fitStars=int(train.sum()),heldoutStars=int(test.sum()),
                fitTiles=len(np.unique(tiles[train],axis=0)),heldoutTiles=len(np.unique(tiles[test],axis=0)))
    if not ok:
        return summary,None
    scale=np.array([4096.,2048.])
    x=np.column_stack((np.ones(len(pts)),pts/scale-.5))
    coefficients,_,rank,_=np.linalg.lstsq(x[train],delta[train],rcond=None)
    require(rank==3,'Independent centroid affine fit is singular')
    summary['polynomialCoefficients']=coefficients.tolist()
    return summary,coefficients

def main():
    recipe=root/'protocollo-traslazione-holdout-v1.json'
    require(digest(recipe)=='b51b8e0786210b595922dea0eb781d0a363b32735d6d68ba9c0f915796a10cfa','Shift holdout protocol changed')
    choice=json.loads(recipe.read_bytes())
    require(digest(root/'diagnosi-traslazione-jbbf01i1q.json')==choice['shiftDiagnosticSha256'],'Training shift changed')
    shifts={k:np.asarray(v) for k,v in choice['offsets'].items()}
    require(digest(footprint)==projections[target_root],
            'Frozen candidate projection changed')
    mapdoc=json.loads(footprint.read_bytes())
    receipt=json.loads((root/f'{target_root}-acquisizione.json').read_bytes())
    require(digest(short)==receipt['sha256'] and digest(long)==mapdoc['referenceFLCsha256'],
            'Measured exposure digest changed')
    ancestor=old/'protocollo.json'
    require(digest(ancestor)==mapdoc['geometryQualificationProtocolSha256']==choice['originalGeometryProtocolSha256'],'Geometry rules changed')
    plan=json.loads(ancestor.read_bytes())
    screen_plan=case_dir/'protocollo.json'
    case_data=json.loads((case_dir/'riscontro.json').read_bytes())
    require(digest(case_dir/'riscontro.json')==mapdoc['sourceCasesSha256'] and digest(screen_plan)==case_data['designSha256'],
            'Frozen aperture rules changed')
    screens=json.loads(screen_plan.read_bytes())
    helpers=runpy.run_path(str(old/'verifica.py'))
    load_fn=helpers['load_fn']
    centroid=load_fn(base/'BKL046-GO14949-registrazione-profondita-v1'/'transfer.py',
                     plan['centroidSourceSha256'],'centroid')
    seeds=load_fn(base/'BKL046-GO14949-nuovo-puntamento-v1'/'check_new_pointing.py',
                  plan['seedSourceSha256'],'seeds')
    evaluate=runpy.run_path(str(case_dir/'verifica.py'))['screen']
    out,checks={},[]
    with fits.open(long,memmap=True,mode='readonly') as a,fits.open(short,memmap=True,mode='readonly') as b:
        require(a[0].header['EXPTIME']==1457. and b[0].header['EXPTIME']==mapdoc['target']['seconds']
                and b[0].header['ROOTNAME'].lower()==target_root,'Exposure duration drift')
        source,target=inputs(a),inputs(b)
        frames={side:{str(k):str(wcs_to_celestial_frame(v['wcs'])) for k,v in group.items()}
                for side,group in (('source',source),('target',target))}
        require(frames==mapdoc['coordinateFrames'],'FLC frame differs from the bound headerlet')
        models={}
        for chip in (1,2):
            frame=source[chip]
            observations=list(seeds(np,np.where(frame['dq']==0,frame['data'],-np.inf),plan))
            chosen=[]
            for seed in observations:
                xy,error=centroid(np,frame['data'],frame['dq'],np.asarray(seed))
                if not error:
                    chosen.append((*seed,*xy))
            for other in (1,2):
                key=f'{chip}->{other}'
                if key in shifts:
                    out[key],models[key]=fit_pair(frame,target[other],chosen,centroid,helpers['fit'],plan,shifts[key])
                else:
                    out[key],models[key]={'status':'NO_FROZEN_SHIFT','passed':False},None
                out[key]['selectedSourceSeeds']=len(observations)
                out[key]['usableSourceSeeds']=len(chosen)
        for c in mapdoc['positions']:
            record=dict(sourceId=c['sourceId'],chip=c['chip'])
            candidates=c['candidates']
            if len(candidates)!=1:
                checks.append(dict(record,state='no_unique_footprint'))
                continue
            other=candidates[0]['chip']
            key=f"{c['chip']}->{other}"
            frame=target[other]
            src=np.asarray([c['xy']])
            guess=project(source[c['chip']]['wcs'],frame['wcs'],src)[0]+shifts.get(key,np.zeros(2))
            transform=models[key]
            if transform is not None:
                correction=np.r_[1.,src[0]/np.array([4096.,2048.])-.5]@transform
                guess+=correction
            accepted_geometry=transform is not None
            candidate=evaluate(frame['data'],frame['dq'],guess,screens)
            checks.append(dict(record,targetChip=other,geometryPass=accepted_geometry,
                        screen=candidate,state=candidate['state'],
                        referenceCandidate=accepted_geometry and candidate['state']=='CANDIDATE_UNSATURATED_REFERENCE'))
    result=dict(protocolSha256=digest(recipe),coordinateFrames=frames,target=mapdoc['target'],footprintSha256=digest(footprint),shortSha256=digest(short),longSha256=digest(long),
                geometry=out,states=dict(Counter(x['state'] for x in checks)),
                geometricallyQualified=sum(bool(x.get('geometryPass')) for x in checks),
                referenceCandidates=sum(bool(x.get('referenceCandidate')) for x in checks),rows=checks,
                fluxMeasured=False,scientificClosure=False)
    dest=root/f'diagnosi-traslazione-holdout-{target_root}.json'
    with dest.open('x',encoding='utf-8',newline='\n') as report:
        json.dump(result,report,sort_keys=True,indent=2,allow_nan=False)
        report.write('\n')
    print({k:v for k,v in result.items() if k not in ('geometry','rows')},digest(dest),flush=True)

if __name__=='__main__':
    main()
