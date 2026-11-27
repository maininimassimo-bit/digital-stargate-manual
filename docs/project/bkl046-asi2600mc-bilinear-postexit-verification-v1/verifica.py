"""Verify numeric output and binding for a frozen native bilinear witness candidate."""
import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from zipfile import ZipFile


def digest(value):
    return sha256(value).hexdigest()


def require(valid, error):
    if not valid:
        raise ValueError(error)


def parse(raw):
    def unique(items):
        result = {}
        for key, value in items:
            require(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique)


def read(path, maximum=65536):
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    require(len(raw) <= maximum, "INPUT_BUDGET")
    return raw


def sealed(raw, expected):
    require(digest(raw) == expected, "VERIFIED_READBACK_DIGEST")
    return parse(raw)


def verify(cfg, plan_raw, manifest_raw, dir_inputs, output_archive, envelope_raw, envelope_pin,
           context_raw, context_pin, comparator, fits, np):
    manifest = sealed(manifest_raw, cfg["inputManifestSha256"])
    plan = sealed(plan_raw, cfg["numericProtocolSha256"])
    trusted = sealed(context_raw, context_pin)
    envelope = sealed(envelope_raw, envelope_pin)
    require(trusted["schema"] == "BKL046_BILINEAR_EXACT_EXPECTED_CONTEXT_V1", "CONTEXT_SCHEMA")
    require(envelope["schema"] == "BKL046_BILINEAR_ORIGINAL_EXIT_ENVELOPE_V1", "ENVELOPE_SCHEMA")
    require(trusted["operation"] == cfg["operation"] and trusted["inputManifestSha256"] ==
            cfg["inputManifestSha256"], "CONTEXT_STUDY")
    bindings = ("operation", "request", "reservation", "launchSubjectSha256", "inputManifestSha256",
                "processMethod", "processInstanceSha256", "pixInsightExeSha256", "processModuleSha256")
    require(all(envelope[key] == trusted[key] for key in bindings), "ENVELOPE_CONTEXT")
    require(trusted["processMethod"] == "DynamicAlignment" and
            trusted["pixInsightExeSha256"] == cfg["pixInsightExeSha256"] and
            trusted["processModuleSha256"] == cfg["processModuleSha256"], "PROCESS_RUNTIME_OR_METHOD")
    original = trusted["original"]
    observed = envelope["originalExit"]
    require(all(observed[key] == original[key] for key in ("pid", "creationFiletime", "sessionId")),
            "ORIGINAL_PROCESS_IDENTITY")
    require(type(observed["exitCode"]) is int and observed["exitCode"] == 0 and
            observed["normalCloseObserved"] is True and observed["sameOriginalHandle"] is True, "ORIGINAL_EXIT")
    require(type(envelope["outputArchiveBytes"]) is int and envelope["outputArchiveBytes"] == len(output_archive)
            and envelope["outputArchiveSha256"] == digest(output_archive), "OUTPUT_ARCHIVE_BINDING")

    expected = {f"{row['id']}-p{i}.fits" for row in manifest["fixtures"] for i in range(len(plan["phaseSixteenths"]))}
    expected_files = envelope["outputs"]
    require(len(expected) == len(expected_files) == 85, "OUTPUT_COUNT")
    require(set(expected_files) == expected, "OUTPUT_RECORDS")
    with ZipFile(BytesIO(output_archive)) as z, TemporaryDirectory(prefix="bkl046-bilinear-output-") as temp:
        infos = z.infolist()
        require(len(infos) == len(expected) and set(z.namelist()) == expected, "OUTPUT_MEMBERSHIP")
        require(sum(r.file_size for r in infos) <= cfg["maximumExpandedArchiveBytes"], "OUTPUT_EXPANDED_BUDGET")
        root = Path(temp)
        path = root / "outputs"
        path.mkdir()
        pinned_inputs = root / "inputs"
        pinned_inputs.mkdir()
        for row in manifest["fixtures"]:
            data = read(dir_inputs / row["name"])
            require(digest(data) == row["sha256"], "INPUT_MEMBER_DIGEST")
            with (pinned_inputs / row["name"]).open("xb") as f:
                f.write(data)
        for info in infos:
            item = expected_files[info.filename]
            require(info.file_size == item["bytes"] <= 65536, "OUTPUT_BYTE_COUNT")
            raw = z.read(info)
            require(digest(raw) == item["sha256"], "OUTPUT_MEMBER_DIGEST")
            with (path / info.filename).open("xb") as f:
                f.write(raw)
        scope = SimpleNamespace(candidate=path, fixture_dir=pinned_inputs)
        rows = comparator["compare"](fits,np,plan,scope,manifest)
    require(len(rows) == len(expected) and all(r["withinTolerance"] for r in rows), "NUMERIC_CONTRACT")
    return {"verifiedCases":len(rows),"archiveSha256":digest(output_archive),
            "maximumAbsoluteEncodedError":max(row["maximumAbsoluteEncodedError"] for row in rows),
            "externalEnvelopePinMatched":True,"nativeProvenanceIndependentlyAttested":False,
            "releaseAuthorizedByThisVerifier":False,"scientificClosures":0}


def load_comparator(path, pin):
    source = read(path)
    require(digest(source) == pin, "COMPARATOR_PIN")
    module = {"__name__": "bkl046_pinned_comparator", "__file__": str(path)}
    exec(compile(source, str(path), "exec"), module)
    return module


def main():
    p = argparse.ArgumentParser()
    for name in ("protocol","kit","dependencies","archive","context","envelope","report"):
        p.add_argument(name,type=Path)
    p.add_argument("--context-sha256",required=True)
    p.add_argument("--envelope-sha256",required=True)
    a = p.parse_args()
    cfg = parse(read(a.protocol))
    sys.path.insert(0,str(a.dependencies))
    import numpy as np
    from astropy.io import fits
    c = load_comparator(a.kit/"confronta.py",cfg["numericComparatorSha256"])
    f = a.kit/"ingressi"
    values = verify(cfg,read(a.kit/"protocollo.json"),read(f/"manifest.json"),f,
       read(a.archive,cfg["maximumArchiveBytes"]),read(a.envelope),a.envelope_sha256,
       read(a.context),a.context_sha256,c,fits,np)
    with a.report.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(values,stream,indent=2,sort_keys=True)
        stream.write("\n")


if __name__ == "__main__":
    main()
