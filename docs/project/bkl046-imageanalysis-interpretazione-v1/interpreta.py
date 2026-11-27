
"""Interpret both BKL-046 ImageAnalysis control orders without accepting a run."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re

IDS = ('compact-shuffled', 'compact-zones', 'tailed-shuffled', 'compact-wide-psf')
METRICS = ('fwhmPx', 'eccentricity', 'noise', 'stars', 'psfSignalWeight',
           'psfSnr', 'snr', 'median', 'measurementSigma', 'mStar')
CHECKS = (
    ('spatialSigma', IDS[1], 'measurementSigma'),
    ('spatialNoise', IDS[1], 'noise'),
    ('heavyTailSigma', IDS[2], 'measurementSigma'),
    ('heavyTailNoise', IDS[2], 'noise'),
    ('widePsfFwhm', IDS[3], 'fwhmPx'),
)

def need(condition, reason):
    if not condition:
        raise ValueError(reason)

def no_duplicate(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'DUPLICATE_JSON_KEY')
        result[key] = value
    return result

def exact(obj, fields):
    return type(obj) is dict and set(obj) == set(fields)

def finite(value):
    return type(value) in (float, int) and -1e300 <= value <= 1e300

def classify(left, right, metric):
    if left == right:
        return 'INDISTINGUISHABLE_AT_FROZEN_TOLERANCE'
    if metric != 'stars' and math.isclose(left, right, rel_tol=1e-9, abs_tol=1e-12):
        return 'INDISTINGUISHABLE_AT_FROZEN_TOLERANCE'
    return 'INCREASED' if right > left else 'DECREASED'

def evaluate(raw, expected_sha256, operation):
    need(type(raw) is bytes and 0 < len(raw) <= 65536 and
         hashlib.sha256(raw).hexdigest() == expected_sha256, 'RESULT_SHA256')
    need(type(operation) is str and re.fullmatch('[0-9a-f]{32}', operation), 'OPERATION')
    value = json.loads(raw, object_pairs_hook=no_duplicate)
    need(exact(value, ('protocol', 'operationRef', 'version', 'cache', 'extendedMeasurements',
                       'forward', 'reverse', 'deltas', 'scientificAcceptance')) and
         value['protocol'] == 'BKL046_IMAGEANALYSIS_CONTROL_RESULT_V1' and
         value['operationRef'] == operation and value['version'] == '1.9.6 build 1719' and
         value['cache'] is False and value['extendedMeasurements'] is False and
         value['scientificAcceptance'] is False, 'RESULT_SCHEMA')
    runs = {}
    for name, input_order in (('forward', IDS), ('reverse', IDS[::-1])):
        run = value[name]
        need(exact(run, ('inputOrder', 'records')) and run['inputOrder'] == list(input_order) and
             type(run['records']) is list and len(run['records']) == len(IDS), 'RESULT_ORDER')
        runs[name] = {}
        for ident, record in zip(IDS, run['records']):
            need(exact(record, ('id', 'values')) and record['id'] == ident and
                 exact(record['values'], METRICS) and
                 all(finite(v) for v in record['values'].values()), 'RESULT_METRICS')
            fields = record['values']
            need(type(fields['stars']) is int and fields['stars'] > 0 and fields['fwhmPx'] > 0 and
                 fields['noise'] >= 0 and fields['measurementSigma'] >= 0, 'DOMAIN')
            runs[name][ident] = fields
    forward, reverse = runs['forward'], runs['reverse']
    drift = {ident: [] for ident in IDS}
    need(type(value['deltas']) is list and len(value['deltas']) == len(IDS), 'DELTA_SCHEMA')
    for ident, row in zip(IDS, value['deltas']):
        need(exact(row, ('id', 'byMetric')) and row['id'] == ident and exact(row['byMetric'], METRICS),
             'DELTA_SCHEMA')
        for metric, delta in row['byMetric'].items():
            a, b = forward[ident][metric], reverse[ident][metric]
            need(finite(delta) and delta == b - a, 'DELTA_MISMATCH')
            if classify(a, b, metric) != 'INDISTINGUISHABLE_AT_FROZEN_TOLERANCE':
                drift[ident].append(metric)
    contrasts = {}
    for name, target, metric in CHECKS:
        left, right = IDS[0], target
        directions = {order: classify(run[left][metric], run[right][metric], metric)
                      for order, run in runs.items()}
        comparables = [metric not in drift[ident] for ident in (left, right)]
        stable = all(comparables) and directions['forward'] == directions['reverse']
        contrasts[name] = {'field': metric, 'target': target, 'directions': directions,
                           'interpretation': directions['forward'] if stable else 'INCONCLUSIVE_ORDER'}
    return {'protocol': 'BKL046_IMAGEANALYSIS_CONTROL_INTERPRETATION_V1',
            'operationRef': operation, 'inputSha256': expected_sha256,
            'numericTolerance': {'relative': 1e-9, 'absoluteNativeUnits': 1e-12, 'starsExact': True},
            'orderDifferencesByFrame': drift, 'contrasts': contrasts,
            'nativeOriginVerifiedByEvaluator': False, 'scientificAcceptance': False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('result', type=Path)
    parser.add_argument('expected_sha256')
    parser.add_argument('operation')
    args = parser.parse_args()
    with args.result.open('rb') as stream:
        raw = stream.read(65537)
    print(json.dumps(evaluate(raw, args.expected_sha256, args.operation), indent=2))

if __name__ == '__main__':
    main()

