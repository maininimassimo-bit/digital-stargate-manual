"""Replay the pinned BKL-046 v600 corpus from release-named carrier files."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256, file_digest
import json
import os
from pathlib import Path
import re
import stat
from zipfile import ZipFile

BUFFER = 4 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pinned(path, expected):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == expected, f"Metadata SHA-256 mismatch: {path.name}")
    return json.loads(raw)


def digest_rows(rows):
    return sha256(json.dumps(rows, ensure_ascii=True, separators=(",", ":")).encode()).hexdigest()


def regular(path):
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and not (
        getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    ), f"Expected ordinary file: {path.name}")
    return info


def leaf(name):
    require(isinstance(name, str) and name not in {"", ".", ".."}
            and not any(char in name for char in ("/", "\\", ":")), "Invalid file name")
    return name


def bind(plan, index, catalog, args):
    require(plan["schema"] == "BKL046_DELIVERY_PAYLOAD_PLAN_V1"
            and index["schema"] == "BKL046_DUAL_CARRIER_INDEX_V1"
            and catalog["schema"] == "BKL046_GITHUB_RELEASE_ASSET_INVENTORY_V1", "Unexpected schema")
    require(index["fullPlanSha256"] == catalog["planSha256"] == args.plan_pin
            and catalog["indexSha256"] == args.index_pin
            and index["localCarrierAssemblyComplete"] is True
            and catalog["localCarrierAssemblyComplete"] is True, "Plan, index and inventory binding")
    contents = plan["contents"]
    for digest, item in contents.items():
        require(re.fullmatch(r"[0-9a-f]{64}", digest) and item["sha256"] == digest
                and type(item["bytes"]) is int and item["bytes"] >= 0, "Invalid content entry")
    aliases = []
    alias_keys = set()
    for alias in plan["aliases"]:
        key = (alias["role"], alias["name"])
        digest = alias["sha256"]
        require(all(isinstance(value, str) and value for value in key) and key not in alias_keys
                and digest in contents and alias["bytes"] == contents[digest]["bytes"], "Invalid logical alias")
        alias_keys.add(key)
        aliases.append((*key, digest, alias["bytes"]))
    require({row[2] for row in aliases} == set(contents)
            and len(contents) == index["verifiedContentObjects"]
            and len(aliases) == index["totalLogicalAliases"] == index["verifiedLogicalAliases"],
            "Content or alias coverage")
    sources = []
    jobs = list(zip(plan["jobs"], index["carriers"], catalog["jobs"], strict=True))
    require(len(jobs) == index["plannedJobs"] == index["verifiedJobs"]
            and len({job["id"] for job, _, _ in jobs}) == len(jobs), "Job coverage")
    assigned = [digest for job, _, _ in jobs for digest in job["items"]]
    require(len(assigned) == len(set(assigned)) and set(assigned) == set(contents), "Object assignment coverage")
    for job, carrier, transport in jobs:
        job_id = job["id"]
        require(re.fullmatch(r"(?:history|group-[0-9]{3}|large-[0-9]{3})", job_id)
                and job_id == carrier["job"] == transport["job"]
                and carrier["receiptSha256"] == transport["receiptSha256"]
                and carrier["members"] == len(job["items"]), "Carrier job binding")
        parts = carrier["files"]
        require((job["kind"] == "zip" and len(parts) == 1)
                or (job["kind"] == "split" and len(parts) > 1 and len(job["items"]) == 1),
                "Unsupported carrier layout")
        names = []
        for part_index, part in enumerate(parts, 1):
            require(re.fullmatch(r"[0-9a-f]{64}", part["sha256"]) and type(part["bytes"]) is int
                    and 0 < part["bytes"] <= 1024**3, "Invalid carrier metadata")
            name = f"bkl046-{job_id}-{part_index:04d}-{part['sha256'][:16]}.bin"
            names.append(name)
            sources.append((dict(name=name, bytes=part["bytes"], sha256=part["sha256"]),
                            Path(carrier["carrierPathRelativeToMediumRoot"]) / leaf(part["name"])))
        require(names == transport["assetOrder"], "Carrier part order")
    assets = [row for row, _ in sources]
    require(assets == catalog["assets"] and len(assets) == index["verifiedCarrierFiles"]
            and len({row["name"] for row in assets}) == len(assets)
            and sum(row["bytes"] for row in assets) == index["verifiedCarrierBytes"], "Carrier coverage")
    return jobs, aliases, sources


def stream_object(stream, digest):
    size = 0
    while chunk := stream.read(BUFFER):
        digest.update(chunk)
        size += len(chunk)
    return size


def replay(job, transport, root, contents, assets):
    files = [root / name for name in transport["assetOrder"]]
    object_hash = sha256()
    sizes = {}
    if job["kind"] == "split":
        digest, = job["items"]
        total = 0
        for path in files:
            expected = assets[path.name]
            part_hash = sha256()
            part_bytes = 0
            with path.open("rb") as stream:
                while chunk := stream.read(BUFFER):
                    object_hash.update(chunk)
                    part_hash.update(chunk)
                    part_bytes += len(chunk)
            require(part_bytes == expected["bytes"] and part_hash.hexdigest() == expected["sha256"],
                    f"Split part differs: {path.name}")
            total += part_bytes
        require(object_hash.hexdigest() == digest, f"Split object differs: {digest}")
        sizes[digest] = total
    else:
        path, = files
        with path.open("rb") as stream:
            before = os.fstat(stream.fileno())
            require(file_digest(stream, "sha256").hexdigest() == assets[path.name]["sha256"],
                    f"Carrier SHA-256 differs: {path.name}")
            with ZipFile(stream) as archive:
                members = archive.infolist()
                require(len(members) == len(job["items"])
                        and {m.filename for m in members} == {"objects/" + d for d in job["items"]},
                        f"ZIP member set differs: {job['id']}")
                for member in members:
                    digest = member.filename.removeprefix("objects/")
                    require(member.file_size == contents[digest]["bytes"], f"ZIP member size differs: {digest}")
                    with archive.open(member) as entry:
                        sizes[digest] = stream_object(entry, object_hash := sha256())
                    require(object_hash.hexdigest() == digest, f"ZIP object SHA-256 differs: {digest}")
            after = os.fstat(stream.fileno())
            require((before.st_mtime_ns, before.st_size) == (after.st_mtime_ns, after.st_size),
                    f"Carrier changed during read: {path.name}")
    require(all(size == contents[digest]["bytes"] for digest, size in sizes.items()), "Restored object size")
    return sizes


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    for name in ("plan", "index", "inventory"):
        cli.add_argument(name, type=Path)
        cli.add_argument(name + "_pin")
    cli.add_argument("assets", type=Path)
    cli.add_argument("report", type=Path)
    cli.add_argument("--local-mirror", type=Path, help="Build a new release-named NTFS hard-link fixture")
    args = cli.parse_args()
    plan = pinned(args.plan, args.plan_pin)
    index = pinned(args.index, args.index_pin)
    catalog = pinned(args.inventory, args.inventory_pin)
    jobs, aliases, sources = bind(plan, index, catalog, args)
    assets = {row["name"]: row for row, _ in sources}
    require(not args.report.exists(), "Report path already exists")
    if args.local_mirror is not None:
        args.assets.mkdir()
        base = args.local_mirror.resolve(strict=True)
        for row, relative in sources:
            path = (base / relative).resolve(strict=True)
            require(path.is_relative_to(base) and regular(path).st_size == row["bytes"], "Local carrier path or size")
            link = args.assets / row["name"]
            os.link(path, link)
            require(os.path.samestat(path.stat(), link.stat()), "Hard-link identity")
    require({path.name for path in args.assets.iterdir()} == set(assets), "Release-named carrier set differs")
    for name, asset in assets.items():
        require(regular(args.assets / name).st_size == asset["bytes"], f"Carrier size differs: {name}")
    contents = plan["contents"]
    reconstructed = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        tasks = [pool.submit(replay, job, transport, args.assets, contents, assets)
                 for job, _, transport in jobs]
        for count, task in enumerate(tasks, 1):
            reconstructed.update(task.result())
            if count % 10 == 0 or count == len(jobs):
                print(f"Jobs {count}/{len(jobs)}", flush=True)
    require(set(reconstructed) == set(contents)
            and all(reconstructed[digest] == size for _, _, digest, size in aliases), "Reconstruction coverage")
    report = dict(schema="BKL046_FULL_LOGICAL_REPLAY_V1", planSha256=args.plan_pin,
                  indexSha256=args.index_pin, inventorySha256=args.inventory_pin,
                  verifiedCarrierFiles=len(assets), verifiedCarrierBytes=index["verifiedCarrierBytes"],
                  verifiedObjects=len(reconstructed), verifiedObjectBytes=sum(reconstructed.values()),
                  verifiedLogicalAliases=len(aliases), verifiedJobs=len(jobs),
                  recoveredObjectsSha256=digest_rows(sorted(reconstructed.items())),
                  logicalAliasMapSha256=digest_rows(sorted(aliases)),
                  source="LOCAL_MIRROR_HARDLINK_FIXTURE" if args.local_mirror is not None else "PROVIDED_ASSET_DIRECTORY",
                  githubTransferVerifiedByThisRun=False)
    with args.report.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(report, indent=2, sort_keys=True) + "\n")
    require(json.loads(args.report.read_bytes()) == report, "Report readback")
    print(json.dumps(report))


if __name__ == "__main__":
    main()