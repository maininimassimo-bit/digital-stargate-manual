from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import sys

ROOT = Path(sys.argv[1])
OBS = ("jfln05ykq", "jfln05ymq")
SIZES = {"jfln05ykq": 168_431_040, "jfln05ymq": 168_546_240}
CHUNK = 8_000_000


def get_range(obs, start):
    size = SIZES[obs]
    end = min(start + CHUNK, size) - 1
    filename = obs + "_flt.fits"
    query = urlencode({"uri": "mast:HST/product/" + filename})
    url = "https://mast.stsci.edu/api/v0.1/Download/file?" + query
    req = Request(url, headers={"Range": f"bytes={start}-{end}"})
    with urlopen(req, timeout=20) as response:
        if response.status != 206 or response.headers["Content-Range"] != f"bytes {start}-{end}/{size}":
            raise OSError(f"Unexpected range response: {obs} {start}")
        data = response.read(end - start + 2)
    if len(data) != end - start + 1:
        raise OSError(f"Incomplete range: {obs} {start}")
    return data


with ThreadPoolExecutor(max_workers=10) as pool:
    tasks = {obs: [pool.submit(get_range, obs, start) for start in range(0, SIZES[obs], CHUNK)] for obs in OBS}
    receipt = []
    for obs in OBS:
        filename = obs + "_flt.fits"
        digest = sha256()
        temp = ROOT / (filename + ".ranged")
        with temp.open("xb") as stream:
            for part in tasks[obs]:
                data = part.result()
                stream.write(data)
                digest.update(data)
        if temp.stat().st_size != SIZES[obs]:
            raise OSError(f"Unexpected total size: {obs}")
        final = ROOT / filename
        if final.exists():
            with final.open("rb") as stream:
                if sha256(stream.read()).hexdigest() != digest.hexdigest():
                    raise OSError(f"Conflicting full download: {obs}")
        else:
            temp.rename(final)
        print(obs, digest.hexdigest(), flush=True)
        receipt.append({"file": filename, "bytes": SIZES[obs], "sha256": digest.hexdigest()})
(ROOT / "acquisizione-range.json").write_bytes((json.dumps(receipt, sort_keys=True, indent=2) + "\n").encode())
