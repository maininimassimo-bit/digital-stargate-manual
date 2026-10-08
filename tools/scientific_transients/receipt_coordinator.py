"""Durable delivery receipts. No processing launch, credential file or automatic replay."""
import copy
import re
import urllib.request

from tools.pixinsight.local_pilot.broker import encode, require, opaque, ProtocolError
from tools.pixinsight.local_pilot.transport import Transport as OriginTransport
from tools.scientific_transients.attempt_journal import identity, read_json, write_new
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.queue import BINDING_FIELDS, TERMINAL, fields, digest

PROTOCOL = "DSG_TRANSIENT_OUTBOX_V1"


def receipt_schema(value):
    fields(value, {"attemptId", "sequence", "stage", "result"})
    require(opaque(value["attemptId"]) and type(value["sequence"]) is int
            and 1 <= value["sequence"] <= 128, "OUTBOX_RECEIPT")
    require(type(value["stage"]) is str and value["stage"] in TERMINAL | {"RUNNING"}, "OUTBOX_RECEIPT")
    if value["stage"] == "COMPLETED":
        fields(value["result"], {"reportSha256", "bindingRef", "qualityCounts"})
        require(digest(value["result"]["reportSha256"]) and opaque(value["result"]["bindingRef"]), "OUTBOX_RECEIPT")
        fields(value["result"]["qualityCounts"], {"measured", "excluded", "incomplete"})
        require(all(type(v) is int and 0 <= v <= 10000000 for v in value["result"]["qualityCounts"].values()), "OUTBOX_RECEIPT")
    else:
        require(value["result"] is None, "OUTBOX_RECEIPT")


def observed_schema(value, expected):
    fields(value, {"jobId", "attemptId", "rootId", "binding", "state", "cancelRequested", "sequence", "result", "lastReceipt"})
    require(all(value[k] == expected[k] for k in ["jobId", "attemptId", "rootId", "binding"]), "OUTBOX_REMOTE_IDENTITY")
    fields(value["binding"], BINDING_FIELDS)
    require(type(value["state"]) is str and value["state"] in TERMINAL | {"RESERVED", "RUNNING"}
            and type(value["cancelRequested"]) is bool and type(value["sequence"]) is int
            and 0 <= value["sequence"] <= 128, "OUTBOX_REMOTE_STATE")
    if value["lastReceipt"] is None:
        require(value["sequence"] == 0 and value["result"] is None, "OUTBOX_REMOTE_STATE")
    else:
        receipt_schema(value["lastReceipt"])
        require(value["lastReceipt"]["attemptId"] == expected["attemptId"]
                and value["lastReceipt"]["sequence"] == value["sequence"]
                and value["lastReceipt"]["result"] == value["result"], "OUTBOX_REMOTE_STATE")


class TransientTransport(OriginTransport):
    """One-shot, bounded dedicated routes; inherited TLS/origin/no-proxy/no-redirect policy."""
    def request(self, path, value=None):
        require(re.fullmatch(r"/v1/transient-analysis/worker/(?:claim|reserve|register|jobs/TRN_[a-f0-9]{32}(?:/report)?)", path), "TRANSIENT_ROUTE_INVALID")
        is_read = bool(re.fullmatch(r"/v1/transient-analysis/worker/jobs/TRN_[a-f0-9]{32}", path))
        require((value is None) == is_read, "TRANSIENT_METHOD_INVALID")
        raw = None if is_read else encode(value)
        require(raw is None or len(raw) <= 16384, "TRANSIENT_REQUEST_SIZE")
        request = urllib.request.Request(self.origin + path, raw, method="GET" if is_read else "POST",
            headers={"Authorization": "Bearer " + self.token, "Content-Type": "application/json"})
        try:
            with self.opener.open(request, timeout=30) as response:
                require(response.status == 200 and response.url == self.origin + path
                        and response.headers.get_content_type() == "application/json", "TRANSIENT_RESPONSE_INVALID")
                data = response.read(65537)
                require(0 < len(data) <= 65536, "TRANSIENT_RESPONSE_SIZE")
                from tools.pixinsight.local_pilot.broker import decode
                return decode(data)
        except ProtocolError:
            raise
        except Exception:
            raise ProtocolError("TRANSIENT_DELIVERY_UNCONFIRMED") from None


class ReceiptOutbox:
    @classmethod
    def prepare(cls, root, journal):
        root = safe_path(root)
        require(root.is_dir() and root != journal.directory and root not in journal.directory.parents
                and journal.directory not in root.parents, "OUTBOX_ROOT_OVERLAP")
        value = journal.anchor["identity"]
        directory = root / value["attemptId"]; directory.mkdir()
        (directory / "messages").mkdir()
        write_new(directory / "identity.json", {"protocol": PROTOCOL, "identity": value})
        result = cls(directory, journal)
        result.reopened = False
        return result

    def __init__(self, directory, journal):
        self.directory, self.journal = safe_path(directory), journal
        value, _ = read_json(self.directory / "identity.json")
        fields(value, {"protocol", "identity"}); identity(value["identity"])
        require(value["protocol"] == PROTOCOL and value["identity"] == journal.anchor["identity"]
                and self.directory.name == value["identity"]["attemptId"], "OUTBOX_IDENTITY")
        self.identity = value["identity"]
        self.reopened = True
        self._records()

    def _records(self):
        self.journal._events()
        journal_heads = {self.journal.anchor_sha}
        for event_path in safe_path(self.journal.directory / "events").iterdir():
            journal_heads.add(read_json(event_path)[1])
        paths = sorted(safe_path(self.directory / "messages").iterdir())
        require(len(paths) <= 128, "OUTBOX_CAPACITY")
        rows = []
        for number, path in enumerate(paths, 1):
            safe_path(path)
            require(path.name == str(number).zfill(3) and path.is_dir(), "OUTBOX_ORDER")
            allowed = {"receipt.json", "ack.json", "recovery.json"}
            require({p.name for p in path.iterdir()} <= allowed, "OUTBOX_FILES")
            message, sha = read_json(path / "receipt.json")
            fields(message, {"identity", "journalHeadSha256", "receipt"})
            require(message["identity"] == self.identity and digest(message["journalHeadSha256"]), "OUTBOX_IDENTITY")
            require(message["journalHeadSha256"] in journal_heads, "OUTBOX_JOURNAL_HEAD")
            receipt_schema(message["receipt"])
            require(message["receipt"]["attemptId"] == self.identity["attemptId"]
                    and message["receipt"]["sequence"] == number, "OUTBOX_ORDER")
            if message["receipt"]["result"] is not None:
                require(message["receipt"]["result"]["bindingRef"] == self.identity["binding"]["bindingRef"], "OUTBOX_RESULT_BINDING")
            ack = recovery = None
            if (path / "ack.json").exists():
                ack, _ = read_json(path / "ack.json")
                fields(ack, {"receiptSha256", "remote"}); observed_schema(ack["remote"], self.identity)
                require(ack["receiptSha256"] == sha and ack["remote"]["lastReceipt"] == message["receipt"]
                        and ack["remote"]["state"] == message["receipt"]["stage"], "OUTBOX_ACK_MISMATCH")
            if (path / "recovery.json").exists():
                recovery, _ = read_json(path / "recovery.json")
                fields(recovery, {"receiptSha256", "remote", "state"})
                observed_schema(recovery["remote"], self.identity)
                require(recovery["receiptSha256"] == sha and recovery["state"] == "RECONCILIATION_REQUIRED"
                        and ack is None, "OUTBOX_RECOVERY")
            require(number == len(paths) or (ack is not None and message["receipt"]["stage"] not in TERMINAL), "OUTBOX_PREVIOUS_PENDING")
            rows.append((path, message, sha, ack, recovery))
        return rows

    def enqueue(self):
        require(not self.reopened, "OUTBOX_RESTART_RECONCILIATION_REQUIRED")
        rows = self._records()
        require(not rows or (rows[-1][3] is not None and rows[-1][1]["receipt"]["stage"] not in TERMINAL), "OUTBOX_PREVIOUS_PENDING")
        require(len(rows) < 128, "OUTBOX_CAPACITY")
        receipt = self.journal.queue_receipt(len(rows) + 1)
        self.journal._events()
        path = self.directory / "messages" / str(len(rows) + 1).zfill(3); path.mkdir()
        write_new(path / "receipt.json", {"identity": self.identity, "journalHeadSha256": self.journal.head_sha, "receipt": receipt})
        return copy.deepcopy(receipt)

    def reconcile(self, remote):
        """Caller must obtain remote through authenticated transport; declarations are not attestation."""
        observed_schema(remote, self.identity)
        rows = self._records(); require(bool(rows), "OUTBOX_EMPTY")
        path, message, sha, ack, recovery = rows[-1]
        if ack is not None:
            return "ACKNOWLEDGED"
        if recovery is not None:
            return "RECONCILIATION_REQUIRED"
        if remote["lastReceipt"] == message["receipt"] and remote["state"] == message["receipt"]["stage"]:
            write_new(path / "ack.json", {"receiptSha256": sha, "remote": remote})
            return "ACKNOWLEDGED"
        # Restarts never renew a lease or deliver an old active-stage receipt.
        cancel_terminal = message["receipt"]["stage"] in {"CANCELLED", "RECOVERY_REQUIRED"}
        if self.reopened or remote["state"] in TERMINAL or (remote["cancelRequested"] and not cancel_terminal) or remote["sequence"] != message["receipt"]["sequence"] - 1:
            write_new(path / "recovery.json", {"receiptSha256": sha, "remote": remote, "state": "RECONCILIATION_REQUIRED"})
            return "RECONCILIATION_REQUIRED"
        return "NOT_ACKNOWLEDGED"

    def deliver(self, transport, lease_token):
        require(not self.reopened, "OUTBOX_RESTART_RECONCILIATION_REQUIRED")
        require(digest(lease_token), "OUTBOX_LEASE")
        rows = self._records(); require(bool(rows), "OUTBOX_EMPTY")
        require(rows[-1][4] is None, "OUTBOX_RECOVERY")
        if rows[-1][3] is not None: return "ACKNOWLEDGED"
        receipt = rows[-1][1]["receipt"]
        # Validate current local artifacts before success delivery; failures carry no result.
        require(self.journal.queue_receipt(receipt["sequence"]) == receipt, "OUTBOX_JOURNAL_ADVANCED")
        path = "/v1/transient-analysis/worker/jobs/" + self.identity["jobId"]
        remote = transport.request(path)
        state = self.reconcile(remote)
        if state != "NOT_ACKNOWLEDGED": return state
        transport.post(path + "/report", {**receipt, "leaseToken": lease_token})
        # A fresh authenticated read confirms receipt bytes, not just state/counts.
        return self.reconcile(transport.request(path))
