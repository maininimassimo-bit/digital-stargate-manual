import ast
from hashlib import file_digest, sha256
from importlib.metadata import version
import json
import logging
from pathlib import Path
import shutil
import sys
from urllib.request import urlopen
from zipfile import ZipFile

sys.path.insert(0, r'O:\BKL046-ACS-WFC-runtime-7.2.0')
from astropy.io import fits
import numpy as np

base = Path(__file__).resolve().parent
inputs = Path(r'O:\BKL046-ACS11677-drizzle-ingressi-v1')
provenance = Path(r'O:\BKL046-ACS11677-drizzle-provenienza-v1')
bit = 4096

def require(ok, text):
    if not ok:
        raise ValueError(text)

def digest(path):
    with path.open('rb') as stream:
        return file_digest(stream, 'sha256').hexdigest()

def save(name, value):
    with (base / name).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')

def package_source(wheel):
    with ZipFile(wheel) as archive:
        sources = {n: archive.read('drizzlepac/' + n)
                   for n in ('resetbits.py', 'drizCR.py', 'processInput.py')}
    tree = ast.parse(sources['resetbits.py'])
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'reset_dq_bits']
    require(len(functions) == 1, 'Expected exactly one upstream function')
    return sources, compile(ast.Module(body=functions, type_ignores=[]), 'DrizzlePac-3.11.0/resetbits.py', 'exec')

def trailer_parameters(trailer):
    start, end = 8156, 8460
    result = []
    with fits.open(trailer) as hdus:
        lines = hdus[1].data['TEXT_FILE']
        require('jb6v01010_pipeline_flc_asn.fits' in lines[start-1], 'Wrong run')
        for line_number in range(start, end + 1):
            line = lines[line_number-1]
            prefix = '[INFO    ] \t'
            if line.startswith(prefix) and ' :' in line[len(prefix):]:
                key, raw = line[len(prefix):].split(' :', 1)
                result.append(dict(line=line_number, key=key.strip(), value=raw.strip()))
    conditions = {'crbit': '4096', 'resetbits': '4096', 'updatewcs': 'False', 'wcskey': '',
                  'mdriztab':'True', 'driz_cr':'True', 'driz_cr_corr':'False'}
    for key, expected in conditions.items():
        found = {row['value'] for row in result if row['key'] == key}
        # crbit can legitimately be None in the separate drizzle stage.
        require(expected in found and (len(found) == 1 or (key == 'crbit' and found == {expected,'None'})),
                f'Unexpected {key}: {found}')
    return result

def test_reset(source, scratch, action, expected_sha):
    require(digest(source) == expected_sha, f'Input drift: {source.name}')
    shutil.copyfile(source, scratch)
    require(digest(scratch) == expected_sha, f'Scratch copy drift: {source.name}')
    action(str(scratch), 0, extver=[1,2])
    counts = []
    with fits.open(source, memmap=False) as original, fits.open(scratch, memmap=False) as keep:
        for ext in (1,2):
            require(np.array_equal(original['DQ', ext].data, keep['DQ', ext].data),
                    f'Reset 0 changed values: {source.name} ext {ext}')
    action(str(scratch), bit, extver=[1,2])
    with fits.open(source, memmap=False) as original, fits.open(scratch, memmap=False) as reset:
        for ext in (1,2):
            a, b = (x['DQ', ext].data.astype(np.uint16) for x in (original, reset))
            former = int(np.count_nonzero(a & bit))
            current = int(np.count_nonzero(b & bit))
            other = int(np.count_nonzero((a ^ b) & np.uint16(0xFFFF ^ bit)))
            require(current == 0 and other == 0 and int(np.count_nonzero(a != b)) == former,
                    f'Reset semantics differ: {source.name} ext {ext}')
            for kind in ('SCI', 'ERR'):
                payloads = [x[kind, ext].data.tobytes() for x in (original, reset)]
                require(payloads[0] == payloads[1], f'{kind} changed for {source.name} ext {ext}')
            counts.append(dict(extension=ext, chip=original['SCI',ext].header['CCDCHIP'], before=former,
                               reset0=former, after4096=current, otherDqBitsChanged=other))
    require(digest(source) == expected_sha, f'Archived FLC was modified: {source.name}')
    return dict(file=source.name, originalSha256=expected_sha, resetCopySha256=digest(scratch), results=counts)

def main():
    manifest = inputs / 'manifest.json'
    require(digest(manifest) == 'cf50443b5e475e0337da90334176ed97e61f603dc27a5397ab24e74a3ad7c5cb',
            'Wrong inputs manifest')
    data = json.loads(manifest.read_bytes())
    wheel = inputs / data['pypi']['python312LinuxWheel']
    require(digest(wheel) == data['pypi']['wheelSha256'], 'Wrong DrizzlePac wheel')
    sources, function = package_source(wheel)
    trailer = provenance / 'jb6v01010_trl.fits'
    require(digest(trailer) == 'b39d93ff19af1b6de4e9cc37e2759400d44fee37dcde66f85413faeceef97c6d', 'Wrong trailer')
    tools = base / 'stsci_tools-4.3.1-py3-none-any.whl'
    expected = '1c46a155ae344a881ec5235d528beb7ba141fc726661a56efc1363d8c37f20a3'
    if not tools.exists():
        with urlopen('https://pypi.org/pypi/stsci-tools/4.3.1/json',timeout=20) as response:
            release = json.load(response)
        item = next(i for i in release['urls'] if i['filename'] == tools.name)
        require(item['digests']['sha256'] == expected, 'Unexpected PyPI digest')
        with urlopen(item['url'],timeout=20) as response:
            binary = response.read()
        require(sha256(binary).hexdigest() == expected, 'STSci wheel digest differs')
        with tools.open('xb') as stream:
            stream.write(binary)
    require(digest(tools) == expected, 'Unexpected STSci wheel')
    dependencies = base / 'dependencies'
    dependencies.mkdir(exist_ok=True)
    with ZipFile(tools) as archive:
        archive.extractall(dependencies)
    sys.path.insert(0, str(dependencies))
    from stsci.tools import parseinput, stpyfits
    from stsci.tools.bitmask import interpret_bit_flags
    namespace = dict(fits=stpyfits, parseinput=parseinput, interpret_bit_flags=interpret_bit_flags,
                     log=logging.getLogger('BKL046.reset_dq_bits'))
    exec(function, namespace)
    report = []
    scratch = base / 'working-copies'
    scratch.mkdir()
    for item in data['data']:
        source = inputs/'flc'/item['file']
        report.append(test_reset(source, scratch/source.name, namespace['reset_dq_bits'], item['sha256']))
        print(item['file'], [(r['chip'],r['before']) for r in report[-1]['results']], flush=True)
    save('parametri-trailer.json', dict(trailerSha256=digest(trailer), firstLine=8156, lastLine=8460,
                                       parameters=trailer_parameters(trailer)))
    save('riscontro-reset.json', dict(files=report, inputManifestSha256=digest(manifest),
                                     drizzlepacWheelSha256=digest(wheel), toolsWheelSha256=expected,
                                     sourceSha256={n:sha256(s).hexdigest() for n,s in sources.items()},
                                     python=sys.version.split()[0], numpy=np.__version__,
                                     astropy=version('astropy'), method='Exact upstream reset_dq_bits function, loaded from pinned wheel',
                                     astroDrizzlePipelineExecuted=False, pixInsightStarted=False))
    print(sum(r['before'] for item in report for r in item['results']), flush=True)

if __name__ == '__main__':
    main()
