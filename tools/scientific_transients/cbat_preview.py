"""Private ASCII preview for a declared Galactic-nova candidate. Never sends."""
import datetime as dt
from decimal import Decimal
import os
import re

from tools.pixinsight.local_pilot.broker import opaque, require
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.local_registry import safe_path, fingerprint, relative
from tools.scientific_transients.queue import fields, digest

PROTOCOL = 'DSG_CBAT_NOVA_PREVIEW_V1'
RECIPIENT = 'cbatiau@eps.harvard.edu'
SOURCES = ['https://tamkin3.eps.harvard.edu/HowToReportDiscovery.html',
           'https://tamkin3.eps.harvard.edu/iau/DiscoveryInfo.html']


def ascii_text(value, maximum):
    require(type(value) is str and 0 < len(value) <= maximum and value == value.strip()
            and all(32 <= ord(c) <= 126 for c in value), 'CBAT_ASCII_SINGLE_LINE')
    return value


def number(value, minimum, maximum, fraction=9):
    require(type(value) is str and len(value) <= 24
            and re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]{1,' + str(fraction) + r'})?', value),
            'CBAT_DECIMAL_TEXT')
    require(Decimal(str(minimum)) <= Decimal(value) <= Decimal(str(maximum)), 'CBAT_DECIMAL_RANGE')
    return value


def utc(value):
    require(type(value) is str and re.fullmatch(
        r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z', value), 'CBAT_UTC_TEXT')
    try: return dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError: require(False, 'CBAT_UTC_UNSUPPORTED')


def inspect(registry, request_path, expected_sha):
    require(digest(expected_sha), 'CBAT_EXPECTED_DIGEST')
    request, actual = read_json(request_path)
    require(actual == expected_sha, 'CBAT_REQUEST_CHANGED')
    fields(request, {'protocol', 'exportRef', 'candidateRef', 'bindingRef', 'manifestSha256',
                     'categoryDeclared', 'sourceOriginDeclared', 'author', 'siteDeclared',
                     'instrument', 'position', 'observations', 'referenceImages', 'catalogChecks', 'noveltyNote'})
    require(request['protocol'] == PROTOCOL and all(opaque(request[k]) for k in
            ('exportRef', 'candidateRef', 'bindingRef')) and digest(request['manifestSha256']), 'CBAT_IDENTITY')
    require(request['categoryDeclared'] == 'GALACTIC_NOVA_CANDIDATE', 'CBAT_CATEGORY')
    require(type(request['sourceOriginDeclared']) is str and request['sourceOriginDeclared']
            in {'REAL', 'SYNTHETIC', 'NOT_ATTESTED'}, 'CBAT_ORIGIN')
    unknown, selected = [], set()
    def optional(value, label, validator):
        if value is None: unknown.append(label)
        else: validator(value)
    author = request['author']; fields(author, {'name', 'contactEmail', 'address', 'experience'})
    ascii_text(author['name'], 200)
    def email(value):
        ascii_text(value, 254)
        require(re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+", value), 'CBAT_CONTACT_EMAIL')
        require('..' not in value and not value.startswith('.') and '.@' not in value, 'CBAT_CONTACT_EMAIL')
    optional(author['contactEmail'], 'author.contactEmail', email)
    for key in ('address', 'experience'): optional(author[key], 'author.' + key, lambda v: ascii_text(v, 1024))
    optional(request['siteDeclared'], 'siteDeclared', lambda v: ascii_text(v, 512))
    optional(request['noveltyNote'], 'noveltyNote', lambda v: ascii_text(v, 4096))
    instrument = request['instrument']; fields(instrument, {'methodDeclared', 'description', 'apertureMeters', 'fRatio'})
    require(type(instrument['methodDeclared']) is str and instrument['methodDeclared']
            in {'CCD', 'CMOS', 'PHOTOGRAPHIC'}, 'CBAT_METHOD')
    ascii_text(instrument['description'], 1024)
    def positive(value):
        number(value, 0, 1000000); require(Decimal(value) > 0, 'CBAT_POSITIVE')
    for key in ('apertureMeters', 'fRatio'): optional(instrument[key], 'instrument.' + key, positive)
    position = request['position']; fields(position, {'raDegrees', 'decDegrees', 'equinoxDeclared',
                                                     'rmsRaCosDecArcsec', 'rmsDecArcsec'})
    require(position['equinoxDeclared'] == 'J2000', 'CBAT_EQUINOX_SCOPE')
    require((position['raDegrees'] is None) == (position['decDegrees'] is None), 'CBAT_POSITION_PAIR')
    def ra(value):
        number(value, 0, 360); require(Decimal(value) < 360, 'CBAT_RA_RANGE')
    optional(position['raDegrees'], 'position.raDegrees', ra)
    optional(position['decDegrees'], 'position.decDegrees', lambda v: number(v, -90, 90))
    for key in ('rmsRaCosDecArcsec', 'rmsDecArcsec'): optional(position[key], 'position.' + key, positive)
    require(position['raDegrees'] is not None or all(position[k] is None for k in
            ('rmsRaCosDecArcsec', 'rmsDecArcsec')), 'CBAT_POSITION_ERROR_WITHOUT_POSITION')
    manifest = registry.verify(request['bindingRef'], request['manifestSha256'])
    records = {r['path']: r for r in manifest['files']}
    def evidence(path):
        relative(path); require(path in records, 'CBAT_UNREGISTERED_EVIDENCE'); selected.add(path)
    rows = request['observations']
    require(type(rows) is list and 1 <= len(rows) <= 128, 'CBAT_OBSERVATIONS')
    seen = set()
    for index, row in enumerate(rows):
        fields(row, {'obsTime', 'timeMeaningDeclared', 'exposureSeconds', 'magnitude', 'magnitudeError',
                     'uncertaintyConventionDeclared', 'bandpassDeclared', 'imagePath', 'reductionPath'})
        utc(row['obsTime'])
        require(row['timeMeaningDeclared'] == 'MID_EXPOSURE_UTC'
                and row['uncertaintyConventionDeclared'] == 'RANDOM_1SIGMA_MAG', 'CBAT_CONVENTIONS')
        evidence(row['imagePath']); evidence(row['reductionPath'])
        require(row['imagePath'] not in seen, 'CBAT_DUPLICATE_IMAGE'); seen.add(row['imagePath'])
        label = 'observations[' + str(index) + '].'
        optional(row['exposureSeconds'], label + 'exposureSeconds', positive)
        optional(row['magnitude'], label + 'magnitude', lambda v: number(v, -1000000, 1000000))
        optional(row['magnitudeError'], label + 'magnitudeError', positive)
        require(row['magnitude'] is not None or row['magnitudeError'] is None, 'CBAT_ERROR_WITHOUT_MAGNITUDE')
        optional(row['bandpassDeclared'], label + 'bandpassDeclared', lambda v: ascii_text(v, 80))
    refs = request['referenceImages']; require(type(refs) is list and len(refs) <= 128, 'CBAT_REFERENCE_IMAGES')
    ref_seen = set()
    for index, row in enumerate(refs):
        fields(row, {'obsTime', 'timeMeaningDeclared', 'bandpassDeclared', 'limitingMagnitude',
                     'presenceDeclared', 'imagePath', 'reductionPath'})
        utc(row['obsTime']); require(row['timeMeaningDeclared'] == 'MID_EXPOSURE_UTC', 'CBAT_CONVENTIONS')
        require(type(row['presenceDeclared']) is str and row['presenceDeclared'] in
                {'NON_DETECTION_DECLARED', 'DETECTION_DECLARED', 'NOT_ASSESSED'}, 'CBAT_REFERENCE_PRESENCE')
        evidence(row['imagePath']); evidence(row['reductionPath'])
        require(row['imagePath'] not in ref_seen and row['imagePath'] not in seen, 'CBAT_DUPLICATE_REFERENCE')
        ref_seen.add(row['imagePath']); label = 'referenceImages[' + str(index) + '].'
        optional(row['bandpassDeclared'], label + 'bandpassDeclared', lambda v: ascii_text(v, 80))
        optional(row['limitingMagnitude'], label + 'limitingMagnitude', lambda v: number(v, -1000000, 1000000))
        if row['presenceDeclared'] == 'NOT_ASSESSED': unknown.append(label + 'presence')
    checks = request['catalogChecks']; require(type(checks) is list and len(checks) <= 32, 'CBAT_CATALOG_CHECKS')
    checked = set()
    for row in checks:
        fields(row, {'kind', 'catalogDeclared', 'checkedUTC', 'outcomeDeclared', 'evidencePath'})
        require(type(row['kind']) is str and row['kind'] in {'VARIABLE', 'MOVING_OBJECT', 'PREVIOUS_REPORT'}, 'CBAT_CHECK_KIND')
        ascii_text(row['catalogDeclared'], 200); key = (row['kind'], row['catalogDeclared'])
        require(key not in checked, 'CBAT_DUPLICATE_CHECK'); checked.add(key)
        require(type(row['outcomeDeclared']) is str and row['outcomeDeclared'] in
                {'NOT_CHECKED', 'NO_MATCH_DECLARED', 'POSSIBLE_MATCH_DECLARED', 'INCONCLUSIVE_DECLARED'}, 'CBAT_CHECK_OUTCOME')
        if row['outcomeDeclared'] == 'NOT_CHECKED':
            require(row['checkedUTC'] is None and row['evidencePath'] is None, 'CBAT_UNCHECKED_CONTRADICTION')
            unknown.append('catalogChecks.' + row['kind'] + '.' + row['catalogDeclared'])
        else: utc(row['checkedUTC']); evidence(row['evidencePath'])
    return {'protocol': PROTOCOL, 'requestSha256': actual, 'declarations': request, 'manifest': manifest,
            'selectedEvidence': [records[p] for p in sorted(selected)], 'unknownFields': unknown,
            'intendedRecipient': RECIPIENT, 'subjectPreview': 'PRIVATE PREVIEW - possible Galactic nova - '
                + instrument['methodDeclared'] + ' - ' + request['candidateRef'],
            'state': 'PRIVATE_PREVIEW', 'declarationsAttested': False, 'scienceValidation': 'NOT_VALIDATED',
            'externalSubmission': 'NONE', 'submissionAuthorized': False, 'providerAcknowledgement': 'NONE',
            'providerReadiness': 'NOT_EVALUATED', 'completeDependencyArchive': False,
            'integrityScope': 'POINT_IN_TIME_REGISTERED_BYTES_ONLY', 'sources': SOURCES,
            'missingGates': ['INDEPENDENT_CLASSIFICATION_ASTROMETRY_TIMING_PHOTOMETRY',
                             'FULL_CALIBRATION_AND_UNCERTAINTY', 'MULTI_EXPOSURE_AND_REFERENCE_VALIDATION',
                             'CURRENT_DUPLICATE_VARIABLE_AND_MOVING_OBJECT_CHECKS',
                             'PROVIDER_CURRENT_REQUIREMENTS', 'OWNER_EXACT_PAYLOAD_AND_RECIPIENT_AUTHORIZATION']}


def render(value):
    """Internal renderer of inspected declarations, not an intake or sendable email."""
    request = value['declarations']; lines = ['PRIVATE PREVIEW - NOT A DISCOVERY REPORT - NOT SENT',
        'Origin declared: ' + request['sourceOriginDeclared'] + ' (not attested)',
        'Intended recipient (not contacted): ' + value['intendedRecipient'],
        'Subject preview: ' + value['subjectPreview'],
        'All values and checks below are declarations, not validated measurements.']
    def add(label, content): lines.append(label + ': ' + ('UNKNOWN' if content is None else content))
    for group, labels in [
        ('author', [('name', 'Observer name'), ('contactEmail', 'Contact email'), ('address', 'Address'),
                    ('experience', 'Observing experience')]),
        ('instrument', [('methodDeclared', 'Observation method (declared)'), ('description', 'Instrument'),
                        ('apertureMeters', 'Aperture (m)'), ('fRatio', 'Focal ratio')]),
        ('position', [('raDegrees', 'RA (degrees, J2000 equinox declared)'),
                      ('decDegrees', 'Dec (degrees, J2000 equinox declared)'),
                      ('rmsRaCosDecArcsec', 'Random RA*cos(Dec) error (1sigma, arcsec)'),
                      ('rmsDecArcsec', 'Random Dec error (1sigma, arcsec)')])]:
        for key, label in labels: add(label, request[group][key])
    add('Site (declared)', request['siteDeclared']); add('Reason for suspecting a new object (declared)', request['noveltyNote'])
    lines.append('Observations (declared count): ' + str(len(request['observations'])))
    for index, row in enumerate(request['observations']):
        lines.append('Observation ' + str(index + 1))
        for key, label in [('obsTime', 'Mid-exposure UTC (declared)'), ('exposureSeconds', 'Exposure (s)'),
                           ('bandpassDeclared', 'Bandpass (declared)'), ('magnitude', 'Magnitude (declared)'),
                           ('magnitudeError', 'Random magnitude error (1sigma, mag)')]: add(label, row[key])
    lines.append('Reference images (declared count): ' + str(len(request['referenceImages'])))
    for index, row in enumerate(request['referenceImages']):
        lines.append('Reference ' + str(index + 1))
        for key, label in [('obsTime', 'Mid-exposure UTC (declared)'), ('bandpassDeclared', 'Bandpass (declared)'),
                           ('limitingMagnitude', 'Limiting magnitude (declared)')]: add(label, row[key])
        add('Reference presence (declared)', {'NOT_ASSESSED': 'Not assessed',
            'NON_DETECTION_DECLARED': 'Nondetection declared, not validated',
            'DETECTION_DECLARED': 'Detection declared, not validated'}[row['presenceDeclared']])
    lines.append('Catalogue checks (declared count): ' + str(len(request['catalogChecks'])))
    for row in request['catalogChecks']:
        add('Check type', {'VARIABLE': 'Variable star', 'MOVING_OBJECT': 'Moving object', 'PREVIOUS_REPORT': 'Previous report'}[row['kind']])
        add('Catalogue (declared)', row['catalogDeclared']); add('Check UTC (declared)', row['checkedUTC'])
        add('Outcome (declared)', {'NOT_CHECKED': 'Not checked', 'NO_MATCH_DECLARED': 'No match declared, not validated',
            'POSSIBLE_MATCH_DECLARED': 'Possible match declared, not validated',
            'INCONCLUSIVE_DECLARED': 'Inconclusive declared, not validated'}[row['outcomeDeclared']])
    lines.extend(['Units: positions in degrees; coordinate random 1sigma RA*cos(Dec) and Dec in arcsec.',
                  'Magnitude errors: declared random 1sigma in mag, never a complete error budget.',
                  'No comparison, nondetection, matching, observing independence or discovery inferred.',
                  'No attachments, image uploads, transport, provider acknowledgement or authorization added.'])
    return ('\n'.join(lines) + '\n').encode('ascii')


def export(registry, request_path, expected_sha, output_root):
    root, source = safe_path(output_root), safe_path(request_path)
    require(root.is_dir(), 'CBAT_OUTPUT_DIRECTORY')
    for other in (registry.artifacts, registry.registry):
        require(root != other and root not in other.parents and other not in root.parents, 'CBAT_ROOT_OVERLAP')
    require(root not in source.parents, 'CBAT_SOURCE_IN_OUTPUT')
    value = inspect(registry, source, expected_sha)
    directory = root / value['declarations']['exportRef']; directory.mkdir()
    try:
        write_new(directory / 'preview.json', value)
        with (directory / 'preview.txt').open('xb') as stream:
            stream.write(render(value)); stream.flush(); os.fsync(stream.fileno())
        require(inspect(registry, source, expected_sha) == value, 'CBAT_SOURCE_CHANGED')
        write_new(directory / 'export.json', {'protocol': PROTOCOL, 'state': 'PRIVATE_PREVIEW',
                  'requestSha256': expected_sha, 'files': {name: fingerprint(directory / name)
                  for name in ('preview.json', 'preview.txt')}, 'externalSubmission': 'NONE'})
    except Exception:
        write_new(directory / 'failed.json', {'state': 'CBAT_PREVIEW_INCOMPLETE'})
        raise
    return directory
