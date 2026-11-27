from hashlib import file_digest
import json
from pathlib import Path
import sys

base=Path(__file__).resolve().parent
inputs=Path(r'O:\BKL046-ACS11677-drizzle-ingressi-v1')
geometry=Path(r'O:\BKL046-ACS11677-drizzle-geometria-verificata-v1')
control=Path(r'O:\BKL046-ACS11677-drizzle-control-v1')
library=base/'pycdlib-1.22.0-py3-none-any.whl'

def sha(path):
    with path.open('rb') as stream:
        return file_digest(stream,'sha256').hexdigest()

def check(ok, reason):
    if not ok: raise ValueError(reason)

check(sha(library)=='bfa0b3631345a14b2741fe088398b6b8dc2838442ea607fd07d027dcc67b9e94','pycdlib wheel changed')
sys.path.insert(0,str(library))
import pycdlib

manifest=inputs/'manifest.json'
binding=geometry/'binding.json'
parameters=control/'parametri-trailer.json'
wheel_self=base/'wheel-cp313.json'
drizzle=json.loads(wheel_self.read_bytes())
entries=[
    ('meta',manifest,'cf50443b5e475e0337da90334176ed97e61f603dc27a5397ab24e74a3ad7c5cb'),
    ('meta',binding,'0f2cc9d954c837c297de2b719312828b1c37d79a90d67a2b8069764b1ec1e191'),
    ('meta',parameters,'bf88c8f86ca42424889ef9feb2247e2385e3cec1fd00c94e9f4f254d98c297ef'),
    ('wheel',base/drizzle['cp313File'],drizzle['cp313Sha256']),
]
for row in json.loads(manifest.read_bytes())['data']:
    entries.append(('flc',inputs/'flc'/row['file'],row['sha256']))
for row in json.loads(binding.read_bytes())['references'].values():
    entries.append(('jref',geometry/row['name'],row['sha256']))
target=base/'acs11677-input-only.iso'
check(not target.exists(),'ISO already exists')
staged=target.with_suffix('.partial')
iso=pycdlib.PyCdlib()
iso.new(interchange_level=3,vol_ident='ACS11677',rock_ridge='1.09')
for folder in ('meta','flc','jref','wheel'):
    iso.add_directory(iso_path=f'/{folder.upper()}',rr_name=folder)
for i,(folder,file,digest) in enumerate(entries,1):
    check(sha(file)==digest,f'Source drift: {file.name}')
    iso.add_file(str(file),iso_path=f'/{folder.upper()}/F{i:03d}.BIN;1',rr_name=file.name)
iso.write(str(staged))
iso.close()
iso.open(str(staged))
results=[]
for folder,file,digest in entries:
    path=f'/{folder}/{file.name}'
    with iso.open_file_from_iso(rr_path=path) as stream:
        check(file_digest(stream,'sha256').hexdigest()==digest,f'ISO drift: {path}')
    results.append(dict(path=path,sha256=digest))
iso.close()
staged.rename(target)
with (base/'iso-ingressi.json').open('x',encoding='utf-8',newline='\n') as stream:
    json.dump(dict(iso=target.name,sha256=sha(target),bytes=target.stat().st_size,
                   entriesVerified=len(results),inputs=results),stream,indent=2,sort_keys=True)
    stream.write('\n')
print(target,len(results),target.stat().st_size,sha(target),flush=True)
