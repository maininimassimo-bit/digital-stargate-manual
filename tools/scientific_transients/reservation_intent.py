"""Durable single selected-job reservation intent. No credentials on disk or replay after restart."""
import copy
import datetime as dt

from tools.pixinsight.local_pilot.broker import require, opaque, ProtocolError
from tools.scientific_transients.attempt_journal import identity, write_new, read_json
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.native_aperture import ENGINE, CATALOG
from tools.scientific_transients.native_supervisor import inspect_registered_prepared_run
from tools.scientific_transients.local_driver import LocalDriver
from tools.scientific_transients.queue import BINDING_FIELDS, fields, digest, LEASE_SECONDS

JOB_FIELDS = {'jobId', 'request', 'binding', 'state', 'cancelRequested', 'sequence', 'result', 'reviews',
              'createdAt', 'updatedAt', 'rootId', 'attemptId', 'leaseToken', 'leaseIssuedAt', 'leaseExpiresAt',
              'executionEvidence', 'scientificValidation', 'detailsLocation', 'publication'}


class ReservationIntent:
    @classmethod
    def prepare(cls, registry, root, worker_id, root_id, job_id, reservation_ref, binding,
                manifest_sha256, directory, operation_ref, *, engine=ENGINE, catalog=CATALOG):
        fields(binding, BINDING_FIELDS)
        require(all(opaque(v) for v in binding.values()) and digest(manifest_sha256), 'RESERVATION_BINDING')
        require(all(opaque(v) for v in [worker_id, root_id, reservation_ref, operation_ref])
                and type(job_id) is str and job_id.startswith('TRN_') and opaque(job_id[4:]), 'RESERVATION_ID')
        root, directory = safe_path(root), safe_path(directory)
        require(root.is_dir(), 'RESERVATION_ROOT')
        for other in [registry.artifacts, registry.registry]:
            require(root != other and root not in other.parents and other not in root.parents,
                    'RESERVATION_ROOT_OVERLAP')
        inspect_registered_prepared_run(registry, directory, operation_ref, binding, manifest_sha256,
                                        engine=engine, catalog=catalog)
        destination = root / reservation_ref; destination.mkdir()
        result = cls.__new__(cls)
        result.registry, result.directory, result.records, result.root = registry, directory, destination, root
        result.binding, result.manifest_sha = copy.deepcopy(binding), manifest_sha256
        result.engine, result.catalog, result.operation = engine, catalog, operation_ref
        result.request = {'workerId':worker_id, 'rootId':root_id, 'jobId':job_id,
                          'bindingRef':binding['bindingRef'], 'reservationRef':reservation_ref}
        result.phase, result.lease, result.reserved_identity = 'PREPARED', None, None
        result.request_sha = write_new(destination / 'request.json', result.request)
        result.expectation_sha = write_new(destination / 'expectation.json', {'binding':result.binding,
                              'manifestSha256':manifest_sha256, 'operationRef':operation_ref, 'implicitReplay':False})
        result.marker_sha = write_new(directory / 'reservation-intent.json',
                                     {'reservationRef':reservation_ref, 'requestSha256':result.request_sha})
        return result

    def _verify_intent(self):
        require(read_json(self.records / 'request.json')[1] == self.request_sha
                and read_json(self.records / 'expectation.json')[1] == self.expectation_sha
                and read_json(self.directory / 'reservation-intent.json')[1] == self.marker_sha,
                'RESERVATION_INTENT_CHANGED')
        inspect_registered_prepared_run(self.registry, self.directory, self.operation, self.binding,
                                        self.manifest_sha, engine=self.engine, catalog=self.catalog)

    def _freeze(self):
        self.phase, self.lease = 'RECONCILIATION_REQUIRED', None
        try:
            write_new(self.records / 'failed.json', {'state':self.phase, 'nativeLaunchRequested':False,
                      'implicitReplay':False, 'leasePersisted':False})
        except OSError:
            pass  # Existing/partial files remain; no exception detail or secret is persisted.

    def reserve(self, transport):
        require(self.phase == 'PREPARED', 'RESERVATION_REPLAY_REFUSED')
        self.phase = 'DISPATCHING'  # Freeze before any persistence/network uncertainty.
        try:
            self._verify_intent()
            write_new(self.records / 'dispatch-intent.json', {'requestSha256':self.request_sha, 'implicitRetry':False})
            response = transport.request('/v1/transient-analysis/worker/reserve', self.request)
            fields(response, {'disposition', 'job'})
            if response['disposition'] == 'RECONCILIATION_REQUIRED':
                require(response['job'] is None, 'RESERVATION_EXISTING_LEASE_REFUSED')
                self._freeze()
                return {'state':self.phase, 'nativeLaunchRequested':False}
            require(response['disposition'] == 'CREATED', 'RESERVATION_RESPONSE')
            job = response['job']; fields(job, JOB_FIELDS)
            fields(job['request'], {'requestId','bindingRef'})
            require(job['jobId'] == self.request['jobId'] and job['rootId'] == self.request['rootId']
                    and job['binding'] == self.binding and opaque(job['attemptId']) and digest(job['leaseToken'])
                    and job['request'] == {'requestId':job['jobId'][4:], 'bindingRef':self.binding['bindingRef']},
                    'RESERVATION_RESPONSE_IDENTITY')
            require(job['state'] == 'RESERVED' and job['cancelRequested'] is False
                    and type(job['sequence']) is int and job['sequence'] == 0
                    and job['result'] is None and job['reviews'] == []
                    and job['executionEvidence'] == 'WORKER_REPORTED_NOT_ATTESTED'
                    and job['scientificValidation'] == 'NOT_VALIDATED'
                    and job['detailsLocation'] == 'OWNER_PC' and job['publication'] == 'NONE', 'RESERVATION_RESPONSE_STATE')
            times = [dt.datetime.fromisoformat(job[key]) for key in ['createdAt','updatedAt','leaseIssuedAt','leaseExpiresAt']]
            require(all(t.tzinfo is not None and t.utcoffset() == dt.timedelta(0) for t in times)
                    and times[0] <= times[1] == times[2] and times[3] - times[2] == dt.timedelta(seconds=LEASE_SECONDS),
                    'RESERVATION_RESPONSE_TIME')
            value = {key:copy.deepcopy(job[key]) for key in ['jobId','attemptId','rootId','binding']}
            value['manifestSha256'] = self.manifest_sha; identity(value)
            self.reserved_sha = write_new(self.records / 'reserved.json',
                {'identity':value, 'leasePersisted':False, 'nativeLaunchRequested':False, 'implicitReplay':False})
            self.reserved_identity, self.lease, self.phase = value, job['leaseToken'], 'RESERVED'
            return {'state':self.phase, 'identity':copy.deepcopy(value), 'nativeLaunchRequested':False}
        except Exception:
            self._freeze()
            raise ProtocolError('RESERVATION_UNCONFIRMED_NO_REPLAY') from None

    def prepare_driver(self, journal_root, outbox_root, transport, *, supervisor_options=None, **driver_options):
        require(self.phase == 'RESERVED', 'RESERVATION_REPLAY_REFUSED')
        self.phase = 'PREPARING_DRIVER'
        try:
            for target in [safe_path(journal_root), safe_path(outbox_root)]:
                require(target != self.root and target not in self.root.parents and self.root not in target.parents,
                        'RESERVATION_DRIVER_ROOT_OVERLAP')
            self._verify_intent()
            require(read_json(self.records / 'reserved.json')[1] == self.reserved_sha,
                    'RESERVATION_RECEIPT_CHANGED')
            options = dict(supervisor_options or {})
            require('engine' not in options and 'catalog' not in options, 'RESERVATION_RUNTIME_CONFLICT')
            options.update(engine=self.engine, catalog=self.catalog)
            driver = LocalDriver.prepare(self.registry, journal_root, outbox_root, self.reserved_identity,
                self.directory, self.operation, transport, self.lease, supervisor_options=options, **driver_options)
            write_new(self.records / 'driver-prepared.json', {'attemptId':self.reserved_identity['attemptId'],
                      'nativeLaunchRequested':False, 'implicitReplay':False})
            self.phase, self.lease = 'DRIVER_PREPARED', None
            return driver  # Caller must invoke start explicitly; this method never launches.
        except Exception:
            self._freeze()
            raise ProtocolError('RESERVATION_DRIVER_UNCONFIRMED_NO_REPLAY') from None
