from contextlib import ExitStack
from hashlib import file_digest, sha256
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
BASE=Path('O:/')
sys.path.insert(0,str(BASE/'BKL046-ACS-WFC-runtime-7.2.0'))
from astropy.io import fits
import numpy as np


def pin(path):
    with path.open('rb') as stream:
        return file_digest(stream,'sha256').hexdigest()


def compare(a,b,bit):
    p=(a&bit)!=0
    q=(b&bit)!=0
    return dict(bit=bit,flt=int(p.sum()),flc=int(q.sum()),common=int((p&q).sum()),
                fltOnly=int((p&~q).sum()),flcOnly=int((q&~p).sum()))


def measure(out):
    raw=(ROOT/'protocollo.json').read_bytes()
    plan=json.loads(raw)
    report=[]
    for key,group in plan['images'].items():
        with ExitStack() as stack:
            images={}
            for kind,meta in group.items():
                path=BASE/meta['folder']/'source'/meta['file']
                assert pin(path)==meta['sha256']
                images[kind]=stack.enter_context(fits.open(path,mode='readonly',memmap=True))
            a,b=images['FLT'],images['FLC']
            for field in ('ROOTNAME','EXPTIME','EXPSTART','EXPEND','FILTER1','FILTER2'):
                assert a[0].header[field]==b[0].header[field]
            assert a[0].header['EXPTIME']==plan['times'][key]
            for ext in (1,2):
                x,y=a['SCI',ext].header,b['SCI',ext].header
                for field in ('CCDCHIP','NAXIS1','NAXIS2','LTV1','LTV2','LTM1_1','LTM2_2'):
                    assert x.get(field)==y.get(field)
                adq,bdq=a['DQ',ext].data,b['DQ',ext].data
                assert adq.shape==bdq.shape
                flags=[compare(adq,bdq,bit) for bit in plan['bits']]
                afull=(adq&256)!=0
                bfull=(bdq&256)!=0
                both=dict(flt=int((afull&((adq&4096)!=0)).sum()),
                          flc=int((bfull&((bdq&4096)!=0)).sum()),
                          common=int((afull&bfull&((adq&4096)!=0)&((bdq&4096)!=0)).sum()))
                report.append(dict(exposure=key,chip=int(x['CCDCHIP']),pixels=adq.size,flags=flags,
                    differingDqWords=int(np.count_nonzero(adq!=bdq)),fullWellAndCosmicFlag=both,
                    calibration=dict(fltPcteCorr=a[0].header.get('PCTECORR'),flcPcteCorr=b[0].header.get('PCTECORR'),
                        fltVersion=a[0].header.get('CAL_VER'),flcVersion=b[0].header.get('CAL_VER'))))
    data=dict(protocol='BKL046_ACS11677_DQ_PRODUCT_LINEAGE_RESULT_V1',
              planSha256=sha256(raw).hexdigest(),rows=report,photometryPerformed=False,
              astronomicalTruthIndependent=False,nativeExecutions=0,scientificClosures=0)
    with out.open('xb') as sink:
        sink.write(json.dumps(data,indent=2,sort_keys=True,allow_nan=False).encode()+b'\n')


if __name__=='__main__':
    measure(Path(sys.argv[1]))