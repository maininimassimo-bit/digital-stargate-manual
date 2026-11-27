from hashlib import file_digest
import json
from pathlib import Path
from shutil import copyfile
from zipfile import ZipFile, ZIP_STORED

root = Path(__file__).resolve().parent
names = ('README.md', 'verifica-reset.py', 'riscontro-reset.json', 'parametri-trailer.json',
         'stsci_tools-4.3.1-py3-none-any.whl', 'archivia.py')

def digest(path):
    with path.open('rb') as stream:
        return file_digest(stream, 'sha256').hexdigest()

checks = {name: digest(root / name) for name in names}
archive = root / 'controllo-reset-4096.zip'
with ZipFile(archive, 'x', compression=ZIP_STORED) as z:
    for name in names:
        z.write(root / name, name)
sha = digest(archive)
out = Path(r'U:\coordinatore-r4-bkl046') / f'DSG-Shared-BKL046-ACS11677-drizzle-reset-{sha[:12]}'
out.mkdir()
temporary = out / (archive.name + '.partial')
copyfile(archive, temporary)
if digest(temporary) != sha:
    raise ValueError('Physical H readback failed')
with ZipFile(temporary) as z:
    if sorted(z.namelist()) != sorted(names):
        raise ValueError('Archive contents differ')
    for name in names:
        with z.open(name) as stream:
            if file_digest(stream,'sha256').hexdigest() != checks[name]:
                raise ValueError(f'Archive entry drift: {name}')
final = out / archive.name
temporary.rename(final)
receipt = dict(archiveSha256=sha, filesVerified=len(names), output=checks, localPath=str(archive),
               physicalHPath=str(final), workingCopiesArchived=False)
for folder in (root, out):
    with (folder / 'custodia.json').open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(receipt,stream,indent=2,sort_keys=True)
        stream.write('\n')
if digest(root/'custodia.json') != digest(out/'custodia.json'):
    raise ValueError('Receipt readback failed')
print(json.dumps(receipt))
