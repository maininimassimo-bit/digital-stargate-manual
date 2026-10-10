"""Passive private archive of a sealed attempt; no execution, extraction or network."""
import hashlib
import os
import zipfile

from tools.pixinsight.local_pilot.broker import encode, require
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.local_registry import safe_path, relative, fingerprint
from tools.scientific_transients.local_report import inspect, render

PROTOCOL = 'DSG_TRANSIENT_RETAINED_REPORT_BUNDLE_V1'
MAX_BYTES = 8 * 1024 ** 3  # Storage bound, not a scientific threshold.


def export_bundle(journal, expected_report_sha, output_root):
    """Archive only referenced, verified evidence. Partial output blocks retry."""
    root = safe_path(output_root)
    require(root.is_dir() and root != journal.directory and root not in journal.directory.parents
            and journal.directory not in root.parents, 'BUNDLE_ROOT_OVERLAP')
    value = inspect(journal, expected_report_sha)
    events = journal._events()
    rows = {r['path']: {k: r[k] for k in ('bytes', 'sha256')} for r in value['artifacts']}
    for name in ['attempt.json', 'report.json'] + ['events/' + str(i).zfill(3) + '.json'
                                                for i in range(1, len(events) + 1)]:
        rows[name] = fingerprint(journal.directory / relative(name))
    require(sum(r['bytes'] for r in rows.values()) <= MAX_BYTES, 'BUNDLE_SIZE_LIMIT')
    directory = root / journal.anchor['identity']['attemptId']
    directory.mkdir()
    archive = directory / 'retained-report.zip'
    try:
        entries = []
        with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_STORED) as bundle:
            for name, expected in sorted(rows.items()):
                path = safe_path(journal.directory / relative(name))
                require(fingerprint(path) == expected, 'BUNDLE_SOURCE_CHANGED')
                sha, size = hashlib.sha256(), 0
                with path.open('rb') as source, bundle.open('attempt/' + name, 'w', force_zip64=True) as target:
                    while chunk := source.read(1024 * 1024):
                        size += len(chunk)
                        require(size <= expected['bytes'], 'BUNDLE_SOURCE_CHANGED')
                        sha.update(chunk); target.write(chunk)
                require({'bytes': size, 'sha256': sha.hexdigest()} == expected
                        and fingerprint(path) == expected, 'BUNDLE_SOURCE_CHANGED')
                entries.append({'path': 'attempt/' + name, **expected})
            for name, raw in [('report.json', encode(value)), ('report.html', render(value).encode('utf-8'))]:
                bundle.writestr(name, raw)
                entries.append({'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
            manifest = {'protocol': PROTOCOL, 'classification': 'PRIVATE',
                        'technicalReportSha256': expected_report_sha, 'journalHeadSha256': value['journalHeadSha256'],
                        'entries': entries, 'scope': 'REFERENCED_RETAINED_ATTEMPT_ONLY',
                        'completeDependencyArchive': False, 'scienceValidation': 'NOT_VALIDATED',
                        'externalSubmission': 'NONE', 'ownerAcceptance': 'NOT_GRANTED_BY_EXPORT'}
            bundle.writestr('manifest.json', encode(manifest))
        with safe_path(archive).open('r+b') as stream: os.fsync(stream.fileno())
        require(inspect(journal, expected_report_sha) == value, 'BUNDLE_SOURCE_CHANGED')
        with zipfile.ZipFile(archive) as bundle:
            require(set(bundle.namelist()) == {r['path'] for r in entries} | {'manifest.json'}
                    and len(bundle.namelist()) == len(entries) + 1, 'BUNDLE_ENTRY_SET')
            for entry in entries:
                sha, size = hashlib.sha256(), 0
                with bundle.open(entry['path']) as stream:
                    while chunk := stream.read(1024 * 1024): sha.update(chunk); size += len(chunk)
                require({'bytes': size, 'sha256': sha.hexdigest()} ==
                        {k: entry[k] for k in ('bytes', 'sha256')}, 'BUNDLE_VERIFY')
            require(bundle.read('manifest.json') == encode(manifest), 'BUNDLE_MANIFEST')
        write_new(directory / 'bundle-receipt.json', {'protocol': PROTOCOL, 'archive': fingerprint(archive),
                  'entryCount': len(entries) + 1, 'technicalReportSha256': expected_report_sha,
                  'journalHeadSha256': value['journalHeadSha256'], 'scope': manifest['scope'],
                  'completeDependencyArchive': False, 'scienceValidation': 'NOT_VALIDATED'})
    except Exception:
        write_new(directory / 'failed.json', {'state': 'BUNDLE_INCOMPLETE_SOURCE_RECHECK_REQUIRED'})
        raise
    return directory


def main():
    import argparse
    from pathlib import Path
    from tools.pixinsight.local_pilot.broker import ProtocolError
    from tools.scientific_transients.attempt_journal import AttemptJournal
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--attempt-directory', type=Path, required=True)
    parser.add_argument('--expected-report-sha256', required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    args = parser.parse_args()
    try:
        anchor, _ = read_json(args.attempt_directory / 'attempt.json')
        journal = AttemptJournal(args.attempt_directory, anchor['identity'])
        export_bundle(journal, args.expected_report_sha256, args.output_root)
    except (ProtocolError, OSError, KeyError, TypeError, ValueError, zipfile.BadZipFile):
        parser.exit(1, 'Archivio incompleto. Conservare i file parziali; nessuna elaborazione avviata.\n')
    print('PRIVATE_RETAINED_REPORT_BUNDLE_VERIFIED_NOT_SCIENCE_ACCEPTANCE')


if __name__ == '__main__': main()
