import argparse
import hashlib
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("matrix", type=Path)
parser.add_argument("pixinsight", type=Path)
parser.add_argument("upstream", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()


def pinned(path, expected):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError(f"Unexpected SHA-256: {path.name}")
    return raw


def one_line(source, pattern):
    matches = [(i, line) for i, line in enumerate(source.splitlines(), 1)
               if re.search(pattern, line)]
    if len(matches) != 1:
        raise ValueError(f"Unexpected match count for {pattern}")
    return matches[0]


matrix_sha = "6a709bcb1ceb3963c296541f283d6e00c0a7f835ee7b878d19b844d20fd0ecf3"
matrix = json.loads(pinned(args.matrix, matrix_sha))
historic_path = "src/scripts/BlindSolver2000.js"
historic, = (r for r in matrix["rows"] if r["id"] == historic_path)
historic_sha = "6a754310323d02a34b814da89ecb19d3001680e3df8475ddb9148a3f3234136e"
assert historic["source"]["sha256"] == historic_sha
assert not (args.pixinsight / historic_path).exists()

main_path = "src/scripts/BlindSolver/BlindSolver.js"
main_sha = "cf117244161f18cfb2694486238bbddcd793d630d5114436f11fc645c0a1bd4e"
main = pinned(args.pixinsight / main_path, main_sha).decode("utf-8-sig")
feature_line, feature_text = one_line(main, r"^\s*#feature-id\s")
feature = feature_text.split("#feature-id", 1)[1].strip()
assert feature == "BlindSolver : Astrometry > BlindSolver"
assert feature != historic["featureId"]

engine_path = "src/scripts/BlindSolver/BlindSolverEngine.js"
engine_sha = "ce315e997ff707d5af66b6b6eb2ff367f636d5c2719020d4663735fed40ec4ac"
engine = pinned(args.pixinsight / engine_path, engine_sha).decode("utf-8-sig")
call_line, _ = one_line(engine, r"new BlindAstrometricSolver\(\s*indexFilePath\s*\)")
gaia_line, _ = one_line(engine, r"^\s*G\.dataRelease\s*=\s*Gaia\.DataRelease_BestAvailable;")
one_line(main, r'^#include\s+"BlindSolverEngine\.js"$')

references = [
    ("setiastro-commit.js",
     "https://github.com/setiastro/pixinsight-updates/blob/a357ba4ca7c7d27a3920d71abf9b372f50d5e57f/blindsolver2000.js",
     "ed0f9202f020215b5e8c1339f945a200093f11ddb9a3f02d96b0475be7416d86"),
    ("setiastro-download.js", "https://www.setiastro.com/s/BlindSolver2000-xz44.js",
     "20fda04153c10c8c4ef11d34a3d79a83aeaa6738d7805fe03774d30388af3490"),
]
upstream = []
for name, url, digest in references:
    source = pinned(args.upstream / name, digest).decode("utf-8-sig")
    _, declaration = one_line(source, r"^\s*#feature-id\s")
    assert declaration.split("#feature-id", 1)[1].strip() == historic["featureId"]
    assert re.search(r"https?://nova\.astrometry\.net/api", source)
    compact = source.replace("\r\n", "\n")
    variants = {hashlib.sha256(text.encode(encoding)).hexdigest() for text in (compact, compact.replace("\n", "\r\n"))
                for encoding in ("utf-8", "utf-8-sig")}
    assert historic_sha not in variants and historic_sha != digest
    upstream.append(dict(url=url, sha256=digest, featureIdMatchesHistoricalMatrix=True,
                         referencesAstrometryNetApi=True, exactHistoricBytesVerified=False,
                         lineEndingAndBomVariantsMatchHistoric=False))

result = dict(schema="BKL046_BLINDSOLVER_SOURCE_RECONCILIATION_V1",
              historical=dict(matrixSha256=matrix_sha, id=historic_path, sha256=historic_sha,
                              featureId=historic["featureId"], filePresentAtHistoricalInstallPath=False),
              installed=dict(id=main_path, sha256=main_sha, featureId=feature,
                             featureLine=feature_line, engine=engine_path, engineSha256=engine_sha,
                             localIndexConstructorLine=call_line, gaiaReleaseSelectionLine=gaia_line),
              publicUpstreamVariants=upstream, aliasSupportedByEvidence=False,
              historicalExactSourceRecovered=False, runtimeEquivalenceTested=False,
              scientificClosures=0, canonicalRegistryChanged=False)
with args.output.open("x", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
    f.write("\n")
