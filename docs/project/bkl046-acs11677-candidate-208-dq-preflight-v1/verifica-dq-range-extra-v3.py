
from concurrent.futures import ThreadPoolExecutor
from math import prod
from pathlib import Path
from urllib.request import Request,urlopen
from hashlib import file_digest,sha256
import json,sys,warnings
sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
from astropy.io import fits
from astropy.wcs import WCS,FITSFixedWarning
import numpy as np

root=Path(r'O:\BKL046-ACS11677-epsf-dither-v1')
src=Path(r'O:\BKL046-ACS11677-gaia-screen-v1')
cross=Path(r'O:\BKL046-ACS11677-epsf-cross-visit-30s-v1')
def sha(p):
    with p.open('rb') as f:return file_digest(f,'sha256').hexdigest()
def read(p):return json.loads(p.read_bytes())
source=Path(r'O:\BKL046-ACS11677-drizzle-ingressi-v1\flc\jb6v01e0q_flc.fits')
anchor=cross/'riscontro-proiezione-picco-dominante-208.json'
if sha(source)!='e6011691a50b2608a3cb91e5f9ceb0957aa4a17e46aa04f8e00bee30df5fdd4d' or sha(anchor)!='dc3011919ce361c5c741d2f4ac2251a0fd94ac61f8e764ca8b8e9152dadb52d6' or not read(anchor)['roundedBackprojectionHitsComponent']:
    raise ValueError('Candidate position inputs were not recognized')
# Exact anchored location from the published dominant-peak report.
pos=read(anchor)['sourceBackprojection']
with fits.open(source,memmap=True) as f:
    sky=WCS(f['SCI',2].header,f).all_pix2world([pos],0,ra_dec_order=True)
products=read(src/'prodotti-risposta.json')['data']
steps={x['root']:x for x in read(src/'acquisizione.json')['headerlets']}
def target_scan(key):
    row=steps[key]
    hlet=src/row['file']
    if sha(hlet)!=row['sha256']:raise ValueError('Headerlet changed')
    with fits.open(hlet) as f:
        h=f['SIPWCS',1].header
        if h['RADESYS']!='ICRS' or h['TG_EVER']!=1:raise ValueError('Unverified target celestial frame')
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',message='The WCS transformation has more axes',category=FITSFixedWarning)
            wcs=WCS(h,f)
        x,y=wcs.all_world2pix(sky,0,tolerance=1e-8,maxiter=70,ra_dec_order=True)[0]
    cx,cy=np.rint([x,y]).astype(int)
    hwidth=17
    if not(hwidth<=cx<4096-hwidth and hwidth<=cy<2048-hwidth):
        raise ValueError('Target DQ search box is outside detector support')
    name=key+'_flc.fits'
    if {r['dataURI'] for r in products if r['productFilename']==name}!={'mast:HST/product/'+name}:
        raise ValueError('Object is not the MAST exposure product')
    url=f'https://stpubdata.s3.amazonaws.com/hst/public/{key[:4]}/{key}/{name}'
    with urlopen(Request(url,method='HEAD'),timeout=25) as req:
        version=req.headers['x-amz-version-id']
        etag=req.headers['ETag']
        size=int(req.headers['Content-Length'])
    version_url=url+'?versionId='+version
    def fetch(start,stop):
        with urlopen(Request(version_url,headers={'Range':f'bytes={start}-{stop-1}'}),timeout=30) as r:
            if (r.status!=206 or r.headers['Content-Range']!=f'bytes {start}-{stop-1}/{size}'
                or r.headers.get('x-amz-version-id')!=version or r.headers.get('ETag')!=etag):
                raise ValueError('Partial object revision differs')
            data=r.read(stop-start+1)
        if len(data)!=stop-start:raise ValueError('Incomplete exact byte range')
        return data
    offset=0
    order=('PRIMARY','SCI','ERR','DQ')
    records=[]
    for expected in order:
        chunks=[]
        for n in range(64):
            start=offset+n*2880
            block=fetch(start,start+2880)
            chunks.append(block)
            if any(block[i:i+80]==b'END'+b' '*77 for i in range(0,2880,80)):
                break
        else:
            raise ValueError('FITS primary or extension header exceeds the bounded block count: '+expected)
        blob=b''.join(chunks)
        pad=len(blob)
        hdr=fits.Header.fromstring(blob[:pad].decode('ascii'),sep='')
        actual=hdr.get('EXTNAME','PRIMARY').strip()
        if actual!=expected or (actual!='PRIMARY' and hdr['EXTVER']!=1):raise ValueError('Unexpected FITS extension order')
        if actual=='SCI' and hdr['CCDCHIP']!=2:raise ValueError('Target DQ detector binding failed')
        if actual=='PRIMARY' and (hdr['ROOTNAME'].lower()!=key or hdr['PROPOSID']!=int(row['candidate']['proposal'])):
            raise ValueError('Actual archival science provenance changed')
        record=dict(name=actual,headerOffset=offset,headerSha256=sha256(blob[:pad]).hexdigest())
        records.append(record)
        offset+=pad
        axes=[hdr[f'NAXIS{i+1}'] for i in range(hdr['NAXIS'])]
        if actual=='DQ':
            if axes!=[4096,2048] or hdr['BITPIX']!=16 or hdr.get('BSCALE',1)!=1 or hdr.get('BZERO',0)!=0:
                raise ValueError('Unexpected detector DQ representation')
            break
        count=(prod(axes) if axes else 0)+hdr.get('PCOUNT',0)
        payload=count*hdr.get('GCOUNT',1)*abs(hdr['BITPIX'])//8
        offset+=(payload+2879)//2880*2880
    first=offset+((cy-hwidth)*4096)*2
    end=offset+((cy+hwidth+1)*4096)*2
    raw=fetch(first,end)
    picture=np.frombuffer(raw,dtype='>i2').reshape(2*hwidth+1,4096)[:,cx-hwidth:cx+hwidth+1]
    yy,xx=np.mgrid[cy-hwidth:cy+hwidth+1,cx-hwidth:cx+hwidth+1]
    stats={}
    for radius in (10,13,16):
        cut=picture[(xx-x)**2+(yy-y)**2<=radius**2]
        stats[str(radius)]=dict(pixels=len(cut),dqNonzero=int(np.count_nonzero(cut)),fullWell=int(np.count_nonzero(cut&256)))
    return dict(root=key,objectVersion=version,etag=etag,detectorXY=[float(x),float(y)],headers=records,
                dqByteRange=[int(first),int(end)-1],dqRangeSha256=sha256(raw).hexdigest(),nominalNeighborhood=stats)

with ThreadPoolExecutor(max_workers=2) as pool:
    targets=list(pool.map(target_scan,('jbbf01hxq','je5v02rhq')))
doc=dict(protocol='BKL046_ACS11677_ARCHIVE_DQ_ONLY_PREFLIGHT_V1',sourcePositionSha256=sha(anchor),
         targetDiagnostics=targets,sciencePixelValuesRead=False,fluxMeasured=False,scientificClosure=False)
payload=json.dumps(doc,indent=2,allow_nan=False).encode()+b'\n'
with (root/'riscontro-dq-range-extra-v3.json').open('xb') as out:out.write(payload)
print([(r['root'],r['nominalNeighborhood']) for r in targets],flush=True)
