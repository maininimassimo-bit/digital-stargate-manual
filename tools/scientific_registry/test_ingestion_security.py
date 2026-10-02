import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

from PIL import Image
from .ingestion_security import ClamScanner, sanitize_preview
from .photo_ingestion import IngestionError


class SecurityTests(unittest.TestCase):
    def test_missing_database_failed_refresh_never_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch('subprocess.run', return_value=SimpleNamespace(returncode=1)):
                self.assertEqual(ClamScanner(directory).scan(b'file'), 'UNAVAILABLE')

    def test_scanner_exit_codes_and_resource_flags(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, 'daily.cvd').write_bytes(b'synthetic definitions placeholder')
            for code, expected in [(0,'PASS'),(1,'FAIL'),(2,'UNAVAILABLE')]:
                with patch('subprocess.run', return_value=SimpleNamespace(returncode=code)) as run:
                    self.assertEqual(ClamScanner(directory).scan(b'file'), expected)
                    self.assertIn('--alert-exceeds-max=yes', run.call_args.args[0])
                    self.assertIn('--max-filesize=1024M', run.call_args.args[0])
                    self.assertFalse(Path(run.call_args.args[0][-1]).exists())

    def test_preview_wrong_type_truncated_or_bomb_reject(self):
        output=io.BytesIO();Image.new('RGB',(20,20),'red').save(output,format='PNG');raw=output.getvalue()
        for input_raw, media in ((raw,'image/jpeg'),(raw[:20],'image/png'),(b'\xff\xd8\xffinvalid','image/jpeg')):
            with self.assertRaises(IngestionError):
                sanitize_preview(input_raw,media)
        with patch.object(Image,'MAX_IMAGE_PIXELS',10):
            with self.assertRaises(IngestionError):
                sanitize_preview(raw,'image/png')


if __name__ == '__main__':
    unittest.main()
