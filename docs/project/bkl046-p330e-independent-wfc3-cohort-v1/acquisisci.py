"""Acquire exact public P330E FLCs selected from the frozen MAST catalog."""
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

PIN = "98dc06c0708be16b94b1285e299c15ddc1da9bcd3272bcfe523937e649adbdc4"


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
    raw = (root / "P330E-observations.json").read_bytes()
    require(digest(raw) == p["catalogSha256"], "Catalog changed")
    catalog = json.loads(raw)
    require(catalog["status"] == "COMPLETE" and catalog["paging"]["pagesFiltered"] == 1, "Incomplete catalog")
    selected = [row for row in catalog["data"] if row["proposal_id"] in p["proposals"]
                and row["instrument_name"] == "WFC3/UVIS" and row["filters"] in p["bands"]
                and row["target_name"] == p["target"] and row["dataRights"] == "PUBLIC"
                and re.fullmatch(r"i[a-z0-9]{7}q", row["obs_id"])]
    require(len(selected) == len({row["obs_id"] for row in selected}) == 30, "Exposure set changed")
    counts = Counter((r["obs_id"][:6], r["filters"]) for r in selected)
    require(counts == {(visit, band): count for visit in p["visits"]
                       for band, count in zip(p["bands"], p["expectedCountsPerVisit"], strict=True)},
            "Visit-band structure changed")
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
        name = obs + "_flc.fits"
        uri = "mast:HST/product/" + name
        products = [r for r in result["data"] if r["productFilename"] == name and r["project"] == "CALWF3"
                    and r["productType"] == "SCIENCE" and r["dataRights"] == "PUBLIC"
                    and r["productSubGroupDescription"] == "FLC"]
        output = dict(file=name, band=row["filters"], obsid=str(row["obsid"]), visit=obs[:6],
                      proposal=int(row["proposal_id"]), catalogStartMjd=row["t_min"],
                      querySha256=query_pin, productsSha256=response_pin)
        if not products:
            print(obs, "NO_EXACT_PUBLIC_FLC", flush=True)
            return dict(output, status="NO_EXACT_PUBLIC_FLC")
        require(all((r["dataURI"], r["filters"]) == (uri, row["filters"]) for r in products),
                f"Product identity differs: {obs}")
        download = folder / name
        blob = fetch("https://mast.stsci.edu/api/v0.1/Download/file?" + urlencode({"uri": uri}),
                     p["productSizeLimit"])
        require(blob.startswith(b"SIMPLE  =") and len(blob) % 2880 == 0, "Incomplete FITS data")
        pin = save(download, blob)
        print(obs, len(blob), flush=True)
        return dict(output, status="EXACT_FLC", uri=uri, bytes=len(blob), sha256=pin)

    with ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(acquire, sorted(selected, key=lambda r: r["obs_id"])))
    report = dict(schema="BKL046_P330E_WFC3_INDEPENDENT_ACQUISITION_V1", protocolSha256=PIN,
                  programSha256=digest(Path(__file__).read_bytes()), records=records)
    save(root / "acquisizione.json", (json.dumps(report, indent=2, sort_keys=True) + "\n").encode())
    print(json.dumps(dict(catalog=len(records), acquired=sum(r["status"] == "EXACT_FLC" for r in records))))


if __name__ == "__main__":
    main()