
from hashlib import file_digest
from pathlib import Path
from zipfile import ZipFile,ZIP_STORED
import json
import shutil

home=Path(__file__).resolve().parent
ten=Path(r'O:\BKL046-ACS11677-epsf-10s-v1')
repeat=Path(r'O:\BKL046-ACS11677-epsf-repeat-40s-v1')
def sha(p):
    with p.open('rb') as f:return file_digest(f,'sha256').hexdigest()
def read(p):return json.loads(p.read_bytes())
names={'README.md':home/'README.md','archivia.py':home/'archivia.py'}
specs=(
 ('ten',ten,'j9dw06xoq',('standard-sm3.json','STDPSF_ACSWFC_F606W_SM3.fits','headerlet.json','acquisisci-flc.py')),
 ('repeat',repeat,'jbb502ijq',('verifica-epsf-dq.py','riscontro-epsf-dq.json','riscontro-ripetibilita-dq.json','confronta-dq.py')),
)
for label,folder,target,extra in specs:
    geo=read(folder/'riscontro-epsf.json')
    dates=read(folder/'protocollo-epsf.json')
    if (geo['target']!=target or geo['targetSha256']!=sha(folder/(target+'_flc.fits'))
        or geo['protocolSha256']!=sha(folder/'protocollo-epsf.json')
        or dates['targetHeaderletSha256']!=sha(folder/(target+'_flt_hlet.fits'))
        or geo['scientificClosure'] or geo['independentFluxMeasured']):
        raise ValueError('Unexpected geometric control or pinned objects')
    for n in ('verifica-epsf.py','riscontro-epsf.json','protocollo-epsf.json','flc-metadati.json',target+'_flc.fits',
              target+'_flt_hlet.fits',target+'-acquisizione.json',*extra):
        names[label+'/'+n]=folder/n
pair=read(repeat/'riscontro-ripetibilita-dq.json')
if (pair['eligibleForStellarFlux'] or pair['commonQualifiedFootprints']!=276
    or pair['measuredFiles'][1]['sha256']!=sha(repeat/'riscontro-epsf-dq.json')):
    raise ValueError('Repeat DQ binding differs')
pins={n:sha(p) for n,p in names.items()}
out=home/'acs11677-epsf-10s-e-ripetizione-40s.zip'
with ZipFile(out,'x',compression=ZIP_STORED) as z:
    for n,p in names.items():z.write(p,n)
digest=sha(out)
h=Path(r'U:\coordinatore-r4-bkl046')/f'DSG-Shared-BKL046-ACS11677-epsf-estensione-{digest[:12]}'
h.mkdir()
partial=h/(out.name+'.partial')
shutil.copyfile(out,partial)
if sha(partial)!=digest:raise ValueError('Physical H archive differs')
for p in (out,partial):
    with ZipFile(p) as z:
        if sorted(z.namelist())!=sorted(pins):raise ValueError('Archive membership changed')
        for n,pin in pins.items():
            with z.open(n) as f:
                if file_digest(f,'sha256').hexdigest()!=pin:raise ValueError('Member changed '+n)
final=h/out.name
partial.rename(final)
receipt=dict(archiveSha256=digest,entriesVerified=len(pins),bytes=out.stat().st_size,localPath=str(out),
             physicalHPath=str(final),tenSecondsSha256=pins['ten/riscontro-epsf.json'],
             sameVisitReplaySha256=pins['repeat/riscontro-epsf.json'],dqRepeatabilitySha256=pins['repeat/riscontro-ripetibilita-dq.json'],
             scienceClosure=False)
data=json.dumps(receipt,indent=2).encode()+b'\n'
for folder in (home,h):
    p=folder/'custodia.json'
    with p.open('xb') as f:f.write(data)
    if p.read_bytes()!=data:raise ValueError('Receipt differs')
print(json.dumps(receipt))
