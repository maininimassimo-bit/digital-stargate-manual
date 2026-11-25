from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from urllib.request import urlopen

base = Path(__file__).resolve().parent
url='https://pypi.org/pypi/pycdlib/1.22.0/json'
with urlopen(url,timeout=20) as response:
    metadata=json.load(response)
wheel=next(w for w in metadata['urls'] if w['filename']=='pycdlib-1.22.0-py3-none-any.whl')
with urlopen(wheel['url'],timeout=20) as response:
    data=response.read()
if sha256(data).hexdigest()!=wheel['digests']['sha256']:
    raise ValueError('Wrong pycdlib digest')
file=base/wheel['filename']
if not file.exists():
    file.write_bytes(data)
if sha256(file.read_bytes()).hexdigest()!=wheel['digests']['sha256']:
    raise ValueError('Wrong cached digest')
sys.path.insert(0,str(file))
import pycdlib

config = b"""#cloud-config
ssh_pwauth: false
disable_root: true
package_update: false
package_upgrade: false
runcmd:
  - [sh, -ec, 'exec >/dev/ttyS0 2>&1; test "$(uname -m)" = x86_64; test -x /usr/bin/python3; echo BKL046_DEBIAN_SMOKE_OK; uname -srm; python3 --version']
power_state:
  mode: poweroff
  timeout: 90
  condition: true
"""
files = {
    'user-data': ('USER.DAT',config),
    'meta-data': ('META.DAT',b'instance-id: bkl046-debian-smoke-01\nlocal-hostname: bkl046-drizzle-smoke\n'),
    'network-config': ('NETWORK.CFG',b'version: 2\nethernets: {}\n'),
}
iso=pycdlib.PyCdlib()
iso.new(interchange_level=3,vol_ident='CIDATA',joliet=3,rock_ridge='1.09')
for name,(plain,content) in files.items():
    iso.add_fp(BytesIO(content),len(content),iso_path='/'+plain+';1',rr_name=name,joliet_path='/'+name)
target=base/'seed-smoke.iso'
iso.write(str(target))
iso.close()
print(target,sha256(target.read_bytes()).hexdigest(),wheel['digests']['sha256'])
