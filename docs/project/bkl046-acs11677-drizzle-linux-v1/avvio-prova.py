from hashlib import file_digest
import json
from pathlib import Path
import subprocess
import time

base = Path(__file__).resolve().parent
qemu = base / 'qemu'
binary = qemu / 'qemu-system-x86_64.exe'
img = qemu / 'qemu-img.exe'
image = base / 'debian-13-genericcloud-amd64.qcow2'
seed = base / 'seed-smoke.iso'
overlay = base / 'smoke-overlay.qcow2'
serial = base / 'serial-smoke.log'
stderr = base / 'qemu-smoke.err'
manifest = base/'environment-smoke.json'

def digest(path, algorithm='sha256'):
    with path.open('rb') as stream:
        return file_digest(stream,algorithm).hexdigest()

def run(args):
    return subprocess.run([str(s) for s in args],cwd=base,check=True,capture_output=True,text=True,
                          creationflags=subprocess.CREATE_NO_WINDOW).stdout

def require(passed, name):
    if not passed:
        raise ValueError(name)

expected = '76488ba3bea2349cc595fedad7748b8ba98d6b36da398eaf2bbbae3db896ba1017d4ff41cd277926784cef2c1c11145a0d600f9b4afde9b8f174d698db0cda03'
require(digest(image,'sha512')==expected,'Wrong Debian image')
require(not any(p.exists() for p in (overlay,serial,stderr,manifest)), 'Use a new working directory for a fresh boot')
version = run([binary,'--version']).splitlines()[0]
backing = run([img,'info','--output=json',image])
run([img,'create','-f','qcow2','-F','qcow2','-b',image,overlay])
run([img,'resize',overlay,'12G'])
args = [binary,'-accel','tcg,thread=multi','-cpu','max','-m','5120','-smp','2','-machine','q35',
        '-display','none','-monitor','none','-serial','file:'+str(serial),
        '-drive',f'file={overlay},if=virtio,format=qcow2',
        '-drive',f'file={seed},media=cdrom,format=raw,readonly=on',
        '-boot','order=c','-nic','none','-no-reboot']
t=time.monotonic()
with stderr.open('xb') as err:
    process=subprocess.Popen([str(a) for a in args],cwd=base,stderr=err,stdout=subprocess.DEVNULL,
                             creationflags=subprocess.CREATE_NO_WINDOW)
    print(f'QEMU PID={process.pid}',flush=True)
    try:
        code=process.wait(timeout=420)
    except subprocess.TimeoutExpired:
        process.terminate()
        process.wait(timeout=10)
        raise
require(code==0,f'QEMU status {code}, examine {stderr}')
lines=serial.read_text(encoding='utf-8',errors='replace').splitlines()
matches=[x.strip() for x in lines if any(s in x for s in ('BKL046_DEBIAN_SMOKE_OK','Linux bkl046','Python 3.','Power down','DataSourceNoCloud'))]
require(any('BKL046_DEBIAN_SMOKE_OK' in x for x in matches), f'No NoCloud success marker in {serial}')
require(any('Python 3.13.' in x for x in matches),'Guest Python 3.13 is missing')
require(any('Power down' in x for x in matches),'Clean guest shutdown not observed')
require(digest(image,'sha512')==expected,'Debian image changed')
report=dict(qemuVersion=version,qemuSha256=digest(binary),debianSha512=expected,
            debianVirtualBytes=json.loads(backing)['virtual-size'],seedSha256=digest(seed),
            guestEvidence=matches,serialSha256=digest(serial),networkEnabled=False,
            qemuExit=code,elapsedSeconds=round(time.monotonic()-t,1),
            astroDrizzleExecuted=False,pixInsightStarted=False)
with manifest.open('x',encoding='utf-8',newline='\n') as stream:
    json.dump(report,stream,indent=2,sort_keys=True)
    stream.write('\n')
print(json.dumps(report),flush=True)
