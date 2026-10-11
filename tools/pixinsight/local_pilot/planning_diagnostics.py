"""Bounded numerical evidence contract; never grants scientific acceptance."""
import math
import re

from .broker import require
from .image_analysis import METHOD, LIMITATIONS
from . import worker

def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate_reports(rows, masters, recipe):
    require(isinstance(rows, list) and len(rows) == len(masters), 'AI_DIAGNOSTICS_ROLES')
    report_fields = {'method', 'sourceSha256', 'imageIndex', 'width', 'height', 'channels', 'allFinite',
                     'linearity', 'calibration', 'psf', 'backgroundNoise', 'acceptance', 'limitations'}
    channel_fields = {'channelIndex', 'sampleCount', 'minimum', 'maximum', 'mean',
                      'populationVariance', 'zeroSamples', 'oneSamples', 'belowZeroSamples',
                      'aboveOneSamples', 'constant', 'sampledDistribution'}
    for row, master in zip(rows, masters):
        require(isinstance(row, dict) and set(row) == {'role', 'report'} and
                row['role'] == master['role'], 'AI_DIAGNOSTICS_ROLES')
        report = row['report']
        require(isinstance(report, dict) and set(report) == report_fields and
                report['method'] == METHOD and isinstance(report['sourceSha256'], str) and
                re.fullmatch(r'[a-f0-9]{64}', report['sourceSha256']) and
                type(report['width']) is int and type(report['height']) is int and
                (report['width'], report['height']) == (master['width'], master['height']) and
                type(report['imageIndex']) is int and report['imageIndex'] == master['imageIndex'] and report['allFinite'] is True and
                report['linearity'] == report['calibration'] == 'NOT_ESTABLISHED' and
                report['psf'] == {'status': 'UNAVAILABLE', 'reason': 'NATIVE_FIT_REQUIRED'} and
                report['backgroundNoise'] == {'status': 'UNAVAILABLE', 'reason': 'VALIDATED_BACKGROUND_MASK_REQUIRED'} and
                report['acceptance'] == 'DIAGNOSTIC_ONLY' and report['limitations'] == LIMITATIONS,
                'AI_DIAGNOSTICS_REPORT')
        expected_channels = 3 if worker.RECIPE_MODES.get(recipe, 'LRGB') == 'OSC' else 1
        channels = report['channels']
        require(isinstance(channels, list) and len(channels) == expected_channels, 'AI_DIAGNOSTICS_CHANNELS')
        count = report['width'] * report['height']
        for index, channel in enumerate(channels):
            require(isinstance(channel, dict) and set(channel) == channel_fields and
                    type(channel['channelIndex']) is int and channel['channelIndex'] == index and
                    type(channel['sampleCount']) is int and channel['sampleCount'] == count,
                    'AI_DIAGNOSTICS_CHANNEL')
            require(all(number(channel[k]) for k in ('minimum', 'maximum', 'mean', 'populationVariance')) and
                    channel['minimum'] <= channel['mean'] <= channel['maximum'] and
                    channel['populationVariance'] >= 0 and
                    type(channel['constant']) is bool and
                    channel['constant'] == (channel['minimum'] == channel['maximum']), 'AI_DIAGNOSTICS_MOMENTS')
            counts = [channel[k] for k in ('zeroSamples', 'oneSamples', 'belowZeroSamples', 'aboveOneSamples')]
            require(all(type(v) is int and 0 <= v <= count for v in counts) and sum(counts) <= count,
                    'AI_DIAGNOSTICS_COUNTS')
            sample = channel['sampledDistribution']
            nx, ny = min(64, report['width']), min(64, report['height'])
            require(isinstance(sample, dict) and set(sample) ==
                    {'gridWidth', 'gridHeight', 'count', 'method', 'median', 'mad', 'quantiles'} and
                    all(type(sample[k]) is int for k in ('gridWidth', 'gridHeight', 'count')) and
                    (sample['gridWidth'], sample['gridHeight'], sample['count']) == (nx, ny, nx * ny) and
                    sample['method'] == 'UNIFORM_CELL_CENTERS_NO_INTERPOLATION' and
                    number(sample['median']) and number(sample['mad']) and sample['mad'] >= 0,
                    'AI_DIAGNOSTICS_SAMPLE')
            q = sample['quantiles']
            require(isinstance(q, list) and len(q) == 5 and all(number(v) for v in q) and
                    channel['minimum'] <= q[0] <= q[1] <= q[2] <= q[3] <= q[4] <= channel['maximum'] and
                    q[2] == sample['median'], 'AI_DIAGNOSTICS_QUANTILES')
