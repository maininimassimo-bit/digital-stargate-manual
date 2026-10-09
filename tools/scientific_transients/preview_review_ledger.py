"""Private append-only review history for frozen previews. Never grants send authority."""
import os
from tools.pixinsight.local_pilot.broker import opaque, require
from tools.scientific_transients.attempt_journal import read_json, write_new, copy_verified
from tools.scientific_transients.cbat_preview import utc
from tools.scientific_transients.channel_review import text
from tools.scientific_transients.local_registry import safe_path, fingerprint, LIMIT
from tools.scientific_transients.queue import fields, digest

PROTOCOL = 'DSG_PRIVATE_PREVIEW_REVIEW_LEDGER_V1'
FORMATS = {'CBAT': ('DSG_CBAT_NOVA_PREVIEW_V1', 'PRIVATE_PREVIEW', 'preview.json', 'preview.txt'),
           'MPC': ('DSG_MPC_ADES_PREVIEW_V1', 'PRIVATE_PREVIEW', 'preview.json', 'preview.xml'),
           'TNS': ('DSG_CHANNEL_REVIEW_V1', 'PRIVATE_REVIEW_WORKSHEET', 'worksheet.json', 'worksheet.txt'),
           'VSX': ('DSG_CHANNEL_REVIEW_V1', 'PRIVATE_REVIEW_WORKSHEET', 'worksheet.json', 'worksheet.txt')}
ACTIONS = {'KEEP_FOR_REVIEW', 'REJECT_CANDIDATE', 'FOLLOW_UP', 'REVOKE_REVIEW'}
MAX_EVENTS = 128


def inspect_preview(directory, receipt_sha, channel):
    require(type(channel) is str and channel in FORMATS and digest(receipt_sha), 'LEDGER_PREVIEW_IDENTITY')
    directory = safe_path(directory); require(directory.is_dir(), 'LEDGER_PREVIEW_DIRECTORY')
    protocol, state, data_name, text_name = FORMATS[channel]
    receipt, actual = read_json(directory / 'export.json')
    require(actual == receipt_sha, 'LEDGER_PREVIEW_RECEIPT_CHANGED')
    fields(receipt, {'protocol', 'state', 'requestSha256', 'files', 'externalSubmission'})
    require(receipt['protocol'] == protocol and receipt['state'] == state and digest(receipt['requestSha256'])
            and receipt['externalSubmission'] == 'NONE', 'LEDGER_PREVIEW_RECEIPT')
    fields(receipt['files'], {data_name, text_name})
    require({p.name for p in directory.iterdir()} == {'export.json', data_name, text_name}, 'LEDGER_PREVIEW_PARTIAL_OR_EXTRA')
    records = [{'sourceName': 'export.json', **fingerprint(directory / 'export.json')}]
    for name in (data_name, text_name):
        record = receipt['files'][name]; fields(record, {'sha256', 'bytes'})
        require(digest(record['sha256']) and type(record['bytes']) is int and 0 < record['bytes'] <= LIMIT,
                'LEDGER_PREVIEW_FILE_RECORD')
        require(fingerprint(directory / name) == record, 'LEDGER_PREVIEW_BYTES_CHANGED')
        records.append({'sourceName': name, **record})
    value, _ = read_json(directory / data_name)
    require(value['protocol'] == protocol and value['state'] == state and value['requestSha256'] == receipt['requestSha256']
            and value['scienceValidation'] == 'NOT_VALIDATED' and value['declarationsAttested'] is False
            and value['submissionAuthorized'] is False and value['externalSubmission'] == 'NONE'
            and value['providerAcknowledgement'] == 'NONE', 'LEDGER_PRIVATE_PREVIEW_REQUIRED')
    declarations = value['declarations']
    if channel in {'TNS', 'VSX'}: require(declarations['channelDeclared'] == channel, 'LEDGER_DECLARED_CHANNEL')
    elif channel == 'CBAT': require(declarations['categoryDeclared'] == 'GALACTIC_NOVA_CANDIDATE', 'LEDGER_DECLARED_CHANNEL')
    preview_ref = declarations['reviewRef' if channel in {'TNS', 'VSX'} else 'exportRef']
    candidate = declarations.get('candidateRef')
    require(opaque(preview_ref) and (candidate is None or opaque(candidate)), 'LEDGER_PREVIEW_REF')
    return {'channel': channel, 'previewRef': preview_ref, 'candidateRef': candidate, 'receiptSha256': receipt_sha,
            'sourceRequestSha256': receipt['requestSha256'], 'files': records}


class PreviewReviewLedger:
    @classmethod
    def prepare(cls, source_directory, receipt_sha, channel, ledger_root, ledger_ref):
        require(opaque(ledger_ref), 'LEDGER_ID')
        root, source = safe_path(ledger_root), safe_path(source_directory)
        require(root.is_dir() and root != source and root not in source.parents and source not in root.parents, 'LEDGER_ROOT_OVERLAP')
        preview = inspect_preview(source, receipt_sha, channel)
        directory = root / ledger_ref; directory.mkdir()
        try:
            (directory / 'snapshot').mkdir(); (directory / 'events').mkdir()
            rows = []
            for record in preview['files']:
                name = 'snapshot/' + record['sourceName']; expected = {k: record[k] for k in ('sha256', 'bytes')}
                copy_verified(source / record['sourceName'], directory / name, expected)
                rows.append({'path': name, **record})
            require(inspect_preview(source, receipt_sha, channel) == preview, 'LEDGER_PREVIEW_CHANGED_DURING_COPY')
            anchor = {'protocol': PROTOCOL, 'ledgerRef': ledger_ref, 'preview': {k: v for k, v in preview.items() if k != 'files'},
                'snapshot': rows, 'scope': 'PRIVATE_PREVIEW_REVIEW_ONLY', 'scienceValidation': 'NOT_VALIDATED',
                'submissionAuthorized': False, 'externalSubmission': 'NONE', 'completeDependencyArchive': False}
            sha = write_new(directory / 'ledger.json', anchor)
        except Exception:
            write_new(directory / 'failed.json', {'state': 'LEDGER_PREPARATION_INCOMPLETE'}); raise
        return cls(directory, sha)

    def __init__(self, directory, expected_anchor_sha):
        require(digest(expected_anchor_sha), 'LEDGER_ANCHOR_DIGEST')
        self.directory, self.anchor_sha = safe_path(directory), expected_anchor_sha
        self._anchor()

    def _anchor(self):
        safe_path(self.directory)
        require({p.name for p in self.directory.iterdir()} == {'ledger.json', 'snapshot', 'events'}, 'LEDGER_PARTIAL_OR_EXTRA')
        value, actual = read_json(self.directory / 'ledger.json')
        require(actual == self.anchor_sha, 'LEDGER_ANCHOR_CHANGED')
        fields(value, {'protocol', 'ledgerRef', 'preview', 'snapshot', 'scope', 'scienceValidation',
                       'submissionAuthorized', 'externalSubmission', 'completeDependencyArchive'})
        require(value['protocol'] == PROTOCOL and opaque(value['ledgerRef']) and self.directory.name == value['ledgerRef']
                and value['scope'] == 'PRIVATE_PREVIEW_REVIEW_ONLY' and value['scienceValidation'] == 'NOT_VALIDATED'
                and value['submissionAuthorized'] is False and value['externalSubmission'] == 'NONE'
                and value['completeDependencyArchive'] is False, 'LEDGER_ANCHOR')
        fields(value['preview'], {'channel', 'previewRef', 'candidateRef', 'receiptSha256', 'sourceRequestSha256'})
        require(opaque(value['preview']['previewRef']) and (value['preview']['candidateRef'] is None or
                opaque(value['preview']['candidateRef'])) and digest(value['preview']['sourceRequestSha256']), 'LEDGER_PREVIEW')
        observed = inspect_preview(self.directory / 'snapshot', value['preview']['receiptSha256'], value['preview']['channel'])
        require({k: v for k, v in observed.items() if k != 'files'} == value['preview'], 'LEDGER_SNAPSHOT_PREVIEW')
        require(type(value['snapshot']) is list and len(value['snapshot']) == 3, 'LEDGER_SNAPSHOT')
        require(value['snapshot'] == [{'path': 'snapshot/' + row['sourceName'], **row} for row in observed['files']], 'LEDGER_SNAPSHOT_RECORDS')
        safe_path(self.directory / 'events'); require((self.directory / 'events').is_dir(), 'LEDGER_EVENTS_DIRECTORY')
        return value

    @staticmethod
    def _decision(value):
        fields(value, {'eventRef', 'actorRef', 'recordedUTC', 'action', 'targetEventRef', 'note'})
        require(opaque(value['eventRef']) and opaque(value['actorRef']), 'LEDGER_DECISION_ID')
        utc(value['recordedUTC']); text(value['note'], 2048)
        require(type(value['action']) is str and value['action'] in ACTIONS, 'LEDGER_ACTION')
        require((value['action'] == 'REVOKE_REVIEW' and opaque(value['targetEventRef'])) or
                (value['action'] != 'REVOKE_REVIEW' and value['targetEventRef'] is None), 'LEDGER_REVOCATION_TARGET')

    def inspect(self, expected_head_sha):
        require(digest(expected_head_sha), 'LEDGER_HEAD_DIGEST')
        anchor = self._anchor(); events, head, revoked = [], self.anchor_sha, set()
        paths = sorted((self.directory / 'events').iterdir())
        require(len(paths) <= MAX_EVENTS, 'LEDGER_EVENT_LIMIT')
        seen = set()
        for index, path in enumerate(paths):
            require(path.name == str(index).zfill(4) + '.json', 'LEDGER_SEQUENCE_GAP_OR_EXTRA')
            event, actual = read_json(path)
            fields(event, {'protocol', 'sequence', 'anchorSha256', 'previousSha256', 'decision', 'scope', 'submissionAuthorized'})
            require(event['protocol'] == PROTOCOL and type(event['sequence']) is int and event['sequence'] == index
                    and event['anchorSha256'] == self.anchor_sha and event['previousSha256'] == head
                    and event['scope'] == 'PRIVATE_PREVIEW_REVIEW_ONLY' and event['submissionAuthorized'] is False, 'LEDGER_CHAIN')
            decision = event['decision']; self._decision(decision)
            require(decision['eventRef'] not in seen, 'LEDGER_DUPLICATE_EVENT')
            require(not events or utc(decision['recordedUTC']) >= utc(events[-1]['decision']['recordedUTC']), 'LEDGER_TIME_ORDER')
            if decision['action'] == 'REVOKE_REVIEW':
                target = next((e for e in events if e['decision']['eventRef'] == decision['targetEventRef']), None)
                require(target is not None and target['decision']['action'] != 'REVOKE_REVIEW'
                        and decision['targetEventRef'] not in revoked, 'LEDGER_REVOCATION_TARGET')
                revoked.add(decision['targetEventRef'])
            seen.add(decision['eventRef']); events.append(event); head = actual
        require(head == expected_head_sha, 'LEDGER_HEAD_CHANGED_OR_ROLLED_BACK')
        return {'anchor': anchor, 'headSha256': head, 'events': events, 'revokedEventRefs': sorted(revoked),
                'state': 'PRIVATE_REVIEW_HISTORY', 'actorIdentityAttested': False, 'scientificAcceptance': False,
                'submissionAuthorized': False, 'externalSubmission': 'NONE', 'providerAcknowledgement': 'NONE'}

    def append(self, decision, expected_head_sha):
        self._decision(decision); value = self.inspect(expected_head_sha); events = value['events']
        prior = next((e for e in events if e['decision']['eventRef'] == decision['eventRef']), None)
        if prior is not None:
            require(prior['decision'] == decision, 'LEDGER_EVENT_IDEMPOTENCY_CONFLICT')
            return value  # A current pinned head is still required; no rewrite or retry after uncertainty.
        require(len(events) < MAX_EVENTS, 'LEDGER_EVENT_LIMIT')
        event = {'protocol': PROTOCOL, 'sequence': len(events), 'anchorSha256': self.anchor_sha,
                 'previousSha256': expected_head_sha, 'decision': decision,
                 'scope': 'PRIVATE_PREVIEW_REVIEW_ONLY', 'submissionAuthorized': False}
        if events: require(utc(decision['recordedUTC']) >= utc(events[-1]['decision']['recordedUTC']), 'LEDGER_TIME_ORDER')
        if decision['action'] == 'REVOKE_REVIEW':
            target = next((e for e in events if e['decision']['eventRef'] == decision['targetEventRef']), None)
            require(target is not None and target['decision']['action'] != 'REVOKE_REVIEW'
                    and decision['targetEventRef'] not in value['revokedEventRefs'], 'LEDGER_REVOCATION_TARGET')
        sha = write_new(self.directory / 'events' / (str(len(events)).zfill(4) + '.json'), event)
        return self.inspect(sha)  # Failure leaves the immutable record for explicit reconciliation.

    def verify_current_preview(self, source_directory, receipt_sha, expected_head_sha):
        value = self.inspect(expected_head_sha)
        current = inspect_preview(source_directory, receipt_sha, value['anchor']['preview']['channel'])
        require({k: v for k, v in current.items() if k != 'files'} == value['anchor']['preview']
                and [{'path': 'snapshot/' + row['sourceName'], **row} for row in current['files']]
                == value['anchor']['snapshot'], 'LEDGER_PREVIEW_REVISION_CHANGED')
        return {'state': 'FROZEN_PREVIEW_BYTES_MATCH', 'headSha256': value['headSha256'],
                'submissionAuthorized': False, 'scientificAcceptance': False, 'externalSubmission': 'NONE'}

    def export_history(self, expected_head_sha, output_root, export_ref):
        require(opaque(export_ref), 'LEDGER_HISTORY_EXPORT_ID')
        root = safe_path(output_root)
        require(root.is_dir() and root != self.directory and root not in self.directory.parents
                and self.directory not in root.parents, 'LEDGER_HISTORY_ROOT_OVERLAP')
        value = self.inspect(expected_head_sha); directory = root / export_ref; directory.mkdir()
        try:
            write_new(directory / 'history.json', value)
            preview = value['anchor']['preview']
            lines = ['PRIVATE REVIEW HISTORY - NO SUBMISSION AUTHORITY', 'Channel: ' + preview['channel'],
                     'Preview receipt SHA256: ' + preview['receiptSha256'], 'Ledger head SHA256: ' + expected_head_sha,
                     'Actor identities and review timestamps are declarations, not authenticated attestations.',
                     'Scientific acceptance: NONE. External submission: NONE. Provider acknowledgement: NONE.']
            for event in value['events']:
                decision = event['decision']; revoked = decision['eventRef'] in value['revokedEventRefs']
                lines.extend(['Review event ' + str(event['sequence'] + 1), 'UTC (declared): ' + decision['recordedUTC'],
                    'Action: ' + decision['action'], 'Review revoked: ' + ('YES' if revoked else 'NO'),
                    'Note: ' + decision['note']])
            lines.append('Original scientific evidence and installed dependencies remain external; archive is not self-contained.')
            with (directory / 'history.txt').open('xb') as stream:
                stream.write(('\n'.join(lines) + '\n').encode('utf-8')); stream.flush(); os.fsync(stream.fileno())
            require(self.inspect(expected_head_sha) == value, 'LEDGER_CHANGED_DURING_EXPORT')
            write_new(directory / 'export.json', {'protocol': PROTOCOL, 'headSha256': expected_head_sha,
                'files': {name: fingerprint(directory / name) for name in ('history.json', 'history.txt')},
                'state': 'PRIVATE_REVIEW_HISTORY', 'submissionAuthorized': False, 'externalSubmission': 'NONE'})
        except Exception:
            write_new(directory / 'failed.json', {'state': 'LEDGER_HISTORY_EXPORT_INCOMPLETE'}); raise
        return directory
