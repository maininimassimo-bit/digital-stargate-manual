from concurrent.futures import ThreadPoolExecutor
import hashlib,json,sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

root=Path(sys.argv[1])
ids=("jfln02qtq","jfln02qzq","jfln02021","jfln02qtj","jfln02qzj")
products=[f"{obs}_{suffix}.fits" for obs in ids for suffix in ("spt","jit","jif")]

def fetch(name):
    url="https://mast.stsci.edu/api/v0.1/Download/file?"+urlencode({"uri":"mast:HST/product/"+name})
    try:
        with urlopen(url,timeout=12) as response:
            data=response.read(10_000_001)
        if not data.startswith(b"SIMPLE  =") or len(data)>10_000_000 or len(data)%2880:
            return {"name":name,"status":"NOT_VALID_FITS"}
        (root/name).write_bytes(data)
        return {"name":name,"status":"OK","sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data)}
    except OSError as error:
        return {"name":name,"status":type(error).__name__,"httpCode":getattr(error,"code",None)}

with ThreadPoolExecutor(max_workers=6) as pool:
    results=list(pool.map(fetch,products))
(root/"acquisizione.json").write_bytes((json.dumps(results,sort_keys=True,indent=2)+"\n").encode())
print([(row["name"],row["status"]) for row in results])
