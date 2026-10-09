"""Separately gated future S4 lab entry point. Importing performs no cloud access."""
import hashlib
import os
from pathlib import Path
import re
import time

from tools.pixinsight.local_pilot.broker import require, decode, encode
from tools.scientific_transients.lab_gateway import LabState, RequestBudget, GatewayServer, gateway_for


def validate_config(config, source_revision, now=None):
    now = time.time() if now is None else now
    fields = {"activation", "sessionRef", "sourceRevision", "project", "primaryBucket",
              "backupBucket", "runtimeServiceAccount", "googleClientId", "ownerEmail",
              "portalOrigin", "workerId", "workerSha256", "deadline", "maximumEuro"}
    require(type(config) is dict and set(config) == fields, "LAB_CONFIG_FIELDS")
    require(config["activation"] == "FRESH_OWNER_AUTHORIZED", "LAB_FRESH_AUTHORIZATION_REQUIRED")
    require(re.fullmatch(r"[a-f0-9]{40}", source_revision or "") is not None
            and config["sourceRevision"] == source_revision and source_revision != "0" * 40,
            "LAB_SOURCE_PIN")
    require(re.fullmatch(r"[a-f0-9]{32}", config["sessionRef"] or "") is not None, "LAB_SESSION")
    prefix = "dsg-s4-lab-" + config["sessionRef"][:12]
    require(config["project"] == "digital-stargate-telemetry", "LAB_PROJECT")
    require(config["primaryBucket"] == prefix + "-primary"
            and config["backupBucket"] == prefix + "-backup", "LAB_NEW_BUCKET_NAMES")
    require(config["runtimeServiceAccount"] == prefix + "@" + config["project"] + ".iam.gserviceaccount.com",
            "LAB_NEW_SERVICE_IDENTITY")
    require(re.fullmatch(r"[a-f0-9]{32}", config["workerId"] or "") is not None
            and re.fullmatch(r"[a-f0-9]{64}", config["workerSha256"] or "") is not None, "LAB_WORKER_IDENTITY")
    require(type(config["deadline"]) in (int, float) and now < config["deadline"] <= now + 1800,
            "LAB_BOUNDED_DEADLINE")
    require(type(config["maximumEuro"]) in (int, float) and 0 < config["maximumEuro"] <= 10,
            "LAB_OWNER_COST_LIMIT")
    require(config["portalOrigin"] == "https://maininimassimo-bit.github.io", "LAB_APPROVED_ORIGIN")
    require(type(config["googleClientId"]) is str
            and config["googleClientId"] == "183451329061-8iedbjrn60u6iau42u1tlsonn6bi6hjd.apps.googleusercontent.com",
            "LAB_GOOGLE_AUDIENCE")
    require(type(config["ownerEmail"]) is str and re.fullmatch(r"[^\s@]+@[^\s@]+", config["ownerEmail"]),
            "LAB_OWNER_EMAIL")
    return dict(config)


def main():
    # Source pin is staged by the future reviewed build controller, never from old P6.
    revision = Path("/app/source-revision.txt").read_text(encoding="ascii").strip()
    config = validate_config(decode(os.environ["DSG_S4_LAB_CONFIG"].encode()), revision)
    require(os.environ.get("K_SERVICE") == "dsg-s4-lab-" + config["sessionRef"][:12],
            "LAB_NEW_CLOUD_RUN_SERVICE_REQUIRED")
    # Only now can optional cloud SDKs discover this new container's service ADC.
    from tools.scientific_transients.lab_cloud_transport import make_cloud_stores
    budget = RequestBudget(deadline=config["deadline"])
    stores, owner, close = make_cloud_stores(config, budget)
    try:
        # Create-only sentinel prevents cold starts/restarts from replaying this session.
        # This is a runtime guard, not a global Cloud Billing spending cap.
        primary = stores["A"][0]
        primary.put("control/s4-lab-start-once.json", encode({"sessionRef": config["sessionRef"],
                    "sourceRevision": revision}), 0)
        require(primary.get("control/transient-analysis-state-v1.json")[0] is None,
                "LAB_STATE_MUST_START_EMPTY")
        with LabState(stores, config["sessionRef"], config["workerId"], config["workerSha256"],
                      hashlib.sha256(os.urandom(32)).hexdigest(), owner, config["portalOrigin"],
                      config["deadline"], budget, "GCS_ADC", revision) as lab:
            with GatewayServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), gateway_for(lab)) as server:
                server.timeout = 0.5
                # No daemon lifetime beyond the finite final audit window.
                while time.time() < config["deadline"] + 600:
                    server.handle_request()
    finally:close()


if __name__ == "__main__":main()
