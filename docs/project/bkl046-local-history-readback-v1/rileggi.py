import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import file_digest, sha256
import json
import os
from pathlib import Path

parser = argparse.ArgumentParser()
for key in ("inventory", "archive", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
inventory_sha = "c5818bf6cd0c8dbaaf030d108bfff91e1fc15b1ddb5f95cf3aa82619919322c0"
raw = args.inventory.read_bytes()
assert sha256(raw).hexdigest() == inventory_sha
rows = [r for r in json.loads(raw)["rows"] if r["status"] == "RECORDED_PIN_UNVERIFIED_READBACK"]
assert len(rows) == 45 and sum(r["bytes"] for r in rows) == 63599156359


def identity(info):
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns


def check(row):
    name = "Conoscenza-PixInsight-v" + row["version"] + ".json"
    assert name == row["name"] and row["archive"] == "H"
    expected = {receipt["knowledgeSha256"] for receipt in row["receipts"]}
    assert expected == {row["recordedSha256"]}
    receipt_sizes = {r["expectedBytes"] for r in row["receipts"] if r["expectedBytes"] is not None}
    assert not receipt_sizes or receipt_sizes == {row["bytes"]}
    path = args.archive / name
    result = {k: row[k] for k in ("version", "name", "bytes", "recordedSha256")}
    try:
        before = identity(path.stat())
        with path.open("rb") as stream:
            first = identity(os.fstat(stream.fileno()))
            if first != before or before[2] != row["bytes"]:
                raise ValueError("Size or identity changed before reading")
            actual = file_digest(stream, "sha256", _bufsize=1024*1024).hexdigest()
            if first != identity(os.fstat(stream.fileno())):
                raise ValueError("Source changed during reading")
        if first != identity(path.stat()):
            raise ValueError("Path changed during reading")
        matched = actual == row["recordedSha256"]
        return dict(**result, actualSha256=actual, stableRead=True,
                    status="MATCHES_RECORDED_PIN" if matched else "DIFFERS_FROM_RECORDED_PIN")
    except (OSError, ValueError) as error:
        return dict(**result, actualSha256=None, stableRead=False,
                    status="READ_FAILED", errorClass=type(error).__name__,
                    winError=getattr(error, "winerror", None))


args.output.mkdir()
verified = []
with (args.output / "progress.jsonl").open("x", encoding="utf-8", newline="\n") as log:
    with ThreadPoolExecutor(max_workers=2) as pool:
        for index, checked in enumerate(pool.map(check, rows), 1):
            verified.append(checked)
            log.write(json.dumps(checked) + "\n")
            log.flush()
            if index == 1 or index % 5 == 0 or checked["status"] != "MATCHES_RECORDED_PIN":
                print(index, checked["version"], checked["status"], flush=True)
matches = sum(r["status"] == "MATCHES_RECORDED_PIN" for r in verified)
result = dict(protocol="BKL046_KNOWLEDGE_HISTORY_REMAINING_BYTE_READBACK_V1",
              inventorySha256=inventory_sha, planned=len(rows),
              exactMatches=matches, stableReadbacks=sum(r["stableRead"] for r in verified),
              bytesMatched=sum(r["bytes"] for r in verified if r["status"]=="MATCHES_RECORDED_PIN"),
              remoteAssetIdsVerified=0, githubTransferVerified=False,
              scientificClosures=0, results=verified)
with (args.output / "riscontro.json").open("x", encoding="utf-8", newline="\n") as out:
    json.dump(result, out, indent=2)
    out.write("\n")
print("MATCHED", matches, flush=True)
if matches != len(rows):
    raise SystemExit(1)
