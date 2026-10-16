"""Same-parent V5 linear lifecycle composition; no CLI, cloud or consent factory.

The future preparer must supply original records/locks after fresh human consent,
with the original budget created before preparation IO. No persisted recovery.
"""
import os
import re
import subprocess

from tools.pixinsight.local_pilot.broker import ProtocolError, require
from tools.scientific_transients import native_publication as pub
from tools.scientific_transients.native_held_process import HeldNativeProcess
from tools.scientific_transients.native_owned_closure import OwnedNativeClosure
from tools.scientific_transients.native_read_locks import NativeReadLocks
from tools.scientific_transients.native_retained_verification import RetainedRunVerification
from tools.scientific_transients.native_run_records import NativeRunRecords
from tools.scientific_transients.native_supervision_signals import NativeSupervisionSignals


def _spawn_native(executable,entry,work):
    require(os.name=='nt','LINEAR_SUPERVISOR_WINDOWS_REQUIRED')
    startup=subprocess.STARTUPINFO()
    startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow=subprocess.SW_HIDE
    return subprocess.Popen([str(executable),'-n','--automation-mode','--no-startup-scripts',
        '--no-startup-check-updates','-r='+str(entry)],cwd=work,startupinfo=startup,
        shell=False,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)


def _acquire_owner_locks(rows,guard):
    return NativeReadLocks(rows,guard=guard)


class LinearNativeSupervisor:
    """Monouse original objects only. Construction is NOT authorization to start.

    The enclosing reviewed preparer/driver authenticates fresh scoped consent and
    constructs the private entry, source closure, seal and grant. This component
    neither reconstructs them nor schedules ticks or native runs by itself.
    """
    def __init__(self,records,signals,static_locks):
        self._records=records; self._signals=signals; self._locks=list(static_locks) if type(static_locks) in {list,tuple} else []
        self._state='PREPARING'; self._process=None; self._held=None; self._owner_locks=None
        self._start_attempted=False; self._publication_attempted=False
        self._publication=None; self._proof=None; self._closer=None; self._closure=None
        self._last_observation=None; self._last_error=None
        require(type(records) is NativeRunRecords and type(signals) is NativeSupervisionSignals
                and signals._records is records,'LINEAR_SUPERVISOR_ORIGINAL_CONTEXT')
        try:
            require(not getattr(records,'_linear_supervisor_attached',False),'LINEAR_SUPERVISOR_RECONSTRUCTION')
            records._linear_supervisor_attached=True
            require(not records._consume_attempted and not records._owner_attempted and
                    records._start_sha is None and records._held is None and signals._held is None,
                    'LINEAR_SUPERVISOR_PRIOR_ATTEMPT')
            require(1<=len(self._locks)<=2 and all(type(g) is NativeReadLocks for g in self._locks),
                    'LINEAR_SUPERVISOR_STATIC_LOCKS')
            records.verify(); self._verify_locks(); records._budget.require_running()
            self._state='PREPARED_LIVE'
        except BaseException as exc:
            self._uncertain(exc)
            raise

    def _expected_locks(self):
        r=self._records
        rows={path:(row['sha256'],row['byteLength']) for path,row,_ in r._pins if path.parent==r._work}
        for role in ['ENTRY','LAUNCHER']:
            row=next(v for v in r._control['files'] if v['role']==role)
            path=pub.safe_path(row['path']); require(path not in rows,'LINEAR_SUPERVISOR_CODE_ALIAS')
            rows[path]=(row['sha256'],row['byteLength'])
        return rows

    def _verify_locks(self):
        rows={}
        for group in self._locks:
            require(type(group) is NativeReadLocks and not group._released,'LINEAR_SUPERVISOR_RELEASED_LOCK')
            group.verify()
            for _,path,row,_ in group._held:
                require(path not in rows,'LINEAR_SUPERVISOR_DUPLICATE_LOCK')
                rows[path]=(row['sha256'],row['byteLength'])
        require(rows==self._expected_locks(),'LINEAR_SUPERVISOR_LOCK_COVERAGE')

    def _guard(self):
        r=self._records
        require(not r._failed and not self._signals.diagnostic()['liveUncertain'],
                'LINEAR_SUPERVISOR_OBSERVED_UNCERTAINTY')
        r._budget.check(); r._session.assert_intact(); self._signals.verify_records()
        require([pub._directory(p) for p,_ in r._roots]==r._roots,'LINEAR_SUPERVISOR_ROOT_CHANGED')
        for path in [r._work/'native-publication-uncertain.json',r._journal/'publication-uncertain.json',
                     r._journal/'supervision-uncertain.json',r._journal/'owned-closure.json']:
            require(not os.path.lexists(path),'LINEAR_SUPERVISOR_FENCE')
        for path,row,info in r._pins:
            require(pub._hash_bounded(path,row['byteLength'],info)==row['sha256'],'LINEAR_SUPERVISOR_RECORD_CHANGED')
        self._verify_locks()
        if self._held is not None:
            require(r._held is self._held and self._signals._held is self._held
                    and self._held.identity()==r._held_identity,'LINEAR_SUPERVISOR_HELD_CHANGED')
        r._budget.check()
        require(not r._failed and not self._signals.diagnostic()['liveUncertain'],
                'LINEAR_SUPERVISOR_OBSERVED_UNCERTAINTY')
        require([pub._directory(p) for p,_ in r._roots]==r._roots,'LINEAR_SUPERVISOR_ROOT_CHANGED')
        for path in [r._work/'native-publication-uncertain.json',r._journal/'publication-uncertain.json',
                     r._journal/'supervision-uncertain.json',r._journal/'owned-closure.json']:
            require(not os.path.lexists(path),'LINEAR_SUPERVISOR_FENCE')

    def _observe(self):
        if self._held is not None:
            self._last_observation=self._held.observe()
        return self._last_observation

    def _uncertain(self,exc):
        self._signals._fail()
        if self._last_error is None:
            code=str(exc) if isinstance(exc,ProtocolError) else 'LINEAR_SUPERVISOR_FAILURE'
            self._last_error=code if re.fullmatch('[A-Z0-9_]{1,96}',code) else 'LINEAR_SUPERVISOR_FAILURE'
        self._state='UNCERTAIN_HELD'
        if self._closer is not None and self._closer.diagnostic()['processExitObserved']:
            self._state='EXIT_VERIFIED_EVIDENCE_UNCERTAIN'
        try:
            observed=self._observe()
            if observed is not None and observed['processObservation']=='HELD_EXITED':
                self._state='EXIT_VERIFIED_EVIDENCE_UNCERTAIN'
        except BaseException: pass
        # Stop-only writes are each consumed before IO. No per-poll growth/retry.
        if not self._signals.diagnostic()['cancelAttemptConsumed']:
            try: self._signals.request_cancel()
            except BaseException: pass
        if not self._signals.diagnostic()['uncertaintyAttemptConsumed']:
            try: self._signals.mark_uncertain(self._last_error)
            except BaseException: pass

    def start(self):
        require(not self._start_attempted and self._state=='PREPARED_LIVE','LINEAR_SUPERVISOR_START_REPLAY')
        self._start_attempted=True
        try:
            r=self._records
            r.verify(); self._verify_locks(); r._budget.require_running()
            r.consume(r._budget._last_wall.strftime('%Y-%m-%dT%H:%M:%SZ'))
            self._state='START_CONSUMED'
            r.verify(); self._verify_locks(); r._budget.require_running()
            fixed={v['role']:v for v in r._control['files'] if v['role']!='PARENT_SOURCE'}
            executable=pub.safe_path(fixed['EXECUTABLE']['path']); entry=pub.safe_path(fixed['ENTRY']['path'])
            r._budget.require_running(); r._session.assert_intact(); self._signals.verify_records()
            require(not r._failed and not self._signals.diagnostic()['liveUncertain'],
                    'LINEAR_SUPERVISOR_OBSERVED_UNCERTAINTY')
            require([pub._directory(p) for p,_ in r._roots]==r._roots,'LINEAR_SUPERVISOR_ROOT_CHANGED')
            for path in [r._work/'cancel.json',r._work/'native-publication-uncertain.json',
                         r._journal/'publication-uncertain.json',r._journal/'supervision-uncertain.json',
                         r._journal/'publication-intent.json',r._journal/'owned-closure.json']:
                require(not os.path.lexists(path),'LINEAR_SUPERVISOR_PRESPAWN_FENCE')
            # Assignment precedes every identity query, persistence and diagnostic.
            self._process=_spawn_native(executable,entry,r._work)
            self._held=HeldNativeProcess(self._process)
            self._signals.adopt_held(self._held)
            self._held.capture()
            r.write_owner(self._held)
            owner_rows=[dict(path=p.as_posix(),sha256=row['sha256'],byteLength=row['byteLength'])
                        for p,row,_ in r._pins if p.parent==r._work and
                        p.name in {'native-owner.json','native-owner-ready.json'}]
            def observer_guard(): r._budget.check(); r._session.assert_intact()
            self._owner_locks=_acquire_owner_locks(owner_rows,observer_guard)
            self._locks.append(self._owner_locks)
            self._guard(); self._state='RUNNING_HELD'
            budget=r._budget.diagnostic()
            if budget['parentMonotonicDeadlineExceeded'] or budget['parentWallDeadlineExceeded']:
                self._state='RETENTION_ONLY'; self._signals.request_cancel()
            return self.diagnostic()
        except BaseException as exc:
            self._uncertain(exc)
            raise

    def tick(self,*,cancel=False):
        require(type(cancel) is bool,'LINEAR_SUPERVISOR_CANCEL_TYPE')
        if self._state=='CLOSED_RETAINED': return self.diagnostic()
        if self._state in {'UNCERTAIN_HELD','EXIT_VERIFIED_EVIDENCE_UNCERTAIN'}:
            try:
                observed=self._observe()
                if observed is not None and observed['processObservation']=='HELD_EXITED':
                    self._state='EXIT_VERIFIED_EVIDENCE_UNCERTAIN'
            except BaseException as exc:
                self._uncertain(exc)
                raise
            return self.diagnostic()
        try:
            r=self._records
            require(not r._failed and not self._signals.diagnostic()['liveUncertain'],
                    'LINEAR_SUPERVISOR_OBSERVED_UNCERTAINTY')
            budget=r._budget.check()
            if cancel or budget['parentMonotonicDeadlineExceeded'] or budget['parentWallDeadlineExceeded']:
                self._state='RETENTION_ONLY'
                if not self._signals.diagnostic()['cancelAttemptConsumed']: self._signals.request_cancel()
            if self._held is None: return self.diagnostic()
            self._guard(); observed=self._observe()
            require(observed['identityTrusted'] is True,'LINEAR_SUPERVISOR_IDENTITY_UNCERTAIN')
            if not os.path.lexists(r._work/'native-return.json'):
                require(observed['processObservation']!='HELD_EXITED','LINEAR_SUPERVISOR_RETURN_MISSING_AFTER_EXIT')
                return self.diagnostic()
            require(not self._publication_attempted,'LINEAR_SUPERVISOR_PUBLICATION_REPLAY')
            self._publication_attempted=True
            self._publication=pub.publish_native_bundle(r._work,r._retained,r._journal,r._binding,
                clock=r._budget.publication_clock,deadline=r._budget.deadline_monotonic,bootstrap_session=r._session)
            self._proof=RetainedRunVerification(r,self._signals,self._publication,self._locks)
            self._closer=OwnedNativeClosure(self._proof)
            self._closure=self._closer.close()
            self._state='CLOSED_RETAINED'
            return self.diagnostic()
        except BaseException as exc:
            self._uncertain(exc)
            raise

    def diagnostic(self):
        observed=self._last_observation or {}
        closer=self._closer.diagnostic() if self._closer is not None else {}
        return {'state':self._state,'startAttemptConsumed':self._start_attempted,
                'popenReferenceRetained':self._process is not None,'heldReferenceRetained':self._held is not None,
                'publicationAttemptConsumed':self._publication_attempted,
                'processExitObserved':closer.get('processExitObserved',False) or observed.get('processObservation')=='HELD_EXITED',
                'exitCode':closer.get('exitCode') if closer.get('processExitObserved') else observed.get('exitCode'),
                'closureReceiptCommitted':self._closure is not None,'lastError':self._last_error,
                'newNativeStartAllowed':False,'measurementAccepted':False,'scientificValidation':'NOT_VALIDATED',
                'qualifiedControls':0}
