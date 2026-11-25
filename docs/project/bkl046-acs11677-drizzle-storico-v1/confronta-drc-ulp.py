import json
from pathlib import Path
import runpy
from tarfile import open as open_tar
from tempfile import TemporaryDirectory
import shutil

here=Path(__file__).resolve().parent
core=runpy.run_path(str(here/'confronta-drc.py'))
np,fits=core['np'],core['fits']
sha,require=core['digest'],core['require']

def sortable(x):
    # Big-endian FITS arrays are normalized to host byte order before inspecting bits.
    bits=x.astype(np.float32,copy=False).view(np.uint32)
    return np.where((bits&0x80000000)!=0,~bits,bits|np.uint32(0x80000000)).astype(np.int64)

def difference(a,b):
    require(a.shape==b.shape and a.dtype.kind==b.dtype.kind=='f' and a.dtype.itemsize==b.dtype.itemsize==4,
            'Expected compatible 32-bit floating-point arrays')
    hist={}
    n=0
    for start in range(0,a.shape[0],128):
        aa=a[start:start+128]
        bb=b[start:start+128]
        selection=np.isfinite(aa)&np.isfinite(bb)&(aa!=bb)
        n+=int(np.count_nonzero(selection))
        distance=np.abs(sortable(aa[selection])-sortable(bb[selection]))
        keys,counts=np.unique(distance,return_counts=True)
        for k,c in zip(keys,counts,strict=True):
            hist[str(int(k))]=hist.get(str(int(k)),0)+int(c)
    return dict(changedFinite=n,ulpHistogram=hist,maxUlp=max(map(int,hist),default=0))

def main():
    baseline=here/'confronto-drc-mast.json'
    cmp=json.loads(baseline.read_bytes())
    mast=here/'jb6v01010_drc-official.fits'
    ref=here/'historical-export.tar'
    receipt=json.loads((here/'historical-received.json').read_bytes())
    require(sha(mast)==cmp['officialSha256'],'Official file changed')
    require(sha(ref)==receipt['archiveSha256'] and receipt['data']['drcSha256']==cmp['replicaSha256'],'Replica archive changed')
    require(cmp['context']['inputOrderMatches'] and cmp['payloads']['CTX']['unequalFinite']==0,'CTX differs or its meaning changed')
    with TemporaryDirectory(prefix='bkl046-float32-',dir=here) as folder,open_tar(ref,'r:') as tar:
        leaf=receipt['data']['file']
        entry,=[m for m in tar.getmembers() if m.isfile() and m.name.removeprefix('./')==leaf]
        replica=Path(folder)/'generated.fits'
        with tar.extractfile(entry) as source,replica.open('xb') as destination:
            shutil.copyfileobj(source,destination,length=1048576)
        require(sha(replica)==cmp['replicaSha256'],'Replica DRC changed')
        with fits.open(mast,memmap=False) as a,fits.open(replica,memmap=False) as b:
            stats={name:difference(a[name,1].data,b[name,1].data) for name in ('SCI','WHT')}
            weights=a['WHT',1].data,b['WHT',1].data
            coverage=0
            for start in range(0,weights[0].shape[0],128):
                aa,bb=[x[start:start+128] for x in weights]
                coverage+=int(np.count_nonzero((np.isfinite(aa)&(aa>0))^(np.isfinite(bb)&(bb>0))))
    for name,m in stats.items():
        require(m['changedFinite']==cmp['payloads'][name]['unequalFinite'],'Difference count does not match independent baseline')
    saved=dict(drcComparisonSha256=sha(baseline),officialSha256=cmp['officialSha256'],replicaSha256=cmp['replicaSha256'],
               whtPositiveCoverageDisagreements=coverage,float32=stats,scientificClosure=False)
    where=here/'confronto-drc-ulp.json'
    with where.open('x',encoding='utf-8',newline='\n') as out:
        json.dump(saved,out,sort_keys=True,indent=2)
        out.write('\n')
    print(json.dumps(saved),flush=True)

if __name__=='__main__':
    main()
