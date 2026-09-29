"""Offline checks for the exact, owner-approved F4 reporter; never contacts GCP."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import urllib.request
import yaml

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / '.github/workflows/bkl-043-f4-github-outcome-reporter.yml'
body = PATH.read_bytes().replace(b'\r\n', b'\n')
assert hashlib.sha256(body).hexdigest() == 'e3c92f1efbea2135719b5bc5219e16696b5b41f97cc90e43c35eb15fd8f35557'
workflow = yaml.load(body, Loader=yaml.BaseLoader)
assert workflow['on'] == {'workflow_run': {'workflows': ['BKL-031 F9 MeteoHub Refresh', 'Analyze Observatory Session Automatically'], 'types': ['completed']}}
assert workflow['permissions'] == {'contents': 'read', 'id-token': 'write'}
job = workflow['jobs']['report']
assert 'github.event.workflow_run.head_branch == github.event.repository.default_branch' in job['if']
auth = next(s for s in job['steps'] if s.get('id') == 'auth')
assert auth['with']['create_credentials_file'] == 'false'
assert auth['with']['export_environment_variables'] == 'false'
assert not any('checkout' in s.get('uses', '') or 'download-artifact' in s.get('uses', '') for s in job['steps'])
code = job['steps'][-1]['run'].split("python - <<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
compiled = compile(code, 'reviewed-reporter', 'exec')
BASE = dict(REPOSITORY='maininimassimo-bit/digital-stargate-manual', WORKFLOW_NAME='BKL-031 F9 MeteoHub Refresh', RUN_ID='123', RUN_ATTEMPT='1', EVENT_NAME='schedule', STATUS='completed', CONCLUSION='success', HEAD_SHA='a'*40, CREATED_AT='2026-09-29T00:00:00Z', STARTED_AT='2026-09-29T00:00:01Z', COMPLETED_AT='2026-09-29T00:01:00Z', RECEIVER_URL='https://synthetic.invalid', ID_TOKEN='OFFLINE_SYNTHETIC_ONLY')
FIELDS = {'schema_version','event_id','repository','workflow_name','run_id','run_attempt','event','status','conclusion','head_sha','created_at_utc','started_at_utc','completed_at_utc'}

class Response:
    status = 200
    def __init__(self, value): self.value = value
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self): return json.dumps(self.value).encode()

def check(overrides=None, mode='created', expected=True):
    seen = []
    def fake(request, timeout):
        payload = json.loads(request.data)
        seen.append(payload)
        assert set(payload) == FIELDS
        assert request.full_url == 'https://synthetic.invalid/v1/github-workflow-outcome'
        assert timeout == 30
        if mode == 'network': raise TimeoutError('synthetic')
        return Response({'ack': 'DURABLE_DUPLICATE' if mode == 'duplicate' else 'WRONG' if mode == 'bad_ack' else 'DURABLE_CREATED', 'event_id': payload['event_id'] if mode != 'wrong_id' else 'wrong'})
    saved = {k: os.environ.get(k) for k in BASE}
    original = urllib.request.urlopen
    os.environ.update(BASE)
    os.environ.update(overrides or {})
    urllib.request.urlopen = fake
    try:
        try:
            with contextlib.redirect_stdout(io.StringIO()): exec(compiled, {})
            success = True
        except SystemExit:
            success = False
        assert success == expected, (mode, overrides)
        return seen
    finally:
        urllib.request.urlopen = original
        for k, v in saved.items():
            if v is None: os.environ.pop(k, None)
            else: os.environ[k] = v

for conclusion in ('success','failure','cancelled','skipped'):
    assert check({'CONCLUSION': conclusion})[0]['conclusion'] == conclusion
check(mode='duplicate')
for mode in ('network','bad_ack','wrong_id'): check(mode=mode, expected=False)
for overrides in ({'REPOSITORY':'unapproved/repo'}, {'WORKFLOW_NAME':'unapproved'}):
    assert not check(overrides, expected=False)
print('PASS: exact reviewed bytes, scope/permissions, ten offline transport and outcome scenarios.')
