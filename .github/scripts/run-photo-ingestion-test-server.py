"""Loopback-only synthetic HTTP/browser fixture, never a deployment entry point."""
import base64
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
from http.server import HTTPServer

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PIL import Image
from tools.scientific_registry.ingestion_service import IngestionService
from tools.scientific_registry.ingestion_storage import MemoryStore

root = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("photo_http", root / "infrastructure/scientific-photo-ingestion/app.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class SyntheticScanner:
    def scan(self, _):
        return "PASS"

def authenticate(token):
    if token != "synthetic-owner-token":
        raise module.AuthenticationError("SIGN_IN_REQUIRED")
    return "synthetic-owner@example.com"

service = IngestionService(MemoryStore(), (root / "docs/data/scientific-session-catalog.json").read_bytes(),
                           SyntheticScanner(), "https://photo-test.run.app")
server = HTTPServer(("127.0.0.1", 0), module.handler_for(service, authenticate, os.environ["DSG_TEST_ORIGIN"], "synthetic.apps.googleusercontent.com"))
preview = io.BytesIO()
Image.new("RGB", (60, 40), "navy").save(preview, format="PNG")
print(json.dumps({"port": server.server_port, "preview": base64.b64encode(preview.getvalue()).decode()}), flush=True)
server.serve_forever()
