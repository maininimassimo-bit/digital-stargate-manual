"""Authenticated queue HTTP adapter; deployed only after activation approval."""
import hashlib
import re
import secrets
import socket
import time
from http.server import BaseHTTPRequestHandler

from tools.pixinsight.local_pilot.broker import ProtocolError, decode, encode, require, opaque
from tools.scientific_registry.ingestion_storage import Conflict
from tools.scientific_registry.photo_ingestion import IngestionError
from tools.pixinsight.workflow_archive.archive import ArchiveError
from tools.pixinsight.local_pilot.transport import RESEARCH_CHECKPOINT_LIMIT


class AuthError(ValueError):
    pass


def google_owner(token, client_id, owner_email, *, request=None):
    from google.auth.transport.requests import Request
    from google.oauth2 import id_token
    try:
        claims = id_token.verify_oauth2_token(token, Request() if request is None else request, client_id)
        if claims.get("email_verified") is not True or claims.get("email", "").lower() != owner_email.lower():
            raise AuthError()
    except Exception:
        raise AuthError() from None


def handler_for(broker, authenticate_owner, portal_origin, worker_digest, scientific=None,
                transient=None, transient_worker_digest=None, campaigns=None, *, campaign_queue=None):
    require(re.fullmatch(r"[a-f0-9]{64}", worker_digest) is not None, "WORKER_DIGEST_INVALID")
    if transient is not None or campaigns is not None:
        require(isinstance(transient_worker_digest, str) and
                re.fullmatch(r"[a-f0-9]{64}", transient_worker_digest) is not None and
                transient_worker_digest != worker_digest, "TRANSIENT_DISTINCT_CREDENTIAL_REQUIRED")
    if campaigns is not None:
        require(transient is not None and campaigns.worker_id == transient.worker_id,
                'CAMPAIGN_TRANSIENT_WORKER_BINDING')
    if campaign_queue is not None:
        from tools.scientific_transients.campaign_queue import CampaignQueue
        require(type(campaign_queue) is CampaignQueue and campaign_queue.campaigns is campaigns
                and campaign_queue.queue is transient, 'CAMPAIGN_QUEUE_HTTP_COMPOSITION')
        campaign_queue._assert_composition()
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

        def reject(self, code, value):
            # RFC 9112 §9.6: immediate close with unread POST bytes can reset TCP
            # before the client receives the rejection. Half-close output, then discard a
            # bounded amount without parsing, authenticating or dispatching it.
            self.close_connection = True
            self.send(code, value)
            self.wfile.flush()
            try:
                self.connection.shutdown(socket.SHUT_WR)
                deadline, remaining = time.monotonic() + 0.25, 65536
                while remaining > 0:
                    timeout = deadline - time.monotonic()
                    if timeout <= 0: break
                    self.connection.settimeout(timeout)
                    raw = self.rfile.read1(min(8192, remaining))
                    if not raw: break
                    remaining -= len(raw)
            except OSError:
                pass  # Rejection already sent; never retry or dispatch the request.

        def deny_access(self):
            return self.reject(403, {"error": "ACCESS_DENIED"})

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
                return self.reject(403, {"error": "ACCESS_DENIED"})
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", portal_origin)
            self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Vary", "Origin")
            self.end_headers()

        def dispatch(self):
            path = self.path
            campaign_base = '/v1/transient-analysis/campaigns'
            campaign_worker = '/v1/transient-analysis/worker/campaigns'
            if (path == campaign_base or path.startswith(campaign_base + '/') or
                    path == campaign_worker or path.startswith(campaign_worker + '/')):
                if transient is None:
                    return self.reject(404, {'error':'NOT_FOUND'})
                is_campaign_worker = path == campaign_worker or path.startswith(campaign_worker + '/')
                self.authenticate(is_campaign_worker, transient_worker_digest)
                if campaigns is None:
                    return self.reject(404, {'error':'NOT_FOUND'})
                protected = re.fullmatch(
                    (campaign_worker if is_campaign_worker else campaign_base) +
                    r'/([a-f0-9]{32})/(dispatch-intents(?:/([a-f0-9]{64})/(receipt|jobs/([0-2])/(project|unreserved-context|close-unreserved|reserve-once)))?|frame-closures)', path)
                if protected:
                    if campaign_queue is None:
                        return self.reject(404, {'error':'NOT_FOUND'})
                    plan_ref, action, intent_sha, tail, ordinal, job_action = protected.groups()
                    if not is_campaign_worker:
                        if action == 'dispatch-intents' and self.command == 'POST':
                            return self.send(200, campaign_queue.prepare_dispatch(plan_ref, self.body()))
                        if tail == 'receipt' and self.command == 'GET':
                            return self.send(200, campaign_queue.dispatch_receipt(plan_ref, intent_sha))
                        if job_action == 'project' and self.command == 'POST':
                            require(self.body() == {}, 'REQUEST_FIELDS')
                            return self.send(200, campaign_queue.project(plan_ref, intent_sha, int(ordinal)))
                        if job_action == 'unreserved-context' and self.command == 'GET':
                            return self.send(200, campaign_queue.unreserved_context(plan_ref, intent_sha, int(ordinal)))
                        if job_action == 'close-unreserved' and self.command == 'POST':
                            return self.send(200, campaign_queue.close_unreserved(plan_ref, intent_sha, int(ordinal), self.body()))
                    elif self.command == 'POST':
                        if action == 'frame-closures':
                            event = campaign_queue.close_frame(plan_ref, self.body())
                            return self.send(200, {
                                'protocol': 'DSG_CAMPAIGN_FRAME_CLOSURE_RECEIPT_V1',
                                'closureSha256': event['sha256'],
                                'admissionSha256': event['request']['admissionSha256'],
                                'status': event['request']['technicalState'],
                                'nativeStoppedAttested': False,
                                'scientificValidation': 'NOT_VALIDATED'})
                        if job_action == 'reserve-once':
                            value = self.body()
                            require(type(value) is dict and set(value) == {'protocol', 'decisionId', 'reservation'}
                                    and value['protocol'] == 'DSG_CAMPAIGN_RESERVATION_V1', 'REQUEST_FIELDS')
                            return self.send(200, campaign_queue.reserve_envelope(
                                plan_ref, intent_sha, int(ordinal), value['reservation'], value['decisionId']))
                    return self.reject(404, {'error':'NOT_FOUND'})
                if self.command == 'POST' and path == campaign_worker + '/inputs':
                    return self.send(200, campaigns.register_inputs(self.body()))
                if not is_campaign_worker and path == campaign_base:
                    if self.command == 'POST': return self.send(200, campaigns.create(self.body()))
                    if self.command == 'GET': return self.send(200, campaigns.view())
                match = re.fullmatch(campaign_base + r'/([a-f0-9]{32})/inputs/([a-f0-9]{32})/dispatch-context', path)
                if match and self.command == 'GET':
                    return self.send(200, campaigns.dispatch_context(*match.groups()))
                match = re.fullmatch(campaign_base + r'/inputs/([a-f0-9]{32})(/review)?', path)
                if match:
                    witness_ref, action = match.groups()
                    if self.command == 'GET' and action is None:
                        return self.send(200, campaigns.input_view(witness_ref))
                    if self.command == 'POST' and action == '/review':
                        return self.send(200, campaigns.review_input(witness_ref, self.body()))
                match = re.fullmatch(campaign_worker + r'/([a-f0-9]{32})/executions', path)
                if match and self.command == 'POST':
                    return self.send(200, campaigns.record_execution(match[1], self.body()))
                match = re.fullmatch(campaign_base + r'/([a-f0-9]{32})(?:/(freeze|review-outcome|finalize|revoke|review-receipt))?', path)
                if match:
                    plan_ref, action = match.groups()
                    if self.command == 'GET' and action is None:
                        return self.send(200, campaigns.view(plan_ref))
                    if self.command == 'GET' and action == 'review-receipt':
                        return self.send(200, campaigns.review_receipt(plan_ref))
                    actions = {'freeze':campaigns.freeze, 'review-outcome':campaigns.review_outcome,
                               'finalize':campaigns.finalize, 'revoke':campaigns.revoke}
                    if self.command == 'POST' and action in actions:
                        return self.send(200, actions[action](plan_ref, self.body()))
                return self.reject(404, {'error':'NOT_FOUND'})
            if path == "/v1/transient-analysis" or path.startswith("/v1/transient-analysis/"):
                if transient is None:
                    return self.reject(404, {"error": "NOT_FOUND"})
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
                if self.command == "POST" and path == "/v1/transient-analysis/worker/reserve":
                    return self.send(200, transient.reserve_once(self.body()))
                match = re.fullmatch(r"/v1/transient-analysis/(worker/)?jobs/(TRN_[a-f0-9]{32})(?:/(cancel|report|review|close-recovery))?", path)
                if match:
                    worker_route, job_id, action = match.groups()
                    if worker_route and self.command == "GET" and action is None:
                        return self.send(200, transient.worker_receipt(job_id))
                    if worker_route and self.command == "POST" and action == "report":
                        return self.send(200, transient.report(job_id, self.body()))
                    if not worker_route and self.command == "GET" and action is None:
                        return self.send(200, transient.status(job_id))
                    if not worker_route and self.command == "POST" and action == "close-recovery":
                        return self.send(200, transient.close_recovery(job_id, self.body()))
                    if not worker_route and self.command == "POST" and action == "cancel":
                        require(self.body() == {}, "REQUEST_FIELDS")
                        return self.send(200, transient.cancel(job_id))
                    if not worker_route and self.command == "POST" and action == "review":
                        return self.send(200, transient.review(job_id, self.body()))
                return self.reject(404, {"error": "NOT_FOUND"})
            if self.command == "GET" and path == "/health":
                if scientific is not None and scientific.planner is not None:
                    return self.send(200, {'protocol': 'DSG_PIAI_QUEUE_V1', 'aiMode': 'OPENAI_API_PLANNING_AVAILABLE',
                                           'providerRequests': None})
                return self.send(200, {"protocol": "DSG_PIAI_QUEUE_V1", "aiMode": "SESSION_ASSISTED", "providerRequests": 0})
            worker = path.startswith("/v1/worker/")
            self.authenticate(worker)
            if scientific:
                research_match=re.fullmatch(r'/v1/(worker/)?science/intakes/([a-f0-9]{32})/research-(analysis|approve|state|reserve|start|checkpoint|decision|context|final|result|review|cancel|halt|resume)',path)
                if research_match:
                    worker_research,request_id,action=research_match.groups()
                    if self.command == 'GET' and action == 'state':
                        return self.send(200,scientific.research_state(request_id))
                    if self.command == 'GET' and not worker_research and action == 'resume':
                        return self.send(200,scientific.research_resume_offer(request_id))
                    if self.command == 'GET' and ((worker_research and action == 'context') or
                                                 (not worker_research and action == 'result')):
                        return self.send(200,getattr(scientific,'research_'+action)(request_id))
                    allowed={'analysis','reserve','start','checkpoint','decision','final','halt'} if worker_research else {'approve','cancel','review','resume'}
                    if self.command == 'POST' and action in allowed:
                        limit=6291456 if action in {'analysis','decision','final'} else RESEARCH_CHECKPOINT_LIMIT if action == 'checkpoint' else 65536
                        return self.send(200,getattr(scientific,'research_'+action)(request_id,self.body(limit)))
                    return self.reject(404,{'error':'NOT_FOUND'})
                adaptive_match = re.fullmatch(r'/v1/(worker/)?science/intakes/([a-f0-9]{32})/adaptive-(analysis|approve|state|reserve|start|checkpoint|decision|context|final|result|review|halt)', path)
                if adaptive_match:
                    worker_adaptive, request_id, action = adaptive_match.groups()
                    if worker_adaptive and action == 'analysis' and self.command == 'POST':
                        return self.send(200, scientific.generate_adaptive(request_id, self.body(6291456)))
                    if worker_adaptive and action in {'reserve','start','checkpoint','decision','final','halt'} and self.command == 'POST':
                        method = getattr(scientific,'adaptive_' + action)
                        return self.send(200,method(request_id,self.body(6291456 if action in {'decision','final'} else 262144)))
                    if worker_adaptive and action=='context' and self.command=='GET':
                        return self.send(200,scientific.adaptive_context(request_id))
                    if not worker_adaptive and action=='result' and self.command=='GET':
                        return self.send(200,scientific.adaptive_result(request_id))
                    if not worker_adaptive and action=='review' and self.command=='POST':
                        return self.send(200,scientific.adaptive_review(request_id,self.body()))
                    if not worker_adaptive and action == 'approve' and self.command == 'POST':
                        return self.send(200, scientific.approve_adaptive(request_id, self.body()))
                    if action == 'state' and self.command == 'GET':
                        return self.send(200, scientific.adaptive_state(request_id))
                    return self.reject(404, {'error':'NOT_FOUND'})
                ai_match = re.fullmatch(r'/v1/worker/science/intakes/([a-f0-9]{32})/openai-plan', path)
                if ai_match and self.command == 'POST':
                    return self.send(200, scientific.generate_openai(ai_match[1], self.body(16384)))
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
            return self.reject(404, {"error": "NOT_FOUND"})

        def handle_request(self):
            try:
                self.dispatch()
            except AuthError:
                self.deny_access()
            except (ProtocolError, IngestionError, ArchiveError) as error:
                self.reject(400, {"error": str(error)})
            except Conflict:
                self.reject(409, {"error": "CONFLICT_RETRY_IDENTICAL"})
            except Exception:
                self.reject(503, {"error": "UNAVAILABLE_RETRY_IDENTICAL"})
        do_GET = do_POST = handle_request
    return Handler
