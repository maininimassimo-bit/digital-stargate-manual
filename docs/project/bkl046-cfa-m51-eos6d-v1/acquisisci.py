from argparse import ArgumentParser
from hashlib import sha256
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from zlib import crc32

URL = "https://amor.cms.hu-berlin.de/~rodrigus/Resources/WhirlpoolGalaxy.zip"
SIZE = 4422280670
ETAG = '"10796a5de-5df0ec3d12b22"'
TAIL_PIN = "6ff2cc1be5f742a4fd020ea99413a8d7ec39928041079f7d8147c508e6a78057"
BUDGET = 150_000_000

parser = ArgumentParser()
parser.add_argument("tail", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()


def sha(raw):
    return sha256(raw).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


class RangeReader:
    def __init__(self, directory, tail):
        self.directory, self.tail = directory, tail
        self.pos = 0
        self.received = 0
        self.ranges = []

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, position, whence=io.SEEK_SET):
        anchor = {io.SEEK_SET: 0, io.SEEK_CUR: self.pos, io.SEEK_END: SIZE}[whence]
        self.pos = anchor + position
        require(0 <= self.pos <= SIZE, "ZIP seek outside source")
        return self.pos

    def read(self, count=-1):
        start = self.pos
        count = SIZE - start if count < 0 else min(count, SIZE - start)
        if count == 0:
            return b""
        if count > 4_000_000:
            return b"".join(self.read(min(4_000_000, count - offset))
                            for offset in range(0, count, 4_000_000))
        end = start + count - 1
        tail_position = SIZE - len(self.tail)
        if start >= tail_position:
            raw = self.tail[start - tail_position:end - tail_position + 1]
        else:
            require(count <= 40_000_000 and self.received + count <= BUDGET, "Network budget exhausted")
            part = self.directory / f"range-{len(self.ranges)}.bin"
            maximum = str(count)
            response = subprocess.run([
                "curl.exe", "--silent", "--show-error", "--fail", "--location", "--proto", "=https",
                "--max-time", "20", "--retry", "2", "--retry-max-time", "45",
                "--max-filesize", maximum, "--header", "If-Match: " + ETAG,
                "--range", f"{start}-{end}", "--dump-header", "-", "--output", str(part), URL
            ], check=True, timeout=50, capture_output=True, text=True)
            final = response.stdout.strip().split("\n\n")[-1]
            headers = {k.lower(): v.strip() for k, v in (
                row.split(":", 1) for row in final.splitlines()[1:] if ":" in row
            )}
            require(final.startswith(("HTTP/1.1 206 ", "HTTP/2 206 "))
                    and headers.get("content-range") == f"bytes {start}-{end}/{SIZE}"
                    and headers.get("etag") == ETAG, "Origin range or revision mismatch")
            raw = part.read_bytes()
            self.received += len(raw)
            self.ranges.append(dict(start=start, end=end, sha256=sha(raw)))
        require(len(raw) == count, "Range length differs")
        self.pos += count
        return raw


tail = args.tail.read_bytes()
require(len(tail) == 65536 and sha(tail) == TAIL_PIN, "Source tail changed")
args.output.mkdir(exist_ok=True)
require({path.name for path in args.output.iterdir()} <= {"sample-1.CR2", "sample-2.CR2", "sample-3.CR2"},
        "Unexpected resume directory")
with TemporaryDirectory(prefix="zip-ranges-", dir=args.output) as work:
    work = Path(work).resolve()
    require(work.parent == args.output.resolve(), "Unexpected temporary range directory")
    reader = RangeReader(work, tail)
    with ZipFile(reader) as archive:
        entries = archive.infolist()
        require(len(entries) == len({entry.filename for entry in entries}), "Duplicate ZIP members")
        candidates = sorted(
            (entry for entry in entries if entry.filename.lower().endswith(".cr2")
             and any(part.lower().startswith("light") for part in PurePosixPath(entry.filename).parts[:-1])),
            key=lambda entry: entry.filename
        )
        require(len(candidates) >= 3, "No usable light cohort in the central directory")
        selected = [candidates[j] for j in (0, len(candidates) // 2, len(candidates) - 1)]
        samples = []
        for i, entry in enumerate(selected):
            require(0 < entry.file_size <= 40_000_000 and 0 < entry.compress_size <= 40_000_000,
                    "CR2 length outside bound")
            local = f"sample-{i + 1}.CR2"
            target = args.output / local
            reused = target.exists()
            if reused:
                require(target.is_file() and not target.is_symlink() and target.stat().st_size == entry.file_size,
                        "Invalid resume member")
                raw = target.read_bytes()
            else:
                raw = archive.read(entry)
            require(len(raw) == entry.file_size and crc32(raw) == entry.CRC and raw[8:10] == b"CR",
                    "Original CR2 member failed its central-directory check")
            if not reused:
                with target.open("xb") as out:
                    out.write(raw)
            samples.append(dict(file=local, member=entry.filename, bytes=len(raw), sha256=sha(raw),
                                centralCrc32=f"{entry.CRC:08x}", resumedAndCrcVerified=reused))
record = dict(schema="BKL046_WHIRLPOOL_ORIGINAL_RANGE_ACQUISITION_V1", url=URL, bytesOfOrigin=SIZE,
              etag=ETAG, tailSha256=TAIL_PIN, entries=len(entries), lightEntries=len(candidates),
              declaredRanges=reader.ranges, additionalBytesDownloaded=reader.received,
              fullOriginDownloaded=False, samples=samples)
with (args.output / "acquisizione.json").open("x", encoding="utf8", newline="\n") as out:
    json.dump(record, out, indent=2)
    out.write("\n")
