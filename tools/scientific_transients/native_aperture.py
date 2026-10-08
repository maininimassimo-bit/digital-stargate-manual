"""Prepare/collect trusted local PJSR runs. No subprocess, credentials, network or discovery."""
import math
from pathlib import Path

from tools.pixinsight.local_pilot.broker import encode, opaque, require
from tools.scientific_transients.attempt_journal import read_json, write_new, copy_verified
from tools.scientific_transients.local_registry import safe_path, fingerprint
from tools.scientific_transients.queue import fields

PROTOCOL = "DSG_NATIVE_APERTURE_V1"
ENGINE = Path('C:/Program Files/PixInsight/src/scripts/AperturePhotometry/AperturePhotometryEngine.js')
CATALOG = ENGINE.with_name('AperturePhotometryCatalogs.js')
LIBRARY = Path(__file__).with_suffix('.jsh')


def finite(value): return type(value) in {int, float} and math.isfinite(value)


def validate_row(row, target):
    fields(row, {'sourceRef','x','y','clipped','backgroundAvailable','fluxNormalizedSampleSum','area','background',
                 'skyNoiseDiagnostic','skySampleCount','fullVariance','significance','scienceValidation'})
    require(all(row[k] == target[k] for k in ['sourceRef','x','y']) and type(row['clipped']) is bool
            and type(row['backgroundAvailable']) is bool and row['fullVariance'] is None
            and row['significance'] is None and row['scienceValidation'] == 'NOT_VALIDATED', 'AP_ROW')
    require(type(row['skySampleCount']) is int and row['skySampleCount'] >= 0, 'AP_ROW')
    if row['clipped']:
        require(row['backgroundAvailable'] is False and row['area'] is None and row['skySampleCount'] == 0, 'AP_ROW')
    else:
        require(finite(row['area']) and row['area'] > 0 and row['backgroundAvailable'] == (row['skySampleCount'] > 0), 'AP_ROW')
    if row['backgroundAvailable']:
        require(all(finite(row[k]) for k in ['fluxNormalizedSampleSum','background','skyNoiseDiagnostic'])
                and row['skyNoiseDiagnostic'] >= 0, 'AP_ROW')
    else:
        require(all(row[k] is None for k in ['fluxNormalizedSampleSum','background','skyNoiseDiagnostic']), 'AP_ROW')


def validate(image, parameters, targets):
    fields(image, {'imageIndex', 'width', 'height', 'channels', 'linearity'})
    require(type(image['imageIndex']) is int and 0 <= image['imageIndex'] < 16, 'AP_IMAGE_INDEX')
    require(all(type(image[k]) is int and image[k] > 0 for k in ['width', 'height'])
            and image['width'] * image['height'] <= 100000000 and type(image['channels']) is int
            and image['channels'] == 1 and image['linearity'] == 'DECLARED_LINEAR_NOT_ATTESTED', 'AP_INPUT')
    fields(parameters, {'coordinateConvention', 'apertureRadius', 'annulusInner', 'annulusOuter'})
    require(parameters['coordinateConvention'] == 'PI_NATIVE_GEOMETRIC'
            and all(finite(parameters[k]) for k in ['apertureRadius', 'annulusInner', 'annulusOuter'])
            and 0 < parameters['apertureRadius'] <= 512
            and 1 < parameters['annulusInner'] < parameters['annulusOuter'] <= 16, 'AP_PARAMETERS')
    require(type(targets) is list and 0 < len(targets) <= 1024, 'AP_TARGETS')
    ids = set()
    for target in targets:
        fields(target, {'sourceRef', 'x', 'y'})
        require(opaque(target['sourceRef']) and target['sourceRef'] not in ids
                and finite(target['x']) and finite(target['y'])
                and 0 <= target['x'] < image['width'] and 0 <= target['y'] < image['height'], 'AP_TARGET')
        ids.add(target['sourceRef'])


def prepare_run(input_path, run_root, operation_ref, image, parameters, targets, expected_version,
                *, engine=ENGINE, catalog=CATALOG):
    """Caller chooses trusted local files and runtime. Never consumes a portal payload."""
    validate(image, parameters, targets)
    require(opaque(operation_ref) and type(expected_version) is str and 0 < len(expected_version) <= 64, 'AP_RUNTIME')
    source, root = safe_path(input_path), safe_path(run_root)
    require(root.is_dir() and source.is_file(), 'AP_ROOT')
    require(not any(c in str(root) for c in ['"', '\r', '\n', '\x00']), 'AP_ROOT')
    directory = root / operation_ref; directory.mkdir()
    expected = fingerprint(source)
    copy_verified(source, directory / 'input.xisf', expected)
    runtime = {'librarySha256': fingerprint(LIBRARY)['sha256'], 'engineSha256': fingerprint(engine)['sha256'],
               'catalogSha256': fingerprint(catalog)['sha256'], 'pixInsightVersion': expected_version}
    copy_verified(LIBRARY, directory / 'native_aperture.jsh', fingerprint(LIBRARY))
    manifest = {'protocol': PROTOCOL, 'runDirectory': str(directory).replace('\\', '/'), 'operationRef': operation_ref,
                'input': {**image, 'sha256': expected['sha256']}, 'parameters': parameters, 'runtime': runtime, 'targets': targets}
    write_new(directory / 'parameters.json', manifest)
    # No executable text supplied by the caller. Installed includes stay external dependencies.
    launcher = ('#engine v8\n#define SETTINGS_MODULE "DSGScientificApertureReadOnly"\n'
                '#define TITLE "DSGScientificApertureReadOnly"\n#define VERSION "1.0"\n'
                '#include "C:/Program Files/PixInsight/src/scripts/AperturePhotometry/AperturePhotometryEngine.js"\n'
                '#include "' + str(directory / 'native_aperture.jsh').replace('\\', '/') + '"\n'
                'console.beginLog(' + encode(str(directory / 'Console.txt').replace('\\', '/')).decode('utf-8') + ');\n'
                'try { DSGNativeAperture(JSON.parse(File.readTextFile(' + encode(str(directory / 'parameters.json').replace('\\', '/')).decode('utf-8') + '))); } finally { console.endLog(); }\n')
    with (directory / 'entry.js').open('xb') as stream: stream.write(launcher.replace('\n', '\r\n').encode('utf-8'))
    write_new(directory / 'preflight.json', {'parameters': fingerprint(directory / 'parameters.json'),
            'launcher': fingerprint(directory / 'entry.js'), 'input': expected,
            'nativeLibrary': fingerprint(directory / 'native_aperture.jsh'),
            'engine': fingerprint(engine), 'catalog': fingerprint(catalog), 'completeDependencyArchive': False})
    return directory


def inspect_prepared_run(directory, expected_operation, *, engine=ENGINE, catalog=CATALOG):
    directory = safe_path(directory)
    require(opaque(expected_operation) and directory.name == expected_operation, 'AP_OPERATION')
    manifest, _ = read_json(directory / 'parameters.json')
    fields(manifest, {'protocol', 'runDirectory', 'operationRef', 'input', 'parameters', 'runtime', 'targets'})
    require(manifest['operationRef'] == expected_operation and manifest['protocol'] == PROTOCOL
            and manifest['runDirectory'] == str(directory).replace('\\', '/'), 'AP_OPERATION')
    image = dict(manifest['input']); expected_input_sha = image.pop('sha256')
    validate(image, manifest['parameters'], manifest['targets'])
    preflight, _ = read_json(directory / 'preflight.json')
    fields(preflight, {'parameters', 'launcher', 'input', 'nativeLibrary', 'engine', 'catalog', 'completeDependencyArchive'})
    require(preflight['completeDependencyArchive'] is False, 'AP_DEPENDENCIES')
    for key, path in [('parameters','parameters.json'),('launcher','entry.js'),('input','input.xisf'),('nativeLibrary','native_aperture.jsh')]:
        require(fingerprint(directory / path) == preflight[key], 'AP_BYTES_CHANGED')
    require(fingerprint(engine) == preflight['engine'] and fingerprint(catalog) == preflight['catalog'], 'AP_RUNTIME_CHANGED')
    fields(manifest['runtime'], {'librarySha256','engineSha256','catalogSha256','pixInsightVersion'})
    require(manifest['runtime']['librarySha256'] == preflight['nativeLibrary']['sha256']
            and manifest['runtime']['engineSha256'] == preflight['engine']['sha256']
            and manifest['runtime']['catalogSha256'] == preflight['catalog']['sha256']
            and expected_input_sha == preflight['input']['sha256'], 'AP_RUNTIME_BINDING')
    return manifest


def collect_run(directory, expected_operation, *, engine=ENGINE, catalog=CATALOG):
    directory = safe_path(directory)
    manifest = inspect_prepared_run(directory, expected_operation, engine=engine, catalog=catalog)
    image, expected_input_sha = manifest['input'], manifest['input']['sha256']
    terminal, _ = read_json(directory / 'terminal.json')
    require(terminal.get('state') == 'COMPLETED', 'AP_RUN_NOT_COMPLETED')
    fields(terminal, {'protocol','operationRef','state','runtime','inputSha256','imageIndex','rows','changedPixels',
                     'checkpointSha256','historySha256','parametersSha256','scienceValidation','unit',
                     'fullAperturePhotometryWorkflowExecuted','providerRequestsInvoked'})
    require(terminal['protocol'] == PROTOCOL and terminal['operationRef'] == expected_operation
            and terminal['runtime'] == manifest['runtime'] and terminal['inputSha256'] == expected_input_sha
            and terminal['imageIndex'] == image['imageIndex'] and type(terminal['changedPixels']) is int
            and terminal['changedPixels'] == 0 and terminal['scienceValidation'] == 'NOT_VALIDATED'
            and terminal['unit'] == 'NORMALIZED_SAMPLE_SUM' and terminal['fullAperturePhotometryWorkflowExecuted'] is False
            and type(terminal['providerRequestsInvoked']) is int and terminal['providerRequestsInvoked'] == 0, 'AP_TERMINAL')
    for key, path in [('checkpointSha256','checkpoint.xisf'),('historySha256','checkpoint-current.js'),('parametersSha256','parameters.json')]:
        require(fingerprint(directory / path)['sha256'] == terminal[key], 'AP_OUTPUT_CHANGED')
    require(type(terminal['rows']) is list and len(terminal['rows']) == len(manifest['targets']), 'AP_ROWS')
    clipped = 0
    for i, (row, target) in enumerate(zip(terminal['rows'], manifest['targets']), 1):
        validate_row(row, target)
        clipped += row['clipped']
        require(read_json(directory / ('measurement-' + str(i).zfill(5) + '.json'))[0] == row, 'AP_ROW_CHANGED')
    # Kernel reads do not add process instances to native image History; preserve both exports and receipt.
    history = {'scope': 'NATIVE_OPENED_VIEW_HISTORY_PLUS_READ_ONLY_KERNEL_RECEIPT', 'upstreamAcquisitionHistory': 'NOT_ATTESTED',
               'operationRef': expected_operation, 'inputSha256': expected_input_sha, 'terminal': terminal,
               'exports': {name: safe_path(directory / name).read_text(encoding='utf-8') for name in
                           ['input-initial.js','input-current.js','checkpoint-initial.js','checkpoint-current.js']}}
    path = directory / 'history-bundle.json'
    if path.exists(): require(path.read_bytes() == encode(history), 'AP_HISTORY_CHANGED')
    else: write_new(path, history)
    return {'operationRef': expected_operation, 'sources': {'CHECKPOINT': directory / 'checkpoint.xisf',
            'PARAMETERS': directory / 'parameters.json', 'HISTORY': path},
            'qualityCounts': {'measured': 0, 'excluded': clipped, 'incomplete': len(terminal['rows']) - clipped},
            'nativeRows': terminal['rows'], 'scienceValidation': 'NOT_VALIDATED'}
