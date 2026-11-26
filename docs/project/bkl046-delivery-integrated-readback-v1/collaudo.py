import argparse
from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace

parser = argparse.ArgumentParser()
for key in ("program", "subject", "inventory", "prior_replay", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
scope = {"__name__": "test_join", "__file__": str(args.program)}
exec(compile(args.program.read_bytes(), str(args.program), "exec"), scope)

subject = json.loads(scope["checked"](args.subject, "subject"))
inventory = json.loads(scope["checked"](args.inventory, "inventory"))
asset_rows, _ = scope["expected_assets"](subject, inventory)
logical = json.loads(args.prior_replay.read_bytes())
assert logical["source"] == "LOCAL_MIRROR_HARDLINK_FIXTURE"
logical["source"] = "PROVIDED_ASSET_DIRECTORY"
identity = SimpleNamespace(repository="example/fixture", repository_id=11, visibility="private",
                           release_id=22, tag="fixture-v1")
metadata = {name: dict(id=i, size=row["bytes"], state="uploaded", digest="sha256:"+row["sha256"],
                       updated_at="2000-01-01T00:00:00Z")
            for i, (name, row) in enumerate(asset_rows.items(), 1)}
remote = dict(repository=identity.repository, repositoryId=identity.repository_id,
              visibility=identity.visibility, releaseId=identity.release_id, tag=identity.tag,
              allAssetBytesVerified=True, knowledgeCapsuleRecovered=True,
              downloadedBytes=subject["totalBytes"], assets=metadata)
case_inputs = (identity, subject, inventory, remote, logical, metadata)
names = list(metadata)
first, second = names[:2]
assert scope["bind_results"](*case_inputs)["releaseId"] == 22

cases = {
    "wrong_release_id": (3, ("releaseId",), 42, "RELEASE_IDENTITY"),
    "capsule_unverified": (3, ("knowledgeCapsuleRecovered",), False, "READBACK_STATUS"),
    "short_readback": (3, ("downloadedBytes",), 0, "READBACK_STATUS"),
    "release_changes_during_replay": (5, (first,"updated_at"), "2000-01-02T00:00:00Z", "RELEASE_SNAPSHOT_CHANGED"),
    "incorrect_corpus_carrier_pins": (2, ("assets",0,"sha256"), "0"*64, "TRANSPORT_PINS"),
    "duplicate_logical_alias_digest": (4, ("logicalAliasMapSha256",), "0"*64, "LOGICAL_MAPPING_OR_SOURCE"),
    "object_digest_changed": (4, ("recoveredObjectsSha256",), "0"*64, "LOGICAL_MAPPING_OR_SOURCE"),
    "local_fixture_report": (4, ("source",), "LOCAL_MIRROR_HARDLINK_FIXTURE", "LOGICAL_MAPPING_OR_SOURCE"),
    "wrong_reconstruction_plan": (4, ("planSha256",), "0"*64, "LOGICAL_MAPPING_OR_SOURCE"),
}
passed = []
for name, (index, keys, value, code) in cases.items():
    sample = deepcopy(list(case_inputs))
    target = sample[index]
    for key in keys[:-1]:
        target = target[key]
    target[keys[-1]] = value
    if index == 5:
        sample[3]["assets"] = metadata
    try:
        scope["bind_results"](*sample)
    except ValueError as error:
        assert str(error) == code, (name, error)
    else:
        raise AssertionError(name)
    passed.append(name)
sample = deepcopy(list(case_inputs))
sample[3]["assets"][second]["id"] = sample[3]["assets"][first]["id"]
try:
    scope["bind_results"](*sample)
except ValueError as error:
    assert str(error) == "ASSET_IDENTITY"
else:
    raise AssertionError("reused asset ID")
passed.append("reused_asset_id")

report = dict(protocol="BKL046_RELEASE_RECONSTRUCTION_JOIN_FIXTURE_V1", positiveFixtureAccepted=True,
              rejectedCases=passed, releaseSubjectAssets=len(asset_rows),
              candidateLogicalObjects=logical["verifiedObjects"], remoteCalls=0,
              githubReadbackPerformed=False, githubTransferVerified=False, scientificClosures=0)
with args.output.open("x", encoding="utf-8", newline="\n") as f:
    json.dump(report, f, indent=2)
    f.write("\n")
