import test from 'node:test';
import assert from 'node:assert/strict';
import { inspectPixelPosition as inspect } from './pixel.mjs';
const input = (extra = {}) => ({ x: 64.25, y: 63.75, width: 129, height: 129,
  convention: 'SAMPLE_INDEX_ZERO', axes: 'X_RIGHT_Y_DOWN', ...extra });

test('native geometric and FITS centers from an explicit sample index', () => {
  const v = inspect(input());
  assert.deepEqual(v.sampleIndex, { x: 64.25, y: 63.75 });
  assert.deepEqual(v.nativeGeometric, { x: 64.75, y: 64.25 });
  assert.deepEqual(v.fitsOneBased, { x: 65.25, y: 64.75 });
  assert.equal(v.insideImage, true);
  assert.equal(v.scientificComparison, 'NOT_VALIDATED');
  assert.equal(v.astrometryComputed, false);
});
test('already geometric coordinates receive no second half-pixel offset', () => {
  const v = inspect(input({ x: 64.75, y: 64.25, convention: 'NATIVE_GEOMETRIC' }));
  assert.deepEqual(v.sampleIndex, { x: 64.25, y: 63.75 });
  assert.deepEqual(v.nativeGeometric, { x: 64.75, y: 64.25 });
});
test('FITS one-based conversion and declared-origin round trips', () => {
  for (const [x, y] of [[0, 0], [128, 128], [64.25, 63.75], [63, 64]]) {
    const a = inspect(input({ x, y }));
    const b = inspect(input({ ...a.fitsOneBased, convention: 'FITS_ONE_BASED' }));
    const c = inspect(input({ ...a.nativeGeometric, convention: 'NATIVE_GEOMETRIC' }));
    assert.deepEqual(b.sampleIndex, a.sampleIndex);
    assert.deepEqual(c.sampleIndex, a.sampleIndex);
  }
});
test('continuous footprint includes the first edge, excludes the opposite edge', () => {
  assert.equal(inspect(input({ x: -0.5, y: -0.5 })).insideImage, true);
  const outside = inspect(input({ x: 128.5, y: 64 }));
  assert.equal(outside.insideImage, false);
  assert.equal(outside.sampleIndex.x, 128.5); // no clamping or invented missing source
});
test('fractional centroid in edge pixel remains inside the continuous footprint', () => {
  assert.equal(inspect(input({ x: 128.4 })).insideImage, true);
});
test('ordinary non-binary fractions round trip within numerical precision', () => {
  const a = inspect(input({ x: 0.2, y: 0.3 }));
  const b = inspect(input({ ...a.nativeGeometric, convention: 'NATIVE_GEOMETRIC' }));
  assert.ok(Math.abs(b.sampleIndex.x - 0.2) <= Number.EPSILON);
  assert.ok(Math.abs(b.sampleIndex.y - 0.3) <= Number.EPSILON);
});
test('unknown origin or axes yields no conversion', () => {
  for (const extra of [{ convention: null }, { axes: null }, { x: null }, { y: null }]) {
    const v = inspect(input(extra));
    assert.equal(v.status, 'INCOMPLETE');
    assert.equal(v.nativeGeometric, null);
    assert.equal(v.insideImage, null);
  }
});
test('unsupported axes, origin and nonfinite coordinates rejected', () => {
  for (const extra of [{ axes: 'Y_UP' }, { convention: 'AUTO' }, { convention: ['NATIVE_GEOMETRIC'] },
    { x: NaN }, { y: Infinity }])
    assert.throws(() => inspect(input(extra)), /INVALID_PIXEL_POSITION/);
});
test('invalid geometry and added authority or execution declarations rejected', () => {
  for (const extra of [{ width: 0 }, { height: 1.5 }, { width: Number.MAX_SAFE_INTEGER + 1 },
    { accepted: true }, { execute: true }, { fitted: false }])
    assert.throws(() => inspect(input(extra)), /INVALID_PIXEL_POSITION/);
});
test('floating point cannot silently erase a half pixel', () => {
  assert.throws(() => inspect(input({ x: 2 ** 52 })), /PIXEL_CONVERSION_PRECISION/);
});
test('results and input remain separate; conversion never changes the source', () => {
  const v = input(); const before = { ...v }; const out = inspect(v);
  assert.deepEqual(v, before);
  assert.equal(Object.isFrozen(out), true);
  assert.equal(Object.isFrozen(out.nativeGeometric), true);
  assert.equal(out.classification, 'NOT_EVALUATED');
});
