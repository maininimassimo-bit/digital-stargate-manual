'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const vm = require('node:vm');

const [source, destination] = process.argv.slice(2);
const buf = fs.readFileSync(source);
const sourceSha256 = crypto.createHash('sha256').update(buf).digest('hex');
assert.equal(sourceSha256, '1743bfde348ebf65bdb8e55a9537d32f5f645b2b5f2063fb333edae2cf7f0f1f');
const text = buf.toString('utf8');
function section(start, end) {
  const a = text.indexOf(start);
  const b = text.indexOf(end, a + start.length);
  assert(a >= 0 && b > a, 'source section missing');
  return text.slice(a, b);
}

const code = [
  section('function Pair(', 'function uniqueViewIdNoLeadingZero('),
  section('function uniqueArray(', 'function starProfilesOfImageWindow('),
  section('function parametersPrototype(', 'function Pair('),
  'function measure(starProfiles, model) {',
  'const parameters = new parametersPrototype(); parameters.modelFunctionIndex = model;',
  section('   var FWHMs = new Array();', '\n   enable();\n}'),
  'return { fwhm: parameters.medianFWHM, eccentricity: parameters.medianEccentricity, residual: parameters.medianResidual, spreadFwhm: parameters.MADMedianFWHM, support: parameters.starSupport };',
  '}',
].join('\n');

const ctx = vm.createContext({});
vm.runInContext(code, ctx);
function almost(actual, expected) {
  assert(Math.abs(actual - expected) < 1e-10, {actual, expected});
}
const location = ctx.medianMADMedianOfArray([1, 1, 1, 9]);
assert.equal(location.first, 1);
assert.equal(location.last, 2);
const samePixel = [
  {x:10.1,y:20.1},
  {x:10.4,y:20.4},
  {x:10.6,y:20.4},
];
assert.equal(ctx.uniqueArray(samePixel, ctx.starProfileCompare).length, 2);
const fit = {sx:2, sy:1.5, residual:0.0005};
const mock = [fit, fit, fit];
const gaussian = ctx.measure(mock, 0);
const moffat = ctx.measure(mock, 4);
almost(gaussian.fwhm, 2*Math.sqrt(2*Math.log(2))*Math.sqrt(3));
almost(moffat.fwhm, 2*Math.sqrt(Math.pow(2, 1/4)-1)*Math.sqrt(3));
almost(gaussian.eccentricity, Math.sqrt(1-(1.5/2)**2));
almost(gaussian.residual, 65535*0.0005);
assert.equal(gaussian.support, 3);
const selected = ctx.measure([fit, fit, fit, {sx:4, sy:3, residual:0.0005}], 4);
almost(selected.fwhm, moffat.fwhm);
assert(selected.spreadFwhm > moffat.spreadFwhm);

const result = {
  schema: 'BKL046_FWHMECCENTRICITY_SOURCE_AGGREGATION_V1',
  sourceSha256,
  sourceScriptVersion: '1.5.3',
  cases: {
    reportedMadForOneOneOneNine: location.last,
    medianAbsoluteDeviationForSameSample: 0,
    uniqueRoundedPositions: 2,
    sameSyntheticWidths: {gaussian, moffat4: moffat},
    widerOutlier: {medianUnchanged: true, spreadFwhm: selected.spreadFwhm, support: selected.support},
  },
  syntheticFitRows: true,
  pixInsightExecuted: false,
  scientificClosures: 0,
};
const bytes = Buffer.from(JSON.stringify(result, null, 2) + '\n');
if (fs.existsSync(destination)) assert(fs.readFileSync(destination).equals(bytes));
else fs.writeFileSync(destination, bytes, {flag:'wx'});
process.stdout.write(JSON.stringify(result));
