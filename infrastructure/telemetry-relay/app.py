import json, os, re, tempfile
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

TOKEN = os.environ.get('DSG_TELEMETRY_INGEST_TOKEN', '')
PORT = int(os.environ.get('PORT', '8080'))
OBSERVATORY_STORE = Path(os.environ.get('DSG_RELAY_STORE_PATH', '/data/observatory-status.json'))
EAGLE_HEALTH_STORE = Path(os.environ.get('DSG_RELAY_EAGLE_HEALTH_STORE_PATH', '/data/eagle-health.json'))
SESSION_COMPLETED_SHADOW_STORE = Path(os.environ.get('DSG_RELAY_SESSION_COMPLETED_SHADOW_STORE_PATH', '/data/session-completed-shadow.ndjson'))
ALLOWED_ORIGIN = os.environ.get('DSG_RELAY_ALLOWED_ORIGIN', '*')
AUTHORIZED_SOURCE = os.environ.get('DSG_RELAY_AUTHORIZED_SOURCE', 'EAGLE30154')
MAX_BODY_BYTES = int(os.environ.get('DSG_RELAY_MAX_BODY_BYTES', '65536'))
STATS = {
    'accepted': 0,
    'rejected': 0,
    'last_accepted_utc': None,
    'last_correlation_id': None,
    'channels': {
        'observatory_status': {'accepted': 0, 'rejected': 0, 'last_accepted_utc': None, 'last_correlation_id': None},
        'eagle_health': {'accepted': 0, 'rejected': 0, 'last_accepted_utc': None, 'last_correlation_id': None},
        'session_completed_shadow': {'accepted': 0, 'rejected': 0, 'last_accepted_utc': None, 'last_correlation_id': None},
    },
}


def parse_utc(value):
    if not isinstance(value, str):
        raise ValueError('timestamp must be string')
    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)


def validate_freshness(payload):
    observed = parse_utc(payload.get('observed_at_utc'))
    fresh_until = parse_utc(payload.get('fresh_until_utc'))
    if fresh_until < observed:
        raise ValueError('fresh_until_utc precedes observed_at_utc')
    if fresh_until < datetime.now(timezone.utc):
        raise ValueError('snapshot already stale')


def validate_observatory_status(payload, idempotency_key):
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
    validate_freshness(payload)
    return correlation_id


def validate_eagle_health(payload, idempotency_key):
    if payload.get('schema_version') != '1.0':
        raise ValueError('EAGLE health schema_version must be 1.0')
    if payload.get('component') != 'DSG.EagleHealthPortalProjection':
        raise ValueError('invalid EAGLE health component')
    if payload.get('host') != AUTHORIZED_SOURCE:
        raise PermissionError('host not authorized')
    if payload.get('source_component') != 'DSG.EagleHostHealthCollector':
        raise ValueError('invalid EAGLE health source_component')

    summary = payload.get('summary') or {}
    if summary.get('state') != 'UNKNOWN' or summary.get('reason') != 'POLICY_NOT_ACTIVATED':
        raise ValueError('EAGLE health summary policy mismatch')

    diagnostics = payload.get('diagnostics') or {}
    if diagnostics.get('projection_mode') != 'READ_ONLY_PUBLIC':
        raise ValueError('EAGLE health projection must be READ_ONLY_PUBLIC')
    if diagnostics.get('automatic_remediation') is not False:
        raise ValueError('automatic remediation must be false')
    if diagnostics.get('safety_authority') != 'OUTSIDE_SCOPE':
        raise ValueError('Safety Authority must remain outside scope')

    correlation_id = payload.get('source_correlation_id')
    if not correlation_id or idempotency_key != correlation_id:
        raise ValueError('Idempotency-Key must equal source_correlation_id')
    validate_freshness(payload)
    return correlation_id


def atomic_store(raw, store, prefix):
    store.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=prefix, suffix='.tmp', dir=str(store.parent))
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, store)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)



def validate_session_completed_shadow(payload, idempotency_key):
    if payload.get('contract_id') != 'DSG.Observation.Event.SessionCompleted':
        raise ValueError('invalid SessionCompleted contract_id')
    if payload.get('contract_version') != '1.0.0':
        raise ValueError('unsupported SessionCompleted contract_version')
    producer = payload.get('producer') or {}
    if producer.get('instance') != AUTHORIZED_SOURCE:
        raise PermissionError('producer instance not authorized')
    if producer.get('mode') != 'shadow':
        raise ValueError('only shadow transport is enabled by this endpoint')
    if payload.get('activation_mode') != 'shadow':
        raise ValueError('activation_mode must be shadow')
    if payload.get('runtime_event_published') is not False:
        raise ValueError('runtime_event_published must remain false')
    if payload.get('safety_authority') != 'NONE':
        raise ValueError('safety_authority must remain NONE')
    if payload.get('command_authority') != 'NONE':
        raise ValueError('command_authority must remain NONE')

    message_id = payload.get('message_id')
    if not message_id or idempotency_key != message_id:
        raise ValueError('Idempotency-Key must equal message_id')

    subject = payload.get('subject') or {}
    body = payload.get('payload') or {}
    if not subject.get('session_id') or body.get('session_id') != subject.get('session_id'):
        raise ValueError('subject and payload session_id must match')
    if not re.fullmatch(r'[0-9a-fA-F]{64}', str(body.get('manifest_sha256', ''))):
        raise ValueError('payload.manifest_sha256 must be a SHA-256 hex digest')
    if not isinstance(body.get('evidence_files'), list) or not body.get('evidence_files'):
        raise ValueError('payload.evidence_files must be non-empty')
    if body.get('diagnostic_status') not in {'GREEN', 'YELLOW', 'RED', 'UNKNOWN'}:
        raise ValueError('invalid diagnostic_status')
    return message_id


def append_session_event(raw, store, message_id):
    store.parent.mkdir(parents=True, exist_ok=True)
    if store.exists():
        with store.open('rb') as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    existing = json.loads(line.decode('utf-8'))
                except Exception:
                    continue
                if existing.get('message_id') == message_id:
                    return False
    with store.open('ab') as handle:
        handle.write(raw.rstrip(b'\r\n') + b'\n')
        handle.flush()
        os.fsync(handle.fileno())
    return True


def read_last_session_event(store):
    if not store.exists():
        return None
    last = None
    with store.open('rb') as handle:
        for line in handle:
            if line.strip():
                last = line.rstrip(b'\r\n')
    return last

def record_result(channel, accepted, correlation_id=None):
    now = datetime.now(timezone.utc).isoformat()
    key = 'accepted' if accepted else 'rejected'
    STATS[key] += 1
    STATS['channels'][channel][key] += 1
    if accepted:
        STATS['last_accepted_utc'] = now
        STATS['last_correlation_id'] = correlation_id
        STATS['channels'][channel]['last_accepted_utc'] = now
        STATS['channels'][channel]['last_correlation_id'] = correlation_id


class Handler(BaseHTTPRequestHandler):
    server_version = 'DSGTelemetryRelay/1.2'

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

    def write_store(self, store):
        if not store.exists():
            self.write_json(404, {'error': 'snapshot_not_found'})
            return
        raw = store.read_bytes()
        self.send_response(200)
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
            self.write_json(200, {'component': 'DSG.ObservatoryStatusTelemetryRelay.Hosted', 'state': 'RUNNING', **STATS})
            return
        if path == '/v1/observatory-status':
            self.write_store(OBSERVATORY_STORE)
            return
        if path == '/v1/eagle-health':
            self.write_store(EAGLE_HEALTH_STORE)
            return
        if path == '/v1/session-completed-shadow':
            raw = read_last_session_event(SESSION_COMPLETED_SHADOW_STORE)
            if raw is None:
                self.write_json(404, {'error': 'event_not_found'})
                return
            self.send_response(200)
            self.headers_common()
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return
        self.write_json(404, {'error': 'not_found'})

    def do_POST(self):
        path = urlparse(self.path).path.rstrip('/')
        if path == '/v1/session-completed-shadow':
            channel = 'session_completed_shadow'
            authorization = self.headers.get('Authorization', '')
            if not TOKEN or authorization != 'Bearer ' + TOKEN:
                record_result(channel, False)
                self.write_json(401, {'error': 'unauthorized'})
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if length <= 0 or length > MAX_BODY_BYTES:
                    raise ValueError('invalid payload length')
                raw = self.rfile.read(length)
                payload = json.loads(raw.decode('utf-8'))
                message_id = validate_session_completed_shadow(payload, self.headers.get('Idempotency-Key'))
                created = append_session_event(raw, SESSION_COMPLETED_SHADOW_STORE, message_id)
                record_result(channel, True, message_id)
                if not created:
                    self.write_json(200, {'result': 'no_op', 'channel': channel, 'message_id': message_id})
                else:
                    self.write_json(202, {'result': 'accepted', 'channel': channel, 'message_id': message_id})
            except PermissionError as exc:
                record_result(channel, False)
                self.write_json(403, {'error': 'forbidden', 'message': str(exc)})
            except Exception as exc:
                record_result(channel, False)
                self.write_json(422, {'error': 'validation_failed', 'message': str(exc)})
            return

        channels = {
            '/v1/observatory-status': ('observatory_status', OBSERVATORY_STORE, validate_observatory_status, 'observatory-status-'),
            '/v1/eagle-health': ('eagle_health', EAGLE_HEALTH_STORE, validate_eagle_health, 'eagle-health-'),
        }
        if path not in channels:
            self.write_json(404, {'error': 'not_found'})
            return

        channel, store, validator, prefix = channels[path]
        authorization = self.headers.get('Authorization', '')
        if not TOKEN or authorization != 'Bearer ' + TOKEN:
            record_result(channel, False)
            self.write_json(401, {'error': 'unauthorized'})
            return

        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length <= 0 or length > MAX_BODY_BYTES:
                raise ValueError('invalid payload length')
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode('utf-8'))
            correlation_id = validator(payload, self.headers.get('Idempotency-Key'))
            atomic_store(raw, store, prefix)
            record_result(channel, True, correlation_id)
            self.write_json(202, {'result': 'accepted', 'channel': channel, 'correlation_id': correlation_id})
        except PermissionError as exc:
            record_result(channel, False)
            self.write_json(403, {'error': 'forbidden', 'message': str(exc)})
        except Exception as exc:
            record_result(channel, False)
            self.write_json(422, {'error': 'validation_failed', 'message': str(exc)})


if __name__ == '__main__':
    if not TOKEN:
        raise SystemExit('DSG_TELEMETRY_INGEST_TOKEN is required')
    print(f'DSG hosted relay listening on 0.0.0.0:{PORT}', flush=True)
    ThreadingHTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
