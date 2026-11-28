"""Verify one F9 Actions artifact using the repository's live-time validator."""
import hashlib
import io
import json
import subprocess
import sys
import zipfile
from pathlib import Path


def github(endpoint):
    return subprocess.check_output(["gh", "api", endpoint])


def main(run_id):
    if not run_id.isdecimal():
        raise SystemExit("Expected a numeric run ID")
    repo = "repos/maininimassimo-bit/digital-stargate-manual/actions"
    run = json.loads(github(f"{repo}/runs/{run_id}"))
    if run["event"] != "schedule" or run["head_branch"] != "main":
        raise SystemExit("Expected a scheduled run on main")
    root = Path(__file__).resolve().parents[4]
    subprocess.run([
        "git", "merge-base", "--is-ancestor",
        "c2dff35385c36fe7694b4363496bed7dea288729", run["head_sha"],
    ], cwd=root, check=True)
    artifacts = json.loads(github(
        f"{repo}/runs/{run_id}/artifacts?name=f9-current-night-projection"
    ))["artifacts"]
    if len(artifacts) != 1 or artifacts[0]["expired"]:
        raise SystemExit("Expected one available F9 artifact")
    artifact = artifacts[0]
    archive = github(f"{repo}/artifacts/{artifact['id']}/zip")
    archive_hash = hashlib.sha256(archive).hexdigest()
    if artifact.get("digest") and artifact["digest"] != f"sha256:{archive_hash}":
        raise SystemExit("Artifact digest mismatch")
    filename = "observation-planner-f9-current-night.json"
    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        if bundle.namelist() != [filename]:
            raise SystemExit("Unexpected ZIP contents")
        payload = bundle.read(filename)
    sys.path.insert(0, str(root / ".github" / "scripts"))
    from observation_planner_f9 import validate_projection
    from datetime import datetime, timezone

    projection = json.loads(payload)
    now = datetime.now(timezone.utc)
    validate_projection(projection, now)
    initialized = datetime.fromisoformat(projection["forecast"]["runInitialisationUtc"])
    print(json.dumps({
        "runId": run_id,
        "head": run["head_sha"],
        "artifactId": artifact["id"],
        "verifiedAtUtc": now.isoformat(),
        "runAgeHours": round((now - initialized).total_seconds() / 3600, 2),
        "nightWindow": {key: projection["nightWindow"][key]
                        for key in ("fromUtc", "toUtcExclusive")},
        "payloadSha256": hashlib.sha256(payload).hexdigest(),
    }))


if __name__ == "__main__":
    main(sys.argv[1])
