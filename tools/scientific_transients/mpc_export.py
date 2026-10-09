"""Private ADES 2022 preview for declared numbered-object astrometry. Never sends."""
import datetime as dt
from decimal import Decimal
import os
import re
import xml.etree.ElementTree as ET

from tools.pixinsight.local_pilot.broker import opaque, require
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.local_registry import safe_path, fingerprint, relative
from tools.scientific_transients.queue import fields, digest

PROTOCOL = 'DSG_MPC_ADES_PREVIEW_V1'
SCHEMA_COMMIT = 'f4158f96a049b83dfcf848fa33eaac4391db9460'
SCHEMA_SHA256 = '2a5d049808e947cffa11a973a2395c1dde09f00207313a496450b0ef1be27026'
SCHEMA_URL = f'https://raw.githubusercontent.com/IAU-ADES/ADES-Master/{SCHEMA_COMMIT}/xsd/submit.xsd'


def text(value, maximum):
    require(type(value) is str and 0 < len(value) <= maximum and value == value.strip()
            and not any(ord(c) < 32 or c in '|\u007f' for c in value)
            and not any(0xD800 <= ord(c) <= 0xDFFF or ord(c) in (0xFFFE, 0xFFFF) for c in value),
            'MPC_TEXT')
    return value


def decimal(value, low, high, width, fraction, inclusive=True):
    require(type(value) is str and len(value) <= width
            and re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]{1,' + str(fraction) + r'})?', value),
            'MPC_DECIMAL_TEXT')
    number = Decimal(value)
    require(Decimal(str(low)) <= number <= Decimal(str(high)) if inclusive
            else Decimal(str(low)) < number < Decimal(str(high)), 'MPC_DECIMAL_RANGE')
    return value


def names(values):
    require(type(values) is list and 1 <= len(values) <= 64, 'MPC_NAMES')
    return [text(v, 100) for v in values]


def inspect(registry, request_path, expected_sha):
    require(digest(expected_sha), 'MPC_EXPECTED_DIGEST')
    request, actual = read_json(request_path)
    require(actual == expected_sha, 'MPC_REQUEST_CHANGED')
    fields(request, {'protocol', 'exportRef', 'bindingRef', 'manifestSha256',
                     'sourceOriginDeclared', 'context', 'observations'})
    require(request['protocol'] == PROTOCOL and opaque(request['exportRef'])
            and opaque(request['bindingRef']) and digest(request['manifestSha256']), 'MPC_IDENTITY')
    require(type(request['sourceOriginDeclared']) is str
            and request['sourceOriginDeclared'] in {'REAL', 'SYNTHETIC', 'NOT_ATTESTED'}, 'MPC_ORIGIN')
    context = request['context']
    fields(context, {'mpcCode', 'submitterName', 'observers', 'measurers', 'telescope'})
    require(type(context['mpcCode']) is str and re.fullmatch('[A-Za-z0-9]{3}', context['mpcCode']), 'MPC_STATION')
    text(context['submitterName'], 100); names(context['observers']); names(context['measurers'])
    telescope = context['telescope']
    fields(telescope, {'design', 'apertureMeters', 'detector'})
    text(telescope['design'], 35); decimal(telescope['apertureMeters'], 0, 100000, 6, 4, False)
    require(type(telescope['detector']) is str and telescope['detector'] in {'CCD', 'CMO'}, 'MPC_DETECTOR')
    rows = request['observations']
    require(type(rows) is list and 1 <= len(rows) <= 1024, 'MPC_OBSERVATIONS')
    manifest = registry.verify(request['bindingRef'], request['manifestSha256'])
    records = {r['path']: r for r in manifest['files']}
    seen, missing, selected = set(), [], set()
    for row in rows:
        fields(row, {'permID', 'obsTime', 'timeMeaningDeclared', 'coordinateMeaningDeclared',
                     'uncertaintyConventionDeclared', 'ra', 'dec', 'rmsRA', 'rmsDec', 'rmsCorr',
                     'rmsTime', 'astCat', 'imagePath', 'reductionPath'})
        require(type(row['permID']) is str and re.fullmatch('[1-9][0-9]{0,24}', row['permID']), 'MPC_NUMBERED_OBJECT')
        require(type(row['obsTime']) is str and re.fullmatch(
            r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z', row['obsTime']), 'MPC_UTC_TEXT')
        try:
            instant = dt.datetime.fromisoformat(row['obsTime'].replace('Z', '+00:00'))
        except ValueError:
            require(False, 'MPC_UTC_UNSUPPORTED')
        require(row['timeMeaningDeclared'] == 'MID_EXPOSURE_UTC'
                and row['coordinateMeaningDeclared'] == 'J2000_ASTROMETRIC_DEGREES'
                and row['uncertaintyConventionDeclared'] == 'RANDOM_1SIGMA_ARCSEC_RA_COSDEC_TIME_SECONDS', 'MPC_CONVENTIONS')
        key = (row['permID'], instant)
        require(key not in seen, 'MPC_DUPLICATE_OBJECT_TIME'); seen.add(key)
        decimal(row['ra'], 0, 360, 13, 9); require(Decimal(row['ra']) < 360, 'MPC_RA_RANGE')
        decimal(row['dec'], -90, 90, 13, 9)
        require(row['astCat'] == 'Gaia3', 'MPC_CATALOG_SCOPE')
        absent = []
        for key, width, fraction in [('rmsRA', 7, 5), ('rmsDec', 7, 5), ('rmsTime', 8, 6)]:
            if row[key] is None: absent.append(key)
            else: decimal(row[key], 0, 100000, width, fraction, False)
        if row['rmsCorr'] is None: absent.append('rmsCorr')
        else:
            require(row['rmsRA'] is not None and row['rmsDec'] is not None, 'MPC_CORRELATION_WITHOUT_SIGMAS')
            decimal(row['rmsCorr'], -1, 1, 14, 11, False)
        for key in ('imagePath', 'reductionPath'):
            relative(row[key]); require(row[key] in records, 'MPC_UNREGISTERED_EVIDENCE'); selected.add(row[key])
        missing.append({'permID': row['permID'], 'obsTime': row['obsTime'], 'unknownFields': absent})
    return {'protocol': PROTOCOL, 'requestSha256': actual, 'declarations': request,
            'manifest': manifest, 'selectedEvidence': [records[p] for p in sorted(selected)],
            'unknownFieldsByObservation': missing, 'declarationsAttested': False,
            'state': 'PRIVATE_PREVIEW', 'scienceValidation': 'NOT_VALIDATED',
            'submissionAuthorized': False, 'externalSubmission': 'NONE',
            'providerAcknowledgement': 'NONE', 'observingNightOrAssociationValidated': False,
            'schemaValidation': 'NOT_EXECUTED_BY_EXPORTER',
            'schemaReference': {'url': SCHEMA_URL, 'commit': SCHEMA_COMMIT, 'sha256': SCHEMA_SHA256},
            'missingGates': ['FINAL_INDEPENDENT_ASTROMETRY_AND_TIMING', 'REAL_TRACKLET_AND_KNOWN_OBJECT_VALIDATION',
                             'PROVIDER_CURRENT_REQUIREMENTS_AND_SITE_CODE', 'OWNER_EXACT_PAYLOAD_AUTHORIZATION'],
            'completeDependencyArchive': False}


def render(value):
    def add(parent, key, content):
        ET.SubElement(parent, key).text = content
    request = value['declarations']; context = request['context']
    root = ET.Element('ades', version='2022'); block = ET.SubElement(root, 'obsBlock')
    ctx = ET.SubElement(block, 'obsContext')
    add(ET.SubElement(ctx, 'observatory'), 'mpcCode', context['mpcCode'])
    add(ET.SubElement(ctx, 'submitter'), 'name', context['submitterName'])
    for group in ('observers', 'measurers'):
        element = ET.SubElement(ctx, group)
        for name in context[group]: add(element, 'name', name)
    telescope = ET.SubElement(ctx, 'telescope')
    for key, source in [('design', 'design'), ('aperture', 'apertureMeters'), ('detector', 'detector')]:
        add(telescope, key, context['telescope'][source])
    data = ET.SubElement(block, 'obsData')
    for row in request['observations']:
        observation = ET.SubElement(data, 'optical')
        add(observation, 'permID', row['permID']); add(observation, 'mode', context['telescope']['detector'])
        add(observation, 'stn', context['mpcCode'])
        for key in ('obsTime', 'rmsTime', 'ra', 'dec', 'rmsRA', 'rmsDec', 'rmsCorr', 'astCat'):
            if row[key] is not None: add(observation, key, row[key])
    ET.indent(root)
    return ET.tostring(root, encoding='utf-8', xml_declaration=True) + b'\n'


def export(registry, request_path, expected_sha, output_root):
    root, source = safe_path(output_root), safe_path(request_path)
    require(root.is_dir(), 'MPC_OUTPUT_DIRECTORY')
    for other in (registry.artifacts, registry.registry):
        require(root != other and root not in other.parents and other not in root.parents, 'MPC_ROOT_OVERLAP')
    require(root not in source.parents, 'MPC_SOURCE_IN_OUTPUT')
    value = inspect(registry, source, expected_sha)
    directory = root / value['declarations']['exportRef']; directory.mkdir()
    try:
        write_new(directory / 'preview.json', value)
        with (directory / 'preview.xml').open('xb') as stream:
            stream.write(render(value)); stream.flush(); os.fsync(stream.fileno())
        require(inspect(registry, source, expected_sha) == value, 'MPC_SOURCE_CHANGED')
        write_new(directory / 'export.json', {'protocol': PROTOCOL, 'state': 'PRIVATE_PREVIEW',
                  'requestSha256': expected_sha, 'files': {name: fingerprint(directory / name)
                  for name in ('preview.json', 'preview.xml')}, 'externalSubmission': 'NONE'})
    except Exception:
        write_new(directory / 'failed.json', {'state': 'MPC_PREVIEW_INCOMPLETE'})
        raise
    return directory
