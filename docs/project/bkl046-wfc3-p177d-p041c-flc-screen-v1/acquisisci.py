"""Acquire public CALWF3 products for frozen independent calibrator visits."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

PIN = "b69b780754e308ba09ade311bc2be8bf50d69659a33ad4184ad69c0bd824e2b0"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return sha256(raw).hexdigest()


def fetch(url, limit, data=None):
    for attempt in range(3):
        try:
            with urlopen(url, data=data, timeout=40) as f:
                require(f.status == 200, "HTTP status")
                raw = f.read(limit + 1)
            require(0 < len(raw) <= limit, "Unexpected response size")
            return raw
        except (HTTPError, URLError, TimeoutError) as exc:
            if attempt == 2 or isinstance(exc, HTTPError) and exc.code not in (408, 429, 500, 502, 503, 504):
                raise
            time.sleep(attempt + 1)


def save(path, raw):
    if path.exists():
        require(digest(path.read_bytes()) == digest(raw), f"Existing {path.name} differs")
    else:
        with path.open("xb") as f:
            f.write(raw)
    return digest(raw)


def main():
    root = Path(sys.argv[1])
    raw = (root / "protocollo.json").read_bytes()
    require(digest(raw) == PIN, "Protocol changed")
    p = json.loads(raw)
    raw = (root / "catalogo.json").read_bytes()
    require(digest(raw) == p["catalogSha256"], "Catalog changed")
    selected = [dict(row, target=v["target"]) for v in p["selected"] for row in v["rows"]]
    require(len(selected) == len({row["obs_id"] for row in selected}) == 9, "Catalog selection changed")
    folder = root / "source"

    def acquire(row):
        obs = row["obs_id"]
        query = json.dumps(dict(service="Mast.Caom.Products", params=dict(obsid=str(row["obsid"])),
                                page=1, pagesize=1000, format="json"), sort_keys=True).encode()
        query_pin = save(folder / f"{obs}-query.json", query)
        response = folder / f"{obs}-products.json"
        raw = response.read_bytes() if response.exists() else fetch(
            "https://mast.stsci.edu/api/v0/invoke", 2 * 1024**2, urlencode({"request": query}).encode())
        response_pin = save(response, raw)
        result = json.loads(raw)
        require(result["status"] == "COMPLETE", f"Partial product response for {obs}")
        products = [r for r in result["data"] if r["project"] == "CALWF3" and r["productType"] == "SCIENCE"
                    and r["dataRights"] == "PUBLIC" and r["productSubGroupDescription"] == "FLC"
                    and r["filters"] == row["filters"] and (obs.endswith("0") or r["productFilename"] == obs+"_flc.fits")]
        names = {}
        for match in products:
            leaf = match["productFilename"]
            uri = match["dataURI"]
            require(re.fullmatch(r"i[a-z0-9]{7}q_flc[.]fits", leaf) and leaf.startswith(obs[:6])
                    and uri == "mast:HST/product/" + leaf, f"FLC identity: {obs}")
            names[leaf] = uri
        entries = []
        for leaf, uri in sorted(names.items()):
            download = folder / leaf
            if download.exists():
                blob = download.read_bytes()
            else:
                blob = fetch("https://mast.stsci.edu/api/v0.1/Download/file?" + urlencode({"uri": uri}),
                             100663296)
            require(blob.startswith(b"SIMPLE  =") and len(blob) % 2880 == 0, "Incomplete FITS data")
            pin = save(download, blob)
            entries.append(dict(file=leaf, uri=uri, bytes=len(blob), sha256=pin))
        print(obs, len(entries), flush=True)
        return dict(observation=obs, band=row["filters"], obsid=str(row["obsid"]), visit=obs[:6],
                    proposal=int(row["proposal_id"]), target=row["target"], targetAlias=row["target_name"],
                    querySha256=query_pin, productsSha256=response_pin, entries=entries)

    with ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(acquire, sorted(selected, key=lambda r: r["obs_id"])))
    all_files = [leaf["file"] for record in records for leaf in record["entries"]]
    require(len(set(all_files)) == len(all_files), "Selected product sets overlap")
    report = dict(schema="BKL046_WFC3_P177D_P041C_ACQUISITION_V1", protocolSha256=PIN,
                  programSha256=digest(Path(__file__).read_bytes()), records=records)
    save(root / "acquisizione.json", (json.dumps(report, indent=2, sort_keys=True) + "\n").encode())
    print(json.dumps(dict(catalog=len(records), acquired=len(all_files))))


if __name__ == "__main__":
    main()