from pathlib import Path
import hashlib
import json
import sys
from zipfile import ZipFile


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream,"sha256").hexdigest()


root, eos6d, heart = map(Path, sys.argv[1:])
raws = root/"input"
raws.mkdir()
rows = []
capture = eos6d/"acquisizione.json"
if sha(capture) != "95e4253dd93eca3ab2b8565bd12fe598967cd0e7fa290011bca8438db73fde36":
    raise ValueError("Invalid EOS6D acquisition")
metadata = json.loads(capture.read_bytes())
for item in metadata["samples"]:
    source = eos6d/item["file"]
    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != item["sha256"]:
        raise ValueError("Invalid EOS6D sample")
    dest = "EOS6D-light-"+item["file"]
    (raws/dest).write_bytes(data)
    rows.append({"camera":"EOS6D","group":"light","file":dest,"originMember":item["member"],
                 "sha256":item["sha256"]})
if sha(heart) != "4a0c4142d8d0e7b056ec9b46046eec78fe6fc149aabf3c028923f81d6851f0a0":
    raise ValueError("Invalid EOS40D archive")
with ZipFile(heart) as bundle:
    for group, count in (("light",39),("dark",17)):
        members = sorted(item for item in bundle.namelist()
                         if item.startswith("HeartNebula/"+group+"s/") and item.lower().endswith(".cr2"))
        if len(members) != count:
            raise ValueError("Wrong exposure inventory")
        for i, member in enumerate((members[0],members[len(members)//2],members[-1]),1):
            data = bundle.read(member)
            dest = f"EOS40D-{group}-{i}.CR2"
            (raws/dest).write_bytes(data)
            rows.append({"camera":"EOS40D","group":group,"file":dest,"originMember":member,
                         "sha256":hashlib.sha256(data).hexdigest()})
cfg = {"schema":"BKL046_REAL_CFA_NATIVE_CODE_CLIPPING_V1","inputs":rows,
       "rawpyWheelSha256":"fb91f8fb21b56037ecc3c062ce2de4d97fdc7d4ecb1d2738280461d74c593562",
       "thresholdsBelowWhiteFraction":[0.001, 0.01],
       "scope":"Use the stored visible CFA and preserve its four phases. Thresholds are decoder-declared, not measured full well. Compare recurrence in detector coordinates and the sampled 40D darks. No demosaic, colour conversion or signal recovery."}
(root/"protocollo.json").write_bytes((json.dumps(cfg,sort_keys=True,indent=2)+"\n").encode())
print(json.dumps({"samples":len(rows),"protocolSha256":sha(root/"protocollo.json")}))
