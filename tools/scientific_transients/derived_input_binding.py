"""Private, byte-pinned association for one preliminary derived-input job.

This evidence never grants native launch or scientific qualification. Source
files are rechecked before dispatch and when archived evidence is audited.
"""
from pathlib import Path
from tools.pixinsight.local_pilot.broker import require, opaque
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.input_lineage import inspect_lineage
from tools.scientific_transients.derived_input_preflight import preflight, signed_read_evidence
from tools.scientific_transients.queue import fields, digest


class DerivedInputBinding:
    @classmethod
    def prepare(cls, plan, case_ref, frame_ref, operator, output, lineage_directory,
                lineage_receipt_sha, draft_path, draft_sha, signed_directory, signed_sha):
        audit = preflight(plan, case_ref, frame_ref, operator, lineage_directory,
            lineage_receipt_sha, draft_path, draft_sha,
            signed_evidence_directory=signed_directory, signed_evidence_sha=signed_sha)
        require(all(audit['matches'].values()), 'DERIVED_ASSOCIATION_INCOMPLETE')
        value = {'protocol': 'DSG_DERIVED_INPUT_BINDING_V1',
            'planSha256': plan.sha, 'caseRef': case_ref, 'frameRef': frame_ref,
            'rawSha256': audit['rawSha256'], 'derivedSha256': audit['derivedSha256'],
            'operatorPlanSha256': operator.sha, 'jobId': operator.value['jobId'],
            'manifestSha256': operator.value['manifestSha256'],
            'algorithmSha256': plan.read()['draft']['algorithmRef'],
            'lineageDirectory': str(safe_path(lineage_directory)),
            'lineageReceiptSha256': lineage_receipt_sha, 'draftPath': str(safe_path(draft_path)),
            'draftSha256': draft_sha, 'signedDirectory': str(safe_path(signed_directory)),
            'signedSha256': signed_sha, 'scienceValidation': 'NOT_VALIDATED',
            'calibrationSemantics': 'NOT_ATTESTED_BY_THIS_IMPORT'}
        output = Path(output)
        require(output.name not in {'', '.', '..'}, 'DERIVED_OUTPUT_PATH')
        output = safe_path(output.parent) / output.name
        sha = write_new(output, value)
        return cls(output, sha)

    def __init__(self, path, sha):
        self.path, self.sha = safe_path(path), sha
        self.value, actual = read_json(self.path)
        require(actual == sha, 'DERIVED_BINDING_CHANGED')
        fields(self.value, {'protocol','planSha256','caseRef','frameRef','rawSha256','derivedSha256',
            'operatorPlanSha256','jobId','manifestSha256','algorithmSha256','lineageDirectory',
            'lineageReceiptSha256','draftPath','draftSha256','signedDirectory','signedSha256',
            'scienceValidation','calibrationSemantics'})
        require(self.value['protocol'] == 'DSG_DERIVED_INPUT_BINDING_V1'
            and opaque(self.value['caseRef']) and opaque(self.value['frameRef'])
            and type(self.value['jobId']) is str and self.value['jobId'].startswith('TRN_')
            and opaque(self.value['jobId'][4:])
            and all(type(self.value[k]) is str and Path(self.value[k]).is_absolute()
                for k in ('lineageDirectory','draftPath','signedDirectory'))
            and self.value['scienceValidation'] == 'NOT_VALIDATED'
            and self.value['calibrationSemantics'] == 'NOT_ATTESTED_BY_THIS_IMPORT'
            and all(digest(self.value[k]) for k in ('planSha256','rawSha256','derivedSha256',
                'operatorPlanSha256','manifestSha256','algorithmSha256','lineageReceiptSha256',
                'draftSha256','signedSha256')), 'DERIVED_BINDING_SCHEMA')

    def verify(self, plan, case_ref, *, operator=None, journal=None):
        require(read_json(self.path) == (self.value, self.sha), 'DERIVED_BINDING_CHANGED')
        v = self.value; anchor = plan.read()
        case = next((c for c in anchor['draft']['cases'] if c['caseRef'] == case_ref), None)
        require(v['planSha256'] == plan.sha and v['caseRef'] == case_ref and case is not None
            and any(f['frameRef'] == v['frameRef'] and f['sha256'] == v['rawSha256'] for f in case['frames'])
            and anchor['draft']['algorithmRef'] == v['algorithmSha256'], 'DERIVED_PLAN_BINDING')
        lineage = inspect_lineage(v['lineageDirectory'], v['lineageReceiptSha256'],
                                  v['draftPath'], v['draftSha256'])
        require(lineage['candidatePlanRef'] == anchor['draft']['planRef'] and any(
            r['rawSha256'] == v['rawSha256'] and r['derivedSha256'] == v['derivedSha256']
            and r['sampleMembership'] == 'IN_CANDIDATE_MANIFEST' for r in lineage['inputs']),
            'DERIVED_LINEAGE_BINDING')
        signed_read_evidence(v['signedDirectory'], v['signedSha256'], v['algorithmSha256'])
        if operator is not None:
            operator.verify()
            require(operator.sha == v['operatorPlanSha256'] and operator.value['jobId'] == v['jobId']
                and operator.value['manifestSha256'] == v['manifestSha256'], 'DERIVED_OPERATOR_BINDING')
            manifest = operator.registry.verify(operator.value['binding']['bindingRef'], v['manifestSha256'])
            require([r['sha256'] for r in manifest['files'] if r['role'] == 'INPUT']
                    == [v['derivedSha256']], 'DERIVED_OPERATOR_INPUT')
        if journal is not None:
            require(journal.anchor['identity']['jobId'] == v['jobId']
                and journal.anchor['identity']['manifestSha256'] == v['manifestSha256'], 'DERIVED_JOURNAL_BINDING')
            require([r['sha256'] for r in journal.anchor['snapshot'] if r['role'] == 'INPUT']
                    == [v['derivedSha256']], 'DERIVED_JOURNAL_INPUT')
            rules = next(r['sha256'] for r in anchor['evidence'] if r['role'] == 'RULES')
            require([r['sha256'] for r in journal.anchor['snapshot'] if r['role'] == 'ALGORITHM']
                    == [v['algorithmSha256']]
                and [r['sha256'] for r in journal.anchor['snapshot'] if r['role'] == 'CONTRACT']
                    == [rules], 'DERIVED_JOURNAL_ALGORITHM_RULES')
        return v


def archived_binding(plan, event):
    """Reopen the immutable private evidence copy; never recreates a runnable job."""
    row = next(r for r in event['evidence'] if r['role'] == 'INPUT_DERIVATION')
    return DerivedInputBinding(plan.directory / 'events' / str(event['sequence']).zfill(4) / row['path'],
                               event['data']['inputDerivationSha256'])
