"""Resume official Gaia CDN acquisition with bounded HTTP ranges and multipart ETag checks."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import md5, sha256
import json
from pathlib import Path
import subprocess
import sys
from time import sleep

root = Path(sys.argv[1])
targets = (
    ("GD71", "3348071631670500736", "380498-380760", 1753936887, "adfe12e15e5f9fd1abf42ad7e14f693c-34"),
    ("GD153", "3944400490365194368", "446881-450181", 1313361743, "50bdfd143d8a7bf8972c4b4a7849ca0d-26"),
)
fetch_block = 32 << 20
etag_block = 50 << 20
base = "https://cdn.gea.esac.esa.int/Gaia/gdr3/Spectroscopy/xp_continuous_mean_spectrum/"


def request(url, token, size, start, stop):
    expected_range = f"bytes {start}-{stop}/{size}"
    error = "unknown"
    for attempt in range(4):
        run = subprocess.run(
            ["curl.exe", "--silent", "--show-error", "--max-time", "25",
             "--header", "Accept-Encoding: identity", "--header", f'If-Match: "{token}"',
             "--range", f"{start}-{stop}", "--dump-header", "-", "--output", "-", url],
            capture_output=True, check=False)
        header, sep, raw = run.stdout.partition(b"\r\n\r\n")
        if run.returncode == 0 and sep and len(raw) == stop - start + 1:
            lines = header.decode("iso-8859-1").splitlines()
            fields = dict((k.casefold(), v.strip()) for k,v in (item.split(":", 1) for item in lines[1:]))
            if " 206 " in lines[0] and fields.get("content-range") == expected_range and fields.get("etag") == f'"{token}"':
                return raw
        error = run.stderr.decode(errors="replace")[:160] or "Unexpected range response"
        sleep(attempt / 2)
    raise ValueError(f"Range {expected_range} failed: {error}")


def digests(path, size, token):
    combined = md5()
    whole = sha256()
    parts = 0
    with path.open("rb") as stream:
        while data := stream.read(etag_block):
            whole.update(data)
            combined.update(md5(data).digest())
            parts += 1
    if path.stat().st_size != size or f"{combined.hexdigest()}-{parts}" != token:
        raise ValueError("Reconstructed bytes do not match the CDN multipart ETag")
    return whole.hexdigest()


def fetch(row):
    star, sid, interval, size, token = row
    name = "XpContinuousMeanSpectrum_" + interval + ".csv.gz"
    final = root / name
    temporary = final.with_suffix(final.suffix + ".part")
    url = base + name
    reused = 0
    if not final.exists():
        cursor = temporary.stat().st_size if temporary.exists() else 0
        reused = cursor
        if not 0 <= cursor <= size:
            raise ValueError("Invalid partial size")
        with temporary.open("ab") as destination:
            while cursor < size:
                stop = min(cursor + fetch_block, size) - 1
                destination.write(request(url, token, size, cursor, stop))
                cursor = stop + 1
                if cursor == size or cursor // fetch_block % 8 == 0:
                    print(star, cursor, size, flush=True)
        digest = digests(temporary, size, token)
        temporary.rename(final)
    else:
        digest = digests(final, size, token)
    return dict(star=star, sourceId=sid, file=name, url=url, bytes=size, sha256=digest,
                multipartETag=token, multipartETagVerified=True, resumedBytes=reused)


with ThreadPoolExecutor(2) as pool:
    records = list(pool.map(fetch, targets))
receipt = dict(schema="BKL046_GAIA_CALSPEC_CONTINUOUS_ACQUISITION_V1",
               acquiredAtUtc=datetime.now(timezone.utc).isoformat(), records=records)
with (root / "cdn.json").open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(receipt, stream, sort_keys=True, indent=2, allow_nan=False)
    stream.write("\n")
