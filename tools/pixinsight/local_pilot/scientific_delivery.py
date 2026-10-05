"""Explicit private P5 registration/delivery on the Owner PC; no native launch."""
import argparse
import base64
import io
import os
from pathlib import Path
import struct
import xml.etree.ElementTree as ET

from . import worker
from .broker import decode, encode, require
from .scientific_portal import digest
from .transport import Transport


def registry_digest(request):
    # Exclude paths/job IDs; include exact master hashes, image selection and recipe.
    value = {"recipe": request["recipe"], "background": request["background"],
             "inputs": [{k: v for k, v in row.items() if k != "path"} for row in request["inputs"]]}
    return digest(encode(value))


def preview_bytes(path):
    from PIL import Image
    from .quality import inspect_pixels
    inspect_pixels(path)
    header = worker.xisf_header(path)
    size = (header["width"], header["height"])
    with path.open("rb") as stream:
        stream.seek(8)
        length = struct.unpack("<I", stream.read(4))[0]
        stream.read(4)
        image = next(e for e in ET.fromstring(stream.read(length)) if e.tag.split("}")[-1] == "Image")
        stream.seek(int(image.get("location").split(":")[1]))
        bands = []
        for _ in range(3):
            raw = stream.read(size[0] * size[1] * 4)
            plane = Image.frombytes("F", size, raw, "raw", "F;32F")
            bands.append(plane.point(lambda x: x * 255).convert("L"))
    preview = Image.merge("RGB", bands)
    preview.thumbnail((2400, 2400), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    preview.save(output, format="JPEG", quality=95)
    return output.getvalue()


def register(config, transport):
    rows = []
    for ref, request in config["registry"].items():
        if request["recipe"] != worker.NONLINEAR_RECIPE:
            continue
        worker.validate({**request, "jobId": "P5Registration"})
        rows.append(transport.post("/v1/worker/science/register", {"inputRef": ref, "target": "M27",
            "recipe": request["recipe"], "manifestSha256": registry_digest(request)}))
    require(rows, "NO_M27_REGISTERED_INPUT")
    return {"registeredInputs": len(rows)}


def deliver(config, transport, job_id):
    require(isinstance(job_id, str) and __import__('re').fullmatch(r"PIAI_[a-f0-9]{32}", job_id), "JOB_ID")
    root = Path(config["workerRoot"]).resolve(strict=True)
    job = root / job_id
    context = transport.request("/v1/worker/science/" + job_id + "/context")
    binding = decode((root / "transport" / job_id / "closed.json").read_bytes())
    require(binding["jobId"] == job_id and binding["workerId"] == config["workerId"] and
            binding["request"]["inputRef"] == context["input"]["inputRef"], "CLOSED_BINDING_REQUIRED")
    registered = config["registry"][context["input"]["inputRef"]]
    require(registry_digest(registered) == context["input"]["manifestSha256"], "INPUT_BINDING")
    manifest = decode((job / "manifest.json").read_bytes())
    projected = {"recipe": manifest["recipe"], "background": manifest["background"],
                 "inputs": [{k: row[k] for k in ("role", "sha256", "imageIndex", "width", "height")} for row in manifest["inputs"]]}
    require(digest(encode(projected)) == context["input"]["manifestSha256"], "MANIFEST_BINDING")
    verification = worker.collect(root, job_id)  # Reverify originals, copies, journal, outputs and all final pixels.
    require(verification["status"] == "COMPLETED" and verification["processCount"] == 29, "VERIFIED_COMPLETION_REQUIRED")
    final = job / "outputs" / "LRGB-nonlinear.xisf"
    workflow = (job / "workflow.js").read_bytes()
    require(digest(workflow) == verification["workflowSha256"], "WORKFLOW_INTEGRITY")
    path = job / "p5-preview.jpg"
    if not path.exists():
        with path.open("xb") as stream:
            stream.write(preview_bytes(final))
    # Compare to the deterministic derivative rather than trusting an existing arbitrary JPEG.
    preview = path.read_bytes()
    require(preview == preview_bytes(final), "PREVIEW_BINDING")
    header = worker.xisf_header(final)
    payload = {"workerId": config["workerId"], "leaseToken": binding["leaseToken"],
               "original": {"sha256": worker.digest(final), "byteSize": final.stat().st_size,
                            "width": header["width"], "height": header["height"], "nonLinear": True},
               "previewBase64": base64.b64encode(preview).decode(), "workflowBase64": base64.b64encode(workflow).decode(),
               "correlationsBase64": base64.b64encode((job / "runtime-correlations.json").read_bytes()).decode()}
    result = transport.post("/v1/worker/science/" + job_id + "/result", payload)
    require(result["jobId"] == job_id and result["publication"] == "NONE", "RESULT_ACK")
    receipt = job / "p5-delivery.json"
    if receipt.exists():
        require(decode(receipt.read_bytes()) == result, "DELIVERY_CONFLICT")
    else:
        worker.write_new(receipt, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("register", "deliver"))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--job")
    args = parser.parse_args()
    try:
        require(args.config.stat().st_size <= 16384, "CONFIG_SIZE")
        config = decode(args.config.read_bytes())
        require(set(config) == {"serviceOrigin", "workerId", "workerRoot", "registry"}, "CONFIG_FIELDS")
        transport = Transport(config["serviceOrigin"], os.environ.get("DSG_PIAI_WORKER_TOKEN", ""))
        print(encode(register(config, transport) if args.action == "register" else deliver(config, transport, args.job)).decode())
    except Exception:
        parser.exit(1, "Operazione non completata. Conserva il job e ripeti la stessa richiesta.\n")


if __name__ == "__main__":
    main()
