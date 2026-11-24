"""Explicit manual publication gate; the temporal detector itself remains private."""
import base64, datetime as dt, grp, hashlib, json, os, re, socket, socketserver
import sqlite3, stat, struct, tempfile
from pathlib import Path
from zoneinfo import ZoneInfo
import cv2

STAMP = re.compile(r'^[0-9]{14}$')
UTC = dt.timezone.utc

def digest(data):
    return hashlib.sha256(data).hexdigest()

class Review:
    def __init__(self, config):
        self.cfg = config
        self.root = Path(config['candidates']).resolve(strict=True)
        self.public = Path(config['public']).resolve(strict=True)
        self.state = Path(config['state']).resolve(strict=True)
        self.cutoff = dt.datetime.fromisoformat(config['new_after']).astimezone(UTC)
        fixed = self.state / 'new-after.json'
        if fixed.exists():
            if json.loads(fixed.read_text()) != {'new_after': config['new_after']}:
                raise ValueError('La data iniziale della revisione è cambiata: manutenzione richiesta')
        else:
            with fixed.open('x') as stream:
                json.dump({'new_after': config['new_after']}, stream)
        self.db = sqlite3.connect(self.state / 'decisions.sqlite3')
        self.db.execute('CREATE TABLE IF NOT EXISTS decisions (stamp TEXT PRIMARY KEY, decision TEXT NOT NULL, version TEXT NOT NULL, actor TEXT NOT NULL, decided TEXT NOT NULL, published TEXT)')
        self.db.commit()

    def files(self, stamp):
        if not isinstance(stamp, str) or not STAMP.fullmatch(stamp):
            raise ValueError('Identificativo non valido')
        local = dt.datetime.strptime(stamp, '%Y%m%d%H%M%S').replace(tzinfo=ZoneInfo('Europe/Rome'))
        if local.astimezone(UTC) <= self.cutoff or local.astimezone(UTC) > dt.datetime.now(UTC) + dt.timedelta(minutes=2):
            raise ValueError('Fotogramma escluso dalla nuova revisione')
        # Allsky assigns post-midnight frames to the preceding observing night.
        nights = [local.strftime('%Y%m%d'), (local - dt.timedelta(days=1)).strftime('%Y%m%d')]
        for night in nights:
            folder = self.root / night / 'meteors'
            image = folder / ('meteors-' + stamp + '.jpg')
            meta = image.with_suffix('.json')
            if not image.is_file() or not meta.is_file():
                continue
            for path in [folder.parent, folder, image, meta]:
                if path.is_symlink() or not path.resolve().is_relative_to(self.root):
                    raise ValueError('Percorso non consentito')
            if image.stat().st_size > 10000000 or meta.stat().st_size > 1000000:
                raise ValueError('File oltre il limite')
            if dt.datetime.fromtimestamp(min(image.stat().st_mtime, meta.stat().st_mtime), UTC) <= self.cutoff:
                raise ValueError('File storico escluso')
            image_bytes = image.read_bytes()
            meta_bytes = meta.read_bytes()
            entries = json.loads(meta_bytes)
            if not isinstance(entries, list) or not entries or any(not isinstance(e, dict) or str(e.get('time')) != stamp for e in entries):
                raise ValueError('Metadati incoerenti')
            version = digest(image_bytes + b'\0' + meta_bytes)
            return image_bytes, entries, version
        raise ValueError('Candidato non trovato')

    def pending(self):
        result = []
        for path in sorted(self.root.glob('*/meteors/meteors-*.json'), reverse=True):
            stamp = path.stem.removeprefix('meteors-')
            if self.db.execute('SELECT 1 FROM decisions WHERE stamp=?', (stamp,)).fetchone():
                continue
            try:
                _, entries, version = self.files(stamp)
                result.append({'stamp': stamp, 'traces': len(entries), 'version': version})
            except (ValueError, OSError, json.JSONDecodeError):
                continue
            if len(result) == 100:
                break
        return {'cutoff': self.cfg['new_after'], 'pending': result}

    def preview(self, stamp):
        import numpy as np
        data, entries, version = self.files(stamp)
        image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError('Immagine illeggibile')
        height, width = image.shape[:2]
        ratio = min(1, 1000 / width)
        display = cv2.resize(image, (round(width * ratio), round(height * ratio)))
        for entry in entries:
            for point in ('p1', 'p2'):
                xy = entry.get(point)
                if isinstance(xy, list) and len(xy) == 2:
                    x, y = round(float(xy[0]) * ratio), round(float(xy[1]) * ratio)
                    cv2.circle(display, (x, y), 9, (0, 220, 255), 1)
        ok, encoded = cv2.imencode('.jpg', display, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not ok:
            raise ValueError('Anteprima non disponibile')
        return {'image': base64.b64encode(encoded).decode(), 'version': version, 'traces': len(entries)}

    def decide(self, stamp, version, action, actor):
        if action not in ('approve', 'reject') or not isinstance(actor, str) or not 1 <= len(actor) <= 80:
            raise ValueError('Decisione non valida')
        data, entries, current = self.files(stamp)
        if not isinstance(version, str) or current != version:
            raise ValueError('Il candidato Ã¨ cambiato: rivedere la nuova anteprima')
        previous = self.db.execute('SELECT decision, version, published FROM decisions WHERE stamp=?', (stamp,)).fetchone()
        if previous:
            if previous[0] != action or previous[1] != version:
                raise ValueError('Decisione giÃ  registrata')
            return {'decision': previous[0], 'published': previous[2], 'repeat': True}
        published = None
        if action == 'approve':
            target = self.public / ('meteors-' + stamp + '.jpg')
            if target.exists():
                # The existing detector owns this filename: never replace it.
                published = 'already-present'
            else:
                import numpy as np
                image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
                if image is None:
                    raise ValueError('Immagine illeggibile')
                h, w = image.shape[:2]
                thumb = cv2.resize(image, (180, max(1, round(h * 180 / w))))
                ok, encoded = cv2.imencode('.jpg', thumb)
                if not ok:
                    raise ValueError('Miniatura non disponibile')
                self.atomic_new(self.public / 'thumbnails' / target.name, encoded.tobytes())
                if self.atomic_new(target, data):
                    published = target.name
                else:
                    published = 'already-present'
        self.db.execute('INSERT INTO decisions VALUES (?,?,?,?,?,?)',
                        (stamp, action, version, actor, dt.datetime.now(UTC).isoformat(), published))
        self.db.commit()
        return {'decision': action, 'published': published, 'repeat': False}

    @staticmethod
    def atomic_new(target, data):
        if target.parent.is_symlink() or target.is_symlink():
            raise ValueError('Destinazione non consentita')
        fd, temp = tempfile.mkstemp(prefix='.review-', dir=target.parent)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.chmod(temp, 0o644)
            try:
                os.link(temp, target)
                return True
            except FileExistsError:
                return False
        finally:
            os.unlink(temp)

    def dispatch(self, request):
        action = request.get('action')
        if action == 'list':
            return self.pending()
        if action == 'preview':
            return self.preview(request.get('stamp'))
        return self.decide(request.get('stamp'), request.get('version'), action, request.get('actor'))

class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        _, uid, _ = struct.unpack('3i', self.request.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))
        if uid not in self.server.allowed_uids:
            return
        raw = self.rfile.readline(16385)
        if len(raw) > 16384 or not raw.endswith(b'\n'):
            return
        try:
            result = {'ok': True, 'result': self.server.review.dispatch(json.loads(raw))}
        except Exception as exc:
            result = {'ok': False, 'error': str(exc) if isinstance(exc, ValueError) else 'Operazione non riuscita'}
        self.wfile.write(json.dumps(result, ensure_ascii=True).encode() + b'\n')

def serve(config_path):
    import pwd
    config = json.loads(Path(config_path).read_text())
    review = Review(config)
    path = Path(config['socket'])
    if path.exists():
        if not stat.S_ISSOCK(path.lstat().st_mode):
            raise RuntimeError('Socket path occupied')
        path.unlink()
    with socketserver.UnixStreamServer(str(path), Handler) as server:
        os.chmod(path, 0o660)
        server.allowed_uids = {0, pwd.getpwnam('www-data').pw_uid}
        server.review = review
        server.serve_forever()

if __name__ == '__main__':
    import sys
    serve(sys.argv[1])
