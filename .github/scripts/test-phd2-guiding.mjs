import test from 'node:test';
import assert from 'node:assert/strict';
import { parseCsvRecord, parseGuideLog } from './phd2-guiding.mjs';

test('parseCsvRecord preserves all PHD2 positional columns', () => {
  const row = parseCsvRecord('7,13.949,"Mount",-0.482,0.261,0.547,-0.029,0.371,0.000,84,W,0,,,,667283,454.53,0');
  assert.equal(row.length, 18);
  assert.equal(row[1], '13.949');
  assert.equal(row[7], '0.371');
  assert.equal(row[8], '0.000');
  assert.equal(row[17], '0');
});

test('parseGuideLog excludes settling and ErrorCode samples and preserves segments', () => {
  const log = [
    'Guiding Begins at 2026-08-10 22:18:22',
    'Frame,Time,mount,dx,dy,RARawDistance,DECRawDistance,RAGuideDistance,DECGuideDistance,RADuration,RADirection,DECDuration,DECDirection,XStep,YStep,StarMass,SNR,ErrorCode',
    'INFO: SETTLING STATE CHANGE, Settling started',
    '1,2.137,"Mount",-0.009,0.200,0.093,-0.177,0.500,0.500,0,,0,,,,647845,451.47,0',
    'INFO: SETTLING STATE CHANGE, Settling complete',
    '7,13.949,"Mount",-0.482,0.261,0.547,-0.029,0.371,0.000,84,W,0,,,,667283,454.53,0',
    '8,15.921,"Mount",-0.158,-0.012,0.138,0.078,0.113,0.200,26,W,0,,,,670723,454.00,0',
    '9,17.933,"Mount",0.217,-0.024,-0.207,-0.072,-0.900,0.900,28,E,0,,,,642406,475.90,2',
    'Guiding Begins at 2026-08-10 23:00:00',
    '10,19.829,"Mount",-0.183,0.012,0.170,0.067,0.099,-0.100,22,W,0,,,,641874,433.69,0'
  ].join('\n');

  const result = parseGuideLog(log, 'data\\session\\raw\\phd2\\guide.txt');
  assert.ok(result);
  assert.equal(result.sampleCount, 3);
  assert.equal(result.segmentCount, 2);
  assert.equal(result.samples.length, 3);
  assert.deepEqual(result.samples.map((sample) => sample.segment), [1, 1, 2]);
  assert.equal(result.samples[0].elapsedSeconds, 13.949);
  assert.equal(result.samples[0].raArcsec, 0.371);
  assert.equal(result.samples[1].decArcsec, 0.2);
  assert.equal(result.sourcePath, 'data/session/raw/phd2/guide.txt');
  assert.ok(result.rmsRaArcsec > 0);
  assert.ok(result.rmsDecArcsec > 0);
  assert.ok(result.rmsTotalArcsec > 0);
});
