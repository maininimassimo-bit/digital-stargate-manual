"""Bind attribution of the v571 Gaia products to exact archived bytes."""
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile

spec_path, capsule, provenance, embedded, readback, output = map(Path, sys.argv[1:])
spec = json.loads(spec_path.read_bytes())


def file_hash(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_report(path, expected):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == expected, f"Changed receipt {path.name}")
    return json.loads(raw)


def read_member(archive, member, expected):
    require(archive.namelist().count(member) == 1, "Missing or duplicate ZIP member")
    data = archive.read(member)
    require(len(data) == expected["bytes"] and sha256(data).hexdigest() == expected["sha256"],
            f"Changed member {member}")
    return data


require(file_hash(capsule) == spec["capsule"], "Changed v571 capsule")
previous = read_report(provenance, spec["provenance"])
legacy = read_report(embedded, spec["embeddedInventory"])
capsule_receipt = read_report(readback, spec["capsuleReadback"])
require(legacy["knowledgeSha256"] == capsule_receipt["knowledgeSha256"], "Different knowledge subjects")

records = previous["esaProducts"]["records"]
roots = [x for x in records if "::" not in x["member"]]
require(len(roots) == 2 and len(records) == 4, "Unexpected product catalogue")
archive_name = "objects/Prove-GaiaXPy-campionamento-reale-v3.zip"
matrix_name = "Matrici-GaiaXPy-campionamento-reale-v1.npz"
products = {}
with ZipFile(capsule) as outer:
    raw_evidence = read_member(outer, archive_name, capsule_receipt["verifiedMembers"][archive_name])
    with ZipFile(BytesIO(raw_evidence)) as evidence:
        protocol = json.loads(evidence.read("real/Protocollo-GaiaXPy-campionamento-reale-v1.json"))
        for product, source in spec["products"].items():
            matches = [row for row in roots if "Source-ESA-" + product + "-" in row["member"]]
            require(len(matches) == 1, f"Different mapping for {product}")
            wrapper, = matches
            children = [row for row in records if row["member"].startswith(wrapper["member"] + "::")]
            require(len(children) == 1, "Unexpected derived XML index")
            xml, = children
            with ZipFile(BytesIO(read_member(evidence, wrapper["member"], wrapper))) as content:
                member = xml["member"].split("::")[1]
                require(content.namelist() == [member], "Unexpected DataLink delivery")
                read_member(content, member, xml)
            require(any(row["file"] == Path(wrapper["member"]).name and row["sha256"] == wrapper["sha256"]
                        for row in protocol["inputs"]), "Missing analysis dependency")
            products[product] = dict(archiveMember=wrapper["member"], wrapperSha256=wrapper["sha256"],
                                     innerMember=member, xmlSha256=xml["sha256"], **source)
        matrix_member = "objects/" + matrix_name
        meta = capsule_receipt["verifiedMembers"][matrix_member]
        read_member(outer, matrix_member, meta)
        for prefix in ("real/", "output/"):
            read_member(evidence, prefix + matrix_name, meta)

require(protocol["sourceId"] == "4458990005388621952", "Unexpected Gaia source")
report = dict(schema="BKL046_V571_GAIA_ATTRIBUTION_SCOPE_V1", sourceId=protocol["sourceId"],
              credit="ESA/Gaia/DPAC", dataReuseLicense=spec["license"], products=products,
              esaCreditTerms=spec["esaCredit"], archiveGeneralRightsReference=spec["esaArchiveRightsExample"],
              publications=spec["citations"], separateSoftwareLicense=spec["softwareLicense"],
              upstreamSoftwareFilesPreviouslyVerified=len(previous["sourceFiles"]),
              pinnedCapsuleSha256=spec["capsule"], embeddedKnowledgeSha256=legacy["knowledgeSha256"],
              embeddedReportsInHistoricalInventory=legacy["evidenceObjects"],
              embeddedReportsMatchedToPriorRightsInventory=legacy["matchingPriorRightsAudit"],
              derivativeMatrix=dict(sha256=meta["sha256"], verifiedOccurrences=3),
              scopeStatus="PRODUCT_ATTRIBUTION_VERIFIED_MIXED_CAPSULE_DISTRIBUTION_UNRESOLVED",
              completeRedistributionClearanceEstablished=False, scientificClosures=0)
with output.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, sort_keys=True, indent=2, allow_nan=False)
    stream.write("\n")
