"""Exercise preflight rejection with altered reads, leaving all inputs untouched."""
import json
from hashlib import sha256
from pathlib import Path
import subprocess
import sys

root, report = map(Path, sys.argv[1:3])
subject = (root / "launcher-subject.json").read_bytes()
bootstrap = (root / "bootstrap.py").read_text("utf-8")
prefix = """\
from pathlib import Path
import sys
original_reader = Path.read_bytes
changed = sys.argv.pop()
def read_with_fault(path):
    raw = original_reader(path)
    return raw + b'\\n' if path.name == changed else raw
Path.read_bytes = read_with_fault
"""
members = {
    "runtime": "PixInsight.exe",
    "xdrz": "shear-a-center0-origin0.0.xdrz",
    "fits": next(iter(json.loads((root / "autorita" / "batch-manifest.json").read_bytes())["fitsInputsSha256"])),
    "batch": "batch-origine.js",
}
cases = {}
for label, member in members.items():
    result = subprocess.run(
        [sys.executable, "-I", "-B", "-S", "-c", prefix + bootstrap,
         str(root), subject.decode(), "preflight", member],
        capture_output=True, text=True, timeout=120,
    )
    expected = "ValueError: UNEXPECTED_BYTES:" + member
    if result.returncode != 1 or result.stdout or expected not in result.stderr:
        raise RuntimeError(f"{label}: unexpected preflight outcome\n{result.stdout}\n{result.stderr}")
    cases[label] = {"member": member, "rejected": True}

result = {"schema": "BKL046_CFA_V3_PREFLIGHT_ALTERED_READS_V1",
          "subjectSha256": sha256(subject).hexdigest(), "cases": cases,
          "admissionRequested": False, "nativeExecutions": 0}
with report.open("x", encoding="utf-8", newline="\n") as stream:
    stream.write(json.dumps(result, sort_keys=True, indent=2) + "\n")
print(json.dumps(result, sort_keys=True))
