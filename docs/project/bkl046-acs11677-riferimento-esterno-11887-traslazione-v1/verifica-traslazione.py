
from collections import Counter
from hashlib import file_digest
from pathlib import Path
import json
import runpy
import sys

root=Path(__file__).resolve().parent
sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
from astropy.io import fits
import numpy as np

def sha(path):
    with path.open('rb') as f:
        return file_digest(f,'sha256').hexdigest()

def apply(source,target,plan,geometry,seeds,centroid,project):
    tile=geometry['tilePixels']
    margin=plan['minimumTrainingSourceTileEdgeMarginPx']
    width=plan['searchHalfWidthPx']
    source_peaks=np.asarray(list(seeds(np,np.where(source['dq']==0,source['data'],-np.inf),geometry)))
    block=np.floor_divide(source_peaks,tile)
    relative=source_peaks%tile
    train=(block.sum(axis=1)%2==0)&np.all((relative>=margin)&(relative<tile-margin),axis=1)
    location=[]
    anchors=[]
    for p,t in zip(source_peaks[train],block[train],strict=True):
        xy,reason=centroid(np,source['data'],source['dq'],p)
        if reason is None:
            location.append(t)
            anchors.append(xy)
    if not anchors:
        return dict(status='NO_TRAINING_ANCHORS',sourceTrainingAnchors=0)
    location=np.asarray(location)
    forecast=project(source['wcs'],target['wcs'],np.asarray(anchors))
    keep=(forecast[:,0]>=6)&(forecast[:,0]<4090)&(forecast[:,1]>=6)&(forecast[:,1]<2042)
    forecast,location=forecast[keep],location[keep]
    target_peaks=np.asarray(list(seeds(np,np.where(target['dq']==0,target['data'],-np.inf),geometry)))
    candidate_deltas=[]
    indices=[]
    target_xy={}
    for j,prediction in enumerate(forecast):
        nearby=np.flatnonzero(np.max(abs(target_peaks-prediction),axis=1)<=width)
        for k in nearby:
            if k not in target_xy:
                target_xy[k],_=centroid(np,target['data'],target['dq'],target_peaks[k])
            xy=target_xy[k]
            if xy is not None and np.max(abs(xy-prediction))<=width:
                indices.append((j,int(k)))
                candidate_deltas.append(xy-prediction)
    result=dict(sourceTrainingAnchors=len(forecast),targetPeakChecks=len(target_xy),possiblePairs=len(indices))
    if not candidate_deltas:
        return dict(result,status='NO_TRANSLATION_SUPPORT')
    delta=np.asarray(candidate_deltas)
    cell=np.rint(delta).astype(int)+width
    counts=np.zeros((2*width+1,2*width+1),dtype=int)
    np.add.at(counts,(cell[:,0],cell[:,1]),1)
    padded=np.pad(counts,1)
    n=2*width+1
    smooth=sum(padded[x:x+n,y:y+n] for x in range(3) for y in range(3))
    center=np.array(np.unravel_index(np.argmax(smooth),smooth.shape))
    axes=np.indices(smooth.shape)
    far=((axes-center[:,None,None])**2).sum(axis=0)>=plan['independentPeakDistancePx']**2
    runner=int(smooth[far].max())
    coarse=center-width
    errors=np.linalg.norm(delta-coarse,axis=1)
    matched=[]
    seen_source=set()
    seen_target=set()
    for choice in np.argsort(errors,kind='stable'):
        if errors[choice]>plan['supportRadiusPx']:
            break
        j,k=indices[choice]
        if j in seen_source or k in seen_target:
            continue
        seen_source.add(j)
        seen_target.add(k)
        matched.append(int(choice))
    tiles=len({tuple(location[j]) for j in seen_source})
    votes=int(smooth[tuple(center)])
    accepted=(len(matched)>=plan['minimumDominantUniqueAnchors'] and tiles>=plan['minimumDominantSourceTiles']
              and votes>=plan['minimumRatioToRunnerUp']*runner)
    return dict(result,status='COHERENT_TRANSLATION_ON_TRAINING' if accepted else 'INSUFFICIENT_OR_AMBIGUOUS',
                coarseShiftPx=coarse.tolist(),peakVotes=votes,runnerUpVotes=runner,uniqueSupport=len(matched),
                sourceTiles=tiles,medianShiftPx=np.median(delta[matched],axis=0).tolist() if matched else None)

def main():
    path=root/'protocollo-traslazione-diagnostica-v1.json'
    plan_sha='0d287520e74b28b3b0269ba4fa26cd65d53db7cf999955d9b506f0c30bd361e7'
    if sha(path)!=plan_sha:
        raise ValueError('Translation protocol changed')
    plan=json.loads(path.read_bytes())
    old=Path(r'O:\BKL046-ACS-11677-geometria-lunghe-v1')
    actual={
        'geometryProtocol':old/'protocollo.json',
        'initialDiagnostic':root/'diagnosi-jbbf01i1q.json',
        'jb6v01e0q_flc.fits':Path(r'O:\BKL046-ACS11677-drizzle-ingressi-v1\flc\jb6v01e0q_flc.fits'),
        'jbbf01i1q_flc.fits':root/'jbbf01i1q_flc.fits',
    }
    if any(sha(p)!=plan['inputs'][k] for k,p in actual.items()):
        raise ValueError('Frozen scientific input changed')
    geometry=json.loads(actual['geometryProtocol'].read_bytes())
    helpers=runpy.run_path(str(root/'verifica-candidato-frame-v2.py'),run_name='translation_helpers')
    load=runpy.run_path(str(old/'verifica.py'))['load_fn']
    centroid=load(Path(r'O:\BKL046-GO14949-registrazione-profondita-v1\transfer.py'),geometry['centroidSourceSha256'],'centroid')
    seeds=load(Path(r'O:\BKL046-GO14949-nuovo-puntamento-v1\check_new_pointing.py'),geometry['seedSourceSha256'],'seeds')
    with fits.open(actual['jb6v01e0q_flc.fits'],memmap=True) as native, fits.open(actual['jbbf01i1q_flc.fits'],memmap=True) as trial:
        a,b=(helpers['inputs'](f) for f in (native,trial))
        result={f'{i}->{j}':apply(a[i],b[j],plan,geometry,seeds,centroid,helpers['project'])
                for i in (1,2) for j in (1,2)}
    report=dict(protocolSha256=plan_sha,heldoutMeasured=False,scientificClosure=False,chipPairs=result)
    out=root/'diagnosi-traslazione-jbbf01i1q.json'
    with out.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(report,stream,indent=2,allow_nan=False)
        stream.write('\n')
    print(json.dumps(report),flush=True)

if __name__=='__main__':
    sys.argv[:]=[sys.argv[0],'jbbf01i1q']
    main()
