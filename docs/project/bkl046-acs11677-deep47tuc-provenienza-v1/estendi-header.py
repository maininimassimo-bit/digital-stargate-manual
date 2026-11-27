
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import sys
root=Path(sys.argv[1])
old=next(r for r in json.loads((root/'acquisizione.json').read_bytes()) if r['file']=='drz-prefix.fits')
head=(root/old['file']).read_bytes()
if sha256(head).hexdigest()!=old['sha256']:
    raise ValueError('Initial archive range changed')
start, stop = len(head), 570240
expected=f'bytes {start}-{stop-1}/437912640'
with urlopen(Request(old['url'],headers={'Range':f'bytes={start}-{stop-1}','If-Match':old['etag']}),timeout=35) as response:
    if response.status!=206 or response.headers.get('ETag')!=old['etag'] or response.headers.get('Content-Range')!=expected:
        raise ValueError('Extended range or provider version changed')
    tail=response.read(stop-start+1)
if len(tail)!=stop-start:
    raise ValueError('Partial extended FITS range')
full=head+tail
end=next((p+80 for p in range(0,len(full),80) if full[p:p+80]==b'END'+b' '*77),None)
if end is None:
    raise ValueError('No complete FITS header in extended range')
size=((end+2879)//2880)*2880
if size!=stop or full[end:size].strip(b' '):
    raise ValueError('Invalid FITS header padding')
path=root/'drz-primary-header.fits'
with path.open('xb') as target:
    target.write(full[:size])
result=dict(file=path.name,headerBytes=size,sha256=sha256(full[:size]).hexdigest(),source=old['url'],
            firstRange=old['contentRange'],secondRange=expected,secondRangeSha256=sha256(tail).hexdigest(),etag=old['etag'])
with (root/'acquisizione-header.json').open('x',encoding='utf-8') as out:
    json.dump(result,out,indent=2)
print(result,flush=True)
