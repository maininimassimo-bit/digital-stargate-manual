"""Exercise the replay's refusal paths with independently pinned tiny packages."""
from hashlib import sha256
import io
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile


def digest(data):
    return sha256(data).hexdigest()


def write(path, data):
    raw = json.dumps(data, sort_keys=True).encode()
    path.write_bytes(raw)
    return str(path), digest(raw)


def run_case(root, name):
    folder = root / name
    folder.mkdir()
    assets_dir = folder / "assets"
    assets_dir.mkdir()
    simple = b"first object"
    split = [b"first part", b"second part"]
    a, b = digest(simple), digest(b"".join(split))
    aliases = [dict(role="report", name="test.json", sha256=a, bytes=len(simple)),
               dict(role="sample", name="test.fits", sha256=b, bytes=sum(map(len, split)))]
    if name == "invalid-alias":
        aliases[0]["bytes"] += 1
    plan = dict(schema="BKL046_DELIVERY_PAYLOAD_PLAN_V1", aliases=aliases,
                contents={a: dict(sha256=a, bytes=len(simple)), b: dict(sha256=b, bytes=sum(map(len, split)))},
                jobs=[dict(id="history", kind="zip", items=[a]), dict(id="large-001", kind="split", items=[b])])
    plan_args = write(folder / "plan.json", plan)
    in_memory = io.BytesIO()
    with ZipFile(in_memory, "w") as carrier:
        carrier.writestr("objects/" + a, simple if name != "wrong-object" else b"altered obj!")
        if name == "extra-member":
            carrier.writestr("unexpected", b"extra")
    if name == "wrong-split-order":
        split.reverse()
    carriers, jobs, assets = [], [], []
    for job, payloads in (("history", [in_memory.getvalue()]), ("large-001", split)):
        files, asset_order = [], []
        for idx, data in enumerate(payloads, 1):
            sig = digest(data)
            leaf = f"bkl046-{job}-{idx:04d}-{sig[:16]}.bin"
            assets.append(dict(name=leaf, bytes=len(data), sha256=sig))
            files.append(dict(name=f"part-{idx}", bytes=len(data), sha256=sig))
            asset_order.append(leaf)
            if name == "missing-asset" and job == "history":
                continue
            if name == "altered-carrier" and job == "history":
                data = bytes([data[0] ^ 1]) + data[1:]
            (assets_dir / leaf).write_bytes(data)
        if name == "wrong-transport-order" and job == "large-001":
            asset_order.reverse()
        receipt = digest(job.encode())
        carriers.append(dict(job=job, files=files, receiptSha256=receipt,
                             members=1, carrierPathRelativeToMediumRoot=job))
        jobs.append(dict(job=job, assetOrder=asset_order, receiptSha256=receipt))
    index = dict(schema="BKL046_DUAL_CARRIER_INDEX_V1", fullPlanSha256=plan_args[1],
                 localCarrierAssemblyComplete=True, verifiedContentObjects=2, totalLogicalAliases=2,
                 verifiedLogicalAliases=2, plannedJobs=2, verifiedJobs=2, verifiedCarrierFiles=3,
                 verifiedCarrierBytes=sum(row["bytes"] for row in assets), carriers=carriers)
    index_args = write(folder / "index.json", index)
    inventory = dict(schema="BKL046_GITHUB_RELEASE_ASSET_INVENTORY_V1", indexSha256=index_args[1],
                     planSha256=plan_args[1], localCarrierAssemblyComplete=True, jobs=jobs, assets=assets)
    inventory_args = write(folder / "inventory.json", inventory)
    report = folder / "report.json"
    result = subprocess.run([sys.executable, "-I", "-S", "-B", str(Path(__file__).with_name("replay_corpus.py")),
                             *plan_args, *index_args, *inventory_args, str(assets_dir), str(report)],
                            capture_output=True, text=True, timeout=30)
    return result, report


def main():
    refusals = {
        "invalid-alias": "Invalid logical alias",
        "wrong-object": "ZIP object SHA-256 differs",
        "extra-member": "ZIP member set differs",
        "wrong-split-order": "Split object differs",
        "missing-asset": "Release-named carrier set differs",
        "altered-carrier": "Carrier SHA-256 differs",
        "wrong-transport-order": "Carrier part order",
    }
    with TemporaryDirectory() as temp:
        root = Path(temp)
        result, report = run_case(root, "valid")
        if result.returncode or json.loads(report.read_bytes())["verifiedObjects"] != 2:
            raise AssertionError(result.stderr)
        for name, expected_error in refusals.items():
            result, report = run_case(root, name)
            if not result.returncode or expected_error not in result.stderr or report.exists():
                raise AssertionError((name, result.returncode, result.stderr, report.exists()))
    print(json.dumps(dict(valid=True, expectedRefusals=list(refusals)), indent=2))


if __name__ == "__main__":
    main()