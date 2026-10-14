"""Verify technical coverage of three plan images. No scientific flux comparison.

All linked attempts remain visible, including failures and duplicate coverage.
Three technical completions never imply a qualified null or statistical PASS.
"""
from tools.pixinsight.local_pilot.broker import require, opaque
from tools.scientific_transients.attempt_journal import AttemptJournal, write_new
from tools.scientific_transients.local_report import inspect as inspect_report
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.test_plan import PlanVersion


def inspect_triplet(plan, case_ref, journal_directories):
    require(opaque(case_ref) and type(journal_directories) is dict
            and all(opaque(k) for k in journal_directories), 'TRIPLET_REQUEST')
    anchor = plan.read(); events, head = plan.events()
    case = next((c for c in anchor['draft']['cases'] if c['caseRef'] == case_ref), None)
    require(case is not None, 'TRIPLET_CASE_UNKNOWN')
    attempts = [e['data'] for e in events if e['caseRef'] == case_ref and e['kind'] == 'ATTEMPT']
    rules_sha = next(r['sha256'] for r in anchor['evidence'] if r['role'] == 'RULES')
    frames = [{'frameRef': f['frameRef'], 'sha256': f['sha256'], 'attemptHeads': []} for f in case['frames']]
    rows = []
    for data in attempts:
        identity = data['identity']; directory = journal_directories.get(identity['attemptId'])
        row = {'journalHeadSha256': data['journalHeadSha256'], 'technicalState': data['technicalState'],
               'verification': 'UNAVAILABLE_OR_CHANGED', 'frameRefs': [], 'blockers': []}
        try:
            require(directory is not None, 'TRIPLET_JOURNAL_MISSING')
            journal = AttemptJournal(safe_path(directory), identity)
            retained = journal._events()
            require(retained and journal.head_sha == data['journalHeadSha256']
                    and retained[-1]['kind'] == data['technicalState'], 'TRIPLET_JOURNAL_CHANGED')
            inputs = [r['sha256'] for r in journal.anchor['snapshot'] if r['role'] == 'INPUT']
            require(len(inputs) == 1, 'TRIPLET_SINGLE_INPUT_REQUIRED')
            if 'inputDerivationSha256' in data:
                from tools.scientific_transients.derived_input_binding import archived_binding
                event = next(e for e in events if e['kind'] == 'ATTEMPT' and e['data'] == data)
                proof = archived_binding(plan, event).verify(plan, case_ref, journal=journal)
                inputs = [proof['rawSha256']]
            frame = next((f for f in frames if f['sha256'] == inputs[0]), None)
            require(frame is not None, 'TRIPLET_INPUT_MISMATCH')
            row['frameRefs'] = [frame['frameRef']]
            frame['attemptHeads'].append(data['journalHeadSha256'])
            require({r['sha256'] for r in journal.anchor['snapshot'] if r['role'] == 'ALGORITHM'}
                    == {anchor['draft']['algorithmRef']}, 'TRIPLET_ALGORITHM_MISMATCH')
            require({r['sha256'] for r in journal.anchor['snapshot'] if r['role'] == 'CONTRACT'}
                    == {rules_sha}, 'TRIPLET_RULES_MISMATCH')
            if data['technicalState'] == 'COMPLETED':
                inspect_report(journal, data['technicalReportSha256'])
                row['verification'] = 'RECHECKED_TECHNICAL_REPORT'
            else:
                row['verification'] = 'RETAINED_TECHNICAL_FAILURE'
                row['blockers'].append('TECHNICAL_NOT_COMPLETED')
        except (OSError, ValueError, KeyError, TypeError):
            # Hide local paths and raw parser exceptions from this minimised report.
            row['blockers'].append('JOURNAL_OR_INPUT_BINDING_UNVERIFIED')
        rows.append(row)
    unique = all(len(f['attemptHeads']) == 1 for f in frames)
    complete = (len(rows) == 3 and unique
                and all(r['verification'] == 'RECHECKED_TECHNICAL_REPORT' for r in rows))
    blockers = []
    if len(rows) != 3: blockers.append('EXACTLY_THREE_LINKED_ATTEMPTS_REQUIRED')
    if not unique: blockers.append('ONE_ATTEMPT_PER_DISTINCT_FRAME_REQUIRED')
    if any(r['verification'] != 'RECHECKED_TECHNICAL_REPORT' for r in rows):
        blockers.append('ALL_TECHNICAL_REPORTS_MUST_BE_RECHECKED')
    return {'schema': 'BKL051_TRIPLET_TECHNICAL_V1', 'planRef': anchor['draft']['planRef'],
            'versionRef': anchor['versionRef'], 'planSha256': plan.sha, 'headSha256': head,
            'caseRef': case_ref, 'status': 'TECHNICAL_COVERAGE_COMPLETE' if complete else 'INCOMPLETE',
            'frames': frames, 'attempts': rows, 'blockers': blockers,
            'scope': 'THREE_SINGLE_FRAME_DIAGNOSTIC_RUNS_ONLY', 'qualifiedControls': 0,
            'scienceValidation': 'NOT_VALIDATED', 'photometricComparability': 'NOT_VALIDATED',
            'crossEpochResult': None, 'fullVariance': None, 'significance': None,
            'statisticalResult': None, 'confirmatoryEligible': False}


def main():
    import argparse
    from pathlib import Path
    from tools.scientific_transients.attempt_journal import read_json
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('plan', 'sha256', 'case', 'journal-map', 'output'):
        p.add_argument('--' + name, required=True)
    a = p.parse_args()
    directories, _ = read_json(Path(a.journal_map))
    value = inspect_triplet(PlanVersion(a.plan, a.sha256), a.case, directories)
    print(write_new(Path(a.output), value))


if __name__ == '__main__':
    main()
