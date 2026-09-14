import test from 'node:test';
import assert from 'node:assert/strict';
import { parseCsvRecord, parseGuideLog } from './phd2-guiding.mjs';

const header = 'Frame,Time,mount,dx,dy,RARawDistance,DECRawDistance,RAGuideDistance,DECGuideDistance,RADuration,RADirection,DECDuration,DECDirection,XStep,YStep,StarMass,SNR,ErrorCode';

test('parseCsvRecord preserves all PHD2 positional columns', () => {
  const row = parseCsvRecord('7,13.949,"Mount",-0.482,0.261,0.547,-0.029,0.371,0.000,84,W,0,,,,667283,454.53,0');
  assert.equal(row.length, 18);
  assert.equal(row[1], '13.949');
  assert.equal(row[5], '0.547');
  assert.equal(row[6], '-0.029');
  assert.equal(row[17], '0');
});

test('parseGuideLog converts raw tracking error with the SW4P segment scale', () => {
  const log = [
    'INFO: SETTLING STATE CHANGE, Settling started',
    'Guiding Begins at 2026-08-10 22:18:22',
    'Equipment Profile = SW4P_ToupTek294',
    'Pixel scale = 2.00 arc-sec/px, Binning = 1, Focal length = 400 mm',
    header,
    '1,2.137,"Mount",-0.009,0.200,9,9,99,99,0,,0,,,,647845,451.47,0',
    'INFO: SETTLING STATE CHANGE, Settling complete',
    '7,13.949,"Mount",-0.482,0.261,0.547,-0.029,0.371,0.000,84,W,0,,,,667283,454.53,0',
    '8,15.921,"Mount",-0.158,-0.012,0.138,0.078,0.113,0.200,26,W,0,,,,670723,454.00,0',
    '9,17.933,"DROP",,,,,,,,,,,,,0,0.00,2,"Star lost - low SNR"',
    'Guiding Ends at 2026-08-10 22:30:00'
  ].join('\n');

  const result = parseGuideLog(log, 'data\\session\\raw\\phd2\\guide.txt');
  assert.ok(result);
  assert.equal(result.sampleCount, 2);
  assert.equal(result.sampleCountTotal, 4);
  assert.equal(result.settlingExcludedSampleCount, 1);
  assert.equal(result.rejectedSampleCount, 1);
  assert.equal(result.segmentCount, 1);
  assert.deepEqual(result.equipmentProfiles, ['SW4P_ToupTek294']);
  assert.equal(result.samples[0].raArcsec, 1.094);
  assert.equal(result.samples[0].decArcsec, -0.058);
  assert.equal(result.samples[1].raArcsec, 0.276);
  assert.equal(result.samples[1].decArcsec, 0.156);
  assert.equal(result.sourcePath, 'data/session/raw/phd2/guide.txt');
  assert.ok(result.rmsTotalArcsec > 0);
});

test('parseGuideLog includes C8 saturated samples and closes failed settling', () => {
  const log = [
    'INFO: SETTLING STATE CHANGE, Settling started',
    'Guiding Begins at 2026-09-13 21:04:39',
    'Equipment Profile = C8_QHY695A',
    'Pixel scale = 0.61 arc-sec/px, Binning = 1, Focal length = 1260 mm',
    header,
    '1,3.0,"Mount",0,0,50,50,50,50,0,,0,,,,100,20,1',
    'Guiding Ends at 2026-09-13 21:04:48',
    'INFO: SETTLING STATE CHANGE, Settling failed',
    'Guiding Begins at 2026-09-13 21:04:58',
    'Equipment Profile = C8_QHY695A',
    'Pixel scale = 0.61 arc-sec/px, Binning = 1, Focal length = 1260 mm',
    header,
    '1,3.0,"Mount",0,0,0.5,-0.25,9,9,0,,0,,,,100,20,1',
    '2,6.0,"Mount",0,0,-1,0.75,8,8,0,,0,,,,100,20,0',
    '3,9.0,"DROP",,,,,,,,,,,,,0,0.00,2,"Stella persa per SNR basso"',
    'Guiding Ends at 2026-09-13 21:10:00'
  ].join('\n');

  const result = parseGuideLog(log);
  assert.ok(result);
  assert.equal(result.segmentCount, 2);
  assert.equal(result.sampleCountTotal, 4);
  assert.equal(result.sampleCount, 2);
  assert.equal(result.saturatedSampleCount, 1);
  assert.equal(result.rejectedSampleCount, 1);
  assert.equal(result.settlingExcludedSampleCount, 1);
  assert.equal(result.settlingFailureCount, 1);
  assert.deepEqual(result.equipmentProfiles, ['C8_QHY695A']);
  assert.equal(result.rmsRaArcsec, 0.482);
  assert.equal(result.rmsDecArcsec, 0.341);
  assert.equal(result.rmsTotalArcsec, 0.591);
  assert.equal(result.samples[0].saturated, true);
});
