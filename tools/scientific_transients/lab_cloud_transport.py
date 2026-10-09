"""Optional SDK adapter for the isolated lab. Importing this module uses no ADC.

Every requests-adapter send is counted, including SDK retries and auth refresh.
No URL, header, token, email, response body or credential is retained by the meter.
"""
from urllib.parse import urlsplit

from tools.pixinsight.local_pilot.broker import require
from tools.pixinsight.local_pilot.transport_http import google_owner
from tools.scientific_registry.ingestion_storage import GCSStore


def endpoint_kind(url):
    parsed = urlsplit(url)
    require(not parsed.username and not parsed.password and not parsed.fragment, "LAB_PROVIDER_URL")
    if parsed.hostname in {"metadata.google.internal", "169.254.169.254"} and parsed.scheme == "http":
        require(parsed.port in (None, 80), "LAB_METADATA_PORT")
        return "ADC_METADATA"
    require(parsed.scheme == "https" and parsed.port in (None, 443), "LAB_PROVIDER_TLS")
    if parsed.hostname == "storage.googleapis.com":
        return "GCS_UPLOAD" if parsed.path.startswith("/upload/") else "GCS_READ"
    if parsed.hostname in {"www.googleapis.com", "oauth2.googleapis.com"}:
        require(parsed.path in {"/oauth2/v1/certs", "/oauth2/v3/certs", "/token"}, "LAB_AUTH_PATH")
        return "GOOGLE_AUTH"
    raise ValueError("LAB_PROVIDER_HOST_BLOCKED")


def counted_adapter(budget, base_adapter):
    """Base adapter injection exists solely for offline transport tests."""
    class Counted(base_adapter):
        def send(self, request, **kwargs):
            require(request.method in {"GET", "POST"}, "LAB_PROVIDER_METHOD_BLOCKED")
            kind = endpoint_kind(request.url)
            sequence = budget.before(kind, request.method)
            timeout = kwargs.get("timeout")
            if isinstance(timeout, tuple):
                timeout = tuple(min(float(value), 10) if value is not None else 10 for value in timeout)
            elif isinstance(timeout, (int, float)):
                timeout = min(timeout, 10)
            else:timeout = 10
            kwargs["timeout"] = timeout
            # requests/urllib3 transport retries are disabled by factory construction.
            # SDK/Google-auth retries above this adapter each invoke send and count.
            response = super().send(request, **kwargs)
            budget.after(sequence, response.status_code)
            return response
    return Counted


def make_cloud_stores(config, budget):
    """Called only by the separately guarded future lab image entry point."""
    import os
    require(not any(name in os.environ for name in (
        "GOOGLE_APPLICATION_CREDENTIALS", "CLOUDSDK_CONFIG", "GCE_METADATA_HOST",
        "GCE_METADATA_IP", "GCE_METADATA_ROOT", "GOOGLE_API_USE_MTLS_ENDPOINT",
        "STORAGE_EMULATOR_HOST", "GOOGLE_CLOUD_QUOTA_PROJECT", "GOOGLE_CLOUD_UNIVERSE_DOMAIN")),
        "LAB_CREDENTIAL_OR_ENDPOINT_OVERRIDE_BLOCKED")
    require(os.environ.get("DISABLE_GCS_PYTHON_CLIENT_OTEL_BUCKET_METADATA") == "true",
            "LAB_BACKGROUND_BUCKET_METADATA_MUST_BE_DISABLED")
    import google.auth
    from google.auth.transport.requests import AuthorizedSession, Request
    from google.cloud import storage
    import requests
    from requests.adapters import HTTPAdapter

    require(config["primaryBucket"] != config["backupBucket"], "LAB_BUCKETS_DISTINCT")
    adapter = counted_adapter(budget, HTTPAdapter)

    def plain_session():
        session = requests.Session()
        session.trust_env = False
        session.mount("http://", adapter(max_retries=0))
        session.mount("https://", adapter(max_retries=0))
        return session

    sessions = []
    def google_request():
        session = plain_session();sessions.append(session)
        return Request(session=session)

    def store(bucket_name):
        credentials, _ = google.auth.default(request=google_request(),
                    scopes=["https://www.googleapis.com/auth/devstorage.read_write"])
        # Cloud runtime ADC must be its new service identity, not user/external/key creds.
        from google.auth.compute_engine.credentials import Credentials
        require(isinstance(credentials, Credentials), "LAB_SERVICE_ADC_REQUIRED")
        credentials.refresh(google_request())
        require(credentials.service_account_email == config["runtimeServiceAccount"],
                "LAB_SERVICE_IDENTITY_MISMATCH")
        session = AuthorizedSession(credentials, auth_request=google_request())
        session.trust_env = False
        session.mount("http://", adapter(max_retries=0))
        session.mount("https://", adapter(max_retries=0))
        sessions.append(session)
        client = storage.Client(project=config["project"], credentials=credentials, _http=session)
        # Keep GCSStore get/put/412 behavior byte-for-byte unchanged, inject its bucket.
        result = object.__new__(GCSStore)
        result.bucket = client.bucket(bucket_name)
        return result

    try:
        stores = {executor: (store(config["primaryBucket"]), store(config["backupBucket"]))
                  for executor in ("A", "B")}
        owner_request = google_request()
    except BaseException:
        for session in sessions:session.close()
        raise

    import threading
    owner_lock = threading.Lock()
    def owner(token):
        # The requests session is shared only for certificate verification, serialized.
        with owner_lock:
            return google_owner(token, config["googleClientId"], config["ownerEmail"], request=owner_request)

    def close():
        for session in sessions:session.close()
    return stores, owner, close
