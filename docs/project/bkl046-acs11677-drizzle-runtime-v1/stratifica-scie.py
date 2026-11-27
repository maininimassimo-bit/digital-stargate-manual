from argparse import ArgumentParser
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
from tarfile import open as open_tar
import sys

sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
from astropy.io import fits
import numpy as np

root=Path(__file__).resolve().parent
original=Path(r'O:\BKL046-ACS11677-drizzle-ingressi-v1\flc\jb6v01e0q_flc.fits')
prior=Path(r'O:\BKL046-ACS-11677-scie-DQ-v1\riscontro.json')
original_sha='e6011691a50b2608a3cb91e5f9ceb0957aa4a17e46aa04f8e00bee30df5fdd4d'
prior_sha='c7ab445f872054b6c4261c1250a733443c8b0d2316a8f0126e102f976235e43d'

def check(test,message):
    if not test:raise ValueError(message)

def sha(path):
    with path.open('rb') as stream:
        return file_digest(stream,'sha256').hexdigest()

def components(mask):
    points=set(map(tuple,np.argwhere(mask).tolist()))
    while points:
        seed=min(points)
        points.remove(seed)
        stack=[seed]
        group=[]
        while stack:
            y,x=stack.pop()
            group.append((y,x))
            for i in range(y-1,y+2):
                for j in range(x-1,x+2):
                    point=(i,j)
                    if point in points:
                        points.remove(point)
                        stack.append(point)
        yield np.array(group)

def signature(values):
    v,n=np.unique(values,return_counts=True)
    return {str(int(x)):int(c) for x,c in zip(v,n)}

def matching_support(flags,expected):
    selected=np.zeros(flags.shape,dtype=bool)
    cases=[]
    for cluster in components(flags&256!=0):
        y,x=cluster.T
        span=int(y.max()-y.min()+1)
        if span<21:
            continue
        selected[y,x]=True
        cases.append((span,len(y),[float(np.median(x)),float((y.min()+y.max())/2)],signature(flags[y,x])))
    historical=[(c['verticalSpan'],c['fullWellPixels'],c['centerXY'],c['longDqCounts']) for c in expected]
    check(cases==historical,'The derived trail membership differs from the frozen case list')
    return selected

def count_cells(a,b,where):
    check(a.shape==b.shape==where.shape,'Masks have incompatible shape')
    return dict(neither=int(np.count_nonzero(~a & ~b & where)),both=int(np.count_nonzero(a & b & where)),
                archiveOnly=int(np.count_nonzero(a & ~b & where)),replicaOnly=int(np.count_nonzero(~a & b & where)))

def store(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(value,stream,sort_keys=True,indent=2)
        stream.write('\n')

def preflight():
    check(sha(original)==original_sha and sha(prior)==prior_sha,'Input evidence hash mismatch')
    cases=json.loads(prior.read_bytes())['cases']
    result=[]
    with fits.open(original,memmap=False,mode='readonly') as hdu:
        for ext in (1,2):
            flags=hdu['DQ',ext].data
            chip=hdu['SCI',ext].header['CCDCHIP']
            expected=[c for c in cases if c['chip']==chip]
            support=matching_support(flags,expected)
            archived=flags&4096!=0
            result.append(dict(chip=chip,extension=ext,shape=list(support.shape),components=len(expected),
                               trailPixels=int(np.count_nonzero(support)),trailWithArchive4096=int(np.count_nonzero(support&archived)),
                               maskSha256=sha256(support.tobytes()).hexdigest()))
    check(sum(x['components'] for x in result)==340,'Unexpected total of long trail components')
    check(sum(x['trailPixels'] for x in result)==82560,'Unexpected trail population')
    check(sum(x['trailWithArchive4096'] for x in result)==14372,'Unexpected archived trail 4096 count')
    return result

def measure(path,expected_archive_digest):
    check(sha(path)==expected_archive_digest,'Unexpected archive digest')
    baseline=preflight()
    rows=[]
    with open_tar(path,'r:') as archive, fits.open(original,memmap=False,mode='readonly') as hdu:
        with archive.extractfile('replica.json') as stream:
            science=json.load(stream)
        source,=[x for x in science['masks'] if x['file']==original.name]
        cases=json.loads(prior.read_bytes())['cases']
        for fixed in baseline:
            chip,ext=fixed['chip'],fixed['extension']
            expected,=[x for x in source['science'] if x['chip']==chip and x['sciExt']==ext]
            masks=[m for m in archive.getmembers() if m.isfile() and m.name.removeprefix('./')==expected['maskFile']]
            check(len(masks)==1,'Unexpected mask archive member count')
            with archive.extractfile(masks[0]) as stream:
                pixels=stream.read()
            check(sha256(pixels).hexdigest()==expected['maskSha256'],'CR mask SHA mismatch')
            with fits.open(BytesIO(pixels),memmap=False) as src:
                indicator=src[0].data
            original_flags=hdu['DQ',ext].data
            support=matching_support(original_flags,[c for c in cases if c['chip']==chip])
            check(sha256(support.tobytes()).hexdigest()==fixed['maskSha256'],'Trail mask drift')
            check(indicator.shape==support.shape and np.isin(indicator,(0,1)).all(),'Invalid replica mask')
            a=original_flags&4096!=0
            b=indicator==0
            on,off=count_cells(a,b,support),count_cells(a,b,~support)
            expected_counts=expected['counts']
            check(all(on[k]+off[k]==expected_counts[k] for k in expected_counts),'The stratified counts do not sum to the complete chip')
            rows.append(dict(fixed,archive=expected['maskSha256'],onTrail=on,offTrail=off))
    return dict(measured=True,archiveSha256=expected_archive_digest,archivedReportSha256=prior_sha,
                inputSha256=original_sha,scope='Frozen L1457 saturated trails, pixel-grid comparison only.',chips=rows)

if __name__=='__main__':
    parser=ArgumentParser()
    parser.add_argument('--archive',type=Path)
    parser.add_argument('--sha256')
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    if args.archive:
        check(args.sha256 is not None,'An expected archive SHA-256 is required')
        data=measure(args.archive,args.sha256)
    else:
        data=dict(measured=False,archivedReportSha256=prior_sha,inputSha256=original_sha,baseline=preflight())
    store(args.output,data)
    print(sha(args.output),flush=True)
