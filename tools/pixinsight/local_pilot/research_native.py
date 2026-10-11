"""Private exact-parent research attempts, fixed native code and read-only checks."""
import copy
import json
from pathlib import Path
import shutil
from .broker import require, encode
from .intake import sha
from .image_analysis import fingerprint
from .native_analysis import local_file
from .native_measurements import validate
from .source_provenance import _image
from .adaptive_native_adapter import read, safe_path, validate_runtime_files, require_installed_dependencies
from .research_photometry import inspect
from .research_contract import step, digest

VERSION='DSG_PIAI_RESEARCH_NATIVE_V1'


def validate_factory(runtime, factory=None):
    library=Path(__file__).parent
    require(runtime['executorSha256'] == sha({
        'controller':fingerprint(library/'adaptive_executor.jsh'),
        'factory':fingerprint(factory or library/'adaptive_native.jsh')}),
        'RESEARCH_APPROVED_FACTORY_CHANGED')


def prepare(directory, *, context, permit, sources, runtime_files, pixinsight_root,
            allowed_roots, background_roi, profile, native_lease, parent=None):
    state=context['state']; analysis=context['analysis']['analysis']
    require(state['approved'] and not state['cancelRequested'] and
            sha(state['policy']) == permit['policySha256'] and
            permit['parentId'] == state['selectedId'], 'RESEARCH_NATIVE_POLICY')
    step(permit['step'])
    require(sha(profile) == context['analysis']['instrument']['profileSha256'], 'RESEARCH_NATIVE_PROFILE_CHANGED')
    validate_runtime_files(analysis['runtime'],runtime_files)
    require_installed_dependencies(runtime_files,pixinsight_root)
    validate_factory(analysis['runtime'])
    directory=Path(directory);require(not directory.exists(), 'RESEARCH_ATTEMPT_ALREADY_EXISTS')
    safe_path(directory.parent,directory.parent.parent)
    directory.mkdir();(directory/'outputs').mkdir()
    guards=[]
    for source, descriptor in zip(sources,analysis['inputs']):
        require({k:source.get(k) for k in descriptor} == descriptor, 'RESEARCH_NATIVE_SOURCE_BINDING')
        path=local_file(source['path'],allowed_roots)
        require(fingerprint(path) == descriptor['sha256'], 'RESEARCH_ORIGINAL_CHANGED')
        guards.append({**descriptor,'source':path.as_posix()})
    require(len(guards) == len(analysis['inputs']), 'RESEARCH_NATIVE_SOURCE_COUNT')
    selected=sources if permit['parentId'] == 'CP000' else parent
    require(isinstance(selected,list) and [r['role'] for r in selected] ==
            (['R','G','B','L'] if permit['parentId'] == 'CP000' else ['RGB','L']), 'RESEARCH_EXACT_PARENT_ROLES')
    inputs=[]
    for row in selected:
        path=local_file(row['path'],allowed_roots+[str(directory.parent)])
        require(fingerprint(path) == row['sha256'], 'RESEARCH_PARENT_CHANGED')
        index=row.get('imageIndex',0);g,_,_=_image(path,index)
        require(all(g[k] == row[k] for k in ('width','height','channels')), 'RESEARCH_PARENT_GEOMETRY')
        target=directory/(row['role']+'.xisf');shutil.copyfile(path,target)
        require(fingerprint(target) == row['sha256'] == fingerprint(path), 'RESEARCH_PARENT_COPY')
        inputs.append({k:row[k] for k in ('role','sha256','width','height','channels')} |
                      {'imageIndex':index,'copy':target.as_posix()})
    library=Path(__file__).parent; runtime=copy.deepcopy(runtime_files)
    for name in ('research_executor.jsh','adaptive_native.jsh','measurements.jsh'):
        shutil.copyfile(library/name,directory/name)
        runtime.append({'path':(directory/name).as_posix(),'sha256':fingerprint(directory/name)})
    validate_factory(analysis['runtime'],directory/'adaptive_native.jsh')
    require(fingerprint(directory/'research_executor.jsh') == context['analysis']['executorSha256'] and
            fingerprint(directory/'measurements.jsh') == analysis['runtime']['measurementSha256'],
            'RESEARCH_EXECUTOR_SNAPSHOT_CHANGED')
    root=Path(pixinsight_root)
    for path,expected in ((root/'library/filters.xspd',profile['filtersSha256']),
                          (root/'library/white-references.xspd',profile['whiteSha256'])):
        require(fingerprint(path) == expected, 'RESEARCH_SPCC_LIBRARY_CHANGED')
        runtime.append({'path':path.as_posix(),'sha256':expected})
    width,height=inputs[0]['width'],inputs[0]['height']
    require(isinstance(background_roi,list) and len(background_roi) == 4 and
            all(type(n) is int for n in background_roi) and
            0 <= background_roi[0] < background_roi[2] <= width and
            0 <= background_roi[1] < background_roi[3] <= height and
            background_roi[2]-background_roi[0] >= 32 and background_roi[3]-background_roi[1] >= 32,
            'RESEARCH_BACKGROUND_ROI')
    require(analysis['evidence']['provenance']['backgroundROI'] == 'VERIFIED', 'RESEARCH_BACKGROUND_ATTESTATION')
    require(background_roi == context['analysis']['backgroundROI'],'RESEARCH_PINNED_BACKGROUND_CHANGED')
    # Internal native controller fields are host generated, never model supplied.
    native_permit={**permit,'jobId':'PIAI_'+state['requestId'],'ordinal':int(permit['checkpointId'][2:])-1}
    manifest={'version':VERSION,'permit':native_permit,'permitSha256':sha(permit),
        'sources':guards,'inputs':inputs,'runtimeFiles':runtime,
        'coreVersion':analysis['runtime']['coreVersion'],
        'measurementSha256':analysis['runtime']['measurementSha256'],
        'starDetectorSha256':analysis['runtime']['starDetectorSha256'],
        'context':{'mode':'LRGB','domain':state['checkpoints'][permit['parentId']]['domain'],
            'branch':'DIRECT','backgroundROI':background_roi,
            'models':{k:v['selectedVersion'] for k,v in analysis['runtime']['models'].items()}},
        'preparation':{'mode':'LRGB','rgbMapping':['R','G','B'],'luminance':{'role':'L'},'factor':1,'workingGeometry':[width,height]},
        'regions':[background_roi,[0,0,width,height]],'parentArtifacts':parent,
        'photometricProfile':copy.deepcopy(profile),'profileSha256':sha(profile),
        'outputDirectory':(directory/'outputs').as_posix(),'nativeLease':Path(native_lease).as_posix(),
        **{key:(directory/name).as_posix() for key,name in
           (('report','report.json'),('failure','failure.json'),('events','events.json'),('cancel','cancel.json'),('log','native.log'),('done','native-done.json'))}}
    # Start acknowledgement is written by the worker only after durable backend ACK.
    manifest['startAcknowledgement']=(directory/'start.json').as_posix()
    ack={'executeAllowed':True,'ordinal':native_permit['ordinal']}
    manifest['startAcknowledgementSha256']=__import__('hashlib').sha256(
        (json.dumps(ack,indent=2,allow_nan=False)+'\n').encode('utf-8')).hexdigest()
    with (directory/'manifest.json').open('xb') as stream:stream.write(encode(manifest))
    manifest_sha=fingerprint(directory/'manifest.json')
    lines=['#engine v8','#define __PJSR_USE_STAR_DETECTOR_V2','#include <pjsr/StarDetector.jsh>']
    lines += ['#include '+json.dumps((directory/name).as_posix()) for name in
              ('measurements.jsh','adaptive_native.jsh','research_executor.jsh')]
    lines += ['var m=JSON.parse(File.readTextFile('+json.dumps((directory/'manifest.json').as_posix())+'));',
              'DSGResearchExecute(m);']
    (directory/'run.js').write_bytes(('\r\n'.join(lines)+'\r\n').encode())
    (directory/'begin-log.js').write_bytes(('console.beginLog('+json.dumps((directory/'native.log').as_posix())+');\r\n').encode())
    (directory/'end-log.js').write_bytes(b'console.endLog();\r\n')
    return {'permit':permit,'permitSha256':sha(permit),'manifestSha256':manifest_sha,
            'launcherSha256':fingerprint(directory/'run.js'),'ack':ack}


def verify(directory, binding):
    import numpy as np
    directory=Path(directory);safe_path(directory,directory.parent)
    require(fingerprint(directory/'manifest.json') == binding['manifestSha256'], 'RESEARCH_MANIFEST_CHANGED')
    m=read(directory/'manifest.json');report=read(safe_path(directory/'report.json',directory))
    require(report['version'] == VERSION and report['status'] == 'NATIVE_SEGMENT_COMPLETE' and
            report['permitSha256'] == binding['permitSha256'] and
            read(directory/'native-done.json') == {'status':'OWNED_VIEWS_CLOSED','permitSha256':binding['permitSha256']} and
            report['eventsSha256'] == fingerprint(directory/'events.json') and report['sourceGuard'] == 'UNCHANGED',
            'RESEARCH_NATIVE_RECEIPT')
    for item in m['runtimeFiles']:
        require(fingerprint(Path(item['path'])) == item['sha256'],'RESEARCH_RUNTIME_CHANGED')
    guards=[]
    for row in m['sources']:
        require(fingerprint(Path(row['source'])) == row['sha256'], 'RESEARCH_ORIGINAL_CHANGED')
        guards.append({k:v for k,v in row.items() if k != 'source'} | {'unchanged':True})
    def check(rows):
        artifacts=[];measurements=[];bindings={};pixel_statistics={}
        require([r['role'] for r in rows] == ['RGB','L'], 'RESEARCH_NATIVE_TRACKS')
        for row in rows:
            path=local_file(row['path'],[str(directory.parent)])
            history=safe_path(row['historyPath'],directory.parent)
            require(fingerprint(path) == row['sha256'] and fingerprint(history) == row['historySha256'],
                    'RESEARCH_CHECKPOINT_CHANGED')
            g,_,offset=_image(path,0)
            require(all(g[k] == row[k] for k in ('width','height','channels')),'RESEARCH_CHECKPOINT_GEOMETRY')
            samples=np.memmap(path,dtype='<f4',mode='r',offset=offset,shape=(g['channels'],g['height'],g['width']))
            stats=[{'sampleCount':g['width']*g['height'],'negative':0,'overOne':0,'exactZero':0,'exactOne':0,
                    'minimum':None,'maximum':None} for _ in range(g['channels'])]
            for first in range(0,g['height'],128):
                block=samples[:,first:first+128,:]
                require(bool(np.isfinite(block).all()),'RESEARCH_NONFINITE_PIXELS')
                for channel,s in enumerate(stats):
                    values=block[channel];lo=float(values.min());hi=float(values.max())
                    s['minimum']=lo if s['minimum'] is None else min(lo,s['minimum'])
                    s['maximum']=hi if s['maximum'] is None else max(hi,s['maximum'])
                    for key,condition in (('negative',values < 0),('overOne',values > 1),
                                          ('exactZero',values == 0),('exactOne',values == 1)):
                        s[key] += int(np.count_nonzero(condition))
            del samples
            pixel_statistics[row['role']]=stats
            measured=row['measurement']
            b={k:measured[k] for k in ('sourceSha256','imageIndex','width','height','channels','adapterSha256','starDetectorSha256')}
            validate(measured,b);bindings[row['role']]=b
            measurements.append({'role':row['role'],'report':measured})
            artifacts.append({k:row[k] for k in ('role','sha256','width','height','channels','historySha256')})
        return artifacts,measurements,bindings,pixel_statistics
    parent,pm,pb,pp=check(report['parent']);current,cm,cb,cp=check(report['current'])
    photometry=None
    if binding['permit']['step']['process'] == 'SPCC':
        photometry=inspect(safe_path(directory/'outputs/SPCC-data.csv',directory).read_bytes(),
                          safe_path(directory/'native.log',directory).read_bytes(),
                          geometry=m['preparation']['workingGeometry'],profile_sha256=m['profileSha256'])
    return {'verification':{'status':'PHYSICALLY_VERIFIED','permitSha256':binding['permitSha256'],
        'nativeManifestSha256':binding['manifestSha256'],'nativeReportSha256':fingerprint(directory/'report.json'),
        'originalGuard':guards,'parentArtifacts':parent,'artifacts':current,
        'parentMeasurements':pm,'parentBindings':pb,'measurements':cm,'bindings':cb,
        'pixelStatistics':{'parent':pp,'current':cp},
        'photometricReceiptSha256':sha(photometry) if photometry else None,'photometry':photometry},
        'parentArtifacts':report['parent'],'currentArtifacts':report['current']}
