
from collections import Counter
from hashlib import file_digest
from pathlib import Path
import json
import runpy
import sys

here=Path(__file__).resolve().parent
base=Path('O:/')
sys.path.insert(0,str(base/'BKL046-ACS-WFC-runtime-7.2.0'))
import numpy as np
from astropy.io import fits

def sha(p):
    with p.open('rb') as f:return file_digest(f,'sha256').hexdigest()
def pin(path,value):
    if sha(path)!=value:raise ValueError('Unexpected digest: '+path.name)
    return path
def read(p):return json.loads(p.read_bytes())

def profile(frame,chip,seed,moment,cube,helpers):
    if not np.isfinite(moment).all():raise ValueError('A valid moment is required for PSF fitting')
    x,y=np.rint(seed).astype(int)
    dy,dx=np.mgrid[-3:4,-3:4]
    core=dx*dx+dy*dy<=9
    grid=helpers['psf_at'](np,cube,seed,chip)
    values=frame['data'][y-3:y+4,x-3:x+4][core].astype(float)
    result=helpers['solve'](np,grid,(x+dx)[core],(y+dy)[core],values,seed)
    if result is not None and not np.isfinite(result).all():raise ValueError('Nonfinite PSF result')
    return result

def measure_pair(a,b,target_chip,anchors,settings,geometry):
    retained=[]
    rejected=Counter()
    if not anchors:return dict(status='NO_SOURCE_ANCHORS',pairs=[])
    project=settings['project']
    m=np.asarray([r['sourceMoment'] for r in anchors])
    e=np.asarray([r['sourcePsf'] for r in anchors])
    wcs_a=project(a['wcs'],b['wcs'],m)
    wcs_b=project(a['wcs'],b['wcs'],e)
    used=set()
    for row,moment_seed,psf_seed in zip(anchors,wcs_a,wcs_b,strict=True):
        x,y=moment_seed
        if not(20<=x<4076 and 20<=y<2028):
            rejected['outside']+=1
            continue
        mfit,error=settings['centroid'](np,b['data'],b['dq'],moment_seed)
        if error is not None:
            rejected[error]+=1
            continue
        pfit=profile(b,target_chip,moment_seed,mfit,settings['cube'],settings['psf'])
        if pfit is None:
            rejected['PSF_SEARCH_LIMIT']+=1
            continue
        identity=tuple(np.rint(mfit).astype(int))
        if identity in used:
            rejected['duplicatePeak']+=1
            continue
        used.add(identity)
        retained.append(dict(row,targetMoment=mfit.tolist(),targetPsf=pfit.tolist(),
                             predictMoment=moment_seed.tolist(),predictPsf=psf_seed.tolist()))
    data=dict(commonPairs=len(retained),rejected=dict(rejected),status='NO_COMMON_PAIRS',methods={},pairs=retained)
    if not retained:return data
    coords,tiles,positions,forecast=(np.asarray([r[k] for r in retained]) for k in
        ('sourceMoment','tile','targetMoment','predictMoment'))
    train=tiles.sum(axis=1)%2==0
    test=~train
    data.update(fitStars=int(train.sum()),heldoutStars=int(test.sum()),
                fitTiles=len(np.unique(tiles[train],axis=0)),heldoutTiles=len(np.unique(tiles[test],axis=0)))
    for label,p,q in [('positiveMoment','targetMoment','predictMoment'),('standardEPSF','targetPsf','predictPsf')]:
        residual=np.asarray([r[p] for r in retained])-np.asarray([r[q] for r in retained])
        status,models=settings['fit'](coords,residual,train,test,tiles,geometry,a['data'].shape)
        data['methods'][label]=dict(status=status,models=models,meetsFrozenGeometry=bool(models.get('affine',{}).get('passes')))
    data['status']=data['methods']['standardEPSF']['status']
    return data

def main():
    gap=here/'protocollo-epsf.json'
    plan_sha='c87b1a9393ea160f8aa69ca6abb2950fcec8de202b37b9bd9448abf9b33ff3f2'
    plan=read(pin(gap,plan_sha))
    primary=base/'BKL046-ACS11677-drizzle-ingressi-v1'/'flc'/'jb6v01e0q_flc.fits'
    root=plan['targetRoot']
    target=here/(root+'_flc.fits')
    receipt=read(here/(root+'-acquisizione.json'))
    metadata=read(pin(here/'flc-metadati.json',plan['publicProductMetadataSha256']))[0]
    headerlet=pin(here/(root+'_flt_hlet.fits'),plan['targetHeaderletSha256'])
    if receipt['provider']!=metadata['head'] or receipt['provider']['x-amz-version-id']!=plan['targetObjectVersion']:
        raise ValueError('The measured exposure differs from the frozen provider object')
    pin(primary,plan['sourceSha256'])
    pin(target,receipt['sha256'])
    old=base/'BKL046-ACS-11677-geometria-lunghe-v1'
    geom=read(pin(old/'protocollo.json',plan['geometryProtocolSha256']))
    helpers=runpy.run_path(str(pin(base/'BKL046-ACS11677-riferimento-esterno-v1'/'verifica-candidato-frame-v2.py',
        '2f72a51e7a9a28c44a81f41d9fb8bff2d62ffb495a7fe513ffb1a79637b1a98a')),run_name='epsf_helpers')
    functions=runpy.run_path(str(old/'verifica.py'))
    load=functions['load_fn']
    centroid=load(base/'BKL046-GO14949-registrazione-profondita-v1'/'transfer.py',geom['centroidSourceSha256'],'centroid')
    seeds=load(base/'BKL046-GO14949-nuovo-puntamento-v1'/'check_new_pointing.py',geom['seedSourceSha256'],'seeds')
    psf_path=Path(r'U:\coordinatore-r4-bkl046\DSG-Shared-BKL046-GO14949-ePSF-6f208aaeadf3')
    psf=runpy.run_path(str(pin(psf_path/'compare_epsf.py',plan['psfFunctionsSha256'])))
    cube=fits.getdata(pin(psf_path/'STDPSF_ACSWFC_F606W_SM4.fits',plan['standardPsfSha256']),memmap=False)
    if cube.shape!=(90,101,101) or not np.isfinite(cube).all():
        raise ValueError('Unexpected standard PSF cube')
    setup=dict(project=helpers['project'],centroid=centroid,psf=psf,cube=cube,fit=functions['fit'])
    with fits.open(primary,memmap=True) as orig,fits.open(target,memmap=True) as test,fits.open(headerlet) as hdr:
        t=test[0].header
        if (t['ROOTNAME'].lower()!=root or t['PROPOSID']!=plan['targetProposalId']
            or t['EXPTIME']!=plan['targetExposureSeconds'] or
            not all(test['SCI',ext].header['WCSNAME']==hdr['SIPWCS',ext].header['WCSNAME'] for ext in (1,2))):
            raise ValueError('FITS headers differ from the prospective trial')
        a,b=helpers['inputs'](orig),helpers['inputs'](test)
        results={}
        train_stats={}
        for chip,frame in a.items():
            anchors=[]
            counts=Counter()
            for seed in seeds(np,np.where(frame['dq']==0,frame['data'],-np.inf),geom):
                seed=np.asarray(seed)
                m,status=centroid(np,frame['data'],frame['dq'],seed)
                if status is not None:
                    counts[status]+=1
                    continue
                p=profile(frame,chip,seed,m,cube,psf)
                if p is None:
                    counts['PSF_SEARCH_LIMIT']+=1
                    continue
                anchors.append(dict(sourceSeed=tuple(map(int,seed)),tile=(seed//geom['tilePixels']).tolist(),
                                         sourceMoment=m.tolist(),sourcePsf=p.tolist()))
            train_stats[str(chip)]=dict(common=len(anchors),rejected=dict(counts))
            for j,trial in b.items():
                results[f'{chip}->{j}']=measure_pair(frame,trial,j,anchors,setup,geom)
    report=dict(protocolSha256=plan_sha,sourceSha256=plan['sourceSha256'],target=root,targetSha256=receipt['sha256'],
                sourceAnchorSelection=train_stats,chipPairs=results,focusFit=False,heldoutMeasured=True,
                independentFluxMeasured=False,scientificClosure=False)
    filename=here/'riscontro-epsf.json'
    with filename.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(report,f,indent=2,allow_nan=False)
        f.write('\n')
    for k,v in results.items():
        print(k,v.get('fitStars'),v.get('heldoutStars'),v['status'],v.get('methods'))
    print('reportSha256',sha(filename),flush=True)

if __name__=='__main__':
    sys.argv[:]=[sys.argv[0],'jbbf01i1q']
    main()
