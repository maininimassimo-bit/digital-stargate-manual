"""Paired sensitivity analysis of the archived stellar-radius comparison."""
import contextlib
from hashlib import file_digest
import io
import json
from pathlib import Path
import sys
import tempfile

protocol, parent, out = map(Path, sys.argv[1:4])
config = json.loads(protocol.read_bytes())


def digest(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


program = parent / "match_heart_radius.py"
require(digest(program) == config["parentProgramSha256"], "parent program changed")
require(digest(parent / "riscontro.json") == config["parentReceiptSha256"], "parent receipt changed")
source = program.read_bytes().decode().replace("\r\n", "\n")
marker = "                for image,collection in zip(images,windows,strict=True):"
require(source.count(marker) == 1, "unable to place window observer")
source = source.replace(marker, "                observe(c,cal_index,j,x,y,images,se)\n" + marker)
samples = {}


def observe(parity, cal, star, x, y, images, region):
    key = (parity, cal, star, x, y)
    require(key not in samples, "duplicate window")
    samples[key] = [images[index][region].ravel().copy() for index in (2, 3, 4)]


with tempfile.TemporaryDirectory(prefix="bkl046-radius-") as tmp:
    parent_out = Path(tmp) / "replay.json"
    sys.argv = [str(program), str(parent), *sys.argv[4:], str(parent_out)]
    namespace = dict(__file__=str(program), observe=observe)
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(source, str(program), "exec"), namespace)
    require(digest(parent_out) == config["parentReceiptSha256"], "observed replay differs")

np = namespace["np"]
ids = namespace["ids"]
weights = namespace["weights"]
labels = namespace["labels"]
stellar = namespace["stellar"]
indices = namespace["test_ix"]
tiles = config["heldoutTiles"]
by_tile = [[j for j in indices if stellar["referenceTiles"][ids[j]] == t]
           for t in tiles]
require(sum(map(len, by_tile)) == len(indices) and all(by_tile), "unexpected tile allocation")
rng = np.random.default_rng(config["seed"])
reps = config["starReplicates"]
star_counts = np.zeros((reps, len(ids)), dtype=np.int64)
for group in by_tile:
    draws = rng.choice(group, size=(reps, len(group)))
    np.add.at(star_counts, (np.arange(reps)[:, None], draws), 1)
tile_select = np.zeros((len(tiles), len(ids)), dtype=np.int64)
for row, group in enumerate(by_tile):
    tile_select[row, group] = 1
cases = rng.integers(0, len(tiles), size=(config["tileReplicates"], len(tiles)))
region_counts = tile_select[cases].sum(axis=1)
omissions = tile_select.sum(axis=0) - tile_select


def compare(counts, moments):
    n, total, squares = (counts @ matrix for matrix in moments)
    require(bool(np.all(n >= 2)), "insufficient resampled windows")
    variance = (squares - total**2 / n) / (n - 1)
    require(bool(np.all(np.isfinite(variance) & (variance > 0))), "invalid dispersion")
    scale = np.sqrt(variance)
    return 100 * (scale[:, 0:1] / scale[:, 1:] - 1)


rows = []
for c, label in enumerate(labels):
    a = {key[2:]: values for key, values in samples.items() if key[:2] == (c, 0)}
    b = {key[2:]: values for key, values in samples.items() if key[:2] == (c, 1)}
    require(a.keys() == b.keys(), "A/B window mismatch")
    for cal, windows in enumerate((a, b)):
        prior = namespace["results"][label]["byCalibration"][cal]
        require(prior["windows"] == len(windows), "window count differs")
        for side in (3, 5):
            n, total, squares = [np.zeros((len(ids), 3)) for _ in range(3)]
            projected = []
            for (j, _, _), matrices in windows.items():
                flux = np.asarray(matrices) @ weights(side)
                projected.append(flux)
                n[j] += 1
                total[j] += flux
                squares[j] += flux**2
            point = compare(tile_select.sum(axis=0, keepdims=True), (n, total, squares))[0]
            direct = np.std(projected, axis=0, ddof=1)
            parent_std = [prior["dispersion"][side][m]["apertureStdAdu"] for m in (2, 3, 4)]
            np.testing.assert_allclose(direct, parent_std, atol=1e-8, rtol=1e-12)
            np.testing.assert_allclose(point, 100 * (direct[0]/direct[1:] - 1), atol=1e-9)
            star = np.quantile(compare(star_counts, (n, total, squares)), config["quantiles"], axis=0)
            region = np.quantile(compare(region_counts, (n, total, squares)), config["quantiles"], axis=0)
            omitted = compare(omissions, (n, total, squares))
            for m, drop in enumerate((1.0, 0.7)):
                extrema = [*star[:, m], *region[:, m], *omitted[:, m]]
                direction = "bilinearLower" if max(extrema) < 0 else (
                    "dropLower" if min(extrema) > 0 else "mixed")
                rows.append(dict(parity=label, calibration="AB"[cal], aperture=side, drop=drop,
                                 windows=len(windows), starCountByTile=(tile_select @ (n[:, 0] > 0)).tolist(),
                                 point=round(float(point[m]), 9),
                                 starInterval=star[:, m].round(9).tolist(),
                                 tileInterval=region[:, m].round(9).tolist(),
                                 leaveOneTile=omitted[:, m].round(9).tolist(),
                                 direction=direction))
require(len(rows) == 32, "incomplete endpoint grid")
report = dict(schema=config["schema"], protocolSha256=digest(protocol),
              programSha256=digest(Path(__file__)), parentReceiptSha256=config["parentReceiptSha256"],
              rows=rows, nativeExecutions=0, scientificClosures=0)
with out.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2, sort_keys=True, allow_nan=False)
    stream.write("\n")
print(json.dumps({k:sum(row["direction"]==k for row in rows) for k in ("bilinearLower","dropLower","mixed")}))
