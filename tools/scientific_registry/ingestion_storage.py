"""Generation-guarded persistence for the independent photo ingestion service."""
import threading


class Conflict(RuntimeError):
    pass


class MemoryStore:
    """Synthetic tests only; never a production persistence fallback."""
    def __init__(self):
        self.items = {}
        self.lock = threading.Lock()
        self.serial = 0

    def get(self, key):
        with self.lock:
            return self.items.get(key, (None, 0))

    def put(self, key, raw, generation=0):
        with self.lock:
            if self.items.get(key, (None, 0))[1] != generation:
                raise Conflict("STORAGE_CONFLICT")
            self.serial += 1
            self.items[key] = (raw, self.serial)
            return self.serial

    def exists(self, key):
        return self.get(key)[0] is not None


class GCSStore:
    """One private bucket; the runtime identity has no access to other archives."""
    def __init__(self, bucket):
        from google.cloud import storage
        self.bucket = storage.Client().bucket(bucket)

    def get(self, key):
        from google.api_core.exceptions import NotFound, PreconditionFailed
        blob = self.bucket.blob(key)
        try:
            blob.reload(timeout=30)
            generation = int(blob.generation)
            return blob.download_as_bytes(if_generation_match=generation, timeout=120), generation
        except NotFound:
            return None, 0
        except PreconditionFailed:
            raise Conflict("STORAGE_CONFLICT") from None

    def put(self, key, raw, generation=0):
        from google.api_core.exceptions import PreconditionFailed
        blob = self.bucket.blob(key)
        blob.cache_control = "no-store"
        try:
            blob.upload_from_string(raw, content_type="application/octet-stream",
                                    if_generation_match=generation, timeout=120)
            return int(blob.generation)
        except PreconditionFailed:
            raise Conflict("STORAGE_CONFLICT") from None

    def exists(self, key):
        return self.bucket.blob(key).exists(timeout=30)


class BackedUpStore:
    """Persist an immutable recovery copy before every primary write.

    Backups are evidence/recovery copies, not the current publication head.
    A failed primary compare-and-swap can leave an uncommitted backup candidate.
    """
    def __init__(self, primary, backup):
        self.primary, self.backup = primary, backup

    def get(self, key):
        return self.primary.get(key)

    def exists(self, key):
        return self.primary.exists(key)

    def put(self, key, raw, generation=0):
        import hashlib
        backup_key = "recovery/" + hashlib.sha256(key.encode()).hexdigest() + "/" + hashlib.sha256(raw).hexdigest()
        immutable(self.backup, backup_key, raw)
        return self.primary.put(key, raw, generation)


def immutable(store, key, raw):
    try:
        return store.put(key, raw)
    except Conflict:
        previous, generation = store.get(key)
        if previous != raw:
            raise Conflict("IMMUTABLE_CONTENT_CONFLICT") from None
        return generation
