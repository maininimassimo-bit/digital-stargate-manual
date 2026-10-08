"""Explicit single-reservation driver. No claim, daemon, credential loading or restart replay."""
import math
import time

from tools.pixinsight.local_pilot.broker import require, opaque
from tools.scientific_transients.attempt_journal import AttemptJournal, identity, write_new
from tools.scientific_transients.receipt_coordinator import ReceiptOutbox, observed_schema
from tools.scientific_transients.native_supervisor import NativeSupervisor
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.queue import digest


class LocalDriver:
    @classmethod
    def prepare(cls, registry, journal_root, outbox_root, expected_identity, directory,
                operation_ref, transport, lease_token, *, supervisor_options=None,
                poll_interval=2, clock=time.monotonic):
        """Trusted caller supplies an independently bound current reservation and in-memory lease.

        Claim freshness cannot be inferred from RESERVED/sequence=0. This API does not claim jobs.
        Partial/pre-existing attempt directories are never reused, including PREPARED attempts.
        """
        identity(expected_identity)
        require(digest(lease_token) and opaque(operation_ref), 'DRIVER_LEASE_OR_OPERATION')
        require(type(poll_interval) in {int, float} and math.isfinite(poll_interval)
                and 1 <= poll_interval <= 30, 'DRIVER_POLL_INTERVAL')
        roots = [safe_path(p) for p in [journal_root, outbox_root]]
        for root in roots:
            require(root.is_dir(), 'DRIVER_ROOT')
        all_roots = roots + [registry.artifacts, registry.registry]
        for i, left in enumerate(all_roots):
            for right in all_roots[i + 1:]:
                require(left != right and left not in right.parents and right not in left.parents,
                        'DRIVER_ROOT_OVERLAP')
        require(all(not (root / expected_identity['attemptId']).exists() for root in roots),
                'DRIVER_RESTART_RECONCILIATION_REQUIRED')
        manifest = registry.verify(expected_identity['binding']['bindingRef'],
                                   expected_identity['manifestSha256'])
        require(manifest['binding'] == expected_identity['binding'], 'DRIVER_BINDING')
        remote = transport.request('/v1/transient-analysis/worker/jobs/' + expected_identity['jobId'])
        observed_schema(remote, expected_identity)
        require(remote['state'] == 'RESERVED' and remote['sequence'] == 0
                and remote['lastReceipt'] is None, 'DRIVER_RESERVATION_REQUIRED')
        directory = safe_path(directory)
        require(directory.is_dir() and registry.artifacts in directory.parents,
                'DRIVER_NATIVE_DIRECTORY')
        write_new(directory / 'driver-reservation.json', {'identity': expected_identity,
                  'operationRef': operation_ref, 'implicitReplay': False})
        journal = AttemptJournal.prepare(registry, roots[0], expected_identity)
        records = journal.directory / 'driver'; records.mkdir()
        write_new(records / 'reservation-observed.json', remote)
        try:
            outbox = ReceiptOutbox.prepare(roots[1], journal)
            supervisor = NativeSupervisor(registry, journal, outbox, directory, operation_ref,
                transport, lease_token, **(supervisor_options or {}))
            result = cls.__new__(cls)
            result.supervisor, result.journal, result.outbox = supervisor, journal, outbox
            result.clock, result.interval = clock, poll_interval
            result.started, result.finished, result.last_tick = False, False, None
            write_new(records / 'prepared.json', {'pollIntervalSeconds': poll_interval,
                      'implicitReplay': False, 'scienceValidation': 'NOT_VALIDATED'})
            return result
        except Exception:
            write_new(records / 'prepare-failed.json', {'state': 'RECONCILIATION_REQUIRED',
                      'nativeLaunchRequested': False, 'implicitReplay': False})
            raise

    def _now(self):
        value = self.clock()
        require(type(value) in {int, float} and math.isfinite(value), 'DRIVER_CLOCK')
        require(self.last_tick is None or value >= self.last_tick, 'DRIVER_CLOCK_REGRESSION')
        return value

    def start(self):
        require(not self.started and not self.finished, 'DRIVER_REPLAY_REFUSED')
        self.last_tick = self._now()
        self.started = True  # Set before launch; an exception never permits a second start.
        try:
            result = self.supervisor.start()
        except Exception:
            self.finished = True
            raise
        self.finished = result['state'] != 'RUNNING'
        return result

    def step(self):
        """One explicit poll, no wait/loop or automatic next-job acquisition."""
        require(self.started and not self.finished, 'DRIVER_NOT_RUNNING')
        try:
            now = self._now()
            if now - self.last_tick < self.interval:
                return {'state': 'POLL_NOT_DUE', 'scienceValidation': 'NOT_VALIDATED'}
            self.last_tick = now
            result = self.supervisor.tick()
        except Exception:
            self.finished = True  # Freeze uncertain exceptions; no implicit retry.
            raise
        self.finished = result['state'] != 'WAITING_NATIVE_SAFE_POINT'
        return result


def reconcile_retained(journal, outbox, transport):
    """Explicit post-restart GET and exact-receipt reconciliation; never POST or native replay.

    A historical ACK is not the current remote state. Recovery here does not clear a server
    RECOVERY_REQUIRED job, renew a lease, grant process ownership or accept science.
    """
    require(outbox.reopened and outbox.journal is journal, 'DRIVER_REOPENED_OUTBOX_REQUIRED')
    events = journal._events()
    journal._snapshot()
    journal._verify_artifacts(events)
    rows = outbox._records()
    remote = transport.request('/v1/transient-analysis/worker/jobs/' + outbox.identity['jobId'])
    observed_schema(remote, outbox.identity)
    disposition = outbox.reconcile(remote) if rows else 'NO_RETAINED_RECEIPT'
    current_match = bool(rows and remote['lastReceipt'] == rows[-1][1]['receipt']
                         and remote['state'] == rows[-1][1]['receipt']['stage'])
    return {'localState': events[-1]['kind'], 'remoteState': remote['state'],
            'cancelRequested': remote['cancelRequested'], 'receiptDisposition': disposition,
            'currentRemoteMatchesLastReceipt': current_match,
            'restartReplay': False, 'processOwnership': 'NOT_REACQUIRED',
            'serverRecoveryCleared': False, 'scienceValidation': 'NOT_VALIDATED'}
