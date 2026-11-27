from base64 import b64encode
from concurrent.futures import ThreadPoolExecutor
from hashlib import md5,sha256
import json
from pathlib import Path
import runpy
import shutil
import sys
from tempfile import TemporaryDirectory
from urllib.request import Request,urlopen

root=Path(__file__).resolve().parent
sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
from astropy.io import fits
crc=runpy.run_path(r'O:\BKL046-ACS11677-Linux-v1\verifica-drc-crc64.py')
object_path='https://stpubdata.s3.amazonaws.com/hst/public/jb6v/jb6v25aaq/jb6v25aaq_flc.fits'
version='iS3AP7LtFm3bRRZAFAIpJli6SD9t1Cu7'
uri=f'{object_path}?versionId={version}'
head={'content-length':'168448320','etag':'"172fa519d4db0eb5cd1b8f58964c3ab2"',
      'x-amz-version-id':version,'x-amz-checksum-type':'FULL_OBJECT','x-amz-checksum-crc64nvme':'AtjFqs473oo='}
size=int(head['content-length'])
chunk=4*1024*1024
def check(ok,msg):
    if not ok:raise ValueError(msg)
with urlopen(Request(uri,method='HEAD',headers={'x-amz-checksum-mode':'ENABLED'}),timeout=25) as response:
    check(response.status==200 and {k:response.headers.get(k) for k in head}==head,'HST object metadata changed')
where=root/'jb6v25aaq_flc.fits'
partial=where.with_suffix('.partial')
with TemporaryDirectory(prefix='hst-ranges-',dir=root) as middle:
    def get(start):
        end=min(start+chunk,size)-1
        temp=Path(middle)/str(start)
        for trial in range(3):
            try:
                req=Request(uri,headers={'Range':f'bytes={start}-{end}'})
                with urlopen(req,timeout=40) as r,temp.open('wb') as out:
                    check(r.status==206 and r.headers.get('Content-Range')==f'bytes {start}-{end}/{size}'
                          and r.headers.get('x-amz-version-id')==version,'Wrong archive data range')
                    shutil.copyfileobj(r,out,length=1048576)
                check(temp.stat().st_size==end-start+1,'Short HST data range')
                return temp
            except OSError:
                if trial==2:raise
        raise RuntimeError(start)
    with ThreadPoolExecutor(max_workers=12) as pool:
        order=list(pool.map(get,range(0,size,chunk)))
    a,b=sha256(),md5(usedforsecurity=False)
    state=crc['word_mask']
    with partial.open('xb') as out:
        for part in order:
            val=part.read_bytes()
            a.update(val)
            b.update(val)
            state=crc['update'](state,val)
            out.write(val)
checksum=b64encode((state^crc['word_mask']).to_bytes(8,'big')).decode('ascii')
check(partial.stat().st_size==size and b.hexdigest()==head['etag'].strip('"')
      and checksum==head['x-amz-checksum-crc64nvme'],'HST full-object integrity failed')
with fits.open(partial,memmap=True) as f:
    f.verify('exception')
    h=f[0].header
    check(h['ROOTNAME'].lower()=='jb6v25aaq' and h['ASN_ID'].lower()=='jb6v25010'
          and h['INSTRUME']=='ACS' and h['DETECTOR']=='WFC' and h['PROPOSID']==11677
          and h['EXPTIME']==100. and 'F606W' in (h['FILTER1'],h['FILTER2']),'Unexpected scientific exposure')
    public=dict(root=h['ROOTNAME'].lower(),association=h['ASN_ID'].lower(),seconds=h['EXPTIME'],
                proposal=h['PROPOSID'],instrument=h['INSTRUME'],detector=h['DETECTOR'],filter='F606W')
partial.rename(where)
with (root/'acquisizione.json').open('x',encoding='utf-8',newline='\n') as out:
    json.dump(dict(file=where.name,sha256=a.hexdigest(),bytes=size,uri=uri,provider=head,science=public),
              out,sort_keys=True,indent=2)
    out.write('\n')
print(where.name,a.hexdigest(),flush=True)
