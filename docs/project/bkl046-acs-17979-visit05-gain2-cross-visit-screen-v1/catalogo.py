import json
from pathlib import Path
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

root = Path(sys.argv[1])
query = {"service": "Mast.Caom.Products", "params": {"obsid": "434647373"},
         "page": 1, "pagesize": 1000, "format": "json"}
body = json.dumps(query)
(root / "query.json").write_text(body, encoding="ascii")
url = "https://mast.stsci.edu/api/v0/invoke"
with urlopen(Request(url, data=urlencode({"request": body}).encode()), timeout=20) as response:
    data = response.read(2_000_001)
if len(data) > 2_000_000:
    raise OSError("Oversized MAST response")
(root / "prodotti.json").write_bytes(data)
products = json.loads(data)
if products["status"] != "COMPLETE" or products["paging"]["pagesFiltered"] != 1:
    raise OSError(f"Incomplete MAST product query: {products['status']}")
flight = sorted({(row["productFilename"], row["size"]) for row in products["data"]
                 if row["project"] == "CALACS" and row["dataRights"] == "PUBLIC"
                 and row["productSubGroupDescription"] in ("FLT", "RAW")})
print(flight)
