from argparse import ArgumentParser
from hashlib import file_digest
import json
import math
from pathlib import Path
import shutil
from tarfile import open as open_tar
from tempfile import TemporaryDirectory
import sys

root=Path(__file__).resolve().parent
sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
from astropy.io import fits
import numpy as np

def require(ok,message):
    if not ok:raise ValueError(message)

def digest(path):
    with path.open('rb') as stream:
        return file_digest(stream,'sha256').hexdigest()

def header_grid(hdu):
    keys=('NAXIS1','NAXIS2','CRPIX1','CRPIX2','CRVAL1','CRVAL2','CTYPE1','CTYPE2','CUNIT1','CUNIT2',
          'CD1_1','CD1_2','CD2_1','CD2_2','BUNIT')
    return {k:hdu.header.get(k) for k in keys}

def same_grid(a,b):
    require(a.keys()==b.keys(),'Different grid keys')
    mismatches=[]
    for key in a:
        x,y=a[key],b[key]
        if key in ('CRVAL1','CRVAL2','CRPIX1','CRPIX2','CD1_1','CD1_2','CD2_1','CD2_2'):
            equal=isinstance(x,(float,int)) and isinstance(y,(float,int)) and math.isclose(x,y,rel_tol=0,abs_tol=1e-12)
        else:
            equal=x==y
        if not equal:mismatches.append((key,x,y))
    return mismatches

def compare(a,b,label):
    require(a.shape==b.shape,f'Different {label} payload dimensions')
    planes=1 if a.ndim==2 else a.shape[0]
    ah=a.reshape((planes,*a.shape[-2:]))
    bh=b.reshape((planes,*b.shape[-2:]))
    out=dict(shape=list(a.shape),elements=int(a.size),bothFinite=0,bothNonfinite=0,finiteMismatch=0,
             equalFinite=0,unequalFinite=0,maxAbsDifference=0.0)
    squared=0.0
    # Bounded slices so the FITS arrays can remain memory mapped.
    for i in range(planes):
        for start in range(0,a.shape[-2],128):
            x=ah[i,start:start+128]
            y=bh[i,start:start+128]
            ix,iy=np.isfinite(x),np.isfinite(y)
            both=ix & iy
            n=int(np.count_nonzero(both))
            equal=int(np.count_nonzero(both & (x==y)))
            out['bothFinite']+=n
            out['equalFinite']+=equal
            out['unequalFinite']+=n-equal
            out['bothNonfinite']+=int(np.count_nonzero(~ix & ~iy))
            out['finiteMismatch']+=int(np.count_nonzero(ix ^ iy))
            if n:
                delta=x[both].astype(np.float64)-y[both].astype(np.float64)
                out['maxAbsDifference']=max(out['maxAbsDifference'],float(np.max(np.abs(delta))))
                squared+=float(np.sum(delta*delta,dtype=np.float64))
    out['rmsDifference']=math.sqrt(squared/out['bothFinite']) if out['bothFinite'] else None
    return out

def context_order(hdul):
    import re
    order={}
    for key in hdul[0].header:
        match=re.fullmatch(r'D(\d{3})DATA',key)
        if match:
            value=str(hdul[0].header[key]).replace('\\','/').rsplit('/',1)[-1].strip().lower()
            number=int(match.group(1))
            require(number not in order,'Duplicate context mapping card')
            require(re.fullmatch(r'jb6v01[a-z0-9]{3}_flc\.fits\[sci,[12]\]',value) is not None,
                    'Invalid context mapping '+value)
            order[number]=value
    if sorted(order)!=list(range(1,13)) or len(set(order.values()))!=12:
        return []
    return [order[i] for i in range(1,13)]

def compare_payloads(first,second):
    a,b=context_order(first),context_order(second)
    data={key:compare(first[key,1].data,second[key,1].data,key) for key in ('SCI','WHT')}
    same=bool(a) and a==b
    if same:
        data['CTX']=compare(first['CTX',1].data,second['CTX',1].data,'CTX')
    return data,dict(inputOrderMatches=same,first=a,second=b)


def main():
    cli=ArgumentParser()
    cli.add_argument('official',type=Path)
    cli.add_argument('official_receipt',type=Path)
    cli.add_argument('replica_archive',type=Path)
    cli.add_argument('replica_receipt',type=Path)
    cli.add_argument('output',type=Path)
    args=cli.parse_args()
    a=json.loads(args.official_receipt.read_bytes())
    b=json.loads(args.replica_receipt.read_bytes())
    require(digest(args.official)==a['sha256'],'Official DRC checksum mismatch')
    require(digest(args.replica_archive)==b['archiveSha256'],'Replica TAR checksum mismatch')
    with TemporaryDirectory(prefix='bkl046-drc-compare-',dir=root) as tmp,open_tar(args.replica_archive,'r:') as archive:
        name=b['data']['file']
        require(Path(name).name==name and name.endswith('_drc.fits'),'Unexpected DRC name')
        entries=[m for m in archive.getmembers() if m.isfile() and m.name.removeprefix('./')==name]
        require(len(entries)==1,'Unexpected DRC TAR membership')
        local=Path(tmp)/name
        with archive.extractfile(entries[0]) as source,local.open('xb') as dest:
            shutil.copyfileobj(source,dest,length=1048576)
        require(digest(local)==b['data']['drcSha256'],'Extracted DRC checksum mismatch')
        with fits.open(args.official,memmap=True) as official,fits.open(local,memmap=True) as replica:
            grids=[header_grid(x['SCI',1]) for x in (official,replica)]
            mismatches=same_grid(*grids)
            receipt=dict(officialSha256=a['sha256'],replicaSha256=b['data']['drcSha256'],
                         officialGrid=grids[0],replicaGrid=grids[1],gridMismatches=mismatches,
                         maximumWcsHeaderAbsDifference=1e-12,scientificClosure=False)
            if not mismatches:
                receipt['payloads'],receipt['context']=compare_payloads(official,replica)
                receipt['comparablePixelGrid']=True
            else:
                receipt['comparablePixelGrid']=False
    with args.output.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(receipt,stream,indent=2,sort_keys=True)
        stream.write('\n')
    print(digest(args.output),flush=True)

if __name__=='__main__':
    main()
