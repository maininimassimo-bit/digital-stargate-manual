"""Join the two pinned-comparison grids on their common endpoint definitions."""
from hashlib import file_digest
import json
from pathlib import Path
import sys

primary, replica, output = map(Path, sys.argv[1:])
protocol = json.loads(Path(__file__).with_name("protocollo.json").read_bytes())


def read(path):
    with path.open("rb") as stream:
        digest = file_digest(stream, "sha256").hexdigest()
    report = json.loads(path.read_bytes())
    rows = {
        (row["parity"], row["calibration"], row["aperture"], row["drop"]): row
        for row in report["rows"]
    }
    if len(rows) != 32 or len(report["rows"]) != 32:
        raise ValueError("invalid endpoint grid")
    return digest, report, rows


sha_primary, report_primary, rows_primary = read(primary)
sha_replica, report_replica, rows_replica = read(replica)
if sha_primary != "0170f9d57ebf387d78572d053f18139cbe04c98657174d6fd8a2a049b6a0aeeb":
    raise ValueError("unexpected M8–M20 receipt")
if (report_replica["schema"] != protocol["schema"]
        or report_replica["parentReceiptSha256"] != protocol["parentReceiptSha256"]
        or rows_primary.keys() != rows_replica.keys()):
    raise ValueError("unexpected replication scope")
matched = []
for key, row in rows_primary.items():
    if row["direction"] == "mixed":
        continue
    comparison = rows_replica[key]
    matched.append(dict(parity=key[0], calibration=key[1], aperture=key[2], drop=key[3],
                        m8m20=row["point"], ic1805=comparison["point"],
                        ic1805Direction=comparison["direction"],
                        ic1805StarInterval=comparison["starInterval"],
                        ic1805TileInterval=comparison["tileInterval"],
                        replicated=row["direction"] == comparison["direction"]))
report = dict(m8m20Sha256=sha_primary, ic1805Sha256=sha_replica,
              results=matched, replicated=sum(row["replicated"] for row in matched),
              nativeExecutions=0, scientificClosures=0)
with output.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2, sort_keys=True, allow_nan=False)
    stream.write("\n")
