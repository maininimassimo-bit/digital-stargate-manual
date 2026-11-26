"""Build or audit the BKL-046 v89 increment from exact archived reports."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

PARENT = "2d91c2aba2a359271ec2c8a4e958f874aee1d7a8517800d4ad962e5c6994b115"
INDEX = "ddfe335801ed5559a778674eaa61c8f32597cafbc9f463789dbc71a256adc5db"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read(path, pin=None):
    raw = path.read_bytes()
    if pin is not None:
        need(sha256(raw).hexdigest() == pin, f"SHA-256 mismatch: {path.name}")
    return json.loads(raw)


def facts(reports):
    cross = reports[("romanLin0Cross", "riscontro.json")]
    matched = reports[("romanLin0Signal", "riscontro.json")]
    matrix = reports[("ownerCriteriaV3", "BKL-046-MATRICE-CRITERI-v3.json")]
    permutation = reports[("m8GreenPermutation", "riscontro.json")]
    green = reports[("m8GreenZone", "riscontro.json")]
    ngc = reports[("ngc6341Zone", "riscontro.json")]
    uncertainty = reports[("ngc6341ZoneBootstrap", "riscontro.json")]
    need(not cross["calibratedDoseMatched"] and not matched["calibratedDoseMatched"]
         and sum(r["measured"] for r in cross["summary"]) == 2880
         and sum(r["signalMatched"] for r in matched["summary"]) == 960
         and sum(r["outsideGainRange"] for r in matched["summary"]) == 1920, "Roman scope")
    need(len(matrix["criteria"]) == matrix["openCriteria"] == 19 and matrix["criteriaPromoted"] == 0
         and all(r["status"] == "NOT_YET_SATISFIED" for r in matrix["criteria"]), "Owner criteria scope")
    within = permutation["reports"]["A"]["zoneConstrained"]
    need(within["assignments"] == within["atLeastObservedAgreements"] == 48
         and permutation["independentReplications"] == 0 and green["verifiedParentGreenFits"] == 76,
         "Green parity scope")
    need(len(ngc["rows"]) == 1472 and sum(r["state"] == "MEASURED" for r in ngc["rows"]) == 1466
         and uncertainty["replicates"] == 9999 and not uncertainty["fieldPopulationInferenceVerified"],
         "NGC 6341 scope")
    return dict(
        romanLin0CrossSession=cross["summary"], romanSignalOverlap=matched["summary"],
        greenZoneAssignment=within, greenHeldExposure=green["summary"], ngc6341HeldExposure=ngc["summary"],
        ngc6341Resampling=[dict(chip=row["chip"], stars=row["stars"], zones=len(row["zoneSizes"]), stats=row["stats"])
                           for row in uncertainty["chips"]],
        ownerCriteria=[dict(id=r["id"], status=r["status"], nextVerification=r["nextVerification"])
                       for r in matrix["criteria"]])

def generate(root):
    src = root / "fonti"
    parent = read(src / "v88.json", PARENT)
    prior_knowledge = read(src / "conoscenza-v88.json", "89483f9766405520aefbf67fd89b5b2f24c8b6b40826e5d4a1386afdf467685c")
    index = read(src / "indice-v88.json", INDEX)
    need(parent["schema"] == "BKL046_RESIDUAL_EVIDENCE_APPENDIX_V88"
         and prior_knowledge["baselineVersion"] == parent["baselineKnowledge"] == "1.171"
         and index["releaseState"] == "INTERIM_REGISTERED_BASELINE", "Parent scope changed")
    evidence = read(src / "evidenze-v89.json", "a67aad0f9f8a032bd135e5e47f5ae0a94a58e704205667ef7662e882cbfb4394")
    need(len(evidence)==7 and sum(len(row["reports"]) for row in evidence)==7, "Source coverage differs")
    report_data={}
    for row in evidence:
        for report in row["reports"]:
            actual=read(src/report["copiedReport"],report["sha256"])
            if row["id"] != "ownerCriteriaV3":
                need(actual["scientificClosures"]==actual["nativeExecutions"]==0,"Source scope changed")
            job=(row["id"],report["archiveMember"])
            need(job not in report_data, "Duplicate archived result")
            report_data[job]=actual
    coverage = parent["coverage"]
    need(coverage == dict(requirements=4920, criteria=14521, ownerCriteriaOpen=19,
                          scientificFamiliesOpen=7, scientificAxesOpen=25, scientificClosures=0),
         "Coverage changed")
    need(set(axis for row in evidence for axis in row["axes"]) == {"NOISE_FLUX/1", "NOISE_FLUX/3", "PSF_PIXEL/2", "PSF_PIXEL/3"}
         and len(parent["axes"]) == 25 and all(row["open"] for row in parent["axes"])
         and len(parent["ownerCriteria"]) == 19
         and all(row["status"] == "NOT_YET_SATISFIED" for row in parent["ownerCriteria"]), "Residual scope differs")
    combined = parent["evidence"] + evidence
    need(len(combined) == len({row["id"] for row in combined}), "Duplicate evidence identity")
    axes = [{**row, "newEvidence": row["newEvidence"] +
             [item["id"] for item in evidence if row["id"] in item["axes"]]} for row in parent["axes"]]
    ledger = dict(parent, schema="BKL046_RESIDUAL_EVIDENCE_APPENDIX_V89", parentLedgerSha256=PARENT,
                  evidence=combined, axes=axes)
    need(ledger["scientificClosuresAdded"] == ledger["nativeExecutionsAdded"] == 0 and
         not ledger["finalKnowledgeAccepted"] and not ledger["completeGithubTransferVerified"], "Completion changed")
    knowledge = dict(
        schema="BKL046_KNOWLEDGE_V1171_SUPPLEMENT_V89", baselineVersion="1.171",
        baselineCapsuleSha256=prior_knowledge["baselineCapsuleSha256"],
        parentLedger=dict(sha256=PARENT, commit="5c188d61a0ed4fcc62c8d5f283607e95646f8a32"),
        sourceIndex=dict(sha256=INDEX, commit="9bc191f5483c9730d15a8b1489467018df5ea18a"),
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
    print(json.dumps(dict(sourceReports=7, scientificStudies=6, operationalReports=1,
                          axesOpen=25, ownerCriteriaOpen=19, scientificClosures=0)))


if __name__ == "__main__":
    main()