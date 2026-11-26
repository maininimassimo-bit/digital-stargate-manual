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

URL = "https://api.repository.cam.ac.uk/server/api/core/bitstreams/e52f491b-ea00-4102-ab15-1aa0f088b737/content"
SIZE = 1308210989
ETAG = '"2788bb6dd6ff0a857d86240c2ac8726d"'
TAIL_PIN = "53edee1876e82e46c13b3f286ecaa0dfa46d1affa963c9cfdf73ba8cf781167a"
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
                "--max-filesize", maximum,
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
require(len(tail)==262144 and sha(tail)==TAIL_PIN,"Wrong archive revision")
dest=args.output/"originali"
dest.mkdir(exist_ok=True)
records=[]
with TemporaryDirectory(prefix="cam-range-",dir=args.output) as temporary:
    reader=RangeReader(Path(temporary).resolve(),tail)
    with ZipFile(reader) as bundle:
        for case in (1,2):
            prefix=f"exposure_stacks_part1/complex/image_set{case}/ground_truth/raw/"
            selected=sorted(m for m in bundle.namelist() if m.startswith(prefix) and m.lower().endswith(".cr2"))
            require(len(selected)==5,"Unexpected static bracket roster")
            for slot,name in enumerate(selected,1):
                info=bundle.getinfo(name)
                local=f"raw-{case}-{slot}.CR2"
                file=dest/local
                data=file.read_bytes() if file.is_file() else bundle.read(info)
                require(len(data)==info.file_size and crc32(data)==info.CRC and data[8:10]==b"CR",
                        "Archive member checksum failed")
                if not file.exists():
                    file.write_bytes(data)
                records.append({"scene":case,"file":local,"sourceMember":name,
                                "sha256":sha(data),"bytes":len(data),"crc32":f"{info.CRC:08x}"})
                print(local,len(data),flush=True)
report={"source":URL,"archiveETag":ETAG,"archiveBytes":SIZE,"directorySha256":TAIL_PIN,"records":records,
        "downloadedBytes":reader.received,"ranges":reader.ranges}
(args.output/"acquisizione.json").write_bytes((json.dumps(report,indent=2,sort_keys=True)+"\n").encode())