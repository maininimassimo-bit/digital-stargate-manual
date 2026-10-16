"""Exclusive same-attempt records and Owner handshake. Never starts/closes a process."""
import datetime as dt
import os
import re

from tools.pixinsight.local_pilot.broker import encode, require
from tools.scientific_transients import native_publication as pub
from tools.scientific_transients.native_held_process import HeldNativeProcess
from tools.scientific_transients.native_run_budget import LiveNativeBudget


class NativeRunRecords:
    """Future supervisor supplies fresh consent and this one live prepared context.

    Existing records cannot reconstruct an object. Failed operations latch in memory;
    the supervisor must retain this object and block reconstruction/retry after failure.
    """
    def __init__(self, work, retained, supervision, binding, *, bootstrap_session, budget):
        require(type(budget) is LiveNativeBudget, 'RUN_RECORDS_LIVE_BUDGET')
        pub._fields(binding, {'operationRef','parentIntentSha256','launchControlSha256','sealSha256','grantSha256'})
        require(type(binding['operationRef']) is str and re.fullmatch('[a-f0-9]{32}',binding['operationRef'])
                and all(pub._sha(binding[k]) for k in binding if k!='operationRef'), 'RUN_RECORDS_BINDING')
        self._binding=dict(binding); self._budget=budget; self._session=bootstrap_session
        self._pins=[]; self._failed=False; self._consume_attempted=False; self._owner_attempted=False
        self._start_sha=None; self._owner_committed=False; self._held=None; self._held_identity=None
        budget.require_running()
        self._roots=[pub._directory(p) for p in [work,retained,supervision]]
        self._work,self._retained,self._journal=[row[0] for row in self._roots]
        op=binding['operationRef']
        require(all(p.name==op for p in [self._work,self._retained,self._journal])
                and [p.parent.name for p in [self._work,self._retained,self._journal]]==
                    ['native-work','native-retained','native-supervision']
                and self._work.parent.parent==self._retained.parent.parent==self._journal.parent.parent,
                'RUN_RECORDS_LAYOUT')
        for name in ['start-consumed.json','held-process.json','supervision-uncertain.json',
                     'publication-intent.json','publication-uncertain.json','owned-closure.json',
                     'native-owner.json','native-owner-ready.json']:
            require(not os.path.lexists(self._journal/name),'RUN_RECORDS_PRIOR_ATTEMPT')
        require(not list(self._retained.iterdir()),'RUN_RECORDS_PRIOR_RETAINED')
        self._base_guard()
        intent,record,info=pub._read_control(self._journal/'parent-intent.json')
        pub._fields(intent,pub.INTENT_FIELDS)
        require(record['sha256']==binding['parentIntentSha256'] and
                intent['protocol']=='DSG_NATIVE_LINEAR_PARENT_INTENT_V2' and
                all(intent[k]==binding[k] for k in ['operationRef','launchControlSha256','sealSha256','grantSha256']),
                'RUN_RECORDS_PARENT_INTENT')
        for prefix,(path,identity) in zip(['nativeWork','retained','supervision'],self._roots):
            require(intent[prefix+'CanonicalPath']==path.as_posix() and
                    type(intent[prefix+'DirectoryIdentity']) is list and
                    all(type(n) is int for n in intent[prefix+'DirectoryIdentity']) and
                    intent[prefix+'DirectoryIdentity']==identity,'RUN_RECORDS_PARENT_ROOT')
        self._pins.append((self._journal/'parent-intent.json',record,info))
        require(type(intent['createdUTC']) is str and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ',intent['createdUTC']),
                'RUN_RECORDS_PARENT_TIME')
        dt.datetime.strptime(intent['createdUTC'],'%Y-%m-%dT%H:%M:%SZ')
        self._intent_created=intent['createdUTC']
        self._snapshot,self._control,_,inputs,input_bytes=pub._v2_launch(
            self._work,self._journal,binding,bootstrap_session,self._base_guard,
            progress_guard=self._progress_guard)
        self._pins.extend(inputs)
        _,grant,grant_info=pub._read_control(self._work/'launch-grant.json')
        require(grant['sha256']==binding['grantSha256'],'RUN_RECORDS_GRANT_PIN')
        self._pins.append((self._work/'launch-grant.json',grant,grant_info))
        self._initial_names={path.name for path,_,_ in inputs}|{'launch-grant.json'}
        require({p.name for p in self._work.iterdir()}==self._initial_names,'RUN_RECORDS_INITIAL_INVENTORY')
        require(self._control['parentDeadlineUTC']==budget.deadline_utc,'RUN_RECORDS_ORIGINAL_DEADLINE')
        worst=self._owner({'nativeProcessId':'4294967295','processCreationFileTime':'f'*16})
        self._owner_reserve=len(encode(worst))+len(encode(self._ready('f'*64)))
        require(input_bytes+grant['byteLength']+self._owner_reserve+pub.MIB<=200*pub.MIB,
                'RUN_RECORDS_INPUT_AGGREGATE')
        self.verify()

    def _progress_guard(self):
        require(not self._failed,'RUN_RECORDS_FAILED')
        self._budget.require_running()
        require([pub._directory(p) for p,_ in self._roots]==self._roots,'RUN_RECORDS_ROOT_CHANGED')
        pub._metadata_bound(self._journal)
        self._budget.require_running()
        for path in [self._work/'native-publication-uncertain.json',self._work/'cancel.json',
                     self._journal/'supervision-uncertain.json',self._journal/'publication-uncertain.json',
                     self._journal/'publication-intent.json',self._journal/'owned-closure.json']:
            require(not os.path.lexists(path),'RUN_RECORDS_UNCERTAINTY_OR_CANCEL')

    def _base_guard(self):
        self._budget.require_running(); self._session.assert_intact(); self._progress_guard()

    def _inventory(self):
        expected=self._initial_names|{p.name for p,_,_ in self._pins if p.parent==self._work}
        actual={p.name for p in self._work.iterdir()}
        if any(p==self._work/'native-owner-ready.json' for p,_,_ in self._pins):
            require(expected<=actual and actual<=expected|pub.ALLOWED,'RUN_RECORDS_WORK_INVENTORY')
        else: require(actual==expected,'RUN_RECORDS_WORK_INVENTORY')

    def verify(self):
        require(not self._failed,'RUN_RECORDS_FAILED')
        try:
            self._base_guard(); self._snapshot.verify()
            for path,record,info in self._pins:
                require(pub._hash_bounded(path,record['byteLength'],info)==record['sha256'], 'RUN_RECORDS_PIN_CHANGED')
                self._base_guard()
            if self._held_identity is not None:
                require(self._held.identity()==self._held_identity,'RUN_RECORDS_HELD_CHANGED')
            self._base_guard()
            self._inventory()
            self._budget.require_running()
            for path in [self._work/'cancel.json',self._work/'native-publication-uncertain.json',
                         self._journal/'supervision-uncertain.json',self._journal/'publication-uncertain.json']:
                require(not os.path.lexists(path),'RUN_RECORDS_UNCERTAINTY_OR_CANCEL')
        except BaseException:
            self._failed=True
            raise

    def _write(self,path,value):
        self.verify()
        sha,info=pub._write_control(path,value)
        self._pins.append((path,{'sha256':sha,'byteLength':info.st_size},info))
        self.verify()
        return sha

    def consume(self,created_utc):
        require(not self._consume_attempted,'RUN_RECORDS_START_REPLAY')
        self._consume_attempted=True
        try:
            require(type(created_utc) is str and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ',created_utc),
                    'RUN_RECORDS_CREATED_UTC')
            dt.datetime.strptime(created_utc,'%Y-%m-%dT%H:%M:%SZ')
            require(self._intent_created<=created_utc<self._control['parentDeadlineUTC'],'RUN_RECORDS_TIME_ORDER')
            require({p.name for p in self._work.iterdir()}==self._initial_names,'RUN_RECORDS_PRESTART_INVENTORY')
            value=dict(protocol='DSG_NATIVE_LINEAR_START_CONSUMED_V1',
                **{k:self._binding[k] for k in ['operationRef','parentIntentSha256','launchControlSha256','grantSha256']},
                processSessionRef=self._control['processSessionRef'],createdUTC=created_utc,permission='ONE_ATTEMPT_NO_REPLAY')
            self._start_sha=self._write(self._journal/'start-consumed.json',value)
            return {'startConsumedSha256':self._start_sha,'newNativeStartAllowed':False}
        except BaseException:
            self._failed=True
            raise

    def _owner(self,identity):
        return dict(protocol='DSG_NATIVE_LINEAR_OWNER_V1',**self._binding,
            processSessionRef=self._control['processSessionRef'],ownerNonce=self._control['ownerNonce'],
            parentDeadlineUTC=self._control['parentDeadlineUTC'],**identity)

    def _ready(self,owner_sha):
        return dict(protocol='DSG_NATIVE_LINEAR_OWNER_READY_V1',operationRef=self._binding['operationRef'],
            processSessionRef=self._control['processSessionRef'],ownerNonce=self._control['ownerNonce'],ownerSha256=owner_sha)

    def write_owner(self,held):
        require(not self._owner_attempted,'RUN_RECORDS_OWNER_REPLAY')
        self._owner_attempted=True; self._held=held
        try:
            require(self._start_sha is not None and type(held) is HeldNativeProcess,'RUN_RECORDS_HELD_REQUIRED')
            self._held_identity=held.identity(); self.verify()
            value=dict(protocol='DSG_NATIVE_LINEAR_HELD_PROCESS_V1',operationRef=self._binding['operationRef'],
                processSessionRef=self._control['processSessionRef'],**self._held_identity,
                parentIntentSha256=self._binding['parentIntentSha256'],startConsumedSha256=self._start_sha,
                ownership='CURRENT_POPEN_HANDLE_ONLY')
            self._write(self._journal/'held-process.json',value)
            owner=self._owner(self._held_identity); owner_sha=self._write(self._work/'native-owner.json',owner)
            require(self._write(self._journal/'native-owner.json',owner)==owner_sha,'RUN_RECORDS_OWNER_COPY')
            ready=self._ready(owner_sha)
            require(len(encode(owner))+len(encode(ready))<=self._owner_reserve,'RUN_RECORDS_OWNER_RESERVE')
            ready_sha=self._write(self._journal/'native-owner-ready.json',ready)
            # Native commit last: both parent copies are already durable and pinned.
            require(self._write(self._work/'native-owner-ready.json',ready)==ready_sha,'RUN_RECORDS_READY_COPY')
            self._owner_committed=True
            return {'ownerSha256':owner_sha,'ownerReadySha256':ready_sha,'processClosureAuthorized':False}
        except BaseException:
            self._failed=True
            raise

    def diagnostic(self):
        return {'failed':self._failed,'startAttemptConsumed':self._consume_attempted,
                'ownerAttemptConsumed':self._owner_attempted,'ownerCommitted':self._owner_committed,
                'newNativeStartAllowed':False,'processClosureAuthorized':False}
