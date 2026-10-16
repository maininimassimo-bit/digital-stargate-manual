"""Explicit same-parent command driver. No automatic prepare, start or recovery.

The trusted operator must obtain fresh scoped human consent before PREPARE.
Neither stdin nor an authorization JSON authenticates that consent. Only the
reviewed isolated bootstrap may supply the live session in operational use.
"""
import re
import sys

from tools.pixinsight.local_pilot.broker import ProtocolError, encode, require
from tools.scientific_transients.native_launch_control import _json
from tools.scientific_transients.native_linear_preparation import LinearAttemptPreparation

PROTOCOL = 'DSG_NATIVE_LINEAR_DRIVER_V1'
MAX_LINE = 4096
COMMANDS = {'PREPARE', 'START', 'TICK', 'CANCEL', 'OBSERVE', 'STATUS', 'RELEASE_FILES', 'EXIT'}


def command(raw):
    require(type(raw) is bytes and 0 < len(raw) <= MAX_LINE and raw.endswith(b'\n'),
            'LINEAR_DRIVER_FRAME')
    value = _json(raw)
    require(type(value) is dict and value.get('protocol') == PROTOCOL
            and type(value.get('command')) is str and value['command'] in COMMANDS,
            'LINEAR_DRIVER_COMMAND')
    fields = {'protocol', 'command'}
    if value['command'] == 'PREPARE':
        fields |= {'planPath', 'planSha256', 'approvalPath', 'approvalSha256'}
    require(set(value) == fields, 'LINEAR_DRIVER_FIELDS')
    if value['command'] == 'PREPARE':
        for key in ['planPath', 'approvalPath']:
            require(type(value[key]) is str and 1 <= len(value[key]) <= 512
                    and value[key].isascii() and all(32 <= ord(c) < 127 for c in value[key]),
                    'LINEAR_DRIVER_PATH')
        for key in ['planSha256', 'approvalSha256']:
            require(type(value[key]) is str and re.fullmatch('[a-f0-9]{64}', value[key]),
                    'LINEAR_DRIVER_SHA')
    return value


def _code(exc):
    value = str(exc) if isinstance(exc, ProtocolError) else 'LINEAR_DRIVER_FAILURE'
    return value if re.fullmatch('[A-Z0-9_]{1,96}', value) else 'LINEAR_DRIVER_FAILURE'


class LinearNativeDriver:
    """Keep original live objects, including failed preparation and held process.

    No persisted state can rebuild this context. Every TICK is explicit; it may
    publish/close only via the supervisor's independently verified lifecycle.
    OBSERVE never calls TICK and never closes a process.
    """
    def __init__(self, session):
        self._session = session
        self._preparation = None; self._supervisor = None
        self._prepare_attempted = False; self._failed = False; self._exited = False
        self._released = False; self._last_error = None
        session.assert_intact()
        require(not getattr(session, '_linear_driver_attached', False), 'LINEAR_DRIVER_RECONSTRUCTION')
        session._linear_driver_attached = True

    def _uncertain(self, exc):
        self._failed = True
        if self._last_error is None: self._last_error = _code(exc)
        # Preparations may fail after storing an original supervisor. Keep it.
        if self._supervisor is None and self._preparation is not None:
            self._supervisor = self._preparation._supervisor
        if self._supervisor is not None:
            self._supervisor._uncertain(exc)

    def _release_allowed(self):
        sup = self._supervisor
        if sup is None:
            # Preparation has no spawn operation, including its failure paths.
            return True
        if not sup._start_attempted and sup._process is None and sup._held is None:
            return True
        if sup._held is None: return False  # Spawn/capture ambiguity never means stopped.
        observed = sup._observe()
        if observed is not None and observed['identityTrusted'] is not True:
            self._uncertain(ProtocolError('LINEAR_DRIVER_IDENTITY_UNCERTAIN'))
            return False
        return observed is not None and observed['identityTrusted'] is True \
            and observed['processObservation'] == 'HELD_EXITED'

    def _release_files(self):
        require(self._release_allowed(), 'LINEAR_DRIVER_EXIT_NOT_VERIFIED')
        groups = []
        if self._preparation is not None and self._preparation._locks is not None:
            groups.append(self._preparation._locks)
        if self._supervisor is not None:
            groups.extend(self._supervisor._locks)
        seen = set()
        for group in groups:
            if id(group) not in seen:
                seen.add(id(group)); group.release()
        self._released = True

    def dispatch(self, raw):
        value = command(raw)  # Invalid frames cannot partially execute a command.
        name = value['command']
        require(not self._exited, 'LINEAR_DRIVER_ALREADY_EXITED')
        if name == 'STATUS': return self.diagnostic()
        if name == 'PREPARE':
            require(not self._prepare_attempted and not self._failed and not self._released,
                    'LINEAR_DRIVER_PREPARE_REPLAY')
        elif name in {'START', 'TICK', 'CANCEL'}:
            require(self._supervisor is not None and not self._failed and not self._released,
                    'LINEAR_DRIVER_NOT_ACTIONABLE')
            if name == 'START':
                require(not self._supervisor._start_attempted
                        and self._supervisor.diagnostic()['state'] == 'PREPARED_LIVE',
                        'LINEAR_DRIVER_START_REPLAY')
        try:
            # Source uncertainty allows observation and safe release, never computation.
            if name not in {'OBSERVE', 'RELEASE_FILES', 'EXIT'}:
                self._session.assert_intact()
            if name == 'PREPARE':
                self._prepare_attempted = True
                self._preparation = LinearAttemptPreparation(self._session, value['planPath'], value['planSha256'])
                self._supervisor = self._preparation.prepare(value['approvalPath'], value['approvalSha256'])
            elif name == 'START': self._supervisor.start()
            elif name == 'TICK': self._supervisor.tick()
            elif name == 'CANCEL': self._supervisor.tick(cancel=True)
            elif name == 'OBSERVE' and self._supervisor is not None:
                observed = self._supervisor._observe()
                require(observed is None or observed['identityTrusted'] is True,
                        'LINEAR_DRIVER_IDENTITY_UNCERTAIN')
            elif name in {'RELEASE_FILES', 'EXIT'}:
                # An ordinary request to exit a live parent is refused, not a
                # cancellation or permission to discard its held references.
                require(self._release_allowed(), 'LINEAR_DRIVER_EXIT_NOT_VERIFIED')
                self._release_files()
                if name == 'EXIT': self._exited = True
            return self.diagnostic()
        except BaseException as exc:
            if isinstance(exc, ProtocolError) and str(exc) == 'LINEAR_DRIVER_EXIT_NOT_VERIFIED':
                raise
            self._uncertain(exc)
            raise

    def input_lost(self, exc):
        """EOF/transport loss is not a native-return or process-exit receipt."""
        self._uncertain(exc)
        # Do not release or close anything: even safe cleanup remains explicit.
        return self.diagnostic()

    def diagnostic(self):
        return {'protocol': PROTOCOL, 'prepareAttemptConsumed': self._prepare_attempted,
                'failed': self._failed, 'driverExitCommitted': self._exited,
                'filesReleased': self._released, 'lastError': self._last_error,
                'preparation': self._preparation.diagnostic() if self._preparation is not None else None,
                'supervisor': self._supervisor.diagnostic() if self._supervisor is not None else None,
                'newNativeStartAllowed': False, 'measurementAccepted': False,
                'scientificValidation': 'NOT_VALIDATED', 'qualifiedControls': 0}


def serve(driver, source, destination):
    """Bounded binary newline frames. No autonomous ticks, native waits or startup.

    EOF, oversized/incomplete frames and stream failures end the command transport
    with an uncertainty fence; the child is never assumed dead. An operator must
    reconcile a lost parent separately, without reconstructing process ownership.
    """
    try:
        while not driver._exited:
            raw = source.readline(MAX_LINE + 1)
            require(type(raw) is bytes and raw and len(raw) <= MAX_LINE and raw.endswith(b'\n'),
                    'LINEAR_DRIVER_INPUT_LOST')
            try:
                status = driver.dispatch(raw)
                response = {'ok': True, 'status': status}
            except ProtocolError as exc:
                response = {'ok': False, 'error': _code(exc), 'status': driver.diagnostic()}
            encoded = encode(response) + b'\n'
            require(len(encoded) <= 16384, 'LINEAR_DRIVER_RESPONSE_SIZE')
            require(destination.write(encoded) == len(encoded), 'LINEAR_DRIVER_SHORT_WRITE')
            destination.flush()
    except BaseException as exc:
        driver.input_lost(exc)
        raise
    return driver.diagnostic()


def main(session):
    """Bootstrap entry only; no __main__, command-line grant or automatic work."""
    driver = LinearNativeDriver(session)
    # Retain the context on the original session even if the transport raises.
    session._linear_driver_context = driver
    return serve(driver, sys.stdin.buffer, sys.stdout.buffer)
