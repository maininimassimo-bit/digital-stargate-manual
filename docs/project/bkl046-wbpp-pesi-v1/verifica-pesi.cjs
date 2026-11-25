'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const crypto = require('node:crypto');
const [source, output] = process.argv.slice(2);
const raw = fs.readFileSync(source);
const sha256 = crypto.createHash('sha256').update(raw).digest('hex');
assert.equal(sha256, '2e238f66ec3e0aa31cb791b1be9190ce55e8321f6d8023694b289f10c33d4620');
const text = raw.toString('utf8').replace(/\r\n/g,'\n');
function method(name) {
  const marker = '\n   ' + name + '(';
  const start = text.indexOf(marker);
  const end = text.indexOf('\n   }', start);
  assert(start >= 0 && end > start);
  return text.slice(start + 1, end + 5);
}
const valid = text.match(/let isDescriptorValid = function\( descriptor \)\s*\{[\s\S]*?\n\s*\};/);
assert(valid);
const ctx = vm.createContext({});
const names = ['getMinMaxDescriptorsValues','computeWeightForLight','findRegistrationReferenceFileItem'];
const code = 'var analyzer = new class {\n'+names.map(method).join('\n')+'\n};\n'+valid[0]+'\nvar accepts = isDescriptorValid;';
vm.runInContext(code, ctx);
const a = ctx.analyzer;
function desc(id, fwhm, snr, stars=20) {
  return {filePath:id, FWHM:fwhm, eccentricity:0.4, SNR:snr, noise:0.01, numberOfStars:stars,
    PSFSignalWeight:4, PSFSNR:3, median:0.15, mad:0.01, Mstar:0.05};
}
const first = desc('A',2,10);
const second = desc('B',3,12);
const cohort = [first,second,desc('C',4,11)];
function compare(pool) {
  const ranges = a.getMinMaxDescriptorsValues(pool);
  return [first,second].map(x=>a.computeWeightForLight(x,ranges,1,0,1,0,0,0,1,1,false));
}
const before = compare(cohort);
const after = compare([...cohort,desc('D',2.5,30)]);
assert(before[0] < before[1] && after[0] > after[1]);
const bad = [
  ['undefinedFwhm', {...first,FWHM:undefined}],
  ['nanFwhm', {...first,FWHM:NaN}],
  ['zeroStars', {...first,numberOfStars:0}],
  ['nullFwhm', {...first,FWHM:null}],
];
const actual = Object.fromEntries(bad.map(([id,item])=>[id,ctx.accepts(item)]));
assert.deepEqual(actual, {undefinedFwhm:false,nanFwhm:false,zeroStars:false,nullFwhm:true});
const items = [
  {binning:1, descriptor:desc('normalLow',2,4,60)},
  {binning:1, descriptor:{...desc('highWeightLow',2,4,80),weightOvershoot:['synthetic']}},
  {binning:2, descriptor:desc('normalHigh',2,4,200)},
];
function reference(x) {
  return a.findRegistrationReferenceFileItem([{activeFrames:()=>x}]).descriptor.filePath;
}
assert.equal(reference(items),'normalLow');
assert.equal(reference(items.slice(1)),'highWeightLow');
const result = {
  schema:'BKL046_WBPP_MEASUREMENT_WEIGHT_DECISIONS_V1',
  sourceSha256:sha256,
  scriptVersion:'3.2.2',
  weightScenario:{metrics:['FWHM','SNR'],before,after,rankingReversed:true},
  descriptorGuard:actual,
  registrationReference:{normalFrameAvailable:reference(items),allLowestBinningFlagged:reference(items.slice(1))},
  syntheticInput:true,
  nativeExecutions:0,
  scientificClosures:0,
};
const out=Buffer.from(JSON.stringify(result,null,2)+'\n');
if (fs.existsSync(output)) assert(fs.readFileSync(output).equals(out));
else fs.writeFileSync(output,out,{flag:'wx'});
process.stdout.write(JSON.stringify(result));
