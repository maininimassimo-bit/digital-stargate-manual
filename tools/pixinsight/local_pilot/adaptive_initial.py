"""Build the first API request from a supervised read-only native receipt.

No native launch, provider call, credential access or inferred attestations.
The configured provenance record and runtime hashes must bind these exact inputs.
"""
import base64
import copy
from pathlib import Path

from .broker import require
from .intake import sha
from .adaptive_catalog import provenance
from .native_analysis import verify, local_file
from .adaptive_native_adapter import read, safe_path, validate_runtime_files, require_installed_dependencies
from .image_analysis import fingerprint
from .image_previews import curve, render
from .source_provenance import _image
from .source_profile import source_profile


def pixels(path, expected_sha, image_index=0):
    import numpy as np
    require(fingerprint(path)==expected_sha,'ADAPTIVE_INITIAL_PIXEL_SOURCE_CHANGED')
    geometry,_,offset=_image(path,image_index)
    samples=np.memmap(path,dtype='<f4',mode='r',offset=offset,
                     shape=(geometry['channels'],geometry['height'],geometry['width']))
    return np.moveaxis(samples,0,2)


def build(intake, settings, worker_id):
    import numpy as np
    directory=Path(settings['analysisDirectory'])
    safe_path(directory,directory.parent)
    report,bindings,receipt=verify(directory,expected_manifest_sha256=settings['analysisManifestSha256'],
                                   write_receipt=False)
    manifest=read(directory/'manifest.json')
    inputs=[{k:r[k] for k in ('role','sha256','imageIndex','width','height','channels')}
            for r in manifest['inputs']]
    profile=source_profile(intake['selection'])
    mode='OSC' if profile['mode']=='OSC_CFA' else profile['mode']
    require(settings['mode']==mode,'ADAPTIVE_INITIAL_MODE_CHANGED')
    upstream=None
    if profile['mode']=='OSC_CFA' or profile['layout']=='PANELS':
        from .preparation_bridge import prepared_inputs
        preparation_root=Path(settings['preparationRoot'])
        safe_path(preparation_root,preparation_root.parent)
        prepared,upstream=prepared_inputs(preparation_root,intake['selection']['requestId'])
        require(intake.get('preparationApproved') is True and intake.get('preparationResult') and
                all(upstream[k]==intake['preparationResult'][k] for k in upstream if k!='requestId'),
                'ADAPTIVE_INITIAL_UPSTREAM_APPROVAL')
        require([{k:r[k] for k in ('role','sha256','imageIndex','width','height')} for r in inputs]==
                [{k:r[k] for k in ('role','sha256','imageIndex','width','height')} for r in prepared],
                'ADAPTIVE_INITIAL_UPSTREAM_OUTPUT_CHANGED')
    else:
        selected_directory=Path(intake['selection']['masterDirectory'])
        selected_directory=safe_path(selected_directory,selected_directory.parent)
        require(all(Path(r['source']).parent==selected_directory for r in manifest['inputs']),
                'ADAPTIVE_INITIAL_INTAKE_DIRECTORY_CHANGED')
    record_path=safe_path(settings['provenanceRecord'],directory.parent)
    require(fingerprint(record_path)==settings['provenanceRecordSha256'],'ADAPTIVE_INITIAL_PROVENANCE_CHANGED')
    record=read(record_path)
    require(set(record)=={'inputs','facts','scope'} and record['inputs']==inputs and
            isinstance(record['scope'],str) and 0<len(record['scope'])<=4096,'ADAPTIVE_INITIAL_PROVENANCE_BINDING')
    facts=provenance(record['facts'])
    require(facts['sourceSha256']==sha(inputs),'ADAPTIVE_INITIAL_FACTS_BINDING')
    # A record cannot contain its own SHA. The external record digest binds its
    # facts after loading; its stored recordSha256 instead identifies underlying evidence.
    facts['recordSha256']=settings['provenanceRecordSha256']
    runtime=copy.deepcopy(settings['runtime'])
    library=Path(__file__).parent
    require(runtime['executorSha256']==sha({'controller':fingerprint(library/'adaptive_executor.jsh'),
                                           'factory':fingerprint(library/'adaptive_native.jsh')}) and
            runtime['measurementSha256']==manifest['measurementSha256'] and
            runtime['starDetectorSha256']==manifest['starDetectorSha256'] and
            all(r['report']['coreVersion']==runtime['coreVersion'] for r in report['measurements']),
            'ADAPTIVE_INITIAL_RUNTIME_CHANGED')
    validate_runtime_files(runtime,settings['runtimeFiles'])
    require_installed_dependencies(settings['runtimeFiles'],settings['pixinsightRoot'])
    median_role='L' if any(r['role']=='L' for r in inputs) else ('Ha' if any(r['role']=='Ha' for r in inputs) else 'RGB')
    reference=next(r for r in manifest['inputs'] if r['role']==median_role)
    path=local_file(reference['source'],settings['allowedMasterRoots'])
    samples=pixels(path,reference['sha256'],reference['imageIndex'])
    display=curve(float(np.median(samples[::max(1,samples.shape[0]//512),::max(1,samples.shape[1]//512)])))
    del samples
    previews=[];assets=[]
    for row in manifest['inputs']:
        path=local_file(row['source'],settings['allowedMasterRoots'])
        data=pixels(path,row['sha256'],row['imageIndex']);raw,png=render(data,display);del data
        require(fingerprint(path)==row['sha256'],'ADAPTIVE_INITIAL_PREVIEW_SOURCE_CHANGED')
        previews.append({'role':row['role'],'sha256':png['sha256'],'displayCurve':display,'region':None})
        assets.append(base64.b64encode(raw).decode())
    value={'workerId':worker_id,'inputs':inputs,'runtime':runtime,'bindings':bindings,
            'evidence':{'mode':settings['mode'],'intent':intake['selection']['prompt'],
                        'provenance':facts,'measurements':report['measurements'],'previews':previews},
            'assetsBase64':assets}
    if upstream:value['preparationTrace']=upstream
    return value
