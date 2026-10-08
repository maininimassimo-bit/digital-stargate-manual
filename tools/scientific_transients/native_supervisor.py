"""Trusted same-session native lifecycle. No daemon, claim, recovery replay or credentials on disk."""
import subprocess
import time
from pathlib import Path

from tools.pixinsight.local_pilot.broker import ProtocolError, require
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.local_registry import safe_path, fingerprint
from tools.scientific_transients.native_aperture import inspect_prepared_run, collect_run, ENGINE, CATALOG
from tools.scientific_transients.receipt_coordinator import observed_schema
from tools.scientific_transients.queue import TERMINAL, digest, fields

EXE = Path('C:/Program Files/PixInsight/bin/PixInsight.exe')


class NativeProcess:
    """Owns only the handle created here; persisted PIDs never grant ownership after restart."""
    def __init__(self, directory):
        require(safe_path(EXE).is_file(), 'SUPERVISOR_NATIVE_UNAVAILABLE')
        startup = None
        if hasattr(subprocess, 'STARTUPINFO'):
            startup = subprocess.STARTUPINFO()
            startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup.wShowWindow = subprocess.SW_HIDE
        self.process = subprocess.Popen([str(EXE), '-n', '--automation-mode', '--no-startup-scripts',
            '--no-startup-check-updates', '-r=' + str(directory / 'entry.js')], cwd=directory,
            startupinfo=startup, shell=False)
        self.pid = self.process.pid

    def close_after_retained_terminal(self):
        # Never called for missing/invalid terminal, timeout, lost transport or restart.
        if self.process.poll() is None:
            try: self.process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.process.terminate(); self.process.wait(timeout=30)
        return self.process.returncode


class NativeSupervisor:
    def __init__(self, registry, journal, outbox, directory, operation_ref, transport, lease_token,
                 *, spawn=NativeProcess, clock=time.monotonic, timeout=300, engine=ENGINE, catalog=CATALOG):
        require(outbox.journal is journal and not outbox.reopened and not journal.reopened_active,
                'SUPERVISOR_SAME_SESSION_REQUIRED')
        require(journal._events()[-1]['kind'] == 'PREPARED' and not outbox._records(), 'SUPERVISOR_FRESH_ATTEMPT')
        require(digest(lease_token) and type(timeout) in {int, float} and 1 <= timeout <= 900, 'SUPERVISOR_RUNTIME')
        self.registry, self.journal, self.outbox = registry, journal, outbox
        self.directory, self.operation = safe_path(directory), operation_ref
        self.transport, self.lease = transport, lease_token  # In-memory only, never serialized.
        self.spawn, self.clock, self.timeout = spawn, clock, timeout
        self.engine, self.catalog = engine, catalog
        self.process, self.started, self.stop_reason, self.outcome = None, None, None, None
        for other in [registry.artifacts, registry.registry]:
            require(outbox.directory != other and outbox.directory not in other.parents
                    and other not in outbox.directory.parents, 'SUPERVISOR_OUTBOX_OVERLAP')
        self.manifest = self._preflight()
        self.records = journal.directory / 'supervisor'; self.records.mkdir()
        write_new(self.records / 'identity.json', {'identity': outbox.identity, 'operationRef': operation_ref,
                  'runtime': self.manifest['runtime'], 'scienceValidation': 'NOT_VALIDATED'})

    def _preflight(self):
        manifest = inspect_prepared_run(self.directory, self.operation, engine=self.engine, catalog=self.catalog)
        require(not (self.directory / 'started.json').exists() and not (self.directory / 'terminal.json').exists(),
                'SUPERVISOR_REPLAY_REFUSED')
        anchor = self.journal.anchor['identity']
        registered = self.registry.verify(anchor['binding']['bindingRef'], anchor['manifestSha256'])
        require(registered['binding'] == anchor['binding'], 'SUPERVISOR_BINDING')
        for role, name in [('INPUT', 'input.xisf'), ('PARAMETERS', 'parameters.json'), ('ALGORITHM', 'native_aperture.jsh')]:
            relative = (self.directory / name).relative_to(self.registry.artifacts).as_posix()
            expected = fingerprint(self.directory / name)
            require(any(row['role'] == role and row['path'] == relative
                        and all(row[k] == expected[k] for k in ['sha256', 'bytes'])
                        for row in registered['files']), 'SUPERVISOR_REGISTERED_BYTES')
        return manifest

    def _remote(self):
        value = self.transport.request('/v1/transient-analysis/worker/jobs/' + self.outbox.identity['jobId'])
        observed_schema(value, self.outbox.identity)
        rows = self.outbox._records()
        if rows:
            require(rows[-1][3] is not None and value['lastReceipt'] == rows[-1][1]['receipt'],
                    'SUPERVISOR_REMOTE_ADVANCED')
        else: require(value['sequence'] == 0, 'SUPERVISOR_REMOTE_ADVANCED')
        return value

    def _send(self):
        self.outbox.enqueue()
        require(self.outbox.deliver(self.transport, self.lease) == 'ACKNOWLEDGED', 'SUPERVISOR_ACK_REQUIRED')

    def _outcome(self, state, reason, acknowledged=False):
        require(self.outcome is None, 'SUPERVISOR_CLOSED')
        self.outcome = {'state': state, 'reason': reason, 'operationRef': self.operation,
                        'processHandleHeld': self.process is not None, 'remoteReceiptAcknowledged': acknowledged,
                        'scienceValidation': 'NOT_VALIDATED'}
        write_new(self.records / 'outcome.json', self.outcome)
        self.lease = None
        return dict(self.outcome)

    def _recovery(self, reason):
        events = self.journal._events()
        if events[-1]['kind'] not in TERMINAL: self.journal.terminal('RECOVERY_REQUIRED')
        # Pending receipt stays intact. Only a new non-renewing recovery receipt after all prior ACKs.
        acknowledged = False
        try:
            rows = self.outbox._records()
            if events[-1]['kind'] not in TERMINAL and (not rows or rows[-1][3] is not None):
                self._send(); acknowledged = True
        except Exception: pass  # Preserve pending envelope; no implicit retry/replay.
        return self._outcome('RECOVERY_REQUIRED', reason, acknowledged)

    def _terminal(self, state):
        self.journal.terminal(state)
        try: self._send()
        except Exception: return self._outcome('RECOVERY_REQUIRED', 'TERMINAL_DELIVERY_UNCONFIRMED')
        return self._outcome(state, 'TERMINAL_ACKNOWLEDGED', True)

    def start(self):
        require(self.outcome is None and self.process is None and self.started is None, 'SUPERVISOR_REPLAY_REFUSED')
        try:
            remote = self._remote()
            if remote['state'] in TERMINAL: return self._recovery('REMOTE_TERMINAL_BEFORE_START')
            if remote['cancelRequested']: return self._terminal('CANCELLED')
            self.journal.running(); self._send()
            remote = self._remote()
            if remote['state'] in TERMINAL: return self._recovery('REMOTE_TERMINAL_BEFORE_START')
            if remote['cancelRequested']: return self._terminal('CANCELLED')
            self._preflight()
            sources = {k: (self.directory / n).relative_to(self.registry.artifacts).as_posix()
                       for k,n in [('PARAMETERS','parameters.json'),('RUNTIME','native_aperture.jsh')]}
            self.journal.begin_operation(self.registry, self.operation, sources); self._send()
            remote = self._remote()
            if remote['state'] in TERMINAL: return self._recovery('REMOTE_TERMINAL_BEFORE_START')
            if remote['cancelRequested']: return self._terminal('CANCELLED')
            self._preflight()
            write_new(self.records / 'launch-intent.json', {'operationRef': self.operation,
                      'launcher': fingerprint(self.directory / 'entry.js'), 'implicitReplay': False})
            self.started = self.clock()
            self.process = self.spawn(self.directory)
            write_new(self.records / 'process-created.json', {'pid': self.process.pid, 'ownership': 'CURRENT_HANDLE_ONLY'})
            return {'state': 'RUNNING', 'operationRef': self.operation}
        except Exception:
            # Launch or post-launch persistence failure is ambiguous, never assume no child was created.
            return self._recovery('START_OR_DELIVERY_UNCONFIRMED')

    def _cancel_marker(self, reason):
        if self.stop_reason is not None: return
        value = {'operationRef': self.operation, 'requested': True}
        path = self.directory / 'cancel.json'
        if path.exists(): require(read_json(path)[0] == value, 'SUPERVISOR_CANCEL_CONFLICT')
        else: write_new(path, value)
        write_new(self.records / 'stop-request.json', {'reason': reason, 'nativeStoppedAttested': False})
        self.stop_reason = reason

    def tick(self):
        """Caller polls explicitly. No scheduler/heartbeat; no resume after outcome/restart."""
        require(self.outcome is None and self.process is not None, 'SUPERVISOR_NOT_RUNNING')
        try:
            remote = self._remote()
            reason = 'REMOTE_TERMINAL' if remote['state'] in TERMINAL else 'OWNER_CANCEL' if remote['cancelRequested'] else None
        except Exception: reason = 'REMOTE_OBSERVATION_UNCONFIRMED'
        try:
            if reason: self._cancel_marker(reason)
        except Exception: return self._recovery('CANCEL_MARKER_UNCONFIRMED_PROCESS_NOT_TERMINATED')
        terminal_path = self.directory / 'terminal.json'
        if not terminal_path.exists():
            if self.clock() - self.started >= self.timeout:
                try: self._cancel_marker('TIMEOUT')
                except Exception: return self._recovery('CANCEL_MARKER_UNCONFIRMED_PROCESS_NOT_TERMINATED')
                return self._recovery('NATIVE_TERMINAL_MISSING_PROCESS_NOT_TERMINATED')
            return {'state': 'WAITING_NATIVE_SAFE_POINT', 'stopRequested': self.stop_reason is not None}
        try:
            terminal, _ = read_json(terminal_path)
            require(terminal.get('operationRef') == self.operation and terminal.get('protocol') == self.manifest['protocol']
                    and terminal.get('state') in {'COMPLETED','FAILED','CANCELLED'}, 'SUPERVISOR_NATIVE_TERMINAL')
            if terminal['state'] != 'COMPLETED':
                fields(terminal, {'protocol','operationRef','state','rows','retained','error','scienceValidation'})
                require(type(terminal['rows']) is list and type(terminal['retained']) is list
                        and all(type(p) is str and p in {'failed-checkpoint.xisf','failed-initial.js','failed-current.js','NOT_SAVED'}
                                for p in terminal['retained'])
                        and type(terminal['error']) is str and len(terminal['error']) <= 1024
                        and terminal['scienceValidation'] == 'NOT_VALIDATED', 'SUPERVISOR_NATIVE_TERMINAL')
            # Preserve receipt before closing only the current process handle.
            write_new(self.records / 'native-terminal.json', terminal)
            if terminal['state'] != 'COMPLETED' and 'NOT_SAVED' in terminal['retained']:
                return self._recovery('NATIVE_CHECKPOINT_NOT_SAVED_PROCESS_NOT_TERMINATED')
            if terminal['state'] == 'COMPLETED':
                collected = collect_run(self.directory, self.operation, engine=self.engine, catalog=self.catalog)
                sources = {k:p.relative_to(self.registry.artifacts).as_posix() for k,p in collected['sources'].items()}
                self.journal.checkpoint(self.registry, self.operation, sources)
            exit_code = self.process.close_after_retained_terminal()
            write_new(self.records / 'owned-process-closed.json', {'pid': self.process.pid, 'exitCode': exit_code})
            if self.stop_reason and self.stop_reason != 'OWNER_CANCEL': return self._recovery('NATIVE_RETAINED_REMOTE_UNCERTAIN')
            if self.stop_reason == 'OWNER_CANCEL': return self._terminal('CANCELLED')
            if terminal['state'] != 'COMPLETED': return self._terminal(terminal['state'])
            self._send()
            self.journal.complete(collected['qualityCounts']); self._send()
            return self._outcome('COMPLETED', 'TECHNICAL_REPORT_ACKNOWLEDGED_NOT_SCIENCE_ACCEPTANCE', True)
        except Exception: return self._recovery('NATIVE_COLLECTION_OR_DELIVERY_UNCONFIRMED')
