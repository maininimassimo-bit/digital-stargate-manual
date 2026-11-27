from contextlib import ExitStack
from hashlib import file_digest,sha256
from io import BytesIO
import json
from pathlib import Path
from tarfile import open as open_tar
import sys

root=Path(__file__).resolve().parent
sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
sys.path.insert(0,str(root/'diagnose-tools'))
from astropy.io import fits
from dissect.extfs import ExtFS
from dissect.hypervisor.disk.qcow2 import QCow2
from dissect.volume.disk import Disk

def require(ok,why):
    if not ok:raise ValueError(why)
def digest(path):
    with path.open('rb') as f:return file_digest(f,'sha256').hexdigest()

def filesystem(stack,overlay):
    def stream(name):
        return stack.enter_context((root/name).open('rb'))
    backing=QCow2(stream('qualification-overlay-r2.qcow2'),
                  backing_file=stream('debian-13-genericcloud-amd64.qcow2')).open()
    h=QCow2(stream(overlay),backing_file=backing).open()
    return ExtFS(max(Disk(h).partitions,key=lambda p:p.size).open())

def raw(fs,folder,name):
    with fs.get(f'{folder}/{name}').open() as f:
        return f.read()

def inspect(fs,folder,name,expected_shape):
    source=raw(fs,folder,name)
    with fits.open(BytesIO(source),memmap=False) as doc:
        doc.verify('exception')
        data=doc[0].data
        require(data.shape==expected_shape,'Wrong intermediate dimensions '+name)
        unit=doc[0].header.get('BUNIT')
        return dict(fileSha256=sha256(source).hexdigest(),payloadSha256=sha256(data.tobytes()).hexdigest(),
                    shape=list(data.shape),dtype=str(data.dtype),bunit=unit)

def main():
    include_blots="--blots" in sys.argv[1:]
    authority=json.loads((root/'historical-received.json').read_bytes())
    historical=root/'historical-export.tar'
    require(digest(historical)==authority['archiveSha256'],'Historical output changed')
    with open_tar(historical,'r:') as tar,tar.extractfile('invocation.json') as report:
        old=json.load(report)
    expect=[]
    for file in old['input']:
        name=file.removesuffix('_flc.fits')
        expect.extend([name+'_sci1_blt.fits',name+'_sci2_blt.fits'] if include_blots else
                      [name+'_single_sci.fits',name+'_single_wht.fits'])
    if not include_blots:
        expect.append('jb6v01010_med.fits')
    expected_shape=(2048,4096) if include_blots else (4523,4528)
    a,b='/var/lib/bkl046-replica/historical','/var/lib/bkl046-control'
    with ExitStack() as st:
        one=filesystem(st,'historical-overlay.qcow2')
        two=filesystem(st,'control-overlay.qcow2')
        invocation_raw=raw(two,b,'control-invocation.json')
        invocation=json.loads(invocation_raw)
        require(old['input']==invocation['input'] and old['tableValue']==invocation['tableValue'] and
                old['mdriztab'] is invocation['mdriztab'] is True,'Dataset or MDRIZTAB differs')
        require(invocation['parameters']==dict(old['parameters'],driz_cr=False),'Control changed additional invocation parameters')
        for f,folder in ((one,a),(two,b)):
            log=raw(f,folder,'replica.log')
            require(b"Processing Step 'Create Median' finished" in log and b"Processing Step 'Blot' started" in log,
                    'Common intermediate stage has not yet closed')
            if include_blots:
                require(b"Processing Step 'Blot' finished" in log,'Blot stage is still active')
        comparison=[]
        for name in expect:
            x,y=inspect(one,a,name,expected_shape),inspect(two,b,name,expected_shape)
            require(x['shape']==y['shape'] and x['bunit']==y['bunit'] and x['dtype']==y['dtype'],
                    'Intermediate format differs '+name)
            comparison.append(dict(name=name,historical=x,control=y,identicalPixelBytes=x['payloadSha256']==y['payloadSha256']))
    require(len(comparison)==(12 if include_blots else 13),'Incomplete set of intermediate products')
    summary=dict(compared=len(comparison),sameBytes=sum(x['identicalPixelBytes'] for x in comparison),
                 historicalArchiveSha256=authority['archiveSha256'],controlInvocationSha256=sha256(invocation_raw).hexdigest(),
                 soleInvocationChange={'driz_cr':False},controlFinished=False,
                 scope=('Readback of every blotted chip before the CR step.' if include_blots else
                        'Independent readback of the completed pre-rejection separate and median products.'),
                 data=comparison,scientificClosure=False)
    where=root/('confronto-blot-comuni.json' if include_blots else 'confronto-intermedi-comuni.json')
    with where.open('x',encoding='utf-8',newline='\n') as out:
        json.dump(summary,out,sort_keys=True,indent=2)
        out.write('\n')
    print('STAGES_READ_BACK',summary['sameBytes'],len(comparison),digest(where),flush=True)

if __name__=='__main__':
    main()
