"""One-shot cooperative cancel and truthful uncertainty records; no process control."""
import re
import stat

from tools.pixinsight.local_pilot.broker import encode, require
from tools.scientific_transients import native_publication as pub
from tools.scientific_transients.native_held_process import HeldNativeProcess
from tools.scientific_transients.native_run_records import NativeRunRecords


def _metadata_bytes(root):
    total=0; count=0; pending=[(root,0)]
    while pending:
        directory,depth=pending.pop()
        require(depth<=8,'SUPERVISION_METADATA_DEPTH')
        for path in directory.iterdir():
            count+=1; require(count<=256,'SUPERVISION_METADATA_ENTRIES')
            path=pub.safe_path(path); info=path.lstat()
            if stat.S_ISDIR(info.st_mode): pending.append((path,depth+1))
            else:
                require(stat.S_ISREG(info.st_mode) and info.st_nlink==1,'SUPERVISION_METADATA_FILE')
                total+=info.st_size
                require(total<=16*pub.MIB,'SUPERVISION_METADATA_AGGREGATE')
    return total


class NativeSupervisionSignals:
    """Attach once to the original records object, before any attempted process start.

    The future supervisor owns consent, state and this live object. On clock/code
    failure, these stop-only writes may still be attempted in the original private
    directories; they never authorize computation, process closure or replay.
    """
    def __init__(self,records):
        require(type(records) is NativeRunRecords,'SUPERVISION_SIGNALS_CONTEXT')
        require(not getattr(records,'_signals_attached',False),'SUPERVISION_SIGNALS_RECONSTRUCTION')
        records._signals_attached=True
        self._records=records; self._held=None; self._adopt_attempted=False
        self._cancel_attempted=False; self._cancel_committed=False
        self._uncertainty_attempted=False; self._uncertainty_committed=False
        self._live_uncertain=False; self._pins=[]

    def _fail(self):
        self._live_uncertain=True; self._records._failed=True

    def _roots(self):
        r=self._records
        require([pub._directory(p) for p,_ in r._roots]==r._roots,'SUPERVISION_SIGNALS_ROOT_CHANGED')
        return _metadata_bytes(r._journal)

    def _verify_pins(self):
        for path,sha,info in self._pins:
            require(pub._hash_bounded(path,info.st_size,info)==sha,'SUPERVISION_SIGNALS_PIN_CHANGED')

    def _write(self,path,value):
        size=self._roots()
        raw=encode(value); require(len(raw)<=pub.MIB,'SUPERVISION_SIGNALS_RECORD_SIZE')
        if path.parent==self._records._journal:
            require(size+len(raw)<=16*pub.MIB,'SUPERVISION_METADATA_AGGREGATE')
        sha,info=pub._write_control(path,value)
        self._pins.append((path,sha,info))
        self._roots()
        require(pub._hash_bounded(path,info.st_size,info)==sha,'SUPERVISION_SIGNALS_PIN_CHANGED')
        self._roots()
        return sha

    def verify_records(self):
        """Read-only integrity check; failure does not prevent later stop-only writes."""
        try: self._roots(); self._verify_pins(); self._roots()
        except BaseException:
            self._fail()
            raise

    def adopt_held(self,held):
        require(not self._adopt_attempted,'SUPERVISION_SIGNALS_ADOPT_REPLAY')
        self._adopt_attempted=True; self._held=held
        try:
            require(type(held) is HeldNativeProcess and self._records._start_sha is not None,
                    'SUPERVISION_SIGNALS_HELD_CONTEXT')
            require(self._records._held is None or self._records._held is held,'SUPERVISION_SIGNALS_HELD_CHANGED')
        except BaseException:
            self._fail()
            raise

    def request_cancel(self):
        require(not self._cancel_attempted,'SUPERVISION_CANCEL_REPLAY')
        self._cancel_attempted=True
        try:
            value=dict(protocol='DSG_NATIVE_LINEAR_CANCEL_V1',
                operationRef=self._records._binding['operationRef'],requested=True)
            sha=self._write(self._records._work/'cancel.json',value)
            self._cancel_committed=True
            return {'cancelSha256':sha,'processStopVerified':False,'newNativeStartAllowed':False}
        except BaseException:
            self._fail()
            raise

    def mark_uncertain(self,reason):
        require(not self._uncertainty_attempted,'SUPERVISION_UNCERTAINTY_REPLAY')
        self._uncertainty_attempted=True; self._fail()
        try:
            require(type(reason) is str and re.fullmatch('[A-Z0-9_]{1,96}',reason),'SUPERVISION_UNCERTAINTY_REASON')
            r=self._records
            if r._held is not None:
                require(type(r._held) is HeldNativeProcess and (self._held is None or self._held is r._held),
                        'SUPERVISION_SIGNALS_HELD_CHANGED')
                self._held=r._held; self._adopt_attempted=True
            observation,code='NO_HANDLE_AMBIGUOUS',None
            if self._held is not None:
                require(type(self._held) is HeldNativeProcess,'SUPERVISION_SIGNALS_HELD_CONTEXT')
                # A failed poll cannot truthfully be serialized as running/exited.
                # Keep live uncertainty and raise rather than inventing an observation.
                observed=self._held.observe()
                observation,code=observed['processObservation'],observed['exitCode']
                require(observation in {'HELD_RUNNING','HELD_EXITED'} and
                        (code is None if observation=='HELD_RUNNING' else type(code) is int),
                        'SUPERVISION_UNCERTAINTY_OBSERVATION')
            value=dict(protocol='DSG_NATIVE_LINEAR_SUPERVISION_UNCERTAIN_V1',
                operationRef=r._binding['operationRef'],processSessionRef=r._control['processSessionRef'],
                parentIntentSha256=r._binding['parentIntentSha256'],startConsumedSha256=r._start_sha,
                reason=reason,processObservation=observation,exitCode=code,launchCountBound=1,
                newNativeStartAllowed=False)
            sha=self._write(r._journal/'supervision-uncertain.json',value)
            self._uncertainty_committed=True
            return {'uncertaintySha256':sha,'newNativeStartAllowed':False,'processClosureAuthorized':False}
        except BaseException:
            self._fail()
            raise

    def diagnostic(self):
        return {'liveUncertain':self._live_uncertain,'cancelAttemptConsumed':self._cancel_attempted,
                'cancelCommitted':self._cancel_committed,'uncertaintyAttemptConsumed':self._uncertainty_attempted,
                'uncertaintyCommitted':self._uncertainty_committed,
                'processReferenceRetained':type(self._held) is HeldNativeProcess or type(self._records._held) is HeldNativeProcess,
                'newNativeStartAllowed':False,'processClosureAuthorized':False}
