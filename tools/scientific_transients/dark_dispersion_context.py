"""Recheck referenced local dark-dispersion evidence for a passive portal receipt.

Unfiltered sample dispersion is not uncertainty of the rejected master. No
LIGHT association, execution, authentication, qualification or full variance.
"""
import math
from pathlib import Path
from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.local_registry import safe_path, fingerprint
from tools.scientific_transients.queue import digest

SCHEMA = 'BKL051_DARK_DISPERSION_CONTEXT_V1'
SCOPE = 'REFERENCED_LOCAL_DARK_DISPERSION_ONLY_NOT_MASTER_VARIANCE'
KINDS = ('unfiltered-sample-mean', 'unfiltered-sample-variance',
         'iid-conditional-unfiltered-mean-variance')
NATIVE_SCOPE = 'LOCAL_READ_ONLY_50DARK_DESCRIPTIVE_DISPERSION_NOT_ACTUAL_REJECTED_MASTER_VARIANCE'


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def integer(value, expected):
    return type(value) is int and value == expected


def inspect_context(directory, receipt_sha, proof_sha, inventory_path):
    root = safe_path(directory)
    require(digest(receipt_sha) and digest(proof_sha), 'DARK_CONTEXT_PIN')
    receipt, actual = read_json(root/'receipt.json')
    require(actual == receipt_sha and receipt['state'] == 'COMPLETED_DESCRIPTIVE_DARK_DISPERSION'
            and receipt['inputHashesUnchanged'] is True and receipt['scope'] == NATIVE_SCOPE
            and receipt['scienceValidation'] == 'NOT_VALIDATED' and type(receipt['qualifiedControls']) is int
            and receipt['qualifiedControls'] == 0 and integer(receipt['cloudRequests'],0), 'DARK_RECEIPT_SCOPE')
    # Mutable continuity notes in the directory are not scientific dependencies.
    # This export never claims verification of every historical directory entry.
    def retained(name):
        require(type(name) is str and Path(name).name == name, 'DARK_LOCAL_NAME')
        value, sha = read_json(root/name)
        require(sha == receipt['retainedFiles'][name], 'DARK_RETAINED_CHANGED')
        return value
    manifest = retained('manifest.json')
    seal = retained('Sigillo-preavvio.json')
    for name, expected in seal['files'].items():
        require(type(name) is str and Path(name).name == name and digest(expected)
                and fingerprint(root/name)['sha256'] == expected, 'DARK_SEALED_SOURCE_CHANGED')
    terminal = retained('terminal.json')
    require(retained('native-terminal-retained.json') == terminal
            and retained('terminal-ready.json')['terminalSha256'] == receipt['retainedFiles']['terminal.json'],
            'DARK_NATIVE_TERMINAL_BINDING')
    created, closed = retained('process-created.json'), retained('owned-process-closed.json')
    require(type(created['pid']) is int and created['pid'] > 0 and closed['pid'] == created['pid']
            and type(closed['exitCode']) is int and closed['onlyAfterValidRetainedTerminalHistoryAndProducts'] is True,
            'DARK_OWNED_CLOSURE')
    launch = retained('launch-intent.json')
    require(integer(launch['maxStarts'],1) and launch['scope'] == NATIVE_SCOPE
            and launch['sealSha256'] == receipt['retainedFiles']['Sigillo-preavvio.json'], 'DARK_LAUNCH_BINDING')
    require(manifest['scope'] == NATIVE_SCOPE and len(manifest['sources']) == 50
            and terminal['state'] == receipt['state'] and integer(terminal['count'],50)
            and integer(terminal['pixels'],5944320) and terminal['version'] == manifest['expectedVersion']
            and terminal['inputFilesUnchanged'] is True and terminal['inputsModified'] is False
            and terminal['unit'] == 'PIXINSIGHT_NATIVE_NORMALIZED_SAMPLE_SQUARED_FOR_VARIANCE'
            and integer(terminal['unclosedOwnedViews'],0) and terminal['masterReproductionPerformed'] is False
            and terminal['actualRejectedMasterVariance'] is None and terminal['fullVariance'] is None
            and terminal['significance'] is None and terminal['iidAssumptionAttested'] is False
            and terminal['temporal2024to2026Stability'] == 'UNKNOWN'
            and terminal['scienceValidation'] == 'NOT_VALIDATED' and integer(terminal['qualifiedControls'],0),
            'DARK_TERMINAL_SCOPE')
    inventory, inventory_sha = read_json(safe_path(inventory_path))
    require(inventory_sha == manifest['inventorySha256'] and integer(inventory['sourceCount'],50)
            and integer(inventory['distinctCurrentSourceHashes'],50), 'DARK_INVENTORY_PIN')
    inventory_rows = {str(safe_path(r['path'])):r for r in inventory['sources']}
    histories = retained('input-history.json')
    require(len(histories) == 50 and len(inventory_rows) == 50
            and len({r['path'] for r in manifest['sources']}) == 50
            and len({r['sha256'] for r in manifest['sources']}) == 50, 'DARK_SOURCE_COUNT')
    for source, history in zip(manifest['sources'], histories):
        path = safe_path(source['path']); row = inventory_rows.get(str(path)); h = row['header'] if row else {}
        require(row is not None and row['sha256'] == source['sha256']
                and fingerprint(path)['sha256'] == source['sha256']
                and history['path'] == source['path'] and history['sha256'] == source['sha256']
                and type(history['history']) is dict and set(history['history']) == {'initial','current','historyIndex'}
                and all(type(history['history'][k]) is str for k in ('initial','current'))
                and h['DATE-OBS'].startswith('2024-') and float(h['EXPTIME']) == 600
                and h['NAXIS1'] == '2752' and h['NAXIS2'] == '2160'
                and h['XBINNING'] == h['YBINNING'] == '1' and h['IMAGETYP'] == 'DARK', 'DARK_SOURCE_BINDING')
    proof, actual = read_json(root/'Verifica-pixel-indipendente.json')
    require(actual == proof_sha and proof['schema'] == 'BKL051_INDEPENDENT_FULL_DARK_PIXEL_RECOMPUTATION_V1'
            and integer(proof['sources'],50) and integer(proof['sourcePixels'],297216000)
            and proof['toleranceAbsoluteNativeSampleUnits'] == 1e-15
            and proof['fullVariance'] is None and proof['actualRejectedMasterVariance'] is None
            and proof['iidAttested'] is False and proof['temporal2024to2026Stability'] == 'UNKNOWN'
            and proof['scienceValidation'] == 'NOT_VALIDATED' and integer(proof['qualifiedControls'],0),
            'DARK_PIXEL_PROOF_SCOPE')
    products = terminal['products']; checks = proof['nativeMapsRechecked']
    require(len(products) == len(checks) == 3 and [r['name'] for r in products] == list(KINDS)
            and {r['name'] for r in checks} == set(KINDS) and receipt['products'] == products
            and len({r['sha256'] for r in products}) == 3, 'DARK_MAP_SET')
    maps = []
    for product in products:
        name = product['name']; check = next(r for r in checks if r['name'] == name)
        path = safe_path(product['path'])
        require(path == root/(name+'.xisf') and digest(product['sha256'])
                and fingerprint(path)['sha256'] == product['sha256'] == check['sha256']
                == receipt['retainedFiles'][name+'.xisf']
                and finite(product['maxSaveReopenError']) and product['maxSaveReopenError'] == 0
                and integer(check['pixelsRechecked'],5944320)
                and finite(check['maxAbsoluteError']) and 0 <= check['maxAbsoluteError'] <= 1e-15
                and all(finite(product[k]) and product[k] >= 0 for k in ('minimum','maximum','mean'))
                and product['minimum'] <= product['mean'] <= product['maximum'], 'DARK_MAP_CHANGED')
        # Native summaries use a linear sum of 5,944,320 nonnegative pixels;
        # independent NumPy summation need not round to the same scalar mean.
        # Compare means within two gamma_n forward-error bounds (u=2^-53),
        # while requiring exact extrema and the separate full-pixel QA bound.
        gamma = 5944320 * 2**-53 / (1 - 5944320 * 2**-53)
        require(finite(check['pixelMinimum']) and finite(check['pixelMaximum']) and finite(check['pixelMean'])
                and check['pixelMean'] >= 0
                and product['minimum'] == check['pixelMinimum'] and product['maximum'] == check['pixelMaximum']
                and math.isclose(product['mean'],check['pixelMean'],rel_tol=2*gamma,abs_tol=1e-18),
                'DARK_MAP_PROOF_SUMMARY')
        retained(name+'-history.json')
        maps.append({'kind':name, 'sha256':product['sha256'], 'minimum':product['minimum'],
                     'maximum':product['maximum'], 'mean':product['mean'], 'pixels':5944320,
                     'unit':'NATIVE_NORMALIZED_SAMPLE' if name == KINDS[0] else 'NATIVE_NORMALIZED_SAMPLE_SQUARED',
                     'nativeReopenError':0, 'independentPixelError':check['maxAbsoluteError']})
    # Recheck the three scalar summaries of the conditional division; no IID claim.
    require(all(math.isclose(maps[1][k]/50, maps[2][k], rel_tol=1e-12, abs_tol=0)
                for k in ('minimum','maximum','mean')), 'DARK_CONDITIONAL_ARITHMETIC')
    return {'schema':SCHEMA, 'scope':SCOPE, 'nativeReceiptSha256':receipt_sha,
            'pixelProofSha256':proof_sha, 'sourceInventorySha256':inventory_sha,
            'sources':50, 'exposureSeconds':600, 'sourceYear':2024, 'geometry':[2752,2160,1],
            'maps':maps, 'actualRejectedMasterVariance':None, 'iidAttested':False,
            'temporal2024to2026Stability':'UNKNOWN', 'lightAssociationAttested':False,
            'completeUncertainty':None, 'significance':None, 'qualifiedControls':0,
            'executionAuthorized':False, 'scienceValidation':'NOT_VALIDATED'}


def main():
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('directory','receipt-sha','proof-sha','inventory-path','output'):p.add_argument('--'+name,required=True)
    a = p.parse_args()
    print(write_new(Path(a.output),inspect_context(a.directory,a.receipt_sha,a.proof_sha,a.inventory_path)))


if __name__ == '__main__':main()
