from hashlib import file_digest
import json
from pathlib import Path

def sha(path):
    with path.open('rb') as stream:
        return file_digest(stream, 'sha256').hexdigest()

science=Path('/mnt/science')
wheels=Path('/mnt/wheels')
for desc in json.loads(Path('iso-ingressi.json').read_bytes())['inputs']:
    relative=Path(desc['path'].lstrip('/'))
    if '..' in relative.parts or sha(science/relative)!=desc['sha256']:
        raise ValueError('Scientific ISO drift: '+desc['path'])
rows=json.loads((wheels/'wheels.json').read_bytes())['rows']
for row in rows:
    path=wheels/'wheelhouse'/row['file']
    if row['file']!=path.name or sha(path)!=row['sha256'] or path.stat().st_size!=row['bytes']:
        raise ValueError('Wheel ISO drift: '+row['file'])
print('BKL046_MEDIA_OK',len(rows),flush=True)
