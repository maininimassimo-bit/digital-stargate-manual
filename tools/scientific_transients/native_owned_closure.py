"""Owned post-retention exit and exclusive S7 receipt. No entry point or launcher.

The future reviewed supervisor may call this only in its original freshly
authorized run. Constructing this helper grants no authority to execute it.
"""
import ctypes
import os

from tools.pixinsight.local_pilot.broker import encode, require
from tools.scientific_transients import native_publication as pub
from tools.scientific_transients.native_retained_verification import RetainedRunVerification


class _WindowsOwnedExit:
    def __init__(self):
        require(os.name=='nt','OWNED_EXIT_WINDOWS_REQUIRED')
        self.dll=ctypes.WinDLL('kernel32',use_last_error=True)
        self.dll.WaitForSingleObject.argtypes=[ctypes.c_void_p,ctypes.c_uint32]
        self.dll.WaitForSingleObject.restype=ctypes.c_uint32
        self.dll.TerminateProcess.argtypes=[ctypes.c_void_p,ctypes.c_uint32]
        self.dll.TerminateProcess.restype=ctypes.c_int

    def wait(self,handle,milliseconds):
        status=self.dll.WaitForSingleObject(handle,milliseconds)
        if status==0xffffffff: raise ctypes.WinError(ctypes.get_last_error())
        require(status in {0,258},'OWNED_EXIT_WAIT_RESULT')
        return status==0

    def terminate(self,handle):
        # Only after an actual causal return and all retained/live proof gates.
        if not self.dll.TerminateProcess(handle,0): raise ctypes.WinError(ctypes.get_last_error())


class OwnedNativeClosure:
    """Monouse closure of the same retained handle, never Popen.terminate/wait.

    Source preparation is not fresh execution consent. The enclosing supervisor
    owns that gate, prestart provenance, state and all original live objects.
    Neither a persisted marker nor a reconstructed PID is accepted as context.
    """
    def __init__(self,proof):
        self._proof=proof; self._attempted=False; self._termination_attempted=False
        self._exit_observed=False; self._exit_code=None; self._receipt=None
        self._cancel_pin=None
        self._state='READY_NO_ACTION'; self._failed=False
        require(type(proof) is RetainedRunVerification,'OWNED_EXIT_LIVE_PROOF')
        self._records=proof._records; self._signals=proof._signals; self._held=self._records._held
        try:
            require(not getattr(self._records,'_owned_closure_attached',False),'OWNED_EXIT_RECONSTRUCTION')
            self._records._owned_closure_attached=True
            require(proof.diagnostic()['verified'] and not proof.diagnostic()['verificationFailed'],
                    'OWNED_EXIT_UNVERIFIED_PROOF')
        except BaseException:
            self._fail()
            raise

    def _fail(self):
        self._failed=True; self._signals._fail()
        self._state='EXIT_VERIFIED_EVIDENCE_UNCERTAIN' if self._exit_observed else 'UNCERTAIN_HELD'

    def observe_exit(self):
        """Read-only bounded observation remains possible after any failure."""
        observed=self._held.observe()
        if observed['processObservation']=='HELD_EXITED':
            self._exit_observed=True; self._exit_code=observed['exitCode']
            if self._failed: self._state='EXIT_VERIFIED_EVIDENCE_UNCERTAIN'
        return dict(observed)

    def _observe_trusted(self):
        observed=self.observe_exit()
        require(observed['identityTrusted'] is True,'OWNED_EXIT_IDENTITY_UNCERTAIN')
        return observed

    def _original_handle(self):
        self._held.verify()
        require(self._records._held is self._held and self._signals._held is self._held,
                'OWNED_EXIT_HELD_CHANGED')
        return self._held._handle_value

    def _post_receipt_verify(self,sha,info):
        """Terminal phase: allow ONLY this exact newly committed closure file.

        The preclosure proof deliberately rejects any owned-closure.json. Do not
        reset that guard. Recheck its original pins and live publication here,
        plus the one exclusive terminal receipt, after actual held exit.
        """
        r=self._records; p=self._proof
        def clean():
            require(self._exit_observed and not self._failed and not r._failed
                    and not self._signals.diagnostic()['liveUncertain']
                    and not p.diagnostic()['verificationFailed'],'OWNED_EXIT_UNCERTAIN')
        clean()
        r._budget.check(); r._session.assert_intact(); self._signals.verify_records()
        require([pub._directory(path) for path,_ in r._roots]==r._roots,'OWNED_EXIT_ROOT_CHANGED')
        pub._metadata_bound(r._journal)
        for path in [r._work/'native-publication-uncertain.json',r._journal/'publication-uncertain.json',
                     r._journal/'supervision-uncertain.json']:
            require(not os.path.lexists(path),'OWNED_EXIT_FENCE')
        for path,row,original in r._pins:
            require(pub._hash_bounded(path,row['byteLength'],original)==row['sha256'],'OWNED_EXIT_RECORD_CHANGED')
        for group in p._locks: group.verify()
        p._live.verify()
        self._original_handle()
        require(self._held.identity()==r._held_identity,'OWNED_EXIT_HELD_CHANGED')
        observed=self._observe_trusted()
        require(observed['processObservation']=='HELD_EXITED' and observed['exitCode']==self._exit_code,
                'OWNED_EXIT_NOT_EXITED')
        path=r._journal/'owned-closure.json'
        require(pub._hash_bounded(path,info.st_size,info)==sha,'OWNED_EXIT_RECEIPT_CHANGED')
        r._budget.check(); r._session.assert_intact(); self._signals.verify_records()
        p._live.verify()
        require(pub._hash_bounded(r._journal/'owned-closure.json',info.st_size,info)==sha,
                'OWNED_EXIT_RECEIPT_CHANGED')
        # The last receipt read is itself fallible IO. Recheck original S7 pins
        # and immutable cancel records afterwards, rather than accepting the
        # earlier positive snapshot. Publication also pins an initial cancel
        # created outside the signals writer.
        final_pins=r._pins+([self._cancel_pin] if self._cancel_pin is not None else [])
        for path,row,original in final_pins:
            require(pub._hash_bounded(path,row['byteLength'],original)==row['sha256'],
                    'OWNED_EXIT_RECORD_CHANGED')
        self._signals.verify_records(); p._live.verify()
        r._budget.check()
        # Close the readback boundary with original descriptor identities after
        # all raw hashes/callbacks. No receipt reread after this scan can silently
        # invalidate an earlier pin. This is private/quiescent continuity, not
        # an atomic snapshot against hostile concurrent same-user writes.
        identities=[(path,original) for path,_,original in final_pins]
        identities.extend((path,original) for path,_,original in self._signals._pins)
        identities.append((r._journal/'owned-closure.json',info))
        for path,original in identities:
            with pub.safe_path(path).open('rb') as stream:
                current=os.fstat(stream.fileno())
                require(pub.signature(current)==pub.signature(original) and current.st_nlink==1,
                        'OWNED_EXIT_FINAL_IDENTITY_CHANGED')
            require(pub.signature(current)[:4]==pub.signature(pub.safe_path(path).lstat())[:4],
                    'OWNED_EXIT_FINAL_IDENTITY_CHANGED')
        require([pub._directory(path) for path,_ in r._roots]==r._roots,'OWNED_EXIT_ROOT_CHANGED')
        for path in [r._work/'native-publication-uncertain.json',r._journal/'publication-uncertain.json',
                     r._journal/'supervision-uncertain.json']:
            require(not os.path.lexists(path),'OWNED_EXIT_FENCE')
        require(os.path.lexists(r._work/'cancel.json')==p._last['parentCancelRequested'],
                'OWNED_EXIT_CANCEL_CHANGED')
        clean()

    def close(self):
        require(not self._attempted,'OWNED_EXIT_REPLAY')
        self._attempted=True
        try:
            value=self._proof.verify()
            self._original_handle()
            cancel_path=self._records._work/'cancel.json'
            require(os.path.lexists(cancel_path)==value['parentCancelRequested'],'OWNED_EXIT_CANCEL_CHANGED')
            if value['parentCancelRequested']:
                cancel,row,info=pub._read_control(cancel_path)
                pub._fields(cancel,{'protocol','operationRef','requested'})
                require(cancel['protocol']=='DSG_NATIVE_LINEAR_CANCEL_V1' and cancel['requested'] is True
                        and cancel['operationRef']==self._records._binding['operationRef'],'OWNED_EXIT_CANCEL_RECORD')
                self._cancel_pin=(cancel_path,row,info)
            observed=self._observe_trusted(); method='NATURAL_EXIT'
            if observed['processObservation']=='HELD_RUNNING':
                api=_WindowsOwnedExit()
                # A brief natural wait cannot terminate anything.
                signaled=api.wait(self._original_handle(),1000)
                observed=self._observe_trusted()
                require(not signaled or observed['processObservation']=='HELD_EXITED','OWNED_EXIT_WAIT_DISAGREEMENT')
                if observed['processObservation']=='HELD_RUNNING':
                    # Fresh causal/state/byte/time/fence/lock gates immediately
                    # before the sole termination of the captured original handle.
                    value=self._proof.verify()
                    handle=self._original_handle()
                    self._termination_attempted=True
                    api.terminate(handle)
                    method='OWNED_POST_RETAINED_TERMINATION'
                    require(api.wait(handle,30000),'OWNED_EXIT_TERMINATION_NOT_OBSERVED')
                    observed=self._observe_trusted()
            require(observed['processObservation']=='HELD_EXITED','OWNED_EXIT_NOT_EXITED')
            # Exit is already recorded in private memory, before any further IO.
            value=self._proof.verify()
            self._original_handle()
            budget=self._records._budget.check()
            accepted=(value['conditionalComputationDeclaredComplete'] is True and self._exit_code==0
                and not budget['parentMonotonicDeadlineExceeded'] and not budget['parentWallDeadlineExceeded']
                and not value['nativeCooperativeDeadlineExceeded'] and not value['parentCancelRequested'])
            r=self._records
            receipt=dict(protocol='DSG_NATIVE_LINEAR_OWNED_CLOSURE_V1',
                **{k:r._binding[k] for k in ['operationRef','parentIntentSha256','launchControlSha256','grantSha256']},
                retainedMarkerSha256=value['markerSha256'],nativeReturnSha256=value['nativeReturnSha256'],
                processSessionRef=value['processSessionRef'],processCreationFileTime=value['processCreationFileTime'],
                exitCode=self._exit_code,closeMethod=method,
                parentMonotonicDeadlineExceeded=budget['parentMonotonicDeadlineExceeded'],
                nativeCooperativeDeadlineExceeded=value['nativeCooperativeDeadlineExceeded'],
                technicalComputationAccepted=accepted,scientificValidation='NOT_VALIDATED',qualifiedControls=0)
            require(self._signals._roots()+len(encode(receipt))<=16*pub.MIB,'OWNED_EXIT_METADATA_RESERVE')
            sha,info=pub._write_control(r._journal/'owned-closure.json',receipt)
            self._post_receipt_verify(sha,info)
            after=r._budget.diagnostic()
            require(receipt['parentMonotonicDeadlineExceeded']==after['parentMonotonicDeadlineExceeded'] and
                    (not accepted or not after['parentWallDeadlineExceeded']), 'OWNED_EXIT_DEADLINE_CROSSED_DURING_RECEIPT')
            self._receipt=dict(receipt); self._state='CLOSED_RETAINED'
            return dict(receipt,closureSha256=sha,newNativeStartAllowed=False,measurementAccepted=False)
        except BaseException:
            self._fail()
            # An IO/diagnostic error cannot turn an already observed exit into a
            # claim that the process is alive. No termination/retry follows here.
            try: self.observe_exit()
            except BaseException: pass
            raise

    def diagnostic(self):
        return {'state':self._state,'attemptConsumed':self._attempted,
                'terminationAttempted':self._termination_attempted,'processExitObserved':self._exit_observed,
                'exitCode':self._exit_code,'receiptCommitted':self._receipt is not None,
                'newNativeStartAllowed':False,'processClosureAuthorized':False,'measurementAccepted':False}
