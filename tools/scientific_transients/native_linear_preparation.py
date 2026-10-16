"""Private V5 preparation only. No CLI, native start, cloud or consent authentication.

The trusted operator must have fresh scoped human consent BEFORE calling prepare.
A matching authorization record is provenance, never self-authorizing JSON.
"""
import datetime as dt
import hashlib
import os
from pathlib import Path
import re
import shutil
import stat
import time

from tools.pixinsight.local_pilot.broker import encode, require
from tools.scientific_transients import native_publication as pub
from tools.scientific_transients.native_launch_control import FIXED, HASH_ROLES, _pin
from tools.scientific_transients.native_linear_supervisor import LinearNativeSupervisor
from tools.scientific_transients.native_read_locks import NativeReadLocks
from tools.scientific_transients.native_run_budget import LiveNativeBudget
from tools.scientific_transients.native_run_records import NativeRunRecords
from tools.scientific_transients.native_supervision_signals import NativeSupervisionSignals

LIBRARIES={'CORE':'native_linear_uncertainty.jsh','PARSER':'strict_passive_json.jsh',
           'PRIMARY':'native_float32_primary.jsh','WRAPPER':'native_linear_measurement.jsh'}
WORK=set(LIBRARIES.values())|{'source.fits','kernel-spec.json','source-lineage.json'}
RESOURCES=FIXED-{'ENTRY','APPROVAL',*LIBRARIES}


def _canonical(value):
    require(type(value) is str and value.isascii() and 1<=len(value)<=512
            and all(32<=ord(c)<127 for c in value),'PREPARATION_PATH')
    path=pub.safe_path(value)
    require(path.as_posix()==value and path.resolve()==path,'PREPARATION_PATH')
    return path


def _utc(value):
    require(type(value) is str and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ',value),'PREPARATION_TIME')
    return dt.datetime.strptime(value,'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc)


def render_entry(work,launcher,expected):
    """Definition-only includes and a single literal call; no arbitrary JS input."""
    def native_path(value):
        require(type(value) is str and len(value)<=512 and re.match('^[A-Za-z]:/',value)
                and not re.search(r'[\x00-\x1f\x7f-\uffff\\\"\'<>|:*?\[\]]',value[2:]),'PREPARATION_NATIVE_PATH')
        require(all(part and part not in {'.','..'} and not part.endswith(('.',' '))
                    for part in value[3:].split('/')),'PREPARATION_NATIVE_PATH')
        return value
    work=native_path(work); launcher=native_path(launcher)
    pub._fields(expected,{'operationRef','ownerNonce','processSessionRef','sealSha256','grantSha256',
                         'wrapperSha256','parentDeadlineUTC'})
    for key in ['operationRef','ownerNonce','processSessionRef']:
        require(type(expected[key]) is str and re.fullmatch('[a-f0-9]{32}',expected[key]),'PREPARATION_ENTRY_ID')
    require(work.rsplit('/',1)[-1]==expected['operationRef'],'PREPARATION_ENTRY_ROOT')
    require(all(pub._sha(expected[k]) for k in ['sealSha256','grantSha256','wrapperSha256']),'PREPARATION_ENTRY_SHA')
    _utc(expected['parentDeadlineUTC'])
    lines=['#include "'+work+'/'+name+'"' for name in LIBRARIES.values()]
    lines.append('#include "'+launcher+'"')
    lines.append('DSGNativeLinearLaunch('+encode(work).decode('ascii')+','+encode(expected).decode('ascii')+');')
    return ('\r\n'.join(lines)+'\r\n').encode('ascii')


class LinearAttemptPreparation:
    """Create this live object before ANY plan/preparation IO, after real consent.

    Caller retains this object on failure. No rearm, cleanup, overwrite, grant
    renewal, process creation or implicit supervisor.start call exists here.
    """
    def __init__(self,session,plan_path,plan_sha,*,monotonic=time.monotonic,
                 wall=lambda:dt.datetime.now(dt.timezone.utc)):
        self._budget=LiveNativeBudget(monotonic=monotonic,wall=wall)
        self._session=session; self._plan_path=plan_path; self._plan_sha=plan_sha
        self._attempted=False; self._failed=False; self._grant_created=False; self._grant_attempted=False
        self._records=None; self._signals=None; self._locks=None; self._supervisor=None
        self._roots=[]; self._base_identity=None; self._state='PREPARING'

    def _guard(self):
        self._budget.require_running(); self._session.assert_intact()
        require(not self._failed,'PREPARATION_FAILED')
        require(self._base_identity is None or pub._directory(self._base_identity[0])==self._base_identity,
                'PREPARATION_BASE_CHANGED')
        require(all(pub._directory(path)==(path,identity) for path,identity in self._roots),
                'PREPARATION_ROOT_CHANGED')

    def _write_bytes(self,path,raw):
        self._guard(); require(type(raw) is bytes and len(raw)<=pub.MIB,'PREPARATION_METADATA_SIZE')
        with path.open('xb') as stream:
            require(stream.write(raw)==len(raw),'PREPARATION_SHORT_WRITE')
            stream.flush(); os.fsync(stream.fileno()); info=os.fstat(stream.fileno())
        sha=hashlib.sha256(raw).hexdigest()
        require(pub._hash_bounded(path,len(raw),info)==sha,'PREPARATION_READBACK')
        self._guard()
        return {'name':path.name,'role':path.name,'sha256':sha,'byteLength':len(raw)},info

    def _write_json(self,path,value):
        pub._control_tree(value,array_limit=128,string_limit=512)
        row,info=self._write_bytes(path,encode(value))
        observed,_,_=pub._read_control(path,array_limit=128,string_limit=512)
        require(observed==value,'PREPARATION_JSON_READBACK')
        return row,info

    def _copy(self,row,destination,cap):
        pub._fields(row,{'path','sha256','byteLength'})
        source=_canonical(row['path'])
        require(pub._sha(row['sha256']) and type(row['byteLength']) is int
                and 0<row['byteLength']<=cap,'PREPARATION_INPUT_SIZE')
        self._guard(); digest=hashlib.sha256(); count=0
        require(stat.S_ISREG(source.lstat().st_mode),'PREPARATION_REGULAR_INPUT')
        with source.open('rb') as incoming:
            before=os.fstat(incoming.fileno())
            require(stat.S_ISREG(before.st_mode) and before.st_nlink==1 and before.st_size==row['byteLength'],
                    'PREPARATION_INPUT_SHAPE')
            with destination.open('xb') as outgoing:
                while block:=incoming.read(min(65536,row['byteLength']-count+1)):
                    self._budget.require_running(); count+=len(block)
                    require(count<=row['byteLength'],'PREPARATION_SOURCE_GREW')
                    require(outgoing.write(block)==len(block),'PREPARATION_SHORT_WRITE'); digest.update(block)
                outgoing.flush(); os.fsync(outgoing.fileno()); info=os.fstat(outgoing.fileno())
            require(pub.signature(os.fstat(incoming.fileno()))==pub.signature(before),'PREPARATION_SOURCE_CHANGED')
        require(pub.signature(source.lstat())[:4]==pub.signature(before)[:4]
                and count==row['byteLength'] and digest.hexdigest()==row['sha256'],'PREPARATION_SOURCE_CHANGED')
        require(pub._hash_bounded(destination,count,info)==row['sha256'],'PREPARATION_COPY_READBACK')
        self._guard()
        return dict(role=destination.name,name=destination.name,sha256=row['sha256'],byteLength=count),info

    def _validate_parameters(self,p,files):
        pub._fields(p,{'protocol','operationRef','purpose','expectedPixInsightVersion','kernelSpecSha256',
            'lineageSha256','source','dependencies','maxRuntimeSeconds','bindings','ownerNonce','processSessionRef'})
        require(p['protocol']=='DSG_NATIVE_LINEAR_MEASUREMENT_V2' and p['purpose']=='DEVELOPMENT'
                and type(p['maxRuntimeSeconds']) is int and p['maxRuntimeSeconds']==180,'PREPARATION_PARAMETERS')
        for key in ['operationRef','ownerNonce','processSessionRef']:
            require(type(p[key]) is str and re.fullmatch('[a-f0-9]{32}',p[key]),'PREPARATION_SESSION')
        require(type(p['expectedPixInsightVersion']) is str and re.fullmatch('[\x20-\x7e]{1,96}',p['expectedPixInsightVersion']),
                'PREPARATION_VERSION')
        source=p['source']; pub._fields(source,{'sha256','byteLength','primaryHeaderSha256','dataOffset','width',
            'height','sampleFormat','orientation','bscale','bzero'})
        require(source['sha256']==files['source.fits']['sha256'] and source['byteLength']==files['source.fits']['byteLength']
                and pub._sha(source['primaryHeaderSha256']) and source['sampleFormat']=='FLOAT32_BE'
                and source['orientation']=='FITS_AXIS1_FAST_NO_FLIP','PREPARATION_SOURCE_METADATA')
        require(all(type(source[k]) is int for k in ['width','height','dataOffset','byteLength','bscale','bzero'])
                and 1<=source['width']<=4194304 and 1<=source['height']<=4194304
                and source['width']*source['height']<=4194304 and 2880<=source['dataOffset']<=1048320
                and source['dataOffset']%2880==0 and source['bscale']==1 and source['bzero']==0
                and source['dataOffset']+4*source['width']*source['height']<=source['byteLength'],
                'PREPARATION_GEOMETRY_METADATA')
        require(p['kernelSpecSha256']==files['kernel-spec.json']['sha256']
                and p['lineageSha256']==files['source-lineage.json']['sha256'],'PREPARATION_MODEL_PINS')
        pub._fields(p['dependencies'],{'coreSha256','parserSha256','primarySha256','wrapperSha256'})
        for role,key in [('CORE','coreSha256'),('PARSER','parserSha256'),('PRIMARY','primarySha256'),('WRAPPER','wrapperSha256')]:
            require(p['dependencies'][key]==files[LIBRARIES[role]]['sha256'],'PREPARATION_LIBRARY_PIN')
        require(type(p['bindings']) is list and len(p['bindings'])<=64,'PREPARATION_BINDINGS')
        roles=set(); cards=set()
        for binding in p['bindings']:
            pub._fields(binding,{'role','referenceSha256','cardSha256'})
            require(type(binding['role']) is str and re.fullmatch('[A-Za-z0-9_.]{1,192}',binding['role'])
                    and binding['role'] not in roles and pub._sha(binding['referenceSha256'])
                    and pub._sha(binding['cardSha256']),'PREPARATION_BINDING')
            roles.add(binding['role']); name='source-card-'+binding['cardSha256']+'.json'; cards.add(name)
            require(name in files and files[name]['sha256']==binding['cardSha256'],'PREPARATION_CARD_PIN')
        require(cards==set(files)-WORK,'PREPARATION_UNUSED_CARD')

    def prepare(self,approval_path,approval_sha):
        require(not self._attempted,'PREPARATION_REPLAY'); self._attempted=True
        try:
            # Includes failures before any directory/record can be written. The
            # original bootstrap session cannot mint a replacement context.
            require(not getattr(self._session,'_linear_preparation_attempted',False),
                    'PREPARATION_SESSION_REPLAY')
            self._session._linear_preparation_attempted=True
            self._guard(); path=_canonical(self._plan_path)
            require(stat.S_ISREG(path.lstat().st_mode),'PREPARATION_PLAN_FILE')
            plan,pr,pi=pub._read_control(path,array_limit=128,string_limit=512)
            require(pub._sha(self._plan_sha) and pr['sha256']==self._plan_sha,'PREPARATION_PLAN_PIN')
            pub._fields(plan,{'protocol','root','parameters','workFiles','resources'})
            require(plan['protocol']=='DSG_NATIVE_LINEAR_PREPARATION_V1','PREPARATION_PLAN_PROTOCOL')
            base=_canonical(plan['root']); require(base.is_dir(),'PREPARATION_BASE')
            self._base_identity=pub._directory(base)
            files={}
            require(type(plan['workFiles']) is list and 7<=len(plan['workFiles'])<=71,'PREPARATION_INPUT_COUNT')
            total=0
            for row in plan['workFiles']:
                pub._fields(row,{'name','path','sha256','byteLength'}); name=row['name']
                require(type(name) is str and (name in WORK or re.fullmatch('source-card-[a-f0-9]{64}\\.json',name))
                        and name not in files,'PREPARATION_INPUT_NAME')
                cap=64*pub.MIB if name in {'source.fits','kernel-spec.json'} else pub.MIB
                require(type(row['byteLength']) is int and 0<row['byteLength']<=cap and pub._sha(row['sha256']),
                        'PREPARATION_INPUT_SIZE')
                total+=row['byteLength']; files[name]=row
            require(WORK<=files.keys() and total<200*pub.MIB,'PREPARATION_INPUT_AGGREGATE')
            p=plan['parameters']; self._validate_parameters(p,files)
            approval_file=_canonical(approval_path)
            require(stat.S_ISREG(approval_file.lstat().st_mode),'PREPARATION_APPROVAL_FILE')
            approval,ar,ai=pub._read_control(approval_file,string_limit=512)
            require(pub._sha(approval_sha) and ar['sha256']==approval_sha,'PREPARATION_APPROVAL_PIN')
            pub._fields(approval,{'protocol','operationRef','planSha256','proposalSha256','decisionRef',
                'permission','authorizedUTC','expiresUTC','maxStarts','maxRuntimeSeconds','cloudAuthorized'})
            require(approval['protocol']=='DSG_NATIVE_LINEAR_HUMAN_SCOPE_V1' and approval['operationRef']==p['operationRef']
                and approval['planSha256']==self._plan_sha and pub._sha(approval['proposalSha256'])
                and type(approval['decisionRef']) is str and re.fullmatch('[a-f0-9]{32}',approval['decisionRef'])
                and approval['permission']=='SINGLE_PREPARATION_SINGLE_START_WITH_OWNED_CLEANUP'
                and type(approval['maxStarts']) is int and approval['maxStarts']==1
                and type(approval['maxRuntimeSeconds']) is int and approval['maxRuntimeSeconds']==180
                and approval['cloudAuthorized'] is False,'PREPARATION_APPROVAL_SCOPE')
            self._guard()
            require(_utc(approval['authorizedUTC'])<=self._budget._last_wall
                    and _utc(approval['expiresUTC'])>=_utc(self._budget.deadline_utc),'PREPARATION_APPROVAL_TIME')
            require(type(plan['resources']) is list and len(plan['resources'])==len(RESOURCES),'PREPARATION_RESOURCES')
            resources={}
            for row in plan['resources']:
                pub._fields(row,{'role','path','sha256','byteLength'})
                role=row['role']; require(role in RESOURCES and role not in resources,'PREPARATION_RESOURCE_ROLE')
                cap=512*pub.MIB if role=='EXECUTABLE' else 16*pub.MIB if role=='PYTHON_EXECUTABLE' else pub.MIB
                require(pub._sha(row['sha256']) and type(row['byteLength']) is int and 0<row['byteLength']<=cap,
                        'PREPARATION_RESOURCE_SIZE')
                resource_path=_canonical(row['path'])
                resources[role]=dict(row,name=resource_path.name)
                require(stat.S_ISREG(resource_path.lstat().st_mode),'PREPARATION_REGULAR_RESOURCE')
                _pin(row['path'],row['sha256'],cap,self._budget.require_running,size=row['byteLength'])
                self._guard()
            self._guard(); sources=self._session.attest_sources(); bootstrap=self._session.attest_bootstrap()
            supervisor=sources.get('tools.scientific_transients.native_linear_supervisor')
            require(supervisor=={k:resources['SUPERVISOR'][k] for k in ['path','sha256','byteLength']}
                    and 'tools.scientific_transients.native_linear_preparation' in sources,'PREPARATION_LOADED_SOURCE')
            require(resources['BOOTSTRAP_ENTRY']['sha256']==bootstrap['bootstrapEntrySha256']
                    and resources['BOOTSTRAP_MANIFEST']['sha256']==bootstrap['bootstrapManifestSha256']
                    and resources['PYTHON_EXECUTABLE']['path']==bootstrap['pythonExecutable']
                    and resources['PYTHON_EXECUTABLE']['sha256']==bootstrap['pythonExecutableSha256'],
                    'PREPARATION_BOOTSTRAP_BINDING')
            require(len(FIXED)+len(sources)<=128,'PREPARATION_PARENT_SOURCE_COUNT')
            native_expected={k:p[k] for k in ['operationRef','ownerNonce','processSessionRef']}
            native_expected.update(sealSha256='f'*64,grantSha256='f'*64,wrapperSha256=p['dependencies']['wrapperSha256'],
                                   parentDeadlineUTC=self._budget.deadline_utc)
            render_entry((base/'native-work'/p['operationRef']).as_posix(),
                         (base/'native-supervision'/p['operationRef']/'native_linear_launcher.jsh').as_posix(),native_expected)
            for name in ['native-work','native-retained','native-supervision']:
                parent=base/name
                if not os.path.lexists(parent): parent.mkdir()
                pub._directory(parent)
                target=parent/p['operationRef']; target.mkdir()
                self._roots.append(pub._directory(target)); self._guard()
            work,retained,journal=[root for root,_ in self._roots]
            require(all(len(root.as_posix())<=192 for root in [work,retained,journal]),'PREPARATION_PARENT_PATH_LENGTH')
            # Preserve the exact externally pinned plan/decision before deriving outputs.
            plan_copy,plan_info=self._copy(dict(path=path.as_posix(),sha256=pr['sha256'],byteLength=pr['byteLength']),
                                           journal/'preparation-plan.json',pub.MIB)
            auth_copy,_=self._copy(dict(path=_canonical(approval_path).as_posix(),sha256=ar['sha256'],byteLength=ar['byteLength']),
                                  journal/'authorization.json',pub.MIB)
            sealed=[]
            for name,row in files.items():
                cap=64*pub.MIB if name in {'source.fits','kernel-spec.json'} else pub.MIB
                copied,_=self._copy({k:row[k] for k in ['path','sha256','byteLength']},work/name,cap); sealed.append(copied)
            for binding in p['bindings']:
                card,_,_=pub._read_control(work/('source-card-'+binding['cardSha256']+'.json'))
                require(card==dict(protocol='DSG_NATIVE_LINEAR_BINDING_CARD_V1',role=binding['role'],
                    referenceSha256=binding['referenceSha256'],
                    sourceSha256=p['source']['sha256'],kernelSpecSha256=p['kernelSpecSha256'],
                    scope='DECLARATION_ONLY_NOT_PHYSICAL_ACCEPTANCE'),'PREPARATION_CARD_METADATA')
            lineage,_,_=pub._read_control(work/'source-lineage.json')
            pub._fields(lineage,{'protocol','sourceSha256','parentManifestSha256','providerProductCardSha256',
                                 'upstreamPixInsightHistory','interpretation'})
            require(lineage['protocol']=='DSG_NATIVE_SOURCE_LINEAGE_V1' and lineage['sourceSha256']==p['source']['sha256']
                    and pub._sha(lineage['parentManifestSha256']) and pub._sha(lineage['providerProductCardSha256'])
                    and lineage['upstreamPixInsightHistory']=='NOT_PRESENT_IN_SOURCE_FITS'
                    and lineage['interpretation']=='SOURCE_PROVENANCE_NOT_PHYSICAL_ACCEPTANCE','PREPARATION_LINEAGE')
            parameters,_=self._write_json(work/'parameters.json',p); sealed.append(parameters)
            seal=dict(protocol='DSG_NATIVE_LINEAR_LAUNCH_SEAL_V1',operationRef=p['operationRef'],
                createdUTC=self._budget._last_wall.strftime('%Y-%m-%dT%H:%M:%SZ'),files=sealed,
                arbSha256=resources['ARB_REPORT']['sha256'],rqSha256=resources['RQ_REPORT']['sha256'],inputClosureAccepted=False)
            seal_row,_=self._write_json(work/'launch-seal.json',seal)
            launcher_row,_=self._copy({k:resources['LAUNCHER'][k] for k in ['path','sha256','byteLength']},
                                      journal/'native_linear_launcher.jsh',pub.MIB)
            resources['LAUNCHER']=dict(launcher_row,role='LAUNCHER',path=(journal/'native_linear_launcher.jsh').as_posix())
            self._guard(); require(shutil.disk_usage(base).free>=1024**3,'PREPARATION_FREE_SPACE')
            created=self._budget._last_wall.replace(microsecond=0)
            grant=dict(protocol='DSG_NATIVE_LINEAR_SINGLE_START_GRANT_V1',operationRef=p['operationRef'],
                sealSha256=seal_row['sha256'],purpose='DEVELOPMENT',authorized=True,maxStarts=1,maxRuntimeSeconds=180,
                createdUTC=created.strftime('%Y-%m-%dT%H:%M:%SZ'),deadlineUTC=(created+dt.timedelta(seconds=180)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                expiresUTC=self._budget.deadline_utc)
            owner=dict(protocol='DSG_NATIVE_LINEAR_OWNER_V1',operationRef=p['operationRef'],parentIntentSha256='f'*64,
                launchControlSha256='f'*64,sealSha256=seal_row['sha256'],grantSha256='f'*64,
                processSessionRef=p['processSessionRef'],ownerNonce=p['ownerNonce'],parentDeadlineUTC=self._budget.deadline_utc,
                nativeProcessId='4294967295',processCreationFileTime='f'*16)
            ready=dict(protocol='DSG_NATIVE_LINEAR_OWNER_READY_V1',operationRef=p['operationRef'],
                processSessionRef=p['processSessionRef'],ownerNonce=p['ownerNonce'],ownerSha256='f'*64)
            require(sum(row['byteLength'] for row in sealed)+seal_row['byteLength']+len(encode(grant))+
                    len(encode(owner))+len(encode(ready))+pub.MIB<=200*pub.MIB,'PREPARATION_DYNAMIC_INPUT_RESERVE')
            self._grant_attempted=True
            grant_row,_=self._write_json(work/'launch-grant.json',grant); self._grant_created=True
            expected={k:p[k] for k in ['operationRef','ownerNonce','processSessionRef']}
            expected.update(sealSha256=seal_row['sha256'],grantSha256=grant_row['sha256'],
                wrapperSha256=p['dependencies']['wrapperSha256'],parentDeadlineUTC=self._budget.deadline_utc)
            entry_row,_=self._write_bytes(journal/'entry.js',render_entry(work.as_posix(),resources['LAUNCHER']['path'],expected))
            resources['ENTRY']=dict(entry_row,role='ENTRY',path=(journal/'entry.js').as_posix())
            resources['APPROVAL']=dict(auth_copy,role='APPROVAL',path=(journal/'authorization.json').as_posix())
            for role,name in LIBRARIES.items():
                row=next(row for row in sealed if row['name']==name)
                resources[role]=dict(row,role=role,path=(work/name).as_posix())
            control=dict(protocol='DSG_NATIVE_LINEAR_LAUNCH_CONTROL_V1',**{k:p[k] for k in ['operationRef','ownerNonce','processSessionRef']},
                sealSha256=seal_row['sha256'],grantSha256=grant_row['sha256'],expectedPixInsightVersion=p['expectedPixInsightVersion'],
                expectedPythonVersion=bootstrap['expectedPythonVersion'],parentDeadlineUTC=self._budget.deadline_utc,
                files=list(resources.values())+[dict(role='PARENT_SOURCE',name=name,**row) for name,row in sources.items()])
            for key,role in HASH_ROLES.items(): control[key]=resources[role]['sha256']
            control_row,_=self._write_json(journal/'launch-control.json',control)
            intent=dict(protocol='DSG_NATIVE_LINEAR_PARENT_INTENT_V2',operationRef=p['operationRef'],
                createdUTC=self._budget._last_wall.strftime('%Y-%m-%dT%H:%M:%SZ'),sealSha256=seal_row['sha256'],
                grantSha256=grant_row['sha256'],launchControlSha256=control_row['sha256'])
            for prefix,(root,identity) in zip(['nativeWork','retained','supervision'],self._roots):
                intent[prefix+'CanonicalPath']=root.as_posix(); intent[prefix+'DirectoryIdentity']=identity
            intent_row,_=self._write_json(journal/'parent-intent.json',intent)
            binding={k:intent[k] for k in ['operationRef','sealSha256','grantSha256','launchControlSha256']}
            binding['parentIntentSha256']=intent_row['sha256']
            self._records=NativeRunRecords(work,retained,journal,binding,bootstrap_session=self._session,budget=self._budget)
            self._records._pins.append((journal/'preparation-plan.json',plan_copy,plan_info))
            self._signals=NativeSupervisionSignals(self._records)
            rows=[dict(path=path.as_posix(),sha256=row['sha256'],byteLength=row['byteLength'])
                  for path,row,_ in self._records._pins if path.parent==work]
            rows.extend({k:resources[role][k] for k in ['path','sha256','byteLength']} for role in ['ENTRY','LAUNCHER'])
            def observer_guard(): self._budget.check(); self._session.assert_intact()
            self._guard(); self._locks=NativeReadLocks(rows,guard=observer_guard,progress_guard=self._budget.check)
            self._supervisor=LinearNativeSupervisor(self._records,self._signals,[self._locks])
            self._guard(); self._state='PREPARED_LIVE'
            return self._supervisor
        except BaseException:
            self._failed=True; self._state='FAILED_PREPARATION'
            raise

    def diagnostic(self):
        return {'state':self._state,'attemptConsumed':self._attempted,'failed':self._failed,
                'grantAttemptConsumed':self._grant_attempted,'grantCommitted':self._grant_created,
                'preparedSupervisorRetained':self._supervisor is not None,
                'newNativeStartAllowed':False,'scientificValidation':'NOT_VALIDATED','qualifiedControls':0}
