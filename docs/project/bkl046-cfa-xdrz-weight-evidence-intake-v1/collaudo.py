from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
from shutil import copyfile, copytree
import subprocess
import sys

parser = ArgumentParser()
for key in ("component", "fixture", "classifier", "packages", "comparison", "scratch", "report"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.comparison.parent))
from confronto import COMPONENT, PLAN, SETTINGS, FIXTURE_ROOT, RUN_ROOT

reservation = "52d471bc-3d3d-42ea-ad47-29146dbd36a5"
plan = json.loads(args.component.read_bytes())
case_ids = [case["id"] for case in plan["cases"]]
args.scratch.mkdir()
fixture = args.scratch / "original"
fixture.mkdir()
rows = []
for case in plan["cases"]:
    arm = case["id"]
    value_model, weight_model = {
        "unmasked": ("unmasked", "unmasked"),
        "mask-green": ("detector", "detector"),
        "mask-wrong-channel": ("unmasked", "unmasked"),
        "zero-detector": ("zero-detector-retained", "unmasked"),
        "zero-reference": ("zero-reference-retained", "unmasked"),
    }[arm]
    for kind, model in (("rgb", value_model), ("weight", weight_model)):
        copyfile(args.fixture / f"{model}-expected-{kind}.fits", fixture / f"{arm}-{kind}.fits")
    knobs = dict(SETTINGS, onError=0, cfaPattern=0, kernelFunction=1, enableRejection=case["rejection"],
                 inputData=[[True, FIXTURE_ROOT + name, ""] for name in case["xdrz"]])
    path = RUN_ROOT + reservation + "/" + arm
    rows.extend([("DSG_CFA_PARAMETERS", dict(caseId=arm, settings=knobs, source="simulated PJSR state")),
                 ("DSG_CFA_EXPORT", dict(caseId=arm, intensity=path + "-rgb.fits", weights=path + "-weight.fits",
                                         weightWindowId="weight_" + str(len(rows)),
                                         weightMeaning="NATIVE_WEIGHT_WINDOW_UNCLASSIFIED"))])
marker = dict(schema="BKL046_CFA_XDRZ_BATCH_OUTPUT_MARKER_V1", scope="OUTPUT_MARKER_NOT_ADMISSION",
              reservation=reservation, operation=plan["operation"], planSha256=PLAN,
              componentContractSha256=COMPONENT, cases=case_ids)
marker_raw = (json.dumps(marker) + "\n").encode()
pin = sha256(marker_raw).hexdigest()
(fixture / "batch.done.json").write_bytes(marker_raw)


def transcript(target, events):
    raw = "".join(f"{prefix} {json.dumps(value)}\n" for prefix, value in events)
    (target / "events.txt").write_bytes(raw.encode())


def execute(name, folder, expected_pin, resolved):
    out = args.scratch / f"{name}.json"
    command = [sys.executable, "-I", "-B", "-S", str(args.comparison), str(args.component),
               str(args.classifier), str(args.packages), str(args.fixture), str(folder),
               str(out), reservation, expected_pin]
    result = subprocess.run(command, capture_output=True, timeout=60)
    if resolved is None:
        if result.returncode == 0 or out.exists():
            raise ValueError(f"Expected rejection: {name}")
        return "REJECTED"
    if result.returncode != 0:
        raise ValueError(result.stderr.decode(errors="replace"))
    report = json.loads(out.read_bytes())
    if report["resolved"] is not resolved or report["provesCoordinatorAdmission"] or report["nativeProvenanceVerified"]:
        raise ValueError(f"Unexpected output: {name}")
    return dict(resolved=resolved, scaleStatus=report["comparison"]["scaleStatus"],
                weightProfile=report["comparison"]["weightProfile"])


transcript(fixture, rows)
results = {"valid": execute("valid", fixture, pin, True)}
mutations = ("wrong_pin", "foreign_marker", "missing_export", "swapped_events", "extra_file", "wrong_path",
             "mask_knob_changed", "inconsistent_map_retained")
for name in mutations:
    folder = args.scratch / name
    copytree(fixture, folder)
    marker_pin = pin
    if name == "wrong_pin":
        marker_pin = "0" * 64
    elif name == "foreign_marker":
        damaged = (json.dumps({**marker, "reservation": "00000000-0000-4000-8000-000000000000"}) + "\n").encode()
        (folder / "batch.done.json").write_bytes(damaged)
        marker_pin = sha256(damaged).hexdigest()
    elif name == "missing_export":
        (folder / "unmasked-weight.fits").unlink()
    elif name == "swapped_events":
        transcript(folder, [rows[1], rows[0], *rows[2:]])
    elif name == "extra_file":
        (folder / "extra.txt").write_text("extra")
    elif name == "wrong_path":
        transcript(folder, [rows[0], (rows[1][0], {**rows[1][1], "weights": "elsewhere/unmasked-weight.fits"}), *rows[2:]])
    elif name == "mask_knob_changed":
        wrong = {**rows[2][1]["settings"], "enableRejection": False}
        transcript(folder, [*rows[:2], (rows[2][0], {**rows[2][1], "settings": wrong}), *rows[3:]])
    else:
        copyfile(args.fixture / "detector-expected-weight.fits", folder / "zero-reference-weight.fits")
    results[name] = execute(name, folder, marker_pin, False if name == "inconsistent_map_retained" else None)
if results["valid"]["weightProfile"] != "RAW" or results["inconsistent_map_retained"]["scaleStatus"] != "NO_COMMON_PROFILE":
    raise ValueError("Wrong fixture classification")
with args.report.open("x", encoding="utf8", newline="\n") as stream:
    json.dump(dict(schema="BKL046_CFA_WEIGHT_WINDOW_LINK_TEST_V1", cases=results, nativeExecutions=0,
                   scientificClosures=0), stream, indent=2)
    stream.write("\n")
