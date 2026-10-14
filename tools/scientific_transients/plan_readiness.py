"""Read-only prerequisites audit. Never launches jobs or grants acceptance.

Reports precise blockers on a verified plan/event head. No local declaration
can satisfy scientific attestation; this protocol cannot return READY or PASS.
"""
from tools.pixinsight.local_pilot.broker import ProtocolError, require
from tools.scientific_transients.attempt_journal import AttemptJournal, write_new
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.local_report import inspect as inspect_report
from tools.scientific_transients.test_plan import PlanVersion


def _journal_status(event, root, plan=None):
    if root is None:
        return 'NOT_RECHECKED'
    data = event['data']
    try:
        journal = AttemptJournal(root / data['identity']['attemptId'], data['identity'])
        events = journal._events()
        require(events and events[-1]['kind'] == data['technicalState']
                and journal.head_sha == data['journalHeadSha256'], 'READINESS_JOURNAL_CHANGED')
        if 'inputDerivationSha256' in data:
            from tools.scientific_transients.derived_input_binding import archived_binding
            archived_binding(plan, event).verify(plan, event['caseRef'], journal=journal)
        if data['technicalState'] == 'COMPLETED':
            inspect_report(journal, data['technicalReportSha256'])
        return 'RECHECKED_BYTE_INTEGRITY_ONLY'
    except (OSError, ProtocolError, KeyError, TypeError, ValueError):
        # No absolute path, raw exception or private journal content in the export.
        return 'UNAVAILABLE_OR_CHANGED'


def assess(plan, journal_root=None):
    anchor = plan.read(); events, head = plan.events()
    root = safe_path(journal_root) if journal_root is not None else None
    if root is not None:
        require(root.is_dir(), 'READINESS_JOURNAL_ROOT')
    cases = []
    for case in anchor['draft']['cases']:
        related = [e for e in events if e['caseRef'] == case['caseRef']]
        qualifications = [e for e in related if e['kind'] == 'QUALIFICATION']
        outcomes = [e for e in related if e['kind'] == 'OUTCOME_REVIEW']
        reviews = [e for e in related if e['kind'] == 'OWNER_REVIEW']
        qualification = qualifications[-1]['data']['state'] if qualifications else 'CANDIDATE'
        blockers = ['NULL_REFERENCE_NOT_ATTESTED', 'INDEPENDENCE_NOT_ATTESTED']
        blockers.append({'CANDIDATE': 'QUALIFICATION_MISSING',
                         'DOCUMENTED_PENDING_REVIEW': 'QUALIFICATION_REVIEW_PENDING',
                         'NON_EVALUABLE': 'CASE_NON_EVALUABLE'}[qualification])
        attempts = []
        for event in (e for e in related if e['kind'] == 'ATTEMPT'):
            data = event['data']; reasons = []
            verified = _journal_status(event, root, plan)
            if verified != 'RECHECKED_BYTE_INTEGRITY_ONLY':
                reasons.append('JOURNAL_NOT_RECHECKED' if verified == 'NOT_RECHECKED' else 'JOURNAL_UNAVAILABLE_OR_CHANGED')
            if data['technicalState'] != 'COMPLETED': reasons.append('TECHNICAL_NOT_COMPLETED')
            if data['coverage'] != 'FULL': reasons.append('INPUT_COVERAGE_PARTIAL')
            if not data['algorithmMatches']: reasons.append('ALGORITHM_MISMATCH')
            if data['chronology'] == 'PREEXISTING': reasons.append('ATTEMPT_PREEXISTING')
            # After-declared-freeze is not an authenticated temporal proof.
            reasons.append('CHRONOLOGY_NOT_ATTESTED')
            attempts.append({'journalHeadSha256': data['journalHeadSha256'],
                             'technicalState': data['technicalState'], 'byteIntegrity': verified,
                             'confirmatoryEligible': False, 'blockers': reasons})
        if not attempts: blockers.append('ATTEMPT_MISSING')
        outcome = outcomes[-1]['data']['outcome'] if outcomes else 'NOT_EVALUATED'
        if outcome == 'NOT_EVALUATED': blockers.append('SCIENTIFIC_OUTCOME_MISSING')
        else:
            blockers.append('SCIENTIFIC_OUTCOME_NOT_ATTESTED')
            if outcome == 'FALSE_ALERT_DECLARED': blockers.append('FALSE_ALERT_DECLARED')
            if outcome == 'INCONCLUSIVE': blockers.append('SCIENTIFIC_OUTCOME_INCONCLUSIVE')
        review = 'MISSING' if not reviews else 'CURRENT_DECLARATION' if reviews[-1] is events[-1] else 'HISTORICAL'
        blockers.append({'MISSING': 'OWNER_REVIEW_MISSING', 'CURRENT_DECLARATION': 'OWNER_IDENTITY_NOT_ATTESTED',
                         'HISTORICAL': 'OWNER_REVIEW_HISTORICAL'}[review])
        cases.append({'caseRef': case['caseRef'], 'clusterRef': case['clusterRef'],
                      'qualification': qualification, 'attempts': attempts, 'scientificOutcome': outcome,
                      'ownerReview': review, 'confirmatoryEligible': False, 'blockers': blockers})
    return {'schema': 'BKL051_CONFIRMATORY_BLOCKERS_V1', 'planRef': anchor['draft']['planRef'],
            'versionRef': anchor['versionRef'], 'planSha256': plan.sha, 'headSha256': head,
            'status': 'BLOCKED', 'scope': 'READ_ONLY_LOCAL_PREREQUISITES_AUDIT',
            'globalBlockers': ['PRELIMINARY_PLAN_ONLY', 'ALGORITHM_AND_RULES_SCIENTIFIC_APPROVAL_MISSING',
                               'FREEZE_CHRONOLOGY_NOT_ATTESTED', 'SCIENTIFIC_PIPELINE_NOT_VALIDATED',
                               'QUALIFIED_INDEPENDENT_CONTROLS_MISSING', 'OWNER_ACCEPTANCE_NOT_GRANTED'],
            'requiredIndependentControls': 59, 'falsePositiveMaximum': .05, 'confidence': .95,
            'candidateCases': len(cases), 'declaredDependencyGroups': len({c['clusterRef'] for c in cases}),
            'qualifiedControls': 0, 'confirmatoryEligibleCases': 0, 'statisticalResult': None,
            'scienceValidation': 'NOT_VALIDATED', 'cases': cases}


def main():
    import argparse
    from pathlib import Path
    p = argparse.ArgumentParser(description=__doc__)
    for key in ('directory', 'sha256', 'output'):
        p.add_argument('--' + key, required=True)
    p.add_argument('--journal-root')
    a = p.parse_args()
    value = assess(PlanVersion(a.directory, a.sha256), a.journal_root)
    print(write_new(Path(a.output), value))


if __name__ == '__main__':
    main()
