import json, os, tempfile
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

TOKEN = os.environ.get('DSG_TELEMETRY_INGEST_TOKEN', '')
PORT = int(os.environ.get('PORT', '8080'))
STORE = Path(os.environ.get('DSG_RELAY_STORE_PATH', '/data/observatory-status.json'))
ALLOWED_ORIGIN = os.environ.get('DSG_RELAY_ALLOWED_ORIGIN', '*')
AUTHORIZED_SOURCE = os.environ.get('DSG_RELAY_AUTHORIZED_SOURCE', 'EAGLE30154')
MAX_BODY_BYTES = int(os.environ.get('DSG_RELAY_MAX_BODY_BYTES', '65536'))
STATS = {'accepted': 0, 'rejected': 0, 'last_accepted_utc': None, 'last_correlation_id': None}


def parse_utc(value):
    if not isinstance(value, str):
        raise ValueError('timestamp must be string')
    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)


def validate(payload, idempotency_key):
    if payload.get('schema_version') != '1.1':
        raise ValueError('schema_version must be 1.1')
    if payload.get('source_instance') != AUTHORIZED_SOURCE:
        raise PermissionError('source_instance not authorized')

    safety = payload.get('safety') or {}
    if safety.get('observed_state') not in {'SAFE', 'UNSAFE', 'UNKNOWN'}:
        raise ValueError('safety observed_state must be SAFE, UNSAFE, or UNKNOWN')
    if safety.get('authority') not in {'LOCAL_SAFETY_AUTHORITY', 'NINA_SAFETY_MONITOR_OBSERVATION'}:
        raise ValueError('safety authority mismatch')

    correlation_id = payload.get('correlation_id')
    if not correlation_id or idempotency_key != correlation_id:
        raise ValueError('Idempotency-Key must equal correlation_id')
    observed = parse_utc(payload.get('observed_at_utc'))
    fresh_until = parse_utc(payload.get('fresh_until_utc'))
    if fresh_until < observed:
        raise ValueError('fresh_until_utc precedes observed_at_utc')
    if fresh_until < datetime.now(timezone.utc):
        raise ValueError('snapshot already stale')


def atomic_store(raw):
    STORE.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='observatory-status-', suffix='.tmp', dir=str(STORE.parent))
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, STORE)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


class Handler(BaseHTTPRequestHandler):
    server_version = 'DSGTelemetryRelay/1.0'

    def log_message(self, fmt, *args):
        print('%s %s' % (datetime.now(timezone.utc).isoformat(), fmt % args), flush=True)

    def headers_common(self):
        self.send_header('Access-Control-Allow-Origin', ALLOWED_ORIGIN)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Type', 'application/json; charset=utf-8')

    def write_json(self, status, body):
        raw = json.dumps(body, separators=(',', ':')).encode('utf-8')
        self.send_response(status)
        self.headers_common()
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', ALLOWED_ORIGIN)
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type, Idempotency-Key')
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path.rstrip('/') or '/'
        if path == '/health':
            self.write_json(200, {'component':'DSG.ObservatoryStatusTelemetryRelay.Hosted','state':'RUNNING',**STATS})
            return
        if path == '/v1/observatory-status':
            if not STORE.exists():
                self.write_json(404, {'error':'snapshot_not_found'})
                return
            raw = STORE.read_bytes()
            self.send_response(200)
            self.headers_common()
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return
        self.write_json(404, {'error':'not_found'})

    def do_POST(self):
        path = urlparse(self.path).path.rstrip('/')
        if path != '/v1/observatory-status':
            self.write_json(404, {'error':'not_found'})
            return
        authorization = self.headers.get('Authorization', '')
        if not TOKEN or authorization != 'Bearer ' + TOKEN:
            STATS['rejected'] += 1
            self.write_json(401, {'error':'unauthorized'})
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length <= 0 or length > MAX_BODY_BYTES:
                raise ValueError('invalid payload length')
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode('utf-8'))
            validate(payload, self.headers.get('Idempotency-Key'))
            atomic_store(raw)
            STATS['accepted'] += 1
            STATS['last_accepted_utc'] = datetime.now(timezone.utc).isoformat()
            STATS['last_correlation_id'] = payload['correlation_id']
            self.write_json(202, {'result':'accepted','correlation_id':payload['correlation_id']})
        except PermissionError as exc:
            STATS['rejected'] += 1
            self.write_json(403, {'error':'forbidden','message':str(exc)})
        except Exception as exc:
            STATS['rejected'] += 1
            self.write_json(422, {'error':'validation_failed','message':str(exc)})


if __name__ == '__main__':
    if not TOKEN:
        raise SystemExit('DSG_TELEMETRY_INGEST_TOKEN is required')
    print(f'DSG hosted relay listening on 0.0.0.0:{PORT}', flush=True)
    ThreadingHTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
