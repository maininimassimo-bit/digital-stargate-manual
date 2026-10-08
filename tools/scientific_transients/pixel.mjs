// Coordinate arithmetic only. A declared convention does not attest an API or WCS.
const fields = ['x', 'y', 'width', 'height', 'convention', 'axes'];
const offsets = Object.freeze({ SAMPLE_INDEX_ZERO: 0, NATIVE_GEOMETRIC: 0.5, FITS_ONE_BASED: 1 });
const finite = v => typeof v === 'number' && Number.isFinite(v);
const point = (x, y) => Object.freeze({ x, y });
// Rounding tolerance only; never an astrometric acceptance radius.
const close = (a, b) => Math.abs(a - b) <= 4 * Number.EPSILON * Math.max(1, Math.abs(a), Math.abs(b));

export function inspectPixelPosition(v) {
  if (!v || typeof v !== 'object' || Array.isArray(v)
      || Object.keys(v).length !== fields.length || !fields.every(k => Object.hasOwn(v, k))
      || !['x', 'y'].every(k => v[k] === null || finite(v[k]))
      || !['width', 'height'].every(k => Number.isSafeInteger(v[k]) && v[k] > 0)
      || !(v.convention === null || typeof v.convention === 'string' && Object.hasOwn(offsets, v.convention))
      || !(v.axes === null || v.axes === 'X_RIGHT_Y_DOWN')) throw new Error('INVALID_PIXEL_POSITION');
  const base = { scientificComparison: 'NOT_VALIDATED', classification: 'NOT_EVALUATED',
    conventionAuthority: 'DECLARED_NOT_ATTESTED', astrometryComputed: false, externalRequests: 0 };
  if (v.x === null || v.y === null || v.convention === null || v.axes === null)
    return Object.freeze({ ...base, status: 'INCOMPLETE', sampleIndex: null, nativeGeometric: null,
      fitsOneBased: null, insideImage: null, reason: 'COORDINATE_CONVENTION_OR_AXES_UNKNOWN' });
  const offset = offsets[v.convention];
  const x = v.x - offset, y = v.y - offset;
  // Fail rather than silently lose the half-pixel offset at extreme magnitudes.
  if (![x, y].every(finite) || !close(x + offset, v.x) || !close(y + offset, v.y)
      || x + 0.5 === x || y + 0.5 === y
      || !close(x + 0.5 - x, 0.5) || !close(y + 0.5 - y, 0.5)
      || !close(x + 1 - x, 1) || !close(y + 1 - y, 1)) throw new Error('PIXEL_CONVERSION_PRECISION');
  const native = point(x + 0.5, y + 0.5);
  // Continuous image footprint: geometric [0,width) × [0,height), not a quality criterion.
  const inside = native.x >= 0 && native.x < v.width && native.y >= 0 && native.y < v.height;
  return Object.freeze({ ...base, status: 'CONVENTION_CONVERTED', sampleIndex: point(x, y),
    nativeGeometric: native, fitsOneBased: point(x + 1, y + 1), insideImage: inside,
    reason: 'DECLARED_ORIGIN_TRANSLATION_ONLY_NO_WCS_OR_SCIENTIFIC_ACCEPTANCE' });
}
