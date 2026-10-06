"""Bounded local master-preparation contract; no portal dispatch or native launch."""
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import uuid

from .source_profile import MODES, PATTERNS, image_metadata
from .worker import digest, require, write_new

INSTALLED_ENGINE = Path('C:/Program Files/PixInsight/src/scripts/MosaicByCoordinates/MosaicByCoordinatesEngine.js')


def output_roles(mode):
    return ('RGB',) if mode == 'OSC_CFA' else MODES[mode]


def specification(request):
    """Deterministic checkpoint/process envelope, derived from the exact selection."""
    panels = list(dict.fromkeys(row['panelId'] for row in request['inputs']))
    roles = output_roles(request['mode'])
    outputs = {}
    if request['mode'] == 'OSC_CFA':
        outputs.update({f'RGB-{panel}-debayer.xisf':3 for panel in panels})
    if request['layout'] == 'PANELS':
        for role in roles:
            channels = 3 if role == 'RGB' else 1
            outputs.update({f'{role}-{panel}-registered.xisf':channels for panel in panels})
            outputs[f'{role}-mosaic-linear.xisf'] = channels
    else:
        outputs['RGB-linear.xisf'] = 3
    count = (len(panels) if request['mode'] == 'OSC_CFA' else 0) + (len(roles) if request['layout'] == 'PANELS' else 0)
    return {'panels':panels,'roles':roles,'outputs':outputs,'nativeProcessCount':count}


def validate(request, *, verify_files=True):
    fields = {'schemaVersion','jobId','mode','layout','bayerPattern','canvas','shrink','feather','inputs'}
    require(isinstance(request,dict) and set(request) == fields, 'PREPARATION_FIELDS')
    require(request['schemaVersion'] == '1.0' and isinstance(request['jobId'],str) and
            re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,47}',request['jobId']), 'PREPARATION_ID')
    require(isinstance(request['mode'],str) and request['mode'] in MODES and
            isinstance(request['layout'],str) and request['layout'] in {'SINGLE','PANELS'}, 'PREPARATION_PROFILE')
    require((isinstance(request['bayerPattern'],str) and request['bayerPattern'] in PATTERNS) if request['mode']=='OSC_CFA' else request['bayerPattern'] is None,
            'EXPLICIT_BAYER_PATTERN_REQUIRED')
    if request['layout'] == 'SINGLE':
        require(request['mode']=='OSC_CFA' and request['canvas'] is None and
                type(request['shrink']) is int and request['shrink']==0 and
                type(request['feather']) is int and request['feather']==0, 'SINGLE_CFA_PREPARATION_ONLY')
    else:
        canvas=request['canvas']
        require(isinstance(canvas,dict) and set(canvas)=={'centerRA','centerDec','resolution','rotation','width','height'}, 'PREPARATION_CANVAS')
        bounds={'centerRA':(0,360),'centerDec':(-90,90),'resolution':(0,0.01),'rotation':(-360,360)}
        for key,(low,high) in bounds.items():
            n=canvas[key]
            require(type(n) in (int,float) and math.isfinite(n) and low <= n <= high, 'PREPARATION_CANVAS_BOUNDS')
        require(canvas['centerRA']<360 and canvas['resolution']>0, 'PREPARATION_CANVAS_BOUNDS')
        require(type(canvas['width']) is int and type(canvas['height']) is int and
                1000<=canvas['width']<=12000 and 800<=canvas['height']<=12000, 'PREPARATION_GEOMETRY')
        require(type(request['shrink']) is int and 0<=request['shrink']<=5 and
                type(request['feather']) is int and 1<=request['feather']<=100, 'PREPARATION_MERGE_BOUNDS')
    inputs=request['inputs']
    require(isinstance(inputs,list) and 1<=len(inputs)<=64, 'PREPARATION_INPUT_COUNT')
    seen=set();panels=[];geometry={}
    for row in inputs:
        require(isinstance(row,dict) and set(row)=={'panelId','role','path','sha256','imageIndex','width','height'}, 'PREPARATION_INPUT_FIELDS')
        panel=row['panelId']
        require(isinstance(panel,str) and re.fullmatch(r'[A-Za-z0-9_-]{1,40}',panel), 'PREPARATION_PANEL_ID')
        if panel not in panels:panels.append(panel)
        require(isinstance(row['role'],str) and row['role'] in MODES[request['mode']], 'PREPARATION_INPUT_ROLE')
        require(isinstance(row['sha256'],str) and re.fullmatch(r'[a-f0-9]{64}',row['sha256']), 'PREPARATION_INPUT_DIGEST')
        require(type(row['imageIndex']) is int and 0<=row['imageIndex']<16 and
                type(row['width']) is int and type(row['height']) is int and
                1<=row['width']<=12000 and 1<=row['height']<=12000, 'PREPARATION_INPUT_GEOMETRY')
        require(isinstance(row['path'],str) and Path(row['path']).is_absolute(), 'PREPARATION_ABSOLUTE_INPUT')
        identity=(str(Path(row['path'])).casefold(),row['imageIndex'])
        require(identity not in seen, 'PREPARATION_SOURCE_REUSE');seen.add(identity)
        pair=(row['width'],row['height'])
        require(panel not in geometry or geometry[panel]==pair, 'PREPARATION_PANEL_GEOMETRY')
        geometry[panel]=pair
        if verify_files:
            path=Path(row['path'])
            require(path.is_file() and path.suffix.lower()=='.xisf' and not path.is_symlink() and not path.is_junction(), 'PREPARATION_SOURCE_FILE')
            require(digest(path)==row['sha256'], 'PREPARATION_SOURCE_CHANGED')
            metadata=image_metadata(path,request['mode'],row['imageIndex'])
            require((metadata['width'],metadata['height'])==pair, 'PREPARATION_SOURCE_HEADER')
    require(len(panels)==1 if request['layout']=='SINGLE' else 2<=len(panels)<=16, 'PREPARATION_PANEL_COUNT')
    require([(r['panelId'],r['role']) for r in inputs]==[(p,r) for p in panels for r in MODES[request['mode']]], 'PREPARATION_ROLE_ORDER')
    return specification(request)


def prepare(root, request):
    """Create a private immutable local preparation job; never launch PixInsight.

    Portal Owner approval and dispatch are separate, currently gated contracts.
    This local job cannot be reported as an approved scientific portal job.
    """
    spec=validate(request)
    root=Path(root)
    require(root.is_dir() and not root.is_symlink() and not root.is_junction(),'PREPARATION_ROOT')
    root=root.resolve(strict=True)
    engine=INSTALLED_ENGINE.resolve(strict=True)
    require(engine.is_file() and engine.name=='MosaicByCoordinatesEngine.js','PREPARATION_INSTALLED_ENGINE')
    sources=[Path(row['path']).resolve(strict=True) for row in request['inputs']]
    require(all(root not in p.parents and p.parent not in root.parents and root!=p.parent for p in sources),'PREPARATION_SEPARATE_SOURCES')
    require(len({(p,row['imageIndex']) for p,row in zip(sources,request['inputs'])})==len(sources),'PREPARATION_SOURCE_REUSE')
    job=root/request['jobId'];require(not job.exists(),'PREPARATION_NO_OVERWRITE')
    normalized=copy.deepcopy(request)
    for row,source in zip(normalized['inputs'],sources):row['path']=source.as_posix()
    raw_request=(json.dumps(normalized,indent=2,allow_nan=False)+'\n').encode('utf-8')
    reservation={'schemaVersion':'1.0','jobId':request['jobId'],'token':uuid.uuid4().hex,
                 'authority':'LOCAL_SOURCE_PREPARATION_NOT_OWNER_PORTAL_JOB',
                 'requestSha256':hashlib.sha256(raw_request).hexdigest()}
    write_new(root/'active-job.json',reservation)
    try:
        job.mkdir();write_new(job/'reservation.json',reservation)
        with (job/'request.json').open('xb') as stream:stream.write(raw_request)
        for name in ('inputs','outputs','events'):(job/name).mkdir()
        inputs=[]
        for source,row in zip(sources,request['inputs']):
            target=job/'inputs'/f"{row['role']}-{row['panelId']}.xisf"
            with source.open('rb') as incoming,target.open('xb') as outgoing:shutil.copyfileobj(incoming,outgoing,1024*1024)
            require(digest(source)==row['sha256']==digest(target),'PREPARATION_SOURCE_COPY_INTEGRITY')
            inputs.append({**row,'path':target.as_posix(),'sourcePath':source.as_posix()})
        runtime={}
        for name in ('source_preparation.jsh','preparation_executor.jsh'):
            path=job/name
            with Path(__file__).with_name(name).open('rb') as incoming,path.open('xb') as outgoing:shutil.copyfileobj(incoming,outgoing)
            runtime[name]=digest(path)
        manifest={**request,**reservation,'inputs':inputs,'workerRoot':root.as_posix(),'jobDirectory':job.as_posix(),
                  'runtimeHashes':runtime,'enginePath':engine.as_posix(),'engineSha256':digest(engine),
                  'expectedOutputs':spec['outputs'],'nativeProcessCount':spec['nativeProcessCount']}
        write_new(job/'manifest.json',manifest)
        includes=['#engine v8','#define TITLE "DSG master preparation"','#define VERSION "1.0"',
                  '#define SETTINGS_MODULE "DSG_Master_Preparation"',
                  '#include <pjsr/astrometry/AstrometricMetadata.js>',
                  '#include <pjsr/astrometry/ImageReprojection.js>',
                  '#include <pjsr/astrometry/ProjectionConfigurationDialog.js>',
                  '#include '+json.dumps(engine.as_posix())]
        includes+=['#include '+json.dumps((job/name).as_posix()) for name in runtime]
        launcher='\n'.join(includes)+'\nDSGExecuteMasterPreparation(JSON.parse(File.readTextFile('+json.dumps((job/'manifest.json').as_posix())+')));\n'
        with (job/'run.js').open('x',encoding='utf-8',newline='\r\n') as stream:stream.write(launcher)
        return job
    except Exception:
        if job.is_dir():write_new(job/'preparation-failed.json',{'status':'PREPARATION_FAILED','authority':reservation['authority']})
        raise


def collect(root, job_id):
    """Independently verify a completed local stage; retain lease on any conflict.

    This is technical preparation evidence, never a portal or scientific approval.
    Native instance parsing and portal delivery are separate pending contracts.
    """
    from .quality import inspect_pixels
    from .worker import xisf_header
    require(isinstance(job_id,str) and re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,47}',job_id),'PREPARATION_ID')
    root=Path(root).resolve(strict=True);job=root/job_id
    require(job.is_dir() and not job.is_symlink() and not job.is_junction(),'PREPARATION_JOB_SCOPE')
    def read(path):
        require(path.is_file() and not path.is_symlink() and not path.is_junction(),'PREPARATION_ARTIFACT_SCOPE')
        require(path.stat().st_size<=4*1024*1024,'PREPARATION_ARTIFACT_SIZE')
        return json.loads(path.read_text(encoding='utf-8'))
    request=read(job/'request.json');spec=validate(request)
    manifest=read(job/'manifest.json');receipt=read(job/'terminal.json');reservation=read(job/'reservation.json')
    require(request['jobId']==manifest['jobId']==receipt['jobId']==reservation['jobId']==job_id,'PREPARATION_RECEIPT_ID')
    require(manifest['workerRoot']==root.as_posix() and manifest['jobDirectory']==job.as_posix(),'PREPARATION_MANIFEST_SCOPE')
    require(manifest['authority']==receipt['authority']==reservation['authority']=='LOCAL_SOURCE_PREPARATION_NOT_OWNER_PORTAL_JOB','PREPARATION_AUTHORITY')
    require(manifest['token']==receipt['token']==reservation['token'],'PREPARATION_RECEIPT_TOKEN')
    require(digest(job/'request.json')==manifest['requestSha256']==receipt['requestSha256']==reservation['requestSha256'],'PREPARATION_REQUEST_DIGEST')
    require(all(manifest[k]==request[k] for k in request if k!='inputs'),'PREPARATION_IMMUTABLE_PARAMETERS')
    require(manifest['expectedOutputs']==spec['outputs'] and manifest['nativeProcessCount']==spec['nativeProcessCount'],'PREPARATION_ENVELOPE')
    require(len(manifest['inputs'])==len(request['inputs']),'PREPARATION_INPUT_BINDING')
    for source,copied in zip(request['inputs'],manifest['inputs']):
        expected={**source,'sourcePath':source['path'],'path':(job/'inputs'/f"{source['role']}-{source['panelId']}.xisf").as_posix()}
        require(copied==expected,'PREPARATION_INPUT_BINDING')
        copy_path=Path(copied['path'])
        require(not copy_path.is_symlink() and digest(copy_path)==source['sha256'],'PREPARATION_COPY_INTEGRITY')
    require(set(manifest['runtimeHashes'])=={'source_preparation.jsh','preparation_executor.jsh'} and receipt['runtimeHashes']==manifest['runtimeHashes'],'PREPARATION_RUNTIME_BINDING')
    for name,sha in manifest['runtimeHashes'].items():
        require(digest(job/name)==sha,'PREPARATION_RUNTIME_INTEGRITY')
    require(Path(manifest['enginePath']).resolve(strict=True)==INSTALLED_ENGINE.resolve(strict=True) and digest(INSTALLED_ENGINE)==manifest['engineSha256']==receipt['engineSha256'],'PREPARATION_ENGINE_BINDING')
    require(receipt['status']=='COMPLETED' and receipt['recipe']=='MASTER_PREPARATION_V1' and receipt['exclusiveLeaseVerified'] is True and receipt['originalIntegrity']=='UNCHANGED','PREPARATION_COMPLETION_REQUIRED')
    require(receipt['nonLinear'] is False and type(receipt['providerRequests']) is int and receipt['providerRequests']==0 and type(receipt['processCount']) is int and receipt['processCount']==spec['nativeProcessCount'],'PREPARATION_PROCESS_COMPLETENESS')
    event_paths=sorted((job/'events').glob('*.json'))
    require(1<=len(event_paths)<=512 and [p.name for p in event_paths]==[f'{i:04d}.json' for i in range(1,len(event_paths)+1)],'PREPARATION_EVENT_SEQUENCE')
    events=[read(p) for p in event_paths]
    allowed={'source-selected','process-started','process-completed','checkpoint','astrometric-reprojection','astrometric-metadata-transfer','sample-format-conversion'}
    require(all(set(e)=={'event','data'} and e['event'] in allowed and isinstance(e['data'],dict) for e in events),'PREPARATION_EVENT_FIELDS')
    selected=[e['data'] for e in events if e['event']=='source-selected']
    require(len(selected)==len(request['inputs']),'PREPARATION_SOURCE_LINEAGE')
    expected_sources={(r['panelId'],r['role']):(r['imageIndex'],r['sha256']) for r in request['inputs']}
    observed={}
    for row in selected:
        key=(row['panelId'],row['role'])
        require(key in expected_sources and key not in observed and (row['imageIndex'],row['sourceSha256'])==expected_sources[key] and isinstance(row['target'],str) and row['target'],'PREPARATION_SOURCE_LINEAGE')
        observed[key]=row['target']
    starts=[e['data'] for e in events if e['event']=='process-started']
    completions=[e['data'] for e in events if e['event']=='process-completed']
    expected_processes=[]
    if request['mode']=='OSC_CFA':expected_processes.extend(('Debayer','RGB',p) for p in spec['panels'])
    if request['layout']=='PANELS':expected_processes.extend(('GradientMergeMosaic',r,None) for r in spec['roles'])
    identity=lambda r:(r['process'],r['role'],r.get('panelId'))
    require([identity(r) for r in starts]==expected_processes==[identity(r) for r in completions],'PREPARATION_NATIVE_ORDER')
    require(all(isinstance(r.get('nativeSource'),str) and 0<len(r['nativeSource'])<=1024*1024 for r in starts),'PREPARATION_NATIVE_SOURCE')
    pending=None
    for event in events:
        if event['event']=='process-started':
            require(pending is None,'PREPARATION_NATIVE_SEQUENCE');pending=identity(event['data'])
        elif event['event']=='process-completed':
            require(pending==identity(event['data']),'PREPARATION_NATIVE_SEQUENCE');pending=None
    require(pending is None,'PREPARATION_NATIVE_SEQUENCE')
    native_instances=validate_native_instances(manifest,starts)
    for started,completed in zip(starts,completions):
        require(isinstance(completed.get('target'),str) and completed['target'],'PREPARATION_NATIVE_TARGET')
        if started['process']=='Debayer':
            require(started['target']==observed[(started['panelId'],'CFA')] and started['pattern']==completed['pattern']==request['bayerPattern'],'PREPARATION_CFA_LINEAGE')
        else:
            require(started['dependencies']==[(job/'outputs'/f"{started['role']}-{p}-registered.xisf").as_posix() for p in spec['panels']],'PREPARATION_MERGE_DEPENDENCIES')
    warps=[e['data'] for e in events if e['event']=='astrometric-reprojection']
    require([(r['role'],r['panelId']) for r in warps]==([(r,p) for r in spec['roles'] for p in spec['panels']] if request['layout']=='PANELS' else []),'PREPARATION_WARP_ORDER')
    debayer_targets={r['panelId']:r['target'] for r in completions if r['process']=='Debayer'}
    transfers=[e['data'] for e in events if e['event']=='astrometric-metadata-transfer']
    expected_transfers=spec['panels'] if request['mode']=='OSC_CFA' and request['layout']=='PANELS' else []
    require([r['panelId'] for r in transfers]==expected_transfers,'PREPARATION_METADATA_TRANSFER_ORDER')
    for transfer in transfers:
        require(transfer['source']==observed[(transfer['panelId'],'CFA')] and transfer['target']==debayer_targets[transfer['panelId']] and transfer['geometryUnchanged'] is True,'PREPARATION_METADATA_TRANSFER_LINEAGE')
    conversions=[e['data'] for e in events if e['event']=='sample-format-conversion']
    merged=[r for r in completions if r['process']=='GradientMergeMosaic']
    require(all(type(r.get('bitsPerSample')) is int and r['bitsPerSample'] in (32,64) for r in merged),'PREPARATION_MERGE_SAMPLE_FORMAT')
    require([r['role'] for r in conversions]==[r['role'] for r in merged if r['bitsPerSample']==64],'PREPARATION_CONVERSION_ORDER')
    for conversion in conversions:
        completed=next(r for r in merged if r['role']==conversion['role'])
        require(conversion['target']==completed['target'] and conversion['fromBits']==64 and conversion['toBits']==32 and conversion['method']=='ImageWindow.setSampleFormat','PREPARATION_CONVERSION_LINEAGE')
    for warp in warps:
        target=debayer_targets[warp['panelId']] if request['mode']=='OSC_CFA' else observed[(warp['panelId'],warp['role'])]
        require(warp['sourceView']==target and warp['canvas']==request['canvas'] and warp['method']=='PJSR_IMAGE_REPROJECTION_1_4_4_NO_SOURCE_OFFSET' and warp['output']==(job/'outputs'/f"{warp['role']}-{warp['panelId']}-registered.xisf").as_posix(),'PREPARATION_WARP_LINEAGE')
    outputs=receipt['outputs'];names=[o['name'] for o in outputs]
    require(len(names)==len(set(names)) and set(names)==set(spec['outputs']),'PREPARATION_OUTPUT_COMPLETENESS')
    require([e['data'] for e in events if e['event']=='checkpoint']==outputs,'PREPARATION_CHECKPOINT_BINDING')
    quality={}
    for output in outputs:
        name=output['name'];path=job/'outputs'/name;channels=spec['outputs'][name]
        source=next(r for r in request['inputs'] if name==f"RGB-{r['panelId']}-debayer.xisf") if name.endswith('-debayer.xisf') else request['inputs'][0]
        width,height=(request['canvas']['width'],request['canvas']['height']) if request['layout']=='PANELS' and not name.endswith('-debayer.xisf') else (source['width'],source['height'])
        require(not path.is_symlink() and not path.is_junction() and digest(path)==output['sha256'],'PREPARATION_OUTPUT_INTEGRITY')
        require(output['nonLinear'] is False and (output['width'],output['height'],output['channels'])==(width,height,channels),'PREPARATION_OUTPUT_DOMAIN')
        require(xisf_header(path)==dict(width=width,height=height,channels=channels,sampleFormat='Float32',colorSpace='RGB' if channels==3 else 'Gray'),'PREPARATION_OUTPUT_HEADER')
        quality[name]=inspect_pixels(path,expected_channels=channels)
        require(digest(path)==output['sha256'],'PREPARATION_OUTPUT_CHANGED_DURING_VERIFICATION')
    require(all(digest(Path(r['path']))==r['sha256'] for r in request['inputs']),'PREPARATION_SOURCE_CHANGED_DURING_VERIFICATION')
    native_path=job/'native-instances.json'
    native_value={'schemaVersion':'1.0','jobId':job_id,'requestSha256':manifest['requestSha256'],
                  'instances':native_instances,'upstreamHistoryCompleteness':'NOT_ESTABLISHED'}
    if native_path.exists():require(read(native_path)==native_value,'PREPARATION_NATIVE_ARTIFACT_CONFLICT')
    else:write_new(native_path,native_value)
    result={'schemaVersion':'1.1','jobId':job_id,'status':'COMPLETED','authority':manifest['authority'],
            'manifestSha256':digest(job/'manifest.json'),'terminalSha256':digest(job/'terminal.json'),
            'runtimeHashes':manifest['runtimeHashes'],'engineSha256':manifest['engineSha256'],
            'journalHashes':{p.name:digest(p) for p in event_paths},
            'requestSha256':manifest['requestSha256'],'originalIntegrity':'UNCHANGED','outputCount':len(outputs),
            'nativeProcessCount':len(starts),'pixelVerification':quality,'nonLinear':False,'providerRequests':0,
            'scientificAcceptance':'OWNER_REVIEW_REQUIRED','portalApproval':'NOT_ESTABLISHED',
            'workflowCompleteness':'UPSTREAM_NOT_ESTABLISHED','nativeInstanceValidation':'PARSED_AND_PARAMETERS_BOUND',
            'nativeInstancesSha256':digest(native_path)}
    active=root/'active-job.json';closed=job/'reservation-closed.json'
    if active.exists():require(read(active)==reservation and not closed.exists(),'PREPARATION_ACTIVE_RESERVATION')
    else:require(read(closed)==reservation,'PREPARATION_CLOSED_RESERVATION')
    verification=job/'verification.json'
    if verification.exists():require(read(verification)==result,'PREPARATION_VERIFICATION_CONFLICT')
    else:write_new(verification,result)
    if active.exists():
        require(read(active)==reservation and not closed.exists(),'PREPARATION_ACTIVE_RESERVATION')
        active.rename(closed)
    else:require(read(closed)==reservation,'PREPARATION_CLOSED_RESERVATION')
    return result


def validate_native_instances(manifest, starts):
    """Parse native source as data, bind preparation parameters; never execute JS."""
    from tools.pixinsight.workflow_archive.export_parser import parse_export
    from decimal import Decimal
    verified=[]
    for row in starts:
        parsed=parse_export(row['nativeSource'],profile='1.2')
        instances=list(parsed['instances'].values())
        require(len(instances)==1 and instances[0]['process']==row['process'] and not instances[0]['children'] and not instances[0]['maskCommands'],'PREPARATION_NATIVE_INSTANCE')
        parameters=instances[0]['parameters']
        def numeric(key, expected):
            value=parameters.get(key)
            require(isinstance(value,dict) and value.get('kind')=='number' and Decimal(value['literal'])==Decimal(str(expected)),'PREPARATION_NATIVE_PARAMETER')
        def enum(key, owner, member):
            require(parameters.get(key)=={'kind':'enum','owner':owner,'member':member},'PREPARATION_NATIVE_PARAMETER')
        if row['process']=='GradientMergeMosaic':
            require(set(parameters)=={'targetFrames','type','nShrinkCount','nFeatherRadius','blackPoint','generateMask'},'PREPARATION_NATIVE_PARAMETER_SCOPE')
            require(parameters['targetFrames']==[[True,p] for p in row['dependencies']],'PREPARATION_NATIVE_FRAME_BINDING')
            enum('type','GradientMergeMosaic','Average');numeric('nShrinkCount',manifest['shrink'])
            numeric('nFeatherRadius',manifest['feather']);numeric('blackPoint',0)
            require(parameters['generateMask'] is False,'PREPARATION_NATIVE_PARAMETER')
        elif row['process']=='Debayer':
            enum('cfaPattern','Debayer',manifest['bayerPattern']);enum('debayerMethod','Debayer','VNG')
            numeric('fbddNoiseReduction',0)
            for key,value in {'evaluateNoise':False,'evaluateSignal':False,'showImages':False,'outputRGBImages':True,'outputSeparateChannels':False,'generateHistoryProperties':True,'generateFITSKeywords':True}.items():
                require(parameters.get(key) is value,'PREPARATION_NATIVE_PARAMETER')
        else:require(False,'PREPARATION_NATIVE_PROCESS')
        verified.append({'process':row['process'],'role':row['role'],'panelId':row.get('panelId'),'sourceSha256':parsed['sourceSha256'],'parametersBound':True})
    return verified
