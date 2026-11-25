"""Validate ImageAnalysis return and close evidence before a future R4 release."""
import hashlib
import re

from tools.scientific_transients.f06_ui_closure import validate_close, validate_original_exit


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def hex_pin(value, length):
    return type(value) is str and re.fullmatch('[a-f0-9]{%d}' % length, value) is not None


def matches(raw, digest, maximum):
    return (type(raw) is bytes and 0 < len(raw) <= maximum and
            hashlib.sha256(raw).hexdigest() == digest)


def verify_terminal(*, operation, reservation, entry_sha256, plan_sha256, session,
                    retained, close_raw, close_sha256, binding, frame, console,
                    original_identity, original_exit_filetime, original_exit_code, now):
    """Require evidence correlated to independently held launch and exit observations."""
    require(hex_pin(operation, 32) and hex_pin(entry_sha256, 64) and
            hex_pin(plan_sha256, 64), 'IA_TERMINAL_LAUNCH')
    require(type(retained) is dict and set(retained) ==
            {'operationRef', 'reservation', 'entrySha256', 'returnSha256', 'measurementSha256'} and
            retained['operationRef'] == operation and retained['reservation'] == reservation and
            retained['entrySha256'] == entry_sha256 and hex_pin(retained['returnSha256'], 64) and
            hex_pin(retained['measurementSha256'], 64), 'IA_TERMINAL_RETURN_BINDING')
    require(type(binding) is dict and binding.get('reservation') == reservation,
            'IA_TERMINAL_RESERVATION')
    require(matches(frame, binding.get('frameSha256'), 16 * 1024 * 1024), 'IA_TERMINAL_FRAME')
    marker = 'DSG_BKL046_IMAGEANALYSIS_RETURNED_V1 ' + operation + ' ' + retained['returnSha256']
    context = dict(operationRef=operation, entrySha256=entry_sha256, planSha256=plan_sha256,
                   processSessionRef=session)
    closure = validate_close(close_raw, close_sha256, binding, context, original_identity, now,
                             expected_marker=marker)
    require(matches(console, closure['consoleEvidenceSha256'], 512 * 1024), 'IA_TERMINAL_CONSOLE')
    validate_original_exit(original_exit_filetime, original_exit_code, closure['actionUTC'], now)
    return dict(closureSha256=closure['sha256'], frameSha256=binding['frameSha256'],
                consoleSha256=closure['consoleEvidenceSha256'], returnSha256=retained['returnSha256'],
                measurementSha256=retained['measurementSha256'], operation=operation,
                reservation=reservation, nativeOriginVerifiedByValidator=False,
                scientificAcceptance=False)