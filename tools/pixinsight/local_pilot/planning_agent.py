"""Outbound PC planning loop. Inspects configured folders; never starts PixInsight."""
import argparse
import os
from pathlib import Path
import time

from .broker import decode, encode, require
from .intake import sha, local_directory
from .intake_assistant import inspect, propose
from .source_profile import source_profile, inspect_sources
from .openai_flow import api_requested
from .openai_planner import validate_evidence
from .transport import Transport
from . import worker


def read_private(path):
    require(path.stat().st_size <= 65536 and not path.is_symlink() and not path.is_junction(), 'PLANNING_CONFIG_SIZE')
    return decode(path.read_bytes())


def scope(intake, settings):
    require(isinstance(settings, dict) and set(settings) == {'allowedMasterRoots', 'targets'}, 'PLANNING_SETTINGS')
    roots = settings['allowedMasterRoots']
    require(isinstance(roots, list) and 1 <= len(roots) <= 16, 'PLANNING_ROOTS')
    profile = source_profile(intake['selection'])
    folders = [intake['selection']['masterDirectory']] + profile.get('additionalDirectories', [])
    for folder in folders:
        path = Path(local_directory(folder)).resolve(strict=True)
        require(any(path.is_relative_to(Path(local_directory(root)).resolve(strict=True)) for root in roots), 'PLANNING_FOLDER_OUTSIDE_SCOPE')
    require(isinstance(settings['targets'], dict) and intake['target'] in settings['targets'], 'REVIEWED_TARGET_REQUIRED')
    preset = settings['targets'][intake['target']]
    require(isinstance(preset, dict) and set(preset) == {'recipe', 'field', 'mapping'}, 'REVIEWED_PRESET_FIELDS')
    return preset


def evidence_for(config, intake, preset):
    profile = source_profile(intake['selection'])
    prepared = profile['mode'] == 'OSC_CFA' or profile['layout'] == 'PANELS'
    if prepared:
        require(intake.get('preparationApproved') and intake.get('preparationResult'), 'PREPARATION_RESULT_REQUIRED')
        require(preset['mapping'] is None, 'PREPARED_MAPPING_FORBIDDEN')
        from .preparation_bridge import prepared_inputs
        inputs, trace = prepared_inputs(config['workerRoot'], intake['selection']['requestId'])
        require(all(trace[k] == intake['preparationResult'][k] for k in trace if k != 'requestId'), 'PREPARATION_REMOTE_RESULT_BINDING')
    elif preset['recipe'] == worker.NONLINEAR_RECIPE:
        inputs = inspect(intake, preset['mapping'])
    else:
        rows = inspect_sources(intake, [preset['mapping']] if preset['mapping'] else None)['panels'][0]['masters']
        inputs = [{k: r[k] for k in ('role', 'path', 'sha256', 'imageIndex', 'width', 'height')} for r in rows]
    evidence = {'recipe': preset['recipe'], 'field': preset['field'], 'inputSetSha256': sha(inputs),
                'masters': [{k: r[k] for k in ('role', 'width', 'height', 'imageIndex')} for r in inputs]}
    return validate_evidence(evidence, intake['target'], profile['mode'])


def cycle(config_path, settings, transport):
    config = read_private(config_path)
    require(set(config) == {'serviceOrigin', 'workerId', 'workerRoot', 'registry'}, 'CONFIG_FIELDS')
    rows = transport.request('/v1/worker/science/intakes')['intakes']
    results = []
    for intake in rows:
        if not api_requested(intake['selection']) or intake['state'] in {'WITHDRAWN', 'JOB_CREATED', 'PLAN_READY'}:
            continue
        request_id = intake['selection']['requestId']
        try:
            preset = scope(intake, settings)
            evidence = evidence_for(config, intake, preset)
            draft = intake.get('openai') or {}
            if draft.get('state') == 'AWAITING_LOCAL_EVIDENCE':
                draft = transport.post('/v1/worker/science/intakes/' + request_id + '/openai-plan',
                                       {'workerId': config['workerId'], 'evidence': evidence})
            if draft.get('state') == 'AI_DRAFT_READY':
                require(draft['evidence'] == evidence, 'AI_EVIDENCE_CHANGED')
                # Re-read and hash local sources in propose before registering the plan.
                intake = {**intake, 'openai': draft}
                propose(config_path, intake, draft['plan'], preset['mapping'], transport)
                config = read_private(config_path)
                results.append({'requestId': request_id, 'state': 'PLAN_READY'})
            else:
                results.append({'requestId': request_id, 'state': draft.get('state', 'AWAITING_LOCAL_EVIDENCE')})
        except Exception:
            # No paths, raw provider errors, prompt or tokens on stdout.
            results.append({'requestId': request_id, 'state': 'LOCAL_REVIEW_REQUIRED'})
    return {'requests': results, 'nativeStarted': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--settings', type=Path, required=True)
    parser.add_argument('--watch', action='store_true', help='Keep polling until stopped; no native launch')
    parser.add_argument('--interval', type=int, default=30)
    args = parser.parse_args()
    try:
        require(10 <= args.interval <= 300, 'PLANNING_INTERVAL')
        config = read_private(args.config)
        transport = Transport(config['serviceOrigin'], os.environ.get('DSG_PIAI_WORKER_TOKEN', ''))
        while True:
            print(encode(cycle(args.config, read_private(args.settings), transport)).decode(), flush=True)
            if not args.watch:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        return
    except Exception:
        parser.exit(1, 'Pianificazione non completata; verifica la configurazione privata. Nessun avvio PixInsight.\n')


if __name__ == '__main__':
    main()
