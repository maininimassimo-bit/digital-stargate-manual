"""Explicit SESSION_ASSISTED inspection/proposal; never executes prompt text or starts PixInsight."""
import argparse
import copy
import os
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET

from . import worker
from .broker import decode, encode, opaque, require
from .intake import local_directory
from .scientific_delivery import registry_digest
from .transport import Transport
from .source_profile import inspect_sources, source_profile, inventory_sources, selected_panels


ALIASES = {'R': {'r', 'red', 'rosso'}, 'G': {'g', 'green', 'verde'},
           'B': {'b', 'blue', 'blu'}, 'L': {'l', 'lum', 'luminance', 'luminanza'}}


def master_metadata(path, image_index=None):
    with path.open('rb') as stream:
        require(stream.read(8) == b'XISF0100', 'MASTER_XISF')
        length,reserved = struct.unpack('<II', stream.read(8))
        require(0 < length <= 4 * 1024 * 1024 and reserved==0, 'MASTER_HEADER_LIMIT')
        raw = stream.read(length)
    require(len(raw) == length and b'<!DOCTYPE' not in raw and b'<!ENTITY' not in raw, 'MASTER_HEADER')
    images = [e for e in ET.fromstring(raw) if e.tag.split('}')[-1] == 'Image']
    require(1 <= len(images) <= 16, 'MASTER_IMAGES')
    if image_index is None:
        require(len(images) == 1, 'MULTI_IMAGE_REQUIRES_EXPLICIT_INDEX')
        image_index = 0
    require(type(image_index) is int and 0 <= image_index < len(images), 'MASTER_IMAGE_INDEX')
    image = images[image_index]
    require(image.get('id') not in {'rejection_low','rejection_high','slope_map','weight_map'},'AUXILIARY_IMAGE_NOT_MASTER')
    geometry = image.get('geometry', '').split(':')
    require(len(geometry) == 3 and all(re.fullmatch(r'[0-9]+', x) for x in geometry), 'MASTER_GEOMETRY')
    width, height, channels = map(int, geometry)
    require(channels == 1 and image.get('sampleFormat') == 'Float32' and image.get('colorSpace') == 'Gray', 'MONO_FLOAT32_REQUIRED')
    return {'imageIndex': image_index, 'width': width, 'height': height}


def inspect(intake, mapping=None):
    """Only the explicitly selected local folder, no recursive scan or network path."""
    directory = Path(local_directory(intake['selection']['masterDirectory'])).resolve(strict=True)
    local_directory(str(directory))
    require(directory.is_dir(), 'MASTER_DIRECTORY_MISSING')
    mapping = mapping or {}
    require(isinstance(mapping, dict) and (not mapping or set(mapping) == set(worker.ROLES)), 'ROLE_MAPPING')
    rows = []
    for role in worker.ROLES:
        if mapping:
            entry = mapping[role]
            require(isinstance(entry, dict) and set(entry) == {'filename', 'imageIndex'}, 'ROLE_MAPPING')
            name = entry['filename']
            require(isinstance(name, str) and name not in {'.', '..'} and '/' not in name and '\\' not in name and ':' not in name,
                    'ROLE_FILENAME')
            path = directory / name
            index = entry['imageIndex']
        else:
            candidates = [p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == '.xisf' and
                          set(re.findall(r'[a-z0-9]+', p.stem.lower())) & ALIASES[role]]
            require(len(candidates) == 1, 'AMBIGUOUS_ROLES_EXPLICIT_MAPPING_REQUIRED')
            path, index = candidates[0], None
        require(not path.is_symlink() and not path.is_junction() and path.resolve(strict=True).parent == directory and
                path.suffix.lower() == '.xisf', 'MASTER_OUTSIDE_SELECTED_DIRECTORY')
        rows.append({'role': role, 'path': path.as_posix(), 'sha256': worker.digest(path), **master_metadata(path, index)})
    require(len({r['path'] for r in rows}) == 4 and len({(r['width'], r['height']) for r in rows}) == 1, 'MASTER_ROLES_GEOMETRY')
    return rows


def propose(config_path, intake, plan, mapping, transport):
    lock = config_path.with_name(config_path.name + '.intake-lock')
    worker.write_new(lock, {'requestId': intake['selection']['requestId']})
    try:
        return _propose_locked(config_path, intake, plan, mapping, transport)
    finally:
        lock.unlink()


def _propose_locked(config_path, intake, plan, mapping, transport):
    profile = source_profile(intake['selection'])
    from .scientific_portal import is_m27
    prepared=profile['mode']=='OSC_CFA' or profile['layout']=='PANELS'
    require(not prepared or intake.get('preparationApproved') is True and intake.get('preparationResult'),
            'PREPARATION_RESULT_REQUIRED')
    fields = {'recipe', 'background', 'processing', 'rationale', 'limitations'}
    require(isinstance(plan, dict) and set(plan) in (fields, fields | {'field'}), 'ASSISTANT_PLAN_FIELDS')
    require(plan['recipe'] in worker.NONLINEAR_RECIPES, 'PLAN_RECIPE')
    if plan['recipe'] == worker.NONLINEAR_RECIPE:
        require(not prepared and is_m27(intake.get('target','M27')) and profile['mode'] == 'LRGB', 'M27_RECIPE_TARGET')
    else:
        worker.field_settings(plan.get('field'))
        require(plan['field']['target'] == intake['target'], 'PLAN_FIELD_TARGET')
        require(worker.RECIPE_MODES[plan['recipe']] == ('OSC' if profile['mode']=='OSC_CFA' else profile['mode']), 'PLAN_SOURCE_PROFILE')
    require(all(isinstance(plan[k], str) and 1 <= len(plan[k].strip()) <= 4000 for k in ('rationale','limitations')),
            'ASSISTANT_PLAN_EXPLANATION')
    config=decode(config_path.read_bytes())
    trace=None
    if prepared:
        from .preparation_bridge import prepared_inputs
        from .preparation_flow import sha
        require(mapping is None,'APPROVED_PREPARED_INPUTS_REQUIRED')
        inputs,trace=prepared_inputs(config['workerRoot'],intake['selection']['requestId'])
        require(intake['preparationResultSha256']==sha(intake['preparationResult']) and
                all(trace[k]==intake['preparationResult'][k] for k in trace if k!='requestId'),'PREPARATION_REMOTE_RESULT_BINDING')
    elif plan['recipe'] == worker.NONLINEAR_RECIPE:
        inputs = inspect(intake, mapping)
    else:
        rows = inspect_sources(intake, [mapping] if mapping else None)['panels'][0]['masters']
        inputs = [{k:r[k] for k in ('role','path','sha256','imageIndex','width','height')} for r in rows]
    request = {'schemaVersion': '1.0', 'jobId': 'IntakeRegistration', 'recipe': plan['recipe'],
               'background': plan['background'], 'processing': plan['processing'], 'inputs': inputs}
    if 'field' in plan:
        request['field'] = plan['field']
    if trace:request['preparationTrace']=trace
    worker.validate(request)
    manifest_sha = registry_digest(request)
    ref = manifest_sha[:32]
    require(set(config) == {'serviceOrigin', 'workerId', 'workerRoot', 'registry'}, 'CONFIG_FIELDS')
    if ref in config['registry']:
        require(config['registry'][ref] == request, 'LOCAL_REGISTRY_CONFLICT')
    else:
        require(len(config['registry']) < 8, 'LOCAL_REGISTRY_CAPACITY')
        updated = copy.deepcopy(config)
        updated['registry'][ref] = request
        require(len(encode(updated)) <= 65536, 'CONFIG_SIZE')
        # Atomic replacement and backup before registering this exact immutable input.
        backup = config_path.with_name(config_path.name + '.' + ref + '.backup')
        if not backup.exists():
            with backup.open('xb') as stream:
                stream.write(config_path.read_bytes())
                stream.flush(); os.fsync(stream.fileno())
        temporary = config_path.with_name(config_path.name + '.' + ref + '.pending')
        with temporary.open('xb') as stream:
            stream.write(encode(updated)); stream.flush(); os.fsync(stream.fileno())
        temporary.replace(config_path)
    registration={'inputRef': ref, 'target': intake.get('target','M27'), 'recipe': plan['recipe'],'manifestSha256': manifest_sha}
    if prepared:registration['preparation']={'requestId':intake['selection']['requestId'],'resultSha256':intake['preparationResultSha256']}
    transport.post('/v1/worker/science/register',registration)
    payload = {**plan, 'workerId': config['workerId'], 'inputRef': ref, 'manifestSha256': manifest_sha,
               'masters': [{k: r[k] for k in ('role', 'width', 'height', 'imageIndex')} for r in inputs]}
    if prepared:payload['preparationResultSha256']=intake['preparationResultSha256']
    return transport.post('/v1/worker/science/intakes/' + intake['selection']['requestId'] + '/plan', payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('list', 'inventory', 'inspect', 'propose-sources', 'propose-preparation', 'prepare-sources', 'collect-sources', 'propose'))
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--request-id')
    parser.add_argument('--mapping', type=Path, help='Private explicit R/G/B/L filenames and image indices')
    parser.add_argument('--plan', type=Path, help='Assistant-written bounded recipe/background/rationale/limitations; never code')
    parser.add_argument('--output', type=Path, required=True, help='New private local JSON artifact')
    args = parser.parse_args()
    try:
        require(args.config.stat().st_size <= 65536, 'CONFIG_SIZE')
        config = decode(args.config.read_bytes())
        transport = Transport(config['serviceOrigin'], os.environ.get('DSG_PIAI_WORKER_TOKEN', ''))
        rows = transport.request('/v1/worker/science/intakes')['intakes']
        if args.action == 'list':
            result = {'intakes': rows}
        else:
            require(opaque(args.request_id), 'INTAKE_ID')
            selected = [r for r in rows if r['selection']['requestId'] == args.request_id]
            require(len(selected) == 1 and selected[0]['state'] != 'JOB_CREATED', 'INTAKE_STATE')
            intake = selected[0]
            require(args.mapping is None or args.mapping.stat().st_size <= 65536, 'MAPPING_SIZE')
            mapping = decode(args.mapping.read_bytes()) if args.mapping else None
            if args.action == 'inventory':
                result = {'intake':intake,'inventory':inventory_sources(intake)}
            elif args.action == 'inspect':
                profile = source_profile(intake['selection'])
                if profile['layout'] == 'PANELS' and intake.get('sourcePlan'):
                    require(intake.get('sourceSelectionApproved') is True and mapping is None,'SOURCE_SELECTION_APPROVAL_REQUIRED')
                    selection,mappings = selected_panels(intake['selection'],intake['sourcePlan'])
                    result = {'intake':intake,'sources':inspect_sources({'selection':selection},mappings)}
                else:
                    mappings = [mapping] if profile['layout'] == 'SINGLE' and isinstance(mapping,dict) else mapping
                    result = {'intake': intake, 'sources': inspect_sources(intake, mappings)}
            elif args.action == 'propose-sources':
                require(args.plan is not None and args.plan.stat().st_size <= 65536,'PLAN_SIZE')
                proposal = decode(args.plan.read_bytes())
                selection,mappings = selected_panels(intake['selection'],proposal)
                inspect_sources({'selection':selection},mappings)
                result = transport.post('/v1/worker/science/intakes/'+args.request_id+'/sources',proposal)
            elif args.action == 'propose-preparation':
                from .preparation_bridge import preparation_request
                require(args.plan is not None and args.plan.stat().st_size<=65536,'PLAN_SIZE')
                _,proposal=preparation_request(intake,decode(args.plan.read_bytes()),mapping)
                result=transport.post('/v1/worker/science/intakes/'+args.request_id+'/preparation',{**proposal,'workerId':config['workerId']})
            elif args.action == 'prepare-sources':
                from .preparation_bridge import prepare_approved
                job=prepare_approved(config['workerRoot'],intake,config['workerId'],mapping)
                result={'state':'AWAITING_SUPERVISED_PREPARATION','requestId':args.request_id,'launch':str(job/'run.js')}
            elif args.action == 'collect-sources':
                from .preparation_bridge import result_packet
                from .preparation import collect
                require(mapping is None and intake.get('preparationApproved') is True,'OWNER_PREPARATION_APPROVAL_REQUIRED')
                collect(config['workerRoot'],'PREP_'+args.request_id)
                result=transport.post('/v1/worker/science/intakes/'+args.request_id+'/prepared',result_packet(config['workerRoot'],intake,config['workerId']))
            else:
                require(args.plan is not None and args.plan.stat().st_size <= 16384, 'PLAN_SIZE')
                result = propose(args.config, intake, decode(args.plan.read_bytes()), mapping, transport)
        # Paths/prompt/individual hashes stay in this Owner-local artifact, never stdout logs.
        worker.write_new(args.output, result)
        print(encode({'state': 'LOCAL_ARTIFACT_WRITTEN', 'nativeStarted': False, 'paidAiApiRequests': 0}).decode())
    except Exception:
        parser.exit(1, 'Operazione non completata. Verifica cartella, ruoli/indice immagine e piano con l’assistente; nessun avvio nativo.\n')


if __name__ == '__main__':
    main()
