"""HTTP adapter: public discovery, Google-authenticated owner-only mutations."""
import json
import os
from pathlib import Path
import re
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

from tools.pixinsight.workflow_archive.archive import ArchiveError, IMPORTER_VERSION
from tools.scientific_registry.ingestion_service import IngestionService, CHUNK_BYTES, json_bytes, historical_upload_enabled
from tools.scientific_registry.ingestion_storage import GCSStore, BackedUpStore, Conflict
from tools.scientific_registry.ingestion_security import ClamScanner
from tools.scientific_registry.photo_ingestion import IngestionError


class AuthenticationError(ValueError):
    pass


def current_catalog(portal_origin):
    # Fixed repository projection URL; never use a browser-supplied locator.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *_):
            return None
    url = portal_origin + "/digital-stargate-manual/data/scientific-session-catalog.json"
    request = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=15) as response:
            if response.status != 200 or response.url != url:
                raise IngestionError("CATALOG_UNAVAILABLE")
            raw = response.read(16 * 1024 * 1024 + 1)
            if len(raw) > 16 * 1024 * 1024:
                raise IngestionError("CATALOG_SIZE_INVALID")
            return raw
    except IngestionError:
        raise
    except Exception:
        raise IngestionError("CATALOG_UNAVAILABLE") from None


def owner_auth(token, client_id, owner_email):
    from google.auth.transport.requests import Request
    from google.oauth2 import id_token
    try:
        claims = id_token.verify_oauth2_token(token, Request(), client_id)
        if claims.get("email_verified") is not True or claims.get("email", "").lower() != owner_email.lower():
            raise AuthenticationError("OWNER_ACCOUNT_REQUIRED")
        return owner_email.lower()
    except AuthenticationError:
        raise
    except Exception:
        raise AuthenticationError("SIGN_IN_REQUIRED") from None


def handler_for(service, authenticate, origin, client_id):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass  # Access paths, bearer tokens and private input never enter app logs.

        def send(self, code, value, media="application/json"):
            raw = value if isinstance(value, bytes) else json_bytes(value)
            self.send_response(code)
            self.send_header("Content-Type", media)
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            if self.headers.get("Origin") == origin:
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Vary", "Origin")
            self.end_headers()
            self.wfile.write(raw)

        def actor(self):
            if self.headers.get("Origin") != origin:
                raise AuthenticationError("ORIGIN_NOT_ALLOWED")
            token = self.headers.get("Authorization", "")
            if not token.startswith("Bearer ") or len(token) > 8192:
                raise AuthenticationError("SIGN_IN_REQUIRED")
            return authenticate(token[7:])

        def body(self, binary=False):
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                raise IngestionError("BODY_SIZE_INVALID") from None
            limit = CHUNK_BYTES if binary else 2 * 1024 * 1024
            if not 0 < length <= limit or self.headers.get("Transfer-Encoding"):
                raise IngestionError("BODY_SIZE_INVALID")
            expected = "application/octet-stream" if binary else "application/json"
            if self.headers.get("Content-Type", "").split(";")[0] != expected:
                raise IngestionError("CONTENT_TYPE_INVALID")
            self.connection.settimeout(60)
            raw = self.rfile.read(length)
            if len(raw) != length:
                raise IngestionError("BODY_INCOMPLETE")
            if binary:
                return raw
            try:
                return json.loads(raw)
            except (ValueError, UnicodeError, RecursionError):
                raise IngestionError("JSON_INVALID") from None

        def do_OPTIONS(self):
            if self.headers.get("Origin") != origin:
                self.send(403, {"error": "ORIGIN_NOT_ALLOWED"})
                return
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
            self.send_header("Vary", "Origin")
            self.end_headers()

        def dispatch(self):
            path = self.path
            if self.command == "GET" and path == "/health":
                return self.send(200, {"status": "READY", "googleClientId": client_id,
                    "historicalUploadEnabled": historical_upload_enabled(),
                    "workflowImporterVersion": IMPORTER_VERSION,
                    "chunkBytes": CHUNK_BYTES, "originalLimit": 1024 * 1024 * 1024})
            if self.command == "GET" and path == "/v1/gallery":
                return self.send(200, service.collection())
            match = re.fullmatch(r"/v1/previews/([a-f0-9]{64})", path)
            if self.command == "GET" and match:
                return self.send(200, service.preview(match[1]), "image/jpeg")
            actor = self.actor()
            if self.command == "GET" and path == "/v1/archive":
                return self.send(200, {"items": service.archive(actor)})
            if self.command == "POST" and path == "/v1/uploads":
                item = service.create(self.body(), actor)
                return self.send(200, {"uploadId": item["id"], "state": item["state"]})
            match = re.fullmatch(r"/v1/uploads/([a-f0-9]{64})(?:/(review|commit|withdraw|preview))?", path)
            if match:
                upload_id, action = match.groups()
                if self.command == "GET" and action is None:
                    return self.send(200, service.status(upload_id, actor))
                if self.command == "GET" and action == "preview":
                    return self.send(200, service.preview(upload_id, actor), "image/jpeg")
                if self.command == "POST" and action == "review":
                    payload = self.body()
                    if payload != {} and not (isinstance(payload, dict) and set(payload) == {"recheck"} and payload["recheck"] is True):
                        raise IngestionError("REQUEST_FIELDS_INVALID")
                    return self.send(200, service.review_summary(upload_id, actor, recheck=payload.get("recheck") is True))
                if self.command == "POST" and action == "commit":
                    item = service.commit(upload_id, self.body(), actor)
                    return self.send(200, {"uploadId": item["id"], "state": item["state"], "publication": item["publication"]})
                if self.command == "POST" and action == "withdraw":
                    if self.body() != {}:
                        raise IngestionError("REQUEST_FIELDS_INVALID")
                    return self.send(200, {"state": service.withdraw(upload_id, actor)["state"]})
            match = re.fullmatch(r"/v1/uploads/([a-f0-9]{64})/(original|preview|workflow)/([0-9]{1,3})", path)
            if self.command == "PUT" and match:
                return self.send(200, service.chunk(match[1], match[2], int(match[3]), self.body(binary=True), actor))
            return self.send(404, {"error": "NOT_FOUND"})

        def run_request(self):
            try:
                self.dispatch()
            except AuthenticationError as exc:
                self.send(403, {"error": str(exc)})
            except Conflict:
                self.send(409, {"error": "CONFLICT_RETRY_OR_RESUME"})
            except (IngestionError, ArchiveError) as exc:
                self.send(400, {"error": str(exc)})
            except Exception:
                self.send(503, {"error": "SERVICE_UNAVAILABLE_RETRY"})

        do_GET = do_POST = do_PUT = run_request
    return Handler


def main():
    required = ("DSG_INGESTION_BUCKET", "DSG_INGESTION_BACKUP_BUCKET", "DSG_INGESTION_PUBLIC_BASE", "GOOGLE_CLIENT_ID", "DSG_OWNER_EMAIL", "DSG_PORTAL_ORIGIN")
    if any(not os.environ.get(name) for name in required):
        raise RuntimeError("INGESTION_CONFIGURATION_REQUIRED")
    catalog = Path("docs/data/scientific-session-catalog.json").read_bytes()
    store = BackedUpStore(GCSStore(os.environ["DSG_INGESTION_BUCKET"]), GCSStore(os.environ["DSG_INGESTION_BACKUP_BUCKET"]))
    service = IngestionService(store, catalog, ClamScanner(), os.environ["DSG_INGESTION_PUBLIC_BASE"],
                               catalog_loader=lambda: current_catalog(os.environ["DSG_PORTAL_ORIGIN"]))
    auth = lambda token: owner_auth(token, os.environ["GOOGLE_CLIENT_ID"], os.environ["DSG_OWNER_EMAIL"])
    # Single request per instance matches the reviewed memory/scan envelope.
    HTTPServer(("0.0.0.0", int(os.getenv("PORT", "8080"))),
               handler_for(service, auth, os.environ["DSG_PORTAL_ORIGIN"], os.environ["GOOGLE_CLIENT_ID"])).serve_forever()


if __name__ == "__main__":
    main()
