"""Expose retained M27 nominal noise evidence alongside verified input lineage.

No pixel processing, full uncertainty, calibration attestation or launch.
Filter-level map association does not prove application to a particular LIGHT.
"""
import math
from pathlib import Path
from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.local_registry import safe_path, fingerprint
from tools.scientific_transients.input_lineage import inspect_lineage
from tools.scientific_transients.queue import fields, digest

COMPONENTS = (
    ('LIGHT_PHOTON_READ_DIGITIZATION', 'L photon/read/digitization variance', 'PARTIAL'),
    ('DARK_FINITE_SAMPLE', 'D 2024 master finite-sample uncertainty', 'UNKNOWN'),
    ('DARK_TEMPORAL_2024_2026', 'D temporal systematic, 2024 to 2026', 'UNKNOWN'),
    ('FLAT_REPEATABILITY', 'F conditional repeatability', 'CONDITIONAL'),
    ('FLAT_SHARED_SPATIAL', 'F shared dark-flat, temperature, normalization and spatial covariance', 'PARTIAL'),
    ('NORMALIZATION_COVARIANCE', 's=median(F) uncertainty and Cov(F,s)', 'UNKNOWN'),
    ('CROSS_PIXEL_EPOCH_COVARIANCE', 'Cross-pixel and cross-exposure covariance', 'UNKNOWN'),
    ('FLUX_BACKGROUND_PSF_WCS', 'flux estimator/background/PSF/WCS uncertainty', 'UNKNOWN'))
SOURCE_STATES = ('NOMINAL_READ_NOISE_AND_GAIN_AVAILABLE; PHOTON_RATE_PARAMETER_UNCERTAINTY_AND_CONVENTION_INCOMPLETE',
    'NOT_YET_QUANTIFIED','UNKNOWN','EMPIRICAL_MAPS_AVAILABLE_CONDITIONAL','INCOMPLETE',
    'UNKNOWN_DEPENDENT_ESTIMATOR','UNKNOWN','NOT_ESTABLISHED')


def pinned_json(path, sha):
    require(digest(sha), 'CALIBRATION_PIN')
    value, actual = read_json(safe_path(path))
    require(actual == sha, 'CALIBRATION_SOURCE_CHANGED')
    return value


def inspect_context(lineage_directory, lineage_receipt_sha, draft_path, draft_sha,
                    budget_path, budget_sha, camera_path, camera_sha, maps_directory, maps_receipt_sha):
    lineage = inspect_lineage(lineage_directory, lineage_receipt_sha, draft_path, draft_sha)
    budget = pinned_json(budget_path, budget_sha)
    camera = pinned_json(camera_path, camera_sha)
    require(budget['scope'] == 'PREPARATION_AND_CONDITIONAL_COMPONENTS_ONLY'
        and budget['scienceValidation'] == 'NOT_VALIDATED' and budget['sigmaComplete'] is None
        and budget['significance'] is None and budget['missingCovariancesAreZero'] is False,
        'CALIBRATION_BUDGET_SCOPE')
    gain, noise = budget['physicalGainElectronsPerADU'], budget['readNoiseElectrons']
    require(camera['cells'] == 'M5:N5' and gain['sourceCell'] == 'M5' and noise['sourceCell'] == 'N5'
        and gain['nominal'] == camera['gainElectronsPerADUNominal']
        and noise['nominal'] == camera['readNoiseElectronsNominal']
        and gain['standardUncertainty'] is None and noise['standardUncertainty'] is None
        and camera['parameterStandardUncertainties'] is None
        and budget['activeCharacterization'] == camera, 'CALIBRATION_ACTIVE_PARAMETERS')
    require(all(type(n) in {int,float} and math.isfinite(n) and n > 0
        for n in (gain['nominal'],noise['nominal'])), 'CALIBRATION_NUMERIC_PARAMETERS')
    adu = noise['nominal'] / gain['nominal']
    require(math.isclose(budget['readNoiseADUConditional'], adu, rel_tol=1e-12)
        and math.isclose(budget['readNoiseVarianceNativeNormalizedConditional'], (adu / 65535)**2,
                         rel_tol=1e-12), 'CALIBRATION_CONDITIONAL_ARITHMETIC')
    terms = [r['term'] for r in budget['components']]
    require(len(terms) == len(COMPONENTS) and set(terms) == {r[1] for r in COMPONENTS},
            'CALIBRATION_COMPONENTS_INCOMPLETE')
    require(all(next(r['status'] for r in budget['components'] if r['term'] == component[1]) == state
                for component,state in zip(COMPONENTS,SOURCE_STATES)), 'CALIBRATION_COMPONENT_STATE')
    directory = safe_path(maps_directory)
    receipt = pinned_json(directory/'receipt.json', maps_receipt_sha)
    require(receipt['parentHashesUnchanged'] is True, 'CALIBRATION_MAP_PARENTS')
    terminal = pinned_json(directory/'terminal.json', receipt['products']['terminal.json'])
    require(terminal == receipt['terminal']
        and terminal['status'] == 'COMPLETED_NOMINAL_READ_VARIANCE_COMPONENTS'
        and terminal['scienceValidation'] == 'NOT_VALIDATED', 'CALIBRATION_MAP_SCOPE')
    # Recheck the stored source and parent hashes, not only the exported map.
    manifest = pinned_json(directory/'manifest.json', receipt['products']['manifest.json'])
    require(manifest['parameters'] == camera
        and fingerprint(directory/'entry.js')['sha256'] == receipt['products']['entry.js']
        == manifest['entrySHA256'],
            'CALIBRATION_SCRIPT_CHANGED')
    require(type(manifest['inputs']) is list and 1 <= len(manifest['inputs']) <= 4,
            'CALIBRATION_MAP_INPUTS')
    for parent in manifest['inputs']:
        require(Path(parent['path']).is_absolute()
            and fingerprint(parent['path'])['sha256'] == parent['sha256'], 'CALIBRATION_PARENT_CHANGED')
    maps = {}
    for row in terminal['rows']:
        fields(row, {'filter','path','flatMedianScale','min','max','mean','pixels',
                     'maxAbsoluteSaveReopenError','completeNoiseMap'})
        require(row['filter'] in {'L-Pro','Red','Green','Blu'} and row['filter'] not in maps
            and row['completeNoiseMap'] is False
            and type(row['maxAbsoluteSaveReopenError']) in {int,float} and row['maxAbsoluteSaveReopenError'] == 0
            and type(row['pixels']) is int and row['pixels'] > 0
            and all(type(row[k]) in {int,float} and math.isfinite(row[k]) and row[k] > 0
                    for k in ('flatMedianScale','min','max','mean'))
            and row['min'] <= row['mean'] <= row['max'], 'CALIBRATION_MAP_ROW')
        require(type(row['path']) is str and Path(row['path']).is_absolute(), 'CALIBRATION_MAP_PATH')
        path = safe_path(row['path']); require(path.parent == directory, 'CALIBRATION_MAP_PATH')
        sha = receipt['products'][path.name]
        require(fingerprint(path)['sha256'] == sha, 'CALIBRATION_MAP_CHANGED')
        maps[row['filter']] = {'filter':row['filter'], 'mapSha256':sha,
            'varianceMinimum':row['min'], 'varianceMaximum':row['max'],
            'varianceMean':row['mean'], 'pixels':row['pixels'],
            'unit':'NATIVE_NORMALIZED_SQUARED', 'scope':'NOMINAL_READ_COMPONENT_ONLY',
            'pixelCheck':'RETAINED_NATIVE_SAVE_REOPEN_REPORT_NOT_REMEASURED'}
    require(maps and all(r['filter'] in maps for r in lineage['inputs']), 'CALIBRATION_MAP_FILTER_MISSING')
    return {'schema':'BKL051_CALIBRATION_CONTEXT_V1', 'scienceValidation':'NOT_VALIDATED',
        'lineageReceiptSha256':lineage_receipt_sha, 'candidateDraftSha256':draft_sha,
        'candidatePlanRef':lineage['candidatePlanRef'], 'budgetSha256':budget_sha,
        'cameraChoiceSha256':camera_sha, 'mapsReceiptSha256':maps_receipt_sha,
        'camera':{'sourceCells':'M5:N5', 'gainElectronsPerADU':gain['nominal'],
            'readNoiseElectrons':noise['nominal'], 'parameterStandardUncertainties':None,
            'readNoiseADUConditional':adu, 'ADUConvention':'65535_LEVELS_CONDITIONAL_NOT_ATTESTED'},
        'components':[{'component':key,'status':status} for key,_,status in COMPONENTS],
        'maps':list(maps.values()),
        'inputs':[{'inputRef':r['inputRef'],'rawSha256':r['rawSha256'],
            'derivedSha256':r['derivedSha256'],'filter':r['filter'],
            'mapSha256':maps[r['filter']]['mapSha256'],
            'association':'FILTER_ONLY_APPLICATION_NOT_ATTESTED'} for r in lineage['inputs']],
        'darkTemporalLimitation':'2024_DARK_FOR_2026_LIGHT_STABILITY_UNKNOWN',
        'byteIntegrity':'RECHECKED_LOCAL_FILES', 'completeUncertainty':None,
        'significance':None, 'qualifiedControls':0, 'executionAuthorized':False}


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('lineage-directory','lineage-receipt-sha','draft-path','draft-sha',
                 'budget-path','budget-sha','camera-path','camera-sha','maps-directory','maps-receipt-sha','output'):
        p.add_argument('--'+name,required=True)
    a=vars(p.parse_args());output=a.pop('output')
    print(write_new(Path(output),inspect_context(**a)))


if __name__=='__main__':main()
