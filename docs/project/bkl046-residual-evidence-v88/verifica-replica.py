"""Build or audit the BKL-046 v88 increment from exact archived reports."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

PARENT = "eedceadaffb617d0ce402dcb75fc4504dc2673b83c88ad3738f8d5c8adc5983e"
INDEX = "0274d7fb2a2550f652b3d3e7d4c2912672b92dc77ef0a97ce3271e66adda605f"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read(path, pin=None):
    raw = path.read_bytes()
    if pin is not None:
        need(sha256(raw).hexdigest() == pin, f"SHA-256 mismatch: {path.name}")
    return json.loads(raw)


def facts(reports):
    entry = reports[("streamV11DeploymentPeer", "riscontro.json")]
    spatial = reports[("romanSpatialBands", "riscontro.json")]
    mct = reports[("romanGainPhotodiode", "riscontro.json")]
    dark = reports[("romanNoiwMct", "riscontro.json")]
    direction = reports[("romanDirectional", "riscontro.json")]
    held = reports[("romanHeldPairs", "riscontro.json")]
    need(entry["simulatedHeartbeatThroughDeployment"] and len(entry["rejections"]) == 8
         and not entry["independentApprovalsReceived"] and not entry["productionEnrollment"]
         and not entry["nativeAdmissionRequested"], "Stream34 evidence scope changed")
    need(spatial["newRanges"] == 160 and len(spatial["summary"]) == 9
         and not spatial["incidentDoseVerified"] and not spatial["fullFitsHashesVerified"], "Spatial coverage changed")
    need(mct["summary"]["exposures"] == 21 and dark["summary"]["noiwExposures"] == 39
         and not mct["calibratedDoseVerified"] and not dark["calibratedDoseVerified"]
         and not dark["transferredOffsetVerified"], "Dose evidence scope changed")
    need(direction["comparisons"] == 9600 and direction["halfHalfParentComparisons"] == 1920
         and held["verifiedParentComparisons"] == 1920 and held["trainingPairsPerFold"] == 9,
         "Directional or held pair coverage changed")
    return dict(
        romanSpatialBands=[{k:v for k,v in r.items() if k!="byChannel"} for r in spatial["summary"]],
        romanPhotodiode=mct["summary"], romanDarkMonitor=dark["summary"],
        romanDirectionSensitivity=direction["summary"], romanHeldPairCovariance=held["summary"],
        stream34V11DeploymentPeer=entry)

def generate(root):
    src = root / "fonti"
    parent = read(src / "v87.json", PARENT)
    prior_knowledge = read(src / "conoscenza-v87.json", "600fdc179363ddf6fbb05f716870b2d1208c13bde483ee3301a8dcdc394881e6")
    index = read(src / "indice-v87.json", INDEX)
    need(parent["schema"] == "BKL046_RESIDUAL_EVIDENCE_APPENDIX_V87"
         and prior_knowledge["baselineVersion"] == parent["baselineKnowledge"] == "1.171"
         and index["releaseState"] == "INTERIM_REGISTERED_BASELINE", "Parent scope changed")
    evidence = read(src / "evidenze-v88.json", "f95426be20d2ec9f7615bbcafad4fc210b67b4e0be27728fbeb1af76eb1a0b05")
    need(len(evidence)==6 and sum(len(row["reports"]) for row in evidence)==6, "Source coverage differs")
    report_data={}
    for row in evidence:
        for report in row["reports"]:
            actual=read(src/report["copiedReport"],report["sha256"])
            need(actual["scientificClosures"]==actual["nativeExecutions"]==0,"Source scope changed")
            job=(row["id"],report["archiveMember"])
            need(job not in report_data, "Duplicate archived result")
            report_data[job]=actual
    coverage = parent["coverage"]
    need(coverage == dict(requirements=4920, criteria=14521, ownerCriteriaOpen=19,
                          scientificFamiliesOpen=7, scientificAxesOpen=25, scientificClosures=0),
         "Coverage changed")
    need(set(axis for row in evidence for axis in row["axes"]) == {"NOISE_FLUX/1", "NOISE_FLUX/2", "NOISE_FLUX/3"}
         and len(parent["axes"]) == 25 and all(row["open"] for row in parent["axes"])
         and len(parent["ownerCriteria"]) == 19
         and all(row["status"] == "NOT_YET_SATISFIED" for row in parent["ownerCriteria"]), "Residual scope differs")
    combined = parent["evidence"] + evidence
    need(len(combined) == len({row["id"] for row in combined}), "Duplicate evidence identity")
    axes = [{**row, "newEvidence": row["newEvidence"] +
             [item["id"] for item in evidence if row["id"] in item["axes"]]} for row in parent["axes"]]
    ledger = dict(parent, schema="BKL046_RESIDUAL_EVIDENCE_APPENDIX_V88", parentLedgerSha256=PARENT,
                  evidence=combined, axes=axes)
    need(ledger["scientificClosuresAdded"] == ledger["nativeExecutionsAdded"] == 0 and
         not ledger["finalKnowledgeAccepted"] and not ledger["completeGithubTransferVerified"], "Completion changed")
    knowledge = dict(
        schema="BKL046_KNOWLEDGE_V1171_SUPPLEMENT_V88", baselineVersion="1.171",
        baselineCapsuleSha256=prior_knowledge["baselineCapsuleSha256"],
        parentLedger=dict(sha256=PARENT, commit="8369fa4a3ea86dcf9f07fa3794045d84d82c70a8"),
        sourceIndex=dict(sha256=INDEX, commit="85a44fb74b8b975678f3e9485cf7280ffa25fce3"),
        evidence=evidence, coverage=coverage, findings=facts(report_data),
        finalKnowledgeAccepted=False, completeGithubTransferVerified=False)
    return {"rendiconto.json": ledger, "conoscenza.json": knowledge}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    generated = generate(args.root)
    for name, document in generated.items():
        expected = (json.dumps(document, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
        path = args.root / name
        if args.build:
            with path.open("xb") as output:
                output.write(expected)
        need(path.read_bytes() == expected, f"Regenerated document differs: {name}")
    print(json.dumps(dict(sourceReports=6, scientificStudies=5, operationalReports=1,
                          axesOpen=25, ownerCriteriaOpen=19, scientificClosures=0)))


if __name__ == "__main__":
    main()