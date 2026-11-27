"""Exercise the ImageAnalysis close gate with frozen evidence and distinct failures."""
from copy import deepcopy
import datetime as dt
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SHARED = Path('O:/dsg-shared-r4-permanent-v3/BKL051-F06-VM-sviluppo-v1/project')
sys.path[:0] = [str(ROOT), str(SHARED)]
from verifica_terminale import verify_terminal
from tools.scientific_transients.f06_ui_closure import filetime


def digest(raw):
    return sha256(raw).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('ascii')


def fixture():
    now = dt.datetime(2026, 11, 25, 12, tzinfo=dt.timezone.utc)
    began = now - dt.timedelta(seconds=8)
    action = now - dt.timedelta(seconds=5)
    observed = now - dt.timedelta(seconds=2)
    identity = dict(nativeProcessId='3412', processCreationFileTime=str(filetime(began)))
    operation, entry, plan, session = 'a'*32, 'b'*64, 'c'*64, 'd'*32
    reservation = '00000000-0000-4000-8000-000000000001'
    frame, console = b'synthetic frame', b'synthetic console'
    retained = dict(operationRef=operation, entrySha256=entry, reservation=reservation,
                    returnSha256='e'*64, measurementSha256='f'*64)
    binding = dict(identity, operationRef=operation, entrySha256=entry, planSha256=plan,
                   processSessionRef=session, hwnd='1948290', requestNonce='1'*32,
                   reservation=reservation, frameSha256=digest(frame))
    record = dict(protocol='DSG_F06_SUPERVISED_NORMAL_CLOSE_V1', binding=dict(binding),
                  capturedUTC=began.isoformat(), actionUTC=action.isoformat(), observedUTC=observed.isoformat(),
                  engineIdle=True, unsavedDocuments=0, openImages=0, activeDialogs=0, action='WINDOW_CLOSE',
                  windowGone=True, actionSucceeded=True,
                  consoleMarker='DSG_BKL046_IMAGEANALYSIS_RETURNED_V1 '+operation+' '+retained['returnSha256'],
                  consoleEvidenceSha256=digest(console))
    return record, dict(operation=operation, reservation=reservation, entry_sha256=entry, plan_sha256=plan,
                        session=session, retained=retained, binding=binding, frame=frame, console=console,
                        original_identity=identity, original_exit_filetime=filetime(observed),
                        original_exit_code=0, now=now)


def run():
    record, baseline = fixture()
    checks = [
        ('foreign reservation', 'binding', dict(baseline['binding'], reservation='9'*36), 'IA_TERMINAL_RESERVATION'),
        ('foreign operation', 'retained', dict(baseline['retained'], operationRef='4'*32), 'IA_TERMINAL_RETURN_BINDING'),
        ('replaced frame', 'frame', b'changed', 'IA_TERMINAL_FRAME'),
        ('replaced console', 'console', b'changed', 'IA_TERMINAL_CONSOLE'),
        ('foreign process', 'original_identity', dict(baseline['original_identity'], nativeProcessId='42'), 'F06_UI_CLOSE_ORIGINAL'),
        ('process exited before action', 'original_exit_filetime', 1, 'F06_CLOSE_EXIT_NOT_AFTER_ACTION'),
        ('nonzero process exit', 'original_exit_code', 1, 'F06_CLOSE_NONZERO_EXIT'),
        ('expired evidence', 'now', baseline['now'] + dt.timedelta(minutes=3), 'F06_UI_CLOSE_FRESHNESS'),
        ('wrong return marker', 'record.consoleMarker', 'foreign marker', 'F06_UI_CLOSE_NATIVE_MARKER'),
        ('modal window', 'record.activeDialogs', 1, 'F06_UI_CLOSE_ACTION_OR_STATE'),
    ]
    tests = []
    good = encode(record)
    passed = verify_terminal(close_raw=good, close_sha256=digest(good), **baseline)
    assert passed['returnSha256'] == baseline['retained']['returnSha256']
    def reject(name, body, arguments, expected, pin=None):
        try:
            verify_terminal(close_raw=body, close_sha256=pin or digest(body), **arguments)
        except ValueError as error:
            if str(error) != expected:
                raise
            tests.append(dict(case=name, rejection=expected))
        else:
            raise AssertionError('Unexpected acceptance: '+name)
    for name, field, altered, expected in checks:
        args = deepcopy(baseline)
        variant = deepcopy(record)
        if field.startswith('record.'):
            variant[field.split('.', 1)[1]] = altered
        else:
            args[field] = altered
        reject(name, encode(variant), args, expected)
    reject('different receipt bytes', good+b' ', baseline, 'F06_UI_CLOSE_DIGEST', digest(good))
    reject('duplicate receipt field', b'{"action":"WINDOW_CLOSE",'+good[1:], baseline, 'F06_UI_CLOSE_DUPLICATE_FIELD')
    result = dict(protocol='BKL046_IMAGEANALYSIS_TERMINAL_EVIDENCE_OFFLINE_V1', positive=passed,
                  negative=tests, nativeExecutions=0, productionRegistryModified=False,
                  supervisorIntegrated=False, scientificClosures=0)
    with Path(sys.argv[1]).open('xb') as out:
        out.write(json.dumps(result, indent=2, sort_keys=True).encode()+b'\n')


if __name__ == '__main__':
    run()