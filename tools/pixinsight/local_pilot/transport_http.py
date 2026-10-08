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


def handler_for(broker, authenticate_owner, portal_origin, worker_digest, scientific=None,
                transient=None, transient_worker_digest=None):
    require(re.fullmatch(r"[a-f0-9]{64}", worker_digest) is not None, "WORKER_DIGEST_INVALID")
    if transient is not None:
        require(isinstance(transient_worker_digest, str) and
                re.fullmatch(r"[a-f0-9]{64}", transient_worker_digest) is not None and
                transient_worker_digest != worker_digest, "TRANSIENT_DISTINCT_CREDENTIAL_REQUIRED")
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

        def authenticate(self, worker=False, expected_digest=None):
            if len(self.headers.get_all("Authorization", [])) != 1:
                raise AuthError()
            header = self.headers.get("Authorization", "")
            if not header.startswith("Bearer ") or not 1 <= len(header[7:]) <= 8192:
                raise AuthError()
            token = header[7:]
            if worker:
                if self.headers.get("Origin") is not None or not re.fullmatch(r"[a-f0-9]{64}", token):
                    raise AuthError()
                if not secrets.compare_digest(hashlib.sha256(token.encode()).hexdigest(), expected_digest or worker_digest):
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
            if path == "/v1/transient-analysis" or path.startswith("/v1/transient-analysis/"):
                if transient is None:
                    return self.send(404, {"error": "NOT_FOUND"})
                is_worker = path.startswith("/v1/transient-analysis/worker/")
                self.authenticate(is_worker, transient_worker_digest)
                if self.command == "GET" and path == "/v1/transient-analysis/options":
                    return self.send(200, transient.options())
                if self.command == "GET" and path == "/v1/transient-analysis/jobs":
                    return self.send(200, transient.status())
                if self.command == "POST" and path == "/v1/transient-analysis/jobs":
                    return self.send(200, transient.create(self.body()))
                if self.command == "POST" and path == "/v1/transient-analysis/worker/register":
                    return self.send(200, transient.register(self.body()))
                if self.command == "POST" and path == "/v1/transient-analysis/worker/claim":
                    return self.send(200, transient.claim(self.body()))
                match = re.fullmatch(r"/v1/transient-analysis/(worker/)?jobs/(TRN_[a-f0-9]{32})(?:/(cancel|report|review))?", path)
                if match:
                    worker_route, job_id, action = match.groups()
                    if worker_route and self.command == "POST" and action == "report":
                        return self.send(200, transient.report(job_id, self.body()))
                    if not worker_route and self.command == "GET" and action is None:
                        return self.send(200, transient.status(job_id))
                    if not worker_route and self.command == "POST" and action == "cancel":
                        require(self.body() == {}, "REQUEST_FIELDS")
                        return self.send(200, transient.cancel(job_id))
                    if not worker_route and self.command == "POST" and action == "review":
                        return self.send(200, transient.review(job_id, self.body()))
                return self.send(404, {"error": "NOT_FOUND"})
            if self.command == "GET" and path == "/health":
                return self.send(200, {"protocol": "DSG_PIAI_QUEUE_V1", "aiMode": "SESSION_ASSISTED", "providerRequests": 0})
            worker = path.startswith("/v1/worker/")
            self.authenticate(worker)
            if scientific:
                if self.command == "GET" and path in {"/v1/science/intakes", "/v1/worker/science/intakes"}:
                    return self.send(200, {"intakes": scientific.intakes()})
                if self.command == "POST" and path == "/v1/science/intakes":
                    return self.send(200, scientific.create_intake(self.body(65536)))
                intake_match = re.fullmatch(r"/v1/science/intakes/([a-f0-9]{32})", path)
                if intake_match and self.command == "GET":
                    return self.send(200, scientific.intake(intake_match[1]))
                plan_match = re.fullmatch(r"/v1/(worker/)?science/intakes/([a-f0-9]{32})/(plan|approve|sources|approve-sources|preparation|approve-preparation|prepared|withdraw)", path)
                if plan_match and self.command == "POST":
                    worker_plan, request_id, action = plan_match.groups()
                    if not worker_plan and action == 'withdraw':
                        return self.send(200, scientific.withdraw_intake(request_id, self.body()))
                    if worker_plan and action == "plan":
                        return self.send(200, scientific.propose(request_id, self.body(65536)))
                    if not worker_plan and action == "approve":
                        return self.send(200, scientific.approve_plan(request_id, self.body()))
                    if worker_plan and action == "sources":
                        return self.send(200, scientific.propose_sources(request_id,self.body(65536)))
                    if not worker_plan and action == "approve-sources":
                        return self.send(200, scientific.approve_sources(request_id,self.body()))
                    if worker_plan and action == 'preparation':
                        return self.send(200,scientific.propose_preparation(request_id,self.body(65536)))
                    if not worker_plan and action == 'approve-preparation':
                        return self.send(200,scientific.approve_preparation(request_id,self.body()))
                    if worker_plan and action == 'prepared':
                        return self.send(200,scientific.record_preparation(request_id,self.body()))
                if self.command == "GET" and path == "/v1/science/options":
                    return self.send(200, scientific.options())
                if self.command == "GET" and path == "/v1/science/jobs":
                    return self.send(200, {"jobs": scientific.jobs()})
                if self.command == "POST" and path == "/v1/science/jobs":
                    return self.send(200, scientific.create(self.body()))
                if self.command == "POST" and path == "/v1/worker/science/register":
                    return self.send(200, scientific.register(self.body()))
                revisions = re.fullmatch(r"/v1/science/(PIAI_[a-f0-9]{32})/revisions", path)
                if revisions and self.command == 'GET':
                    return self.send(200, {'revisions':scientific.revisions(revisions[1])})
                revision = re.fullmatch(r"/v1/(worker/)?science/(PIAI_[a-f0-9]{32})/revisions/([a-f0-9]{32})/(result|preview|workflow|correlations|decision)", path)
                if revision:
                    worker_route, job_id, revision_id, action = revision.groups()
                    if worker_route and self.command == 'POST' and action == 'result':
                        result = scientific.deliver_revision(job_id,revision_id,self.body(9*1024*1024))
                        return self.send(200, {'jobId':job_id,'revisionId':revision_id,'reviewSha256':result['reviewSha256'],'publication':'NONE'})
                    if not worker_route and self.command == 'GET' and action == 'result':
                        return self.send(200,scientific.revision(job_id,revision_id))
                    if not worker_route and self.command == 'GET' and action in {'preview','workflow','correlations'}:
                        return self.send(200,scientific.revision_asset(job_id,revision_id,action),
                                         'image/jpeg' if action == 'preview' else 'application/json' if action == 'correlations' else 'text/plain; charset=utf-8')
                    if not worker_route and self.command == 'POST' and action == 'decision':
                        return self.send(200,scientific.decide_revision(job_id,revision_id,self.body()))
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
