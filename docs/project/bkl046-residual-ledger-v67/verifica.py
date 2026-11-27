"""Verify and append BKL-046 residual evidence without changing the baseline criteria."""
from argparse import ArgumentParser
import base64
from concurrent.futures import ThreadPoolExecutor
from hashlib import file_digest, sha1, sha256
import json
from pathlib import Path
import subprocess
from zipfile import ZipFile

PARENT = "692c81b161fd436a678cc6d194d86ef15fd8c922f92819ab74ec3e6c633fb55b"
SOURCES = "92e881e72e17b0083c8e082faa0486d9b453c93c5e4080c8b18d2c4c930d3f2e"
NATIVE = "0ded2aed3c4c17c117d675e62c4360bcc015a68d857802b389fba60a9b72210c"
REPO = "maininimassimo-bit/digital-stargate-manual"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def digest(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def pin(data):
    return sha256(data).hexdigest()


def save(path, data):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, sort_keys=True, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")


def local(item, a, content):
    root = a.storage / item["folder"]
    backup = a.backup / item["h"]
    kind = item["kind"]
    leaf = "riepilogo.json" if kind == "native" else "riscontro.json"
    require((root / leaf).read_bytes() == content, "Source receipt differs")
    report = json.loads(content)
    if kind in ("zip", "native"):
        filename = item["folder"] + ".zip"
        archive = digest(root / filename)
        require(digest(backup / filename) == archive and
                archive.startswith(item["h"].rsplit("-",1)[1]), "Archive pin differs")
        with ZipFile(backup / filename) as package:
            require(package.testzip() is None and package.read(leaf) == content, "Archive receipt differs")
            if kind == "native":
                members = [name for name in package.namelist() if name.startswith("stream34-")]
                require(len(members) == 1 and pin(package.read(members[0])) == report["streamReceiptSha256"],
                        "Native checkpoint detached")
        return {"archiveSha256": archive}
    require(kind in ("sampled","continuous") and (backup / leaf).read_bytes() == content,
            "Loose receipt differs")
    acquisition = (backup / "cdn.json").read_bytes()
    require((root / "cdn.json").read_bytes() == acquisition and
            pin(acquisition) == report.get("cdnReceiptSha256", report.get("acquisitionSha256")),
            "CDN receipt detached")
    records = json.loads(acquisition)
    if kind == "continuous":
        records = records["records"]
        require(all(row["multipartETagVerified"] for row in records), "Source integrity missing")
    require(len(records) == (3 if kind == "sampled" else 2), "Unexpected CDN roster")
    for row in records:
        name = row["file"]
        require(Path(name).name == name, "Archive path is not a leaf")
        for directory in (root, backup):
            sample = directory / name
            require(sample.stat().st_size == row["bytes"] and digest(sample) == row["sha256"],
                    "Catalogue bytes differ")
    return {"acquisitionSha256": pin(acquisition), "originalCataloguesVerified": len(records)}


def evidence(item, a, axes):
    label = item["id"]
    if item["commit"]:
        cache = a.readback / (label + ".json")
        if a.mode == "online":
            reply = subprocess.run(["gh", "api", f"repos/{REPO}/contents/{item['path']}?ref={item['commit']}"],
                                   capture_output=True, check=True)
            with cache.open("xb") as stream:
                stream.write(reply.stdout)
        remote = json.loads(cache.read_bytes())
        raw = base64.b64decode("".join(remote["content"].split()), validate=True)
        blob = sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        require(remote["sha"] == blob and remote["path"] == item["path"] and remote["size"] == len(raw),
                "GitHub receipt metadata mismatch")
        location = {"commit": item["commit"], "path": item["path"], "gitBlob": blob}
    else:
        raw = (a.storage / item["folder"] / "riepilogo.json").read_bytes()
        require(item["kind"] == "native" and pin(raw) == NATIVE, "Unexpected local-only evidence")
        location = {"remoteReadback": False}
    stored = local(item, a, raw)
    report = json.loads(raw)
    require(all(axis in axes for axis in item["axes"]), "Unknown axis")
    require(all(report.get(key,0) == 0 for key in ("nativeExecutions","scientificClosures")),
            "Unexpected evidence classification")
    return label, report, dict(axes=item["axes"], sha256=pin(raw), verifiedLocalCopies=2, **location, **stored)


def main():
    parser = ArgumentParser(description=__doc__)
    for field in ("sources","parent","storage","backup","output","readback"):
        parser.add_argument(field,type=Path)
    parser.add_argument("mode",choices=("online","offline"))
    a = parser.parse_args()
    source = a.sources.read_bytes()
    parent = a.parent.read_bytes()
    require(pin(source) == SOURCES and pin(parent) == PARENT, "Pinned ledger or source map differs")
    spec = json.loads(source)
    require(len(spec) == len({row["id"] for row in spec}) == 14, "Evidence roster differs")
    ledger = json.loads(parent)
    require(ledger["status"] == "PROVISIONAL_APPEND_ONLY_DSG_SHARED_V66", "Wrong predecessor")
    scope = ledger["scope"]
    require(tuple(scope[k] for k in ("requirements","criteria","families","axes","ownerCriteriaOpen","scientificClosures"))
            == (4920,14521,7,25,19,0), "Residual scope changed")
    require(len(ledger["axes"]) == 25 and all(v["open"] for v in ledger["axes"].values())
            and len(ledger["ownerCriteria"]) == 19 and
            all(v["status"] == "NOT_YET_SATISFIED" for v in ledger["ownerCriteria"]),
            "Closed requirement or axis")
    require(not any(scope[k] for k in ("completeStudy","completeGitHubTransfer","finalKnowledge")),
            "Unverified completion detected")
    if a.mode == "online":
        a.readback.mkdir()
    with ThreadPoolExecutor(4) as pool:
        checked = list(pool.map(lambda row: evidence(row, a, ledger["axes"]), spec))
    data = {label: report for label, report, _ in checked}
    references = {label: ref for label, _, ref in checked}
    historical = data["historical-rights-reconciliation"]
    queue = data["historical-queue"]
    covariance = data["acs-covariance"]
    aperture = data["acs-aperture"]
    native = data["native-prerequisites"]
    worker = data["isolated-worker"]
    require(not native["admissionRequested"] and not native["authenticatedApprovalsVerified"],
            "Native checkpoint classification changed")
    residual = {star: min(row["minimumFurtherIncreaseAcrossPairs"] for row in target["methods"]
                          if "minimumFurtherIncreaseAcrossPairs" in row)
                for star, target in aperture["targets"].items()}
    result = dict(schema="BKL046_RESIDUAL_KNOWLEDGE_ADDENDUM_V67", parentLedgerSha256=PARENT,
                  sourceMapSha256=SOURCES, scope=scope, evidence=references,
                  historicalDelivery=dict(embeddedReports=queue["embeddedCount"],
                    exactlyIndexedSections=queue["sectionCount"],
                    reviewedHistoricalValues=historical["equalJsonValues"],
                    archivedRightsMatches=historical["archivedCandidatesHashVerified"],
                    redistributionClearanceEstablished=historical["redistributionClearanceEstablished"],
                    completeGitHubTransfer=False),
                  gaiaACS=dict(fixedWindowFailures=data["gaia-cohort-failure"]["fixedWindowFailures"],
                    fixedWindowDeletionsPassing=data["gaia-mask"]["fixedMasksPassing"],
                    verifiedObservedComparisons=data["acs-observed"]["independentInstrumentObservedComparisons"],
                    standardFormalNarrowRatioSigmas={star: row["ratios"]["F658N/F660N"]["full"]["conditional"]
                                                   for star,row in covariance["targets"].items()},
                    lowerAdditionalIncreaseAmongObservedApertures=residual,
                    independentAbsoluteCalibrationEstablished=False),
                  isolatedIA=dict(syntheticTickets=worker["syntheticTickets"],
                    syntheticClaims=worker["verifiedFixtureClaims"],
                    independentConfirmationUnits=worker["independentConfirmationUnits"]),
                  nativePreparation=dict(verifiedArchiveMembers=native["verifiedArchiveMembers"],
                    measuredMemoryIsSnapshot=native["memorySnapshotOnly"],
                    authenticatedApprovalsVerified=False, admissionRequested=False,
                    cfaProductionDirectoryExists=native["cfaProductionDirectoryExists"]),
                  remoteEvidenceReadbacks=sum(bool(row["commit"]) for row in spec),
                  localOnlyEvidence=1, finalKnowledgePublished=False, scientificClosures=0)
    ledger["status"] = "PROVISIONAL_APPEND_ONLY_DSG_SHARED_V67"
    ledger["parentV66Sha256"] = PARENT
    ledger["evidenceSinceV67"] = result
    save(a.output / "conoscenza.json", result)
    save(a.output / "rendiconto-VM-v67.json", ledger)


if __name__ == "__main__":
    main()
