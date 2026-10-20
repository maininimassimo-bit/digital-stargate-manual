"""Live S6/S7 retained proof composition. No launch, termination or acceptance."""
import os

from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients import native_publication as pub
from tools.scientific_transients.native_held_process import HeldNativeProcess
from tools.scientific_transients.native_read_locks import NativeReadLocks
from tools.scientific_transients.native_run_records import NativeRunRecords
from tools.scientific_transients.native_state_metadata import check_state_metadata
from tools.scientific_transients.native_supervision_signals import NativeSupervisionSignals


class RetainedRunVerification:
    """Keep the original records, signals, publication and lock groups alive.

    This object cannot prove WHEN locks were acquired. The future prepared-run
    owner must supply its original prestart groups and post-handshake Owner group.
    JSON receipts cannot reconstruct that owner. No lock is acquired/released here.
    """
    def __init__(self, records, signals, publication, locks):
        self._records=records; self._signals=signals; self._publication=publication
        self._locks=tuple(locks) if type(locks) in {list,tuple} else ()
        self._live=None; self._failed=False; self._last=None
        require(type(records) is NativeRunRecords,'RETAINED_LIVE_RECORDS')
        try:
            require(not getattr(records,'_retained_verification_attached',False),
                    'RETAINED_LIVE_RECONSTRUCTION')
            records._retained_verification_attached=True
            require(type(signals) is NativeSupervisionSignals and signals._records is records,
                    'RETAINED_LIVE_SIGNALS')
            require(type(publication) is dict and type(publication.get('liveVerification'))
                    is pub.LivePublicationVerification,'RETAINED_LIVE_PUBLICATION')
            self._live=publication['liveVerification']
            require(publication.get('markerSha256')==self._live.diagnostic()['markerSha256'],
                    'RETAINED_LIVE_MARKER_PIN')
            require(1<=len(self._locks)<=3 and all(type(g) is NativeReadLocks for g in self._locks),
                    'RETAINED_LIVE_LOCK_GROUPS')
            self.verify()
        except BaseException:
            self._fail()
            raise

    def _fail(self):
        self._failed=True; self._records._failed=True
        if type(self._signals) is NativeSupervisionSignals and self._signals._records is self._records:
            self._signals._fail()

    def _guard(self):
        r=self._records; s=self._signals
        require(not self._failed and not r._failed and not s.diagnostic()['liveUncertain'],
                'RETAINED_LIVE_UNCERTAIN')
        require(r._owner_committed and r._start_sha is not None and
                type(r._held) is HeldNativeProcess and s._held is r._held,'RETAINED_LIVE_HELD_CONTEXT')
        r._budget.check(); r._session.assert_intact(); s.verify_records()
        require([pub._directory(p) for p,_ in r._roots]==r._roots,'RETAINED_LIVE_ROOT_CHANGED')
        pub._metadata_bound(r._journal)
        for path in [r._work/'native-publication-uncertain.json',
                     r._journal/'publication-uncertain.json',r._journal/'supervision-uncertain.json',
                     r._journal/'owned-closure.json']:
            require(not os.path.lexists(path),'RETAINED_LIVE_FENCE')
        require(r._held.identity()==r._held_identity,'RETAINED_LIVE_HELD_CHANGED')

    def _pins_and_locks(self):
        r=self._records; required={}
        for path,row,info in r._pins:
            require(pub._hash_bounded(path,row['byteLength'],info)==row['sha256'],
                    'RETAINED_LIVE_RECORD_CHANGED')
            if path.parent==r._work:
                require(path not in required,'RETAINED_LIVE_DUPLICATE_INPUT')
                required[path]=(row['sha256'],row['byteLength'])
            self._guard()
        for role in ['ENTRY','LAUNCHER']:
            row=next(v for v in r._control['files'] if v['role']==role)
            path=pub.safe_path(row['path'])
            require(path not in required,'RETAINED_LIVE_CODE_ALIAS')
            required[path]=(row['sha256'],row['byteLength'])
        actual={}
        for group in self._locks:
            group.verify()
            require(not group._released and group._held,'RETAINED_LIVE_RELEASED_LOCKS')
            for _,path,row,_ in group._held:
                require(path not in actual,'RETAINED_LIVE_DUPLICATE_LOCK')
                actual[path]=(row['sha256'],row['byteLength'])
        require(actual==required,'RETAINED_LIVE_LOCK_COVERAGE')

    def _metadata(self):
        r=self._records; archive=r._retained
        def read(name): return pub._read_control(archive/name)
        marker,mr,_=read('retained-native-terminal.json')
        require(mr['sha256']==self._live.diagnostic()['markerSha256'],'RETAINED_LIVE_MARKER_CHANGED')
        pub._fields(marker,{'protocol',*r._binding,'nativeTerminalSha256','nativeReadySha256',
            'nativeReturnSha256','ownerSha256','ownerReadySha256','nativeState','products',
            'allProductsRetained','unclosedOwnedViews','parentMonotonicDeadlineExceeded',
            'measurementAccepted','scientificValidation','qualifiedControls'})
        require(marker['protocol']=='DSG_NATIVE_LINEAR_RETAINED_TERMINAL_V2' and
                all(marker[k]==v for k,v in r._binding.items()) and marker['allProductsRetained'] is True
                and marker['measurementAccepted'] is False and marker['scientificValidation']=='NOT_VALIDATED'
                and type(marker['qualifiedControls']) is int and marker['qualifiedControls']==0
                and type(marker['unclosedOwnedViews']) is int and marker['unclosedOwnedViews']==0
                and type(marker['parentMonotonicDeadlineExceeded']) is bool,'RETAINED_LIVE_MARKER')
        terminal,tr,_=read('terminal.json'); ready,rr,_=read('terminal-ready.json')
        returned,nr,_=read('native-return.json'); owner,ow,_=read('native-owner.json')
        owner_ready,orr,_=read('native-owner-ready.json')
        require(owner==r._owner(r._held_identity) and owner_ready==r._ready(ow['sha256']),
                'RETAINED_LIVE_OWNER')
        require(ready==dict(protocol='DSG_NATIVE_LINEAR_TERMINAL_READY_V1',
                operationRef=r._binding['operationRef'],terminalSha256=tr['sha256']),
                'RETAINED_LIVE_READY')
        fixed={v['role']:v for v in r._control['files'] if v['role']!='PARENT_SOURCE'}
        expected_return=dict(protocol='DSG_NATIVE_LINEAR_RETURNED_V1',operationRef=r._binding['operationRef'],
            sealSha256=r._binding['sealSha256'],wrapperSha256=fixed['WRAPPER']['sha256'],
            terminalSha256=tr['sha256'],readySha256=rr['sha256'],state=terminal['state'],
            unclosedOwnedViews=0,fullPhysicalVariance=None,significance=None,scientificValidation='NOT_VALIDATED',
            qualifiedControls=0,nativeProcessId=r._held_identity['nativeProcessId'],
            processSessionRef=r._control['processSessionRef'],ownerSha256=ow['sha256'],ownerReadySha256=orr['sha256'])
        require(returned==expected_return and type(returned['unclosedOwnedViews']) is int
                and type(returned['qualifiedControls']) is int,'RETAINED_LIVE_RETURN')
        products=pub._terminal(terminal,r._binding['operationRef'])
        require(marker['products']==products+[tr,rr,nr,ow,orr] and marker['nativeState']==terminal['state']
                and all(marker[k]==v['sha256'] for k,v in [('nativeTerminalSha256',tr),
                    ('nativeReadySha256',rr),('nativeReturnSha256',nr),('ownerSha256',ow),('ownerReadySha256',orr)]),
                'RETAINED_LIVE_PRODUCTS')
        by_name={p.name:row for p,row,_ in r._pins if p.parent==r._work}
        expected=dict(operationRef=r._binding['operationRef'],sealSha256=r._binding['sealSha256'],
            parametersSha256=by_name['parameters.json']['sha256'],sourceSha256=by_name['source.fits']['sha256'],
            kernelSpecSha256=by_name['kernel-spec.json']['sha256'],lineageSha256=by_name['source-lineage.json']['sha256'],
            dependencies={key:fixed[role]['sha256'] for role,key in [('CORE','coreSha256'),('PARSER','parserSha256'),
                ('PRIMARY','primarySha256'),('WRAPPER','wrapperSha256')]},
            pixInsightVersion=r._control['expectedPixInsightVersion'],nativeProcessId=r._held_identity['nativeProcessId'],
            processSessionRef=r._control['processSessionRef'],ownerSha256=ow['sha256'],ownerReadySha256=orr['sha256'])
        rows={v['name']:v for v in products}
        started,sr,_=read('started-native.json')
        require(sr==rows.get('started-native.json'),'RETAINED_LIVE_STARTED_PIN')
        evidence=None
        if 'native-evidence.json' in rows:
            evidence,er,_=read('native-evidence.json')
            require(er==rows['native-evidence.json'],'RETAINED_LIVE_EVIDENCE_PIN')
        state=check_state_metadata(terminal,started,evidence,expected)
        return dict(state,retainedStateVerified=True,markerSha256=mr['sha256'],nativeReturnSha256=nr['sha256'],
            processSessionRef=r._control['processSessionRef'],**r._held_identity)

    def verify(self):
        require(not self._failed,'RETAINED_LIVE_UNCERTAIN')
        try:
            self._guard(); self._live.verify(); self._pins_and_locks()
            result=self._metadata()
            self._pins_and_locks(); self._guard(); self._live.verify()
            self._records._budget.check()
            cancelled=os.path.lexists(self._records._work/'cancel.json')
            self._guard()
            budget=self._records._budget.diagnostic()
            result.update(parentMonotonicDeadlineExceeded=budget['parentMonotonicDeadlineExceeded'],
                parentWallDeadlineExceeded=budget['parentWallDeadlineExceeded'],
                parentCancelRequested=cancelled)
            self._last=dict(result)
            return dict(result)
        except BaseException:
            self._fail()
            raise

    def diagnostic(self):
        return {'verificationFailed':self._failed,'verified':self._last is not None,
                'processClosureAuthorized':False,'newNativeStartAllowed':False,'measurementAccepted':False}
