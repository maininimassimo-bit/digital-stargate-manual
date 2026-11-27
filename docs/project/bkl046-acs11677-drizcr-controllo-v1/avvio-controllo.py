import base64
from hashlib import file_digest
from io import BytesIO
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys
from tarfile import open as open_tar
import time

root=Path(__file__).resolve().parent
shared=runpy.run_path(str(root/'avvio-storico.py'))
sha,check=shared['sha'],shared['check']
image=root/'acs11677-input-only.iso'
base=root/'qualification-overlay-r2.qcow2'
working=root/'control-overlay.qcow2'
serial=root/'serial-control.log'
errors=root/'qemu-control.err'
export=root/'control-export.tar'
received=root/'control-received.json'
seed_path=root/'seed-control.iso'
q=root/'qemu'

def historical_invocation():
    first=json.loads((root/'historical-received.json').read_bytes())
    archive=root/'historical-export.tar'
    check(sha(archive)==first['archiveSha256'],'Historical export SHA differs')
    with open_tar(archive,'r:') as original,original.extractfile('invocation.json') as stream:
        return stream.read()

def prepare_seed(previous):
    lib=root/'pycdlib-1.22.0-py3-none-any.whl'
    check(sha(lib)=='bfa0b3631345a14b2741fe088398b6b8dc2838442ea607fd07d027dcc67b9e94','pycdlib changed')
    sys.path.insert(0,str(lib))
    import pycdlib

    files={name:(root/name).read_bytes() for name in ('run-historical.py','run-control.py',
                        'avvia-controllo-guest.sh','protocollo-confronto-r2.json')}
    files['historical-invocation.json']=previous
    lines=['#cloud-config','ssh_pwauth: false','disable_root: true','package_update: false',
          'package_upgrade: false','write_files:']
    for name,raw in files.items():
        content=base64.b64encode(raw).decode('ascii')
        lines += [f'  - path: /opt/bkl046/{name}', "    permissions: '0700'",
                  '    encoding: b64','    content: '+content]
    lines += ['runcmd:','  - [bash, /opt/bkl046/avvia-controllo-guest.sh]',
              'power_state:','  mode: poweroff','  timeout: 120','  condition: true']
    iso=pycdlib.PyCdlib()
    iso.new(interchange_level=3,vol_ident='CIDATA',joliet=3,rock_ridge='1.09')
    inputs=[
        ('user-data','USER.DAT',('\n'.join(lines)+'\n').encode('utf-8')),
        ('meta-data','META.DAT',b'instance-id: bkl046-drizzle-control-01\nlocal-hostname: bkl046-drizzle-control\n'),
        ('network-config','NETWORK.CFG',b"version: 2\nethernets:\n  virtio:\n    match:\n      name: 'en*'\n    dhcp4: true\n")
    ]
    for name,short,raw in inputs:
        iso.add_fp(BytesIO(raw),len(raw),iso_path='/'+short+';1',rr_name=name,joliet_path='/'+name)
    iso.write(str(seed_path))
    iso.close()

def verify_export():
    log=serial.read_text(encoding='utf-8',errors='replace')
    check(all(marker in log for marker in ('Power down','BKL046_CONTROL_EXIT=0','BKL046_EXPORT_DONE')),
          'Control execution did not reach normal shutdown after export')
    pins=re.findall(r'^BKL046_EXPORT_SHA256 ([a-f0-9]{64})\s*$',log,re.MULTILINE)
    check(len(pins)==1 and sha(export)==pins[0],'Transferred control archive SHA differs')
    with open_tar(export,'r:') as bundle:
        names=bundle.getnames()
        expected={'control.json','control-invocation.json','console.log','replica.log'}
        mosaic=[n for n in names if n.removeprefix('./').endswith('_drc.fits')]
        check(len(mosaic)==1 and set(names)==expected|set(mosaic) and len(names)==5 and
              all(m.isfile() for m in bundle.getmembers()),'Unexpected control archive entries')
        with bundle.extractfile('control.json') as stream:
            doc=json.load(stream)
        with bundle.extractfile('replica.log') as stream:
            stdout=stream.read()
        check(b"Step 'Driz_CR' was turned off" in stdout,'Log did not attest Driz_CR off')
        check(doc['file']==mosaic[0].removeprefix('./'),'Control DRC name differs from receipt')
        with bundle.extractfile(mosaic[0]) as stream:
            check(file_digest(stream,'sha256').hexdigest()==doc['drcSha256'],'Control DRC hash differs')
    return dict(data=doc,archiveSha256=pins[0],serialSha256=sha(serial),drizCrOffConfirmed=True)

def main():
    check(not any(p.exists() for p in (working,serial,errors,export,received,seed_path)),'Control already attempted')
    first=shared['signed_inputs']()
    check(sha(base)==first['qualifiedOverlaySha256'],'Qualified environment hash differs')
    previous=historical_invocation()
    prepare_seed(previous)
    subprocess.run([str(q/'qemu-img.exe'),'create','-f','qcow2','-F','qcow2','-b',str(base),str(working)],
                   cwd=root,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
    flags=[q/'qemu-system-x86_64.exe','-accel','tcg,thread=multi','-cpu','max','-m','6144','-smp','2','-machine','q35',
           '-display','none','-monitor','none','-serial','file:'+str(serial),'-drive',f'file={working},if=virtio,format=qcow2',
           '-boot','order=c','-nic','user,model=virtio-net-pci,restrict=on,ipv6=off','-no-reboot','-device','virtio-serial-pci',
           '-chardev',f'file,id=results,path={export}','-device','virtserialport,chardev=results,name=bkl046.results']
    for cd in (seed_path,image):
        flags+=['-drive',f'file={cd},media=cdrom,format=raw,readonly=on']
    begin=time.monotonic()
    with errors.open('xb') as failure:
        guest=subprocess.Popen([str(flag) for flag in flags],cwd=root,stderr=failure,stdout=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        print('BKL046_CONTROL_QEMU_PID',guest.pid,flush=True)
        try:
            code=guest.wait(timeout=7200)
        except subprocess.TimeoutExpired:
            guest.terminate()
            guest.wait(timeout=10)
            raise
    check(code==0,'Control QEMU failed')
    report=verify_export()
    check(sha(base)==first['qualifiedOverlaySha256'] and sha(image)==first['images'][image.name],
           'A read-only control input changed')
    report['elapsedSeconds']=round(time.monotonic()-begin,2)
    with received.open('x',encoding='utf-8',newline='\n') as out:
        json.dump(report,out,sort_keys=True,indent=2)
        out.write('\n')
    print('BKL046_CONTROL_ARCHIVE_OK',report['archiveSha256'],flush=True)

if __name__=='__main__':
    main()
