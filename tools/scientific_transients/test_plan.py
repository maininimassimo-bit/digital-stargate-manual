"""Private create-only test-plan versions and documented reviews. No launch/network.

Local hashes establish byte integrity, not actor identity, UTC attestation,
scientific truth or immutable storage. No confirmatory acceptance is implemented.
"""
import copy
import datetime as dt
import hashlib
import secrets
import base64
import binascii

from tools.pixinsight.local_pilot.broker import encode, opaque, require
from tools.scientific_transients.attempt_journal import read_json, write_new, copy_verified, AttemptJournal
from tools.scientific_transients.local_registry import safe_path, fingerprint
from tools.scientific_transients.queue import fields, digest, TERMINAL
from tools.scientific_transients.local_report import inspect as inspect_report

PROTOCOL = 'DSG_TEST_PLAN_VERSION_V1'
VIEW = 'BKL051_TEST_PLAN_REVIEW_V1'


def validate_draft(value):
    fields(value, {'schema', 'planRef', 'mode', 'falsePositiveMaximum', 'confidence',
                   'requiredControls', 'algorithmRef', 'cases'})
    require(value['schema'] == 'BKL051_TEST_PLAN_DRAFT_V1' and opaque(value['planRef'])
            and value['mode'] == 'PRELIMINARY_DRAFT'
            and value['falsePositiveMaximum'] == .05 and value['confidence'] == .95
            and type(value['requiredControls']) is int and value['requiredControls'] == 59
            and (value['algorithmRef'] is None or digest(value['algorithmRef'])), 'PLAN_DRAFT')
    require(type(value['cases']) is list and len(value['cases']) <= 500, 'PLAN_CASES')
    cases, images, hashes = set(), set(), set()
    for case in value['cases']:
        fields(case, {'caseRef', 'clusterRef', 'frames', 'qualification', 'truth', 'execution'})
        require(opaque(case['caseRef']) and case['caseRef'] not in cases
                and opaque(case['clusterRef']) and case['qualification'] == 'CANDIDATE'
                and case['truth'] == 'UNVERIFIED' and case['execution'] == 'NOT_RUN', 'PLAN_CASE')
        cases.add(case['caseRef'])
        require(type(case['frames']) is list and len(case['frames']) == 3, 'PLAN_TRIPLET')
        for frame in case['frames']:
            fields(frame, {'frameRef', 'sha256'})
            require(opaque(frame['frameRef']) and frame['frameRef'] not in images
                    and digest(frame['sha256']) and frame['sha256'] not in hashes, 'PLAN_IMAGE')
            images.add(frame['frameRef']); hashes.add(frame['sha256'])
    return copy.deepcopy(value)


def declaration(value):
    fields(value, {'actorRef', 'recordedUTC'})
    require(opaque(value['actorRef']) and type(value['recordedUTC']) is str
            and len(value['recordedUTC']) <= 40, 'PLAN_ACTOR')
    try:
        stamp = dt.datetime.fromisoformat(value['recordedUTC'])
    except ValueError:
        require(False, 'PLAN_UTC')
    require(stamp.utcoffset() == dt.timedelta(0), 'PLAN_UTC')


def evidence(directory, sources):
    """Snapshot evidence bytes; original paths never enter the minimised view."""
    require(type(sources) is dict and 1 <= len(sources) <= 12, 'PLAN_EVIDENCE')
    records = []
    for index, (role, source) in enumerate(sorted(sources.items())):
        require(type(role) is str and role in {'ALGORITHM', 'RULES', 'NULL_REFERENCE',
                'INDEPENDENCE', 'RATIONALE', 'SCIENTIFIC_OUTCOME', 'INPUT_DERIVATION'}, 'PLAN_EVIDENCE_ROLE')
        expected = fingerprint(source)
        require(0 < expected['bytes'] <= 16 * 1024 * 1024, 'PLAN_EVIDENCE_SIZE')
        name = 'evidence-' + str(index).zfill(2) + '.dat'
        copy_verified(source, directory / name, expected)
        records.append({'role': role, 'path': name, **expected})
    return records


class PlanVersion:
    @classmethod
    def create(cls, root, draft, actor, algorithm, rules, previous=None):
        """Freeze a preliminary version, never a scientifically accepted plan."""
        draft = validate_draft(draft); declaration(actor)
        root = safe_path(root); require(root.is_dir(), 'PLAN_ROOT')
        if previous is not None:
            old = previous.read()
            require(old['draft']['planRef'] == draft['planRef'] and previous.directory.parent == root,
                    'PLAN_PREVIOUS')
        ref = secrets.token_hex(16); directory = root / ref; directory.mkdir()
        try:
            rows = evidence(directory, {'ALGORITHM': algorithm, 'RULES': rules})
            algorithm_sha = next(r['sha256'] for r in rows if r['role'] == 'ALGORITHM')
            require(draft['algorithmRef'] in {None, algorithm_sha}, 'PLAN_ALGORITHM_CHANGED')
            draft['algorithmRef'] = algorithm_sha
            anchor = {'protocol': PROTOCOL, 'versionRef': ref, 'draft': draft,
                      'previous': None if previous is None else {'versionRef': old['versionRef'], 'sha256': previous.sha},
                      'declaration': actor, 'evidence': rows, 'state': 'FROZEN_PRELIMINARY',
                      'attestation': 'LOCAL_DECLARATION_ONLY', 'scienceValidation': 'NOT_VALIDATED'}
            (directory / 'events').mkdir()
            sha = write_new(directory / 'plan.json', anchor)
        except Exception:
            write_new(directory / 'failed.json', {'state': 'PLAN_CREATION_INCOMPLETE'})
            raise
        return cls(directory, sha)

    def __init__(self, directory, sha):
        require(digest(sha), 'PLAN_EXPECTED_HASH')
        self.directory, self.sha = safe_path(directory), sha
        self.read()

    def read(self):
        value, sha = read_json(self.directory / 'plan.json')
        require(sha == self.sha, 'PLAN_CHANGED')
        fields(value, {'protocol', 'versionRef', 'draft', 'previous', 'declaration', 'evidence',
                       'state', 'attestation', 'scienceValidation'})
        require(value['protocol'] == PROTOCOL and opaque(value['versionRef'])
                and self.directory.name == value['versionRef'] and value['state'] == 'FROZEN_PRELIMINARY'
                and value['attestation'] == 'LOCAL_DECLARATION_ONLY'
                and value['scienceValidation'] == 'NOT_VALIDATED', 'PLAN_ANCHOR')
        validate_draft(value['draft']); declaration(value['declaration'])
        if value['previous'] is not None:
            fields(value['previous'], {'versionRef', 'sha256'})
            require(opaque(value['previous']['versionRef']) and digest(value['previous']['sha256']), 'PLAN_PREVIOUS')
        self._evidence(value['evidence'])
        require({r['role'] for r in value['evidence']} == {'ALGORITHM', 'RULES'}
                and next(r['sha256'] for r in value['evidence'] if r['role'] == 'ALGORITHM')
                    == value['draft']['algorithmRef'], 'PLAN_ALGORITHM_CHANGED')
        require({p.name for p in self.directory.iterdir()} ==
                {'plan.json', 'events'} | {r['path'] for r in value['evidence']}, 'PLAN_PARTIAL_OR_EXTRA')
        safe_path(self.directory / 'events')
        return value

    def _evidence(self, rows, directory=None):
        directory = directory or self.directory
        require(type(rows) is list and 1 <= len(rows) <= 12, 'PLAN_EVIDENCE')
        roles = set()
        for i, row in enumerate(rows):
            fields(row, {'role', 'path', 'sha256', 'bytes'})
            require(type(row['role']) is str and row['role'] not in roles
                    and row['path'] == 'evidence-' + str(i).zfill(2) + '.dat'
                    and digest(row['sha256']) and type(row['bytes']) is int and row['bytes'] > 0,
                    'PLAN_EVIDENCE_RECORD')
            roles.add(row['role'])
            require(fingerprint(directory / row['path']) == {k: row[k] for k in ('sha256', 'bytes')}, 'PLAN_EVIDENCE_CHANGED')

    def events(self):
        anchor = self.read(); head, result = self.sha, []
        paths = sorted((self.directory / 'events').iterdir())
        require(len(paths) <= 500, 'PLAN_EVENT_LIMIT')
        for index, path in enumerate(paths):
            safe_path(path)
            require(path.name == str(index).zfill(4), 'PLAN_EVENT_GAP')
            value, sha = read_json(path / 'event.json')
            fields(value, {'sequence', 'planSha256', 'previousSha256', 'caseRef', 'kind', 'data', 'declaration', 'evidence'})
            require(type(value['sequence']) is int and value['sequence'] == index
                    and value['planSha256'] == self.sha and value['previousSha256'] == head
                    and any(c['caseRef'] == value['caseRef'] for c in anchor['draft']['cases']), 'PLAN_EVENT_BINDING')
            declaration(value['declaration']); self._evidence(value['evidence'], path)
            require({p.name for p in path.iterdir()} == {'event.json'} | {r['path'] for r in value['evidence']}, 'PLAN_EVENT_PARTIAL')
            self._data(value['kind'], value['data'], {r['role'] for r in value['evidence']})
            if value['kind'] == 'OWNER_REVIEW':
                require(value['data']['targetHeadSha256'] == head, 'PLAN_REVIEW_TARGET')
            if value['kind'] == 'OUTCOME_REVIEW':
                require(any(e['kind'] == 'ATTEMPT' and e['caseRef'] == value['caseRef']
                            and e['data']['journalHeadSha256'] == value['data']['targetAttemptHeadSha256']
                            and e['data']['technicalState'] == 'COMPLETED' for e in result), 'PLAN_OUTCOME_TARGET')
            if value['kind'] == 'ATTEMPT':
                if 'inputDerivationSha256' in value['data']:
                    from tools.scientific_transients.derived_input_binding import archived_binding
                    proof = archived_binding(self, value)
                    require(proof.value['planSha256'] == self.sha
                        and proof.value['caseRef'] == value['caseRef']
                        and proof.value['jobId'] == value['data']['identity']['jobId']
                        and proof.value['manifestSha256'] == value['data']['identity']['manifestSha256'],
                        'PLAN_DERIVED_ARCHIVE_BINDING')
                require(not any(e['kind'] == 'ATTEMPT' and e['data']['identity']['attemptId']
                                == value['data']['identity']['attemptId'] for e in result), 'PLAN_ATTEMPT_DUPLICATE')
            head = sha; result.append(value)
        return result, head

    @staticmethod
    def _data(kind, data, roles):
        if kind == 'QUALIFICATION':
            fields(data, {'state'})
            require(data['state'] in {'DOCUMENTED_PENDING_REVIEW', 'NON_EVALUABLE'}
                    and roles == ({'NULL_REFERENCE', 'INDEPENDENCE', 'RATIONALE'}
                                  if data['state'] == 'DOCUMENTED_PENDING_REVIEW' else {'RATIONALE'}), 'PLAN_QUALIFICATION')
        elif kind == 'ATTEMPT':
            derived = 'inputDerivationSha256' in data
            fields(data, {'identity', 'journalHeadSha256', 'technicalReportSha256', 'technicalState',
                          'coverage', 'algorithmMatches', 'chronology', 'scientificOutcome'}
                          | ({'inputDerivationSha256'} if derived else set()))
            require(not derived or digest(data['inputDerivationSha256']), 'PLAN_DERIVED_DIGEST')
            from tools.scientific_transients.attempt_journal import identity
            identity(data['identity'])
            require(digest(data['journalHeadSha256']) and data['technicalState'] in TERMINAL
                    and (digest(data['technicalReportSha256']) if data['technicalState'] == 'COMPLETED'
                         else data['technicalReportSha256'] is None)
                    and data['coverage'] in {'PARTIAL', 'FULL'} and type(data['algorithmMatches']) is bool
                    and data['chronology'] in {'PREEXISTING', 'AFTER_DECLARED_FREEZE'}
                    and data['scientificOutcome'] == 'NOT_EVALUATED'
                    and roles == ({'RATIONALE','INPUT_DERIVATION'} if derived else {'RATIONALE'}), 'PLAN_ATTEMPT')
        elif kind == 'OUTCOME_REVIEW':
            fields(data, {'outcome', 'targetAttemptHeadSha256'})
            require(data['outcome'] in {'NO_SIGNAL_DECLARED', 'FALSE_ALERT_DECLARED', 'INCONCLUSIVE'}
                    and digest(data['targetAttemptHeadSha256']) and roles == {'SCIENTIFIC_OUTCOME'}, 'PLAN_OUTCOME')
        elif kind == 'OWNER_REVIEW':
            fields(data, {'action', 'targetHeadSha256'})
            require(data['action'] in {'KEEP_FOR_REVIEW', 'REJECT', 'FOLLOW_UP'}
                    and digest(data['targetHeadSha256']) and roles == {'RATIONALE'}, 'PLAN_REVIEW')
        else:
            require(False, 'PLAN_EVENT_KIND')

    def append(self, case_ref, kind, data, actor, sources, expected_head):
        declaration(actor); events, head = self.events()
        require(head == expected_head and len(events) < 500, 'PLAN_HEAD_CONFLICT')
        require(any(c['caseRef'] == case_ref for c in self.read()['draft']['cases']), 'PLAN_CASE_UNKNOWN')
        self._data(kind, data, set(sources))
        if kind == 'OWNER_REVIEW':
            require(data['targetHeadSha256'] == head, 'PLAN_REVIEW_TARGET')
        if kind == 'OUTCOME_REVIEW':
            require(any(e['kind'] == 'ATTEMPT' and e['caseRef'] == case_ref
                        and e['data']['journalHeadSha256'] == data['targetAttemptHeadSha256']
                        and e['data']['technicalState'] == 'COMPLETED' for e in events), 'PLAN_OUTCOME_TARGET')
        # The ATTEMPT operation is only permitted through link_attempt, which reads
        # actual journal bytes. Public callers cannot import a success declaration.
        require(kind != 'ATTEMPT', 'PLAN_USE_LINK_ATTEMPT')
        return self._append(case_ref, kind, data, actor, sources, events, head)

    def _append(self, case_ref, kind, data, actor, sources, events, head):
        path = self.directory / 'events' / str(len(events)).zfill(4)
        path.mkdir()  # Concurrent/partial writes never overwrite or repair history.
        try:
            rows = evidence(path, sources)
            self._data(kind, data, {r['role'] for r in rows})
            value = {'sequence': len(events), 'planSha256': self.sha, 'previousSha256': head,
                     'caseRef': case_ref, 'kind': kind, 'data': data, 'declaration': actor, 'evidence': rows}
            return write_new(path / 'event.json', value)
        except Exception:
            write_new(path / 'failed.json', {'state': 'PLAN_EVENT_INCOMPLETE'})
            raise

    def link_attempt(self, case_ref, journal, report_sha, actor, rationale, expected_head, *, derived=None):
        declaration(actor); anchor = self.read(); events, head = self.events()
        require(head == expected_head and len(events) < 500, 'PLAN_HEAD_CONFLICT')
        case = next((c for c in anchor['draft']['cases'] if c['caseRef'] == case_ref), None)
        require(case is not None, 'PLAN_CASE_UNKNOWN')
        journal = AttemptJournal(journal.directory, journal.anchor['identity'])
        attempts = journal._events(); require(attempts and attempts[-1]['kind'] in TERMINAL, 'PLAN_ATTEMPT_ACTIVE')
        state = attempts[-1]['kind']; technical_sha = None
        if state == 'COMPLETED':
            inspect_report(journal, report_sha); technical_sha = report_sha
        else:
            require(report_sha is None, 'PLAN_FAILURE_REPORT')
            # Failure status is retained even when checkpoint bytes are incomplete.
        inputs = {r['sha256'] for r in journal.anchor['snapshot'] if r['role'] == 'INPUT'}
        expected = {f['sha256'] for f in case['frames']}
        sources = {'RATIONALE': rationale}
        if derived is not None:
            from tools.scientific_transients.derived_input_binding import DerivedInputBinding
            require(type(derived) is DerivedInputBinding, 'PLAN_DERIVED_TYPE')
            proof = derived.verify(self, case_ref, journal=journal)
            inputs = {proof['rawSha256']}
            sources['INPUT_DERIVATION'] = derived.path
        require(inputs and inputs <= expected, 'PLAN_ATTEMPT_INPUT_MISMATCH')
        require(not any(e['kind'] == 'ATTEMPT' and e['data']['identity']['attemptId'] == journal.anchor['identity']['attemptId']
                        for e in events), 'PLAN_ATTEMPT_DUPLICATE')
        freeze = dt.datetime.fromisoformat(anchor['declaration']['recordedUTC'])
        prepared = dt.datetime.fromisoformat(attempts[0]['recordedAt'])
        data = {'identity': journal.anchor['identity'], 'journalHeadSha256': journal.head_sha,
                'technicalReportSha256': technical_sha, 'technicalState': state,
                'coverage': 'FULL' if inputs == expected else 'PARTIAL',
                'algorithmMatches': {r['sha256'] for r in journal.anchor['snapshot'] if r['role'] == 'ALGORITHM'}
                    == {anchor['draft']['algorithmRef']},
                'chronology': 'PREEXISTING' if prepared <= freeze else 'AFTER_DECLARED_FREEZE',
                'scientificOutcome': 'NOT_EVALUATED'}
        if derived is not None:
            data['inputDerivationSha256'] = derived.sha
        return self._append(case_ref, 'ATTEMPT', data, actor, sources, events, head)

    def apply_package(self, package, inbox_root):
        """Apply an explicit browser-authored local request; never a native job."""
        fields(package, {'schema', 'packageRef', 'planSha256', 'expectedHeadSha256', 'caseRef',
                         'kind', 'data', 'declaration', 'attachments'})
        require(package['schema'] == 'BKL051_PLAN_REVIEW_REQUEST_V1' and opaque(package['packageRef'])
                and package['planSha256'] == self.sha and digest(package['expectedHeadSha256'])
                and type(package['attachments']) is list and 1 <= len(package['attachments']) <= 3,
                'PLAN_PACKAGE')
        require(package['kind'] in {'QUALIFICATION', 'OUTCOME_REVIEW', 'OWNER_REVIEW'}, 'PLAN_PACKAGE_KIND')
        declaration(package['declaration'])
        decoded, total = {}, 0
        for item in package['attachments']:
            fields(item, {'role', 'sha256', 'base64'})
            require(type(item['role']) is str and item['role'] not in decoded and digest(item['sha256'])
                    and type(item['base64']) is str and len(item['base64']) <= 174764, 'PLAN_PACKAGE_ATTACHMENT')
            try:
                raw = base64.b64decode(item['base64'], validate=True)
            except (ValueError, binascii.Error):
                require(False, 'PLAN_PACKAGE_BASE64')
            require(0 < len(raw) <= 131072 and hashlib.sha256(raw).hexdigest() == item['sha256'], 'PLAN_PACKAGE_HASH')
            decoded[item['role']] = raw; total += len(raw)
        require(total <= 393216, 'PLAN_PACKAGE_LIMIT')
        self._data(package['kind'], package['data'], set(decoded))
        inbox = safe_path(inbox_root)
        require(inbox.is_dir() and inbox != self.directory and inbox not in self.directory.parents
                and self.directory not in inbox.parents, 'PLAN_INBOX_OVERLAP')
        directory = inbox / package['packageRef']; directory.mkdir()
        try:
            write_new(directory / 'request.json', package)
            sources = {}
            for index, (role, raw) in enumerate(sorted(decoded.items())):
                path = directory / ('attachment-' + str(index).zfill(2) + '.dat')
                with path.open('xb') as stream:
                    stream.write(raw)
                    stream.flush()
                    import os
                    os.fsync(stream.fileno())
                sources[role] = path
            sha = self.append(package['caseRef'], package['kind'], package['data'], package['declaration'],
                              sources, package['expectedHeadSha256'])
            write_new(directory / 'receipt.json', {'planSha256': self.sha, 'headSha256': sha,
                                                  'scienceValidation': 'NOT_VALIDATED'})
            return sha
        except Exception:
            write_new(directory / 'failed.json', {'state': 'PLAN_PACKAGE_NOT_ACKNOWLEDGED'})
            raise

    def view(self):
        anchor = self.read(); events, head = self.events(); rows = []
        for case in anchor['draft']['cases']:
            related = [e for e in events if e['caseRef'] == case['caseRef']]
            qualifications = [e for e in related if e['kind'] == 'QUALIFICATION']
            attempts = [e for e in related if e['kind'] == 'ATTEMPT']
            outcomes = [e for e in related if e['kind'] == 'OUTCOME_REVIEW']
            reviews = [e for e in related if e['kind'] == 'OWNER_REVIEW']
            rows.append({'caseRef': case['caseRef'], 'clusterRef': case['clusterRef'],
                         'qualification': qualifications[-1]['data']['state'] if qualifications else 'CANDIDATE',
                         'attempts': [{k: e['data'][k] for k in ('journalHeadSha256', 'technicalState', 'coverage',
                                      'algorithmMatches', 'chronology')} | (
                                      {'inputDerivationSha256': e['data']['inputDerivationSha256']}
                                      if 'inputDerivationSha256' in e['data'] else {}) for e in attempts],
                         'scientificOutcome': outcomes[-1]['data']['outcome'] if outcomes else 'NOT_EVALUATED',
                         'outcomeAttemptHeadSha256': outcomes[-1]['data']['targetAttemptHeadSha256'] if outcomes else None,
                         'ownerReview': ('HISTORICAL' if reviews and reviews[-1] is not events[-1]
                                         else reviews[-1]['data']['action'] if reviews else 'PENDING')})
        return {'schema': ('BKL051_TEST_PLAN_REVIEW_V2' if any('inputDerivationSha256' in e['data']
                            for e in events if e['kind'] == 'ATTEMPT') else VIEW),
                'planRef': anchor['draft']['planRef'], 'versionRef': anchor['versionRef'],
                'planSha256': self.sha, 'headSha256': head, 'state': 'FROZEN_PRELIMINARY',
                'attestation': 'LOCAL_DECLARATION_ONLY', 'scienceValidation': 'NOT_VALIDATED',
                'qualified': 0, 'statisticalResult': None, 'cases': rows}


def main():
    import argparse
    import json
    from pathlib import Path
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    freeze = sub.add_parser('freeze')
    for name in ('root', 'draft', 'algorithm', 'rules', 'actor', 'utc'):
        freeze.add_argument('--' + name, required=True)
    freeze.add_argument('--previous-directory'); freeze.add_argument('--previous-sha256')
    view = sub.add_parser('view')
    for name in ('directory', 'sha256', 'output'):
        view.add_argument('--' + name, required=True)
    record = sub.add_parser('record')
    for name in ('directory', 'sha256', 'request'):
        record.add_argument('--' + name, required=True)
    link = sub.add_parser('link-attempt')
    for name in ('directory', 'sha256', 'case', 'journal', 'actor', 'utc', 'rationale', 'head'):
        link.add_argument('--' + name, required=True)
    link.add_argument('--report-sha256')
    apply = sub.add_parser('apply-package')
    for name in ('directory', 'sha256', 'request', 'inbox'):
        apply.add_argument('--' + name, required=True)
    a = p.parse_args()
    if a.command == 'freeze':
        require(bool(a.previous_directory) == bool(a.previous_sha256), 'PLAN_PREVIOUS_ARGUMENTS')
        previous = PlanVersion(a.previous_directory, a.previous_sha256) if a.previous_directory else None
        plan = PlanVersion.create(a.root, read_json(Path(a.draft))[0], {'actorRef': a.actor, 'recordedUTC': a.utc},
                                  Path(a.algorithm), Path(a.rules), previous)
        print(json.dumps({'directory': str(plan.directory), 'sha256': plan.sha}))
    elif a.command == 'view':
        plan = PlanVersion(a.directory, a.sha256)
        print(write_new(Path(a.output), plan.view()))
    elif a.command == 'record':
        plan = PlanVersion(a.directory, a.sha256); request, _ = read_json(Path(a.request))
        fields(request, {'caseRef', 'kind', 'data', 'declaration', 'sources', 'expectedHeadSha256'})
        print(plan.append(request['caseRef'], request['kind'], request['data'], request['declaration'],
                          request['sources'], request['expectedHeadSha256']))
    elif a.command == 'link-attempt':
        plan = PlanVersion(a.directory, a.sha256)
        anchor, _ = read_json(Path(a.journal) / 'attempt.json')
        journal = AttemptJournal(a.journal, anchor['identity'])
        print(plan.link_attempt(a.case, journal, a.report_sha256,
              {'actorRef': a.actor, 'recordedUTC': a.utc}, Path(a.rationale), a.head))
    else:
        plan = PlanVersion(a.directory, a.sha256)
        print(plan.apply_package(read_json(Path(a.request))[0], a.inbox))


if __name__ == '__main__':
    main()
