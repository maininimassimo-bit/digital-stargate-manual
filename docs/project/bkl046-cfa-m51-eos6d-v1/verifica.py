from argparse import ArgumentParser
import ast
import json
from hashlib import sha256
from io import BytesIO
import os
from pathlib import Path
import struct
import sys
from zipfile import ZipFile
from zlib import crc32

p = ArgumentParser()
for key in ("originals", "canon_reference", "rawpy_packages", "dependencies", "vc", "output"):
    p.add_argument(key, type=Path)
args = p.parse_args()
libs = [os.add_dll_directory(str(args.rawpy_packages / "rawpy")), os.add_dll_directory(str(args.vc))]
sys.path[:0] = [str(args.rawpy_packages), str(args.dependencies)]
import numpy as np
import rawpy

EXIF_PIN = "b8d75d6cad057ebe33539f52df3a408184706f9a5d45ec55c491133df87d3ee2"
WHEEL_PIN = "fb91f8fb21b56037ecc3c062ce2de4d97fdc7d4ecb1d2738280461d74c593562"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return sha256(raw).hexdigest()


require(rawpy.__version__ == "0.25.1" and rawpy.libraw_version == (0, 21, 4)
        and np.__version__ == "2.3.5", "Unexpected decoder environment")
wheel = args.canon_reference / "rawpy-0.25.1-cp312-cp312-win_amd64.whl"
require(sha(wheel.read_bytes()) == WHEEL_PIN, "Changed decoder wheel")
with ZipFile(wheel) as archive:
    for name in archive.namelist():
        if name.startswith("rawpy/") and not name.endswith("/"):
            require(archive.read(name) == (args.rawpy_packages / name).read_bytes(), "Changed decoder member")

exif_source = (args.canon_reference / "audit_raw.py").read_bytes()
require(sha(exif_source) == EXIF_PIN, "Changed EXIF reader")
definitions = [node for node in ast.parse(exif_source).body
               if isinstance(node, ast.FunctionDef) and node.name == "exif"]
require(len(definitions) == 1, "EXIF reader missing")
namespace = dict(struct=struct, require=require)
exec(compile(ast.Module(body=definitions, type_ignores=[]), "pinned-exif-reader", "exec"), namespace)
acquisition_raw = (args.originals / "acquisizione.json").read_bytes()
capture = json.loads(acquisition_raw)
require(capture["schema"] == "BKL046_WHIRLPOOL_ORIGINAL_RANGE_ACQUISITION_V1"
        and capture["etag"] == '"10796a5de-5df0ec3d12b22"' and capture["fullOriginDownloaded"] is False
        and len({row["sha256"] for row in capture["samples"]}) == 3, "Unexpected acquisition")
output = []
for index, item in enumerate(capture["samples"], 1):
    require(item["file"] == f"sample-{index}.CR2", "Sample name changed")
    raw = (args.originals / item["file"]).read_bytes()
    require(len(raw) == item["bytes"] and sha(raw) == item["sha256"]
            and f"{crc32(raw):08x}" == item["centralCrc32"], "Capture checksum changed")
    metadata = namespace["exif"](raw)
    require(metadata["model"] == "Canon EOS 6D" and metadata["secondsNumerator"] > 0
            and metadata["secondsDenominator"] > 0, "Not the stated camera or exposure")
    with rawpy.imread(BytesIO(raw)) as decoder:
        rgba = decoder.color_desc.decode("ascii")
        full = decoder.raw_colors
        visible = decoder.raw_colors_visible
        height, width = visible.shape
        top, left = decoder.sizes.top_margin, decoder.sizes.left_margin
        require(np.array_equal(visible, full[top:top + height, left:left + width]), "Crop geometry changed")
        require(all((visible[a::2, b::2] == visible[a, b]).all()
                    for a in range(2) for b in range(2)), "Non-periodic visible phase")

        def phase(grid):
            return "".join(rgba[int(x)] for x in grid[:2, :2].ravel())

        output.append(dict(sha256=item["sha256"], capture=metadata, cropOriginYX=[top, left],
                           fullPhase=phase(full), visiblePhase=phase(visible), visibleShapeYX=[height, width],
                           decoderFlip=decoder.sizes.flip))
report = dict(schema="BKL046_EOS6D_WHIRLPOOL_STORED_BAYER_PHASE_V1",
              acquisitionSha256=sha(acquisition_raw), acquisitionCoverage="FIRST_MIDDLE_LAST_LIGHT_CR2",
              archiveLightEntries=capture["lightEntries"], exposures=output,
              scientificClosures=0, nativeExecutions=0, physicalOrientationVerified=False)
with args.output.open("x", encoding="utf8", newline="\n") as out:
    json.dump(report, out, indent=2, allow_nan=False)
    out.write("\n")
