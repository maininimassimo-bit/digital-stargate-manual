import hashlib
import json
import shutil
import zipfile
from pathlib import Path

base = Path(r'O:\BKL046-ACS11677-drizzle-ingressi-v1')
sources = Path(r'O:\BKL046-ACS11677-drizzle-provenienza-v1')
archive_root = Path(r'U:\coordinatore-r4-bkl046')
census = Path(r'O:\BKL046-ACS-11677-fotometria-v2\censimento.json')

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def require(result, reason):
    if not result:
        raise ValueError(reason)

manifest = base / 'manifest.json'
data = json.loads(manifest.read_bytes())
prior = json.loads((sources / 'riscontro.json').read_bytes())
wheel = base / data['pypi']['python312LinuxWheel']
pypi = base / 'pypi-3.11.0.json'
entries = {
    **{f"flc/{row['file']}": (base / 'flc' / row['file'], row['sha256']) for row in data['data']},
    **{f"provenienza/{name}": (sources / name, sha) for name, sha in prior['downloadedSha256'].items()},
    'provenienza/37g1550cj_mdz.fits': (sources / '37g1550cj_mdz.fits', prior['tableSha256']),
    'provenienza/riscontro.json': (sources / 'riscontro.json', data['provenanceSha256']),
    'provenienza/censimento.json': (census, data['censusSha256']),
    f"runtime/{wheel.name}": (wheel, data['pypi']['wheelSha256']),
    'runtime/pypi-3.11.0.json': (pypi, data['pypi']['jsonSha256']),
}
for name in ('manifest.json', 'prepara.py', 'archivia.py', 'README.md'):
    entries[name] = (base / name, digest(base / name))
archive = base / 'ingressi-acs11677.zip'
with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_STORED) as output:
    for name, (path, _) in sorted(entries.items()):
        output.write(path, name)
archive_sha = digest(archive)
destination = archive_root / f'DSG-Shared-BKL046-ACS11677-drizzle-ingressi-{archive_sha[:12]}'
destination.mkdir()
partial = destination / (archive.name + '.partial')
shutil.copyfile(archive, partial)
require(digest(partial) == archive_sha, 'Archive SHA-256 mismatch on physical H')
with zipfile.ZipFile(partial) as copy:
    require(len(copy.namelist()) == len(entries) and set(copy.namelist()) == set(entries), 'Archive contents differ')
    for name, (_, value) in entries.items():
        with copy.open(name) as stream:
            require(hashlib.file_digest(stream, 'sha256').hexdigest() == value, f'Archive entry changed: {name}')
partial.rename(destination / archive.name)
receipt = dict(archive=archive.name, archiveSha256=archive_sha, archiveBytes=archive.stat().st_size,
               entriesVerified=len(entries), manifestSha256=digest(manifest), localPath=str(archive),
               physicalHPath=str(destination / archive.name), nativeExecutions=0)
encoded = json.dumps(receipt, indent=2, sort_keys=True) + '\n'
for path in (base, destination):
    (path / 'custodia.json').write_text(encoded, encoding='utf-8', newline='\n')
require(digest(base / 'custodia.json') == digest(destination / 'custodia.json'), 'Receipt round-trip failed')
print(encoded, flush=True)
