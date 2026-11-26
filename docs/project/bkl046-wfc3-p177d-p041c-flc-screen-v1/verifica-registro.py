"""Verify the archived MAST result against the pinned acquisition offline."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode

CAPTURE = "0febc35785b4c30dad737ddffe64faa1241c5fe7e05dbabe219b90fef3641d03"
REPORT = "c8e1156de22038b71042eca0a01dae3e2492f8fe9e70aba4d76206faf9eb759e"
BASE = "https://mast.stsci.edu/api/v0.1/Download/file?"
EXPECTED = {("P041C", "ibnx05"): 9, ("P177D", "ibnx06"): 6, ("P177D", "ibwi04"): 6}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_verified(path, digest):
    data = path.read_bytes()
    require(sha256(data).hexdigest() == digest, path.name)
    return json.loads(data)


def main(root):
    capture = read_verified(root / "acquisizione.json", CAPTURE)
    report = read_verified(root / "riscontro-endpoint.json", REPORT)
    require(report["sourceCaptureSha256"] == CAPTURE, "Capture lineage")
    require(sha256((root / "verifica-endpoint.py").read_bytes()).hexdigest()
            == report["programSha256"], "Probe lineage")
    roster = {}
    for record in capture["records"]:
        association = record["observation"]
        products = read_verified(root / "source" / f"{association}-products.json",
                                 record["productsSha256"])
        for item in products["data"]:
            name = item["productFilename"]
            if (item["project"], item["productType"], item["productSubGroupDescription"], item["dataRights"]) == (
                    "CALWF3", "SCIENCE", "FLT", "PUBLIC") and re.fullmatch(r"i[a-z0-9]{7}q_flt[.]fits", name):
                require(name not in roster, "Duplicate product")
                roster[name] = (record["target"], record["visit"], association, record["band"])
    require(Counter((target, visit) for target, visit, _, _ in roster.values()) == EXPECTED, "Visit counts")
    rows = report["rows"]
    require(len(rows) == len(roster) == len({row["flt"] for row in rows}) == 21, "Product count")
    for row in rows:
        require((row["target"], row["visit"], row["association"], row["band"]) == roster[row["flt"]],
                "Product lineage")
        flc = row["flt"].removesuffix("_flt.fits") + "_flc.fits"
        require(row["flc"] == flc and row["request"] == BASE + urlencode({"uri": "mast:HST/product/" + flc}),
                "Endpoint identity")
        require(row["result"]["httpStatus"] == 404 and row["result"]["startsWithFitsHeader"] is False
                and re.fullmatch(r"[0-9a-f]{64}", row["result"]["responseSha256"]), "Recorded HTTP outcome")
    require(report["notFound"] == 21 and report["verifiedAvailable"] == 0, "HTTP outcome totals")
    print(json.dumps({"archivedHttp404": len(rows), "visits": len(EXPECTED)}))


if __name__ == "__main__":
    main(Path(sys.argv[1]))