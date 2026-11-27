
from concurrent.futures import ThreadPoolExecutor
from hashlib import md5,sha256
from pathlib import Path
from urllib.request import Request,urlopen
import json

root=Path(__file__).resolve().parent
rank=Path(r'O:\BKL046-ACS11677-riferimento-esterno-v1\graduatoria-impronte.json')
query=json.loads((root/'prodotti-query.json').read_bytes())
catalog=json.loads((root/'prodotti-risposta.json').read_bytes())
if catalog['status']!='COMPLETE':raise ValueError('Missing product catalogue')
selected=set(map(int,query['params']['obsid'].split(',')))
rows=[r for r in json.loads(rank.read_bytes())['candidates'] if r['obsid'] in selected]
def verify(row):
    exposure=row['root']
    name=exposure+'_flt_hlet.fits'
    p=root/name
    expected='mast:HST/product/'+name
    found={item['dataURI'] for item in catalog['data'] if item['productFilename']==name}
    if not found and not p.exists():
        return dict(candidate=row,status='NO_HEADERLET_LISTED')
    if found!={expected} or not p.is_file():
        raise ValueError(f'MAST and archive disagree on {name}')
    uri=f'https://stpubdata.s3.amazonaws.com/hst/public/{exposure[:4]}/{exposure}/{name}'
    with urlopen(Request(uri,method='HEAD',headers={'x-amz-checksum-mode':'ENABLED'}),timeout=25) as f:
        length=int(f.headers['Content-Length'])
        version=f.headers.get('x-amz-version-id')
        etag=f.headers['ETag'].strip('"')
    d=p.read_bytes()
    if len(d)!=length or not version or md5(d,usedforsecurity=False).hexdigest()!=etag:
        raise ValueError(f'Unexpected headerlet identity {exposure}')
    return dict(file=name,root=exposure,bytes=length,version=version,etag=etag,sha256=sha256(d).hexdigest(),
                uri=uri,mastUri=expected,candidate=row,status='VERIFIED')
with ThreadPoolExecutor(max_workers=8) as pool:
    all_rows=list(pool.map(verify,rows))
doc=dict(parentRankingSha256=sha256(rank.read_bytes()).hexdigest(),
         headerlets=[r for r in all_rows if r['status']=='VERIFIED'],
         missing=[r for r in all_rows if r['status']!='VERIFIED'])
with (root/'acquisizione.json').open('x',encoding='utf-8') as out:json.dump(doc,out,indent=2)
print(len(doc['headerlets']),len(doc['missing']),flush=True)
