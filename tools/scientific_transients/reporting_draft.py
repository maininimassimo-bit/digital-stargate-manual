"""Private preliminary reporting dossier. No classification, submission or readiness."""
import html
import os

from tools.pixinsight.local_pilot.broker import opaque, require
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.local_registry import safe_path, fingerprint, relative
from tools.scientific_transients.queue import fields, digest

PROTOCOL = 'DSG_TRANSIENT_REPORTING_DRAFT_V1'
CHANNELS = {'GALACTIC_NOVA_CANDIDATE': 'CBAT', 'EXTRAGALACTIC_TRANSIENT_CANDIDATE': 'TNS',
            'VARIABLE_STAR_CANDIDATE': 'VSX', 'MOVING_OBJECT_CANDIDATE': 'MPC'}
GAPS = ('INDEPENDENT_SCIENTIFIC_VALIDATION', 'CALIBRATION_AND_UNCERTAINTY',
        'OBSERVATION_TIMING_AND_PASSBAND', 'PROVIDER_CURRENT_REQUIREMENTS',
        'OWNER_SUBMISSION_AUTHORIZATION')


def inspect(registry, request_path, expected_sha):
    require(digest(expected_sha), 'DRAFT_EXPECTED_DIGEST')
    request, actual = read_json(request_path)
    require(actual == expected_sha, 'DRAFT_REQUEST_CHANGED')
    fields(request, {'protocol', 'dossierRef', 'bindingRef', 'manifestSha256',
                     'categoryDeclared', 'channelDeclared', 'dataOriginDeclared', 'note', 'evidencePaths'})
    require(request['protocol'] == PROTOCOL and opaque(request['dossierRef'])
            and opaque(request['bindingRef']) and digest(request['manifestSha256']), 'DRAFT_IDENTITY')
    category, channel = request['categoryDeclared'], request['channelDeclared']
    require(type(category) is str and type(channel) is str
            and CHANNELS.get(category) == channel, 'DRAFT_DECLARED_CHANNEL')
    require(type(request['dataOriginDeclared']) is str
            and request['dataOriginDeclared'] in {'REAL', 'SYNTHETIC', 'NOT_ATTESTED'}, 'DRAFT_DECLARED_ORIGIN')
    require(type(request['note']) is str and len(request['note']) <= 4096
            and not any(ord(c) < 32 and c not in '\n\t' for c in request['note']), 'DRAFT_NOTE')
    paths = request['evidencePaths']
    require(type(paths) is list and 1 <= len(paths) <= 128
            and all(type(p) is str for p in paths) and len(set(paths)) == len(paths), 'DRAFT_EVIDENCE')
    for path in paths: relative(path)
    manifest = registry.verify(request['bindingRef'], request['manifestSha256'])
    records = {r['path']: r for r in manifest['files']}
    require(all(p in records for p in paths), 'DRAFT_UNREGISTERED_EVIDENCE')
    return {'protocol': PROTOCOL, 'classification': 'PRIVATE', 'state': 'DRAFT',
            'requestSha256': actual, 'declarations': request,
            'declarationsAttested': False, 'manifest': manifest,
            'selectedEvidence': [records[p] for p in paths],
            'integrityScope': 'POINT_IN_TIME_REGISTERED_BYTES_ONLY',
            'scienceValidation': 'NOT_VALIDATED', 'scientificClassification': 'NOT_EVALUATED',
            'missingGates': list(GAPS), 'externalSubmission': 'NONE', 'submissionAuthorized': False,
            'providerAcknowledgement': 'NONE', 'completeDependencyArchive': False,
            'artifactRoot': registry.artifacts.as_posix()}


def render(value):
    esc = lambda v: html.escape(str(v), quote=True)
    declarations = value['declarations']
    return ('<!doctype html><html lang="it"><meta charset="utf-8">'
            '<meta http-equiv="Content-Security-Policy" content="default-src &#39;none&#39;; '
            'base-uri &#39;none&#39;; form-action &#39;none&#39;">'
            '<title>Dossier preliminare privato</title><h1>Dossier preliminare privato</h1>'
            '<p>BOZZA. Nessuna scoperta attestata, autorizzazione o segnalazione inviata.</p>'
            '<p>Categoria e canale dichiarati: ' + esc(declarations['categoryDeclared']) + ' / '
            + esc(declarations['channelDeclared']) + '. Origine dichiarata: '
            + esc(declarations['dataOriginDeclared']) + ', non attestata.</p><pre>'
            + esc(declarations['note']) + '</pre><h2>Evidenze registrate</h2><ul>'
            + ''.join('<li>' + esc(r['path']) + ' — SHA256 ' + esc(r['sha256']) + '</li>'
                      for r in value['selectedEvidence']) + '</ul><h2>Verifiche ancora necessarie</h2><ul>'
            + ''.join('<li>' + esc(g) + '</li>' for g in value['missingGates'])
            + '</ul><p>Integrità dei byte al momento della verifica. Validazione scientifica: '
            'NOT_VALIDATED. Nessuna misura, unità, banda o data osservativa viene dedotta dalla bozza.</p>'
            '<p>Archivio dipendenze non completo: conservare la radice privata ' + esc(value['artifactRoot'])
            + ' e il registro genitore.</p></html>')


def export(registry, request_path, expected_sha, output_root):
    root, source = safe_path(output_root), safe_path(request_path)
    require(root.is_dir(), 'DRAFT_OUTPUT_DIRECTORY')
    for other in (registry.artifacts, registry.registry):
        require(root != other and root not in other.parents and other not in root.parents,
                'DRAFT_ROOT_OVERLAP')
    require(root not in source.parents, 'DRAFT_SOURCE_IN_OUTPUT')
    value = inspect(registry, source, expected_sha)
    directory = root / value['declarations']['dossierRef']
    directory.mkdir()  # Reuse/partial directories block retries; never overwrite.
    try:
        write_new(directory / 'dossier.json', value)
        with (directory / 'dossier.html').open('xb') as stream:
            stream.write(render(value).encode('utf-8')); stream.flush(); os.fsync(stream.fileno())
        require(inspect(registry, source, expected_sha) == value, 'DRAFT_SOURCE_CHANGED')
        files = {name: fingerprint(directory / name) for name in ('dossier.json', 'dossier.html')}
        write_new(directory / 'export.json', {'protocol': PROTOCOL, 'state': 'DRAFT',
                  'requestSha256': expected_sha, 'files': files, 'externalSubmission': 'NONE'})
    except Exception:
        write_new(directory / 'failed.json', {'state': 'DRAFT_EXPORT_INCOMPLETE'})
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
        parser.exit(2, 'Bozza non esportata integralmente. Conservare i file parziali. Nessun invio effettuato.\n')
    print('PRIVATE_DRAFT_EXPORTED_NO_SUBMISSION_OR_SCIENCE_ACCEPTANCE')


if __name__ == '__main__': main()
