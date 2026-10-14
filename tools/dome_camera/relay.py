"""Read-only RTSP to public JPEG/MJPEG relay; source credentials stay in a private config."""
from __future__ import annotations

import argparse
import datetime as dt
import ipaddress
import json
import os
import selectors
import signal
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

PREFIX = "/dome-camera/"
ORIGIN = "https://maininimassimo-bit.github.io"
PUBLIC_BASE = "https://digitalstargate.freeddns.it:23232/dome-camera/"
MAX_FRAME = 1024 * 1024
FRESH_SECONDS = 8


def utc(value: float) -> str:
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat().replace("+00:00", "Z")


def load_source(path: Path) -> str:
    if os.name == "posix" and path.stat().st_mode & 0o077:
        raise ValueError("Camera configuration permissions must be private")
    value = json.loads(path.read_text(encoding="utf-8"))
    source = value.get("sourceUrl") if isinstance(value, dict) else None
    if not isinstance(source, str) or len(source) > 2048 or any(c in source for c in "\r\n\x00"):
        raise ValueError("Invalid private camera configuration")
    uri = urlsplit(source)
    host = ipaddress.ip_address(uri.hostname or "")
    if (uri.scheme != "rtsp" or not uri.username or not uri.password or uri.port != 554
            or not host.is_private or host.is_loopback or host.is_link_local
            or host.is_multicast or host.is_unspecified or uri.path != "/live/ch0"
            or uri.query or uri.fragment):
        raise ValueError("Invalid private camera source")
    return source


class Frames:
    def __init__(self) -> None:
        self.changed = threading.Condition()
        self.frame: bytes | None = None
        self.received = 0.0
        self.monotonic = 0.0
        self.sequence = 0

    def publish(self, frame: bytes) -> None:
        if not (4 <= len(frame) <= MAX_FRAME and frame.startswith(b"\xff\xd8") and frame.endswith(b"\xff\xd9")):
            raise ValueError("Invalid JPEG frame")
        with self.changed:
            self.frame = frame
            self.received = time.time()
            self.monotonic = time.monotonic()
            self.sequence += 1
            self.changed.notify_all()

    def clear(self) -> None:
        with self.changed:
            self.frame = None
            self.changed.notify_all()

    def current(self) -> tuple[bytes | None, float, int]:
        with self.changed:
            frame = self.frame if time.monotonic() - self.monotonic <= FRESH_SECONDS else None
            return frame, self.received, self.sequence

    def status(self) -> dict:
        frame, received, sequence = self.current()
        return {"schemaVersion": "1.0", "kind": "DSG_DOME_CAMERA_PUBLIC_V1",
                "state": "CURRENT" if frame else "UNAVAILABLE",
                "receivedAt": utc(received) if frame else None,
                "freshUntil": utc(received + FRESH_SECONDS) if frame else None,
                "sequence": sequence, "frameUrl": PUBLIC_BASE + "frame.jpg",
                "streamUrl": PUBLIC_BASE + "live.mjpg", "commandAuthority": False,
                "safetyAuthority": False, "audio": False}


def private_input(source: str) -> int:
    # Linux anonymous descriptor: no URI/password in argv, environment or a public file.
    descriptor = os.memfd_create("dsg-camera-input", os.MFD_CLOEXEC)
    escaped = source.replace("\\", "\\\\").replace("'", "'\\''")
    os.write(descriptor, ("ffconcat version 1.0\nfile '" + escaped + "'\n").encode())
    os.lseek(descriptor, 0, 0)
    return descriptor


def producer_command(descriptor: int) -> list[str]:
    return ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "quiet",
            "-threads", "1", "-err_detect", "explode", "-f", "concat", "-safe", "0",
            "-protocol_whitelist", "file,tcp,udp,rtp", "-i", f"/proc/self/fd/{descriptor}",
            "-an", "-sn", "-dn", "-threads", "1", "-vf", "fps=2,scale=960:-2", "-q:v", "5",
            "-f", "image2pipe", "-c:v", "mjpeg", "pipe:1"]


def produce(source: str, frames: Frames, stopped: threading.Event) -> None:
    # One producer shared by all viewers. No audio, recording, camera controls or shell execution.
    delay = 1
    while not stopped.is_set():
        process, descriptor = None, None
        try:
            descriptor = private_input(source)
            process = subprocess.Popen(producer_command(descriptor), pass_fds=(descriptor,),
                                       stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            os.close(descriptor)
            descriptor = None
            with selectors.DefaultSelector() as ready:
                ready.register(process.stdout, selectors.EVENT_READ)
                buffer = bytearray()
                last = time.monotonic()
                while not stopped.is_set() and process.poll() is None:
                    if time.monotonic() - last > 15:
                        break
                    if not ready.select(timeout=0.5):
                        continue
                    chunk = os.read(process.stdout.fileno(), 65536)
                    if not chunk:
                        break
                    buffer.extend(chunk)
                    while True:
                        start = buffer.find(b"\xff\xd8")
                        if start < 0:
                            if len(buffer) > MAX_FRAME:
                                raise ValueError("Frame limit")
                            break
                        if start:
                            del buffer[:start]
                        end = buffer.find(b"\xff\xd9", 2)
                        if end < 0:
                            if len(buffer) > MAX_FRAME:
                                raise ValueError("Frame limit")
                            break
                        frames.publish(bytes(buffer[:end + 2]))
                        del buffer[:end + 2]
                        last = time.monotonic()
                        delay = 1
        except Exception:
            # Never send FFmpeg errors, source URL or private configuration into logs/API.
            pass
        finally:
            if descriptor is not None:
                os.close(descriptor)
            frames.clear()
            if process is not None:
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait(timeout=2)
                if process.stdout:
                    process.stdout.close()
        stopped.wait(delay)
        delay = min(delay * 2, 10)


class CameraServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], frames: Frames):
        self.frames = frames
        self.connections = threading.BoundedSemaphore(24)
        self.streams = threading.BoundedSemaphore(8)
        super().__init__(address, CameraHandler)

    def verify_request(self, request, client_address):
        request.settimeout(5)
        return self.connections.acquire(blocking=False)

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.connections.release()

    def handle_error(self, request, client_address):
        pass


class CameraHandler(BaseHTTPRequestHandler):
    server_version = "DSGDomeCamera"
    sys_version = ""

    def log_message(self, *args):
        pass

    def send_headers(self, status: int, content_type: str, length: int | None = None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Access-Control-Allow-Origin", ORIGIN)
        self.send_header("Vary", "Origin")
        if length is not None:
            self.send_header("Content-Length", str(length))
        self.end_headers()

    def do_GET(self):
        path = urlsplit(self.path).path
        if len(self.path) > 256:
            self.send_headers(404, "text/plain", 0)
            return
        if path == PREFIX + "status.json":
            value = json.dumps(self.server.frames.status(), separators=(",", ":")).encode()
            self.send_headers(200, "application/json", len(value))
            self.wfile.write(value)
            return
        frame, received, sequence = self.server.frames.current()
        if path not in [PREFIX + "frame.jpg", PREFIX + "live.mjpg"]:
            self.send_headers(404, "text/plain", 0)
            return
        if frame is None:
            self.send_headers(503, "text/plain", 0)
            return
        if path == PREFIX + "frame.jpg":
            self.send_headers(200, "image/jpeg", len(frame))
            self.wfile.write(frame)
            return
        if not self.server.streams.acquire(blocking=False):
            self.send_headers(503, "text/plain", 0)
            return
        try:
            self.send_headers(200, "multipart/x-mixed-replace; boundary=dsg-dome")
            while True:
                frame, received, sequence = self.server.frames.current()
                if frame is None:
                    break
                self.wfile.write(b"--dsg-dome\r\nContent-Type: image/jpeg\r\nContent-Length: "
                                 + str(len(frame)).encode() + b"\r\n\r\n" + frame + b"\r\n")
                self.wfile.flush()
                with self.server.frames.changed:
                    self.server.frames.changed.wait_for(
                        lambda: self.server.frames.sequence != sequence or self.server.frames.frame is None,
                        timeout=1)
        except (OSError, TimeoutError):
            pass
        finally:
            self.server.streams.release()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("/etc/digital-stargate/dome-camera.json"))
    args = parser.parse_args()
    try:
        source = load_source(args.config)
    except Exception:
        raise SystemExit("Private camera configuration unavailable or invalid") from None
    frames, stopped = Frames(), threading.Event()
    server = CameraServer(("127.0.0.1", 8076), frames)
    for sig in [signal.SIGTERM, signal.SIGINT]:
        signal.signal(sig, lambda *_: stopped.set())
    producer = threading.Thread(target=produce, args=(source, frames, stopped), daemon=True)
    producer.start()
    server.timeout = 0.5
    try:
        while not stopped.is_set():
            server.handle_request()
    finally:
        frames.clear()
        server.server_close()
        producer.join(timeout=4)


if __name__ == "__main__":
    main()
