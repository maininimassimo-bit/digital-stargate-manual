"""P4 cloud candidate. No resources or credentials are created by this program."""
import os
from http.server import HTTPServer
from tools.pixinsight.local_pilot.broker import Broker, require
from tools.pixinsight.local_pilot.transport_http import handler_for, google_owner
from tools.scientific_registry.ingestion_storage import BackedUpStore, GCSStore
from tools.pixinsight.local_pilot.scientific_portal import ScientificPortal
from tools.pixinsight.local_pilot.broker import decode
import urllib.request


def public_bytes(url):
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *_):
            return None
    opener = urllib.request.build_opener(NoRedirect())
    with opener.open(url, timeout=30) as response:
        raw = response.read(16 * 1024 * 1024 + 1)
        require(response.status == 200 and response.url == url and len(raw) <= 16 * 1024 * 1024, "SOURCE_UNAVAILABLE")
        return raw


def main():
    require(os.environ.get("DSG_PIAI_ACTIVATION") == "OWNER_AUTHORIZED", "ACTIVATION_REQUIRED")
    names = ["DSG_PIAI_PRIMARY_BUCKET", "DSG_PIAI_BACKUP_BUCKET", "DSG_PIAI_WORKER_ID",
             "DSG_PIAI_WORKER_SHA256", "DSG_PIAI_GOOGLE_CLIENT_ID", "DSG_PIAI_OWNER_EMAIL", "DSG_PIAI_PORTAL_ORIGIN"]
    settings = {name: os.environ[name] for name in names}
    require(settings[names[0]] != settings[names[1]], "SEPARATE_BACKUP_REQUIRED")
    require(settings[names[6]].startswith("https://"), "PORTAL_HTTPS_REQUIRED")
    store = BackedUpStore(GCSStore(settings[names[0]]), GCSStore(settings[names[1]]))
    broker = Broker(store, settings[names[2]])
    scientific = ScientificPortal(broker,
        lambda: public_bytes(settings[names[6]] + "/digital-stargate-manual/data/scientific-session-catalog.json"),
        lambda: decode(public_bytes("https://dsg-scientific-photo-ingestion-183451329061.europe-west1.run.app/v1/gallery")))
    handler = handler_for(broker,
        lambda token: google_owner(token, settings[names[4]], settings[names[5]]), settings[names[6]], settings[names[3]], scientific)
    HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), handler).serve_forever()


if __name__ == "__main__":
    main()
