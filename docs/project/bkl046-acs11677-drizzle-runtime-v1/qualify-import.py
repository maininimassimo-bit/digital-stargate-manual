import importlib.machinery
import importlib.metadata
import json
from pathlib import Path
import platform
import sys

from astropy.io import fits
from astropy.wcs import WCS
from drizzlepac import astrodrizzle,cdriz
from scipy.signal import convolve2d
from stwcs import wcsutil
from stsci.tools.fileutil import osfn
import numpy as np
import os

if sys.version_info[:2]!=(3,13) or platform.machine()!='x86_64':
    raise ValueError('Unexpected guest Python ABI')
if importlib.metadata.version('drizzlepac')!='3.11.0' or importlib.metadata.version('stwcs')!='1.7.7':
    raise ValueError('Unexpected scientific package version')
if not callable(astrodrizzle.AstroDrizzle) or not isinstance(cdriz.__loader__,importlib.machinery.ExtensionFileLoader):
    raise ValueError('AstroDrizzle or compiled DrizzlePac module unavailable')
if not callable(cdriz.tdriz) or not callable(cdriz.tblot):
    raise ValueError('Compiled drizzle/blot functions unavailable')
if convolve2d(np.ones((2,2)),np.ones((2,2))).tolist()!=[[1.,2.,1.],[2.,4.,2.],[1.,2.,1.]]:
    raise ValueError('Unexpected SciPy convolution')
os.environ['jref']='/mnt/science/jref/'
root=Path('/mnt/science')
with fits.open(osfn('jref$37g1550cj_mdz.fits')) as h:
    assert h[1].data is not None and len(h[1].data)>=4
rows=json.loads((root/'meta'/'manifest.json').read_bytes())['data']
receipt=[]
for row in rows:
    flc=root/'flc'/row['file']
    with fits.open(flc,memmap=False,mode='readonly') as hdus:
        fits_info=[]
        for ext in (1,2):
            sci=hdus['SCI',ext]
            dq=hdus['DQ',ext]
            wcs=WCS(sci.header,hdus)
            hst=wcsutil.HSTWCS(hdus,ext=('SCI',ext))
            if sci.shape!=dq.shape or not wcs.has_distortion or not hst.has_distortion:
                raise ValueError(f'Invalid input geometry {flc.name}[{ext}]')
            pixel=np.array([[2048.,1024.]])
            coords=wcs.all_pix2world(pixel,0)
            fitted=hst.all_pix2world(pixel,0)
            if not np.isfinite(coords).all() or not np.allclose(coords,fitted,atol=1e-9,rtol=0):
                raise ValueError(f'Invalid world coordinates {flc.name}[{ext}]')
            fits_info.append(dict(chip=sci.header['CCDCHIP'],shape=list(sci.shape),
                                  bit4096Count=int(np.count_nonzero(dq.data&4096))))
        receipt.append(dict(file=flc.name,sci=fits_info))
runtime=dict(python=platform.python_version(),machine=platform.machine(),libc=platform.libc_ver(),
             packages={p:importlib.metadata.version(p) for p in ('drizzlepac','stwcs','numpy','astropy','scipy','stsci.tools')},
             nativeModule=Path(cdriz.__file__).name,source=receipt,astroDrizzleRun=False)
print('BKL046_QUAL_JSON '+json.dumps(runtime,sort_keys=True),flush=True)
