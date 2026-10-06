"""Immutable private refinements of completed deliveries; no queue execution."""
import base64
import re
from datetime import date

from .broker import decode, encode, opaque, require
from tools.pixinsight.workflow_archive.archive import build_packet
from tools.scientific_registry.ingestion_security import sanitize_preview
from tools.scientific_registry.ingestion_storage import immutable


def sha(raw):
    import hashlib
    return hashlib.sha256(raw).hexdigest()


class RevisionMixin:
    def revision(self, job_id, revision_id):
        require(opaque(revision_id), 'REVISION_ID')
        parent = self.result(job_id)
        state, _ = self.broker._state()
        require(revision_id in state.get('scientificRevisions',{}).get(job_id,[]), 'REVISION_PENDING')
        raw, _ = self.store.get(f'science/revisions/{job_id}/{revision_id}')
        require(raw is not None, 'REVISION_PENDING')
        result = decode(raw)
        require(result.get('jobId') == job_id and result.get('revisionId') == revision_id and
                result.get('parentReviewSha256') == parent['reviewSha256'] and
                result.get('context') == parent['context'] and
                result.get('reviewSha256') == sha(encode({k:v for k,v in result.items() if k != 'reviewSha256'})),
                'REVISION_INTEGRITY')
        decision, _ = self.store.get(f'science/revision-decisions/{job_id}/{revision_id}')
        result['decision'] = decode(decision) if decision else None
        require(result['decision'] is None or (set(result['decision']) == {'reviewSha256','decision'} and
                result['decision']['reviewSha256'] == result['reviewSha256'] and
                result['decision']['decision'] in {'ACCEPT_PRIVATE','REJECT'}), 'DECISION_INTEGRITY')
        return result

    def revisions(self, job_id):
        self.context(job_id)
        state, _ = self.broker._state()
        ids = state.get('scientificRevisions', {}).get(job_id, [])
        return [{k:r[k] for k in ('revisionId','imageVersionId','reviewSha256','processingDate','label')}
                for r in (self.revision(job_id, identity) for identity in ids)]

    def deliver_revision(self, job_id, revision_id, value):
        require(opaque(revision_id), 'REVISION_ID')
        fields = {'parentReviewSha256','original','previewBase64','workflowBase64','correlationsBase64','label','processingDate'}
        require(isinstance(value, dict) and set(value) == fields, 'REVISION_FIELDS')
        parent = self.result(job_id)
        require(value['parentReviewSha256'] == parent['reviewSha256'], 'REVISION_PARENT_CHANGED')
        require(self.broker.status(job_id)['job']['state'] == 'COMPLETED', 'RESULT_NOT_COMPLETED')
        label = value['label']
        require(isinstance(label,str) and bool(label.strip()) and len(label) <= 160 and
                not any(ord(c) < 32 for c in label) and not re.search(r'[\\/]', label), 'REVISION_LABEL')
        day = value['processingDate']
        require(isinstance(day,str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}',day), 'PROCESSING_DATE_INVALID')
        try:
            date.fromisoformat(day)
        except ValueError:
            require(False, 'PROCESSING_DATE_INVALID')
        original = value['original']
        require(isinstance(original,dict) and set(original) == {'sha256','byteSize','width','height','nonLinear'} and
                isinstance(original['sha256'],str) and re.fullmatch(r'[a-f0-9]{64}',original['sha256']) and
                type(original['byteSize']) is int and 0 < original['byteSize'] <= 1073741824 and
                original['nonLinear'] is True and all(type(original[k]) is int and 0 < original[k] <= 12000
                for k in ('width','height')), 'ORIGINAL_DESCRIPTOR')
        assets = {}
        for role, maximum in [('preview',4*1024*1024),('workflow',2*1024*1024),('correlations',256*1024)]:
            encoded = value[role+'Base64']
            require(isinstance(encoded,str) and 0 < len(encoded) <= ((maximum+2)//3)*4, 'RESULT_SIZE')
            try:
                raw = base64.b64decode(encoded,validate=True)
            except ValueError:
                require(False,'RESULT_ENCODING')
            require(0 < len(raw) <= maximum,'RESULT_SIZE')
            assets[role] = raw
        assets['preview'] = sanitize_preview(assets['preview'],'image/jpeg')
        packet = build_packet(assets['workflow'],'BKL049-refinement-'+revision_id,
                              self.broker.clock().strftime('%Y-%m-%dT%H:%M:%SZ'))
        require(packet['extractionState'] == 'PARSED_SUBSET', 'REVISION_WORKFLOW_REQUIRED')
        archive = packet['archive']; root = archive['instances'][archive['root']]
        require(root['process'] == 'ProcessContainer' and root['children'], 'REVISION_WORKFLOW_REQUIRED')
        steps = [{'ordinal':i+1,'processId':archive['instances'][name]['process']}
                 for i,name in enumerate(root['children'])]
        correlations = decode(assets['correlations'])
        require(isinstance(correlations,dict) and set(correlations) ==
                {'jobId','revisionId','parentReviewSha256','upstreamHistoryCompleteness','instances'} and
                correlations['jobId'] == job_id and correlations['revisionId'] == revision_id and
                correlations['parentReviewSha256'] == parent['reviewSha256'] and
                correlations['upstreamHistoryCompleteness'] == 'NOT_ESTABLISHED' and
                isinstance(correlations['instances'],list) and len(correlations['instances']) == len(steps),
                'CORRELATIONS_BINDING')
        for ordinal,(row,name) in enumerate(zip(correlations['instances'],root['children']),1):
            require(isinstance(row,dict) and set(row) == {'ordinal','variable'} and
                    type(row['ordinal']) is int and row['ordinal'] == ordinal and row['variable'] == name,
                    'CORRELATIONS_BINDING')
        receipt = {k:parent[k] for k in ('jobId','context','imageId','executionEvidence','upstreamHistoryCompleteness')}
        receipt.update(revisionId=revision_id,parentReviewSha256=parent['reviewSha256'],
                       parentOriginalSha256=parent['original']['sha256'],original=original,
                       imageVersionId='VER-'+revision_id,workflowId='WF-'+revision_id,
                       processingDate=day,label=label,steps=steps,workflowCompleteness='INCREMENTAL_REFINEMENT_ONLY',
                       scientificAcceptance='OWNER_REVIEW_REQUIRED',publication='NONE',originalLocation='OWNER_PC')
        receipt.update({role+'Sha256':sha(raw) for role,raw in assets.items()})
        receipt['reviewSha256'] = sha(encode(receipt))
        # Capacity precedes asset writes. CAS below resolves concurrent additions.
        state, _ = self.broker._state()
        index = state.get('scientificRevisions',{}).get(job_id,[])
        require(revision_id in index or len(index) < 16, 'REVISION_CAPACITY')
        for role,raw in assets.items():
            immutable(self.store,'science/assets/'+receipt[role+'Sha256'],raw)
        immutable(self.store,f'science/revisions/{job_id}/{revision_id}',encode(receipt))
        def operation(state,_now):
            index = state.setdefault('scientificRevisions',{}).setdefault(job_id,[])
            if revision_id not in index:
                require(len(index) < 16,'REVISION_CAPACITY')
                index.append(revision_id)
            return receipt
        return self.broker._mutate(operation)

    def revision_asset(self, job_id, revision_id, role):
        require(role in {'preview','workflow','correlations'},'ASSET_ROLE')
        result = self.revision(job_id,revision_id)
        raw,_ = self.store.get('science/assets/'+result[role+'Sha256'])
        require(raw is not None and sha(raw) == result[role+'Sha256'],'ASSET_INTEGRITY')
        return raw

    def decide_revision(self, job_id, revision_id, value):
        result = self.revision(job_id,revision_id)
        require(isinstance(value,dict) and set(value) == {'reviewSha256','decision'} and
                value['reviewSha256'] == result['reviewSha256'] and value['decision'] in {'ACCEPT_PRIVATE','REJECT'},
                'REVIEW_CHANGED')
        immutable(self.store,f'science/revision-decisions/{job_id}/{revision_id}',encode(value))
        return {'decision':value,'publication':'NONE'}
