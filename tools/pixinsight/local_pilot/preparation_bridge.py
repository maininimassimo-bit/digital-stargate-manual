"""Bridge reviewed source preparation to a separately approved nonlinear job."""
import copy
from pathlib import Path

from . import preparation, worker
from .broker import decode, require
from .preparation_flow import source_digest, output_digest, effective_selection, sha
from .source_profile import source_profile, inspect_sources


def preparation_request(intake, options, mapping=None):
    fields={'canvas','shrink','feather','rationale','limitations'}
    require(isinstance(options,dict) and set(options)==fields,'PREPARATION_OPTIONS')
    selection,mappings=effective_selection(intake);profile=source_profile(selection)
    if profile['layout']=='SINGLE':mappings=[mapping] if mapping else None
    else:require(mapping is None,'APPROVED_SOURCE_MAPPING_REQUIRED')
    inspected=inspect_sources({'selection':selection},mappings)
    inputs=[];masters=[]
    for i,panel in enumerate(inspected['panels']):
        panel_id=profile['panels'][i]['panelId'] if profile['layout']=='PANELS' else 'P1'
        for row in panel['masters']:
            inputs.append({k:row[k] for k in ('role','path','sha256','imageIndex','width','height')}|{'panelId':panel_id})
            masters.append({k:row[k] for k in ('role','imageIndex','width','height')}|{'panelId':panel_id,'filename':Path(row['path']).name})
    request={k:profile[k] for k in ('mode','layout','bayerPattern')}
    request.update(schemaVersion='1.0',jobId='PREP_'+intake['selection']['requestId'],
                   canvas=options['canvas'],shrink=options['shrink'],feather=options['feather'],inputs=inputs)
    preparation.validate(request)
    proposal={k:request[k] for k in ('mode','layout','bayerPattern','canvas','shrink','feather')}
    proposal.update(sourceManifestSha256=source_digest(request),sourcePlanSha256=sha(intake['sourcePlan']) if profile['layout']=='PANELS' else None,
                    masters=masters,rationale=options['rationale'],limitations=options['limitations'])
    return request,proposal


def prepare_approved(root, intake, worker_id, mapping=None):
    require(intake.get('preparationApproved') is True and intake.get('preparationPlan'),'OWNER_PREPARATION_APPROVAL_REQUIRED')
    plan=intake['preparationPlan']
    require(sha(plan)==intake['preparationPlanSha256'] and plan['workerId']==worker_id,'OWNER_PREPARATION_PLAN_BINDING')
    request,proposal=preparation_request(intake,{k:plan[k] for k in ('canvas','shrink','feather','rationale','limitations')},mapping)
    require({**proposal,'workerId':worker_id}=={k:v for k,v in plan.items() if k not in {'nativeProcessCount','checkpointCount','verification'}},'OWNER_PREPARATION_SOURCES_CHANGED')
    job=preparation.prepare(root,request)
    worker.write_new(job/'owner-authorization.json',{'requestId':intake['selection']['requestId'],
        'preparationPlanSha256':intake['preparationPlanSha256'],'sourceManifestSha256':source_digest(request),
        'intake':copy.deepcopy(intake)})
    return job


def prepared_inputs(root, request_id):
    require(__import__('re').fullmatch(r'[a-f0-9]{32}',request_id or ''),'INTAKE_ID')
    root=Path(root).resolve(strict=True);job=root/('PREP_'+request_id)
    require(job.is_dir() and not job.is_symlink() and not job.is_junction(),'PREPARATION_BRIDGE_JOB_SCOPE')
    def read(name):
        path=job/name
        require(path.is_file() and not path.is_symlink() and not path.is_junction() and path.stat().st_size<=4*1024*1024,'PREPARATION_BRIDGE_ARTIFACT')
        return decode(path.read_bytes())
    manifest=read('manifest.json');verification=read('verification.json');authorization=read('owner-authorization.json')
    request=read('request.json');native=read('native-instances.json');reservation=read('reservation.json');closed=read('reservation-closed.json')
    require(reservation==closed and manifest['jobId']==verification['jobId']==request['jobId']==job.name and
            manifest['workerRoot']==root.as_posix() and manifest['jobDirectory']==job.as_posix(),'PREPARATION_BRIDGE_SCOPE')
    require(verification['schemaVersion']=='1.1' and verification['status']=='COMPLETED' and verification['originalIntegrity']=='UNCHANGED' and
            verification['nativeInstanceValidation']=='PARSED_AND_PARAMETERS_BOUND' and verification['nonLinear'] is False,'PREPARATION_VERIFIED_RESULT_REQUIRED')
    require(worker.digest(job/'manifest.json')==verification['manifestSha256'] and worker.digest(job/'terminal.json')==verification['terminalSha256'],'PREPARATION_BRIDGE_RECEIPT_INTEGRITY')
    require(verification['runtimeHashes']==manifest['runtimeHashes'] and all(worker.digest(job/name)==value for name,value in manifest['runtimeHashes'].items()),'PREPARATION_BRIDGE_RUNTIME_INTEGRITY')
    event_paths=sorted((job/'events').glob('*.json'))
    require({p.name:worker.digest(p) for p in event_paths}==verification['journalHashes'],'PREPARATION_BRIDGE_JOURNAL_INTEGRITY')
    require(worker.digest(job/'request.json')==manifest['requestSha256']==verification['requestSha256']==native['requestSha256'] and
            worker.digest(job/'native-instances.json')==verification['nativeInstancesSha256'],'PREPARATION_BRIDGE_INTEGRITY')
    plan=authorization['intake']['preparationPlan']
    require(authorization['requestId']==request_id and authorization['intake']['preparationApproved'] is True and
            authorization['preparationPlanSha256']==sha(plan)==authorization['intake']['preparationPlanSha256'] and
            authorization['sourceManifestSha256']==source_digest(request)==plan['sourceManifestSha256'],'PREPARATION_BRIDGE_AUTHORIZATION')
    selection=authorization['intake']['selection'];profile=selection['sourceProfile']
    require(all(request[k]==profile[k] for k in ('mode','layout','bayerPattern')),'PREPARATION_BRIDGE_PROFILE')
    if request['layout']=='PANELS':
        source_plan=authorization['intake']['sourcePlan']
        require(authorization['intake']['sourceSelectionApproved'] is True and sha(source_plan)==plan['sourcePlanSha256'],'PREPARATION_BRIDGE_SOURCE_APPROVAL')
        directories={p['panelId']:Path(p['directory']).resolve(strict=True) for p in source_plan['panels']}
    else:directories={'P1':Path(selection['masterDirectory']).resolve(strict=True)}
    require(len(plan['masters'])==len(request['inputs']),'PREPARATION_BRIDGE_MASTER_SCOPE')
    for source,descriptor in zip(request['inputs'],plan['masters']):
        require(all(source[k]==descriptor[k] for k in ('panelId','role','width','height','imageIndex')) and
                Path(source['path']).resolve(strict=True)==directories[source['panelId']]/descriptor['filename'],'PREPARATION_BRIDGE_SOURCE_DIRECTORY')
    preparation.validate(request)
    require(len(manifest['inputs'])==len(request['inputs']) and all(worker.digest(Path(row['path']))==row['sha256']==request['inputs'][i]['sha256'] for i,row in enumerate(manifest['inputs'])),'PREPARATION_BRIDGE_COPIES')
    terminal=read('terminal.json');spec=preparation.specification(request)
    require(terminal['status']=='COMPLETED' and terminal['processCount']==spec['nativeProcessCount'] and
            len(terminal['outputs'])==len(spec['outputs']) and {o['name'] for o in terminal['outputs']}==set(spec['outputs']),'PREPARATION_BRIDGE_COMPLETENESS')
    for output in terminal['outputs']:
        checkpoint=job/'outputs'/output['name']
        require(not checkpoint.is_symlink() and not checkpoint.is_junction() and worker.digest(checkpoint)==output['sha256'],'PREPARATION_BRIDGE_CHECKPOINT_CHANGED')
    inputs=[]
    for role in preparation.output_roles(request['mode']):
        name=f'{role}-mosaic-linear.xisf' if request['layout']=='PANELS' else 'RGB-linear.xisf'
        output=next((o for o in terminal['outputs'] if o['name']==name),None)
        require(output and output['nonLinear'] is False,'PREPARATION_BRIDGE_OUTPUT')
        path=job/'outputs'/name
        require(not path.is_symlink() and not path.is_junction() and worker.digest(path)==output['sha256'],'PREPARATION_BRIDGE_OUTPUT_CHANGED')
        require(verification['pixelVerification'][name]['allFinite'] is True and verification['pixelVerification'][name]['normalizedRange'] is True,'PREPARATION_BRIDGE_PIXELS')
        inputs.append({'role':role,'path':path.as_posix(),'sha256':output['sha256'],'imageIndex':0,'width':output['width'],'height':output['height']})
    trace={'requestId':request_id,'preparationPlanSha256':sha(plan),'sourceManifestSha256':source_digest(request),
           'verificationSha256':worker.digest(job/'verification.json'),'nativeInstancesSha256':worker.digest(job/'native-instances.json'),
           'outputManifestSha256':output_digest(inputs)}
    return inputs,trace


def result_packet(root, intake, worker_id):
    request_id=intake['selection']['requestId'];inputs,trace=prepared_inputs(root,request_id)
    require(intake.get('preparationApproved') is True and intake['preparationPlanSha256']==trace['preparationPlanSha256'],'PREPARATION_REMOTE_APPROVAL_BINDING')
    return {'workerId':worker_id,**{k:v for k,v in trace.items() if k!='requestId'},
            'masters':[{k:row[k] for k in ('role','width','height','imageIndex')} for row in inputs],
            'nativeProcessCount':intake['preparationPlan']['nativeProcessCount'],'checkpointCount':intake['preparationPlan']['checkpointCount']}


def verify_trace(root, request):
    trace=request['preparationTrace']
    inputs,expected=prepared_inputs(root,trace['requestId'])
    require(trace==expected and request['inputs']==inputs,'PREPARATION_PROCESSING_INPUT_BINDING')
    return expected


def runtime_graph(root, trace):
    """Verified preparation instances plus PJSR edges; strip local file paths."""
    import hashlib
    import json
    from tools.pixinsight.workflow_archive.export_parser import TOKEN
    inputs,expected=prepared_inputs(root,trace['requestId'])
    require(trace==expected,'PREPARATION_RUNTIME_TRACE')
    job=Path(root)/('PREP_'+trace['requestId'])
    manifest=decode((job/'manifest.json').read_bytes())
    events=[decode(p.read_bytes()) for p in sorted((job/'events').glob('*.json'))]
    starts=[e['data'] for e in events if e['event']=='process-started'];completed=[e['data'] for e in events if e['event']=='process-completed']
    preparation.validate_native_instances(manifest,starts)
    aliases={(job/'outputs'/name).as_posix():'PREP_'+name.removesuffix('.xisf').replace('-','_') for name in manifest['expectedOutputs']}
    source_roles={row['sha256']:'MASTER_'+row['role']+'_'+row['panelId'].replace('-','_') for row in manifest['inputs']}
    instances=[];relations=[]
    for i,(start,end) in enumerate(zip(starts,completed),1):
        raw=start['nativeSource']
        # Only literal native checkpoint paths become explicit logical resource
        # references in the export. The exact raw source remains in local events.
        derived=''.join(json.dumps(aliases[json.loads(t.group())]+'.xisf') if t.lastgroup=='string' and json.loads(t.group()) in aliases else t.group() for t in TOKEN.finditer(raw))
        dependencies=[aliases[p] for p in start['dependencies']] if start['process']=='GradientMergeMosaic' else [start['target']]
        instances.append({'label':'preparation-'+str(i),'process':start['process'],'target':end['target'],
                          'dependencies':dependencies,'nativeSource':derived,'nativeSourceSha256':hashlib.sha256(raw.encode()).hexdigest()})
    for event in events:
        row=event['data'];name=event['event']
        if name=='source-selected':relations.append({'event':'preparation-source','target':row['target'],'dependencies':['MASTER_'+row['role']+'_'+row['panelId'].replace('-','_')],'role':row['role'],'panelId':row['panelId']})
        elif name=='astrometric-reprojection':relations.append({'event':name,'target':aliases[row['output']],'dependencies':[row['sourceView']],'role':row['role'],'panelId':row['panelId'],'canvas':row['canvas'],'method':row['method']})
        elif name=='astrometric-metadata-transfer':relations.append({'event':name,'target':row['target'],'dependencies':[row['source']],'panelId':row['panelId'],'geometryUnchanged':True})
        elif name=='sample-format-conversion':relations.append({'event':name,'target':row['target'],'dependencies':[row['target']],'role':row['role'],'fromBits':64,'toBits':32,'method':row['method']})
    for item in inputs:
        target=next(r['target'] for r in reversed(completed) if r.get('role')==item['role'])
        relations.append({'event':'prepared-linear-master','target':'PREPARED_'+item['role'],'dependencies':[target],
                          'role':item['role'],'nonLinear':False})
    return instances,relations,source_roles
