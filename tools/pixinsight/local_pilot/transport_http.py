"""Authenticated queue HTTP adapter; deployed only after activation approval."""
import hashlib
import re
import secrets
from http.server import BaseHTTPRequestHandler

from tools.pixinsight.local_pilot.broker import ProtocolError, decode, encode, require, opaque
from tools.scientific_registry.ingestion_storage import Conflict
from tools.scientific_registry.photo_ingestion import IngestionError
from tools.pixinsight.workflow_archive.archive import ArchiveError


class AuthError(ValueError):
    pass


def google_owner(token, client_id, owner_email):
    from google.auth.transport.requests import Request
    from google.oauth2 import id_token
    try:
        claims = id_token.verify_oauth2_token(token, Request(), client_id)
        if claims.get("email_verified") is not True or claims.get("email", "").lower() != owner_email.lower():
            raise AuthError()
    except Exception:
        raise AuthError() from None


def handler_for(broker, authenticate_owner, portal_origin, worker_digest, scientific=None):
    require(re.fullmatch(r"[a-f0-9]{64}", worker_digest) is not None, "WORKER_DIGEST_INVALID")
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def send(self, code, value, media="application/json"):
            raw = value if isinstance(value, bytes) else encode(value)
            self.send_response(code)
            for name, value in (("Content-Type", media), ("Content-Length", str(len(raw))),
                                ("Cache-Control", "no-store"), ("X-Content-Type-Options", "nosniff")):
                self.send_header(name, value)
            if self.headers.get("Origin") == portal_origin:
                self.send_header("Access-Control-Allow-Origin", portal_origin)
                self.send_header("Vary", "Origin")
            self.end_headers()
            self.wfile.write(raw)

        def authenticate(self, worker=False):
            if len(self.headers.get_all("Authorization", [])) != 1:
                raise AuthError()
            header = self.headers.get("Authorization", "")
            if not header.startswith("Bearer ") or not 1 <= len(header[7:]) <= 8192:
                raise AuthError()
            token = header[7:]
            if worker:
                if self.headers.get("Origin") is not None or not re.fullmatch(r"[a-f0-9]{64}", token):
                    raise AuthError()
                if not secrets.compare_digest(hashlib.sha256(token.encode()).hexdigest(), worker_digest):
                    raise AuthError()
            else:
                if self.headers.get("Origin") != portal_origin:
                    raise AuthError()
                authenticate_owner(token)

        def body(self, limit=16384):
            require(len(self.headers.get_all("Content-Length", [])) == 1 and not self.headers.get("Transfer-Encoding"), "BODY_SIZE")
            value = self.headers.get("Content-Length", "")
            require(re.fullmatch(r"[0-9]{1,8}", value) is not None and 0 < int(value) <= limit, "BODY_SIZE")
            require(self.headers.get("Content-Type") == "application/json", "CONTENT_TYPE")
            self.connection.settimeout(20)
            raw = self.rfile.read(int(value))
            require(len(raw) == int(value), "BODY_INCOMPLETE")
            return decode(raw)

        def do_OPTIONS(self):
            if self.headers.get("Origin") != portal_origin:
                return self.send(403, {"error": "ACCESS_DENIED"})
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", portal_origin)
            self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Vary", "Origin")
            self.end_headers()

        def dispatch(self):
            path = self.path
            if self.command == "GET" and path == "/health":
                return self.send(200, {"protocol": "DSG_PIAI_QUEUE_V1", "aiMode": "SESSION_ASSISTED", "providerRequests": 0})
            worker = path.startswith("/v1/worker/")
            self.authenticate(worker)
            if scientific:
                if self.command == "GET" and path == "/v1/science/options":
                    return self.send(200, scientific.options())
                if self.command == "GET" and path == "/v1/science/jobs":
                    return self.send(200, {"jobs": scientific.jobs()})
                if self.command == "POST" and path == "/v1/science/jobs":
                    return self.send(200, scientific.create(self.body()))
                if self.command == "POST" and path == "/v1/worker/science/register":
                    return self.send(200, scientific.register(self.body()))
                match = re.fullmatch(r"/v1/(worker/)?science/(PIAI_[a-f0-9]{32})/(context|result|preview|workflow|correlations|decision)", path)
                if match:
                    worker_route, job_id, action = match.groups()
                    if worker_route and self.command == "GET" and action == "context":
                        return self.send(200, scientific.context(job_id))
                    if worker_route and self.command == "POST" and action == "result":
                        result = scientific.deliver(job_id, self.body(9 * 1024 * 1024))
                        return self.send(200, {"jobId": job_id, "reviewSha256": result["reviewSha256"], "publication": "NONE"})
                    if not worker_route and self.command == "GET" and action == "result":
                        return self.send(200, scientific.result(job_id))
                    if not worker_route and self.command == "GET" and action in {"preview", "workflow", "correlations"}:
                        return self.send(200, scientific.asset(job_id, action), "image/jpeg" if action == "preview" else "application/json" if action == "correlations" else "text/plain; charset=utf-8")
                    if not worker_route and self.command == "POST" and action == "decision":
                        return self.send(200, scientific.decide(job_id, self.body()))
            if self.command == "POST" and path == "/v1/jobs":
                return self.send(200, broker.create(self.body()))
            match = re.fullmatch(r"/v1/jobs/(PIAI_[a-f0-9]{32})(/cancel)?", path)
            if match and not worker:
                job_id, action = match.groups()
                if self.command == "GET" and action is None:
                    return self.send(200, broker.status(job_id))
                if self.command == "POST" and action == "/cancel":
                    require(self.body() == {}, "REQUEST_FIELDS")
                    return self.send(200, broker.cancel(job_id))
            if self.command == "POST" and path == "/v1/worker/claim":
                request = self.body()
                require(isinstance(request, dict) and set(request) == {"workerId", "rootId"} and opaque(request["workerId"]) and opaque(request["rootId"]), "REQUEST_FIELDS")
                return self.send(200, {"job": broker.claim(request["workerId"], request["rootId"])})
            match = re.fullmatch(r"/v1/worker/(PIAI_[a-f0-9]{32})/report", path)
            if self.command == "POST" and match:
                request = self.body()
                require(isinstance(request, dict) and set(request) == {"workerId", "report"}, "REQUEST_FIELDS")
                return self.send(200, broker.report(match[1], request["workerId"], request["report"]))
            return self.send(404, {"error": "NOT_FOUND"})

        def handle_request(self):
            try:
                self.dispatch()
            except AuthError:
                self.send(403, {"error": "ACCESS_DENIED"})
            except (ProtocolError, IngestionError, ArchiveError) as error:
                self.send(400, {"error": str(error)})
            except Conflict:
                self.send(409, {"error": "CONFLICT_RETRY_IDENTICAL"})
            except Exception:
                self.send(503, {"error": "UNAVAILABLE_RETRY_IDENTICAL"})
        do_GET = do_POST = handle_request
    return Handler
