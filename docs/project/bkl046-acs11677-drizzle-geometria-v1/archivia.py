from hashlib import file_digest
import json
from pathlib import Path
import shutil
from zipfile import ZipFile, ZIP_STORED

folder = Path(__file__).resolve().parent
out_root = Path(r'U:\coordinatore-r4-bkl046')

def sha(path):
    with path.open('rb') as stream:
        return file_digest(stream,'sha256').hexdigest()

binding_path = folder / 'binding.json'
binding = json.loads(binding_path.read_bytes())
sources = {row['name']: row['sha256'] for row in binding['references'].values()}
sources['stwcs-1.7.7-py3-none-any.whl'] = binding['wheelSha256']
for file in ('binding.json', 'verifica-geometria.py', 'README.md', 'archivia.py'):
    sources[file] = sha(folder / file)

archive = folder / 'geometria-acs11677.zip'
with ZipFile(archive, 'x', compression=ZIP_STORED) as z:
    for name in sorted(sources):
        z.write(folder / name, name)
digest = sha(archive)
destination = out_root / f'DSG-Shared-BKL046-ACS11677-drizzle-geometria-{digest[:12]}'
destination.mkdir()
partial = destination / (archive.name + '.partial')
shutil.copyfile(archive, partial)
if sha(partial) != digest:
    raise ValueError('Hash differs on physical H')
with ZipFile(partial) as z:
    if sorted(z.namelist()) != sorted(sources):
        raise ValueError('Archive contents differ')
    for name, expected in sources.items():
        with z.open(name) as stream:
            if file_digest(stream,'sha256').hexdigest() != expected:
                raise ValueError(f'Entry differs: {name}')
result = destination / archive.name
partial.rename(result)
receipt = dict(archiveSha256=digest, itemsVerified=len(sources), bytes=archive.stat().st_size,
               localPath=str(archive), physicalHPath=str(result), bindingSha256=sources['binding.json'])
data = json.dumps(receipt, indent=2, sort_keys=True) + '\n'
for part in (folder, destination):
    with (part / 'custodia.json').open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(data)
print(data, flush=True)
