"""Archive the MAST WFC3 three-band calibrator catalog, without recency filtering."""
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode
from urllib.request import urlopen

ALIASES = {
    "GD71": ["GD71", "GD-71", "GD 71", "WD0549+158", "WD-0549+158"],
    "G191B2B": ["G191B2B", "G191-B2B", "G191 B2B", "G191-B2B-CENTER", "WD0501+527"],
    "GRW70": ["GRW+70D5824", "GRW+70D5824-CENTER", "GRW+70-5824", "GRW+70D5824-OFFSET",
              "GRW+705824", "GRW+70 5824", "WD2309+105", "WD2309+105-CENTER"],
}
BANDS = {"F438W", "F606W", "F814W"}
COLUMNS = "obsid,obs_id,proposal_id,target_name,filters,t_exptime,t_min,t_max,instrument_name,dataproduct_type,dataRights,s_ra,s_dec,calib_level,project"


def sha(raw):
    return sha256(raw).hexdigest()


def save(path, raw):
    if path.exists():
        if path.read_bytes() != raw:
            raise ValueError(f"Prior file differs: {path.name}")
    else:
        with path.open("xb") as f:
            f.write(raw)


def survey(folder, key):
    filters = [dict(paramName="target_name", values=ALIASES[key]),
               dict(paramName="obs_collection", values=["HST"]),
               dict(paramName="instrument_name", values=["WFC3/UVIS"]),
               dict(paramName="filters", values=sorted(BANDS))]
    q = dict(service="Mast.Caom.Filtered", params=dict(columns=COLUMNS, filters=filters),
             page=1, pagesize=1000, format="json")
    request = json.dumps(q, sort_keys=True, separators=(",", ":")).encode()
    save(folder / (key + "-query.json"), request)
    path = folder / (key + "-observations.json")
    if path.exists():
        raw = path.read_bytes()
    else:
        with urlopen("https://mast.stsci.edu/api/v0/invoke",
                     data=urlencode({"request": request}).encode(), timeout=40) as response:
            raw = response.read(8*1024**2 + 1)
        if not 0 < len(raw) <= 8*1024**2:
            raise ValueError("Archive response size")
        save(path, raw)
    obj = json.loads(raw)
    paging = obj["paging"]
    if obj["status"] != "COMPLETE" or not 0 <= paging["pagesFiltered"] <= 10:
        raise ValueError("Archive page count")
    pages = [dict(page=1, request=sha(request), response=sha(raw))]
    entries = list(obj["data"])
    for page in range(2, paging["pagesFiltered"] + 1):
        query = json.dumps(dict(q, page=page), sort_keys=True, separators=(",", ":")).encode()
        save(folder / f"{key}-query-{page}.json", query)
        leaf = folder / f"{key}-observations-{page}.json"
        if leaf.exists():
            data = leaf.read_bytes()
        else:
            with urlopen("https://mast.stsci.edu/api/v0/invoke",
                         data=urlencode({"request": query}).encode(), timeout=40) as response:
                data = response.read(8*1024**2 + 1)
            if not 0 < len(data) <= 8*1024**2:
                raise ValueError("Archive response size")
            save(leaf, data)
        result = json.loads(data)
        if result["status"] != "COMPLETE" or result["paging"]["page"] != page or (
                result["paging"]["rowsFiltered"] != paging["rowsFiltered"]):
            raise ValueError("Archive pagination changed")
        pages.append(dict(page=page, request=sha(query), response=sha(data)))
        entries.extend(result["data"])
    if len(entries) != paging["rowsFiltered"] or len({r["obsid"] for r in entries}) != len(entries):
        raise ValueError("Archive response not exhaustive")
    visits = defaultdict(list)
    for row in entries:
        ident = row["obs_id"]
        proposed = re.fullmatch(r"i[a-z0-9]{7}[q0]", ident)
        if row["project"] != "HST" or row["dataRights"] != "PUBLIC" or not row["proposal_id"] or not proposed:
            continue
        visits[row["proposal_id"], ident[:6]].append(row)
    accepted = []
    for (proposal, visit), rows in sorted(visits.items()):
        if {r["filters"] for r in rows} == BANDS:
            accepted.append(dict(proposal=proposal, visit=visit, rows=sorted(rows, key=lambda x: x["obs_id"])))
    return dict(target=key, rows=len(entries), visits=accepted, pages=pages)


def main():
    folder = Path(sys.argv[1])
    with ThreadPoolExecutor(max_workers=3) as pool:
        stars = list(pool.map(lambda key: survey(folder, key), ALIASES))
    result = dict(schema="BKL046_WFC3_CALIBRATOR_COHORT_CATALOG_V1", stars=stars)
    save(folder / "catalogo.json", (json.dumps(result, sort_keys=True, indent=2) + "\n").encode())
    for s in stars:
        print(s["target"], s["rows"], len(s["visits"]),
              [(v["proposal"],v["visit"],len(v["rows"])) for v in s["visits"]])


if __name__ == "__main__":
    main()