import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

parser = argparse.ArgumentParser()
for key in ("history", "metadata", "fresh", "destination"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()


def pinned(path, digest):
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != digest:
        raise ValueError(f"Unexpected bytes: {path.name}")
    return json.loads(raw)


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def exclusive(path, value):
    raw = encode(value)
    with path.open("xb") as stream:
        stream.write(raw)
    assert path.read_bytes() == raw
    return sha256(raw).hexdigest()


early_sha = "62dba7e5e5d426733577eb3d0b307fa7abc1dc06a87e87d16a9119c8f8ffd37c"
late_sha = "c5818bf6cd0c8dbaaf030d108bfff91e1fc15b1ddb5f95cf3aa82619919322c0"
corroboration_sha = "21299a8b9c5175c517336238c983b01bba1ce1d59711284890bd1c23ebcf0cf4"
plan_sha = "cb30745073d1a69003e41b78da1948ef3093508b9a7ed5f97d3cf01b2827e90a"
transport_sha = "48262824c9472647d47218c77e0fccc579ce04a9436e8219be42623bbf8b31e6"
release_sha = "ca6ac2dba26e90704bd583d1073744079b9e889a4fc95cc38895d702cab815d1"
early = pinned(args.history / "storia-iniziale.json", early_sha)
late = pinned(args.history / "storia-verificata.json", late_sha)
corroboration = pinned(args.history / "corroborazione-prime-versioni.json", corroboration_sha)
plan = pinned(args.metadata / "piano-completo.json", plan_sha)
transport = pinned(args.metadata / "inventario-trasporto.json", transport_sha)
release = pinned(args.metadata / "soggetto.json", release_sha)
fresh_raw = args.fresh.read_bytes()
fresh = json.loads(fresh_raw)
assert fresh["inventorySha256"] == late_sha and fresh["planned"] == 45
assert fresh["exactMatches"] == fresh["stableReadbacks"] == 45
assert fresh["bytesMatched"] == 63599156359
fresh_rows = {r["version"]: r for r in fresh["results"]}
assert len(fresh_rows) == 45
early_links = {r["version"]: r for r in corroboration["links"]}
early_rows = {r["version"]: r for r in early["rows"]}
transport_jobs = {r["job"]: r for r in transport["jobs"]}
transport_assets = {a["name"]: a for a in transport["assets"]}
release_assets = {a["name"]: a for a in release["assets"]}
assert set(release_assets) == {*transport_assets, release["knowledge"]["assetName"]}
assert all(release_assets[name] == item for name, item in transport_assets.items())
object_job = {}
for job in plan["jobs"]:
    for digest in job["items"]:
        assert digest not in object_job
        object_job[digest] = job
assert set(object_job) == set(plan["contents"])

aliases = {}
for row in plan["aliases"]:
    aliases.setdefault(row["name"], []).append(row)
joined = []
for row in early["rows"] + late["rows"]:
    version = row["version"]
    name = row["name"]
    old_pin = row.get("actualSha256")
    claim = row["recordedSha256"]
    if version in fresh_rows:
        reread = fresh_rows[version]
        assert row["status"] == "RECORDED_PIN_UNVERIFIED_READBACK"
        assert reread["status"] == "MATCHES_RECORDED_PIN" and reread["stableRead"] is True
        assert reread["bytes"] == row["bytes"] and reread["name"] == name
        assert reread["actualSha256"] == reread["recordedSha256"] == claim
        digest = reread["actualSha256"]
        basis = "NEW_FULL_FILE_READBACK_MATCHED_RECORDED_PIN"
    elif row["status"] == "READ_WITHOUT_MATCHING_RECEIPT":
        digest = old_pin
        link = early_links[version]
        successor = early_rows[link["successor"]]
        assert link["sha256"] == digest
        assert link["verifiedSuccessorSha256"] == successor["actualSha256"]
        assert link["successorHasDirectManifest"] == (successor["status"] == "MATCHES_RECORDED_PIN")
        basis = "PRIOR_FILE_READBACK_WITH_VERIFIED_SUCCESSOR_PIN"
    else:
        assert row["status"] == "MATCHES_RECORDED_PIN" and old_pin == claim
        digest = old_pin
        basis = "PRIOR_FULL_FILE_READBACK_MATCHED_RECORDED_PIN"
    entry, = [x for x in aliases[name] if x["sha256"] == digest and x["bytes"] == row["bytes"]]
    assert plan["contents"][digest]["bytes"] == row["bytes"]
    job = object_job[digest]
    order = transport_jobs[job["id"]]["assetOrder"]
    assert len(order) >= 1
    if job["kind"] == "split":
        assert len(job["items"]) == 1 and len(order) >= 2
        assert sum(transport_assets[asset]["bytes"] for asset in order) == row["bytes"]
    else:
        assert job["kind"] == "zip" and len(order) == 1
    joined.append(dict(version=version, name=name, role=entry["role"], bytes=row["bytes"], sha256=digest,
                       localEvidence=basis, job=job["id"], carrierKind=job["kind"],
                       zipMember="objects/" + digest if job["kind"] == "zip" else None,
                       assetOrder=[transport_assets[x] for x in order], remoteAssetIdVerified=False))

assert [r["version"] for r in joined] == [f"0.{i}" for i in range(1, 10)] + [f"1.{i}" for i in range(172)]
assert joined[-1]["sha256"] == release["knowledge"]["innerSha256"]
counts = Counter(r["localEvidence"] for r in joined)
assert sorted(counts.values()) == [4, 45, 132]
coverage = dict(schema="BKL046_KNOWLEDGE_VERSION_CARRIER_MAP_V1", releaseSubjectSha256=release_sha,
                transportInventorySha256=transport_sha, corpusPlanSha256=plan_sha,
                historyReportPins=[early_sha,late_sha,corroboration_sha], rereadSha256=sha256(fresh_raw).hexdigest(),
                allHistoricalVersionsMappedLocally=True, remoteAssetIdsVerified=0, versions=joined)
map_pin = exclusive(args.destination / "mappa-versioni.json", coverage)
public_summary = dict(schema="BKL046_KNOWLEDGE_LOCAL_HISTORY_COVERAGE_V1",
                      firstVersion=joined[0]["version"], lastVersion=joined[-1]["version"],
                      versions=len(joined), historicalFileBytes=sum(row["bytes"] for row in joined),
                      newHashMatchedFiles=fresh["exactMatches"], rereadBytes=fresh["bytesMatched"],
                      verifiedVersionsByEvidence=dict(counts),
                      releaseCandidateAssets=len(release_assets),
                      mappedVersionCarrierAssets=len({a["name"] for row in joined for a in row["assetOrder"]}),
                      versionsUsingSplitAssets=sum(r["carrierKind"]=="split" for r in joined),
                      releaseSubjectSha256=release_sha, historyMapSha256=map_pin,
                      localArchiveByteCoverageVerified=True,
                      remoteAssetIdsVerified=0, githubTransferVerified=False, scientificClosures=0)
exclusive(args.destination / "riscontro.json", public_summary)
print(json.dumps(public_summary))
