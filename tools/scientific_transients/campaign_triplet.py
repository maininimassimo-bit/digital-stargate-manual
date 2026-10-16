"""Explicit sequential triplet caller; never a daemon, replay or science review."""
import copy
import time

from tools.pixinsight.local_pilot.broker import require, opaque, ProtocolError
from tools.scientific_transients.attempt_journal import AttemptJournal, read_json, write_new
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.confirmatory_campaign import fingerprint
from tools.scientific_transients.campaign_input_archive import CampaignInputArchive
from tools.scientific_transients.campaign_dispatch import CampaignOwnerOperations, CampaignReservationAdapter, BASE
from tools.scientific_transients.operator_run import OperatorPlan
from tools.scientific_transients.queue import fields, digest
from tools.scientific_transients.campaign_handoff import validate_handoff, inspect_remote, compare_technical


class CampaignTriplet:
    @classmethod
    def prepare(cls, root, context_path, context_file_sha, archive, plans, decision_id):
        result = cls._build(root, context_path, context_file_sha, archive, plans, decision_id)
        result.directory.mkdir()
        for name in ('owner','adapters','frames'): (result.directory / name).mkdir()
        result.selection_sha = write_new(result.directory / 'selection.json', result.selection)
        result.phase = 'PREPARED'
        return result

    @classmethod
    def _build(cls, root, context_path, context_file_sha, archive, plans, decision_id):
        require(type(archive) is CampaignInputArchive and type(plans) is list and len(plans) == 3
                and all(type(p) is OperatorPlan for p in plans) and opaque(decision_id)
                and digest(context_file_sha), 'CAMPAIGN_TRIPLET_ARGUMENTS')
        context, actual = read_json(context_path)
        require(actual == context_file_sha, 'CAMPAIGN_TRIPLET_CONTEXT_FILE')
        fields(context, {'protocol','planRef','planSha256','freezeEventSha256','frozenUTC',
            'inputReviewSnapshotSha256','witnessRef','witnessSha256','inputReportSha256','frames',
            'launchAuthorized','scientificValidation','algorithmRef','algorithmSha256','contractRef',
            'contractSha256','contextSha256'})
        unhashed = {k:v for k,v in context.items() if k != 'contextSha256'}
        require(context['protocol'] == 'DSG_CONFIRMATORY_DISPATCH_CONTEXT_V1'
                and fingerprint(unhashed) == context['contextSha256'] and opaque(context['planRef'])
                and context['launchAuthorized'] is False and context['scientificValidation'] == 'NOT_VALIDATED',
                'CAMPAIGN_TRIPLET_CONTEXT')
        witness = archive.verify()
        require(context['witnessRef'] == witness['witnessRef'] and context['frames'] == witness['frames']
                and context['inputReportSha256'] == witness['reportSha256'], 'CAMPAIGN_TRIPLET_ARCHIVE')
        root = safe_path(root); require(root.is_dir(), 'CAMPAIGN_TRIPLET_ROOT')
        paths = [archive.directory]
        for plan in plans:
            plan.verify(); paths.extend(plan.roots.values())
        require(all(root != p and root not in p.parents and p not in root.parents for p in paths),
                'CAMPAIGN_TRIPLET_ROOT_OVERLAP')
        values = [p.value for p in plans]
        require(len({v['jobId'] for v in values}) == 3 and all(v['jobId'] is not None for v in values)
                and len({v['binding']['bindingRef'] for v in values}) == 3
                and len({v['operationRef'] for v in values}) == 3
                and len({str(p.roots['run']) for p in plans}) == 3
                and len({v['reservationRef'] for v in values}) == 3
                and len({v['workerId'] for v in values}) == len({v['rootId'] for v in values}) == 1,
                'CAMPAIGN_TRIPLET_DISTINCT_SELECTION')
        result = cls.__new__(cls)
        result.context_path, result.context_file_sha = safe_path(context_path), context_file_sha
        result.context, result.archive, result.plans = context, archive, plans
        result.consumed_ordinals = set()
        result._verify_bindings()
        request = {'decisionId': decision_id, 'contextSha256': context['contextSha256'],
                   'witnessRef': context['witnessRef'], 'workerId': values[0]['workerId'],
                   'rootId': values[0]['rootId'], 'archiveSha256': archive.sha,
                   'jobs': [{'requestId': v['jobId'][4:], 'binding': copy.deepcopy(v['binding'])} for v in values]}
        result.directory = root / context['contextSha256']
        result.selection = {'contextFileSha256': context_file_sha, 'archiveSha256': archive.sha,
                            'operatorPlanSha256': [p.sha for p in plans], 'request': request,
                            'nativeLaunchAuthorized': False, 'implicitReplay': False}
        result.selection_sha = fingerprint(result.selection)
        result.phase = 'UNPERSISTED'
        return result

    @classmethod
    def reopen_prepared(cls, root, context_path, context_file_sha, archive, plans, decision_id):
        result = cls._build(root, context_path, context_file_sha, archive, plans, decision_id)
        safe_path(result.directory)
        require({p.name for p in result.directory.iterdir()} == {'owner','adapters','frames','selection.json'}
                and all(not any(safe_path(result.directory / name).iterdir()) for name in ('owner','adapters','frames')),
                'CAMPAIGN_TRIPLET_NOT_PRISTINE')
        result.verify(); result.phase = 'PREPARED'
        return result

    @classmethod
    def reopen_registered(cls, root, context_path, context_file_sha, archive, plans, decision_id):
        """Open only a registered, never launched package; never recover an attempt."""
        result = cls._build(root, context_path, context_file_sha, archive, plans, decision_id)
        safe_path(result.directory)
        require({p.name for p in result.directory.iterdir()} ==
                {'owner','adapters','frames','selection.json','registration','registered.json'},
                'CAMPAIGN_TRIPLET_NOT_PRISTINE')
        require(all(not any(safe_path(result.directory / name).iterdir()) for name in ('owner','adapters','frames')),
                'CAMPAIGN_TRIPLET_NOT_PRISTINE')
        result.verify(); result._verify_registration()
        result.phase = 'REGISTERED'
        return result

    def _verify_registration(self):
        value, _ = read_json(self.directory / 'registered.json')
        fields(value, {'selectionSha256','ackSha256','nativeLaunchAuthorized'})
        require(value['selectionSha256'] == self.selection_sha and value['nativeLaunchAuthorized'] is False
                and type(value['ackSha256']) is list and len(value['ackSha256']) == 3,
                'CAMPAIGN_TRIPLET_REGISTRATION')
        for ordinal, plan in enumerate(self.plans):
            folder = self.directory / 'registration' / str(ordinal)
            intent, _ = read_json(folder / 'intent.json')
            ack, sha = read_json(folder / 'ack.json')
            require(intent == {'binding': plan.value['binding'], 'implicitRetry': False}
                    and ack == {'binding': plan.value['binding']} and sha == value['ackSha256'][ordinal],
                    'CAMPAIGN_TRIPLET_REGISTRATION')

    def register_all(self, worker_transport):
        require(self.phase == 'PREPARED', 'CAMPAIGN_TRIPLET_REGISTER_ONCE')
        self.phase = 'REGISTERING'
        try:
            self.verify(); directory = self.directory / 'registration'; directory.mkdir(); hashes = []
            for ordinal, plan in enumerate(self.plans):
                self.verify(); folder = directory / str(ordinal); folder.mkdir()
                binding = copy.deepcopy(plan.value['binding'])
                write_new(folder / 'intent.json', {'binding': binding, 'implicitRetry': False})
                response = worker_transport.request('/v1/transient-analysis/worker/register', binding)
                require(response == binding, 'CAMPAIGN_TRIPLET_REGISTER_ACK')
                hashes.append(write_new(folder / 'ack.json', {'binding': binding}))
            write_new(self.directory / 'registered.json', {'selectionSha256': self.selection_sha,
                      'ackSha256': hashes, 'nativeLaunchAuthorized': False})
            self.phase = 'REGISTERED'
            return {'registeredBindings': 3, 'nativeLaunchRequested': False}
        except BaseException:
            self.phase = 'RECONCILIATION_REQUIRED'
            try: write_new(self.directory / 'unconfirmed.json', {'state': self.phase, 'implicitReplay': False})
            except (OSError, ProtocolError): pass
            raise ProtocolError('CAMPAIGN_TRIPLET_REGISTER_UNCONFIRMED_NO_REPLAY') from None

    def owner_proposal(self):
        require(self.phase == 'REGISTERED', 'CAMPAIGN_TRIPLET_REGISTRATION_REQUIRED')
        self.verify(); self._verify_registration()
        value = {'protocol': 'DSG_CAMPAIGN_OWNER_DISPATCH_PROPOSAL_V1',
                 'planRef': self.context['planRef'], 'request': copy.deepcopy(self.selection['request']),
                 'launchAuthorized': False, 'scientificValidation': 'NOT_VALIDATED'}
        value['proposalSha256'] = fingerprint(value)
        return value

    def _verify_bindings(self):
        context = self.context
        witness = self.archive.verify()
        require(witness['frames'] == context['frames'] and witness['reportSha256'] == context['inputReportSha256'],
                'CAMPAIGN_TRIPLET_ARCHIVE_CHANGED')
        for ordinal, (frame, plan) in enumerate(zip(context['frames'], self.plans)):
            if ordinal in self.consumed_ordinals:
                require(read_json(plan.path) == (plan.value, plan.sha), 'CAMPAIGN_TRIPLET_OPERATOR_CHANGED')
            else:
                plan.verify()
            value = plan.value
            require(value['binding']['inputRef'] == frame['frameRef']
                    and value['binding']['algorithmRef'] == context['algorithmRef']
                    and value['binding']['contractRef'] == context['contractRef'], 'CAMPAIGN_TRIPLET_BINDING')
            manifest = plan.registry.verify(value['binding']['bindingRef'], value['manifestSha256'])
            for role, expected in (('INPUT', frame['sha256']), ('ALGORITHM', context['algorithmSha256']),
                                   ('CONTRACT', context['contractSha256'])):
                records = [r for r in manifest['files'] if r['role'] == role]
                require(len(records) == 1 and records[0]['sha256'] == expected, 'CAMPAIGN_TRIPLET_BYTES')

    def verify(self):
        context, sha = read_json(self.context_path)
        require(context == self.context and sha == self.context_file_sha
                and read_json(self.directory / 'selection.json') == (self.selection, self.selection_sha),
                'CAMPAIGN_TRIPLET_CHANGED')
        self._verify_bindings()

    def _stop_evidence(self, ordinal, plan, adapter, outcome):
        mapping = adapter.mapping()
        require(outcome['state'] == 'COMPLETED' and outcome['remoteReceiptAcknowledged'] is True,
                'CAMPAIGN_TRIPLET_COMPLETION_REQUIRED')
        journal_dir = plan.roots['journals'] / mapping['attemptId']
        identity = {k: mapping[k] for k in ('jobId','attemptId','rootId','binding','manifestSha256')}
        journal = AttemptJournal(journal_dir, identity)
        receipt = journal.queue_receipt(1)
        require(receipt['stage'] == 'COMPLETED' and receipt['result']['qualityCounts']['incomplete'] == 0
                and receipt['result']['qualityCounts']['measured'] > 0, 'CAMPAIGN_TRIPLET_INCOMPLETE_REPORT')
        supervisor = journal_dir / 'supervisor'
        created, created_sha = read_json(supervisor / 'process-created.json')
        closed, closed_sha = read_json(supervisor / 'owned-process-closed.json')
        terminal, terminal_sha = read_json(supervisor / 'native-terminal.json')
        retained_outcome, outcome_sha = read_json(supervisor / 'outcome.json')
        require(type(created['pid']) is int and created['pid'] > 0 and closed['pid'] == created['pid']
                and type(closed['exitCode']) is int and terminal['state'] == 'COMPLETED'
                and terminal['operationRef'] == plan.value['operationRef'] and retained_outcome == outcome,
                'CAMPAIGN_TRIPLET_STOP_UNCONFIRMED')
        stop_sha = write_new(self.directory / 'frames' / (str(ordinal) + '-stop-evidence.json'), {
            'protocol': 'DSG_CAMPAIGN_LOCAL_STOP_EVIDENCE_V1', 'mappingSha256': adapter.mapping_sha,
            'jobId': mapping['jobId'], 'attemptId': mapping['attemptId'],
            'processCreatedSha256': created_sha, 'ownedProcessClosedSha256': closed_sha,
            'nativeTerminalSha256': terminal_sha, 'supervisorOutcomeSha256': outcome_sha,
            'reportSha256': receipt['result']['reportSha256'],
            'processStoppedReported': True, 'nativeStoppedAttested': False,
            'scientificValidation': 'NOT_VALIDATED'})
        return mapping, receipt['result']['reportSha256'], stop_sha

    def _execute_frame(self, ordinal, plan, frame_dir, worker_transport, intent_sha, spawn, clock, sleep):
        value = plan.value; binding = value['binding']
        reservation = {k: value[k] for k in ('workerId','rootId','jobId','reservationRef')}
        reservation['bindingRef'] = binding['bindingRef']
        adapter = CampaignReservationAdapter.prepare(self.directory / 'adapters', worker_transport,
            self.context['planRef'], intent_sha, ordinal, value['reservationRef'], reservation,
            binding, value['manifestSha256'], value['operationRef'])
        self.consumed_ordinals.add(ordinal)
        outcome = plan.run_selected(adapter, native_launch_authorized=True, spawn=spawn, clock=clock, sleep=sleep)
        mapping, report_sha, stop_sha = self._stop_evidence(ordinal, plan, adapter, outcome)
        body = {'decisionId': value['operationRef'], 'admissionSha256': mapping['admissionSha256'],
                'jobId': mapping['jobId'], 'attemptId': mapping['attemptId'], 'reportSha256': report_sha,
                'nativeStopEvidenceSha256': stop_sha, 'technicalState': 'COMPLETED', 'processStoppedReported': True}
        self.verify()
        write_new(frame_dir / 'closure-intent.json', body)
        response = worker_transport.request(BASE + self.context['planRef'] + '/frame-closures', body)
        fields(response, {'protocol','closureSha256','admissionSha256','status',
                          'nativeStoppedAttested','scientificValidation'})
        require(response['protocol'] == 'DSG_CAMPAIGN_FRAME_CLOSURE_RECEIPT_V1'
                and digest(response['closureSha256']) and response['admissionSha256'] == mapping['admissionSha256']
                and response['status'] == 'COMPLETED' and response['nativeStoppedAttested'] is False
                and response['scientificValidation'] == 'NOT_VALIDATED', 'CAMPAIGN_TRIPLET_CLOSURE_ACK')
        write_new(frame_dir / 'closure-ack.json', response)

    def _complete(self, intent_sha):
        write_new(self.directory / 'completed.json', {'intentSha256': intent_sha, 'completedFrames': 3,
                  'qualifiedControls': 0, 'scientificValidation': 'NOT_VALIDATED', 'implicitReplay': False})
        self.phase = 'COMPLETED'
        return {'state': self.phase, 'completedFrames': 3, 'qualifiedControls': 0, 'scientificValidation': 'NOT_VALIDATED'}

    def _unconfirmed(self):
        self.phase = 'RECONCILIATION_REQUIRED'
        try: write_new(self.directory / 'unconfirmed.json', {'state': self.phase, 'implicitReplay': False,
                       'nativeStoppedAttested': False, 'scientificValidation': 'NOT_VALIDATED'})
        except (OSError, ProtocolError): pass

    def run_worker(self, handoff, worker_transport, *, native_launch_authorized=False,
                   spawn=None, clock=time.monotonic, sleep=time.sleep):
        """Worker-only entry: no Owner operation, transport, file authority or token."""
        require(native_launch_authorized is True and self.phase == 'REGISTERED', 'CAMPAIGN_TRIPLET_WORKER_ONCE')
        self.phase = 'DISPATCHING'
        try:
            self.verify(); self._verify_registration(); handoff = validate_handoff(handoff)
            request = self.selection['request']
            require(all(handoff[k] == expected for k, expected in {
                'planRef': self.context['planRef'], 'contextSha256': self.context['contextSha256'],
                'archiveSha256': self.archive.sha, 'workerId': request['workerId'], 'rootId': request['rootId']}.items()),
                'CAMPAIGN_TRIPLET_HANDOFF_MISMATCH')
            for ordinal, (job, plan, frame) in enumerate(zip(handoff['jobs'], self.plans, self.context['frames'])):
                value = plan.value
                require(job['jobId'] == value['jobId'] and job['requestId'] == value['jobId'][4:]
                        and job['bindingRef'] == value['binding']['bindingRef']
                        and job['bindingSha256'] == fingerprint(value['binding'])
                        and job['inputSha256'] == frame['sha256'], 'CAMPAIGN_TRIPLET_HANDOFF_BINDING')
            # Consumed before any GET: observation failure never permits replay.
            write_new(self.directory / 'launch-intent.json', {'selectionSha256': self.selection_sha,
                      'handoffSha256': handoff['handoffSha256'], 'nativeLaunchAuthorized': True,
                      'maxSequentialStarts': 3, 'implicitReplay': False})
            inspect_remote(handoff, worker_transport)
            for ordinal, plan in enumerate(self.plans):
                self.verify()
                path = BASE + handoff['planRef'] + '/dispatch-intents/' + handoff['intentSha256'] + \
                       '/jobs/' + str(ordinal) + '/technical-context'
                compare_technical(handoff, worker_transport.request(path), ordinal)
                frame_dir = self.directory / 'frames' / str(ordinal); frame_dir.mkdir()
                self._execute_frame(ordinal, plan, frame_dir, worker_transport, handoff['intentSha256'], spawn, clock, sleep)
            return self._complete(handoff['intentSha256'])
        except BaseException:
            self._unconfirmed()
            raise ProtocolError('CAMPAIGN_TRIPLET_WORKER_UNCONFIRMED_NO_REPLAY') from None

    def run(self, owner_transport, worker_transport, *, native_launch_authorized=False,
            spawn=None, clock=time.monotonic, sleep=time.sleep):
        require(native_launch_authorized is True and self.phase == 'PREPARED', 'CAMPAIGN_TRIPLET_EXPLICIT_ONCE')
        self.phase = 'DISPATCHING'
        try:
            self.verify()
            write_new(self.directory / 'launch-intent.json', {'selectionSha256': self.selection_sha,
                      'nativeLaunchAuthorized': True, 'maxSequentialStarts': 3, 'implicitReplay': False})
            owner = CampaignOwnerOperations(self.directory / 'owner', owner_transport, self.context['planRef'])
            request = self.selection['request']
            intent = owner.prepare_intent(request['decisionId'], request)
            intent_sha = intent['sha256']
            for ordinal, plan in enumerate(self.plans):
                self.verify(); value = plan.value
                # Registration is an explicit durable mutation; no credential or
                # binding may be inferred from the projection response.
                frame_dir = self.directory / 'frames' / str(ordinal); frame_dir.mkdir()
                binding = copy.deepcopy(value['binding'])
                write_new(frame_dir / 'register-intent.json', {'binding': binding, 'implicitRetry': False})
                registered = worker_transport.request('/v1/transient-analysis/worker/register', binding)
                require(registered == binding, 'CAMPAIGN_TRIPLET_REGISTER_ACK')
                write_new(frame_dir / 'register-ack.json', {'binding': binding})
                owner.project(value['reservationRef'], intent_sha, ordinal, value['jobId'][4:], binding)
                self._execute_frame(ordinal, plan, frame_dir, worker_transport, intent_sha, spawn, clock, sleep)
                # Only an acknowledged closure permits the next ordinal.
            return self._complete(intent_sha)
        except BaseException:
            self._unconfirmed()
            raise ProtocolError('CAMPAIGN_TRIPLET_UNCONFIRMED_NO_REPLAY') from None
