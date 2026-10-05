"""Trusted local P2 coordinator. No remote dispatch or PixInsight subprocess launch."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import uuid
import struct
import xml.etree.ElementTree as ET

from tools.pixinsight.workflow_archive.export_parser import TOKEN, parse_export, safe_summary

ROLES = ("R", "G", "B", "L")
RECIPE = "LRGB_LINEAR_PREP_V1"


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write_new(path: Path, value: dict) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def xisf_header(path: Path) -> dict:
    """Inspect bounded metadata only; this does not certify pixel quality."""
    with path.open("rb") as stream:
        require(stream.read(8) == b"XISF0100", "Invalid output XISF signature")
        length = struct.unpack("<I", stream.read(4))[0]
        require(0 < length <= 1024 * 1024, "Output header limit exceeded")
        stream.read(4)
        raw = stream.read(length)
    require(len(raw) == length and b"<!DOCTYPE" not in raw and b"<!ENTITY" not in raw, "Unsupported output header")
    document = ET.fromstring(raw)
    images = [e for e in document if e.tag.split("}")[-1] == "Image"]
    require(len(images) == 1, "Single output image required")
    geometry = images[0].get("geometry", "").split(":")
    require(len(geometry) == 3, "Invalid output geometry")
    return dict(width=int(geometry[0]), height=int(geometry[1]), channels=int(geometry[2]),
                sampleFormat=images[0].get("sampleFormat"), colorSpace=images[0].get("colorSpace"))


def export_runtime_instances(job: Path, receipt: dict) -> dict:
    """Export successful native instances as data, retaining exact raw journal."""
    events = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((job / "events").glob("*.json"))]
    starts = {}
    completed = []
    for event in events:
        if event["event"] == "process-started":
            label = event["data"]["label"]
            require(label not in starts, "Duplicate process action")
            starts[label] = event["data"]
        if event["event"] == "process-completed":
            label = event["data"]["label"]
            require(label in starts, "Completed process lacks start evidence")
            completed.append(starts[label])
    require(len(completed) == receipt["processCount"], "Journal/process count mismatch")
    expected = ["background-R", "background-G", "background-B", "background-L", "RGB-composition"]
    require([e["label"] for e in completed] == expected[:len(completed)], "Journal recipe order mismatch")
    sources, correlations = [], []
    for ordinal, event in enumerate(completed, 1):
        raw = event["nativeSource"]
        parsed = parse_export(raw, profile="1.2")
        require(safe_summary(parsed)["processInstanceCount"] == 1, "One native instance per action required")
        old = next(iter(parsed["instances"]))
        require(parsed["instances"][old]["process"] == ("ChannelCombination" if event["label"] == "RGB-composition" else "AutomaticBackgroundExtractor"), "Journal native process mismatch")
        new = f"DSGPilotProcess{ordinal:03}"
        # Rename only identifier tokens; strings/comments/parameter literals stay exact.
        derived = "".join(new if match.lastgroup == "id" and match.group() == old else match.group()
                          for match in TOKEN.finditer(raw))
        sources.append(derived + f"\nDSGPilotWorkflow.add( {new} );\n")
        correlations.append(dict(ordinal=ordinal, label=event["label"], target=event.get("target"),
                                 dependencies=event["dependencies"], variable=new,
                                 nativeSourceSha256=hashlib.sha256(raw.encode()).hexdigest()))
    raw_export = ("// DSG P2: successful native instances only; imported as data.\n"
                  "// Raw sources and runtime dependencies are retained separately in the private journal.\n"
                  "// This is not complete upstream project History or an executable replay.\n"
                  "var DSGPilotWorkflow = new ProcessContainer;\n" + "\n".join(sources) + "\n").encode()
    if sources:
        require(safe_summary(parse_export(raw_export.decode(), profile="1.2"))["processInstanceCount"] == len(sources), "Workflow export mismatch")
    path = job / "workflow.js"
    if path.exists():
        require(path.read_bytes() == raw_export, "Workflow export conflict")
    else:
        with path.open("xb") as stream:
            stream.write(raw_export)
    correlation_path = job / "runtime-correlations.json"
    value = dict(schemaVersion="1.0", jobId=receipt["jobId"], scope="Successful P2 native instances only",
                 upstreamHistoryCompleteness="NOT_ESTABLISHED", instances=correlations)
    if correlation_path.exists():
        require(json.loads(correlation_path.read_text(encoding="utf-8")) == value, "Correlation conflict")
    else:
        write_new(correlation_path, value)
    return dict(instanceCount=len(sources), sha256=digest(path))


def validate(request: dict) -> None:
    require(set(request) == {"schemaVersion", "jobId", "recipe", "inputs", "background"}, "Unknown request fields")
    require(request["schemaVersion"] == "1.0", "Unsupported request")
    require(isinstance(request["jobId"], str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,47}", request["jobId"]) is not None, "Invalid job ID")
    require(request["recipe"] == RECIPE, "Recipe not allowed")
    require(isinstance(request["inputs"], list) and len(request["inputs"]) == 4, "Four masters required")
    paths = set()
    for role, item in zip(ROLES, request["inputs"]):
        require(set(item) == {"role", "path", "sha256", "imageIndex", "width", "height"}, "Unknown input fields")
        require(item["role"] == role, "Role order must be R,G,B,L")
        require(isinstance(item["sha256"], str) and re.fullmatch(r"[a-f0-9]{64}", item["sha256"]) is not None, "Invalid digest")
        for key in ("imageIndex", "width", "height"):
            require(type(item[key]) is int, "Image index/dimensions must be integers")
        require(0 <= item["imageIndex"] < 16 and 1 <= item["width"] <= 12000 and 1 <= item["height"] <= 12000, "Image bounds exceeded")
        require(isinstance(item["path"], str) and Path(item["path"]).is_absolute(), "Absolute source required")
        path = Path(item["path"]).resolve(strict=True)
        require(path.is_file() and path.suffix.lower() == ".xisf", "XISF source required")
        require(path not in paths, "Source roles must be distinct")
        paths.add(path)
        require(digest(path) == item["sha256"], "Source digest mismatch")
    require(len({(i["width"], i["height"]) for i in request["inputs"]}) == 1, "Master dimensions differ")
    settings = request["background"]
    require(isinstance(settings, dict) and set(settings) == {"polyDegree", "boxSize", "boxSeparation"}, "Unknown background parameters")
    for key, low, high in (("polyDegree", 0, 2), ("boxSize", 5, 32), ("boxSeparation", 5, 64)):
        require(type(settings[key]) is int and low <= settings[key] <= high, "Background parameter outside approved bounds")


def prepare(root: Path, request: dict) -> Path:
    validate(request)
    require(root.is_dir() and not root.is_symlink() and not root.is_junction(), "Existing unlinked local worker root required")
    root = root.resolve()
    sources = [Path(i["path"]).resolve() for i in request["inputs"]]
    require(all(root != p.parent and root not in p.parents and p.parent not in root.parents for p in sources), "Worker and source directories must be separate")
    job = root / request["jobId"]
    require(not job.exists(), "Existing job cannot be overwritten")
    token = uuid.uuid4().hex
    reservation = {"schemaVersion": "1.0", "jobId": request["jobId"], "token": token}
    # Exclusive create: a second preparation cannot displace an active job.
    write_new(root / "active-job.json", reservation)
    job_created = False
    try:
        job.mkdir()
        job_created = True
        for folder in ("inputs", "outputs", "events"):
            (job / folder).mkdir()
        inputs = []
        for item, source in zip(request["inputs"], sources):
            destination = job / "inputs" / f"{item['role']}.xisf"
            with source.open("rb") as incoming, destination.open("xb") as outgoing:
                shutil.copyfileobj(incoming, outgoing, 1024 * 1024)
            require(digest(source) == item["sha256"] == digest(destination), "Source/copy integrity mismatch")
            inputs.append({**item, "path": destination.as_posix(), "sourcePath": source.as_posix()})
        runtime = job / "executor.jsh"
        with Path(__file__).with_name("executor.jsh").open("rb") as incoming, runtime.open("xb") as outgoing:
            shutil.copyfileobj(incoming, outgoing)
        manifest = {"schemaVersion": "1.0", "jobId": request["jobId"], "recipe": RECIPE,
                    "workerRoot": root.as_posix(), "jobDirectory": job.as_posix(), "token": token,
                    "inputs": inputs, "background": request["background"],
                    "runtimeLibrary": runtime.as_posix(), "runtimeSha256": digest(runtime)}
        write_new(job / "manifest.json", manifest)
        library = runtime.as_posix()
        include = '#engine v8\n#include ' + json.dumps(library) + '\n'
        # JSON is data. The only executed code is this repository library.
        manifest_path = json.dumps((job / "manifest.json").as_posix())
        launcher = include + 'DSGExecuteLocalPilot(JSON.parse(File.readTextFile(' + manifest_path + ')));\n'
        with (job / "run.js").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(launcher)
        return job
    except Exception as error:
        # Preserve the reservation and partial artifacts for explicit recovery.
        if job_created:
            write_new(job / "preparation-failed.json", {"status": "PREPARATION_FAILED", "error": str(error)})
        raise


def cancel(root: Path, job_id: str) -> None:
    require(re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,47}", job_id) is not None, "Invalid job ID")
    root = root.resolve()
    active = json.loads((root / "active-job.json").read_text(encoding="utf-8"))
    require(active["jobId"] == job_id, "Different active job")
    write_new(root / job_id / "cancel.json", {"jobId": job_id, "requested": True})


def collect(root: Path, job_id: str) -> dict:
    require(re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,47}", job_id) is not None, "Invalid job ID")
    root = root.resolve()
    job = root / job_id
    manifest = json.loads((job / "manifest.json").read_text(encoding="utf-8"))
    receipt = json.loads((job / "terminal.json").read_text(encoding="utf-8"))
    require(manifest["jobId"] == receipt["jobId"] == job_id, "Receipt identity mismatch")
    require(receipt["status"] in {"COMPLETED", "FAILED", "CANCELLED"}, "Terminal status required")
    require(receipt["token"] == manifest["token"], "Receipt reservation mismatch")
    require(type(receipt["processCount"]) is int and 0 <= receipt["processCount"] <= 5, "Invalid process count")
    integrity = all(digest(Path(i["sourcePath"])) == i["sha256"] == digest(Path(i["path"])) for i in manifest["inputs"])
    require(integrity, "Original/copy changed; reservation retained")
    require(digest(job / "executor.jsh") == manifest.get("runtimeSha256") == receipt.get("runtimeSha256"), "Runtime identity mismatch")
    expected_names = {f"{r}-linear.xisf" for r in ROLES} | {"RGB-linear.xisf"}
    names = [o["name"] for o in receipt["outputs"]]
    require(len(names) == len(set(names)), "Duplicate output")
    require(set(names) <= expected_names, "Unexpected output name")
    for output in receipt["outputs"]:
        path = (job / "outputs" / output["name"]).resolve()
        require(path.parent == (job / "outputs").resolve(), "Output escaped job")
        require(digest(path) == output["sha256"], "Output integrity mismatch")
        header = xisf_header(path)
        channels = 3 if output["name"] == "RGB-linear.xisf" else 1
        require(header == dict(width=manifest["inputs"][0]["width"], height=manifest["inputs"][0]["height"],
                              channels=channels, sampleFormat="Float32", colorSpace="RGB" if channels == 3 else "Gray"), "Output header mismatch")
    if receipt["status"] == "COMPLETED":
        require(set(names) == expected_names and receipt["processCount"] == 5, "Incomplete recipe cannot complete")
        require(receipt.get("exclusiveLeaseVerified") is True and receipt.get("originalViewsUnmodified") is True, "Native integrity/lease evidence required")
    exported = export_runtime_instances(job, receipt)
    result = {"schemaVersion": "1.0", "jobId": job_id, "status": receipt["status"],
              "originalIntegrity": "UNCHANGED", "outputCount": len(receipt["outputs"]),
              "processCount": receipt["processCount"], "workflowInstanceCount": exported["instanceCount"],
              "workflowSha256": exported["sha256"], "providerRequests": 0}
    verification = job / "verification.json"
    if verification.exists():
        require(json.loads(verification.read_text(encoding="utf-8")) == result, "Verification conflict")
    else:
        write_new(verification, result)
    active = root / "active-job.json"
    closed = job / "reservation-closed.json"
    if active.exists():
        reservation = json.loads(active.read_text(encoding="utf-8"))
        require(reservation["jobId"] == job_id and reservation["token"] == manifest["token"], "Active reservation mismatch")
        require(not closed.exists(), "Closed reservation already exists")
        # Native Windows exclusive lease prevents collection while it is held.
        active.rename(closed)
    else:
        require(closed.exists(), "Missing reservation evidence")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "cancel", "collect"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--request", type=Path)
    parser.add_argument("--job")
    args = parser.parse_args()
    if args.action == "prepare":
        require(args.request is not None, "Request required")
        print(prepare(args.root, json.loads(args.request.read_text(encoding="utf-8"))))
    elif args.action == "cancel":
        require(args.job is not None, "Job required")
        cancel(args.root, args.job)
    else:
        require(args.job is not None, "Job required")
        print(json.dumps(collect(args.root, args.job)))


if __name__ == "__main__":
    main()
