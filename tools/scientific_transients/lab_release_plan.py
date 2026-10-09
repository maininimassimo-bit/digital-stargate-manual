"""Create-only local staging of PUBLIC Git objects. Contains no cloud execution."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from tools.pixinsight.local_pilot.broker import require


def resource_plan(session_ref, revision):
    require(re.fullmatch(r"[a-f0-9]{32}", session_ref or "") is not None, "LAB_SESSION")
    require(re.fullmatch(r"[a-f0-9]{40}", revision or "") is not None, "LAB_REVISION")
    name = "dsg-s4-lab-" + session_ref[:12]
    project, region = "digital-stargate-telemetry", "europe-west1"
    return {"protocol": "DSG_S4_FUTURE_RESOURCE_PLAN_V1", "sessionRef": session_ref,
        "sourceRevision": revision, "project": project, "region": region,
        "service": name, "registry": name, "primaryBucket": name + "-primary",
        "backupBucket": name + "-backup", "buildSourceBucket": name + "-source",
        "runtimeServiceAccount": name + "@" + project + ".iam.gserviceaccount.com",
        "buildServiceAccount": name + "-build@" + project + ".iam.gserviceaccount.com",
        "serviceSettings": {"cpu": 1, "memoryGiB": 1, "concurrency": 2,
            "minInstances": 0, "maxInstances": 1, "requestBasedBilling": True},
        "limits": {"maximumEuro": 10, "buildAttempts": 1, "buildMinutes": 20,
            "experimentSeconds": 1800, "finalAuditSeconds": 600,
            "runtimeProviderRequests": 200, "finalProviderReserve": 40,
            "runtimeHttpRequests": 80, "normalHttpRequests": 60},
        "currentAuthorization": "PREPARATION_ONLY", "activationReady": False,
        "pending": ["fresh scoped Owner authorization and isolated login profile",
            "create-only cloud name/API/IAM and EUR rate preflight",
            "reviewed bounded build/deploy/watchdog executor and finite paid retention",
            "built image digest and dependency receipt", "fresh Google Owner OAT",
            "independent final storage verification and observed service stop"],
        "retention": "No deletion authorized now; future finite retention/cleanup requires explicit approval",
        "costGuarantee": "Operational limits are not a Google Billing hard cap",
        "existingP6Resources": "UNCHANGED", "scientificValidation": "NOT_VALIDATED",
        "milestoneClosed": False}


def stage_public_source(repo, revision, output, session_ref):
    repo, output = Path(repo).resolve(), Path(output).resolve()
    plan = resource_plan(session_ref, revision)
    def git(*args):return subprocess.check_output(["git", *args], cwd=repo)
    require(git("rev-parse", revision + "^{commit}").decode().strip() == revision, "LAB_COMMIT_PIN")
    require(not output.exists(), "LAB_STAGE_CREATE_ONLY")
    # Read Git objects, never the working tree; work/, credentials and attachments excluded.
    allowed = ("tools/", "infrastructure/scientific-transients-lab/")
    records = git("ls-tree", "-rz", "--full-tree", revision).split(b"\0")
    files = []
    for record in records:
        if not record:continue
        metadata, encoded_path = record.split(b"\t", 1)
        name = encoded_path.decode("utf-8")
        if not name.startswith(allowed):continue
        require(metadata.split()[0] in {b"100644", b"100755"}, "LAB_NO_SYMLINKS")
        require(not Path(name).is_absolute() and ".." not in Path(name).parts, "LAB_STAGE_PATH")
        raw = git("show", revision + ":" + name)
        require(len(raw) <= 10 * 1024 * 1024, "LAB_PUBLIC_FILE_LIMIT")
        files.append((name, raw))
    require(sum(len(raw) for _, raw in files) <= 64 * 1024 * 1024, "LAB_STAGE_SIZE_LIMIT")
    require(any(name == "infrastructure/scientific-transients-lab/Dockerfile" for name, _ in files), "LAB_IMAGE_SOURCE_REQUIRED")
    output.mkdir(parents=True)
    entries = []
    for name, raw in files + [("source-revision.txt", (revision + "\n").encode())]:
        target = output / name;target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:handle.write(raw)
        entries.append({"path": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    receipt = {"sourceRevision": revision, "entries": entries, "resourcePlan": plan,
               "cloudCalls": 0, "credentialsConsulted": False}
    with (output / "PUBLIC-STAGING-MANIFEST.json").open("x", encoding="utf-8") as handle:
        json.dump(receipt, handle, indent=2)
    return receipt


def main():
    parser = argparse.ArgumentParser(description="Prepare public source locally; never build/deploy/login")
    parser.add_argument("--repo", required=True);parser.add_argument("--revision", required=True)
    parser.add_argument("--output", required=True);parser.add_argument("--session-ref", required=True)
    args = parser.parse_args();receipt = stage_public_source(args.repo, args.revision, args.output, args.session_ref)
    print(json.dumps({"sourceRevision": receipt["sourceRevision"], "files": len(receipt["entries"]),
                      "cloudCalls": 0, "activationReady": False}))


if __name__ == "__main__":main()
