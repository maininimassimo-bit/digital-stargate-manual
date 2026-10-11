"""Prepare/verify a single native attempt. Launching is a separate worker action."""
import copy
import json
import re
from pathlib import Path
import shutil

from .broker import require, encode, decode
from .intake import sha, local_directory
from .image_analysis import fingerprint, analyze
from .source_provenance import _image
from .native_analysis import local_file
from .native_measurements import validate
from .adaptive_catalog import validate_dispatch, provenance
from .adaptive_execution import VERIFICATION_VERSION

VERSION = 'DSG_PIAI_ADAPTIVE_NATIVE_MANIFEST_V2'


def guarded_file(value):
    path=Path(local_directory(str(value)))
    require(all(not p.is_symlink() and not p.is_junction() for p in (path,*path.parents)) and
            path.is_file(),'ADAPTIVE_FILE_REPARSE_OR_MISSING')
    return path


def validate_runtime_files(runtime, files):
    require(isinstance(files,list) and 4<=len(files)<=64 and
            all(isinstance(r,dict) and set(r)=={'path','sha256'} for r in files),
            'ADAPTIVE_RUNTIME_FILE_LIST')
    required={runtime['suiteSha256']} | {r['fileSha256'] for r in runtime['models'].values()}
    require(len(required)==4 and required <= {r['sha256'] for r in files},'ADAPTIVE_RUNTIME_MODELS_OR_SUITE_MISSING')
    dependencies=sorted([r for r in files if r['sha256'] not in required],key=lambda r:r['path'])
    require(dependencies and sha(dependencies)==runtime['dependenciesSha256'],'ADAPTIVE_RUNTIME_DEPENDENCIES_CHANGED')
    for item in files:
        path=Path(local_directory(item['path']))
        require(all(not p.is_symlink() and not p.is_junction() for p in (path,*path.parents)) and
                path.is_file() and fingerprint(path)==item['sha256'],'ADAPTIVE_RUNTIME_FILE_CHANGED')


def require_installed_dependencies(files, pixinsight_root):
    root=Path(local_directory(str(pixinsight_root)))
    include=root/'include'
    pending=[include/'pjsr/StarDetector.jsh'];required={root/'bin/PixInsight.exe'};seen=set()
    while pending:
        path=pending.pop()
        if path in seen:continue
        seen.add(path);require(len(seen)<=64,'ADAPTIVE_INCLUDE_DEPENDENCY_LIMIT')
        guarded_file(path)
        require(path.stat().st_size<=2097152,'ADAPTIVE_INCLUDE_SIZE')
        required.add(path)
        for name in re.findall(r'^\s*#include\s+<([^>]+)>',path.read_text(encoding='utf-8-sig'),re.MULTILINE):
            require(re.fullmatch(r'pjsr/[A-Za-z0-9_]+\.jsh',name) is not None,'ADAPTIVE_INCLUDE_SCOPE')
            pending.append(include/name)
    declared={Path(r['path']) for r in files}
    require(required <= declared,'ADAPTIVE_INSTALLED_DEPENDENCIES_MISSING')
    return sorted(required,key=str)


def safe_path(value, root):
    path = Path(local_directory(str(value)))
    require(all(not p.is_symlink() and not p.is_junction() for p in (path,*path.parents)), 'ADAPTIVE_REPARSE_POINT')
    resolved = path.resolve(strict=True)
    require(resolved.is_relative_to(Path(root).resolve(strict=True)), 'ADAPTIVE_ARTIFACT_OUTSIDE_ATTEMPT')
    return resolved


def read(path, limit=4194304):
    require(path.is_file() and path.stat().st_size <= limit, 'ADAPTIVE_ARTIFACT_SIZE')
    return decode(path.read_bytes())


def prepare(directory, *, permit, approval, analysis, sources, runtime_files, background_roi,
            allowed_roots, pixinsight_root, native_lease, start_acknowledgement,
            parent_artifacts=None, parent_provenance=None):
    require(sha(approval) == permit['approvalSha256'] and sha(analysis['runtime']) == permit['runtimeSha256'],
            'ADAPTIVE_NATIVE_APPROVAL_RUNTIME')
    validate_runtime_files(analysis['runtime'],runtime_files)
    require_installed_dependencies(runtime_files,pixinsight_root)
    require(isinstance(start_acknowledgement,dict) and start_acknowledgement ==
            {'executeAllowed':True,'ordinal':permit['ordinal']}, 'ADAPTIVE_ACKNOWLEDGEMENT_REQUIRED')
    directory = Path(directory)
    require(all(not p.is_symlink() and not p.is_junction() for p in (directory,*directory.parents)),
            'ADAPTIVE_ATTEMPT_REPARSE_POINT')
    directory.mkdir(exist_ok=False,parents=False)
    (directory/'outputs').mkdir()
    require(isinstance(sources,list) and len(sources) == len(analysis['inputs']), 'ADAPTIVE_SOURCE_SELECTION')
    guards = []
    for source, descriptor in zip(sources,analysis['inputs']):
        require({k:source[k] for k in descriptor} == descriptor, 'ADAPTIVE_SOURCE_BINDING')
        path = local_file(source['path'],allowed_roots)
        require(fingerprint(path) == source['sha256'], 'ADAPTIVE_ORIGINAL_CHANGED')
        guards.append({**descriptor,'source':path.as_posix()})
    current_facts = provenance(parent_provenance or analysis['evidence']['provenance'])
    validate_dispatch(permit['step'],analysis['evidence']['mode'],current_facts)
    prep = approval['preparation']
    require(prep['inputSetSha256'] == sha(analysis['inputs']), 'ADAPTIVE_PREPARATION_INPUT_SET')
    width,height = prep['workingGeometry']
    require(isinstance(background_roi,list) and len(background_roi)==4 and all(type(n) is int for n in background_roi),
            'ADAPTIVE_BACKGROUND_RECTANGLE')
    x0,y0,x1,y1 = background_roi
    require(background_roi==prep['backgroundROI'],'ADAPTIVE_APPROVED_BACKGROUND_CHANGED')
    require(0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height and x1-x0 >= 32 and y1-y0 >= 32,
            'ADAPTIVE_BACKGROUND_RECTANGLE')
    if permit['ordinal']:
        require(parent_artifacts and {'RGB','L'} <= {r['role'] for r in parent_artifacts}, 'ADAPTIVE_PARENT_REQUIRED')
        selections = parent_artifacts
    else:
        selections = sources
    rows = []
    for row in selections:
        path = local_file(row['path'],allowed_roots + [directory.parent])
        require(fingerprint(path)==row['sha256'],'ADAPTIVE_PARENT_OR_SOURCE_CHANGED')
        geometry,_,_ = _image(path,row.get('imageIndex',0))
        require(all(geometry[k] == row[k] for k in ('width','height','channels')), 'ADAPTIVE_INPUT_GEOMETRY')
        target=directory/(row['role']+'.xisf')
        shutil.copyfile(path,target)
        require(fingerprint(target)==row['sha256'] and fingerprint(path)==row['sha256'],'ADAPTIVE_COPY_CHANGED')
        rows.append({k:row[k] for k in ('role','sha256','width','height','channels')} |
                    {'copy':target.as_posix(),'imageIndex':row.get('imageIndex',0)})
    runtime=[]
    for item in runtime_files:
        path=Path(local_directory(item['path']))
        require(all(not p.is_symlink() and not p.is_junction() for p in (path,*path.parents)) and
                fingerprint(path)==item['sha256'],'ADAPTIVE_RUNTIME_FILE_CHANGED')
        runtime.append(copy.deepcopy(item))
    library=Path(__file__).parent
    for name in ('adaptive_executor.jsh','adaptive_native.jsh','measurements.jsh'):
        shutil.copyfile(library/name,directory/name)
        runtime.append({'path':(directory/name).as_posix(),'sha256':fingerprint(directory/name)})
    require(sha({'controller':fingerprint(directory/'adaptive_executor.jsh'),
                 'factory':fingerprint(directory/'adaptive_native.jsh')})==analysis['runtime']['executorSha256'],
            'ADAPTIVE_EXECUTOR_SNAPSHOT_CHANGED')
    require(fingerprint(directory/'measurements.jsh')==analysis['runtime']['measurementSha256'],
            'ADAPTIVE_MEASUREMENT_SNAPSHOT_CHANGED')
    detector=Path(pixinsight_root)/'include/pjsr/StarDetector.jsh'
    require(fingerprint(detector)==analysis['runtime']['starDetectorSha256'],'ADAPTIVE_DETECTOR_CHANGED')
    runtime.append({'path':detector.as_posix(),'sha256':fingerprint(detector)})
    ack=directory/'start.json'
    with ack.open('xb') as f:f.write(encode(start_acknowledgement))
    context={'mode':analysis['evidence']['mode'],'domain':current_facts['domain'],
             'branch':approval['branch'],
             'backgroundROI':background_roi,
             'models':{k:v['selectedVersion'] for k,v in analysis['runtime']['models'].items()}}
    manifest={'version':VERSION,'permit':permit,'permitSha256':sha(permit),'approvalSha256':sha(approval),
              'sources':guards,'inputs':rows,'runtimeFiles':runtime,'preparation':prep,'context':context,
              'measurementSha256':analysis['runtime']['measurementSha256'],
              'coreVersion':analysis['runtime']['coreVersion'],
              'starDetectorSha256':analysis['runtime']['starDetectorSha256'],
              'regions':[background_roi,[0,0,width,height]],'parentArtifacts':parent_artifacts,
              'parentProvenance':current_facts,'originalProvenance':analysis['evidence']['provenance'],
              'startAcknowledgement':ack.as_posix(),'startAcknowledgementSha256':fingerprint(ack),
              'outputDirectory':(directory/'outputs').as_posix(),'nativeLease':Path(native_lease).as_posix(),
              **{k:(directory/name).as_posix() for k,name in
                 (('report','report.json'),('failure','failure.json'),('events','events.json'),('cancel','cancel.json'),('log','native.log'),('done','native-done.json'))}}
    with (directory/'manifest.json').open('xb') as f:f.write(encode(manifest))
    lines=['#engine v8','#define __PJSR_USE_STAR_DETECTOR_V2','#include <pjsr/StarDetector.jsh>']
    lines += ['#include '+json.dumps((directory/name).as_posix()) for name in
              ('measurements.jsh','adaptive_native.jsh','adaptive_executor.jsh')]
    lines += ['var manifest=JSON.parse(File.readTextFile('+json.dumps((directory/'manifest.json').as_posix())+'));',
              'DSGAdaptiveExecute(manifest);']
    with (directory/'run.js').open('xb') as f:f.write(('\r\n'.join(lines)+'\r\n').encode())
    return manifest


def verify(directory, *, expected_manifest_sha256, write_receipt=True):
    directory=Path(directory)
    require(fingerprint(safe_path(directory/'manifest.json',directory))==expected_manifest_sha256,
            'ADAPTIVE_NATIVE_MANIFEST_CHANGED')
    m=read(directory/'manifest.json')
    require(not (directory/'failure.json').exists(),'ADAPTIVE_NATIVE_FAILURE_PRESERVED')
    for item in m['runtimeFiles']:
        require(fingerprint(guarded_file(item['path']))==item['sha256'],'ADAPTIVE_RUNTIME_CHANGED')
    for source in m['sources']:
        require(fingerprint(guarded_file(source['source']))==source['sha256'],'ADAPTIVE_ORIGINAL_CHANGED')
    report=read(safe_path(m['report'],directory))
    done=read(safe_path(m['done'],directory))
    require(done=={'status':'OWNED_VIEWS_CLOSED','permitSha256':m['permitSha256']},'ADAPTIVE_NATIVE_CLEANUP_NOT_COMPLETE')
    require(report['version']==VERSION and report['status']=='NATIVE_SEGMENT_COMPLETE' and
            report['permitSha256']==m['permitSha256'] and report['sourceGuard']=='UNCHANGED', 'ADAPTIVE_NATIVE_RECEIPT')
    require(fingerprint(safe_path(m['events'],directory))==report['eventsSha256'],'ADAPTIVE_NATIVE_EVENTS_CHANGED')
    events=read(Path(m['events']))
    started=[e for e in events if e.get('kind')=='process-started']
    completed=[e for e in events if e.get('kind')=='process-completed']
    require(started and len(started)==len(completed),'ADAPTIVE_NATIVE_PARTIAL_PROCESS')
    for a,b in zip(started,completed):
        require(a['role']==b['role'] and type(a['historyIndex']) is int and type(b['historyIndex']) is int and
                b['historyIndex']>a['historyIndex'] and isinstance(a['nativeSource'],str) and
                0 < len(a['nativeSource']) <= 1048576,'ADAPTIVE_NATIVE_HISTORY_EVENT')
    diagnostics={};descriptors={};bindings={};measurements={}
    for phase in ('parent','current'):
        rows=report[phase]
        require(isinstance(rows,list) and 2<=len(rows)<=5 and len({r['role'] for r in rows})==len(rows) and
                {'RGB','L'}<={r['role'] for r in rows},'ADAPTIVE_NATIVE_TRACKS')
        descriptors[phase]=[];bindings[phase.upper()]={};measurements[phase]=[]
        for row in rows:
            # Parent artifacts can be in the preceding attempt; exact hashes bind them.
            artifact_root=directory if phase=='current' or m['permit']['ordinal']==0 else directory.parent
            path=safe_path(row['path'],artifact_root)
            h=safe_path(row['historyPath'],artifact_root)
            require(fingerprint(path)==row['sha256'] and fingerprint(h)==row['historySha256'], 'ADAPTIVE_NATIVE_OUTPUT_CHANGED')
            require(read(h)['historyIndex']>=0,'ADAPTIVE_HISTORY_REQUIRED')
            geometry,_,_=_image(path,0)
            require(all(geometry[k]==row[k] for k in ('width','height','channels')) and
                    [geometry['width'],geometry['height']]==m['preparation']['workingGeometry'], 'ADAPTIVE_NATIVE_OUTPUT_GEOMETRY')
            diagnostics[phase+'_'+row['role']]=analyze(path,expected_sha256=row['sha256'],image_index=0)
            binding={'sourceSha256':row['sha256'],'imageIndex':0,'width':row['width'],'height':row['height'],
                     'channels':row['channels'],'adapterSha256':m['measurementSha256'],
                     'starDetectorSha256':m['starDetectorSha256']}
            validate(row['measurement'],binding)
            require(row['measurement']['coreVersion']==m['coreVersion'],'ADAPTIVE_NATIVE_CORE_CHANGED')
            require(row['measurement']['regions']==m['regions'],'ADAPTIVE_NATIVE_REGION_CHANGED')
            descriptors[phase].append({k:row[k] for k in ('role','sha256','width','height','channels','historySha256')})
            if row['role'] in {'RGB','L'}:
                bindings[phase.upper()][row['role']]=binding
                measurements[phase].append({'role':row['role'],'report':row['measurement']})
    intermediate_rows=report['intermediates']
    require(isinstance(intermediate_rows,list) and len(intermediate_rows)<=3 and
            len({r['role'] for r in intermediate_rows})==len(intermediate_rows),'ADAPTIVE_INTERMEDIATE_TRACKS')
    for row in intermediate_rows:
        path=safe_path(row['path'],directory)
        history=safe_path(row['historyPath'],directory)
        require(fingerprint(path)==row['sha256'] and fingerprint(history)==row['historySha256'],
                'ADAPTIVE_INTERMEDIATE_CHANGED')
        geometry,_,_=_image(path,0)
        require(geometry['channels']==1 and
                [geometry['width'],geometry['height']]==m['preparation']['workingGeometry'],
                'ADAPTIVE_INTERMEDIATE_GEOMETRY')
        binding={'sourceSha256':row['sha256'],'imageIndex':0,'width':geometry['width'],
                 'height':geometry['height'],'channels':1,'adapterSha256':m['measurementSha256'],
                 'starDetectorSha256':m['starDetectorSha256']}
        validate(row['measurement'],binding)
        require(row['measurement']['coreVersion']==m['coreVersion'] and
                row['measurement']['regions']==m['regions'],'ADAPTIVE_INTERMEDIATE_RUNTIME_OR_REGION')
        require(read(history)['historyIndex']>=0,'ADAPTIVE_INTERMEDIATE_HISTORY')
        diagnostics['intermediate_'+row['role']]=analyze(path,expected_sha256=row['sha256'],image_index=0)
    current=copy.deepcopy(m['parentProvenance'])
    if m['permit']['step']['process']=='STRETCH':current['domain']='NONLINEAR_ATTESTED'
    current['recordSha256']=sha({'manifestSha256':expected_manifest_sha256,'eventsSha256':report['eventsSha256'],
                               'outputs':descriptors['current']})
    if any(o['role']=='MASK' for o in descriptors['current']):
        # Range and nonconstant support are technical checks, not mask adequacy.
        import numpy as np
        mask=next(r for r in report['current'] if r['role']=='MASK')
        geometry,_,offset=_image(Path(mask['path']),0)
        samples=np.memmap(mask['path'],dtype='<f4',mode='r',offset=offset,shape=(geometry['height'],geometry['width']))
        require(np.isfinite(samples).all() and 0<=float(samples.min())<float(samples.max())<=1,
                'ADAPTIVE_NATIVE_MASK_SUPPORT')
        del samples
        current['mask']='VERIFIED'
    v={'version':VERIFICATION_VERSION,'jobId':m['permit']['jobId'],'ordinal':m['permit']['ordinal'],
       'permitSha256':m['permitSha256'],'approvalSha256':m['approvalSha256'],
       'runtimeSha256':m['permit']['runtimeSha256'],'nativeManifestSha256':expected_manifest_sha256,
       'outputs':descriptors['current'],'parentOutputs':descriptors['parent'],
       'historySha256':sha([o['historySha256'] for o in descriptors['current']]),
       'sourceGuard':[{'role':s['role'],'sha256':s['sha256'],'imageIndex':s['imageIndex'],'unchanged':True} for s in m['sources']],
       'currentProvenance':current,'parentProvenance':m['parentProvenance'],
       'executedStep':m['permit']['step'],'status':'PHYSICALLY_VERIFIED'}
    result={'verification':v,'parentArtifacts':report['parent'],'currentArtifacts':report['current'],
            'measurements':measurements,'bindings':bindings,'diagnostics':diagnostics,
            'intermediateArtifacts':intermediate_rows}
    if write_receipt:
        with (directory/'verification.json').open('xb') as f:f.write(encode(result))
    else:
        require(read(safe_path(directory/'verification.json',directory))==result,'ADAPTIVE_SAVED_VERIFICATION_CHANGED')
    return result
