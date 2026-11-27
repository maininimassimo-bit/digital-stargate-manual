"""Derive bounded usage decisions from the pinned historical GaiaXPy reports."""
from collections import Counter
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import re
import sys
from zipfile import ZipFile

CAPSULE = "b206e8ec180be461948fe5a55027e1677a52377cf838481ab3bb2666067c55e4"
INDEX = "23bbdf2979d549d8e35db428b0c01c8b81c088086f3ef50c6b0083af3627e3f3"
RECEIPT = "0ee5399abeb0dd2f4d727005c91e1664ef47a6412d3711ef24368540f3c02e40"
INNER = "Prove-GaiaXPy-campionamento-reale-v3.zip"
CATEGORIES = {
    673: "UPSTREAM_SOFTWARE_SOURCE_INVENTORY",
    674: "SYNTHETIC_SOFTWARE_CONTRACT_PROTOCOL",
    675: "CATALOGUE_DIAGNOSTIC_PROTOCOL",
    681: "MIXED_HISTORICAL_REGISTER",
    682: "UPSTREAM_SOFTWARE_TREE_METADATA",
    683: "SYNTHETIC_SOFTWARE_CONTRACT_RESULT",
    684: "CATALOGUE_DERIVED_NUMERIC_DIAGNOSTIC",
    690: "CATALOGUE_DERIVED_NUMERIC_VERIFICATION",
    699: "CATALOGUE_DERIVED_RANK_PROTOCOL",
    700: "CATALOGUE_DERIVED_RANK_RESULT",
    705: "MIXED_CORRELATION_PROTOCOL",
    706: "MIXED_CORRELATION_RESULT",
    707: "MIXED_CORRELATION_WITNESSES",
    708: "MIXED_ARCHIVE_VERIFICATION",
}
LOCAL_REFERENCE = re.compile(r"(?i)(?:[A-Z]:\\|\\\\)[^\s]+")


def require(ok, label):
    if not ok:
        raise ValueError(label)


def checked_json(path, pin):
    data = path.read_bytes()
    require(sha256(data).hexdigest() == pin, "Pinned input changed")
    return json.loads(data)


def local_reference_count(value):
    if isinstance(value, dict):
        return sum(local_reference_count(key) + local_reference_count(val)
                   for key, val in value.items())
    if isinstance(value, list):
        return sum(map(local_reference_count, value))
    return int(isinstance(value, str) and bool(LOCAL_REFERENCE.search(value)))


def main():
    capsule, index, previous, output = map(Path, sys.argv[1:])
    with capsule.open("rb") as stream:
        require(file_digest(stream, "sha256").hexdigest() == CAPSULE, "Capsule changed")
    index = checked_json(index, INDEX)
    previous = checked_json(previous, RECEIPT)
    bindings = {row["ordinal"]: row for row in previous["entries"]}
    require(set(bindings) == set(CATEGORIES), "Previous correspondence set changed")
    values = {}
    review = []
    with ZipFile(capsule) as z:
        with ZipFile(BytesIO(z.read("objects/" + INNER))) as nested:
            for row in index:
                number = row["ordinal"]
                if number not in bindings:
                    continue
                candidate = row["priorAuditMatches"][0]["name"]
                prefix, separator, filename = candidate.partition("::")
                if separator:
                    require(prefix == INNER, "Unexpected child archive")
                raw = nested.read(filename) if separator else z.read(prefix)
                binding = bindings[number]
                require(binding["sourceSha256"] == row["sourceSha256Declared"]
                        == sha256(raw).hexdigest() and binding["jsonValueEqual"]
                        and binding["priorStatuses"] == ["NOT_YET_QUALIFIED"],
                        "Historical source or status changed")
                obj = json.loads(raw)
                values[number] = obj
                review.append({"ordinal": number, "sourceSha256": binding["sourceSha256"],
                               "contentClassification": CATEGORIES[number],
                               "localReferenceStringCount": local_reference_count(obj),
                               "historicalRightsStatus": "NOT_YET_QUALIFIED"})
    require(set(values) == set(CATEGORIES), "Source coverage differs")
    require(all(values[n].get("scientificAdmission") is False for n in (683, 684, 690, 700, 706, 707, 708)),
            "Unexpected admission status")
    candidate = values[684]
    rank = values[700]
    expected_cases = {"artificial3", "candidate343"}
    cases = {row["case"]: row for row in values[706]["cases"]}
    witnesses = {row["case"]: row for row in values[707]["witnesses"]}
    require(set(cases) == set(witnesses) == expected_cases and len(values[706]["cases"]) == 2
            and len(values[707]["witnesses"]) == 2, "Correlation case roster differs")
    require(values[683]["realCatalogPropagationTested"] is False
            and candidate["solutionIdsIdentical"] is False
            and candidate["basisIdCompatibilityIndependentlyEstablished"] is False,
            "Unexpected source applicability")
    require(rank["fullInverseAdmitted"] is False and rank["systematicCovarianceAbsent"] is True
            and rank["samples"] == candidate["sampleCount"]
            and 0 < rank["positiveEigenvaluesAboveTolerance"] <= rank["algebraicRankUpperBound"] < rank["samples"],
            "Unexpected rank applicability")
    require(values[705]["numpyBranchOnly"] is True and all(
        cases[key]["unpackedCorrelationExactlySymmetric"] is True
        and cases[key]["negativeCorrelationEigenvaluesBelowTolerance"] > 0
        and witnesses[key]["negativeVarianceCertificateForPackedCorrelation"] is True
        and witnesses[key]["negativeQuadraticForm"] < 0
        for key in expected_cases), "Unexpected covariance witnesses")
    report = {
        "schema": "BKL046_V1146_GAIA_SEMANTIC_REVIEW_V1",
        "recordsReviewed": len(review),
        "recordsWithLocalReferenceMarkers": sum(row["localReferenceStringCount"] > 0 for row in review),
        "sourceRecords": review,
        "priorReconciliationSha256": RECEIPT,
        "technicalDecisions": {
            "sameCatalogueAgreementIsDiagnostic": True,
            "physicalFilterResponseEstablished": False,
            "modelBasisCompatibilityEstablished": False,
            "fullCovarianceInverseAdmitted": False,
            "packedCorrelationNegativeWitnesses": len(witnesses),
            "fullPackageExportQualified": False,
        },
        "linkedAxesRemainsOpen": ["FILTER_COLOR/1", "FILTER_COLOR/2", "FILTER_COLOR/4", "VERSION_BACKEND/3"],
        "redistributionClearanceEstablished": False,
        "scientificClosures": 0,
    }
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
