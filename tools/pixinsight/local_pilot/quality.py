"""Bounded streaming pixel validation, not scientific/photometric acceptance."""
from array import array
import math
from pathlib import Path
import struct
import sys
import xml.etree.ElementTree as ET

from tools.pixinsight.local_pilot.worker import require, xisf_header


def inspect_pixels(path: Path) -> dict:
    header = xisf_header(path)
    require(header["sampleFormat"] == "Float32" and header["channels"] == 3 and header["colorSpace"] == "RGB", "Float32 RGB pixels required")
    width, height = header["width"], header["height"]
    require(0 < width <= 12000 and 0 < height <= 12000, "Pixel geometry outside bounds")
    with path.open("rb") as stream:
        stream.seek(8)
        length = struct.unpack("<I", stream.read(4))[0]
        stream.read(4)
        image = next(e for e in ET.fromstring(stream.read(length)) if e.tag.split("}")[-1] == "Image")
        require(not image.get("compression") and image.get("pixelStorage", "planar") == "planar", "Uncompressed planar output required")
        require(image.get("byteOrder", "little") == "little", "Little-endian output required")
        location = image.get("location", "").split(":")
        require(len(location) == 3 and location[0] == "attachment", "Attached pixel block required")
        offset, size = int(location[1]), int(location[2])
        require(size == width * height * 3 * 4 and offset >= 16 + length and offset + size <= path.stat().st_size, "Pixel block bounds mismatch")
        stream.seek(offset)
        channels = []
        for _ in range(3):
            remaining = width * height
            low, high, total, zero, clipped = math.inf, -math.inf, 0.0, 0, 0
            while remaining:
                count = min(remaining, 65536)
                data = stream.read(count * 4)
                require(len(data) == count * 4, "Truncated pixel block")
                values = array("f")
                values.frombytes(data)
                if sys.byteorder != "little":
                    values.byteswap()
                require(all(math.isfinite(v) for v in values), "Nonfinite pixel detected")
                block_low, block_high = min(values), max(values)
                require(block_low >= 0 and block_high <= 1, "Pixel outside normalized range")
                low, high = min(low, block_low), max(high, block_high)
                total += math.fsum(values)
                zero += values.count(0)
                clipped += values.count(1)
                remaining -= count
            require(width * height == 1 or high > low, "Constant output channel")
            channels.append(dict(minimum=low, maximum=high, mean=total / (width * height), zeroSamples=zero, saturatedSamples=clipped))
    return dict(width=width, height=height, channels=channels, allFinite=True, normalizedRange=True,
                acceptance="OWNER_REVIEW_REQUIRED", clippingPolicy="Measured, not certified absent")
