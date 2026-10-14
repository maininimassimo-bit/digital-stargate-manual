import importlib.util
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('relay', Path(__file__).with_name('relay.py'))
relay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(relay)
JPEG = b'\xff\xd8test\xff\xd9'


class RelayTests(unittest.TestCase):
    def test_freshness_and_no_private_metadata(self):
        frames = relay.Frames()
        self.assertEqual(frames.status()['state'], 'UNAVAILABLE')
        with patch.object(relay.time, 'time', return_value=100), patch.object(relay.time, 'monotonic', return_value=50):
            frames.publish(JPEG)
            self.assertEqual(frames.status()['state'], 'CURRENT')
        with patch.object(relay.time, 'monotonic', return_value=59):
            self.assertIsNone(frames.current()[0])
            self.assertIsNone(frames.status()['receivedAt'])
        self.assertNotIn('sourceUrl', frames.status())
        self.assertFalse(frames.status()['audio'])
        frames.clear()
        self.assertIsNone(frames.current()[0])

    def test_source_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'private.json'
            for source in ['https://example.com/live/ch0', 'rtsp://a:b@127.0.0.1:554/live/ch0',
                           'rtsp://a:b@8.8.8.8:554/live/ch0', 'rtsp://a:b@192.168.1.2:554/other',
                           'rtsp://a:b@192.168.1.2:554/live/ch0\n']:
                path.write_text(json.dumps({'sourceUrl': source}))
                path.chmod(0o600)
                with self.assertRaises(ValueError):
                    relay.load_source(path)

    def test_http_routes_and_unavailability(self):
        frames = relay.Frames()
        server = relay.CameraServer(('127.0.0.1', 0), frames)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = 'http://127.0.0.1:%d' % server.server_port
        try:
            with urllib.request.urlopen(base + '/dome-camera/status.json') as response:
                self.assertEqual(json.load(response)['state'], 'UNAVAILABLE')
                self.assertEqual(response.headers['Access-Control-Allow-Origin'], relay.ORIGIN)
                self.assertIn('no-store', response.headers['Cache-Control'])
            for route, code in [('/dome-camera/frame.jpg', 503), ('/dome-camera/live.mjpg', 503),
                                ('/dome-camera/private.json', 404), ('/dome-camera/../private.json', 404)]:
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(base + route)
                self.assertEqual(error.exception.code, code)
            frames.publish(JPEG)
            with urllib.request.urlopen(base + '/dome-camera/frame.jpg') as response:
                self.assertEqual(response.read(), JPEG)
            frames.clear()
            with urllib.request.urlopen(base + '/dome-camera/status.json') as response:
                self.assertEqual(json.load(response)['state'], 'UNAVAILABLE')
        finally:
            server.shutdown()
            server.server_close()
            thread.join(2)

    def test_argv_and_frame_bounds(self):
        command = relay.producer_command(7)
        self.assertIn('/proc/self/fd/7', command)
        self.assertFalse(any('rtsp://' in value for value in command))
        self.assertIn('-an', command)
        for bad in [b'', b'not jpeg', b'\xff\xd8' + b'x' * relay.MAX_FRAME + b'\xff\xd9']:
            with self.assertRaises(ValueError):
                relay.Frames().publish(bad)


if __name__ == '__main__':
    unittest.main()
