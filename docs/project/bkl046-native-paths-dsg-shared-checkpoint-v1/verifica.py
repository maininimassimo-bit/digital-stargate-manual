"""Validate the recorded review/admission snapshot without consulting the live gate."""
from hashlib import sha256
import json
from pathlib import Path
import sys


root=Path(sys.argv[1])
pins=json.loads((root/"protocollo.json").read_bytes())
snapshot=json.loads((root/"riscontro.json").read_bytes())
assert sha256((root/"stream34-attuale.json").read_bytes()).hexdigest()==pins["streamAudit"]
stream=json.loads((root/"stream34-attuale.json").read_bytes())
assert stream["archiveMembersVerified"]==70
assert all(item["status"]=="OK" for item in stream["checks"].values())
assert stream["checks"]["coordinator"]["value"]["activePresentAtRead"] is False
assert stream["checks"]["pixInsightInventory"]["value"]["count"]==0
assert stream["approvalLanesInspected"]["adjacentFiles"]==[]
memory=stream["checks"]["hostMemory"]["value"]
assert memory["availableCommitBytes"]>=memory["minimumAvailableCommitBytes"]
assert memory["availablePhysicalBytes"]>=memory["minimumAvailablePhysicalBytes"]
assert snapshot["diagnosticBytes"]=={"commit":memory["availableCommitBytes"],"physical":memory["availablePhysicalBytes"]}
for candidate in snapshot["paths"]:
    assert candidate["archivedEvidenceSha256"]==pins["evidence"][candidate["id"]]
    assert not candidate["admissionRequested"]
    assert candidate["reviewAdjacentNames"]==[]
assert len(snapshot["paths"])==5
assert snapshot["github"]["reviewCount"]==snapshot["github"]["reviewRequests"]==0
assert not snapshot["admissionRequested"] and not snapshot["nativeExecutions"]
print(json.dumps({"candidatePaths":5,"operationalAdmissions":0,"diagnosticChecks":len(stream["checks"])}))
