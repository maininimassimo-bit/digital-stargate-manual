
from hashlib import file_digest
from pathlib import Path
from zipfile import ZipFile
import json
import shutil
import subprocess
import sys

b=Path(__file__).resolve().parent
r=b/'replay-completo'
h=Path(r'U:\coordinatore-r4-bkl046')
store=r/'store'
out=r/'trial'
out.mkdir()
def sha(p):
    with p.open('rb') as f:return file_digest(f,'sha256').hexdigest()
def restore(origin,member,path):
    if member is None:
        with origin.open('rb') as src,path.open('xb') as dest:shutil.copyfileobj(src,dest)
    else:
        with ZipFile(origin) as z,z.open(member) as src,path.open('xb') as dest:shutil.copyfileobj(src,dest)
    return dict(origin=origin.name,member=member,sha256=sha(path),bytes=path.stat().st_size)
def read(p):return json.loads(p.read_bytes())
keeper=read(b/'custodia-screen.json')
matrix={
    'main':(Path(keeper['physicalHPath']),keeper['archiveSha256']),
    'ingress':(h/'DSG-Shared-BKL046-ACS11677-drizzle-ingressi-200401814b6f'/'ingressi-acs11677.zip',
        '200401814b6f5de8a2f25aeb293b7846af2a157cc7267fead3b1b2f6116662d5'),
    'shape':(h/'DSG-Shared-BKL046-ACS11677-geometria-lunghe-b7b11e313d4c'/'archivio.zip',
        'b7b11e313d4c723b2bdd4f724bb9f70eac583c8191210ed230281a23b23f20c7'),
    'case':(h/'DSG-Shared-BKL046-ACS11677-scie-DQ-fa099f18a7d4'/'archivio.zip',
        'fa099f18a7d484e185ec3ffe0a7d81b221e5801c778b31151e05784eaa15c300')}
for p,expected in matrix.values():
    if sha(p)!=expected:raise ValueError('Retained archive changed '+p.name)
members={
    'trial/verifica-go14949.py':('main','verifica-go14949.py'),
    'trial/protocollo-go14949.json':('main','protocollo-go14949.json'),
    'trial/jdg302ctq_flc.fits':('main','jdg302ctq_flc.fits'),
    'trial/jdg302cvq_flc.fits':('main','jdg302cvq_flc.fits'),
    'store/BKL046-ACS11677-drizzle-ingressi-v1/flc/jb6v01e0q_flc.fits':('ingress','flc/jb6v01e0q_flc.fits'),
    'store/BKL046-ACS-11677-geometria-lunghe-v1/protocollo.json':('shape','protocollo.json'),
    'store/BKL046-ACS-11677-geometria-lunghe-v1/verifica.py':('shape','verifica.py'),
    'store/BKL046-ACS-11677-scie-DQ-v1/protocollo.json':('case','protocollo.json'),
    'store/BKL046-ACS-11677-scie-DQ-v1/riscontro.json':('case','riscontro.json'),
    'store/BKL046-ACS-11677-scie-DQ-v1/verifica.py':('case','verifica.py'),
}
pins={}
for n,(key,member) in members.items():
    p=r/n
    p.parent.mkdir(parents=True,exist_ok=True)
    pins[n]=dict(restore(matrix[key][0],member,p),retainedArchive=key,sourceClass='H_ARCHIVE')
local=Path(r'O:\BKL046-GO14949-nuovo-puntamento-v1')
recovered={
    'store/BKL046-GO14949-registrazione-profondita-v1/transfer.py':(
        h/'DSG-Shared-BKL046-GO14949-crociati-54d8fb400281'/'transfer.py',
        '1539c0aa0322b8d3fcf04dec1fafb11d9ab42fdd678dc8d34b5c8ec7b68e8de1','H_STANDALONE'),
    'store/BKL046-GO14949-nuovo-puntamento-v1/protocollo.json':(local/'protocollo.json',
        '1271eaa79ea206c1da5f23fc2ddb3f5f5d53636c41a710f47e8e58a72a8ff7db','PINNED_VM_AUXILIARY'),
    'store/BKL046-GO14949-nuovo-puntamento-v1/check_new_pointing.py':(local/'check_new_pointing.py',
        '28f69e280b3df1e9ce0d7ffd9019739477add1a2561d9d4f7863cd41ebd63edc','PINNED_VM_AUXILIARY'),
    'store/BKL046-ACS11677-riferimento-esterno-v1/verifica-candidato-frame-v2.py':(r/'verifica-candidato-frame-v2.py',
        '2f72a51e7a9a28c44a81f41d9fb8bff2d62ffb495a7fe513ffb1a79637b1a98a','GITHUB_READBACK')}
for rel,(source,expected,kind) in recovered.items():
    p=r/rel
    p.parent.mkdir(parents=True,exist_ok=True)
    if sha(source)!=expected:raise ValueError('Pinned helper changed '+source.name)
    pins[rel]=dict(restore(source,None,p),sourceClass=kind)
    if pins[rel]['sha256']!=expected:raise ValueError('Restored helper changed')
prior=(out/'verifica-go14949.py').read_text()
replacements={
    "base=Path('O:/')":"base=Path(__file__).resolve().parent.parent/'store'",
    "str(base/'BKL046-ACS-WFC-runtime-7.2.0')":r"r'O:\BKL046-ACS-WFC-runtime-7.2.0'",
    "earlier/name":"root/name",
}
subject=prior
for old,new in replacements.items():
    if subject.count(old)!=1:raise ValueError('A scoped replay edit was ambiguous')
    subject=subject.replace(old,new)
exe=out/'verifica-copia-ripristinata.py'
with exe.open('x',encoding='utf-8',newline='\n') as f:f.write(subject)
subprocess.run([sys.executable,'-I','-B',str(exe)],check=True,cwd=out)
outputs=['go14949-jdg302ctq.json','go14949-jdg302cvq.json','go14949-sintesi.json']
with ZipFile(matrix['main'][0]) as z:
    actual={}
    for leaf in outputs:
        with z.open(leaf) as f:original=file_digest(f,'sha256').hexdigest()
        if sha(out/leaf)!=original:raise ValueError('Recovered run differs for '+leaf)
        actual[leaf]=original
sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
import astropy,numpy
report=dict(archives={k:v[1] for k,v in matrix.items()},artifacts=pins,transportOnlyChanges=replacements,
    githubHelperCommit='92659b33fe543b7ea590c2454e9bb5f36eb589ab',
    executedVerifierSha256=sha(exe),byteIdenticalOutputs=actual,scientificClosure=False,
    runtimeStillInstalled=dict(python=sys.version.split()[0],astropy=astropy.__version__,numpy=numpy.__version__))
with (b/'replay-completo-go14949.json').open('x',encoding='utf-8',newline='\n') as f:
    json.dump(report,f,indent=2,sort_keys=True)
    f.write('\n')
print(len(pins),len(actual),sha(b/'replay-completo-go14949.json'),flush=True)
