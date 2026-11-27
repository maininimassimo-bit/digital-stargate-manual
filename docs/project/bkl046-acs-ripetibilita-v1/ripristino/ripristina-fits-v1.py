"""Restore the exact ACS FITS cohort recorded by BKL-046."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
from tempfile import NamedTemporaryFile
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PIN='689621adafc6090f99dd44908e8ae322fe4e93edfa469f32d7b63cf5bdf8f265'
FIT_LIMIT=215_000_000

def parse_manifest(path):
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PIN:
        raise ValueError('Acquisition manifest differs from the frozen cohort')
    rows=json.loads(raw)['files']
    if len(rows)!=24 or len({r['obs'] for r in rows})!=24:
        raise ValueError('Unexpected cohort size')
    return rows

def copy_verified(stream, row, target=None):
    digest=hashlib.sha256()
    size=0
    while chunk:=stream.read(1048576):
        size+=len(chunk)
        if size>row['size']:
            raise ValueError('FITS exceeds the pinned size')
        digest.update(chunk)
        if target:
            target.write(chunk)
    if size!=row['size'] or digest.hexdigest()!=row['sha256']:
        raise ValueError('FITS bytes differ from the pinned product')

def restore(row, dest, offline):
    obs=row['obs']
    if not re.fullmatch(r'[a-z0-9]{9}',obs) or not 0<row['size']<=FIT_LIMIT:
        raise ValueError('Invalid frozen product')
    leaf=obs+'_flt.fits'
    out=dest/leaf
    if out.exists():
        with out.open('rb') as handle:
            copy_verified(handle,row)
        return dict(obs=obs, origin='verified-existing')
    if offline:
        raise FileNotFoundError(out)
    url='https://mast.stsci.edu/api/v0.1/Download/file?'+urlencode({'uri':'mast:HST/product/'+leaf})
    error=None
    for _ in range(2):
        tmp=None
        try:
            req=Request(url,headers={'Range':'bytes=0-','Accept-Encoding':'identity','Cache-Control':'no-cache'})
            with urlopen(req,timeout=25) as stream:
                if stream.status not in (200,206):
                    raise ValueError(f'Unexpected HTTP status {stream.status}')
                if stream.status==206 and stream.headers.get('Content-Range')!=f"bytes 0-{row['size']-1}/{row['size']}":
                    raise ValueError('Incomplete range or different product length')
                with NamedTemporaryFile(dir=dest,prefix=obs+'.',suffix='.partial',delete=False) as handle:
                    tmp=Path(handle.name)
                    copy_verified(stream,row,handle)
                    handle.flush()
                    os.fsync(handle.fileno())
            os.link(tmp,out)
            return dict(obs=obs, origin='MAST')
        except (OSError, ValueError) as exc:
            error=exc
        finally:
            if tmp is not None:
                tmp.unlink(missing_ok=True)
    raise RuntimeError(f'{obs} restore failed') from error

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest',type=Path)
    parser.add_argument('destination',type=Path)
    parser.add_argument('--offline',action='store_true')
    args=parser.parse_args()
    rows=parse_manifest(args.manifest)
    args.destination.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        result=list(pool.map(lambda row:restore(row,args.destination,args.offline),rows))
    print(json.dumps(dict(manifestSha256=PIN,verified=len(result),results=result,scientificClosures=0)))

if __name__=='__main__':
    main()
