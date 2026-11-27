import concurrent.futures
import hashlib
import json
import re
import shutil
import urllib.parse
import urllib.request
from pathlib import Path

base = Path(r'O:\BKL046-ACS11677-drizzle-ingressi-v1')
census = Path(r'O:\BKL046-ACS-11677-fotometria-v2\censimento.json')
provenance = Path(r'O:\BKL046-ACS11677-drizzle-provenienza-v1\riscontro.json')
local = {
    'jb6v01dfq': (Path(r'O:\BKL046-ACS-11677-fotometria-v1\source\jb6v01dfq_flc.fits'), 'a330f28eca9e64cba6c8f47e6607d67fbaeb82f2c6165d254b74b82f6be7d938'),
    'jb6v01e0q': (Path(r'O:\BKL046-ACS-11677-fotometria-v2\source\jb6v01e0q_flc.fits'), 'e6011691a50b2608a3cb91e5f9ceb0957aa4a17e46aa04f8e00bee30df5fdd4d'),
    'jb6v01e5q': (Path(r'O:\BKL046-ACS-11677-DQ-replique-v1\jb6v01e5q_flc.fits'), 'de2f1da705be9509d222f98cd68f9e6453b7ff439393b0c1da3b7002584743d1'),
}

def sha(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()

def check(ok, message):
    if not ok:
        raise ValueError(message)

def primary_header(path):
    cards = {}
    with path.open('rb') as handle:
        for _ in range(100):
            block = handle.read(2880)
            check(len(block) == 2880, f'Incomplete FITS header: {path.name}')
            for i in range(0, 2880, 80):
                card = block[i:i+80].decode('ascii')
                key = card[:8].strip()
                if key == 'END':
                    return cards
                if card[8:10] == '= ':
                    value = card[10:].strip()
                    cards[key] = value.split("'")[1].strip() if value.startswith("'") else value.split('/')[0].strip()
    raise ValueError(f'Missing primary header END: {path.name}')

def acquire(row):
    root = row['root']
    spec = row['files']['FLC']
    target = base / 'flc' / spec['leaf']
    pending = target.with_suffix('.partial')
    url = 'https://mast.stsci.edu/api/v0.1/Download/file?' + urllib.parse.urlencode({'uri': spec['uri']})
    if root in local:
        source, expected = local[root]
        shutil.copyfile(source, pending)
    else:
        expected = None
        with urllib.request.urlopen(url, timeout=90) as response, pending.open('xb') as stream:
            check(response.status == 200, f'Unexpected HTTP status for {root}: {response.status}')
            shutil.copyfileobj(response, stream, length=1024*1024)
    check(pending.stat().st_size == spec['bytes'], f'Wrong size for {root}')
    digest = sha(pending)
    check(expected is None or expected == digest, f'Wrong previously pinned hash for {root}')
    fields = primary_header(pending)
    names = ('ROOTNAME', 'ASN_ID', 'TELESCOP', 'INSTRUME', 'DETECTOR', 'FILTER1', 'FILTER2', 'EXPTIME', 'MDRIZTAB')
    header = {name: fields[name] for name in names}
    check([header[k].lower() for k in names[:5]] == [root, row['association'], 'hst', 'acs', 'wfc'], f'Wrong identity for {root}: {header}')
    check(row['band'] in [header['FILTER1'], header['FILTER2']], f'Wrong band for {root}: {header}')
    check(float(header['EXPTIME']) == row['seconds'], f'Wrong exposure for {root}: {header}')
    pending.rename(target)
    print(f'{target.name} {digest}', flush=True)
    return dict(file=target.name, sha256=digest, size=spec['bytes'], mast=url, previousBytePin=expected, header=header)

def main():
    check(sha(census) == 'f767afda06343a0594c5c02189e712298bee355c4bc8829db0587b6edb5cf236', 'Census hash mismatch')
    results = json.loads(provenance.read_bytes())
    inputs = results['productPrimaryHeaderPrefixes']['flc']['inputs']
    ordered = list(dict.fromkeys(x.split('[')[0] for x in inputs))
    rows = {e['files']['FLC']['leaf']: e for e in json.loads(census.read_bytes())['exposures'] if e['association']=='jb6v01010'}
    check(len(ordered) == 6 and len(inputs) == 12 and set(ordered) == set(rows), 'Association mismatch')
    (base / 'flc').mkdir()
    pypi = 'https://pypi.org/pypi/drizzlepac/3.11.0/json'
    with urllib.request.urlopen(pypi, timeout=30) as response:
        pypi_bytes = response.read()
    artifacts = json.loads(pypi_bytes)['urls']
    release = [a for a in artifacts if 'cp312-cp312-manylinux' in a['filename']]
    check(len(release) == 1 and not any(re.search(r'-win(?:32|_)', a['filename']) for a in artifacts), 'Platform availability changed')
    wheel = release[0]
    check(wheel['digests']['sha256'] == 'cd24ee21f2e0fe7dc37c323d5e66aad5ec6ecce488c950506d4a62146e5d4da4', 'Linux wheel hash changed')
    (base / 'pypi-3.11.0.json').write_bytes(pypi_bytes)
    wheel_path = base / wheel['filename']
    with urllib.request.urlopen(wheel['url'], timeout=45) as response, wheel_path.open('xb') as stream:
        shutil.copyfileobj(response, stream, length=1024*1024)
    check(wheel_path.stat().st_size == wheel['size'] and sha(wheel_path) == wheel['digests']['sha256'], 'Downloaded wheel integrity mismatch')
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as workers:
        exposures = list(workers.map(acquire, map(rows.__getitem__, ordered)))
    report = dict(association='jb6v01010', band='F606W', data=exposures,
                  archiveInputCards=inputs, censusSha256=sha(census), provenanceSha256=sha(provenance),
                  pypi=dict(url=pypi, jsonSha256=hashlib.sha256(pypi_bytes).hexdigest(),
                            python312LinuxWheel=wheel_path.name, wheelSha256=sha(wheel_path), windowsWheel=False),
                  astroDrizzleRerun=False, pixInsightStarted=False)
    (base / 'manifest.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
    print('manifest.json', sha(base / 'manifest.json'), flush=True)

if __name__ == '__main__':
    main()
