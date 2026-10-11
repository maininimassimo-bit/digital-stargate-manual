"""Prepare and verify a read-only native measurement instance; never launch it.

Explicit input selection and allowed local roots come from the existing private
worker scope. No directory discovery, network, credentials or native processing.
"""
import copy
from pathlib import Path
import shutil

from .broker import require, encode, decode
from .intake import local_directory
from .image_analysis import fingerprint
from .source_provenance import _image
from .native_measurements import validate
from .adaptive_ledger import digest

VERSION='DSG_PIAI_READ_ONLY_ANALYSIS_V2'


def local_file(value, roots):
    text=str(value)
    local_directory(text)
    require(not any(ord(c)<32 for c in text) and Path(text).suffix.lower()=='.xisf', 'ANALYSIS_LOCAL_XISF')
    path=Path(text)
    # Reject reparse links before resolution, including every existing ancestor.
    require(all(not p.is_symlink() and not p.is_junction() for p in (path,*path.parents)), 'ANALYSIS_REPARSE_POINT')
    scoped_roots=[]
    for root in roots:
        root_path=Path(local_directory(str(root)))
        require(all(not p.is_symlink() and not p.is_junction() for p in (root_path,*root_path.parents)),
                'ANALYSIS_SCOPE_REPARSE_POINT')
        scoped_roots.append(root_path.resolve(strict=True))
    resolved=path.resolve(strict=True)
    require(any(resolved.is_relative_to(root) for root in scoped_roots),
            'ANALYSIS_OUTSIDE_SCOPE')
    require(resolved.is_file() and resolved.stat().st_size<=1073741824,'ANALYSIS_INPUT_SIZE')
    return resolved


def prepare(directory, inputs, *, allowed_roots, pixinsight_root):
    require(isinstance(inputs,list) and 1<=len(inputs)<=4 and isinstance(allowed_roots,list) and
            1<=len(allowed_roots)<=16,'ANALYSIS_SELECTION')
    directory=Path(directory)
    require(all(not p.is_symlink() and not p.is_junction() for p in (directory,*directory.parents)),
            'ANALYSIS_OUTPUT_REPARSE_POINT')
    directory.mkdir(exist_ok=False,parents=False)
    pi=Path(pixinsight_root);library=Path(__file__).parent/'measurements.jsh'
    detector=pi/'include/pjsr/StarDetector.jsh'
    rows=[];roles=set()
    for row in inputs:
        fields={'role','path','sha256','imageIndex','width','height','channels','regions'}
        require(isinstance(row,dict) and set(row)==fields and row['role'] in
                {'R','G','B','L','RGB','SII','Ha','OIII'} and row['role'] not in roles and digest(row['sha256']) and
                all(type(row[k]) is int and 32<=row[k]<=12000 for k in ('width','height')) and
                type(row['channels']) is int and row['channels'] in (1,3),'ANALYSIS_INPUT_FIELDS')
        require(isinstance(row['regions'],list) and 1<=len(row['regions'])<=8,'ANALYSIS_REGIONS')
        for region in row['regions']:
            require(isinstance(region,list) and len(region)==4 and all(type(v) is int for v in region),'ANALYSIS_REGION')
            x0,y0,x1,y1=region
            require(0<=x0<x1<=row['width'] and 0<=y0<y1<=row['height'] and x1-x0>=32 and y1-y0>=32,'ANALYSIS_REGION')
        roles.add(row['role']);source=local_file(row['path'],allowed_roots)
        require(fingerprint(source)==row['sha256'],'ANALYSIS_SOURCE_CHANGED')
        geometry,_,_=_image(source,row['imageIndex'])
        require(all(geometry[k]==row[k] for k in ('width','height','channels')),'ANALYSIS_SOURCE_GEOMETRY')
        target=directory/(row['role']+'.xisf');shutil.copyfile(source,target)
        require(fingerprint(target)==row['sha256'] and fingerprint(source)==row['sha256'],'ANALYSIS_COPY_CHANGED')
        rows.append({**{k:copy.deepcopy(v) for k,v in row.items() if k!='path'},
                     'source':source.as_posix(),'copy':target.as_posix()})
    measurement=directory/'measurements.jsh';entry=directory/'analysis.jsh'
    shutil.copyfile(library,measurement);shutil.copyfile(Path(__file__).parent/'analysis.jsh',entry)
    manifest={'version':VERSION,'inputs':rows,'measurementLibrary':measurement.as_posix(),
              'measurementSha256':fingerprint(measurement),'starDetectorLibrary':detector.as_posix(),
              'starDetectorSha256':fingerprint(detector),'entrySha256':fingerprint(entry),
              'report':(directory/'report.json').as_posix(),'log':(directory/'native.log').as_posix()}
    with (directory/'manifest.json').open('xb') as stream:stream.write(encode(manifest))
    def literal(path):
        # Paths are strict local configuration, never model output. JSON quoting
        # preserves quotes/backslashes without evaluating shell or JavaScript.
        import json
        return json.dumps(str(path).replace('\\','/'))
    launcher=('#engine v8\n#define __PJSR_USE_STAR_DETECTOR_V2\n#include <pjsr/StarDetector.jsh>\n'
              '#include '+literal(measurement)+'\n#include '+literal(entry)+'\n'
              'var m=JSON.parse(File.readTextFile('+literal(directory/'manifest.json')+'));\n'
              'DSGAnalyzeMasters(m);\n')
    with (directory/'run.js').open('xb') as stream:stream.write(launcher.replace('\n','\r\n').encode())
    return manifest


def verify(directory, *, expected_manifest_sha256, write_receipt=True):
    directory=Path(directory)
    require(digest(expected_manifest_sha256) and fingerprint(directory/'manifest.json')==expected_manifest_sha256,
            'ANALYSIS_MANIFEST_BINDING')
    manifest=decode((directory/'manifest.json').read_bytes())
    require(manifest['version']==VERSION and (directory/'report.json').stat().st_size<=4194304,'ANALYSIS_REPORT_LIMIT')
    report=decode((directory/'report.json').read_bytes())
    require(set(report)=={'version','status','measurements','originalUnchanged','historyUnchanged','scientificAcceptance'} and
            report['version']==VERSION and report['status']=='READ_ONLY_MEASURED' and
            report['originalUnchanged'] is True and report['historyUnchanged'] is True and
            report['scientificAcceptance']=='NOT_ESTABLISHED' and
            len(report['measurements'])==len(manifest['inputs']),'ANALYSIS_RECEIPT')
    require(fingerprint(Path(manifest['measurementLibrary']))==manifest['measurementSha256'] and
            fingerprint(Path(manifest['starDetectorLibrary']))==manifest['starDetectorSha256'] and
            fingerprint(directory/'analysis.jsh')==manifest['entrySha256'],'ANALYSIS_COMPONENT_CHANGED')
    bindings={}
    for row,measured in zip(manifest['inputs'],report['measurements']):
        require(measured['role']==row['role'] and measured['report'].get('regions')==row['regions'] and
                fingerprint(Path(row['source']))==row['sha256'] and
                fingerprint(Path(row['copy']))==row['sha256'],'ANALYSIS_VERIFICATION_SOURCE')
        geometry,_,_=_image(Path(row['copy']),row['imageIndex'])
        require(all(geometry[k]==row[k] for k in ('width','height','channels')),'ANALYSIS_VERIFICATION_GEOMETRY')
        binding={k:row[k] for k in ('imageIndex','width','height','channels')}
        binding.update(sourceSha256=row['sha256'],adapterSha256=manifest['measurementSha256'],
                       starDetectorSha256=manifest['starDetectorSha256'])
        validate(measured['report'],binding);bindings[row['role']]=binding
    receipt={'version':VERSION,'manifestSha256':fingerprint(directory/'manifest.json'),
             'reportSha256':fingerprint(directory/'report.json'),'status':'READ_ONLY_VERIFIED',
             'scientificAcceptance':'NOT_ESTABLISHED'}
    if write_receipt:
        with (directory/'verification.json').open('xb') as stream:stream.write(encode(receipt))
    else:
        require(decode((directory/'verification.json').read_bytes())==receipt,'ANALYSIS_SAVED_RECEIPT_CHANGED')
    return report,bindings,receipt
