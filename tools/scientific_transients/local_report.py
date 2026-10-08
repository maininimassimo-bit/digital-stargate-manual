"""Private report of a sealed attempt. No native launch, network, acceptance or recovery."""
import html

from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.local_registry import safe_path, fingerprint
from tools.scientific_transients.queue import digest, fields

PROTOCOL = 'DSG_TRANSIENT_LOCAL_REPORT_V1'


def kernel_rows(bundle, parameters, checkpoint, operation):
    """Verify correlations of retained declarations; no scientific truth is granted."""
    fields(bundle, {'scope', 'upstreamAcquisitionHistory', 'operationRef', 'inputSha256', 'terminal', 'exports'})
    require(bundle['scope'] == 'NATIVE_OPENED_VIEW_HISTORY_PLUS_READ_ONLY_KERNEL_RECEIPT'
            and bundle['upstreamAcquisitionHistory'] == 'NOT_ATTESTED'
            and bundle['operationRef'] == operation, 'REPORT_HISTORY_SCOPE')
    fields(bundle['exports'], {'input-initial.js', 'input-current.js', 'checkpoint-initial.js', 'checkpoint-current.js'})
    require(all(type(v) is str for v in bundle['exports'].values()), 'REPORT_HISTORY_EXPORTS')
    terminal = bundle['terminal']
    fields(terminal, {'protocol', 'operationRef', 'state', 'runtime', 'inputSha256', 'imageIndex', 'rows',
                     'changedPixels', 'checkpointSha256', 'historySha256', 'parametersSha256',
                     'scienceValidation', 'unit', 'fullAperturePhotometryWorkflowExecuted', 'providerRequestsInvoked'})
    manifest = parameters[0]
    fields(manifest, {'protocol', 'runDirectory', 'operationRef', 'input', 'parameters', 'runtime', 'targets'})
    require(terminal['protocol'] == manifest['protocol'] == 'DSG_NATIVE_APERTURE_V1'
            and terminal['operationRef'] == manifest['operationRef'] == operation
            and terminal['state'] == 'COMPLETED' and terminal['scienceValidation'] == 'NOT_VALIDATED'
            and terminal['unit'] == 'NORMALIZED_SAMPLE_SUM'
            and terminal['fullAperturePhotometryWorkflowExecuted'] is False
            and type(terminal['providerRequestsInvoked']) is int and terminal['providerRequestsInvoked'] == 0
            and type(terminal['changedPixels']) is int and terminal['changedPixels'] == 0
            and terminal['runtime'] == manifest['runtime']
            and terminal['inputSha256'] == bundle['inputSha256'] == manifest['input']['sha256']
            and terminal['imageIndex'] == manifest['input']['imageIndex']
            and terminal['checkpointSha256'] == checkpoint['sha256']
            and terminal['parametersSha256'] == parameters[1], 'REPORT_KERNEL_BINDING')
    import hashlib
    require(terminal['historySha256'] == hashlib.sha256(bundle['exports']['checkpoint-current.js'].encode('utf-8')).hexdigest(),
            'REPORT_HISTORY_BINDING')
    from tools.scientific_transients.native_aperture import validate, validate_row
    image = dict(manifest['input']); image.pop('sha256')
    validate(image, manifest['parameters'], manifest['targets'])
    require(type(terminal['rows']) is list and len(terminal['rows']) == len(manifest['targets']), 'REPORT_ROWS')
    for row, target in zip(terminal['rows'], manifest['targets']):
        validate_row(row, target)
    return {'operationRef': operation, 'unit': terminal['unit'], 'coordinateConvention': manifest['parameters']['coordinateConvention'],
            'parameters': manifest['parameters'], 'rows': terminal['rows'], 'runtime': terminal['runtime']}


def inspect(journal, expected_report_sha):
    require(digest(expected_report_sha), 'REPORT_EXPECTED_DIGEST')
    events = journal._events()
    require(events and events[-1]['kind'] == 'COMPLETED', 'REPORT_ATTEMPT_NOT_COMPLETED')
    journal._verify_artifacts(events)
    report, actual = read_json(journal.directory / 'report.json')
    fields(report, {'protocol', 'identity', 'journalParentSha256', 'qualityCounts', 'nativeExecution', 'scienceValidation'})
    require(actual == expected_report_sha == events[-1]['data']['reportSha256']
            and report['identity'] == journal.anchor['identity']
            and report['journalParentSha256'] == events[-1]['previousSha256']
            and report['protocol'] == journal.anchor['protocol']
            and report['nativeExecution'] == 'CALLER_REPORTED_NOT_ATTESTED'
            and report['scienceValidation'] == 'NOT_VALIDATED', 'REPORT_SEAL_MISMATCH')
    fields(report['qualityCounts'], {'measured', 'excluded', 'incomplete'})
    require(all(type(v) is int and 0 <= v <= 10000000 for v in report['qualityCounts'].values()), 'REPORT_COUNTS')
    artifacts = list(journal.anchor['snapshot'])
    operations, measurements = [], []
    for event in events:
        if event['kind'] not in {'OPERATION_STARTED', 'CHECKPOINT'}: continue
        artifacts.extend(event['data']['files'])
        if event['kind'] == 'OPERATION_STARTED': operations.append(event['data']['processRef'])
        else:
            rows = {r['role']: r for r in event['data']['files']}
            bundle, _ = read_json(journal.directory / rows['HISTORY']['path'])
            parameters = read_json(journal.directory / rows['PARAMETERS']['path'])
            require(any(r['role'] == 'PARAMETERS' and r['sha256'] == parameters[1] for r in journal.anchor['snapshot'])
                    and any(r['role'] == 'INPUT' and r['sha256'] == bundle.get('inputSha256') for r in journal.anchor['snapshot']),
                    'REPORT_SNAPSHOT_BINDING')
            measurements.append(kernel_rows(bundle, parameters, rows['CHECKPOINT'], event['data']['processRef']))
    all_rows = [r for m in measurements for r in m['rows']]
    excluded = sum(r['clipped'] for r in all_rows)
    require(report['qualityCounts'] == {'measured': 0, 'excluded': excluded, 'incomplete': len(all_rows) - excluded},
            'REPORT_COUNTS_BINDING')
    return {'protocol': PROTOCOL, 'classification': 'PRIVATE', 'identity': report['identity'],
            'technicalReportSha256': actual, 'journalHeadSha256': journal.head_sha,
            'technicalState': 'COMPLETED', 'nativeExecution': report['nativeExecution'], 'scienceValidation': 'NOT_VALIDATED',
            'qualityCountsDeclared': report['qualityCounts'], 'operations': operations, 'measurements': measurements,
            'artifacts': artifacts, 'artifactRoot': journal.directory.as_posix(),
            'completeDependencyArchive': False, 'upstreamAcquisitionHistory': 'NOT_ATTESTED',
            'scientificClassification': 'NOT_EVALUATED', 'externalSubmission': 'NONE',
            'ownerAcceptance': 'NOT_GRANTED_BY_EXPORT', 'remoteAcknowledgement': 'NOT_ESTABLISHED_BY_EXPORT'}


def render(value):
    def esc(v): return html.escape('sconosciuta' if v is None else 'sì' if v is True else 'no' if v is False else str(v))
    parts = ['<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width">',
             '<meta http-equiv="Content-Security-Policy" content="default-src &#39;none&#39;; style-src &#39;unsafe-inline&#39;">',
             '<title>Rapporto scientifico privato</title><style>body{font:17px system-ui;max-width:1100px;margin:2rem auto;padding:1rem;background:#101823;color:#edf3ff}td,th{padding:.5rem;text-align:left;border-bottom:1px solid #536070}table{border-collapse:collapse}code{overflow-wrap:anywhere}.scroll{overflow:auto}</style>',
             '<h1>Rapporto scientifico privato</h1><p>Completamento tecnico. Validazione scientifica: NOT_VALIDATED. ',
             'Questo rapporto non attesta un candidato, una scoperta, un limite di non rilevamento o una segnalazione.</p>',
             '<p>Ricevuta tecnica mostrata nel portale: <code>' + esc(value['technicalReportSha256']) + '</code></p>',
             '<p>Job: <code>' + esc(value['identity']['jobId']) + '</code></p>',
             '<p>Unità del flusso: NORMALIZED_SAMPLE_SUM, non ADU calibrati. Varianza completa e significatività sconosciute. ',
             'Coordinate: PI_NATIVE_GEOMETRIC. Misure a posizioni dichiarate; nessuna ricerca cieca attestata.</p>']
    for measurement in value['measurements']:
        parts.append('<h2>Operazione ' + esc(measurement['operationRef']) + '</h2><div class="scroll"><table><thead><tr>')
        keys = ['sourceRef', 'fluxNormalizedSampleSum', 'background', 'clipped', 'fullVariance', 'significance']
        labels = ['Sorgente', 'Flusso (somma normalizzata)', 'Fondo', 'Apertura tagliata', 'Varianza completa', 'Significatività']
        parts.extend('<th scope="col">' + esc(k) + '</th>' for k in labels)
        parts.append('</tr></thead><tbody>')
        for row in measurement['rows']:
            parts.append('<tr>' + ''.join('<td>' + esc(row[k]) + '</td>' for k in keys) + '</tr>')
        parts.append('</tbody></table></div>')
    parts.append('<h2>Provenienza e limiti</h2><p>History a monte: NOT_ATTESTED. Esecuzione: CALLER_REPORTED_NOT_ATTESTED. ')
    parts.append('Il rapporto JSON conserva tutte le righe e i parametri. I checkpoint e le dipendenze restano esterni: ')
    parts.append('<code>' + esc(value['artifactRoot']) + '</code>. Conservare questa cartella. Il digest tecnico e il digest ')
    parts.append('del rapporto esportato sono distinti. L’esportazione non modifica la coda né concede accettazione Owner.</p></html>')
    return ''.join(parts)


def export(journal, expected_report_sha, output_root):
    """Exclusive passive export, preserving partial failures. No lease or credential access."""
    root = safe_path(output_root)
    require(root.is_dir() and root != journal.directory and root not in journal.directory.parents
            and journal.directory not in root.parents, 'REPORT_ROOT_OVERLAP')
    value = inspect(journal, expected_report_sha)
    directory = root / journal.anchor['identity']['attemptId']; directory.mkdir()
    try:
        report_sha = write_new(directory / 'report.json', value)
        with (directory / 'report.html').open('xb') as stream:
            stream.write(render(value).encode('utf-8'))
            stream.flush()
            import os
            os.fsync(stream.fileno())
        require(inspect(journal, expected_report_sha) == value, 'REPORT_SOURCE_CHANGED')
        files = {name: fingerprint(directory / name) for name in ('report.json', 'report.html')}
        write_new(directory / 'export.json', {'protocol': PROTOCOL, 'technicalReportSha256': expected_report_sha,
                  'localReportSha256': report_sha, 'files': files, 'externalSubmission': 'NONE'})
    except Exception:
        write_new(directory / 'failed.json', {'state': 'EXPORT_INCOMPLETE_SOURCE_RECHECK_REQUIRED'})
        raise
    return directory


def main():
    import argparse
    from pathlib import Path
    from tools.pixinsight.local_pilot.broker import ProtocolError
    from tools.scientific_transients.attempt_journal import AttemptJournal
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--attempt-directory', type=Path, required=True)
    parser.add_argument('--expected-report-sha256', required=True,
                        help='Exact technical report digest obtained independently, e.g. Owner receipt')
    parser.add_argument('--output-root', type=Path, required=True, help='Existing separate private directory')
    args = parser.parse_args()
    try:
        anchor, _ = read_json(args.attempt_directory / 'attempt.json')
        journal = AttemptJournal(args.attempt_directory, anchor['identity'])
        export(journal, args.expected_report_sha256, args.output_root)
    except (ProtocolError, OSError, KeyError, TypeError, ValueError):
        parser.exit(1, 'Rapporto non esportato integralmente. Conservare eventuali file parziali; nessuna elaborazione avviata.\n')
    print('PRIVATE_LOCAL_REPORT_EXPORTED_NOT_SCIENCE_ACCEPTANCE')


if __name__ == '__main__': main()
