
import json
import re
from collections import defaultdict
from hashlib import file_digest
from pathlib import Path
import sys

base=Path(__file__).resolve().parent
sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
from astropy.io.fits import Header
from astropy.wcs import WCS
import numpy as np

receipts={r['file']:r for r in json.loads((base/'acquisizione.json').read_bytes())}
wanted={
    'readme.txt':'f13cf79a3652ad9f4131307827e0b92b79a232f8a01b76a9bb184e1baaea5b87',
    'catalog.txt':'bcedbc057f9fc1a1dd0fb6d7c02a80a48c04ece8be041ef2ef90748f78d7a943',
    'drz-prefix.fits':'40f8d6a6ab72ea0925789761a1a967bf0fd833d5a2eecd842cd8827ec9c4ba29',
}
for n,pin in wanted.items():
    record=receipts[n]
    path=base/n
    with path.open('rb') as f:
        found=file_digest(f,'sha256').hexdigest()
    if found!=record['sha256'] or found!=pin or path.stat().st_size!=record['bytes']:
        raise ValueError('Product hash or length changed: '+n)

extended=json.loads((base/'acquisizione-header.json').read_bytes())
data=(base/extended['file']).read_bytes()
with (base/extended['file']).open('rb') as f:
    exact_header_hash=file_digest(f,'sha256').hexdigest()
if exact_header_hash!=extended['sha256'] or len(data)!=extended['headerBytes'] or not data.startswith((base/'drz-prefix.fits').read_bytes()):
    raise ValueError('Extended FITS header does not match its receipt')

end=next(pos+80 for pos in range(0,len(data),80) if data[pos:pos+80]==b'END'+b' '*77)
header_stop=((end+2879)//2880)*2880
if not data.startswith(b'SIMPLE  ') or data[end:header_stop].strip(b' ') or header_stop!=len(data):
    raise ValueError('Incomplete or invalid primary FITS header')
h=Header.fromstring(data[:header_stop].decode('ascii'),sep='')
if h['PROPOSID']!=11677 or 'F606W' not in (h['FILTER1'],h['FILTER2']):
    raise ValueError('FITS science provenance changed')
catalog=(base/'catalog.txt')
with catalog.open(encoding='ascii') as handle:
    columns=handle.readline().strip()
if columns.split()!=['#','ID','X','Y','F606W','error','F814W','error','Chi','Sharp']:
    raise ValueError('Unexpected catalogue column declaration')
rows=np.loadtxt(catalog,dtype=float,comments='#',ndmin=2)
if rows.shape[1]!=9 or not np.isfinite(rows).all() or len(np.unique(rows[:,0]))!=len(rows):
    raise ValueError('Malformed source catalogue')
if not np.equal(rows[:,0],np.trunc(rows[:,0])).all():
    raise ValueError('Source IDs are not integers')
wcs=WCS(h)
def extent(a):
    return [float(a.min()),float(a.max())]
names=('jb6v01dfq','jb6v01diq','jb6v01dkq','jb6v01e0q','jb6v01e5q','jb6v01ekq')
drizzle={}
for card in h.cards:
    if not re.fullmatch(r'D\d{3}DATA',card.keyword):
        continue
    if card.keyword in drizzle:
        raise ValueError('Duplicate drizzle context keyword')
    match=re.fullmatch(r'([a-z0-9]{9})_flt[.]fits\[sci,([12])\]',str(card.value).lower())
    if match is None:
        raise ValueError('Unexpected drizzle source identity for '+card.keyword)
    drizzle[card.keyword]=match.groups()
by_root=defaultdict(set)
for raw,extension in drizzle.values():
    by_root[raw].add(extension)
if (len(drizzle)!=h['NDRIZIM'] or len(drizzle)!=2*len(by_root)
        or any(extensions!={'1','2'} for extensions in by_root.values())):
    raise ValueError('Drizzle context is incomplete')
overlap=sorted(set(names)&set(by_root))
if len(overlap)!=5:
    raise ValueError('Unexpected overlap with the six frozen AstroDrizzle inputs')
result=dict(
    source='https://archive.stsci.edu/prepds/deep47tuc/',
    acquisitionSha256=wanted, primaryHeaderBytes=header_stop, primaryProposalId=h['PROPOSID'],
    hasCelestialWcs=bool(wcs.has_celestial), primaryAxes=[h['NAXIS1'],h['NAXIS2']],
    drizzleInputChipEntries=len(drizzle),drizzleInputExposureRoots=len(by_root),
    checkedAssociationRoots=list(names),sharedRawExposureRoots=overlap,
    sharedContext=[dict(keyword=k,root=r,scienceExtension=int(e))
                   for k,(r,e) in drizzle.items() if r in overlap],
    sameObservingProgram=True, exactHeaderSha256=exact_header_hash,
    completeContextVerified=True,
    catalog=dict(rows=len(rows),columns=columns[1:].split(),xExtent=extent(rows[:,1]),yExtent=extent(rows[:,2]),
                 f606wMagnitudeRange=extent(rows[:,3]),f606wErrorRange=extent(rows[:,4])),
    crossmatchPerformed=False, independentFluxReferenceEstablished=False, scientificClosure=False,
)
with (base/'riscontro-deep47tuc-contesto.json').open('x',encoding='utf-8',newline='\n') as f:
    json.dump(result,f,indent=2,allow_nan=False)
    f.write('\n')
print(json.dumps(result))
