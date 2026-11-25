from argparse import ArgumentParser
import json
from pathlib import Path
import runpy
import shutil
from tarfile import open as open_tar
from tempfile import TemporaryDirectory

folder=Path(__file__).resolve().parent
shared=runpy.run_path(str(folder/'confronta-drc.py'))
fits,np=shared['fits'],shared['np']
require,digest=shared['require'],shared['digest']
header_grid,same_grid=shared['header_grid'],shared['same_grid']
compare_payloads=shared['compare_payloads']

def read_run(tar_path,receipt_path,invocation_name,output):
    report=json.loads(receipt_path.read_bytes())
    require(digest(tar_path)==report['archiveSha256'],'Run TAR SHA changed')
    mosaic=report['data']['file']
    require(Path(mosaic).name==mosaic and mosaic.endswith('_drc.fits'),'Unexpected run mosaic name')
    with open_tar(tar_path,'r:') as tar:
        member,=[x for x in tar.getmembers() if x.isfile() and x.name.removeprefix('./')==mosaic]
        with tar.extractfile(member) as source,output.open('xb') as destination:
            shutil.copyfileobj(source,destination,length=1048576)
        require(digest(output)==report['data']['drcSha256'],'Run mosaic SHA changed')
        with tar.extractfile(invocation_name) as stream:
            return report,json.loads(stream.read())

def compare_coverage(a,b):
    require(a.shape==b.shape,'Weight coverage grid dimensions differ')
    counts={'bothCovered':0,'historicalOnlyCovered':0,'controlOnlyCovered':0,'neitherCovered':0}
    for start in range(0,a.shape[0],128):
        a0,b0=a[start:start+128],b[start:start+128]
        x=np.isfinite(a0) & (a0>0)
        y=np.isfinite(b0) & (b0>0)
        for key,z in (('bothCovered',x&y),('historicalOnlyCovered',x&~y),
                      ('controlOnlyCovered',~x&y),('neitherCovered',~x&~y)):
            counts[key]+=int(np.count_nonzero(z))
    return counts

def compare_effective_logs(control_archive):
    report=folder/'confronto-parametri-effettivi.json'
    original=folder/'astrodrizzle-replica-integrale.log'
    expected=json.loads(report.read_bytes())
    require(digest(original)==expected['replicaLogSha256'],'Historical effective-parameter log changed')
    with open_tar(control_archive,'r:') as tar,tar.extractfile('replica.log') as stream:
        control=stream.read()
    require(b"Step 'Driz_CR' was turned off" in control and b"Processing Step 'Final Drizzle' finished" in control,
            'Control log lacks formal CR or final mosaic evidence')
    source=runpy.run_path(str(folder/'estrai-log-storico.py'))
    scan=source['logged_pairs']
    one=scan(original.read_text(encoding='utf-8').splitlines())
    two=scan(control.decode('utf-8').splitlines())
    shared=sorted(one.keys() & two.keys())
    differences=[dict(stage=k[0],param=k[1],historical=one[k],control=two[k])
                 for k in shared if one[k]!=two[k]]
    historic_only=sorted(one.keys()-two.keys())
    control_only=sorted(two.keys()-one.keys())
    return dict(compared=len(shared),matching=len(shared)-len(differences),
                differing=differences,historicalOnly=[list(k) for k in historic_only],
                controlOnly=[list(k) for k in control_only],
                sameShared=not differences and not control_only and all(k[0]=='Driz_CR' for k in historic_only))


def main():
    parser=ArgumentParser()
    parser.add_argument('historical_tar',type=Path)
    parser.add_argument('historical_receipt',type=Path)
    parser.add_argument('control_tar',type=Path)
    parser.add_argument('control_receipt',type=Path)
    parser.add_argument('report',type=Path)
    args=parser.parse_args()
    with TemporaryDirectory(prefix='bkl046-paired-drc-',dir=folder) as dest:
        a,b=(Path(dest)/n for n in ('historical.fits','control.fits'))
        historic,previous=read_run(args.historical_tar,args.historical_receipt,'invocation.json',a)
        control,current=read_run(args.control_tar,args.control_receipt,'control-invocation.json',b)
        require(historic['data']['masks'] and control['drizCrOffConfirmed'],'Both arms are not verified')
        require(previous['input']==current['input'] and previous['tableValue']==current['tableValue']
                and previous['mdriztab'] is current['mdriztab'] is True,'Input or table difference between arms')
        require('driz_cr' not in previous['parameters'] and current['parameters']==dict(previous['parameters'],driz_cr=False),
                'Unexpected parameter difference between arms')
        with fits.open(a,memmap=True) as ah,fits.open(b,memmap=True) as bh:
            ag,bg=header_grid(ah['SCI',1]),header_grid(bh['SCI',1])
            errors=same_grid(ag,bg)
            result=dict(historicalDrcSha256=historic['data']['drcSha256'],controlDrcSha256=control['data']['drcSha256'],
                        shapeAndWcsMatch=not errors,gridDifferences=errors,
                        scienceGrid=ag,controlDifference={'driz_cr':False},
                        effectiveLogComparison=compare_effective_logs(args.control_tar),scientificClosure=False)
            if not errors:
                result['payloads'],result['context']=compare_payloads(ah,bh)
                result['coverage']=compare_coverage(ah['WHT',1].data,bh['WHT',1].data)
    with args.report.open('x',encoding='utf-8',newline='\n') as out:
        json.dump(result,out,indent=2,sort_keys=True)
        out.write('\n')
    print(digest(args.report),flush=True)

if __name__=='__main__':
    main()
