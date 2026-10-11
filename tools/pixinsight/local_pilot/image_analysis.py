"""Read-only pixel diagnostics candidate; no scientific quality score or dispatch.

Supports uncompressed planar Float32 XISF; multi-image masters require an
explicit index selected by the local worker. Compressed masters require export;
they are never silently approximated or interpreted as this supported layout.
"""
from array import array
import argparse
import hashlib
import math
import re
from pathlib import Path
import struct
import sys
import xml.etree.ElementTree as ET

from tools.pixinsight.local_pilot.worker import require, xisf_header

METHOD = 'DSG_PIAI_PIXEL_DIAGNOSTICS_V1'
LIMITATIONS = ['Whole-field variance/MAD are not background noise or SNR.',
              'Exact zero/one counts are not detector saturation evidence.',
              'Sampled quantiles do not describe every pixel or prove absence of artifacts.']


def fingerprint(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def quantile(values, fraction):
    index = fraction * (len(values) - 1)
    left, right = math.floor(index), math.ceil(index)
    return values[left] + (values[right] - values[left]) * (index - left)


def selected_header(path, image_index):
    """Explicit master index; auxiliary images are never selected implicitly."""
    with path.open('rb') as stream:
        require(stream.read(8) == b'XISF0100', 'ANALYSIS_SIGNATURE')
        size = stream.read(8)
        require(len(size) == 8, 'ANALYSIS_HEADER_INVALID')
        length, reserved = struct.unpack('<II', size)
        require(0 < length <= 1024 * 1024 and reserved == 0, 'ANALYSIS_HEADER_LIMIT')
        raw = stream.read(length)
    require(len(raw) == length and b'<!DOCTYPE' not in raw and b'<!ENTITY' not in raw, 'ANALYSIS_HEADER_INVALID')
    images = [e for e in ET.fromstring(raw) if e.tag.split('}')[-1] == 'Image']
    require(1 <= len(images) <= 16 and type(image_index) is int and 0 <= image_index < len(images), 'ANALYSIS_IMAGE_INDEX')
    image = images[image_index]
    require(image.get('id') not in {'rejection_low', 'rejection_high', 'slope_map', 'weight_map'}, 'ANALYSIS_AUXILIARY_IMAGE')
    geometry = image.get('geometry', '').split(':')
    require(len(geometry) == 3 and all(re.fullmatch(r'[0-9]+', v) for v in geometry), 'ANALYSIS_GEOMETRY')
    return dict(zip(('width', 'height', 'channels'), map(int, geometry)),
                sampleFormat=image.get('sampleFormat'), colorSpace=image.get('colorSpace'))


def analyze(path: Path, *, expected_sha256: str, image_index=None):
    """Diagnostics, not SNR/PSF, linearity, photometry or scientific acceptance.

    Entire attachment checked for finite samples; no [0,1] restriction on
    input/intermediate pixels. Exact moments/clipping and explicitly sampled
    quantiles are different fields. Source is hashed before and after reading.
    """
    require(isinstance(expected_sha256, str) and len(expected_sha256) == 64 and
            all(c in '0123456789abcdef' for c in expected_sha256), 'ANALYSIS_DIGEST')
    require(fingerprint(path) == expected_sha256, 'ANALYSIS_INPUT_CHANGED')
    header = xisf_header(path) if image_index is None else selected_header(path, image_index)
    width, height, channels = (header[k] for k in ('width', 'height', 'channels'))
    require(0 < width <= 12000 and 0 < height <= 12000 and channels in (1, 3) and
            header['sampleFormat'] == 'Float32' and
            header['colorSpace'] == ('Gray' if channels == 1 else 'RGB'), 'ANALYSIS_FORMAT')
    nx, ny = min(64, width), min(64, height)
    xs = [((2 * x + 1) * width) // (2 * nx) for x in range(nx)]
    ys = [((2 * y + 1) * height) // (2 * ny) for y in range(ny)]
    indices = [y * width + x for y in ys for x in xs]
    results = []
    with path.open('rb') as stream:
        stream.seek(8)
        length = struct.unpack('<I', stream.read(4))[0]
        require(0 < length <= 1024 * 1024, 'ANALYSIS_HEADER_LIMIT')
        stream.read(4)
        raw_header = stream.read(length)
        require(len(raw_header) == length and b'<!DOCTYPE' not in raw_header and
                b'<!ENTITY' not in raw_header, 'ANALYSIS_HEADER_INVALID')
        images = [e for e in ET.fromstring(raw_header) if e.tag.split('}')[-1] == 'Image']
        image = images[0 if image_index is None else image_index]
        require(not image.get('compression') and image.get('pixelStorage', 'planar') == 'planar' and
                image.get('byteOrder', 'little') == 'little', 'ANALYSIS_NATIVE_EXPORT_REQUIRED')
        location = image.get('location', '').split(':')
        require(len(location) == 3 and location[0] == 'attachment', 'ANALYSIS_ATTACHMENT')
        offset, size = int(location[1]), int(location[2])
        require(size == width * height * channels * 4 and offset >= 16 + length and
                offset + size <= path.stat().st_size, 'ANALYSIS_ATTACHMENT_BOUNDS')
        stream.seek(offset)
        for channel in range(channels):
            count, mean, m2, low, high = 0, 0.0, 0.0, math.inf, -math.inf
            zero, one, below, above = 0, 0, 0, 0
            samples, cursor = [], 0
            while count < width * height:
                n = min(65536, width * height - count)
                raw = stream.read(n * 4)
                require(len(raw) == n * 4, 'ANALYSIS_TRUNCATED')
                values = array('f'); values.frombytes(raw)
                if sys.byteorder != 'little': values.byteswap()
                require(all(math.isfinite(v) for v in values), 'ANALYSIS_NONFINITE')
                block_mean = math.fsum(values) / n
                block_m2 = math.fsum((v - block_mean) ** 2 for v in values)
                delta = block_mean - mean
                m2 += block_m2 + delta * delta * count * n / (count + n)
                mean += delta * n / (count + n)
                low, high = min(low, min(values)), max(high, max(values))
                zero += values.count(0); one += values.count(1)
                below += sum(v < 0 for v in values); above += sum(v > 1 for v in values)
                while cursor < len(indices) and indices[cursor] < count + n:
                    samples.append(float(values[indices[cursor] - count])); cursor += 1
                count += n
            sorted_samples = sorted(samples)
            median = quantile(sorted_samples, .5)
            mad = quantile(sorted(abs(v - median) for v in samples), .5)
            results.append({'channelIndex': channel, 'sampleCount': count, 'minimum': low,
                'maximum': high, 'mean': mean, 'populationVariance': m2 / count,
                'zeroSamples': zero, 'oneSamples': one, 'belowZeroSamples': below,
                'aboveOneSamples': above, 'constant': high == low,
                'sampledDistribution': {'gridWidth': nx, 'gridHeight': ny, 'count': len(samples),
                    'method': 'UNIFORM_CELL_CENTERS_NO_INTERPOLATION',
                    'median': median, 'mad': mad,
                    'quantiles': [quantile(sorted_samples, q) for q in (.01, .1, .5, .9, .99)]}})
    require(fingerprint(path) == expected_sha256, 'ANALYSIS_INPUT_CHANGED')
    return {**({'imageIndex': image_index} if image_index is not None else {}),
        'method': METHOD, 'sourceSha256': expected_sha256, 'width': width,
        'height': height, 'channels': results, 'allFinite': True,
        'linearity': 'NOT_ESTABLISHED', 'calibration': 'NOT_ESTABLISHED',
        'psf': {'status': 'UNAVAILABLE', 'reason': 'NATIVE_FIT_REQUIRED'},
        'backgroundNoise': {'status': 'UNAVAILABLE', 'reason': 'VALIDATED_BACKGROUND_MASK_REQUIRED'},
        'acceptance': 'DIAGNOSTIC_ONLY',
        'limitations': list(LIMITATIONS)}


def compare(before, after):
    """Numerical diagnostic deltas only; does not certify grid/domain equivalence.

    Geometry equality cannot prove registration or equal transformations.
    Scientific comparison remains unavailable until those prerequisites are
    supplied by the segment protocol; no implicit quality score is returned.
    """
    require(before['method'] == after['method'] == METHOD and
            before['width'] == after['width'] and before['height'] == after['height'] and
            len(before['channels']) == len(after['channels']), 'ANALYSIS_COMPARISON_GEOMETRY')
    rows = []
    for first, second in zip(before['channels'], after['channels']):
        require(first['channelIndex'] == second['channelIndex'] and
                first['sampleCount'] == second['sampleCount'], 'ANALYSIS_COMPARISON_CHANNEL')
        rows.append({'channelIndex': first['channelIndex'],
            'meanDelta': second['mean'] - first['mean'],
            'populationVarianceDelta': second['populationVariance'] - first['populationVariance'],
            'zeroSamplesDelta': second['zeroSamples'] - first['zeroSamples'],
            'oneSamplesDelta': second['oneSamples'] - first['oneSamples'],
            'belowZeroSamplesDelta': second['belowZeroSamples'] - first['belowZeroSamples'],
            'aboveOneSamplesDelta': second['aboveOneSamples'] - first['aboveOneSamples']})
    return {'method': METHOD, 'beforeImageIndex': before.get('imageIndex'),
        'afterImageIndex': after.get('imageIndex'), 'beforeSha256': before['sourceSha256'],
        'afterSha256': after['sourceSha256'], 'channels': rows,
        'scientificComparison': 'NOT_ESTABLISHED',
        'limitations': ['Equal geometry does not prove registration or equal image domain.',
            'Diagnostic deltas are not improvement scores or permission to continue processing.']}


def main():
    """Explicit read-only local file; write a new private diagnostic artifact."""
    from .broker import encode
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--image-index', type=int)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        require(not args.output.exists(), 'ANALYSIS_OUTPUT_EXISTS')
        value = analyze(args.input, expected_sha256=args.sha256, image_index=args.image_index)
        with args.output.open('xb') as stream:
            stream.write(encode(value))
        print('Diagnostica locale conservata; nessuna accettazione scientifica.')
    except Exception:
        parser.exit(1, 'Analisi non completata. Conservare il tentativo e verificare input/export nativo.\n')


if __name__ == '__main__':
    main()
