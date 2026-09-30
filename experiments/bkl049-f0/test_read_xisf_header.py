import io
import struct
import unittest
from read_xisf_header import inspect, LIMIT


def wrap(xml):
    data = xml.encode()
    return b'XISF0100' + struct.pack('<II', len(data), 0) + data


class HeaderTests(unittest.TestCase):
    def test_header_only(self):
        data = wrap('<xisf version="1.0"><Image/></xisf>')
        stream = io.BytesIO(data + b'PRIVATE_PIXEL_PAYLOAD')
        result = inspect(stream)
        self.assertEqual(stream.tell(), len(data))
        self.assertEqual(result['images'][0]['historyStatus'], 'UNAVAILABLE')

    def test_inline_scoped_private(self):
        data = wrap('<xisf version="1.0"><Image><Property id="PixInsight:ProcessingHistory" type="String">&lt;ProcessingHistory version="1.0"&gt;&lt;instance class="PRIVATE"&gt;&lt;parameter id="secret" value="private"/&gt;&lt;table/&gt;&lt;time/&gt;&lt;/instance&gt;&lt;/ProcessingHistory&gt;</Property></Image><Image/></xisf>')
        result = inspect(io.BytesIO(data))
        self.assertEqual(result['imageCount'], 2)
        self.assertEqual(result['images'][0]['instances'], [{'parameterCount': 1, 'tableCount': 1, 'timeCount': 1}])
        self.assertNotIn('PRIVATE', str(result))
        self.assertNotIn('secret', str(result))
        self.assertEqual(result['images'][1]['historyStatus'], 'UNAVAILABLE')

    def test_external_not_followed(self):
        for attr in ['location="attachment:999999:100"', 'compression="zlib"', 'encoding="base64"']:
            with self.subTest(attr=attr):
                result = inspect(io.BytesIO(wrap('<xisf version="1.0"><Image><Property id="PixInsight:ProcessingHistory" type="String" ' + attr + '/></Image></xisf>')))
                self.assertEqual(result['images'][0]['historyStatus'], 'UNSUPPORTED_REPRESENTATION')

    def test_rejections(self):
        cases = [b'', b'BADMAGIC' + bytes(8), b'XISF0100' + struct.pack('<II', LIMIT+1, 0),
                 b'XISF0100' + struct.pack('<II', 5, 1), b'XISF0100' + struct.pack('<II', 50, 0) + b'<x/>',
                 wrap('<!DOCTYPE xisf><xisf version="1.0"/>'), wrap('<xisf version="2.0"/>'),
                 wrap('<xisf version="1.0">' + '<x>'*34 + '</x>'*34 + '</xisf>'),
                 wrap('<xisf version="1.0"><Image>' + '<Property id="PixInsight:ProcessingHistory"/>'*2 + '</Image></xisf>'),
                 wrap('<xisf version="1.0">\x00</xisf>')]
        for data in cases:
            with self.subTest(data=data[:16]):
                with self.assertRaises(ValueError):
                    inspect(io.BytesIO(data))


if __name__ == '__main__':
    unittest.main()
