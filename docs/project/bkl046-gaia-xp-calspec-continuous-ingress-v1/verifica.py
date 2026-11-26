"""Verify and extract the official continuous Gaia DR3 spectra for two ACS standards."""
import csv
from concurrent.futures import ThreadPoolExecutor
import gzip
from hashlib import file_digest, sha256
import json
from pathlib import Path
import sys

import numpy as np

SAMPLED_PIN = "b17057e1a0fefe4ee560ba602a0eddc7ab5bed6990be6e950d636ad3dfb777a6"
EXPECTED = {
    "GD71": ("3348071631670500736", "380498-380760", 1753936887),
    "GD153": ("3944400490365194368", "446881-450181", 1313361743),
}


def require(ok, label):
    if not ok:
        raise ValueError(label)


def verify_file(root, record):
    star = record["star"]
    sid, interval, size = EXPECTED[star]
    leaf = f"XpContinuousMeanSpectrum_{interval}.csv.gz"
    require(sid == record["sourceId"] and leaf == record["file"] and size == record["bytes"] and record["multipartETagVerified"] is True,
            "Changed CDN acquisition roster")
    path = root / leaf
    require(path.stat().st_size == size, "Changed catalogue file size")
    with path.open("rb") as stream:
        require(file_digest(stream, "sha256").hexdigest() == record["sha256"], "Changed catalogue file digest")
    with gzip.open(path, "rb") as stream:
        for line in stream:
            if not line.startswith(b"#"):
                header_bytes = line
                header = next(csv.reader([line.decode()]))
                break
        require(header[:2] == ["source_id", "solution_id"] and len(header) == len(set(header)),
                "Unknown catalogue format")
        prefix = sid.encode() + b","
        matches = [row for row in stream if row.startswith(prefix)]
    require(len(matches) == 1, "Catalogue record should occur exactly once")
    row_bytes = matches[0]
    fields = next(csv.reader([row_bytes.decode()]))
    row = dict(zip(header, fields, strict=True))
    bands = {}
    for band in ("bp", "rp"):
        n = int(row[band + "_n_parameters"])
        coeff, errors, packed = [np.array(json.loads(row[band + "_" + key]), dtype=float)
                                 for key in ("coefficients", "coefficient_errors", "coefficient_correlations")]
        require(n == 55 and coeff.shape == errors.shape == (n,) and packed.shape == (n*(n-1)//2,)
                and all(np.isfinite(x).all() for x in (coeff, errors, packed))
                and (errors > 0).all() and (np.abs(packed) <= 1).all(), "Invalid coefficient arrays")
        matrix = np.eye(n)
        right,left = np.tril_indices(n, -1)
        matrix[right,left] = matrix[left,right] = packed
        basis = int(row[band + "_basis_function_id"])
        stdev = float(row[band + "_standard_deviation"])
        require(basis > 0 and np.isfinite(stdev) and stdev > 0, "Invalid model metadata")
        bands[band] = dict(basisId=basis, coefficients=n, packedCorrelations=len(packed),
                           minimumCoefficientCorrelationEigenvalue=float(np.linalg.eigvalsh(matrix)[0]))
    return star, sid, header_bytes + row_bytes, dict(sourceId=sid, continuousSolutionId=row["solution_id"],
                                     originalRowSha256=sha256(row_bytes).hexdigest(),
                                     catalogueSha256=record["sha256"], bands=bands)


def main():
    root, sampled_path, out_dir, receipt_path = map(Path, sys.argv[1:5])
    acquisition_pin = sys.argv[5]
    require(len(acquisition_pin) == 64, "Need an exact acquisition receipt pin")
    raw = (root / "cdn.json").read_bytes()
    sampled = sampled_path.read_bytes()
    require(sha256(raw).hexdigest() == acquisition_pin and sha256(sampled).hexdigest() == SAMPLED_PIN,
            "Pinned ingress changed")
    records = json.loads(raw)["records"]
    require(len(records) == 2 and {record["star"] for record in records} == set(EXPECTED),
            "Unexpected target set")
    sampled = json.loads(sampled)["spectra"]
    result = {}
    with ThreadPoolExecutor(2) as pool:
        for star, sid, table_row, report in pool.map(lambda item: verify_file(root, item), records):
            require(sid == sampled[star]["sourceId"], "Sampled source differs")
            report["sampledSolutionId"] = sampled[star]["solutionId"]
            report["sameSourceVerified"] = True
            with (out_dir / (star + "-continuous-row.csv")).open("xb") as stream:
                stream.write(table_row)
            result[star] = report
    receipt = dict(schema="BKL046_GAIAXP_CALSPEC_CONTINUOUS_INGRESS_V1",
                   acquisitionSha256=acquisition_pin, targets=result,
                   correlationPacking="upper triangle column-major without diagonal",
                   propagatedCovarianceCalculated=False, scientificClosures=0)
    with receipt_path.open("x",encoding="utf-8",newline="\n") as result_file:
        result_file.write(json.dumps(receipt,sort_keys=True,indent=2,allow_nan=False)+"\n")


if __name__ == "__main__":
    main()
