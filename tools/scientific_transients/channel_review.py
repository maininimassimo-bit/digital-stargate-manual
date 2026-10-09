"""Private TNS/VSX review worksheets, not provider payloads or submission authority."""
from decimal import Decimal
import os
import unicodedata

from tools.pixinsight.local_pilot.broker import opaque, require
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.cbat_preview import number, utc
from tools.scientific_transients.local_registry import safe_path, fingerprint, relative
from tools.scientific_transients.queue import fields, digest

PROTOCOL = 'DSG_CHANNEL_REVIEW_V1'
CHANNELS = {'TNS': 'EXTRAGALACTIC_TRANSIENT_CANDIDATE', 'VSX': 'VARIABLE_STAR_CANDIDATE'}
SOURCES = {'TNS': ['https://www.wis-tns.org/content/tns-getting-started',
                   'https://www.wis-tns.org/sites/default/files/api/tns2_manuals/TNS2.0_bulk_reports_manual.pdf'],
           'VSX': ['https://vsx.aavso.org/index.php?view=about.notice']}


def text(value, maximum=1024):
    require(type(value) is str and 0 < len(value) <= maximum and value == value.strip()
            and all(not unicodedata.category(c).startswith('C') and c not in '\u2028\u2029'
                    for c in value), 'REVIEW_SINGLE_LINE_TEXT')
    return value


def inspect(registry, request_path, expected_sha):
    require(digest(expected_sha), 'REVIEW_EXPECTED_DIGEST')
    request, actual = read_json(request_path)
    require(actual == expected_sha, 'REVIEW_REQUEST_CHANGED')
    fields(request, {'protocol', 'reviewRef', 'candidateRef', 'bindingRef', 'manifestSha256',
                     'channelDeclared', 'categoryDeclared', 'originDeclared', 'reporterDeclared',
                     'position', 'observations', 'catalogChecks', 'channelData'})
    require(request['protocol'] == PROTOCOL and all(opaque(request[k]) for k in
            ('reviewRef', 'candidateRef', 'bindingRef')) and digest(request['manifestSha256']), 'REVIEW_IDENTITY')
    channel = request['channelDeclared']
    require(type(channel) is str and channel in CHANNELS
            and request['categoryDeclared'] == CHANNELS[channel], 'REVIEW_CHANNEL_CATEGORY')
    require(type(request['originDeclared']) is str and request['originDeclared'] in
            {'REAL', 'SYNTHETIC', 'NOT_ATTESTED'}, 'REVIEW_ORIGIN')
    unknown, selected = [], set()
    def optional(value, label, validator):
        if value is None: unknown.append(label)
        else: validator(value)
    def positive(value):
        number(value, 0, 1000000); require(Decimal(value) > 0, 'REVIEW_POSITIVE')
    optional(request['reporterDeclared'], 'reporterDeclared', text)
    manifest = registry.verify(request['bindingRef'], request['manifestSha256'])
    records = {r['path']: r for r in manifest['files']}
    def evidence(path):
        relative(path); require(path in records, 'REVIEW_UNREGISTERED_EVIDENCE'); selected.add(path)
    def position_ra(value):
        number(value, 0, 360); require(Decimal(value) < 360, 'REVIEW_RA_RANGE')
    position = request['position']
    fields(position, {'raDegrees', 'decDegrees', 'frameDeclared', 'equinoxDeclared',
                      'coordinateEpochJulianYear', 'epochTimeScaleDeclared', 'evidencePath'})
    require((position['raDegrees'] is None) == (position['decDegrees'] is None), 'REVIEW_POSITION_PAIR')
    optional(position['raDegrees'], 'position.raDegrees', position_ra)
    optional(position['decDegrees'], 'position.decDegrees', lambda v: number(v, -90, 90))
    require(type(position['frameDeclared']) is str and position['frameDeclared'] in
            {'ICRS', 'FK5', 'NOT_ATTESTED'}, 'REVIEW_FRAME')
    require(type(position['equinoxDeclared']) is str and position['equinoxDeclared'] in
            {'J2000', 'NOT_APPLICABLE', 'NOT_ATTESTED'}, 'REVIEW_EQUINOX')
    require(position['frameDeclared'] != 'ICRS' or position['equinoxDeclared'] == 'NOT_APPLICABLE', 'REVIEW_ICRS_EQUINOX')
    require(position['frameDeclared'] != 'FK5' or position['equinoxDeclared'] != 'NOT_APPLICABLE', 'REVIEW_FK5_EQUINOX')
    optional(position['coordinateEpochJulianYear'], 'position.coordinateEpochJulianYear', lambda v: number(v, 0, 10000))
    require(type(position['epochTimeScaleDeclared']) is str and position['epochTimeScaleDeclared'] in
            {'TCB', 'TDB', 'TT', 'NOT_ATTESTED'}, 'REVIEW_EPOCH_SCALE')
    require(position['coordinateEpochJulianYear'] is not None or
            position['epochTimeScaleDeclared'] == 'NOT_ATTESTED', 'REVIEW_MISSING_EPOCH')
    optional(position['evidencePath'], 'position.evidencePath', evidence)
    observations = request['observations']
    require(type(observations) is list and 1 <= len(observations) <= 128, 'REVIEW_OBSERVATIONS')
    seen = set()
    units = {'AB_MAG', 'VEGA_MAG', 'INSTRUMENTAL_MAG', 'NOT_ATTESTED'}
    for index, row in enumerate(observations):
        fields(row, {'obsTime', 'timeMeaningDeclared', 'exposureSeconds', 'magnitude', 'magnitudeError',
                     'uncertaintyConventionDeclared', 'magnitudeSystemDeclared', 'bandpassDeclared',
                     'imagePath', 'reductionPath'})
        utc(row['obsTime']); require(row['timeMeaningDeclared'] == 'MID_EXPOSURE_UTC'
            and row['uncertaintyConventionDeclared'] == 'RANDOM_1SIGMA_MAG', 'REVIEW_CONVENTIONS')
        require(type(row['magnitudeSystemDeclared']) is str and row['magnitudeSystemDeclared'] in units, 'REVIEW_MAG_SYSTEM')
        evidence(row['imagePath']); evidence(row['reductionPath'])
        require(row['imagePath'] not in seen, 'REVIEW_DUPLICATE_IMAGE'); seen.add(row['imagePath'])
        label = 'observations[' + str(index) + '].'
        optional(row['exposureSeconds'], label + 'exposureSeconds', positive)
        optional(row['magnitude'], label + 'magnitude', lambda v: number(v, -1000000, 1000000))
        optional(row['magnitudeError'], label + 'magnitudeError', positive)
        require(row['magnitude'] is not None or row['magnitudeError'] is None, 'REVIEW_ERROR_WITHOUT_MAG')
        optional(row['bandpassDeclared'], label + 'bandpassDeclared', lambda v: text(v, 80))
    checks = request['catalogChecks']; require(type(checks) is list and len(checks) <= 32, 'REVIEW_CHECKS')
    checked = set()
    for row in checks:
        fields(row, {'kind', 'catalogDeclared', 'checkedUTC', 'outcomeDeclared', 'evidencePath'})
        require(type(row['kind']) is str and row['kind'] in {'VARIABLE', 'MOVING_OBJECT', 'PREVIOUS_REPORT'}, 'REVIEW_CHECK_KIND')
        text(row['catalogDeclared'], 200); key = (row['kind'], row['catalogDeclared'])
        require(key not in checked, 'REVIEW_DUPLICATE_CHECK'); checked.add(key)
        require(type(row['outcomeDeclared']) is str and row['outcomeDeclared'] in
                {'NOT_CHECKED', 'NO_MATCH_DECLARED', 'POSSIBLE_MATCH_DECLARED', 'INCONCLUSIVE_DECLARED'}, 'REVIEW_CHECK_OUTCOME')
        if row['outcomeDeclared'] == 'NOT_CHECKED':
            require(row['checkedUTC'] is None and row['evidencePath'] is None, 'REVIEW_UNCHECKED_CONTRADICTION')
            unknown.append('catalogChecks.' + row['kind'] + '.' + row['catalogDeclared'])
        else: utc(row['checkedUTC']); evidence(row['evidencePath'])
    data = request['channelData']
    if channel == 'TNS':
        fields(data, {'internalNameDeclared', 'reportingGroupDeclared', 'discoveryDataSourceDeclared',
                      'discoveryImagePath', 'priorImages', 'archivalContext', 'hostDeclared'})
        for key in ('internalNameDeclared', 'reportingGroupDeclared', 'discoveryDataSourceDeclared'):
            optional(data[key], 'channelData.' + key, lambda v: text(v, 200))
        if data['discoveryImagePath'] is None: unknown.append('channelData.discoveryImagePath')
        else: require(type(data['discoveryImagePath']) is str and data['discoveryImagePath'] in seen, 'REVIEW_DISCOVERY_IMAGE')
        prior = data['priorImages']; require(type(prior) is list and len(prior) <= 128, 'REVIEW_PRIOR_IMAGES')
        prior_seen = set()
        for index, row in enumerate(prior):
            fields(row, {'obsTime', 'timeMeaningDeclared', 'presenceDeclared', 'limitingMagnitude',
                         'limitSigmaDeclared', 'magnitudeSystemDeclared', 'bandpassDeclared', 'imagePath', 'reductionPath'})
            utc(row['obsTime']); require(row['timeMeaningDeclared'] == 'MID_EXPOSURE_UTC', 'REVIEW_CONVENTIONS')
            require(type(row['presenceDeclared']) is str and row['presenceDeclared'] in
                    {'NOT_ASSESSED', 'NON_DETECTION_DECLARED', 'DETECTION_DECLARED'}, 'REVIEW_PRESENCE')
            require(type(row['magnitudeSystemDeclared']) is str and row['magnitudeSystemDeclared'] in units, 'REVIEW_MAG_SYSTEM')
            evidence(row['imagePath']); evidence(row['reductionPath'])
            require(row['imagePath'] not in seen and row['imagePath'] not in prior_seen, 'REVIEW_DUPLICATE_PRIOR')
            prior_seen.add(row['imagePath']); label = 'channelData.priorImages[' + str(index) + '].'
            optional(row['limitingMagnitude'], label + 'limitingMagnitude', lambda v: number(v, -1000000, 1000000))
            optional(row['limitSigmaDeclared'], label + 'limitSigmaDeclared', positive)
            require(row['limitingMagnitude'] is not None or row['limitSigmaDeclared'] is None, 'REVIEW_SIGMA_WITHOUT_LIMIT')
            optional(row['bandpassDeclared'], label + 'bandpassDeclared', lambda v: text(v, 80))
            if row['presenceDeclared'] == 'NOT_ASSESSED': unknown.append(label + 'presence')
        context = data['archivalContext']; fields(context, {'noteDeclared', 'evidencePath'})
        require((context['noteDeclared'] is None) == (context['evidencePath'] is None), 'REVIEW_ARCHIVAL_PAIR')
        optional(context['noteDeclared'], 'channelData.archivalContext.noteDeclared', lambda v: text(v, 4096))
        optional(context['evidencePath'], 'channelData.archivalContext.evidencePath', evidence)
        host = data['hostDeclared']; fields(host, {'name', 'redshift', 'evidencePath'})
        optional(host['name'], 'channelData.hostDeclared.name', lambda v: text(v, 200))
        optional(host['redshift'], 'channelData.hostDeclared.redshift', lambda v: number(v, -1, 1000000))
        optional(host['evidencePath'], 'channelData.hostDeclared.evidencePath', evidence)
    else:
        fields(data, {'primaryNameDeclared', 'crossIds', 'variabilityTypeDeclared', 'rangeDeclared', 'periodDeclared', 'plots'})
        for key in ('primaryNameDeclared', 'variabilityTypeDeclared'):
            optional(data[key], 'channelData.' + key, lambda v: text(v, 200))
        ids = data['crossIds']; require(type(ids) is list and len(ids) <= 32, 'REVIEW_CROSS_IDS')
        ids_seen = set()
        for row in ids:
            fields(row, {'catalogDeclared', 'idDeclared', 'evidencePath'})
            text(row['catalogDeclared'], 200); text(row['idDeclared'], 200)
            key = (row['catalogDeclared'], row['idDeclared']); require(key not in ids_seen, 'REVIEW_DUPLICATE_CROSS_ID')
            ids_seen.add(key); evidence(row['evidencePath'])
        bounds = data['rangeDeclared']; fields(bounds, {'brightMagnitude', 'faintMagnitude', 'bandpassDeclared', 'evidencePath'})
        require((bounds['brightMagnitude'] is None) == (bounds['faintMagnitude'] is None), 'REVIEW_RANGE_PAIR')
        for key in ('brightMagnitude', 'faintMagnitude'):
            optional(bounds[key], 'channelData.rangeDeclared.' + key, lambda v: number(v, -1000000, 1000000))
        require(bounds['brightMagnitude'] is None or Decimal(bounds['brightMagnitude']) <= Decimal(bounds['faintMagnitude']), 'REVIEW_RANGE_ORDER')
        optional(bounds['bandpassDeclared'], 'channelData.rangeDeclared.bandpassDeclared', lambda v: text(v, 80))
        optional(bounds['evidencePath'], 'channelData.rangeDeclared.evidencePath', evidence)
        period = data['periodDeclared']; fields(period, {'days', 'epochHjd', 'epochTimeScaleDeclared', 'epochEventDeclared', 'evidencePath'})
        optional(period['days'], 'channelData.periodDeclared.days', positive)
        optional(period['epochHjd'], 'channelData.periodDeclared.epochHjd', lambda v: number(v, 0, 1000000000))
        require(type(period['epochTimeScaleDeclared']) is str and period['epochTimeScaleDeclared'] in
                {'UTC', 'TT', 'TDB', 'NOT_ATTESTED'}, 'REVIEW_HJD_SCALE')
        require(type(period['epochEventDeclared']) is str and period['epochEventDeclared'] in
                {'MAXIMUM', 'PRIMARY_MINIMUM', 'NOT_ATTESTED'}, 'REVIEW_HJD_EVENT')
        require(period['epochHjd'] is not None or period['epochTimeScaleDeclared'] == period['epochEventDeclared'] == 'NOT_ATTESTED', 'REVIEW_MISSING_HJD')
        optional(period['evidencePath'], 'channelData.periodDeclared.evidencePath', evidence)
        plots = data['plots']; require(type(plots) is list and len(plots) <= 32, 'REVIEW_PLOTS')
        plot_seen = set()
        for row in plots:
            fields(row, {'kindDeclared', 'sourceDeclared', 'evidencePath'})
            require(type(row['kindDeclared']) is str and row['kindDeclared'] in
                    {'LIGHT_CURVE', 'PHASE', 'FINDING_CHART'}, 'REVIEW_PLOT_KIND')
            require(type(row['sourceDeclared']) is str and row['sourceDeclared'] in
                    {'OWNER_GENERATED', 'NOT_ATTESTED'}, 'REVIEW_PLOT_SOURCE')
            evidence(row['evidencePath']); require(row['evidencePath'] not in plot_seen, 'REVIEW_DUPLICATE_PLOT')
            plot_seen.add(row['evidencePath'])
    return {'protocol': PROTOCOL, 'requestSha256': actual, 'declarations': request, 'manifest': manifest,
            'selectedEvidence': [records[p] for p in sorted(selected)], 'unknownFields': unknown,
            'state': 'PRIVATE_REVIEW_WORKSHEET', 'declarationsAttested': False,
            'scienceValidation': 'NOT_VALIDATED', 'providerPayload': False, 'providerSchemaValidated': False,
            'providerReadiness': 'NOT_EVALUATED', 'submissionAuthorized': False,
            'externalSubmission': 'NONE', 'providerAcknowledgement': 'NONE',
            'completeDependencyArchive': False, 'integrityScope': 'POINT_IN_TIME_REGISTERED_BYTES_ONLY',
            'sources': SOURCES[channel], 'missingGates': ['INDEPENDENT_SCIENTIFIC_VALIDATION',
                'CALIBRATION_ASTROMETRY_TIMING_FULL_UNCERTAINTY', 'CURRENT_DUPLICATE_AND_MOVING_OBJECT_CHECKS',
                'PROVIDER_CURRENT_SCHEMA_AND_IDENTIFIER_MAPPING', 'PROVIDER_TESTS_AND_RECEIPT_RECONCILIATION',
                'OWNER_EXACT_DATA_RELEASE_AND_RECIPIENT_AUTHORIZATION']}


def render(value):
    """Internal plain-text renderer; never turns declarations into a provider request."""
    request = value['declarations']; lines = ['PRIVATE REVIEW WORKSHEET - NOT SENT',
        'Channel declared: ' + request['channelDeclared'],
        'Category declared: ' + request['categoryDeclared'],
        'Origin declared: ' + request['originDeclared'] + ' (not attested)',
        'All scientific values, catalogue results and supporting documents remain unvalidated declarations.',
        'This is not a provider payload or an authorized report.']
    labels = {'reporterDeclared': 'Reporter (declared)', 'position': 'Astrometry (declared)',
        'observations': 'Photometry (declared)', 'catalogChecks': 'Catalogue checks (declared)', 'channelData': 'Channel details (declared)',
        'raDegrees': 'RA (degrees)', 'decDegrees': 'Dec (degrees)', 'frameDeclared': 'Reference frame',
        'equinoxDeclared': 'Equinox', 'coordinateEpochJulianYear': 'Coordinate epoch (Julian year)',
        'epochTimeScaleDeclared': 'Epoch time scale', 'obsTime': 'Mid-exposure UTC', 'timeMeaningDeclared': 'Time convention',
        'exposureSeconds': 'Exposure (s)', 'magnitude': 'Magnitude (mag)', 'magnitudeError': 'Random magnitude error (mag)',
        'uncertaintyConventionDeclared': 'Error convention', 'magnitudeSystemDeclared': 'Magnitude system',
        'bandpassDeclared': 'Passband', 'kind': 'Check kind', 'catalogDeclared': 'Catalogue', 'checkedUTC': 'Check UTC',
        'outcomeDeclared': 'Check outcome', 'internalNameDeclared': 'Internal name', 'reportingGroupDeclared': 'Reporting group',
        'discoveryDataSourceDeclared': 'Discovery data source', 'priorImages': 'Earlier images', 'presenceDeclared': 'Presence',
        'limitingMagnitude': 'Limiting magnitude (mag)', 'limitSigmaDeclared': 'Limit sigma (declared)',
        'archivalContext': 'Archival context', 'noteDeclared': 'Note', 'hostDeclared': 'Host', 'name': 'Name', 'redshift': 'Redshift',
        'primaryNameDeclared': 'Primary name', 'crossIds': 'Cross-identifications', 'idDeclared': 'Identifier',
        'variabilityTypeDeclared': 'Variability type', 'rangeDeclared': 'Brightness range', 'brightMagnitude': 'Magnitude at brightest',
        'faintMagnitude': 'Magnitude at faintest', 'periodDeclared': 'Period and epoch', 'days': 'Period (days)', 'epochHjd': 'Epoch (HJD)',
        'epochEventDeclared': 'Epoch event', 'plots': 'Supporting plots', 'kindDeclared': 'Plot kind', 'sourceDeclared': 'Plot origin'}
    def display(label, content):
        if type(content) is dict:
            for key, item in content.items():
                if not key.endswith('Path'): display(label + ' / ' + labels[key], item)
        elif type(content) is list:
            lines.append(label + ' / declared count: ' + str(len(content)))
            for index, item in enumerate(content): display(label + ' / ' + str(index + 1), item)
        else: lines.append(label + ': ' + ('UNKNOWN' if content is None else str(content)))
    for key in ('reporterDeclared', 'position', 'observations', 'catalogChecks', 'channelData'): display(labels[key], request[key])
    lines.extend(['Positions: degrees; coordinate epoch: declared Julian year and separate time scale.',
        'Observation times: declared mid-exposure UTC; no JD/HJD conversion or heliocentric correction performed.',
        'Magnitudes and their random 1sigma errors: mag; system and passband must be validated separately.',
        'No limit implies nondetection, no catalogue result implies novelty, and no declared host implies association.',
        'No external identifiers, credentials, account, attachment, upload, API call or submission authority added.'])
    return ('\n'.join(lines) + '\n').encode('utf-8')


def export(registry, request_path, expected_sha, output_root):
    root, source = safe_path(output_root), safe_path(request_path)
    require(root.is_dir(), 'REVIEW_OUTPUT_DIRECTORY')
    for other in (registry.artifacts, registry.registry):
        require(root != other and root not in other.parents and other not in root.parents, 'REVIEW_ROOT_OVERLAP')
    require(root not in source.parents, 'REVIEW_SOURCE_IN_OUTPUT')
    value = inspect(registry, source, expected_sha)
    directory = root / value['declarations']['reviewRef']; directory.mkdir()
    try:
        write_new(directory / 'worksheet.json', value)
        with (directory / 'worksheet.txt').open('xb') as stream:
            stream.write(render(value)); stream.flush(); os.fsync(stream.fileno())
        require(inspect(registry, source, expected_sha) == value, 'REVIEW_SOURCE_CHANGED')
        write_new(directory / 'export.json', {'protocol': PROTOCOL, 'state': 'PRIVATE_REVIEW_WORKSHEET',
            'requestSha256': expected_sha, 'files': {name: fingerprint(directory / name)
            for name in ('worksheet.json', 'worksheet.txt')}, 'externalSubmission': 'NONE'})
    except Exception:
        write_new(directory / 'failed.json', {'state': 'REVIEW_WORKSHEET_INCOMPLETE'})
        raise
    return directory


def main():
    import argparse
    from pathlib import Path
    from tools.pixinsight.local_pilot.broker import ProtocolError
    from tools.scientific_transients.local_registry import LocalRegistry
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--registry', type=Path, required=True)
    parser.add_argument('--request', type=Path, required=True)
    parser.add_argument('--request-sha256', required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    args = parser.parse_args()
    try:
        export(LocalRegistry(args.artifacts, args.registry), args.request, args.request_sha256, args.output_root)
    except (ProtocolError, OSError, KeyError, TypeError, ValueError):
        parser.exit(2, 'Scheda privata non esportata integralmente. Conservare i file parziali. Nessun invio effettuato.\n')
    print('PRIVATE_REVIEW_WORKSHEET_EXPORTED_NO_SUBMISSION_OR_SCIENCE_ACCEPTANCE')


if __name__ == '__main__': main()
