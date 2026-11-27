"""Build or audit the BKL-046 v86 increment from exact archived reports."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

PARENT = "a7749273a2c38f5a40033811be173f997fdbe14fb45cdc52ac4399075de6ea57"
INDEX = "4c123b394c29ac869c24440077614949e0624ce87b7a5b70bf930acd581f92ef"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read(path, pin=None):
    raw = path.read_bytes()
    if pin is not None:
        need(sha256(raw).hexdigest() == pin, f"SHA-256 mismatch: {path.name}")
    return json.loads(raw)


def facts(reports):
    epochs = reports[("grw70Epoch", "riscontro.json")]
    tables = reports[("officialEE", "riscontro.json")]
    fields = reports[("clusterEE", "riscontro.json")]
    registration = reports[("clusterRegistration", "riscontro.json")]
    sky = reports[("clusterSky", "riscontro.json")]
    screen = reports[("p177p041Availability", "riscontro.json")]
    endpoints = reports[("p177p041Availability", "riscontro-endpoint.json")]
    need(not epochs["causalChipEffectVerified"] and not tables["independentCalibrationVerified"]
         and not fields["fieldPopulationInferenceVerified"] and not registration["absoluteAstrometricReferenceVerified"]
         and not sky["backgroundTruthVerified"], "Evidence scope changed")
    need(screen["counts"] == {"NO_PUBLIC_FLC": 9} and screen["qualifiedVisits"] == []
         and len(endpoints["rows"]) == endpoints["notFound"] == 21 and endpoints["verifiedAvailable"] == 0,
         "FLC evidence changed")
    return dict(
        temporalMatching=[dict(coverage=row["coverage"], windowDays=row["windowDays"], pairs=len(row["pairs"]),
                               apertureGrowthSummary=row["apertureGrowthSummary"]) for row in epochs["temporalMatching"]],
        officialTableComparison=tables["summary"],
        externalFields=[dict(target=row["target"], visit=row["visit"], state=row["state"]) for row in fields["fields"]],
        registration=[dict(chip=row["chip"], summary=row["summary"]) for row in registration["chips"]],
        sky=[dict(chip=row["chip"], summary=row["summary"]) for row in sky["chips"]],
        calibratorAvailability=dict(associations=screen["counts"], directHttp404=endpoints["notFound"],
                                    qualifiedVisits=screen["qualifiedVisits"]))

def generate(root):
    src = root / "fonti"
    parent = read(src / "v85.json", PARENT)
    prior_knowledge = read(src / "conoscenza-v85.json", "beeb4d7763c9e9d2521c00b387b4bbd1716a6c68216ef91d4c1fc9d7243a374c")
    index = read(src / "indice-v85.json", INDEX)
    need(parent["schema"] == "BKL046_RESIDUAL_EVIDENCE_APPENDIX_V85"
         and prior_knowledge["baselineVersion"] == parent["baselineKnowledge"] == "1.171"
         and index["releaseState"] == "INTERIM_REGISTERED_BASELINE", "Parent scope changed")
    evidence = read(src / "evidenze-v86.json", "ddb1fd88c044f8ca2127cba1c88b5c932601440385bc8544ea9b7f31c8c70ec0")
    need(len(evidence)==6 and sum(len(row["reports"]) for row in evidence)==7, "Source coverage differs")
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
    need(set(axis for row in evidence for axis in row["axes"]) == {"FILTER_COLOR/3", "FILTER_COLOR/4"}
         and len(parent["axes"]) == 25 and all(row["open"] for row in parent["axes"])
         and len(parent["ownerCriteria"]) == 19
         and all(row["status"] == "NOT_YET_SATISFIED" for row in parent["ownerCriteria"]), "Residual scope differs")
    combined = parent["evidence"] + evidence
    need(len(combined) == len({row["id"] for row in combined}), "Duplicate evidence identity")
    axes = [{**row, "newEvidence": row["newEvidence"] +
             [item["id"] for item in evidence if row["id"] in item["axes"]]} for row in parent["axes"]]
    ledger = dict(parent, schema="BKL046_RESIDUAL_EVIDENCE_APPENDIX_V86", parentLedgerSha256=PARENT,
                  evidence=combined, axes=axes)
    need(ledger["scientificClosuresAdded"] == ledger["nativeExecutionsAdded"] == 0 and
         not ledger["finalKnowledgeAccepted"] and not ledger["completeGithubTransferVerified"], "Completion changed")
    knowledge = dict(
        schema="BKL046_KNOWLEDGE_V1171_SUPPLEMENT_V86", baselineVersion="1.171",
        baselineCapsuleSha256=prior_knowledge["baselineCapsuleSha256"],
        parentLedger=dict(sha256=PARENT, commit="b802d5bbd2c326f53832e5a10c52971b3dddb6c7"),
        sourceIndex=dict(sha256=INDEX, commit="019db5457acc35d2cc6448a91ff744a80cd57354"),
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
    print(json.dumps(dict(sourceReports=7, scientificStudies=6,
                          axesOpen=25, ownerCriteriaOpen=19, scientificClosures=0)))


if __name__ == "__main__":
    main()