from concurrent.futures import ThreadPoolExecutor
from hashlib import file_digest,sha256
import json
from pathlib import Path
from zipfile import ZipFile
import shutil
import sys
from urllib.request import urlopen

sys.path.insert(0, r'O:\BKL046-ACS-WFC-runtime-7.2.0')
from astropy.io import fits
import numpy as np
import astropy

here = Path(__file__).resolve().parent
inputs = Path(r'O:\BKL046-ACS11677-drizzle-ingressi-v1')
prior = Path(r'O:\BKL046-ACS11677-drizzle-provenienza-v1')
reference_names = {
    'IDCTAB': ('4bb1536cj_idc.fits', 285120),
    'NPOLFILE': ('4bb1536ej_npl.fits', 51840),
    'D2IMFILE': ('4bb15371j_d2i.fits', 51840),
    'DGEOFILE': ('qbu16424j_dxy.fits', 134308800),
    'MDRIZTAB': ('37g1550cj_mdz.fits', 247680),
}

def require(ok, why):
    if not ok:
        raise ValueError(why)

def digest(path):
    with path.open('rb') as stream:
        return file_digest(stream, 'sha256').hexdigest()

def acquire(item):
    key, (name, length) = item
    url = 'https://hst-crds.stsci.edu/unchecked_get/references/hst/' + name
    target = here / name
    if not target.exists():
        tmp = target.with_suffix('.partial')
        with urlopen(url, timeout=75) as response, tmp.open('xb') as stream:
            require(response.status == 200, f'{name}: expected complete HTTP response')
            shutil.copyfileobj(response, stream, length=1048576)
        require(tmp.stat().st_size == length, f'{name}: size differs')
        tmp.rename(target)
    require(target.stat().st_size == length, f'{name}: size differs')
    with fits.open(target, memmap=True) as hdus:
        hdus.verify('exception')
        meta = dict(instrument=hdus[0].header.get('INSTRUME'),
                    filetype=hdus[0].header.get('FILETYPE'),
                    hdus=[dict(name=h.name, version=h.ver,
                               chip=h.header.get('CCDCHIP'),
                               axis=h.header.get('AXISCORR',h.header.get('EXTNAME')))
                          for h in hdus])
    require(meta['instrument'] == 'ACS', f'{name}: wrong instrument')
    return key, dict(name=name, url=url, size=length, sha256=digest(target), **meta)

def manifest():
    manifest_path = inputs / 'manifest.json'
    require(digest(manifest_path) == 'cf50443b5e475e0337da90334176ed97e61f603dc27a5397ab24e74a3ad7c5cb',
            'Unexpected inputs manifest')
    with ThreadPoolExecutor(max_workers=4) as pool:
        references = dict(pool.map(acquire, reference_names.items()))
    wheel = here / 'stwcs-1.7.7-py3-none-any.whl'
    require(digest(wheel) == 'ba14d35cd581ca614a9e07d6c34d6958181ed96f118dfea8d361098b93deb90c',
            'STWCS 1.7.7 wheel differs')
    with ZipFile(wheel) as package:
        npol_source_sha = sha256(package.read('stwcs/updatewcs/npol.py')).hexdigest()
    trailer = prior / 'jb6v01010_trl.fits'
    require(digest(trailer) == 'b39d93ff19af1b6de4e9cc37e2759400d44fee37dcde66f85413faeceef97c6d', 'Trailer differs')
    with fits.open(trailer, memmap=True) as hdus:
        rows = hdus[1].data['TEXT_FILE']
        require('pipeline_flc_asn.fits' in rows[8155], 'Not the final FLC run')
        require('updatewcs :\tFalse' in rows[8186], 'Unexpected updatewcs setting')
    results = []
    for row in json.loads(manifest_path.read_bytes())['data']:
        path = inputs / 'flc' / row['file']
        require(digest(path) == row['sha256'], f'{path.name}: FLC hash changed')
        with fits.open(path, memmap=True, mode='readonly') as hdus:
            primary = hdus[0].header
            for key, entry in references.items():
                require(primary[key] == 'jref$' + entry['name'], f'{path.name}: {key} changed')
            result = dict(file=path.name, sha256=row['sha256'], context=primary.get('CRDS_CTX'),
                          updateWcsVersion=primary.get('UPWCSVER'), science=[])
            for ver in (1, 2):
                h = hdus['SCI', ver].header
                require(h['A_ORDER'] == h['B_ORDER'] == 5 and h['CTYPE1'].endswith('-SIP')
                        and h['CTYPE2'].endswith('-SIP'), f'{path.name}: missing order-5 SIP')
                require(h['WCSNAME'].startswith('IDC_4bb1536cj-'), f'{path.name}: unexpected WCS origin')
                correction = []
                for array, kind, key, coord in (('D2IMARR','D2IMFILE','D2IM{axis}.EXTVER','D2IMDIS{axis}'),
                                                ('WCSDVARR','NPOLFILE','DP{axis}.EXTVER','CPDIS{axis}')):
                    with fits.open(here/references[kind]['name'], memmap=True) as ref:
                        # STWCS 1.7.7 NPOLCorr converts detector offsets into the SIP frame.
                        reference_arrays = []
                        for axis_name in ('DX', 'DY'):
                            match = [u for u in ref[1:] if u.name == axis_name and u.header.get('CCDCHIP') == h['CCDCHIP']]
                            require(len(match) == 1, f'{path.name}: ambiguous CRDS chip/axis for {kind}')
                            reference_arrays.append(match[0])
                        predicted = [u.data for u in reference_arrays]
                        if kind == 'NPOLFILE':
                            coeffs = np.array([[h['OCX11'], h['OCX10']], [h['OCY11'], h['OCY10']]], dtype=np.float32)
                            inverse = np.linalg.inv(coeffs / h['IDCSCALE'])
                            projected = np.dot(inverse, [data.ravel() for data in predicted]).astype(np.float32)
                            predicted = [data.reshape(orig.shape).astype(orig.dtype)
                                         for data, orig in zip(projected, predicted, strict=True)]
                        for axis, (official, estimate) in enumerate(zip(reference_arrays, predicted, strict=True), 1):
                            require(h[coord.format(axis=axis)] == 'LOOKUP', f'{path.name}: invalid lookup type')
                            extver = int(h[key.format(axis=axis)])
                            embedded = hdus[array, extver]
                            a, b = np.asarray(embedded.data), estimate
                            require(a.shape == b.shape and a.dtype == b.dtype, f'{path.name}: lookup layout mismatch')
                            require(a.tobytes() == b.tobytes(), f'{path.name}: {array} {extver} differs from CRDS')
                            correction.append(dict(name=array, version=extver, referenceHdu=ref.index_of(official),
                                                   axis=axis, shape=list(a.shape), arraySha256=sha256(a.tobytes()).hexdigest()))
                result['science'].append(dict(version=ver, chip=h['CCDCHIP'], wcs=h['WCSNAME'],
                                              sipOrder=h['A_ORDER'], lookups=correction))
            results.append(result)
    document = dict(association='jb6v01010', exposures=results, references=references,
                    geometryQualifiedScope='Header and lookup payload binding, without WCS regeneration or drizzle execution.',
                    inputsManifestSha256=digest(manifest_path), previousMdriztabSha256=digest(prior/'37g1550cj_mdz.fits'),
                    stwcsVersion='1.7.7', wheelSha256=digest(wheel), npolSourceSha256=npol_source_sha,
                    numpyVersion=np.__version__, astropyVersion=astropy.__version__,
                    trailerSha256=digest(trailer), trailerFinalFlcStartLine=8156, trailerUpdateWcsLine=8187,
                    trailerUpdateWcs=False, pixInsightStarted=False, drizzleExecuted=False)
    require(document['previousMdriztabSha256'] == references['MDRIZTAB']['sha256'], 'MDRIZTAB digest differs')
    with (here/'binding.json').open('x',encoding='utf-8',newline='\n') as out:
        json.dump(document,out,indent=2,sort_keys=True)
        out.write('\n')
    print(json.dumps(dict(files=len(results), lookups=sum(len(s['lookups']) for r in results for s in r['science']),
                          references=references, bindingSha256=digest(here/'binding.json'))), flush=True)

if __name__ == '__main__':
    manifest()
