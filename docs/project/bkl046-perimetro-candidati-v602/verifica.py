import argparse
import hashlib
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("ledger", type=Path)
parser.add_argument("inventory", type=Path)
parser.add_argument("pixinsight", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_pinned(path, expected):
    data = path.read_bytes()
    if sha(data) != expected:
        raise ValueError(f"Unexpected digest for {path.name}")
    return data


ledger_sha = "8262abbf38e1c68cedf124e9fced85520b450fc3c859d93629a756000ea7d494"
inventory_sha = "903a27f3cf09d29c9d4a922a2aa84ff71ba29dd54c89a8bc9b87fd5e58fd58d8"
ledger = json.loads(read_pinned(args.ledger, ledger_sha))
scope = json.loads(read_pinned(args.inventory, inventory_sha))
indexed = {row["requirementId"] for row in ledger["requirements"]}
exe = args.pixinsight / "bin/PixInsight.exe"
with exe.open("rb") as stream:
    runtime_sha = hashlib.file_digest(stream, "sha256").hexdigest()
assert runtime_sha == "76d2339130b58be3d112b66cafc578d9f859d80c96842b2ba2dfbbdcdc8b2943"
assert len(indexed) == 4920

candidates = []
for entry in scope["unindexedEntrypoints"]:
    path = entry["path"]
    raw = read_pinned(args.pixinsight / path, entry["sha256"])
    lines = raw.decode("utf-8-sig").splitlines()
    features = [(i, m.group(1).rstrip(" \\").strip())
                for i, line in enumerate(lines, 1)
                if (m := re.match(r"^\s*#feature-id\s+(.+)$", line))]
    assert len(features) == 1
    line, feature = features[0]
    feature_id = feature.split(":", 1)[0].strip()
    assert feature_id == Path(path).stem
    assert feature == entry["feature"].rstrip(" \\").strip()
    rid = "script_file:" + path
    assert rid not in indexed
    candidates.append(dict(id=rid, installedSha256=entry["sha256"], feature=feature,
                           declarationLine=line, exactLedgerIdPresent=False,
                           evidenceClass="INSTALLED_FEATURE_DECLARATION",
                           runtimeRegistrationObserved=False, scientificClosure=False))

uses = {}
for call in scope["constructorGlobalCalls"]:
    name = call["processCandidate"]
    raw = read_pinned(args.pixinsight / call["path"], call["scriptSha256"])
    source = raw.decode("utf-8-sig").splitlines()
    assert re.fullmatch(r"\s*let \w+ = new " + re.escape(name) + r";\s*", source[call["line"] - 1])
    module_path = "bin/" + call["module"]
    read_pinned(args.pixinsight / module_path, call["moduleSha256"])
    uses.setdefault(name, []).append(dict(path=call["path"], line=call["line"],
        scriptSha256=call["scriptSha256"], modulePath=module_path, moduleSha256=call["moduleSha256"]))
for name, calls in sorted(uses.items()):
    rid = "process:" + name
    assert rid not in indexed
    candidates.append(dict(id=rid, observedCallSites=calls, exactLedgerIdPresent=False,
                           evidenceClass="CONSTRUCTOR_CALL_AND_INSTALLED_MODULE",
                           runtimeRegistrationObserved=False, scientificClosure=False))

legacy_path = "src/scripts/BlindSolver2000.js"
assert "script_file:" + legacy_path in indexed
assert not (args.pixinsight / legacy_path).exists()
assert len(candidates) == 9
result = dict(schema="BKL046_INSTALLED_CANDIDATE_PROVENANCE_V1", ledgerSha256=ledger_sha,
              priorInventorySha256=inventory_sha, runtimeSha256=runtime_sha, requirementCount=len(indexed),
              candidates=candidates,
              legacyBlindSolver=dict(ledgerId="script_file:" + legacy_path, installedAtIndexedPath=False,
                                     equivalenceToBlindSolverVerified=False),
              canonicalScopeUpdated=False, nativeExecutions=0, scientificClosures=0)
with args.output.open("x", encoding="utf-8", newline="\n") as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")
