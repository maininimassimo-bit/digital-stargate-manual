"""Rebuild the licensed GaiaXPy source subset from a pinned remote recipe."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha1, sha256
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

REVISION = "349e9a435d81de50b4c09bc4afb14548acc2c9ac"
ZIP_SHA256 = "80ba52aa3b751ab499bfe23f4f4f795e5bc137b4ba66429d3398192700b0e088"
GITHUB = "https://raw.githubusercontent.com/"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def fetch(url, bound):
    with urlopen(Request(url, headers={"User-Agent": "BKL046-GaiaXPy-recovery"}), timeout=20) as response:
        require(response.geturl() == url and response.status == 200, "unexpected raw GitHub response")
        raw = response.read(bound + 1)
    require(0 <= len(raw) <= bound, "unexpected raw GitHub size")
    return raw


def fetch_file(row):
    name = row["path"]
    path = PurePosixPath(name)
    require(path.as_posix() == name and not path.is_absolute() and ".." not in path.parts, "unsafe upstream path")
    require(type(row["bytes"]) is int and 0 <= row["bytes"] <= 8_388_608, "unexpected upstream file size")
    url = GITHUB + "gaia-dpci/GaiaXPy/" + REVISION + "/" + quote(name, safe="/")
    data = fetch(url, row["bytes"])
    blob = sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    require(len(data) == row["bytes"] and sha256(data).hexdigest() == row["sha256"] and blob == row["gitBlobSha1"],
            "upstream bytes changed: " + name)
    return name, data


def rebuild(raw, pin, target):
    require(re.fullmatch("[0-9a-f]{64}", pin) and sha256(raw).hexdigest() == pin,
            "GitHub recipe pin differs")
    recipe = json.loads(raw)
    require(recipe["schema"] == "BKL046_V571_PUBLIC_GAIAXPY_RECONSTRUCTION_V1"
            and recipe["revision"] == REVISION and recipe["sourceZipSha256"] == ZIP_SHA256
            and recipe["license"] == "BSD-3-Clause" and recipe["coversCompleteV571"] is False,
            "recipe scope differs")
    rows = recipe["files"]
    require(len(rows) == 13 and len({row["path"] for row in rows}) == 13, "file set differs")
    with ThreadPoolExecutor(max_workers=4) as pool:
        payload = dict(pool.map(fetch_file, rows))
    require(b"BSD 3-Clause" in payload["LICENSE"], "missing pinned license")
    with ZipFile(target, "x") as package:
        for name, data in sorted(payload.items()):
            package.writestr(ZipInfo(name), data, compress_type=ZIP_DEFLATED)
    with ZipFile(target) as package:
        require(package.namelist() == sorted(payload), "rebuilt archive names differ")
        require(all(package.read(name) == data for name, data in payload.items()), "rebuilt archive bytes differ")
    actual = sha256(target.read_bytes()).hexdigest()
    require(actual == ZIP_SHA256, "rebuilt ZIP bytes differ with this Python/zlib runtime")
    return {"sourceFiles": len(payload), "zipSha256": actual, "licensePreserved": True,
            "coversCompleteV571": False}


locator, expected, output = sys.argv[1:4]
if locator.startswith("https://"):
    require(re.fullmatch(
        r"https://raw[.]githubusercontent[.]com/maininimassimo-bit/digital-stargate-manual/[0-9a-f]{40}/docs/project/BKL-046-V571-GAIAXPY-SOURCE-RECONSTRUCTION-v1[.]json",
        locator), "recipe remote does not identify the reviewed repository and commit")
    raw = fetch(locator, 65536)
else:
    raw = Path(locator).read_bytes()
report = rebuild(raw, expected, Path(output))
report["recipeSha256"] = expected
report["recipeDownloadedFromGitHub"] = locator.startswith("https://")
print(json.dumps(report, sort_keys=True))