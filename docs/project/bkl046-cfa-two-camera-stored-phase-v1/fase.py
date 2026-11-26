from argparse import ArgumentParser
from collections import Counter
from hashlib import file_digest, sha256
from io import BytesIO
import json
import os
from pathlib import Path
import sys
from zipfile import ZipFile

parser = ArgumentParser()
for name in ("canon", "zwo", "rawpy_packages", "dependency_packages", "vc", "output"):
    parser.add_argument(name, type=Path)
args = parser.parse_args()
dlls = [os.add_dll_directory(str(args.rawpy_packages / "rawpy")), os.add_dll_directory(str(args.vc))]
sys.path[:0] = [str(args.rawpy_packages), str(args.dependency_packages)]
import numpy as np
import rawpy
from astropy.io import fits

CANON = "582a3adcdeb5509b4c4e9434b252726cf0473c86fdd6da272a69aa4358bc705f"
ZWO = "9758860a8e09d311f735f37a18f52294c0b802bb8a14218fa957dbb93efa3a05"
CANON_ZIP = "4a0c4142d8d0e7b056ec9b46046eec78fe6fc149aabf3c028923f81d6851f0a0"
ZWO_ZIP = "daa8ba4ee748f7616f3db0371b60d95752ff98d00ceaef280fe8f6e8ab937c76"
WHEEL = "rawpy-0.25.1-cp312-cp312-win_amd64.whl"
WHEEL_PIN = "fb91f8fb21b56037ecc3c062ce2de4d97fdc7d4ecb1d2738280461d74c593562"
ZWO_KEYS = ("BAYERPAT", "XBAYROFF", "YBAYROFF", "ROWORDER", "XORGSUBF", "YORGSUBF",
            "XBINNING", "YBINNING", "INSTRUME")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    with path.open("rb") as handle:
        return file_digest(handle, "sha256").hexdigest()


def frozen_json(folder, pin):
    raw = (folder / "riscontro.json").read_bytes()
    require(sha256(raw).hexdigest() == pin, "Changed capture receipt")
    return json.loads(raw)


def exposure(archive, row):
    member = archive.getinfo(row["member"])
    require(0 < member.file_size < 67_108_864, "Unexpected input size")
    raw = archive.read(member)
    require(sha256(raw).hexdigest() == row["sha256"], "Changed capture bytes")
    return raw


def array_pattern(grid, colors):
    return "".join(colors[int(index)] for index in grid.flatten())


def exposures(archive_path, pin, rows):
    require(digest(archive_path) == pin, "Changed original archive")
    require(len({row["member"] for row in rows}) == len(rows), "Duplicate requested members")
    with ZipFile(archive_path) as archive:
        require(len(set(archive.namelist())) == len(archive.namelist()), "Duplicate archive members")
        for row in rows:
            yield row, exposure(archive, row)


require(rawpy.__version__ == "0.25.1" and rawpy.libraw_version == (0, 21, 4) and np.__version__ == "2.3.5",
        "Changed decoding environment")
require(digest(args.canon / WHEEL) == WHEEL_PIN, "Changed decoder wheel")
with ZipFile(args.canon / WHEEL) as wheel:
    members = [name for name in wheel.namelist() if name.startswith("rawpy/") and not name.endswith("/")]
    for name in members:
        require(wheel.read(name) == (args.rawpy_packages / name).read_bytes(), "Changed decoder member")
canon_receipt = frozen_json(args.canon, CANON)
zwo_receipt = frozen_json(args.zwo, ZWO)
canon_rows = []
for source, raw in exposures(args.canon / "HeartNebula.zip", CANON_ZIP, canon_receipt["inputs"]["lights"]):
    require(source["model"] == "Canon EOS 40D", "Unexpected Canon camera")
    with rawpy.imread(BytesIO(raw)) as decoder:
        color_desc = decoder.color_desc.decode("ascii")
        require(len(color_desc) == 4, "Unexpected color description")
        full = decoder.raw_colors
        visible = decoder.raw_colors_visible
        sizes = decoder.sizes
        height, width = visible.shape
        top, left = sizes.top_margin, sizes.left_margin
        require(visible.shape == decoder.raw_image_visible.shape, "Visible Bayer geometry mismatch")
        require(np.array_equal(visible, full[top:top + height, left:left + width]),
                "Visible pixels do not match raw color coordinates")
        require(all((visible[y::2, x::2] == visible[y, x]).all() for y in range(2) for x in range(2)),
                "Visible period is not a 2x2 lattice")
        canon_rows.append(dict(sha256=source["sha256"], shapeYX=[height, width], cropOriginYX=[top, left],
                               decodedFullPattern=array_pattern(full[:2, :2], color_desc),
                               decodedVisiblePattern=array_pattern(visible[:2, :2], color_desc),
                               decoderFlip=sizes.flip, recordedExifOrientation=source["orientation"]))
zwo_rows = []
for source, raw in exposures(args.zwo / "Brutes_180s.zip", ZWO_ZIP, zwo_receipt["rows"]):
    header = fits.getheader(BytesIO(raw))
    require(header["NAXIS"] == 2 and header["BITPIX"] == 16 and header["INSTRUME"] == "ZWO ASI2600MC Pro",
            "Unexpected ZWO original format")
    zwo_rows.append(dict(sha256=source["sha256"], shapeYX=[header["NAXIS2"], header["NAXIS1"]],
                         storedMetadata={key: header.get(key) for key in ZWO_KEYS}))


def counts(values):
    return dict(sorted(Counter(values).items()))


require(len(canon_rows) == 39 and len(zwo_rows) == 15, "Unexpected coverage")
result = dict(schema="BKL046_CFA_TWO_CAMERA_STORED_PHASE_V1", manifestPins=dict(canon=CANON, zwo=ZWO,
              canonZip=CANON_ZIP, zwoZip=ZWO_ZIP, decoderWheel=WHEEL_PIN), wheelMembersVerified=len(members),
              canon=dict(camera="Canon EOS 40D", rows=canon_rows,
                         fullPattern=counts(row["decodedFullPattern"] for row in canon_rows),
                         visiblePattern=counts(row["decodedVisiblePattern"] for row in canon_rows)),
              zwo=dict(camera="ZWO ASI2600MC Pro", rows=zwo_rows,
                       headerPattern=counts(row["storedMetadata"]["BAYERPAT"] for row in zwo_rows)),
              physicalSensorOrientationVerified=False, distinctAcquisitionSeries=2, scientificClosures=0,
              nativeExecutions=0)
with args.output.open("x", encoding="utf8", newline="\n") as target:
    json.dump(result, target, indent=2, allow_nan=False)
    target.write("\n")
