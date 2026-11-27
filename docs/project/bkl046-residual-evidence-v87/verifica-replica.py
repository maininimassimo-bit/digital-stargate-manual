"""Build or audit the BKL-046 v87 increment from exact archived reports."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

PARENT = "4588fdb9eec3b88ee6a820f6322d158019819c4386a3c46ca84c463654263e22"
INDEX = "a92f9f372cb05328abc64bfb1f8b00db812d61dea27aa6ec645d972bbfff95f3"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read(path, pin=None):
    raw = path.read_bytes()
    if pin is not None:
        need(sha256(raw).hexdigest() == pin, f"SHA-256 mismatch: {path.name}")
    return json.loads(raw)


def facts(reports):
    join = reports[("joinedDelivery", "esito.json")]
    flat = reports[("asiFlatBilinear", "riscontro.json")]
    held = reports[("asiFlatHeldPairs", "riscontro.json")]
    roman = reports[("romanRamp", "riscontro.json")]
    all_channels = reports[("romanAllChannels", "riscontro.json")]
    need(join["scope"] == "offline" and not join["githubReadbackAndReplayVerified"]
         and not join["scientificCompletionVerified"]
         and join["knowledgeCapsuleRecovered"] and join["logicalCorpusReconstructionVerified"],
         "Delivery evidence scope changed")
    need((join["verifiedAssetCount"], join["verifiedObjects"], join["verifiedLogicalAliases"])
         == (81, 10180, 11839), "Delivery coverage changed")
    need(not roman["incidentDoseVerified"] and not all_channels["incidentDoseVerified"]
         and not roman["fullFitsHashesVerified"] and not all_channels["fullFitsHashesVerified"],
         "Roman evidence scope changed")
    need(flat["pairTileParityCases"] == 252 and held["heldOutPairs"] == 7
         and held["trainingPairsPerFold"] == 6, "Flat coverage changed")
    need(len(all_channels["rows"]) == 960 and all_channels["verifiedParentVarianceComparisons"] == 60,
         "Roman channel coverage changed")
    return dict(
        asiFlatBilinear=flat["summary"],
        asiFlatHeldPairCovariance=held["summary"],
        romanSignalLevels=roman["summary"],
        romanChannelCoverage=[{k:r[k] for k in ("frame","comparisons","channelsWithLowerFullError",
                         "aggregateFullErrorMedian","aggregateDiagonalErrorMedian")} for r in all_channels["summary"]],
        romanStorageRailMasks=all_channels["supports"],
        localDeliveryReconstruction={k:join[k] for k in ("verifiedAssetCount","verifiedAssetBytes",
             "verifiedObjects","verifiedLogicalAliases","recoveredObjectsSha256","logicalAliasMapSha256",
             "githubReadbackAndReplayVerified")})

def generate(root):
    src = root / "fonti"
    parent = read(src / "v86.json", PARENT)
    prior_knowledge = read(src / "conoscenza-v86.json", "3dc1adde6501059918f9df686f801d9c7dc25c8b3dfb4b260fb3fce99e909d51")
    index = read(src / "indice-v86.json", INDEX)
    need(parent["schema"] == "BKL046_RESIDUAL_EVIDENCE_APPENDIX_V86"
         and prior_knowledge["baselineVersion"] == parent["baselineKnowledge"] == "1.171"
         and index["releaseState"] == "INTERIM_REGISTERED_BASELINE", "Parent scope changed")
    evidence = read(src / "evidenze-v87.json", "8f69c75de88d8928a0a8470f0353ee25009e1e3cde427cdaf2bca79dd2a24eb7")
    need(len(evidence)==5 and sum(len(row["reports"]) for row in evidence)==5, "Source coverage differs")
    report_data={}
    for row in evidence:
        for report in row["reports"]:
            actual=read(src/report["copiedReport"],report["sha256"])
            if row["id"] != "joinedDelivery":
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
    ledger = dict(parent, schema="BKL046_RESIDUAL_EVIDENCE_APPENDIX_V87", parentLedgerSha256=PARENT,
                  evidence=combined, axes=axes)
    need(ledger["scientificClosuresAdded"] == ledger["nativeExecutionsAdded"] == 0 and
         not ledger["finalKnowledgeAccepted"] and not ledger["completeGithubTransferVerified"], "Completion changed")
    knowledge = dict(
        schema="BKL046_KNOWLEDGE_V1171_SUPPLEMENT_V87", baselineVersion="1.171",
        baselineCapsuleSha256=prior_knowledge["baselineCapsuleSha256"],
        parentLedger=dict(sha256=PARENT, commit="d4f6283a68e87474c1f042fe71a55023e7b0d8f9"),
        sourceIndex=dict(sha256=INDEX, commit="61025f123d5c9efc797a853ab984eafe73dddfc8"),
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
    print(json.dumps(dict(sourceReports=5, scientificStudies=4, operationalReports=1,
                          axesOpen=25, ownerCriteriaOpen=19, scientificClosures=0)))


if __name__ == "__main__":
    main()