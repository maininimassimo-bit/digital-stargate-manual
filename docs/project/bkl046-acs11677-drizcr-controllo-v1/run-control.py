import json
import os
from pathlib import Path
import runpy
import shutil
import time

from astropy.io import fits
from drizzlepac import astrodrizzle, mdzhandler
import numpy as np

module=runpy.run_path('/opt/bkl046/run-historical.py')
check=module['check']
sha=module['sha']
write_json=module['write_json']
originals=module['media']
source_config=Path('/opt/bkl046/historical-invocation.json')
control_root=Path('/var/lib/bkl046-control')
published_plan=Path('/opt/bkl046/protocollo-confronto-r2.json')
plan_sha='2462e94562463ddfa06adb8c50203c1103d6c25ad68f6416dc571c7ac8d5657e'

def run():
    check(sha(published_plan)==plan_sha,'Control protocol hash mismatch')
    plan=json.loads(published_plan.read_bytes())
    runs=json.loads(source_config.read_bytes())
    rows=module['validate_sources']()
    names=[r['file'] for r in rows]
    check(runs['input']==names and runs['mdriztab'] is True,'Historical inputs or table selection mismatch')
    params=runs['parameters']
    check(all(params.get(k)==v for k,v in {
        'updatewcs':False,'wcskey':'','resetbits':'4096','crbit':4096,'num_cores':1,
        'driz_cr_corr':False,'clean':False,'in_memory':False}.items()),'Historical parameter mismatch')
    check('driz_cr' not in params and plan['arms']['control']['driz_cr'] is False,'Incorrect arm distinction')
    control_root.mkdir()
    os.chdir(control_root)
    os.environ['jref']=str(originals/'jref')+'/'
    for row in rows:
        shutil.copyfile(originals/'flc'/row['file'],row['file'])
        check(sha(Path(row['file']))==row['sha256'],'Wrong FLC working copy')
    effective=mdzhandler.getMdriztabParameters(names)
    check({k:str(v) for k,v in effective.items()}==runs['tableValue'],'MDRIZTAB lookup differs')
    params=dict(params,driz_cr=False)
    write_json(control_root/'control-invocation.json',dict(input=names,mdriztab=True,parameters=params,
                 historicalInvocationSha256=sha(source_config),amendmentSha256=sha(published_plan),tableValue=runs['tableValue']))
    stopwatch=time.monotonic()
    astrodrizzle.AstroDrizzle(input=names,mdriztab=True,**params)
    products=list(control_root.glob('jb6v01010*_drc.fits'))
    check(len(products)==1 and not list(control_root.glob('*_crmask.fits')),'Missing control DRC or unexpected CR mask')
    spectra=[]
    for row in rows:
        name=row['file']
        path=originals/'flc'/name
        check(sha(path)==row['sha256'],'Input medium changed')
        with fits.open(path,memmap=False) as original,fits.open(control_root/name,memmap=False) as local:
            for ext in (1,2):
                initial=original['DQ',ext].data.astype(np.uint16)
                after=local['DQ',ext].data.astype(np.uint16)
                check(after.shape==initial.shape and np.array_equal(after,initial&np.uint16(65535^4096)),
                      f'Unexpected control DQ {name} / {ext}')
                spectra.append(dict(file=name,ext=ext,prior4096=int(np.count_nonzero(initial&4096))))
    output=products[0]
    write_json(control_root/'control.json',dict(drcSha256=sha(output),file=output.name,
                       seconds=round(time.monotonic()-stopwatch,2),expectedNoCrMasks=True,controlDq=spectra,
                       inputManifestSha256=sha(module['manifest']),controlOnly=True))
    print('BKL046_CONTROL_RUN_COMPLETE',sha(control_root/'control.json'),flush=True)

if __name__=='__main__':
    run()
