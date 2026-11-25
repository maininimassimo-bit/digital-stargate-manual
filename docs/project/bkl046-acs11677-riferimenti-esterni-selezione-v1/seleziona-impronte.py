
from hashlib import file_digest
from pathlib import Path
import json
import math
import re
import sys

base = Path(__file__).resolve().parent
sys.path.insert(0, r'O:\BKL046-ACS-WFC-runtime-7.2.0')
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np

query_path = base / 'ricerca-cono-query.json'
catalog_path = base / 'ricerca-cono-risposta.json'
cohort_path = Path(r'O:\BKL046-ACS-11677-scie-DQ-v1\riscontro.json')
flc_path = Path(r'O:\BKL046-ACS11677-drizzle-ingressi-v1\flc\jb6v01e0q_flc.fits')

def sha(path):
    with path.open('rb') as file:
        return file_digest(file, 'sha256').hexdigest()

def contains(points, vertices):
    x, y = points.T
    inside = np.zeros(x.shape, dtype=bool)
    for (xa, ya), (xb, yb) in zip(vertices, np.roll(vertices, -1, axis=0)):
        if ya != yb:
            crosses = (ya > y) != (yb > y)
            inside ^= crosses & (x < xa + (y - ya) * (xb - xa) / (yb - ya))
    return inside

def main():
    source_pins = {cohort_path: 'c7ab445f872054b6c4261c1250a733443c8b0d2316a8f0126e102f976235e43d',
                   flc_path: 'e6011691a50b2608a3cb91e5f9ceb0957aa4a17e46aa04f8e00bee30df5fdd4d'}
    for path, expected in source_pins.items():
        if sha(path) != expected:
            raise ValueError(f'Unexpected input hash for {path}')
    catalog = json.loads(catalog_path.read_bytes())
    rows = catalog['data']
    if (catalog['status'] != 'COMPLETE' or catalog['paging']['pagesFiltered'] != 1
            or catalog['paging']['rowsFiltered'] != len(rows)):
        raise ValueError('Incomplete MAST response')
    cohort = json.loads(cohort_path.read_bytes())['cases']
    chips = np.asarray([case['chip'] for case in cohort])
    if len(cohort) != 340 or set(chips) != {1, 2}:
        raise ValueError('Unexpected source cohort')
    sky = np.empty((len(cohort), 2))
    with fits.open(flc_path, mode='readonly', memmap=True) as flc:
        epoch = float(flc[0].header['EXPSTART'])
        for ext, chip in ((1, 2), (2, 1)):
            header = flc['SCI', ext].header
            if header['CCDCHIP'] != chip:
                raise ValueError('Unexpected detector binding')
            positions = [case['centerXY'] for case in cohort if case['chip'] == chip]
            sky[chips == chip] = WCS(header, flc).all_pix2world(positions, 0, ra_dec_order=True)
    if not np.isfinite(sky).all():
        raise ValueError('Invalid cohort sky positions')
    results = []
    for row in rows:
        if (row['dataRights'] != 'PUBLIC' or row['proposal_id'] == '11677'
                or not re.fullmatch(r'j[a-z0-9]{7}q', row['obs_id'])):
            continue
        shape, *coordinates = row['s_region'].split()
        if shape != 'POLYGON':
            raise ValueError(f'Unsupported MAST footprint for {row["obs_id"]}')
        polygon = np.array(coordinates, dtype=float).reshape(-1, 2)
        if not (np.isfinite(polygon).all() and (abs(polygon - sky.mean(axis=0)) < 1).all()):
            raise ValueError('Footprint outside local sky approximation')
        match = contains(sky, polygon)
        results.append(dict(root=row['obs_id'], obsid=row['obsid'], proposal=row['proposal_id'],
                            seconds=row['t_exptime'], deltaDays=row['t_min'] - epoch,
                            candidateCenters=int(match.sum()),
                            sourceChip1=int((match & (chips == 1)).sum()),
                            sourceChip2=int((match & (chips == 2)).sum())))
    results.sort(key=lambda r: (-r['candidateCenters'], r['seconds'], abs(r['deltaDays']), r['root']))
    report = dict(catalogRows=len(rows), individualPublicExternalRows=len(results), sourceEpochMjd=epoch,
                  querySha256=sha(query_path), catalogSha256=sha(catalog_path),
                  inputSha256={path.name: expected for path, expected in source_pins.items()},
                  method='Ray crossing in local RA/Dec using the CAOM outline. Preliminary geometric ranking only.',
                  pixelsInspected=False, scientificClosure=False, candidates=results)
    with (base / 'graduatoria-impronte.json').open('x', encoding='utf-8', newline='\n') as file:
        json.dump(report, file, indent=2, allow_nan=False)
        file.write('\n')
    print(len(rows), len(results))
    print(*[r for r in results if r['candidateCenters'] >= 275][:20], sep='\n')
    print('Short with overlap:', *[r for r in results if r['seconds'] <= 10 and r['candidateCenters'] > 0][:15], sep='\n')

if __name__ == '__main__':
    main()
