"""Synthetic caller receipts with actual local snapshots and MemoryStore queue."""
import copy
import unittest

from tools.pixinsight.local_pilot.broker import ProtocolError, decode, encode
from tools.scientific_registry.ingestion_storage import MemoryStore
from tools.scientific_transients.queue import TransientQueue
from tools.scientific_transients.attempt_journal import AttemptJournal
from tools.scientific_transients import test_local_registry as fixtures


class JournalTests(unittest.TestCase):
    def setUp(self):
        fixtures.RegistryTests.setUp(self)
        self.registered = self.local.register(encode(self.manifest))
        self.root = self.artifacts.parent / "journals"; self.root.mkdir()
        self.identity = {"jobId": "TRN_" + "6" * 32, "attemptId": "7" * 32,
                         "rootId": "8" * 32, "binding": self.binding,
                         "manifestSha256": self.registered["manifestSha256"]}
        (self.artifacts / "runtime.dat").write_bytes(b"synthetic caller runtime, not PixInsight")
        (self.artifacts / "history.dat").write_bytes(b"synthetic history receipt, not native")
        self.start_sources = {"PARAMETERS": "PARAMETERS.dat", "RUNTIME": "runtime.dat"}
        self.sources = {"CHECKPOINT": "INPUT.dat", "PARAMETERS": "PARAMETERS.dat", "HISTORY": "history.dat"}

    def prepare(self): return AttemptJournal.prepare(self.local, self.root, self.identity)

    def active(self):
        journal = self.prepare(); journal.running()
        journal.begin_operation(self.local, "a" * 32, self.start_sources)
        return journal

    def checkpoint(self):
        journal = self.active(); journal.checkpoint(self.local, "a" * 32, self.sources)
        return journal

    def test_snapshot_independent_of_later_source_mutation(self):
        journal = self.prepare(); (self.artifacts / "INPUT.dat").write_bytes(b"later source")
        journal.running()
        self.assertEqual(journal.queue_receipt(1)["stage"], "RUNNING")
        self.assertEqual(len(journal.anchor["snapshot"]), 6)

    def test_reopened_active_requires_explicit_recovery_without_relaunch(self):
        journal = self.active()
        reopened = AttemptJournal(journal.directory, self.identity)
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_EXPLICIT_RECOVERY_REQUIRED"):
            reopened.queue_receipt(2)
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_EXPLICIT_RECOVERY_REQUIRED"):
            reopened.checkpoint(self.local, "a" * 32, self.sources)
        reopened.terminal("RECOVERY_REQUIRED")
        self.assertEqual(reopened.queue_receipt(2)["stage"], "RECOVERY_REQUIRED")

    def test_partial_prepare_directory_blocks_retry_without_overwrite(self):
        directory = self.root / self.identity["attemptId"]; directory.mkdir()
        (directory / "partial").write_bytes(b"keep")
        with self.assertRaises(FileExistsError): self.prepare()
        self.assertEqual((directory / "partial").read_bytes(), b"keep")

    def test_expected_identity_and_roots_reject(self):
        journal = self.prepare(); changed = copy.deepcopy(self.identity); changed["rootId"] = "9" * 32
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_ANCHOR"): AttemptJournal(journal.directory, changed)
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_ROOT_OVERLAP"):
            AttemptJournal.prepare(self.local, self.artifacts, self.identity)

    def test_corrupted_snapshot_blocks_running(self):
        journal = self.prepare(); (journal.directory / journal.anchor["snapshot"][0]["path"]).write_bytes(b"changed")
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_SNAPSHOT_CHANGED"): journal.running()

    def test_damaged_snapshot_can_signal_recovery_without_claiming_success(self):
        journal = self.active()
        (journal.directory / journal.anchor["snapshot"][0]["path"]).write_bytes(b"corrupt")
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_SNAPSHOT_CHANGED"): journal.queue_receipt(1)
        journal.terminal("RECOVERY_REQUIRED")
        reopened = AttemptJournal(journal.directory, self.identity)
        result = reopened.queue_receipt(2)
        self.assertEqual(result["stage"], "RECOVERY_REQUIRED")
        self.assertIsNone(result["result"])

    def test_event_corruption_and_missing_intermediate_event_reject(self):
        journal = self.active(); event = journal.directory / "events/002.json"
        event.write_bytes(event.read_bytes() + b" ")
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_EVENT_CHAIN"): journal.queue_receipt(1)
        event.unlink()
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_EVENT_ORDER"): journal.queue_receipt(1)

    def test_parameter_change_rejected_and_orphan_copy_retained(self):
        journal = self.active(); (self.artifacts / "PARAMETERS.dat").write_bytes(b"different parameters")
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_PARAMETERS_CHANGED"):
            journal.checkpoint(self.local, "a" * 32, self.sources)
        self.assertTrue((journal.directory / "checkpoint-004/parameters.dat").exists())
        journal.terminal("RECOVERY_REQUIRED")

    def test_checkpoint_process_must_match_started_operation(self):
        journal = self.active()
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_PROCESS_BINDING"):
            journal.checkpoint(self.local, "b" * 32, self.sources)

    def test_process_reference_cannot_be_reused(self):
        journal = self.checkpoint()
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_PROCESS_REUSED"):
            journal.begin_operation(self.local, "a" * 32, self.start_sources)

    def test_report_requires_checkpoint_and_checks_counts(self):
        journal = self.active()
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_STAGE"):
            journal.complete({"measured": 0, "excluded": 0, "incomplete": 1})
        journal.checkpoint(self.local, "a" * 32, self.sources)
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_COUNTS"):
            journal.complete({"measured": True, "excluded": 0, "incomplete": 1})

    def test_sealed_report_and_checkpoint_mutation_prevent_queue_completion(self):
        journal = self.checkpoint(); journal.complete({"measured": 0, "excluded": 0, "incomplete": 1})
        self.assertEqual(journal.queue_receipt(2)["stage"], "COMPLETED")
        checkpoint = journal.directory / "checkpoint-004/checkpoint.dat"
        original = checkpoint.read_bytes(); checkpoint.write_bytes(b"changed")
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_CHECKPOINT_CHANGED"): journal.queue_receipt(2)
        checkpoint.write_bytes(original)
        report = journal.directory / "report.json"; report.write_bytes(report.read_bytes() + b" ")
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_REPORT_CHANGED"): journal.queue_receipt(2)

    def test_terminal_immutable_and_cancel_report_is_not_completion(self):
        journal = self.active(); journal.terminal("CANCELLED")
        self.assertEqual(journal.queue_receipt(1)["stage"], "CANCELLED")
        with self.assertRaisesRegex(ProtocolError, "JOURNAL_TERMINAL"): journal.terminal("FAILED")

    def test_secret_or_authority_fields_rejected(self):
        value = {**self.identity, "leaseToken": "0" * 64}
        with self.assertRaises(ProtocolError): AttemptJournal.prepare(self.local, self.root, value)
        self.assertFalse(list(self.root.iterdir()))

    def test_queue_envelope_correlates_without_persisting_lease_or_native_claim(self):
        queue = TransientQueue(MemoryStore(), "b" * 32)
        queue.register(self.binding); queue.create({"requestId": "6" * 32, "bindingRef": self.binding["bindingRef"]})
        claim = queue.claim({"workerId": "b" * 32, "rootId": "8" * 32})["job"]
        self.identity["attemptId"] = claim["attemptId"]
        journal = self.prepare(); journal.running()
        def send(sequence):
            return queue.report(claim["jobId"], {**journal.queue_receipt(sequence), "leaseToken": claim["leaseToken"]})
        self.assertEqual(send(1)["state"], "RUNNING")
        journal.begin_operation(self.local, "a" * 32, self.start_sources)
        journal.checkpoint(self.local, "a" * 32, self.sources)
        self.assertEqual(send(2)["state"], "RUNNING")
        journal.complete({"measured": 0, "excluded": 0, "incomplete": 1})
        result = send(3)
        self.assertEqual(result["state"], "COMPLETED")
        self.assertEqual(result["scientificValidation"], "NOT_VALIDATED")
        for p in journal.directory.rglob("*"):
            if p.is_file(): self.assertNotIn(claim["leaseToken"].encode(), p.read_bytes())
        report = decode((journal.directory / "report.json").read_bytes())
        self.assertEqual(report["nativeExecution"], "CALLER_REPORTED_NOT_ATTESTED")

    def test_queue_cancel_rejects_new_running_and_accepts_local_cancel_receipt(self):
        queue = TransientQueue(MemoryStore(), "b" * 32)
        queue.register(self.binding); queue.create({"requestId": "6" * 32, "bindingRef": self.binding["bindingRef"]})
        claim = queue.claim({"workerId": "b" * 32, "rootId": "8" * 32})["job"]
        self.identity["attemptId"] = claim["attemptId"]
        journal = self.prepare(); journal.running()
        queue.report(claim["jobId"], {**journal.queue_receipt(1), "leaseToken": claim["leaseToken"]})
        queue.cancel(claim["jobId"])
        with self.assertRaisesRegex(ProtocolError, "TRANSIENT_CANCEL_PENDING"):
            queue.report(claim["jobId"], {**journal.queue_receipt(2), "leaseToken": claim["leaseToken"]})
        journal.terminal("CANCELLED")
        result = queue.report(claim["jobId"], {**journal.queue_receipt(2), "leaseToken": claim["leaseToken"]})
        self.assertEqual(result["state"], "CANCELLED")
        self.assertFalse((journal.directory / "report.json").exists())


if __name__ == "__main__": unittest.main()
