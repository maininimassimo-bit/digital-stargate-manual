"""Bind the GitHub release readback to reconstructing the same v600 corpus."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

PINS = {
    "subject": "ca6ac2dba26e90704bd583d1073744079b9e889a4fc95cc38895d702cab815d1",
    "inventory": "48262824c9472647d47218c77e0fccc579ce04a9436e8219be42623bbf8b31e6",
    "plan": "cb30745073d1a69003e41b78da1948ef3093508b9a7ed5f97d3cf01b2827e90a",
    "index": "337de0761a1e104da130c1bdef0300b5855789e32e3e745a240fe9cb0091d090",
    "readback_verifier": "a3ea715b0189852fc862ed7172d4171ee3dda097d918ceeba43a76fda30257db",
    "logical_verifier": "21ca53b67615e776624d7cd44b43747418e9200d860ee5fbfcc6bbed954dae5e",
}
EXPECTED_LOGICAL = {
    "schema": "BKL046_FULL_LOGICAL_REPLAY_V1",
    "inventorySha256": PINS["inventory"], "planSha256": PINS["plan"], "indexSha256": PINS["index"],
    "source": "PROVIDED_ASSET_DIRECTORY", "verifiedCarrierFiles": 80,
    "verifiedCarrierBytes": 27478864996, "verifiedObjects": 10180,
    "verifiedObjectBytes": 103872890757, "verifiedLogicalAliases": 11839, "verifiedJobs": 71,
    "recoveredObjectsSha256": "e2b18426df4b6ed8f9750db39e40f3189807d429c187c78d95b65e1eb685ac8d",
    "logicalAliasMapSha256": "457df7abbfd375e24bd45aaa43bbc362630fe6eeb1ee7cbe0ac078f1f264c097",
    "githubTransferVerifiedByThisRun": False,
}


def require(condition, code):
    if not condition:
        raise ValueError(code)


def checked(path, name):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PINS[name], "INPUT_PIN:" + name)
    return raw


def expected_assets(subject, inventory):
    listed = {a["name"]: a for a in subject["assets"]}
    transport = {a["name"]: a for a in inventory["assets"]}
    cap = subject["knowledge"]["assetName"]
    require(len(listed) == len(subject["assets"]) == 81, "RELEASE_SUBJECT_COVERAGE")
    require(len(transport) == len(inventory["assets"]) == 80, "INVENTORY_COVERAGE")
    require(set(listed) == {*transport, cap} and cap not in transport, "CAPSULE_OR_SET")
    require(all(listed[name] == pin for name, pin in transport.items()), "TRANSPORT_PINS")
    require(subject["totalBytes"] == sum(row["bytes"] for row in listed.values()), "RELEASE_TOTAL")
    return listed, transport


def bind_results(args, subject, inventory, remote, logical, last_snapshot):
    listed, _ = expected_assets(subject, inventory)
    identity = dict(repository=args.repository, repositoryId=args.repository_id,
                    visibility=args.visibility, releaseId=args.release_id, tag=args.tag)
    require(all(remote.get(k) == v for k, v in identity.items()), "RELEASE_IDENTITY")
    require(remote.get("allAssetBytesVerified") is True
            and remote.get("knowledgeCapsuleRecovered") is True
            and remote.get("downloadedBytes") == subject["totalBytes"], "READBACK_STATUS")
    metadata = remote["assets"]
    require(metadata == last_snapshot and set(metadata) == set(listed), "RELEASE_SNAPSHOT_CHANGED")
    ids = set()
    for name, data in metadata.items():
        aid = data["id"]
        require(type(aid) is int and aid > 0 and aid not in ids, "ASSET_IDENTITY")
        require(data["size"] == listed[name]["bytes"] and data["state"] == "uploaded", "ASSET_METADATA")
        require(data["digest"] in (None, "sha256:" + listed[name]["sha256"]), "ASSET_DIGEST")
        ids.add(aid)
    require(logical == EXPECTED_LOGICAL, "LOGICAL_MAPPING_OR_SOURCE")
    return identity


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("subject", "inventory", "plan", "index", "readback_verifier", "logical_verifier"):
        parser.add_argument(key, type=Path)
    parser.add_argument("repository")
    parser.add_argument("repository_id", type=int)
    parser.add_argument("visibility", choices=("private", "public"))
    parser.add_argument("release_id", type=int)
    parser.add_argument("tag")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    require(re.fullmatch(r"[\w.-]+/[\w.-]+", args.repository) and args.repository_id > 0
            and args.release_id > 0 and args.tag, "RELEASE_COORDINATES")
    subject = json.loads(checked(args.subject, "subject"))
    inventory = json.loads(checked(args.inventory, "inventory"))
    checked(args.index, "index")
    checked(args.plan, "plan")
    readback_source = checked(args.readback_verifier, "readback_verifier")
    logical_source = checked(args.logical_verifier, "logical_verifier")
    listed, transport = expected_assets(subject, inventory)

    args.output.mkdir()
    source = args.output / "verified-programs"
    source.mkdir()
    for name, raw in (("readback.py", readback_source), ("logical.py", logical_source)):
        with (source / name).open("xb") as out:
            out.write(raw)
    downloaded = args.output / "downloaded"
    subprocess.run([sys.executable, "-I", "-B", "-S", str(source / "readback.py"), str(args.subject),
                    PINS["subject"], args.repository, str(args.repository_id), args.visibility,
                    str(args.release_id), args.tag, str(downloaded)], check=True)
    readback_report = downloaded / "readback.json"
    readback_bytes = readback_report.read_bytes()
    remote = json.loads(readback_bytes)

    corpus = args.output / "same-corpus-assets"
    corpus.mkdir()
    for name in sorted(transport):
        original, linked = downloaded / name, corpus / name
        os.link(original, linked)
        require(os.path.samestat(original.stat(), linked.stat()), "LOCAL_CARRIER_IDENTITY")
    result_file = args.output / "logical.json"
    subprocess.run([sys.executable, "-I", "-B", "-S", str(source / "logical.py"), str(args.plan), PINS["plan"],
                    str(args.index), PINS["index"], str(args.inventory), PINS["inventory"],
                    str(corpus), str(result_file)], check=True)
    logical_bytes = result_file.read_bytes()
    logical = json.loads(logical_bytes)
    for name in transport:
        require(os.path.samestat((downloaded / name).stat(), (corpus / name).stat()), "CARRIER_CHANGED")
    verifier = {"__name__": "pinned_readback", "__file__": str(source / "readback.py")}
    exec(compile(readback_source, str(source / "readback.py"), "exec"), verifier)
    last = verifier["snapshot"](args.repository, args.repository_id, args.visibility,
                                args.release_id, args.tag, listed)
    identity = bind_results(args, subject, inventory, remote, logical, last)
    report = dict(schema="BKL046_VERIFIED_RELEASE_AND_LOGICAL_REPLAY_V1", **identity, pins=PINS,
                  assetIds={name: data["id"] for name, data in last.items()},
                  readbackReceiptSha256=hashlib.sha256(readback_bytes).hexdigest(),
                  logicalReceiptSha256=hashlib.sha256(logical_bytes).hexdigest(),
                  logicalCorpusReconstructed=True, knowledgeCapsuleVerified=True,
                  scientificCompletionVerified=False)
    with (args.output / "verified-release-reconstruction.json").open("x", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, sort_keys=True, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
