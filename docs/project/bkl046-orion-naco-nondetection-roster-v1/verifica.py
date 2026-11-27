"""Join published NACO targets and detections with potential public ACS coverage."""
import hashlib
import json
import math
from pathlib import Path
import re
import sys

root, parent, report = map(Path, sys.argv[1:])


def pinned(name, expected):
    data = (parent / name).read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f"Changed source: {name}")
    return data


def separation_arcsec(a, b):
    ra1, dec1, ra2, dec2 = map(math.radians, (*a, *b))
    hav = math.sin((dec2-dec1)/2)**2 + math.cos(dec1)*math.cos(dec2)*math.sin((ra2-ra1)/2)**2
    return math.degrees(2*math.asin(math.sqrt(min(1, max(0, hav))))) * 3600


def main():
    raw = (root / "protocollo.json").read_bytes()
    cfg = json.loads(raw)
    source = pinned("verifica.py", cfg["readerSha256"]).decode("utf-8-sig")
    reference = {"__name__": "pinned_catalog_reader"}
    exec(compile(source[:source.index("\ndef main():")].replace("root,report=map(Path,argv[1:])", ""), "pinned_catalog_reader.py", "exec"), reference)
    table, tsv = reference["table"], reference["tsv"]
    naco = pinned("duchene-2018.html", cfg["duchene2018Sha256"])
    hill = tsv(pinned("hillenbrand-vizier.tsv", cfg["hillenbrandSha256"]))
    reip = tsv(pinned("reipurth-vizier.tsv", cfg["reipurthSha256"]))
    mast = json.loads(pinned("mast-go10246.json", cfg["mastSha256"]))
    earlier = json.loads(pinned("riscontro.json", cfg["parentReportSha256"]))
    if mast["status"] != "COMPLETE" or mast["paging"]["rowsFiltered"] != len(mast["data"]):
        raise ValueError("MAST query incomplete")

    roster = {}
    membership = None
    for cells in table(naco, "S2.T1"):
        if len(cells) == 1:
            membership = cells[0]
        if len(cells) == 7 and cells[0].isdigit():
            key = int(cells[0])
            if key in roster or membership not in ("Cluster members", "Likely non-members"):
                raise ValueError("Invalid sample record")
            roster[key] = (membership, cells)
    visits = {}
    date = None
    for day, objects, _ in table(naco, "S2.T2")[1:]:
        date = day or date
        if not date:
            raise ValueError("Missing observation date")
        for name in objects.split(","):
            visits.setdefault(int(name), []).append(date)
    detections = {}
    for cells in table(naco, "S3.T3"):
        if len(cells) == 4 and cells[0].isdigit():
            detections.setdefault(int(cells[0]), []).append(reference["measures"](cells[1])[0])
    if (set(roster) != set(visits) or not set(detections) <= set(roster)
            or len(roster) != cfg["expectedNacoTargets"]
            or sum(member == "Cluster members" for member, _ in roster.values()) != cfg["expectedClusterMembers"]
            or sum(map(len,detections.values())) != cfg["expectedNacoDetectionRows"]):
        raise ValueError("Published tables disagree with the declared census")
    acs = [(row, reference["polygons"](row["s_region"] or "")) for row in mast["data"]
           if re.fullmatch(r"j93k[a-z0-9]{4}q", row["obs_id"]) and row["intentType"] == "science"
           and row["filters"] == "F555W" and row["t_exptime"] and row["dataRights"] == "PUBLIC"]
    records = []
    for key, (member, cells) in sorted(roster.items()):
        positions = [row for row in hill if row["ID"] == str(key)]
        point = reference["degrees"](positions[0]["RAJ2000"], positions[0]["DEJ2000"]) if len(positions) == 1 else None
        hits = reference["footprints"](acs, point).get("F555W", []) if point else []
        neighbors = []
        for row in earlier["acsF555W"] if point else []:
            distance = separation_arcsec(point, row["approximateTwoMassLocationJ2000"])
            if distance <= cfg["proximityFlagArcsec"]:
                neighbors.append(dict(twoMassId=row["twoMassId"], distanceArcsec=distance))
        reip_rows = [float(row["Sep"]) for row in reip if row["[H97b]"] == str(key)]
        exclusions = []
        if member != "Cluster members":
            exclusions.append("LIKELY_NONMEMBER")
        if key in detections:
            exclusions.append("NACO_DETECTION")
        if cells[6]:
            exclusions.append("MULTIPLICITY_FLAG")
        if reip_rows:
            exclusions.append("HST_F658N_REPORTED_COMPANION")
        if neighbors:
            exclusions.append("NEAR_PUBLISHED_F555W_PAIR_REQUIRES_IDENTITY_CHECK")
        if point is None:
            exclusions.append("NO_UNIQUE_H97_POSITION")
        if len(hits) < cfg["minimumCandidateExposureCount"]:
            exclusions.append("BELOW_MINIMUM_GEOMETRIC_COVERAGE")
        records.append(dict(h97=key, membership=member, nirKsMag=float(cells[1]),
                            publishedMultiplicityFlag=cells[6], dates=visits[key],
                            nacoDetectionsMas=detections.get(key,[]), reipurthF658nSeparationsArcsec=reip_rows,
                            nearbyDeFurioF555wPositions=neighbors, h97CatalogLocationJ2000=point,
                            hstPotentialExposures=hits, exclusions=exclusions, cohortCandidate=not exclusions,
                            signedOpticalNegativeTruth=False))
    report_obj = dict(schema=cfg["schema"], protocolSha256=hashlib.sha256(raw).hexdigest(),
                      surveyApproximateDomain=cfg["surveyApproximateDomain"], records=records,
                      publishedNacoTargets=len(roster), nacoTargetsWithDetections=len(detections),
                      candidates=sum(row["cohortCandidate"] for row in records), opticalNegativeLabelsQualified=0,
                      nativeExecutions=0, scientificClosures=0)
    with report.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(report_obj, output, sort_keys=True, indent=2, allow_nan=False)
        output.write("\n")


if __name__ == "__main__":
    main()
