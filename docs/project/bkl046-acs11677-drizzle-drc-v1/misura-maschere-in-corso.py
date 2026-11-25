from hashlib import file_digest,sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from contextlib import ExitStack

root=Path(__file__).resolve().parent
sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
sys.path.insert(0,str(root/'diagnose-tools'))
from dissect.extfs import ExtFS
from dissect.hypervisor.disk.qcow2 import QCow2
from dissect.volume.disk import Disk
from astropy.io import fits
import numpy as np

data=Path(r'O:\BKL046-ACS11677-drizzle-ingressi-v1')
wm=data/'manifest.json'
guest_dir='/var/lib/bkl046-replica/historical'
def require(ok,msg):
    if not ok:raise ValueError(msg)
def digest(path):
    with path.open('rb') as inp:
        return file_digest(inp,'sha256').hexdigest()

def open_guest(stack):
    def stream(file):
        return stack.enter_context((root/file).open('rb'))
    first=QCow2(stream('qualification-overlay-r2.qcow2'),backing_file=stream('debian-13-genericcloud-amd64.qcow2')).open()
    original=QCow2(stream('historical-overlay.qcow2'),backing_file=first).open()
    return ExtFS(max(Disk(original).partitions,key=lambda x:x.size).open())

def read_masks(mapping,rows):
    result={}
    for row in rows:
        rootname=row['file'].removesuffix('_flc.fits')
        for ext in (1,2):
            mask=f'{rootname}_sci{ext}_crmask.fits'
            stream=mapping.get(guest_dir+'/'+mask).open()
            with stream:
                body=stream.read()
            result[mask]=body
    return result

def run():
    require(digest(wm)=='cf50443b5e475e0337da90334176ed97e61f603dc27a5397ab24e74a3ad7c5cb','FLC manifest changed')
    rows=json.loads(wm.read_bytes())['data']
    with ExitStack() as st:
        raw=read_masks(open_guest(st),rows)
    with ExitStack() as st:
        replay=read_masks(open_guest(st),rows)
    require(raw.keys()==replay.keys() and all(raw[n]==replay[n] for n in raw),'A live mask was still changing')
    measurements=[]
    for row in rows:
        file=data/'flc'/row['file']
        require(digest(file)==row['sha256'],'FLC SHA mismatch '+file.name)
        leaf=file.name.removesuffix('_flc.fits')
        chips=[]
        with fits.open(file,memmap=False) as actual:
            for ext in (1,2):
                name=f'{leaf}_sci{ext}_crmask.fits'
                payload=raw[name]
                require(len(payload)%2880==0,'Invalid FITS block alignment')
                with fits.open(BytesIO(payload),memmap=False) as mask:
                    mask.verify('exception')
                    flags=mask[0].data
                original=actual['DQ',ext].data
                require(flags.shape==original.shape==(2048,4096) and np.isin(flags,[0,1]).all(),
                        'Invalid binary mask '+name)
                a=original&4096!=0
                b=flags==0
                record=dict(chip=actual['SCI',ext].header['CCDCHIP'],sciExt=ext,maskFile=name,
                       maskSha256=sha256(payload).hexdigest(),bytes=len(payload),counts=dict(
                       neither=int(np.count_nonzero(~a&~b)),both=int(np.count_nonzero(a&b)),
                       archiveOnly=int(np.count_nonzero(a&~b)),replicaOnly=int(np.count_nonzero(~a&b))))
                require(sum(record['counts'].values())==original.size,'Counts do not cover chip')
                chips.append(record)
        measurements.append(dict(file=file.name,science=chips))
    total={key:sum(r['counts'][key] for m in measurements for r in m['science']) for key in measured_keys}
    require(total['archiveOnly']+total['both']==2910514,'Archived DQ count differs from setup qualification')
    report=dict(masks=measurements,stableReadbacks=2,totals=total,inputManifestSha256=digest(wm),
                finalArchiveVerified=False,scientificClosure=False)
    where=root/'maschere-lettura-in-corso.json'
    with where.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(report,stream,indent=2,sort_keys=True)
        stream.write('\n')
    print(json.dumps(total),digest(where),flush=True)

measured_keys=('neither','both','archiveOnly','replicaOnly')
if __name__=='__main__':
    run()
