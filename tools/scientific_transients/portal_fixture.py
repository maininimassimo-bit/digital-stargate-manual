"""Synthetic queue views for the browser contract; no credentials or real jobs."""
import datetime as dt
from tools.scientific_registry.ingestion_storage import MemoryStore
from tools.scientific_transients.queue import TransientQueue, LEASE_SECONDS


def cases():
    result = []
    review_response = None
    for stage in ['QUEUED', 'QUEUED_CANCELLED', 'RESERVED', 'RUNNING', 'COMPLETED',
                  'FAILED', 'CANCELLED', 'RECOVERY_REQUIRED']:
        now = dt.datetime(2026, 10, 8, tzinfo=dt.timezone.utc)
        queue = TransientQueue(MemoryStore(), 'a' * 32, lambda: now)
        binding = dict(bindingRef='1' * 32, inputRef='2' * 32, referenceRef='3' * 32,
                       algorithmRef='4' * 32, contractRef='5' * 32)
        queue.register(binding)
        job = queue.create(dict(requestId='6' * 32, bindingRef=binding['bindingRef']))
        if stage == 'QUEUED_CANCELLED':
            queue.cancel(job['jobId'])
        elif stage != 'QUEUED':
            attempt = queue.claim(dict(workerId='a' * 32, rootId='b' * 32))['job']
            if stage not in {'RESERVED', 'RECOVERY_REQUIRED'}:
                envelope = dict(attemptId=attempt['attemptId'], leaseToken=attempt['leaseToken'],
                                sequence=1, stage='RUNNING', result=None)
                queue.report(job['jobId'], envelope)
                if stage != 'RUNNING':
                    envelope.update(sequence=2, stage=stage)
                    if stage == 'COMPLETED':
                        envelope['result'] = dict(reportSha256='7' * 64, bindingRef=binding['bindingRef'],
                            qualityCounts=dict(measured=0, excluded=0, incomplete=2))
                    if stage == 'CANCELLED':
                        queue.cancel(job['jobId'])
                    queue.report(job['jobId'], envelope)
                    if stage == 'COMPLETED':
                        review_response = queue.review(job['jobId'], dict(decisionId='8' * 32, reportSha256='7' * 64,
                                                                         decision='FOLLOW_UP'))
            if stage == 'RECOVERY_REQUIRED':
                now += dt.timedelta(seconds=LEASE_SECONDS)
        view = queue.status()
        # Nondeterministic attempt identity is not a credential; normalize for the golden fixture.
        if 'attemptId' in view['jobs'][0]:
            view['jobs'][0]['attemptId'] = '9' * 32
        result.append(dict(stage=stage, response=view))
    return {'kind': 'SYNTHETIC_QUEUE_OWNER_VIEWS_NOT_CLOUD_OAT', 'cases': result,
            'reviewResponse': review_response}


if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    path = Path(__file__).with_name('portal-queue-fixture.json')
    raw = json.dumps(cases(), indent=2) + '\n'
    if args.check:
        if path.read_text(encoding='utf-8') != raw:
            raise SystemExit('PORTAL_QUEUE_FIXTURE_DRIFT')
    else:
        with path.open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(raw)
