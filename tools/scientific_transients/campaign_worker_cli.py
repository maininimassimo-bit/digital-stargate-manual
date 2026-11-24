"""Explicit local package/Worker commands; no Owner token, daemon or restart replay."""
import argparse
import json
import os
from pathlib import Path

from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.campaign_input_archive import CampaignInputArchive
from tools.scientific_transients.campaign_triplet import CampaignTriplet
from tools.scientific_transients.campaign_dispatch import CampaignWorkerTransport
from tools.scientific_transients.campaign_handoff import validate_handoff
from tools.scientific_transients.native_aperture import ENGINE, CATALOG
from tools.scientific_transients.operator_run import OperatorPlan, ORIGIN
from tools.scientific_transients.queue import fields, digest


def load_config(path, expected_sha, *, engine=ENGINE, catalog=CATALOG):
    require(digest(expected_sha), 'CAMPAIGN_LOCAL_CONFIG_DIGEST')
    value, actual = read_json(path)
    fields(value, {'protocol','contextPath','contextFileSha256','archiveDirectory','archiveSha256',
                   'coordinatorRoot','decisionId','operatorPlans'})
    require(actual == expected_sha and value['protocol'] == 'DSG_CAMPAIGN_LOCAL_RUN_CONFIG_V1'
            and type(value['operatorPlans']) is list and len(value['operatorPlans']) == 3,
            'CAMPAIGN_LOCAL_CONFIG')
    for key in ('contextPath','archiveDirectory','coordinatorRoot'):
        require(type(value[key]) is str and Path(value[key]).is_absolute(), 'CAMPAIGN_LOCAL_ABSOLUTE_PATH')
    plans = []
    for row in value['operatorPlans']:
        fields(row, {'path','sha256'})
        require(type(row['path']) is str and Path(row['path']).is_absolute(), 'CAMPAIGN_LOCAL_ABSOLUTE_PATH')
        plans.append(OperatorPlan.load(row['path'], row['sha256'], engine=engine, catalog=catalog))
    archive = CampaignInputArchive(value['archiveDirectory'], value['archiveSha256'])
    return (value['coordinatorRoot'], value['contextPath'], value['contextFileSha256'], archive, plans, value['decisionId'])


def main(argv=None, *, engine=ENGINE, catalog=CATALOG):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['preflight','prepare','register-all','export-owner-proposal','run-worker'])
    parser.add_argument('--config', required=True)
    parser.add_argument('--config-sha256', required=True)
    parser.add_argument('--output')
    parser.add_argument('--handoff')
    parser.add_argument('--handoff-sha256')
    parser.add_argument('--authorize-native-launch', action='store_true')
    args = parser.parse_args(argv)
    try:
        require(not args.authorize_native_launch or args.mode == 'run-worker', 'CAMPAIGN_CLI_LAUNCH_MODE')
        require((args.output is not None) == (args.mode == 'export-owner-proposal')
                and (args.handoff is not None) == (args.mode == 'run-worker')
                and (args.handoff_sha256 is not None) == (args.mode == 'run-worker'), 'CAMPAIGN_CLI_ARGUMENTS')
        if args.mode == 'run-worker': require(args.authorize_native_launch, 'CAMPAIGN_CLI_EXPLICIT_LAUNCH')
        inputs = load_config(args.config, args.config_sha256, engine=engine, catalog=catalog)
        if args.mode == 'preflight':
            CampaignTriplet._build(*inputs)
            result = {'preflightVerified': True, 'networkRequested': False, 'nativeLaunchRequested': False}
        elif args.mode == 'prepare':
            CampaignTriplet.prepare(*inputs)
            result = {'packagePrepared': True, 'networkRequested': False, 'nativeLaunchRequested': False}
        elif args.mode == 'export-owner-proposal':
            triplet = CampaignTriplet.reopen_registered(*inputs)
            require(Path(args.output).is_absolute(), 'CAMPAIGN_LOCAL_ABSOLUTE_PATH')
            write_new(Path(args.output), triplet.owner_proposal())
            result = {'proposalExported': True, 'networkRequested': False, 'nativeLaunchRequested': False}
        else:
            if args.mode == 'register-all': triplet = CampaignTriplet.reopen_prepared(*inputs)
            else:
                triplet = CampaignTriplet.reopen_registered(*inputs)
                require(digest(args.handoff_sha256), 'CAMPAIGN_CLI_HANDOFF_DIGEST')
                handoff, actual = read_json(args.handoff)
                require(actual == args.handoff_sha256, 'CAMPAIGN_CLI_HANDOFF_CHANGED')
                handoff = validate_handoff(handoff)
            # Remove the dedicated credential from the process environment before
            # any native child can inherit it. No file/argv/Google fallback.
            token = os.environ.pop('DSG_TRANSIENT_OPERATOR_TOKEN', None)
            require(digest(token), 'CAMPAIGN_CLI_WORKER_CREDENTIAL')
            transport = CampaignWorkerTransport(ORIGIN, token)
            if args.mode == 'register-all': result = triplet.register_all(transport)
            else: result = triplet.run_worker(handoff, transport, native_launch_authorized=True)
        summary = {'operationConfirmed': True, 'scientificValidation': 'NOT_VALIDATED'}
        summary.update(result)
        print(json.dumps(summary, sort_keys=True))
        return 0
    except (Exception, KeyboardInterrupt):
        print(json.dumps({'operationConfirmed': False, 'implicitReplay': False,
              'evidenceMustBePreserved': True, 'nativeStoppedAttested': False,
              'scientificValidation': 'NOT_VALIDATED'}, sort_keys=True))
        return 2


if __name__ == '__main__': raise SystemExit(main())
