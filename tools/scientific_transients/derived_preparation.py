"""Export one locally prepared triplet. No transport, credentials or native launch.

This point-in-time receipt is a declaration, not an execution permission,
scientific attestation or guarantee that owner files cannot change later.
"""
from pathlib import Path

from tools.pixinsight.local_pilot.broker import opaque, require
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.derived_input_preflight import preflight
from tools.scientific_transients.operator_run import OperatorPlan


def export_preparation(plan, case_ref, prepared, lineage_directory, lineage_sha,
                       draft_path, draft_sha, signed_directory, signed_sha, expected_head):
    """Accept three explicit (frameRef, OperatorPlan) pairs for this exact head."""
    anchor = plan.read(); events, head = plan.events()
    require(head == expected_head and opaque(case_ref), 'PREPARATION_HEAD_OR_CASE')
    case = next((c for c in anchor['draft']['cases'] if c['caseRef'] == case_ref), None)
    require(case is not None, 'PREPARATION_CASE_UNKNOWN')
    require(not any(e['caseRef'] == case_ref and e['kind'] == 'ATTEMPT' for e in events),
            'PREPARATION_CASE_ALREADY_ATTEMPTED')
    require(type(prepared) is list and len(prepared) == 3
            and all(type(row) is tuple and len(row) == 2 and opaque(row[0])
                    and type(row[1]) is OperatorPlan for row in prepared), 'PREPARATION_OPERATORS')
    frames = [row[0] for row in prepared]
    require(len(set(frames)) == 3 and set(frames) == {f['frameRef'] for f in case['frames']},
            'PREPARATION_EXACT_TRIPLET')
    require(len({op.value['binding']['bindingRef'] for _, op in prepared}) == 3
            and len({op.value['operationRef'] for _, op in prepared}) == 3
            and len({op.value['reservationRef'] for _, op in prepared}) == 3,
            'PREPARATION_DISTINCT_OPERATORS')

    def audit(frame, operator):
        require(operator.value['jobId'] is None, 'PREPARATION_SELECTED_JOB_REFUSED')
        # verify() also refuses started/terminal runs and rehashes the registry.
        operator.verify()
        value = preflight(plan, case_ref, frame, operator, lineage_directory, lineage_sha,
                          draft_path, draft_sha, signed_evidence_directory=signed_directory,
                          signed_evidence_sha=signed_sha)
        require(value['headSha256'] == head and value['status'] == 'BLOCKED'
                and len(value['matches']) == 8
                and all(ok is True for ok in value['matches'].values())
                and value['executionAuthorized'] is False, 'PREPARATION_ASSOCIATION_INCOMPLETE')
        return value

    values = [audit(frame, operator) for frame, operator in prepared]
    require(len({v['rawSha256'] for v in values}) == 3
            and len({v['derivedSha256'] for v in values}) == 3, 'PREPARATION_DISTINCT_INPUTS')
    # A later row may have become stale while earlier rows were inspected.
    # Recheck every source/operator and the event head before exporting.
    require([audit(frame, operator) for frame, operator in prepared] == values,
            'PREPARATION_EVIDENCE_CHANGED')
    require(plan.events()[1] == head, 'PREPARATION_HEAD_CHANGED')
    return {'schema': 'BKL051_DERIVED_PREPARATION_V1',
            'scope': 'LOCAL_PREPARATION_ONLY_NO_EXECUTION_PERMISSION',
            'status': 'PREPARED_NOT_EXECUTED', 'planRef': anchor['draft']['planRef'],
            'versionRef': anchor['versionRef'], 'planSha256': plan.sha, 'headSha256': head,
            'caseRef': case_ref, 'preflights': values, 'selectedJobs': 0, 'nativeStarts': 0,
            'attempts': 0, 'executionAuthorized': False, 'scienceValidation': 'NOT_VALIDATED',
            'qualifiedControls': 0, 'completeUncertainty': None, 'significance': None}


def main():
    import argparse
    from tools.scientific_transients.queue import fields
    from tools.scientific_transients.test_plan import PlanVersion
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('plan', 'plan-sha256', 'head-sha256', 'case', 'operators', 'lineage-directory',
                 'lineage-sha256', 'draft', 'draft-sha256', 'signed-directory', 'signed-sha256', 'output'):
        p.add_argument('--' + name, required=True)
    a = p.parse_args()
    rows, _ = read_json(Path(a.operators))
    require(type(rows) is list and len(rows) == 3, 'PREPARATION_OPERATORS')
    prepared = []
    for row in rows:
        fields(row, {'frameRef', 'operatorPath', 'operatorSha256'})
        prepared.append((row['frameRef'], OperatorPlan.load(Path(row['operatorPath']), row['operatorSha256'])))
    value = export_preparation(PlanVersion(Path(a.plan), a.plan_sha256), a.case, prepared,
                               a.lineage_directory, a.lineage_sha256, Path(a.draft), a.draft_sha256,
                               a.signed_directory, a.signed_sha256, a.head_sha256)
    print(write_new(Path(a.output), value))


if __name__ == '__main__':
    main()
