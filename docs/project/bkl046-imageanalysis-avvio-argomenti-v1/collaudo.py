from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import os
import sys
import uuid

BASE=Path(__file__).resolve().parent
sys.path[:0]=[str(BASE), 'O:/BKL046-ImageAnalysis-cadena-R4-v6']
from prepara import stage
from verifica_avvio import verify_launch


def main():
    op,nonce=uuid.uuid4().hex,uuid.uuid4().hex
    staging=BASE/'staging'
    staging.mkdir(exist_ok=True)
    with stage(staging,op,nonce) as (staged,guard):
        root=staging/op
        now=datetime.now(timezone.utc)
        guard()
        result=verify_launch(staged,root,now)
        cases=[]
        for name,change,expected in (
            ('forced exit',lambda d:d['launchArguments'].append('--force-exit'),'IA_LAUNCH_ARGUMENTS'),
            ('automation mode',lambda d:d['launchArguments'].append('--automation-mode'),'IA_LAUNCH_ARGUMENTS'),
            ('open project',lambda d:d['launchArguments'].append('unrelated.pxiproject'),'IA_LAUNCH_ARGUMENTS'),
            ('yield to other instance',lambda d:d['launchArguments'].__setitem__(1,'--yield'),'IA_LAUNCH_ARGUMENTS'),
            ('different entry',lambda d:d['launchArguments'].__setitem__(-1,'--run=foreign.js'),'IA_LAUNCH_ARGUMENTS'),
            ('wrong executable',lambda d:d['launchArguments'].__setitem__(0,'elsewhere.exe'),'IA_LAUNCH_ARGUMENTS'),
            ('entry digest',lambda d:next(p for p in d['staged']
                if p['path'].endswith('/entry.js')).update(sha256='0'*64),'IA_LAUNCH_PIN'),
        ):
            altered=deepcopy(staged)
            change(altered)
            try:
                verify_launch(altered,root,now)
            except ValueError as err:
                if str(err)!=expected:
                    raise
                cases.append(name)
            else:
                raise AssertionError(name)
        for name, clock in (('expired',now+timedelta(seconds=121)),
                            ('outside fresh stage',now-timedelta(seconds=121))):
            try:
                verify_launch(staged,root,clock)
            except ValueError as err:
                if str(err)!='IA_LAUNCH_BUDGET':
                    raise
                cases.append(name)
            else:
                raise AssertionError(name)
        guard()
    assert len(cases)==9
    result.update(rejections=cases, stagedFiles=len(staged['staged']),
                  scope='Actual NTFS staging and exact argv verification')
    with Path(sys.argv[1]).open('xb') as out:
        out.write(json.dumps(result,sort_keys=True,indent=2).encode()+b'\n')


if __name__=='__main__':
    main()