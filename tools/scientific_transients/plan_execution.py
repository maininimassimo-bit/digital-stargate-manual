"""Bind one diagnostic frame/job to an exact plan/event head before dispatch.

Reuses the existing selected-job caller; no daemon, batch, credential loading,
confirmation mode or launch CLI. API execution requires explicit authorization.
"""
import copy

from tools.pixinsight.local_pilot.broker import require, ProtocolError, opaque
from tools.scientific_transients.attempt_journal import read_json, write_new, copy_verified, AttemptJournal
from tools.scientific_transients.local_registry import safe_path, fingerprint
from tools.scientific_transients.native_supervisor import NativeProcess
from tools.scientific_transients.test_plan import PlanVersion, declaration


class PlanExecution:
    @classmethod
    def prepare(cls, plan, case_ref, frame_ref, operator, root, expected_head, actor, rationale,
                *, mode='PRELIMINARY_DIAGNOSTIC', derived=None):
        require(mode == 'PRELIMINARY_DIAGNOSTIC', 'PLAN_EXECUTION_CONFIRMATORY_UNAVAILABLE')
        declaration(actor)
        require(opaque(case_ref) and opaque(frame_ref), 'PLAN_EXECUTION_CASE')
        anchor = plan.read(); _, head = plan.events()
        require(head == expected_head, 'PLAN_EXECUTION_HEAD_CHANGED')
        operator.verify()
        require(operator.value['jobId'] is not None, 'PLAN_EXECUTION_SELECTED_JOB_REQUIRED')
        case = next((c for c in anchor['draft']['cases'] if c['caseRef'] == case_ref), None)
        frame = next((f for f in case['frames'] if f['frameRef'] == frame_ref), None) if case else None
        require(frame is not None, 'PLAN_EXECUTION_FRAME_UNKNOWN')
        manifest = operator.registry.verify(operator.value['binding']['bindingRef'], operator.value['manifestSha256'])
        require(manifest['binding'] == operator.value['binding'], 'PLAN_EXECUTION_BINDING')
        input_sha = frame['sha256']
        if derived is not None:
            from tools.scientific_transients.derived_input_binding import DerivedInputBinding
            require(type(derived) is DerivedInputBinding, 'PLAN_EXECUTION_DERIVED_TYPE')
            proof = derived.verify(plan, case_ref, operator=operator)
            require(proof['frameRef'] == frame_ref, 'PLAN_EXECUTION_DERIVED_FRAME')
            input_sha = proof['derivedSha256']
        require([r['sha256'] for r in manifest['files'] if r['role'] == 'INPUT'] == [input_sha],
                'PLAN_EXECUTION_INPUT_MISMATCH')
        require([r['sha256'] for r in manifest['files'] if r['role'] == 'ALGORITHM'] == [anchor['draft']['algorithmRef']],
                'PLAN_EXECUTION_ALGORITHM_MISMATCH')
        rules_sha = next(r['sha256'] for r in anchor['evidence'] if r['role'] == 'RULES')
        require([r['sha256'] for r in manifest['files'] if r['role'] == 'CONTRACT'] == [rules_sha],
                'PLAN_EXECUTION_RULES_MISMATCH')
        root = safe_path(root); require(root.is_dir(), 'PLAN_EXECUTION_ROOT')
        for other in [plan.directory, *operator.roots.values()]:
            require(root != other and root not in other.parents and other not in root.parents,
                    'PLAN_EXECUTION_ROOT_OVERLAP')
        directory = root / operator.value['reservationRef']; directory.mkdir()
        try:
            reason = fingerprint(rationale)
            require(0 < reason['bytes'] <= 16 * 1024 * 1024, 'PLAN_EXECUTION_RATIONALE')
            copy_verified(rationale, directory / 'rationale.dat', reason)
            value = {'protocol': 'DSG_PLAN_EXECUTION_BINDING_V1', 'mode': mode,
                     'planSha256': plan.sha, 'planHeadSha256': head, 'caseRef': case_ref,
                     'frameRef': frame_ref, 'inputSha256': input_sha, 'operatorPlanSha256': operator.sha,
                     'selectedJobId': operator.value['jobId'], 'manifestSha256': operator.value['manifestSha256'],
                     'coverage': 'SINGLE_FRAME_OF_TRIPLET', 'declaration': copy.deepcopy(actor), 'rationale': reason,
                     'scienceValidation': 'NOT_VALIDATED', 'confirmatoryEligible': False, 'implicitReplay': False}
            if derived is not None:
                value['inputDerivationSha256'] = derived.sha
            sha = write_new(directory / 'binding.json', value)
        except Exception:
            write_new(directory / 'failed.json', {'state': 'PLAN_EXECUTION_PREPARATION_INCOMPLETE'})
            raise
        result = cls.__new__(cls)
        result.plan, result.operator, result.directory = plan, operator, directory
        result.value, result.sha, result.used = value, sha, False
        result.derived = derived
        return result

    def verify(self):
        value, sha = read_json(self.directory / 'binding.json')
        require(sha == self.sha and value == self.value, 'PLAN_EXECUTION_BINDING_CHANGED')
        self.plan.read(); _, head = self.plan.events()
        require(head == value['planHeadSha256'] and self.plan.sha == value['planSha256'], 'PLAN_EXECUTION_HEAD_CHANGED')
        require(self.operator.sha == value['operatorPlanSha256'], 'PLAN_EXECUTION_OPERATOR_CHANGED')
        self.operator.verify()
        if self.derived is not None:
            require(self.derived.sha == value['inputDerivationSha256'], 'PLAN_EXECUTION_DERIVED_CHANGED')
            self.derived.verify(self.plan, value['caseRef'], operator=self.operator)
        require(fingerprint(self.directory / 'rationale.dat') == value['rationale'], 'PLAN_EXECUTION_RATIONALE_CHANGED')

    def run_selected(self, transport, *, native_launch_authorized=False, spawn=None, **options):
        require(native_launch_authorized is True, 'PLAN_EXECUTION_EXPLICIT_LAUNCH_REQUIRED')
        require(not self.used, 'PLAN_EXECUTION_REPLAY_REFUSED')
        self.used = True  # Uncertainty consumes this session before dispatch.
        launched = False
        try:
            self.verify()
            write_new(self.directory / 'dispatch-intent.json', {'bindingSha256': self.sha,
                      'implicitReplay': False, 'confirmatoryEligible': False})
            binding = self

            class GuardedTransport:
                def request(self, path, value=None):
                    if not launched:
                        binding.verify()
                    return transport.request(path, value)

                def post(self, path, value):
                    return transport.post(path, value)

            def guarded_spawn(directory):
                nonlocal launched
                self.verify()
                write_new(self.directory / 'launch-intent.json', {'bindingSha256': self.sha,
                          'nativeLaunchAuthorized': True, 'implicitReplay': False})
                launched = True  # Even a spawn exception must never be retried.
                return (spawn or NativeProcess)(directory)

            result = self.operator.run_selected(GuardedTransport(), native_launch_authorized=True,
                                                spawn=guarded_spawn, **options)
            state = result.get('state')
            require(state in {'COMPLETED', 'FAILED', 'CANCELLED', 'RECOVERY_REQUIRED', 'RECONCILIATION_REQUIRED'},
                    'PLAN_EXECUTION_OUTCOME')
            write_new(self.directory / 'technical-outcome.json', {'state': state, 'bindingSha256': self.sha,
                      'scienceValidation': 'NOT_VALIDATED', 'confirmatoryEligible': False})
        except BaseException:
            try:
                write_new(self.directory / 'unconfirmed.json', {'state': 'RECONCILIATION_REQUIRED',
                          'nativeStoppedAttested': False, 'implicitReplay': False})
            except OSError:
                pass
            raise ProtocolError('PLAN_EXECUTION_UNCONFIRMED_NO_REPLAY') from None

        # A completed technical job is preserved even when a later plan event
        # prevents linkage. Never repeat the job to repair a missing plan receipt.
        try:
            require(state != 'RECONCILIATION_REQUIRED', 'PLAN_EXECUTION_RESERVATION_UNCERTAIN')
            reserved, _ = read_json(self.operator.roots['intents'] / self.operator.value['reservationRef'] / 'reserved.json')
            identity = reserved['identity']
            journal = AttemptJournal(self.operator.roots['journals'] / identity['attemptId'], identity)
            report_sha = read_json(journal.directory / 'report.json')[1] if state == 'COMPLETED' else None
            head = self.plan.link_attempt(self.value['caseRef'], journal, report_sha,
                                         self.value['declaration'], self.directory / 'rationale.dat',
                                         self.value['planHeadSha256'], derived=self.derived)
            write_new(self.directory / 'plan-linked.json', {'headSha256': head, 'bindingSha256': self.sha})
            linkage = 'LINKED'
        except (Exception, KeyboardInterrupt):
            write_new(self.directory / 'link-pending.json', {'state': 'RECONCILIATION_REQUIRED',
                      'technicalState': state, 'implicitReplay': False, 'scienceValidation': 'NOT_VALIDATED'})
            linkage = 'RECONCILIATION_REQUIRED'
        return {'state': state, 'planLinkage': linkage, 'scienceValidation': 'NOT_VALIDATED',
                'confirmatoryEligible': False, 'implicitReplay': False}


def main():
    """Offline preparation only. Deliberately offers no credential/launch flags."""
    import argparse
    import json
    from pathlib import Path
    from tools.scientific_transients.operator_run import OperatorPlan
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('plan', 'plan-sha256', 'head', 'case', 'frame', 'operator', 'operator-sha256',
                 'root', 'actor', 'utc', 'rationale'):
        p.add_argument('--' + name, required=True)
    a = p.parse_args()
    binding = PlanExecution.prepare(PlanVersion(a.plan, a.plan_sha256), a.case, a.frame,
        OperatorPlan.load(Path(a.operator), a.operator_sha256), a.root, a.head,
        {'actorRef': a.actor, 'recordedUTC': a.utc}, Path(a.rationale))
    print(json.dumps({'bindingSha256': binding.sha, 'nativeLaunchRequested': False,
                      'networkRequested': False, 'confirmatoryEligible': False}))


if __name__ == '__main__':
    main()
