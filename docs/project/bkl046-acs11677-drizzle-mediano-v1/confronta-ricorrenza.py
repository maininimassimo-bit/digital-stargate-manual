from argparse import ArgumentParser
from contextlib import ExitStack
from io import BytesIO
import json
from pathlib import Path
import runpy
from tarfile import open as open_tar

root=Path(__file__).resolve().parent
base=Path('O:/')
old=base/'BKL046-ACS-11677-DQ4096-controllo-v1'
source=runpy.run_path(str(old/'verifica.py'))
np,fits,WCS=source['np'],source['fits'],source['WCS']
sha,read_json,trails,distribution=source['pin'],source['read_json'],source['trails'],source['distribution']
raw_plan=old/'protocollo.json'
manifest_drc=base/'BKL046-ACS11677-drizzle-ingressi-v1'/'manifest.json'
targets=('jb6v01e0q_flc.fits','jb6v01e5q_flc.fits')

def require(ok,description):
    if not ok:raise ValueError(description)

def json_out(path,result):
    with path.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(result,f,indent=2,sort_keys=True)
        f.write('\n')

def density(records,aa,bb,plan):
    data=[]
    for trail,sx,sy,tx,ty in records:
        data.append((int(trail),int(tx),int(ty),0.,bool(aa[sy,sx]),bool(bb[ty,tx])))
    return distribution(data,plan)

def freeze(membership,receipt):
    plan=json.loads(raw_plan.read_bytes())
    historic=json.loads((old/'riscontro.json').read_bytes())
    require(sha(raw_plan)==historic['planSha256'],'Recurrence plan changed')
    fan=base/'BKL046-ACS-11677-geometria-lunghe-v1'
    geometry=read_json(fan/'riscontro.json',plan['geometrySha256'])
    report=read_json(base/'BKL046-ACS-11677-DQ-replique-v1'/'riscontro.json',plan['replicaResultSha256'])
    model,=[item for item in geometry['chips'] if item['chip']==plan['chip']]
    require(model['models']['affine']['passes'],'Held-out geometry did not pass for chip')
    files=[manifest_drc.parent/'flc'/name for name in targets]
    require([sha(path) for path in files]==report['inputSha256'],'Input FLC pair differs')
    with ExitStack() as stack:
        a,b=[stack.enter_context(fits.open(f,mode='readonly',memmap=True)) for f in files]
        require(a['SCI',1].header['CCDCHIP']==b['SCI',1].header['CCDCHIP']==plan['chip']==2,'Incorrect detector chip')
        qa,qb=a['DQ',1].data,b['DQ',1].data
        aw,bw=WCS(a['SCI',1].header,a),WCS(b['SCI',1].header,b)
        anchors=model['anchors']
        source_pts=np.asarray([r['source'] for r in anchors])
        train=np.asarray([sum(r['tile'])%2==0 for r in anchors])
        measured=np.asarray([r['observed'] for r in anchors])
        geometric=np.asarray([r['estimate'] for r in anchors])
        size=np.array([qa.shape[1],qa.shape[0]],dtype=float)
        def basis(coords):
            return np.column_stack((np.ones(len(coords)),coords/size-.5))
        coeffs,_,rank,_=np.linalg.lstsq(basis(source_pts)[train],(measured-geometric)[train],rcond=None)
        require(rank==3,'Affine source reconstruction was singular')
        ordered=[]
        for ident,group in enumerate(trails((qa&256)!=0,plan['minimumVerticalSpanPx'])):
            y,x=group.T
            pts=np.column_stack((x,y))
            estimate=bw.all_world2pix(aw.all_pix2world(pts,0,ra_dec_order=True),0,tolerance=1e-8,
                                    maxiter=70,quiet=False,ra_dec_order=True)+basis(pts)@coeffs
            nearest=np.rint(estimate).astype(int)
            for i,(tx,ty) in enumerate(nearest):
                if 0<tx<qb.shape[1]-1 and 0<ty<qb.shape[0]-1 and qb[ty,tx]&256:
                    ordered.append((ident,x[i],y[i],tx,ty,float(np.linalg.norm(estimate[i]-nearest[i]))))
        chosen={}
        for i,(_,_,_,x,y,distance) in enumerate(ordered):
            if (x,y) not in chosen or distance<ordered[chosen[x,y]][5]:
                chosen[x,y]=i
        frozen=np.asarray([ordered[i][:5] for i in sorted(chosen.values())],dtype='<i4')
        original=density(frozen,qa&4096!=0,qb&4096!=0,plan)
    require(len(ordered)==29109 and len(frozen)==29087 and original==historic['distinctTargets'],
            'Frozen recurrence map did not reproduce archived comparison')
    with membership.open('xb') as dst:
        np.save(dst,frozen,allow_pickle=False)
    result=dict(membershipSha256=sha(membership),columns=['trail','sourceX','sourceY','repeatX','repeatY'],
                chip=2,inputFiles=list(targets),geometrySha256=plan['geometrySha256'],
                originalReportSha256=sha(old/'riscontro.json'),archived=original,replicaMeasured=False)
    json_out(receipt,result)
    print('FROZEN',len(frozen),sha(membership),flush=True)

def measure(membership,receipt,source_tar,hash_expected,out):
    known=json.loads(receipt.read_bytes())
    require(sha(membership)==known['membershipSha256'],'Membership changed')
    require(sha(source_tar)==hash_expected,'Replica TAR changed')
    membership=np.load(membership,allow_pickle=False)
    masks=[]
    with open_tar(source_tar,'r:') as tar:
        with tar.extractfile('replica.json') as stream:
            result=json.load(stream)
        for file in targets:
            matches=[x for x in result['masks'] if x['file']==file]
            require(len(matches)==1,'Replica must contain both frozen FLC files')
            item,=[x for x in matches[0]['science'] if x['chip']==2 and x['sciExt']==1]
            member,=[m for m in tar.getmembers() if m.isfile() and m.name.removeprefix('./')==item['maskFile']]
            with tar.extractfile(member) as stream:
                raw=stream.read()
            require(source['sha256'](raw).hexdigest()==item['maskSha256'],'Replica mask drift')
            with fits.open(BytesIO(raw),memmap=False) as opened:
                img=opened[0].data
                require(img.shape==(2048,4096) and np.isin(img,[0,1]).all(),'Replica CR mask format differs')
                masks.append(img==0)
    plan=json.loads(raw_plan.read_bytes())
    observed=density(membership,*masks,plan)
    require(observed['nearestCommonFullWell']==29087 and observed['trails']==121,'Replica map or groups changed')
    json_out(out,dict(membershipSha256=known['membershipSha256'],replicaTarSha256=hash_expected,
                      archived=known['archived'],replica=observed,scope='Frozen projection on chip 2 only.',
                      interpretation='Repeatability of a flag across the two exposures.',scientificClosure=False))
    print('MEASURED',sha(out),flush=True)

if __name__=='__main__':
    parser=ArgumentParser()
    parser.add_argument('membership',type=Path)
    parser.add_argument('receipt',type=Path)
    parser.add_argument('--tar',type=Path)
    parser.add_argument('--sha256')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.tar:
        require(args.sha256 and args.output,'Replica SHA and output required')
        measure(args.membership,args.receipt,args.tar,args.sha256,args.output)
    else:
        freeze(args.membership,args.receipt)
