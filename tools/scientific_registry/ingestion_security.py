"""Antivirus gate and metadata-free publication derivative; originals untouched."""
import io
import os
from pathlib import Path
import subprocess
import tempfile
import time
import warnings

from .photo_ingestion import IngestionError


class ClamScanner:
    def __init__(self, database="/var/lib/clamav"):
        self.database = Path(database)

    def scan(self, raw):
        databases = [p for p in self.database.glob("daily.*") if p.suffix in {".cvd", ".cld"}]
        if not databases or max(p.stat().st_mtime for p in databases) < time.time() - 48 * 3600:
            try:
                update = subprocess.run(["freshclam", "--stdout", "--datadir=" + str(self.database)],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
                databases = [p for p in self.database.glob("daily.*") if p.suffix in {".cvd", ".cld"}]
                if update.returncode != 0 or not databases or max(p.stat().st_mtime for p in databases) < time.time() - 48 * 3600:
                    return "UNAVAILABLE"
            except (OSError, subprocess.TimeoutExpired):
                return "UNAVAILABLE"
        name = None
        try:
            with tempfile.NamedTemporaryFile(delete=False) as source:
                name = source.name
                source.write(raw)
            result = subprocess.run(["clamscan", "--no-summary", "--alert-exceeds-max=yes",
                                     "--max-filesize=1024M", "--max-scansize=2048M",
                                     "--database=" + str(self.database), name],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
            return "PASS" if result.returncode == 0 else "FAIL" if result.returncode == 1 else "UNAVAILABLE"
        except (OSError, subprocess.TimeoutExpired):
            return "UNAVAILABLE"
        finally:
            if name:
                os.unlink(name)


def sanitize_preview(raw, media_type):
    from PIL import Image, ImageOps
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(raw)) as source:
                expected = "JPEG" if media_type == "image/jpeg" else "PNG"
                if source.format != expected or source.width * source.height > 40_000_000:
                    raise IngestionError("PREVIEW_DECODE_INVALID")
                source.verify()
            with Image.open(io.BytesIO(raw)) as source:
                source.load()
                oriented = ImageOps.exif_transpose(source)
                # A newly allocated pixel buffer has no EXIF, XMP, comments or ICC.
                clean = Image.new("RGB", oriented.size, "white")
                if oriented.mode in {"RGBA", "LA"} or "transparency" in oriented.info:
                    rgba = oriented.convert("RGBA")
                    clean.paste(rgba, mask=rgba.getchannel("A"))
                else:
                    clean.paste(oriented.convert("RGB"))
                output = io.BytesIO()
                clean.save(output, format="JPEG", quality=95, exif=b"", icc_profile=None)
                result = output.getvalue()
            if len(result) > 32 * 1024 * 1024:
                raise IngestionError("PREVIEW_SIZE_LIMIT")
            with Image.open(io.BytesIO(result)) as check:
                if check.getexif() or any(k in check.info for k in ("exif", "xmp", "icc_profile", "comment")):
                    raise IngestionError("PREVIEW_SANITATION_FAILED")
            return result
    except IngestionError:
        raise
    except Exception:
        raise IngestionError("PREVIEW_DECODE_INVALID") from None
