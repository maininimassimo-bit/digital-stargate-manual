"""Synthetic journal receipts, MemoryStore and real loopback; not cloud/native OAT."""
import copy
import datetime as dt
import hashlib
import socket
import threading
import unittest
from http.server import HTTPServer

from tools.pixinsight.local_pilot.broker import Broker, ProtocolError, encode, decode
from tools.pixinsight.local_pilot.transport_http import handler_for, AuthError
from tools.scientific_registry.ingestion_storage import MemoryStore
from tools.scientific_transients.queue import TransientQueue
from tools.scientific_transients.attempt_journal import AttemptJournal
from tools.scientific_transients.receipt_coordinator import ReceiptOutbox, TransientTransport
from tools.scientific_transients import test_attempt_journal as fixtures

WORKER, TOKEN, ROOT = "a" * 32, "c" * 64, "8" * 32


class MemoryTransport:
    def __init__(self, queue): self.queue, self.posts, self.lose = queue, [], False
    def request(self, path): return self.queue.worker_receipt(path.rsplit("/", 1)[-1])
    def post(self, path, value):
        self.posts.append(copy.deepcopy(value))
        result = self.queue.report(path.split("/")[-2], value)
        if self.lose:
            self.lose = False
            raise ProtocolError("TRANSIENT_DELIVERY_UNCONFIRMED")
        return result


class CoordinatorTests(unittest.TestCase):
    def setUp(self):
        fixtures.JournalTests.setUp(self)
        self.queue = TransientQueue(MemoryStore(), WORKER)
        self.queue.register(self.binding)
        self.queue.create({"requestId": "6" * 32, "bindingRef": self.binding["bindingRef"]})
        self.claim = self.queue.claim({"workerId": WORKER, "rootId": ROOT})["job"]
        self.identity["attemptId"] = self.claim["attemptId"]
        self.journal = AttemptJournal.prepare(self.local, self.root, self.identity)
        self.outbox_root = self.root.parent / "outboxes"; self.outbox_root.mkdir()
        self.outbox = ReceiptOutbox.prepare(self.outbox_root, self.journal)
        self.transport = MemoryTransport(self.queue)
        self.lease = self.claim["leaseToken"]

    def running(self):
        self.journal.running(); self.outbox.enqueue()

    def deliver(self): return self.outbox.deliver(self.transport, self.lease)

    def restart(self):
        journal = AttemptJournal(self.journal.directory, self.identity)
        return ReceiptOutbox(self.outbox.directory, journal)

    def test_authenticated_exact_receipt_ack_and_no_secrets_on_disk(self):
        self.running(); self.assertEqual(self.deliver(), "ACKNOWLEDGED")
        self.assertEqual(self.deliver(), "ACKNOWLEDGED")
        self.assertEqual(len(self.transport.posts), 1)
        for p in self.outbox.directory.rglob("*.json"):
            raw = p.read_bytes()
            self.assertNotIn(self.lease.encode(), raw)
            self.assertNotIn(b"leaseToken", raw); self.assertNotIn(b"Bearer", raw)

    def test_requested_cancel_accepts_non_renewing_cancel_terminal(self):
        self.queue.cancel(self.claim['jobId']); self.journal.terminal('CANCELLED'); self.outbox.enqueue()
        self.assertEqual(self.deliver(), 'ACKNOWLEDGED')
        self.assertEqual(self.queue.status(self.claim['jobId'])['state'], 'CANCELLED')

    def test_requested_cancel_accepts_non_renewing_recovery_terminal(self):
        self.queue.cancel(self.claim['jobId']); self.journal.terminal('RECOVERY_REQUIRED'); self.outbox.enqueue()
        self.assertEqual(self.deliver(), 'ACKNOWLEDGED')
        self.assertEqual(self.queue.status(self.claim['jobId'])['state'], 'RECOVERY_REQUIRED')

    def test_lost_response_reconciles_without_second_post(self):
        self.running(); self.transport.lose = True
        with self.assertRaisesRegex(ProtocolError, "UNCONFIRMED"): self.deliver()
        pending = (self.outbox.directory / "messages/001/receipt.json").read_bytes()
        self.assertEqual(self.deliver(), "ACKNOWLEDGED")
        self.assertEqual(len(self.transport.posts), 1)
        self.assertEqual((self.outbox.directory / "messages/001/receipt.json").read_bytes(), pending)

    def test_restart_can_ack_accepted_receipt_but_never_deliver(self):
        self.running(); self.transport.lose = True
        with self.assertRaises(ProtocolError): self.deliver()
        reopened = self.restart()
        with self.assertRaisesRegex(ProtocolError, "RESTART_RECONCILIATION"): reopened.deliver(self.transport, self.lease)
        self.assertEqual(reopened.reconcile(self.queue.worker_receipt(self.claim["jobId"])), "ACKNOWLEDGED")
        with self.assertRaises(ProtocolError): reopened.enqueue()
        self.assertEqual(len(self.transport.posts), 1)

    def test_restart_unaccepted_receipt_is_preserved_for_recovery(self):
        self.running(); reopened = self.restart()
        self.assertEqual(reopened.reconcile(self.queue.worker_receipt(self.claim["jobId"])), "RECONCILIATION_REQUIRED")
        self.assertTrue((self.outbox.directory / "messages/001/recovery.json").is_file())
        self.assertEqual(len(self.transport.posts), 0)

    def test_cancel_before_delivery_retains_pending_without_post(self):
        self.running(); self.queue.cancel(self.claim["jobId"])
        self.assertEqual(self.deliver(), "RECONCILIATION_REQUIRED")
        self.assertEqual(self.transport.posts, [])
        with self.assertRaises(ProtocolError): self.outbox.enqueue()

    def test_expired_lease_does_not_send_or_ack_old_running(self):
        self.running()
        self.queue.clock = lambda: dt.datetime.fromisoformat(self.claim["leaseExpiresAt"])
        self.assertEqual(self.deliver(), "RECONCILIATION_REQUIRED")
        self.assertEqual(self.transport.posts, [])
        self.assertEqual(self.queue.worker_receipt(self.claim["jobId"])["state"], "RECOVERY_REQUIRED")

    def test_loss_before_commit_preserves_identical_retry_in_same_session(self):
        self.running()
        calls = []
        original = self.transport.post
        def interrupted(path, message):
            calls.append(copy.deepcopy(message))
            if len(calls) == 1: raise ProtocolError("TRANSIENT_DELIVERY_UNCONFIRMED")
            return original(path, message)
        self.transport.post = interrupted
        with self.assertRaises(ProtocolError): self.deliver()
        self.assertEqual(self.deliver(), "ACKNOWLEDGED")
        self.assertEqual(calls[0], calls[1])

    def test_completed_delivery_is_not_scientific_acceptance(self):
        self.running(); self.deliver()
        self.journal.begin_operation(self.local, "a" * 32, self.start_sources)
        self.journal.checkpoint(self.local, "a" * 32, self.sources)
        self.journal.complete({"measured": 1, "excluded": 0, "incomplete": 1})
        self.outbox.enqueue()
        self.assertEqual(self.deliver(), "ACKNOWLEDGED")
        remote = self.queue.status(self.claim["jobId"])
        self.assertEqual(remote["scientificValidation"], "NOT_VALIDATED")
        self.assertEqual(remote["publication"], "NONE")
        reopened = self.restart()
        self.assertEqual(reopened.reconcile(self.queue.worker_receipt(self.claim["jobId"])), "ACKNOWLEDGED")

    def test_wrong_identity_or_secret_echo_rejected_without_ack(self):
        self.running(); remote = self.queue.worker_receipt(self.claim["jobId"])
        for changed in [dict(remote, rootId="9" * 32), dict(remote, leaseToken=self.lease), dict(remote, attemptId="9" * 32)]:
            with self.assertRaises(ProtocolError): self.outbox.reconcile(changed)
        self.assertFalse((self.outbox.directory / "messages/001/ack.json").exists())

    def test_different_accepted_receipt_is_conflict_not_ack(self):
        self.running()
        self.queue.report(self.claim["jobId"], {"attemptId": self.claim["attemptId"], "sequence": 1, "stage": "FAILED", "result": None, "leaseToken": self.lease})
        self.assertEqual(self.deliver(), "RECONCILIATION_REQUIRED")
        self.assertEqual(self.transport.posts, [])

    def test_pending_blocks_new_sequence_and_terminal_closes(self):
        self.running()
        with self.assertRaisesRegex(ProtocolError, "PREVIOUS_PENDING"): self.outbox.enqueue()
        self.deliver()
        self.journal.terminal("FAILED"); self.outbox.enqueue()
        self.assertEqual(self.deliver(), "ACKNOWLEDGED")
        with self.assertRaises(ProtocolError): self.outbox.enqueue()

    def test_advanced_journal_never_sends_stale_receipt(self):
        self.running(); self.journal.terminal("FAILED")
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_ADVANCED"): self.deliver()
        self.assertEqual(self.transport.posts, [])

    def test_corrupted_pending_hash_or_chain_reject(self):
        self.running(); path = self.outbox.directory / "messages/001/receipt.json"
        value = decode(path.read_bytes()); value["journalHeadSha256"] = "f" * 64
        path.write_bytes(encode(value))
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_HEAD"): self.deliver()

    def test_partial_directory_blocks_recreation_without_overwrite(self):
        with self.assertRaises(FileExistsError): ReceiptOutbox.prepare(self.outbox_root, self.journal)
        self.assertTrue((self.outbox.directory / "identity.json").is_file())
        with self.assertRaisesRegex(ProtocolError, "ROOT_OVERLAP"):
            ReceiptOutbox.prepare(self.journal.directory, self.journal)

    def test_ack_tampering_and_extra_credentials_rejected(self):
        self.running(); self.deliver()
        path = self.outbox.directory / "messages/001/ack.json"
        value = decode(path.read_bytes()); value["remote"]["lastReceipt"]["stage"] = "FAILED"
        path.write_bytes(encode(value))
        with self.assertRaisesRegex(ProtocolError, "ACK_MISMATCH"): self.deliver()
        receipt = self.outbox.directory / "messages/001/receipt.json"
        value = decode(receipt.read_bytes()); value["leaseToken"] = self.lease
        receipt.write_bytes(encode(value))
        with self.assertRaisesRegex(ProtocolError, "TRANSIENT_FIELDS"): self.deliver()

    def test_source_completion_is_verified_before_delivery(self):
        self.running(); self.deliver()
        self.journal.begin_operation(self.local, "a" * 32, self.start_sources)
        self.journal.checkpoint(self.local, "a" * 32, self.sources)
        self.journal.complete({"measured": 1, "excluded": 0, "incomplete": 1})
        self.outbox.enqueue()
        checkpoint = next(self.journal.directory.glob("checkpoint-*/checkpoint.dat"))
        checkpoint.write_bytes(b"changed")
        with self.assertRaises(ProtocolError): self.deliver()
        self.assertEqual(len(self.transport.posts), 1)

    def test_loopback_dedicated_worker_route_and_full_delivery(self):
        def owner(token): raise AuthError()
        handler = handler_for(Broker(MemoryStore(), "d" * 32), owner, "https://portal.invalid",
            hashlib.sha256(("e" * 64).encode()).hexdigest(), transient=self.queue,
            transient_worker_digest=hashlib.sha256(TOKEN.encode()).hexdigest())
        server = HTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        self.addCleanup(server.server_close); self.addCleanup(server.shutdown)
        transport = TransientTransport("http://127.0.0.1:" + str(server.server_port), TOKEN, test_loopback=True)
        self.running()
        self.assertEqual(self.outbox.deliver(transport, self.lease), "ACKNOWLEDGED")
        remote = transport.request("/v1/transient-analysis/worker/jobs/" + self.claim["jobId"])
        self.assertNotIn("leaseToken", remote)
        wrong = TransientTransport(transport.origin, "e" * 64, test_loopback=True)
        with self.assertRaisesRegex(ProtocolError, "UNCONFIRMED"):
            wrong.request("/v1/transient-analysis/worker/jobs/" + self.claim["jobId"])
        for route in ["/v1/worker/claim", "/v1/transient-analysis/jobs", "/v1/transient-analysis/worker/jobs/" + self.claim["jobId"] + "?x=1"]:
            with self.assertRaises(ProtocolError): transport.request(route)

    def socket_loss_transport(self, *, after_commit):
        """Drop an actual local socket; no production endpoint or Google identity."""
        def owner(token): raise AuthError()
        base = handler_for(Broker(MemoryStore(), "d" * 32), owner, "https://portal.invalid",
            hashlib.sha256(("e" * 64).encode()).hexdigest(), transient=self.queue,
            transient_worker_digest=hashlib.sha256(TOKEN.encode()).hexdigest())
        observations = {"reportPosts": 0, "socketDrops": 0}
        class DropReportResponse(base):
            def dispatch(handler):
                if handler.command == "POST" and handler.path.endswith("/report"):
                    observations["reportPosts"] += 1
                    if not after_commit:
                        handler.authenticate(True, hashlib.sha256(TOKEN.encode()).hexdigest())
                        handler.body()  # Consume a valid request without committing it.
                        return handler.drop_socket()
                return super().dispatch()

            def send(handler, code, value, media="application/json"):
                if after_commit and handler.command == "POST" and handler.path.endswith("/report") and code == 200:
                    return handler.drop_socket()  # dispatch has already called queue.report.
                return super().send(code, value, media)

            def drop_socket(handler):
                observations["socketDrops"] += 1
                handler.close_connection = True
                handler.connection.shutdown(socket.SHUT_RDWR)
                handler.connection.close()

        server = HTTPServer(("127.0.0.1", 0), DropReportResponse)
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        self.addCleanup(thread.join)
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        transport = TransientTransport("http://127.0.0.1:" + str(server.server_port), TOKEN, test_loopback=True)
        return transport, observations

    def test_actual_socket_lost_ack_after_commit_restart_reads_without_repost(self):
        transport, observations = self.socket_loss_transport(after_commit=True)
        self.running()
        path = self.outbox.directory / "messages/001/receipt.json"
        pending = path.read_bytes()
        with self.assertRaisesRegex(ProtocolError, "UNCONFIRMED"):
            self.outbox.deliver(transport, self.lease)
        self.assertFalse((path.parent / "ack.json").exists())
        reopened = self.restart()
        remote = transport.request("/v1/transient-analysis/worker/jobs/" + self.claim["jobId"])
        self.assertEqual(reopened.reconcile(remote), "ACKNOWLEDGED")
        self.assertEqual(reopened.reconcile(remote), "ACKNOWLEDGED")
        self.assertEqual(remote["sequence"], 1)
        self.assertEqual(remote["lastReceipt"], decode(pending)["receipt"])
        self.assertEqual(path.read_bytes(), pending)
        self.assertEqual(observations, {"reportPosts": 1, "socketDrops": 1})
        with self.assertRaisesRegex(ProtocolError, "RESTART_RECONCILIATION"):
            reopened.deliver(transport, self.lease)

    def test_actual_socket_loss_before_commit_restart_freezes_without_repost(self):
        transport, observations = self.socket_loss_transport(after_commit=False)
        self.running()
        path = self.outbox.directory / "messages/001/receipt.json"
        pending = path.read_bytes()
        with self.assertRaisesRegex(ProtocolError, "UNCONFIRMED"):
            self.outbox.deliver(transport, self.lease)
        remote = transport.request("/v1/transient-analysis/worker/jobs/" + self.claim["jobId"])
        self.assertEqual(remote["sequence"], 0)
        self.assertIsNone(remote["lastReceipt"])
        reopened = self.restart()
        self.assertEqual(reopened.reconcile(remote), "RECONCILIATION_REQUIRED")
        self.assertTrue((path.parent / "recovery.json").exists())
        self.assertFalse((path.parent / "ack.json").exists())
        self.assertEqual(path.read_bytes(), pending)
        self.assertEqual(observations, {"reportPosts": 1, "socketDrops": 1})
        with self.assertRaises(ProtocolError): reopened.enqueue()


if __name__ == "__main__": unittest.main()
