from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

COMPONENT = "d71f3a4dfc2ae411f4a7da212ef3fb37e4f04149c6b70f426e32f9ed3a20a9a2"
PLAN = "677460604bd564285b0571a7149f22f7ae6ea7aed27e5badc1d71b42b0474a0f"
CLASSIFIER = "54615e810d86dc95ea3ad2ca9a2b94520b557c313cede84b80cf672524304be6"
FIXTURE_ROOT = "O:/BKL046-CFA-XDRZ-valor-zero-tre-ingressi-v1/fixture/"
RUN_ROOT = "O:/BKL046-CFA-XDRZ-weight-window-runs-v1/"
ENUMS = ("onError", "cfaPattern", "kernelFunction")
SETTINGS = dict(enableCFA=True, scale=1, dropShrink=.70, useLUT=False,
                enableImageWeighting=False, enableSurfaceSplines=False, enableLocalNormalization=False,
                enableAdaptiveNormalization=False, truncateOnOutOfRange=False,
                closePreviousImages=False, showImages=False)


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def unique_keys(pairs):
    result = dict(pairs)
    require(len(result) == len(pairs), "Repeated JSON field")
    return result


def decode(raw):
    return json.loads(raw, object_pairs_hook=unique_keys)


def read(path, maximum=262144):
    require(path.is_file() and not path.is_symlink(), f"Invalid evidence file: {path.name}")
    with path.open("rb") as stream:
        data = stream.read(maximum + 1)
    require(0 < len(data) <= maximum, f"Invalid evidence size: {path.name}")
    return data


def sha(data):
    return sha256(data).hexdigest()


def check_events(raw, cases, output_root):
    lines = raw.decode("utf8").splitlines()
    require(len(lines) == 2 * len(cases), "Expected one parameter and export event per case")
    enum_values = None
    case_records = []
    for case, settings_line, export_line in zip(cases, lines[::2], lines[1::2], strict=True):
        label = case["id"]
        require(settings_line.startswith("DSG_CFA_PARAMETERS ") and export_line.startswith("DSG_CFA_EXPORT "),
                "Unexpected event order")
        params = decode(settings_line.split(" ", 1)[1])
        export = decode(export_line.split(" ", 1)[1])
        require(params["caseId"] == export["caseId"] == label, "Case order or event identity mismatch")
        knobs = params["settings"]
        require(set(knobs) == set(SETTINGS) | set(ENUMS) | {"inputData", "enableRejection"},
                "Unexpected parameter set")
        require(all(type(knobs[key]) is type(value) and knobs[key] == value for key, value in SETTINGS.items())
                and knobs["enableRejection"] is case["rejection"]
                and knobs["inputData"] == [[True, FIXTURE_ROOT + name, ""] for name in case["xdrz"]],
                "Configuration differs from frozen case")
        observed = [knobs[key] for key in ENUMS]
        require(all(type(value) is int and value >= 0 for value in observed)
                and (enum_values is None or observed == enum_values), "Inconsistent parameter enumeration")
        enum_values = observed
        require(isinstance(params["source"], str) and 0 < len(params["source"].strip()) <= 65536,
                "Missing process source readback")
        require(export["intensity"] == output_root + label + "-rgb.fits"
                and export["weights"] == output_root + label + "-weight.fits"
                and export["weightMeaning"] == "NATIVE_WEIGHT_WINDOW_UNCLASSIFIED"
                and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,127}", export["weightWindowId"]),
                "Unexpected export identity")
        case_records.append(dict(caseId=label, weightWindowId=export["weightWindowId"],
                                 sourceReadbackSha256=sha(params["source"].encode("utf8"))))
    return enum_values, case_records


def main():
    parser = ArgumentParser()
    for name in ("component", "classifier", "packages", "fixture", "outputs", "report"):
        parser.add_argument(name, type=Path)
    parser.add_argument("reservation")
    parser.add_argument("marker_sha256")
    args = parser.parse_args()
    require(re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", args.reservation),
            "Expected a reservation identity")
    component_raw = read(args.component)
    require(sha(component_raw) == COMPONENT, "Component mismatch")
    plan = decode(component_raw)
    require(plan["fixtureReceiptSha256"] == PLAN and sha(read(args.fixture / "riscontro.json")) == PLAN,
            "Fixture mismatch")
    markers = ["batch.done.json", "events.txt"]
    files = [f'{case["id"]}-{kind}.fits' for case in plan["cases"] for kind in ("rgb", "weight")]
    expected = set(markers + files)
    require({p.name for p in args.outputs.iterdir()} == expected, "Unexpected or missing output")
    before = {name: sha(read(args.outputs / name)) for name in markers + files}
    marker_raw = read(args.outputs / markers[0])
    require(sha(marker_raw) == before[markers[0]] == args.marker_sha256, "Marker digest mismatch")
    require(decode(marker_raw) == dict(
        schema="BKL046_CFA_XDRZ_BATCH_OUTPUT_MARKER_V1", scope="OUTPUT_MARKER_NOT_ADMISSION",
        operation=plan["operation"], planSha256=PLAN, componentContractSha256=COMPONENT,
        reservation=args.reservation, cases=[case["id"] for case in plan["cases"]]), "Marker identity mismatch")
    event_raw = read(args.outputs / markers[1])
    require(sha(event_raw) == before[markers[1]], "Transcript changed")
    enums, records = check_events(event_raw, plan["cases"], RUN_ROOT + args.reservation + "/products/")
    classifier = read(args.classifier)
    require(sha(classifier) == CLASSIFIER, "Classifier changed")
    with TemporaryDirectory(prefix="cfa-compare-", dir=args.report.parent) as directory:
        report_path = Path(directory) / "report.json"
        command = [sys.executable, "-I", "-B", "-S", "-c", classifier.decode("utf8"),
                   str(args.packages), str(args.fixture), str(report_path), "--exports", str(args.outputs)]
        subprocess.run(command, check=True, timeout=45, capture_output=True)
        report_raw = read(report_path)
    numeric = decode(report_raw)
    require(numeric["schema"] == "BKL046_CFA_XDRZ_WEIGHT_SCALE_COMPARISON_V1"
            and numeric["fixtureSha256"] == PLAN and numeric["mode"] == "FITS_COMPARISON",
            "Unexpected comparison receipt")
    compared = {name: digest for pair in numeric["inputHashes"].values() for name, digest in pair.items()}
    require(compared == {name: before[name] for name in files}, "Comparator consumed different bytes")
    require({p.name for p in args.outputs.iterdir()} == expected
            and all(sha(read(args.outputs / name)) == pin for name, pin in before.items()), "Outputs changed")
    comparison = numeric["comparison"]
    profile = comparison["weightProfile"]
    status = comparison["profileResults"][profile]["status"] if profile else None
    payload = dict(schema="BKL046_CFA_WEIGHT_WINDOW_OUTPUT_RECEIPT_V1", reservation=args.reservation,
                   operation=plan["operation"], planSha256=PLAN, componentSha256=COMPONENT,
                   classifierSha256=CLASSIFIER, outputHashes=before, parameterEnumerations=enums,
                   observations=records, numericReportSha256=sha(report_raw), comparison=comparison,
                   resolved=profile is not None and status in ("ZERO_WEIGHT_RETAINED", "ZERO_SAMPLE_EXCLUDED"),
                   provesCoordinatorAdmission=False, nativeProvenanceVerified=False, scientificClosures=0)
    with args.report.open("x", encoding="utf8", newline="\n") as stream:
        json.dump(payload, stream, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
