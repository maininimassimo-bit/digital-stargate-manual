from hashlib import file_digest
import json
from pathlib import Path
import sys
import warnings

here=Path(__file__).resolve().parent
sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
from astropy.io import fits
from astropy.wcs import FITSFixedWarning,WCS
import numpy as np

census=Path(r'O:\BKL046-ACS-11677-fotometria-v2\censimento.json')
geometry=Path(r'O:\BKL046-ACS-11677-geometria-v1\riscontro.json')
cases_file=Path(r'O:\BKL046-ACS-11677-scie-DQ-v1\riscontro.json')
reference=Path(r'O:\BKL046-ACS11677-drizzle-ingressi-v1\flc\jb6v01e0q_flc.fits')
headerlet=geometry.parent/'headerlets'/'jb6v25aaq_flt_hlet.fits'
previous=Path(r'O:\BKL046-ACS-11677-geometria-lunghe-v1\protocollo.json')
pins={census:'f767afda06343a0594c5c02189e712298bee355c4bc8829db0587b6edb5cf236',
      cases_file:'c7ab445f872054b6c4261c1250a733443c8b0d2316a8f0126e102f976235e43d',
      reference:'e6011691a50b2608a3cb91e5f9ceb0957aa4a17e46aa04f8e00bee30df5fdd4d',
      headerlet:'8764f5a2509fb068eb8977d21a61677f18b6e424a15448a248c9fc9d7e6a0540'}
def digest(path):
    with path.open('rb') as stream:return file_digest(stream,'sha256').hexdigest()
def require(ok,name):
    if not ok:raise ValueError(name)
for path,sha in pins.items():
    require(digest(path)==sha,'Evidence changed '+path.name)
found=[r for r in json.loads(census.read_bytes())['exposures'] if r['band']=='F606W' and r['seconds']<1000]
require([(i['root'],i['seconds']) for i in found]==[('jb6v01dfq',1.0),('jb6v25aaq',100.0)],
        'The exposure selection changed')
old_plan=json.loads(previous.read_bytes())
selected=[i for i in json.loads(geometry.read_bytes())['selected'] if i['selected']=='jb6v25aaq']
require(len(selected)==1 and selected[0]['headerletSha256']==pins[headerlet],'Visit 25 headerlet pin differs')
cases=json.loads(cases_file.read_bytes())['cases']
per_case=[]
counts={}
with fits.open(reference,mode='readonly',memmap=True) as a,fits.open(headerlet,mode='readonly',memmap=True) as b:
    require(b[0].header['DESTIM'].lower()=='jb6v25aaq','Headerlet is for another exposure')
    wa,wb={},{}
    for ext,chip in ((1,2),(2,1)):
        h=a['SCI',ext].header
        w=b['SIPWCS',ext].header
        require(h['CCDCHIP']==chip and w['TG_ENAME']=='SCI' and w['TG_EVER']==ext and
                w['CRPIX1']==2048 and w['CRPIX2']==1024,'Headerlet has unexpected extension binding')
        wa[chip]=WCS(h,a)
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',message='The WCS transformation has more axes',category=FITSFixedWarning)
            wb[chip]=WCS(w,b)
        require(wb[chip].sip is not None and wb[chip].det2im1 is not None and wb[chip].cpdis1 is not None,
                'Complete target distortion is required for projection')
    for chip in (1,2):
        pool=[(i+1,c) for i,c in enumerate(cases) if c['chip']==chip]
        points=wa[chip].all_pix2world([c['centerXY'] for _,c in pool],0,ra_dec_order=True)
        shots={other:w.all_world2pix(points,0,tolerance=1e-8,maxiter=70,quiet=False,ra_dec_order=True)
               for other,w in wb.items()}
        for slot,(i,c) in enumerate(pool):
            candidates=[]
            for other in (1,2):
                x,y=shots[other][slot]
                if np.isfinite([x,y]).all() and 20<=x<4076 and 20<=y<2028:
                    candidates.append(dict(chip=other,xy=[float(x),float(y)]))
                    key=f'{chip}->{other}'
                    counts[key]=counts.get(key,0)+1
            per_case.append(dict(sourceId=i,chip=chip,xy=c['centerXY'],candidates=candidates))
require(len(per_case)==340,'Frozen saturation case count differs')
out={'sourceCasesSha256':pins[cases_file],'targetHeaderletSha256':pins[headerlet],
     'censusSha256':pins[census],'referenceFLCsha256':pins[reference],
     'target':found[1],'footprints':counts,'uniqueInnerCenters':sum(len(r['candidates'])==1 for r in per_case),
     'edgeMarginPx':20,'positions':sorted(per_case,key=lambda v:v['sourceId']),
     'geometryQualificationProtocolSha256':digest(previous),
     'heldoutP90LimitPx':old_plan['heldoutP90LimitPx'],
     'minFitAndHoldoutStars':old_plan['minFitAndHoldoutStars'],
     'minFitAndHoldoutTiles':old_plan['minFitAndHoldoutTiles'],
     'photometryMeasured':False,'scientificClosure':False}
receipt=here/'copertura-100s.json'
with receipt.open('x',encoding='utf-8',newline='\n') as stream:
    json.dump(out,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write('\n')
print(counts,out['uniqueInnerCenters'],digest(receipt),flush=True)
