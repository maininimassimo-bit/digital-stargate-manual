"""P4 cloud candidate. No resources or credentials are created by this program."""
import os
from http.server import HTTPServer
from tools.pixinsight.local_pilot.broker import Broker, require
from tools.pixinsight.local_pilot.transport_http import handler_for, google_owner
from tools.scientific_registry.ingestion_storage import BackedUpStore, GCSStore


def main():
    require(os.environ.get("DSG_PIAI_ACTIVATION") == "OWNER_AUTHORIZED", "ACTIVATION_REQUIRED")
    names = ["DSG_PIAI_PRIMARY_BUCKET", "DSG_PIAI_BACKUP_BUCKET", "DSG_PIAI_WORKER_ID",
             "DSG_PIAI_WORKER_SHA256", "DSG_PIAI_GOOGLE_CLIENT_ID", "DSG_PIAI_OWNER_EMAIL", "DSG_PIAI_PORTAL_ORIGIN"]
    settings = {name: os.environ[name] for name in names}
    require(settings[names[0]] != settings[names[1]], "SEPARATE_BACKUP_REQUIRED")
    require(settings[names[6]].startswith("https://"), "PORTAL_HTTPS_REQUIRED")
    store = BackedUpStore(GCSStore(settings[names[0]]), GCSStore(settings[names[1]]))
    broker = Broker(store, settings[names[2]])
    handler = handler_for(broker,
        lambda token: google_owner(token, settings[names[4]], settings[names[5]]), settings[names[6]], settings[names[3]])
    HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), handler).serve_forever()


if __name__ == "__main__":
    main()
