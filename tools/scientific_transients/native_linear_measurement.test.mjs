// All pixel values, file bytes and PJSR API objects below are synthetic mocks.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import vm from 'node:vm';

const base = new URL('./', import.meta.url);
const libraries = ['native_linear_uncertainty.jsh', 'strict_passive_json.jsh', 'native_float32_primary.jsh', 'native_linear_measurement.jsh'];
const code = Object.fromEntries(libraries.map(n => [n, readFileSync(new URL(n, base), 'utf8')]));
const launcherCode = readFileSync(new URL('native_linear_launcher.jsh',base),'utf8');
const hash = raw => createHash('sha256').update(raw).digest('hex');
const bytes = value => Buffer.from(JSON.stringify(value), 'ascii');
const componentNames = ['PHOTON_READ_DIGITIZATION', 'DARK_MASTER_AND_TEMPORAL', 'FLAT_GAIN_NORMALIZATION',
  'CALIBRATION', 'SKY_BACKGROUND_ESTIMATOR', 'RESAMPLING_REGISTRATION', 'QUANTIZATION', 'REFERENCE_PSF_APERTURE_SELECTION'];

function fixture(change = () => {}, options = {}) {
  const operation = 'a'.repeat(32), root = 'F:/Synthetic/native-work/' + operation;
  const files = new Map(libraries.map(n => [n, Buffer.from(code[n])]));
  const width = options.width || 3, height = options.height || 2;
  const source = Buffer.alloc(2880 + Math.ceil(width * height * 4 / 2880) * 2880);
  ['SIMPLE  =                    T', 'BITPIX  =                  -32', 'NAXIS   =                    2',
    'NAXIS1  = ' + String(width).padStart(20), 'NAXIS2  = ' + String(height).padStart(20), 'END'].forEach((s, i) => source.write(s.padEnd(80), 80 * i, 'ascii'));
  source.fill(32, 480, 2880);
  const pattern = [2, -1, 0, -0, 1.5, .25];
  for (let i = 0; i < width * height; ++i) source.writeFloatBE(pattern[i % pattern.length], 2880 + 4 * i);
  files.set('source.fits', source);
  const h = n => hash('synthetic-' + n);
  const kernel = {protocol: 'DSG_NATIVE_LINEAR_UNCERTAINTY_V1', identity: {imageSha256: hash(source),
    gridSha256: h('grid'), maskSha256: h('mask'), normalizationSha256: h('normalization'), weightSha256: h('weight'),
    modelSha256: h('model'), factorSourceSha256: h('factor'), epochRef: 'SYNTHETIC_EPOCH', unit: 'ADU', coordinateConvention: 'PI_NATIVE_GEOMETRIC_ROW_MAJOR'},
    grid: {width, height, channels: 1, channel: 0}, pixelIndices: [0, 1], aperture: [1, 0], background: [0, 1],
    basis: {sha256: h('basis'), whiteningEvidenceSha256: h('whitening'), latentRefs: ['Z0']},
    factors: [{latentRef: 'Z0', rows: [0, 1], responses: [.5, .25], structuralZeroEvidenceSha256: null}],
    budget: componentNames.map(component => ({component, state: 'MISSING', evidenceSha256: null, domainSha256: null}))};
  const lineage = {protocol: 'DSG_NATIVE_SOURCE_LINEAGE_V1', sourceSha256: hash(source), parentManifestSha256: h('parent'),
    providerProductCardSha256: h('provider'), upstreamPixInsightHistory: 'NOT_PRESENT_IN_SOURCE_FITS', interpretation: 'SOURCE_PROVENANCE_NOT_PHYSICAL_ACCEPTANCE'};
  change(kernel, lineage, files);
  files.set('kernel-spec.json', bytes(kernel)); files.set('source-lineage.json', bytes(lineage));
  const references = Object.fromEntries(['gridSha256', 'maskSha256', 'normalizationSha256', 'weightSha256', 'modelSha256', 'factorSourceSha256'].map(k => ['identity.' + k, kernel.identity[k]]));
  references['basis.sha256'] = kernel.basis.sha256; references['basis.whiteningEvidenceSha256'] = kernel.basis.whiteningEvidenceSha256;
  for (const b of kernel.budget) if (b.state !== 'MISSING') for (const key of ['evidenceSha256', 'domainSha256']) references[`budget.${b.component}.${key}`] = b[key];
  references['lineage.parentManifestSha256'] = lineage.parentManifestSha256;
  references['lineage.providerProductCardSha256'] = lineage.providerProductCardSha256;
  const bindings = Object.entries(references).map(([role, referenceSha256]) => {
    const card = {protocol: 'DSG_NATIVE_LINEAR_BINDING_CARD_V1', role, referenceSha256, sourceSha256: hash(source),
      kernelSpecSha256: hash(files.get('kernel-spec.json')), scope: 'DECLARATION_ONLY_NOT_PHYSICAL_ACCEPTANCE'};
    options.alterCard?.(card);
    const raw = bytes(card);
    const cardSha256 = hash(raw); files.set('source-card-' + cardSha256 + '.json', raw);
    return {role, referenceSha256, cardSha256};
  });
  const parameters = {protocol: 'DSG_NATIVE_LINEAR_MEASUREMENT_V2', operationRef: operation, purpose: 'DEVELOPMENT',
    ownerNonce: 'b'.repeat(32), processSessionRef: 'c'.repeat(32),
    expectedPixInsightVersion: '1.9.5 build 1706', kernelSpecSha256: hash(files.get('kernel-spec.json')), lineageSha256: hash(files.get('source-lineage.json')),
    source: {sha256: hash(source), byteLength: source.length, primaryHeaderSha256: hash(source.subarray(0, 2880)), dataOffset: 2880,
      width, height, sampleFormat: 'FLOAT32_BE', orientation: 'FITS_AXIS1_FAST_NO_FLIP', bscale: 1, bzero: 0},
    dependencies: {coreSha256: hash(files.get(libraries[0])), parserSha256: hash(files.get(libraries[1])), primarySha256: hash(files.get(libraries[2])), wrapperSha256: hash(files.get(libraries[3]))},
    maxRuntimeSeconds: 180, bindings};
  options.alterParameters?.(parameters);
  files.set('parameters.json', bytes(parameters));
  const created = Date.parse('2026-10-16T10:00:00Z');
  const seal = {protocol: 'DSG_NATIVE_LINEAR_LAUNCH_SEAL_V1', operationRef: operation, createdUTC: '2026-10-16T10:00:00Z',
    files: [...files].map(([name, raw]) => ({role: name, name, sha256: hash(raw), byteLength: raw.length})),
    arbSha256: h('arb'), rqSha256: h('rq'), inputClosureAccepted: false};
  files.set('launch-seal.json', bytes(seal));
  files.set('launch-grant.json', bytes({protocol: 'DSG_NATIVE_LINEAR_SINGLE_START_GRANT_V1', operationRef: operation,
    sealSha256: hash(files.get('launch-seal.json')), purpose: 'DEVELOPMENT', authorized: true, maxStarts: 1, maxRuntimeSeconds: 180,
    createdUTC: '2026-10-16T10:00:00Z', expiresUTC: '2026-10-16T10:03:00Z', deadlineUTC: '2026-10-16T10:03:00Z'}));
  const owner = {protocol:'DSG_NATIVE_LINEAR_OWNER_V1',operationRef:operation,ownerNonce:parameters.ownerNonce,
    processSessionRef:parameters.processSessionRef,sealSha256:hash(files.get('launch-seal.json')),
    grantSha256:hash(files.get('launch-grant.json')),launchControlSha256:h('control'),parentIntentSha256:h('intent'),
    nativeProcessId:'4242',processCreationFileTime:'0123456789abcdef',parentDeadlineUTC:'2026-10-16T10:03:00Z'};
  options.alterOwner?.(owner); files.set('native-owner.json',bytes(owner));
  const ownerReady = {protocol:'DSG_NATIVE_LINEAR_OWNER_READY_V1',operationRef:operation,ownerNonce:parameters.ownerNonce,
    processSessionRef:parameters.processSessionRef,ownerSha256:hash(files.get('native-owner.json'))};
  options.alterOwnerReady?.(ownerReady);files.set('native-owner-ready.json',bytes(ownerReady));
  const state = {wall: created + 1000, mono: 0, reads: [], chunks: [], hashChunks: [], writes: [], closed: [], created: 0, root, operation, files};
  const basename = path => { assert.ok(path.startsWith(root + '/')); return path.slice(root.length + 1); };
  const context = vm.createContext({
    options,
    bridgeNow: () => state.wall,
    bridgeElapsed: () => state.mono,
    bridgeNames: () => JSON.stringify([...files.keys()]),
    bridgeExists: path => files.has(basename(path)),
    bridgeSize: path => { const raw = files.get(basename(path)); if (!raw) throw Error('MOCK_FILE_MISSING'); return raw.length; },
    bridgeRead: (path, start, n) => { const name=basename(path);state.reads.push({name, n});const raw=[...files.get(name).subarray(start,start+n)];options.onRead?.(name,state);return raw; },
    bridgeHash: data => hash(typeof data === 'string' ? Buffer.from(data, 'utf8') : Buffer.from(data)),
    bridgeChunk: n => state.chunks.push(n),
    bridgeHashChunk: n => state.hashChunks.push(n),
    bridgeWrite: (path, text) => { const name = basename(path); state.writes.push(name); if (options.failWrite === name) throw Error('MOCK_WRITE_FAILURE'); files.set(name, Buffer.from(text, 'utf8')); options.onWrite?.(name, state); },
    bridgeCreated: () => { ++state.created; },
    bridgeClosed: kind => { state.closed.push(kind); },
    bridgeOpen: () => { options.onOpen?.(state); },
    bridgeTimeAdvance: () => { state.wall += options.advanceWall || 0; state.mono += options.advanceMono || 0; },
    bridgeSleep: ms => {state.wall+=ms;state.mono+=ms/1000;state.sleeps=(state.sleeps||0)+1;options.onSleep?.(state);},
    bridgeAfterWrapper: () => options.afterWrapper?.(state)
  });
  vm.runInContext(`
    class MockDate extends Date { static now(){return bridgeNow();} } globalThis.Date=MockDate;
    globalThis.ElapsedTime=class{constructor(){this.origin=bridgeElapsed();}get value(){return bridgeElapsed()-this.origin;}};
    globalThis.System={msleep(ms){bridgeSleep(ms);}};
    class MockBytes{constructor(a){this.data=new Uint8Array(a);}get length(){return this.data.length;}toUint8Array(){return new Uint8Array(this.data);}}
    globalThis.CryptographicHash=class{static SHA256=1;hash(a){let s=bridgeHash(a instanceof MockBytes?a.data:a);return{toHex(){return s;}};}initialize(){this.parts=[];}update(a){bridgeHashChunk(a.length);this.parts.push(...a.data);}finalize(){return this.hash(new Uint8Array(this.parts));}};
    globalThis.File=class{static exists(p){return bridgeExists(p);}static writeTextFile(p,t){bridgeWrite(p,t);}openForReading(p){this.path=p;this.pos=0;bridgeSize(p);}get size(){return bridgeSize(this.path);}read(type,n){if(type!==15)throw Error('MOCK_TYPE');let out=new MockBytes(bridgeRead(this.path,this.pos,n));this.pos+=n;return out;}close(){}};
    globalThis.FileFind=class{begin(p){this.items=JSON.parse(bridgeNames());this.i=0;return this.items.length>0;}next(){return ++this.i<this.items.length;}end(){}get name(){return this.items[this.i];}get isFile(){return true;}get isDirectory(){return false;}get isSymbolicLink(){return false;}get isRedirectionPoint(){return false;}get isReparsePoint(){return this.name===options.reparseName;}};
    globalThis.console={beginLog(p){File.writeTextFile(p,'SYNTHETIC_LOG');},endLog(){},writeln(s){}};
    globalThis.CoreApplication={pid:options.nativePid===undefined?'4242':options.nativePid,versionMajor:1,versionMinor:9,versionRelease:5,versionBuild:1706};
    globalThis.mockWindows=[];globalThis.mockSaved=Object.create(null);
    class MockImage{constructor(w,h){this.width=w;this.height=h;this.numberOfChannels=1;this.numberOfNominalChannels=1;this.bitsPerSample=64;this.isInteger=false;this.isComplex=false;this.values=new Float64Array(w*h);}setSamples(v){this.values.set(v);if(options.clamp)this.values[1]=0;}getSamples(v,x0,y0,x1,y1,c){bridgeChunk(v.length);if(v.length>65536||y1!==y0+1||c!==0)throw Error('MOCK_CHUNK');for(let x=x0;x<x1;x++)v[x-x0]=this.values[y0*this.width+x];}sample(x,y,c){return this.values[y*this.width+x]+(options.badSingleSample?1:0);}}
    globalThis.ImageWindow=class{constructor(w,h,c,b,real,color,id){bridgeCreated();this.id=id;this.closed=false;let image=new MockImage(w,h);this.mainView={image,beginProcess(){},endProcess(){},initialProcessing:{toSource(){if(options.failInitial)throw Error('MOCK_HISTORY');return 'SYNTHETIC_INITIAL_HISTORY';}},processing:{toSource(){return 'SYNTHETIC_CURRENT_HISTORY';}}};mockWindows.push(this);}saveAs(path,q,m,s,o,hints){if(options.failSave)return false;mockSaved[path]={width:this.mainView.image.width,height:this.mainView.image.height,values:new Float64Array(this.mainView.image.values)};File.writeTextFile(path,'SYNTHETIC_MOCK_XISF');return true;}forceClose(){if(options.failClose)throw Error('MOCK_CLOSE');this.closed=true;bridgeClosed(this.id);}static open(path){bridgeOpen();bridgeTimeAdvance();let s=mockSaved[path],out=[];for(let i=0;i<(options.openCount??1);i++){let w=new ImageWindow(s.width,s.height,1,64,true,false,'reopened_'+i);w.mainView.image.values.set(s.values);if(options.corruptReopen)w.mainView.image.values[0]+=1;out.push(w);}return out;}};
  `, context);
  for (const name of libraries) vm.runInContext(code[name], context, {filename: name});
  vm.runInContext(launcherCode,context,{filename:'native_linear_launcher.jsh'});
  vm.runInContext('globalThis.syntheticActualWrapper=DSGNativeLinearMeasurement;DSGNativeLinearMeasurement=function(root,budget){var t=syntheticActualWrapper(root,budget);bridgeAfterWrapper();return t;};',context);
  return {state, context, parameters, seal, run() { return vm.runInContext(`DSGNativeLinearMeasurement(${JSON.stringify(root)})`, context); },
    runLauncher(change=()=>{}) {const p={operationRef:operation,ownerNonce:parameters.ownerNonce,processSessionRef:parameters.processSessionRef,
      sealSha256:hash(files.get('launch-seal.json')),grantSha256:hash(files.get('launch-grant.json')),wrapperSha256:hash(files.get('native_linear_measurement.jsh')),
      parentDeadlineUTC:'2026-10-16T10:03:00Z'};change(p);return vm.runInContext(`DSGNativeLinearLaunch(${JSON.stringify(root)},${JSON.stringify(p)})`,context);},
    json(name) { return JSON.parse(files.get(name).toString('ascii')); }};
}

test('native wrapper: synthetic source and actual core produce exact conditional flux and variance', () => {
  const f = fixture(); const terminal = f.run();
  assert.equal(terminal.state, 'COMPLETED_CONDITIONAL_COMPUTATION');
  assert.equal(terminal.unclosedOwnedViews, 0);
  const r = f.json('result.json'); assert.equal(r.observedFiniteApertureFlux, 3); assert.equal(r.varianceUnderSuppliedJointModel, .0625);
  assert.equal(r.fullPhysicalVariance, null); assert.equal(r.significance, null); assert.equal(r.qualifiedControls, 0);
  assert.equal(f.state.closed.length, 2);
  assert.equal(f.json('terminal-ready.json').terminalSha256, hash(f.state.files.get('terminal.json')));
  assert.equal(terminal.products.length, 12);
  for (const p of terminal.products) { assert.equal(p.role, p.name); assert.equal(hash(f.state.files.get(p.name)), p.sha256); }
  assert.ok(vm.runInContext('Object.is(mockSaved[Object.keys(mockSaved)[0]].values[3],-0)', f.context));
});
test('native wrapper: unsealed source mutation blocks before creating images', () => {
  const f = fixture(); f.state.files.get('source.fits')[3000] ^= 1;
  assert.throws(() => f.run(), /SEALED_BYTES_CHANGED/); assert.equal(f.state.created, 0); assert.equal(f.state.writes.length, 0);
});
test('native wrapper: output collision blocks before log truncation', () => {
  const f = fixture(); f.state.files.set('native.log', Buffer.from('KEEP'));
  assert.throws(() => f.run(), /INITIAL_OUTPUT_COLLISION/); assert.equal(f.state.files.get('native.log').toString(), 'KEEP');
});
test('native wrapper: supplied samples and bad support rejected before image allocation', () => {
  for (const change of [k => {k.samples = [0,0];}, k => {k.pixelIndices = [1,0];}, k => {k.factors[0].rows = [0,2];}]) {
    const f = fixture(change); const t = f.run(); assert.equal(t.state, 'FAILED_RETAINED'); assert.equal(f.state.created, 0);
  }
});
test('native wrapper: failed source import comparison retains checkpoint and histories', () => {
  const f = fixture(undefined, {clamp: true}); const t = f.run();
  assert.equal(t.state, 'FAILED_RETAINED'); assert.equal(t.errorCode, 'NATIVE_LINEAR_IMAGE_VALUE_CHANGED');
  assert.equal(t.unclosedOwnedViews, 0); assert.ok(f.state.files.has('error-owned-1.xisf')); assert.ok(f.state.files.has('closing-source.js'));
});
test('native wrapper: checkpoint mismatch is a retained failure, not accepted', () => {
  const f = fixture(undefined, {corruptReopen: true}); const t = f.run();
  assert.equal(t.state, 'FAILED_RETAINED'); assert.equal(t.unclosedOwnedViews, 0); assert.equal(t.qualifiedControls, 0);
  assert.ok(f.state.files.has('error-owned-2.xisf')); assert.equal(f.state.closed.length, 2);
});
test('native wrapper: excess reopened windows stay open and no ready is fabricated', () => {
  const f = fixture(undefined, {openCount: 2}); assert.throws(() => f.run(), /OWNERSHIP_EXCESS_UNCERTAIN/);
  assert.equal(f.state.created, 3); assert.equal(f.state.closed.length, 0); assert.ok(!f.state.files.has('terminal-ready.json'));
});
test('native wrapper: History failure preserves owned view without forced close', () => {
  const f = fixture(undefined, {failInitial: true}); const t = f.run();
  assert.equal(t.state, 'UNCERTAIN_RETENTION'); assert.equal(t.unclosedOwnedViews, 1); assert.equal(f.state.closed.length, 0);
});
test('native wrapper: close failure is uncertainty and never zero owned views', () => {
  const f = fixture(undefined, {failClose: true}); const t = f.run();
  assert.equal(t.state, 'UNCERTAIN_RETENTION'); assert.equal(t.unclosedOwnedViews, 2); assert.equal(f.state.closed.length, 0);
});
test('native wrapper: cooperative timeout after uninterruptible open preserves failure', () => {
  const f = fixture(undefined, {advanceWall: 181000, advanceMono: 181}); const t = f.run();
  assert.equal(t.state, 'FAILED_RETAINED'); assert.equal(t.cooperativeDeadlineExceeded, true); assert.equal(t.unclosedOwnedViews, 0);
});
test('native wrapper: existing cancel request yields retained cancellation without image allocation', () => {
  const f = fixture(); f.state.files.set('cancel.json', bytes({protocol:'DSG_NATIVE_LINEAR_CANCEL_V1',operationRef:f.state.operation,requested:true}));
  const t = f.run(); assert.equal(t.state, 'CANCELLED_RETAINED'); assert.equal(f.state.created, 0);
});
test('native wrapper: all streaming hash requests are bounded and original inputs unchanged', () => {
  const f = fixture(); const original = new Map([...f.state.files].map(([n,b]) => [n,hash(b)])); f.run();
  for (const [n,h] of original) assert.equal(hash(f.state.files.get(n)), h);
  assert.ok(f.state.reads.every(r => r.n > 0 && r.n <= 64 * 1048576));
});
test('native wrapper: terminal IO failure retains a failure fence without ready', () => {
  const f = fixture(undefined, {failWrite: 'terminal.json'});
  assert.throws(() => f.run(), /FINAL_PUBLICATION_UNCERTAIN/);
  assert.ok(f.state.files.has('native-publication-uncertain.json')); assert.ok(!f.state.files.has('terminal-ready.json'));
});
test('native wrapper: deadline crossed during ready write preserves stale receipt plus uncertainty', () => {
  const f = fixture(undefined, {onWrite(name, state) { if(name === 'terminal-ready.json'){state.mono=181;state.wall+=181000;} }});
  assert.throws(() => f.run(), /FINAL_PUBLICATION_UNCERTAIN/);
  assert.ok(f.state.files.has('terminal-ready.json')); assert.ok(f.state.files.has('native-publication-uncertain.json'));
});
test('native wrapper: product changed at ready boundary is uncertainty, never overwritten', () => {
  const f = fixture(undefined, {onWrite(name, state) { if(name === 'terminal-ready.json')state.files.set('result.json',Buffer.from('SYNTHETIC_CORRUPTION')); }});
  assert.throws(() => f.run(), /FINAL_PUBLICATION_UNCERTAIN/);
  assert.equal(f.state.files.get('result.json').toString(), 'SYNTHETIC_CORRUPTION'); assert.ok(f.state.files.has('native-publication-uncertain.json'));
});
test('native wrapper: failure of both ready and fence still throws, without retry or positive return', () => {
  const f = fixture(undefined, {onWrite(name) { if(name === 'terminal-ready.json'||name === 'native-publication-uncertain.json')throw Error('MOCK_IO_AFTER_WRITE'); }});
  assert.throws(() => f.run(), /FINAL_PUBLICATION_UNCERTAIN/);
  assert.equal(f.state.writes.filter(n=>n==='terminal-ready.json').length,1);
  assert.equal(f.state.writes.filter(n=>n==='native-publication-uncertain.json').length,1);
});
test('native wrapper: wide rows and streamed hashes never exceed65536 chunk samples/bytes', () => {
  const f = fixture(undefined, {width:65537,height:1}); assert.equal(f.run().state,'COMPLETED_CONDITIONAL_COMPUTATION');
  assert.ok(f.state.chunks.includes(65536)); assert.ok(f.state.chunks.includes(1));
  assert.ok(f.state.chunks.every(n=>n<=65536)); assert.ok(f.state.hashChunks.every(n=>n<=65536));
});
test('native wrapper: per-pixel native read must equal raw oracle independently of bulk reads', () => {
  const f = fixture(undefined, {badSingleSample:true}); const t=f.run();
  assert.equal(t.state,'FAILED_RETAINED'); assert.equal(t.errorCode,'NATIVE_LINEAR_SUPPORT_SAMPLE_CHANGED');
  assert.ok(!f.state.files.has('result.json'));
});
test('native wrapper: epoch type and nonfinite factor rejected before image allocation', () => {
  for(const change of [k=>{k.identity.epochRef=123;},k=>{k.factors[0].responses[0]=null;}]){
    const f=fixture(change); assert.equal(f.run().state,'FAILED_RETAINED'); assert.equal(f.state.created,0);
  }
});
test('native wrapper: conditional structural zero remains physically unaccepted', () => {
  const f=fixture(k=>{k.factors[0].rows=[];k.factors[0].responses=[];k.factors[0].structuralZeroEvidenceSha256=hash('SYNTHETIC_ZERO_DECLARATION');});
  assert.equal(f.run().state,'COMPLETED_CONDITIONAL_COMPUTATION');const r=f.json('result.json');
  assert.equal(r.varianceUnderSuppliedJointModel,0);assert.equal(r.fullPhysicalVariance,null);assert.equal(r.physicalApplicabilityVerified,false);
});
test('native wrapper: invalid or expired fresh grant never creates outputs', () => {
  for(const update of [{authorized:false},{maxStarts:2},{expiresUTC:'2026-10-16T10:00:00Z'}]){
    const f=fixture(); const grant=f.json('launch-grant.json');Object.assign(grant,update);f.state.files.set('launch-grant.json',bytes(grant));
    assert.throws(()=>f.run());assert.equal(f.state.created,0);assert.equal(f.state.writes.length,0);
  }
});
test('native wrapper: reparse entry refused before any log or image creation', () => {
  const f=fixture(undefined,{reparseName:'source.fits'});assert.throws(()=>f.run(),/UNEXPECTED_ENTRY/);
  assert.equal(f.state.writes.length,0);assert.equal(f.state.created,0);
});
test('native wrapper: cryptographically sealed but semantically wrong source card blocks', () => {
  const f=fixture(undefined,{alterCard(card){card.scope='PHYSICALLY_ACCEPTED';}});
  const t=f.run();assert.equal(t.state,'FAILED_RETAINED');assert.equal(t.errorCode,'NATIVE_LINEAR_BINDING_CARD');assert.equal(f.state.created,0);
});
test('native wrapper: duplicate or unknown binding roles cannot resolve by valid hashes alone', () => {
  for(const alterParameters of [p=>{p.bindings[1]={...p.bindings[0]};},p=>{p.bindings[0].role='identity.unknown';}]){
    const f=fixture(undefined,{alterParameters});assert.equal(f.run().state,'FAILED_RETAINED');assert.equal(f.state.created,0);
  }
});
test('native wrapper: complete supplied budget declarations still do not prove full physical variance', () => {
  const f=fixture(k=>{for(const b of k.budget){b.state='REPRESENTED_JOINTLY';b.evidenceSha256=hash('synthetic-evidence-'+b.component);b.domainSha256=hash('synthetic-domain-'+b.component);}});
  assert.equal(f.run().state,'COMPLETED_CONDITIONAL_COMPUTATION');const r=f.json('result.json');
  assert.ok(r.budget.every(b=>b.state==='REPRESENTED_JOINTLY'));assert.equal(r.fullPhysicalVariance,null);assert.equal(r.qualifiedControls,0);assert.equal(r.physicalApplicabilityVerified,false);
});
test('native wrapper: cancellation arriving during final ready hash preserves stale receipt and uncertainty', () => {
  let readyReads=0;
  const f=fixture(undefined,{onRead(name,state){if(name==='terminal-ready.json'&&++readyReads===3)state.files.set('cancel.json',bytes({protocol:'DSG_NATIVE_LINEAR_CANCEL_V1',operationRef:state.operation,requested:true}));}});
  assert.throws(()=>f.run(),/FINAL_PUBLICATION_UNCERTAIN/);
  assert.equal(readyReads,3);assert.ok(f.state.files.has('terminal-ready.json'));
  assert.equal(f.json('native-publication-uncertain.json').errorCode,'NATIVE_LINEAR_CANCELLED');
  assert.equal(f.state.writes.filter(n=>n==='terminal-ready.json').length,1);
});

test('native ownership: actual process ID must match before any output or image', () => {
  for (const nativePid of ['4243',4242,'04242','0','4294967296']) {
    const f=fixture(undefined,{nativePid});assert.throws(()=>f.run(),/OWNER_PID/);
    assert.equal(f.state.created,0);assert.equal(f.state.writes.length,0);
  }
});

test('native ownership: nonce, session, seal and grant mismatch block before allocation', () => {
  for (const key of ['ownerNonce','processSessionRef','sealSha256','grantSha256']) {
    const f=fixture(undefined,{alterOwner(p){p[key]='d'.repeat(key.endsWith('Sha256')?64:32);}});
    assert.throws(()=>f.run(),/OWNER_(SESSION_BINDING|PARENT_BINDING)/);
    assert.equal(f.state.created,0);assert.equal(f.state.writes.length,0);
  }
});

test('native ownership: ready must pin exact owner bytes and session', () => {
  for (const alterOwnerReady of [r=>{r.ownerSha256='0'.repeat(64);},r=>{r.processSessionRef='d'.repeat(32);},r=>{r.extra=true;}]) {
    const f=fixture(undefined,{alterOwnerReady});assert.throws(()=>f.run(),/OWNER_/);
    assert.equal(f.state.created,0);assert.equal(f.state.writes.length,0);
  }
});

test('native ownership: missing controls and V1 parameters are refused', () => {
  for (const name of ['native-owner.json','native-owner-ready.json']) {
    const f=fixture();f.state.files.delete(name);assert.throws(()=>f.run(),/MISSING_INPUT/);assert.equal(f.state.created,0);
  }
  const f=fixture(undefined,{alterParameters(p){p.protocol='DSG_NATIVE_LINEAR_MEASUREMENT_V1';}});
  assert.throws(()=>f.run(),/PARAMETERS/);assert.equal(f.state.created,0);
});

test('native ownership: malformed PID, parent pins, creation time and expiry block', () => {
  for (const alterOwner of [p=>{p.nativeProcessId='04242';},p=>{p.launchControlSha256='bad';},
    p=>{p.processCreationFileTime='0';},p=>{p.parentDeadlineUTC='2026-10-16T10:00:00Z';},p=>{p.extra=true;}]) {
    const f=fixture(undefined,{alterOwner});assert.throws(()=>f.run(),/OWNER_/);assert.equal(f.state.created,0);
  }
});

test('native ownership: post-read raw mutation blocks before outputs', () => {
  let mutated=false;
  const f=fixture(undefined,{onRead(name,state){if(name==='native-owner.json'&&!mutated){mutated=true;const p=JSON.parse(state.files.get(name));p.parentIntentSha256='0'.repeat(64);state.files.set(name,bytes(p));}}});
  assert.throws(()=>f.run(),/OWNER_BYTES_CHANGED/);assert.equal(f.state.created,0);assert.equal(f.state.writes.length,0);
});

test('native ownership: raw controls remain pinned through final ready publication', () => {
  const f=fixture(undefined,{onWrite(name,state){if(name==='terminal-ready.json')state.files.set('native-owner-ready.json',Buffer.from('{}'));}});
  assert.throws(()=>f.run(),/FINAL_PUBLICATION_UNCERTAIN/);
  assert.ok(f.state.files.has('native-publication-uncertain.json'));assert.ok(f.state.files.has('terminal-ready.json'));
});

test('native ownership: V2 evidence binds actual PID and exact dynamic control hashes', () => {
  const f=fixture();assert.equal(f.run().state,'COMPLETED_CONDITIONAL_COMPUTATION');const e=f.json('native-evidence.json');
  assert.equal(e.protocol,'DSG_NATIVE_LINEAR_EVIDENCE_V2');assert.equal(e.nativeProcessId,'4242');
  assert.equal(e.processSessionRef,f.parameters.processSessionRef);
  assert.equal(e.ownerSha256,hash(f.state.files.get('native-owner.json')));
  assert.equal(e.ownerReadySha256,hash(f.state.files.get('native-owner-ready.json')));
  assert.equal(e.qualifiedControls,0);assert.equal(e.fullPhysicalVariance,null);
});

test('native ownership: stricter parent wall deadline cannot be reset by wrapper', () => {
  const f=fixture(undefined,{alterOwner(p){p.parentDeadlineUTC='2026-10-16T10:00:03Z';},advanceWall:5000,advanceMono:5});
  const t=f.run();assert.equal(t.state,'FAILED_RETAINED');assert.equal(t.cooperativeDeadlineExceeded,true);
});

test('native launcher: actual wrapper return is separately bound to terminal, ready and PID',()=>{
  const f=fixture(),r=f.runLauncher();assert.equal(r.protocol,'DSG_NATIVE_LINEAR_RETURNED_V1');
  assert.equal(r.terminalSha256,hash(f.state.files.get('terminal.json')));assert.equal(r.readySha256,hash(f.state.files.get('terminal-ready.json')));
  assert.equal(r.nativeProcessId,'4242');assert.equal(r.state,'COMPLETED_CONDITIONAL_COMPUTATION');
  assert.equal(r.qualifiedControls,0);assert.equal(f.state.writes.filter(n=>n==='native-return.json').length,1);
  assert.ok(!f.json('terminal.json').products.some(p=>p.name==='native-return.json'));
});

test('native launcher: bounded parent wait precedes any image and supports delayed ready',()=>{
  let ready;
  const f=fixture(undefined,{onSleep(state){assert.equal(state.created,0);if(state.sleeps===3)state.files.set('native-owner-ready.json',ready);}});
  ready=f.state.files.get('native-owner-ready.json');f.state.files.delete('native-owner-ready.json');
  assert.equal(f.runLauncher().state,'COMPLETED_CONDITIONAL_COMPUTATION');assert.equal(f.state.sleeps,3);
});

test('native launcher: absent parent ready expires without wrapper/images or causal return',()=>{
  const f=fixture();f.state.files.delete('native-owner-ready.json');
  assert.throws(()=>f.runLauncher(),/NATIVE_LAUNCH_UNCERTAIN/);assert.equal(f.state.created,0);
  assert.equal(f.json('native-publication-uncertain.json').errorCode,'NATIVE_LAUNCH_DEADLINE');
  assert.ok(!f.state.files.has('native-return.json'));assert.ok(f.state.sleeps<=18000);
});

test('native launcher: cancellation during parent wait prevents native wrapper call',()=>{
  const f=fixture(undefined,{onSleep(state){state.files.set('cancel.json',bytes({protocol:'DSG_NATIVE_LINEAR_CANCEL_V1',operationRef:state.operation,requested:true}));}});
  f.state.files.delete('native-owner-ready.json');assert.throws(()=>f.runLauncher(),/NATIVE_LAUNCH_UNCERTAIN/);
  assert.equal(f.state.created,0);assert.equal(f.json('native-publication-uncertain.json').errorCode,'NATIVE_LAUNCH_CANCELLED');
});

test('native launcher: wrong actual PID or parent deadline is refused before wrapper outputs',()=>{
  for(const option of [{nativePid:'4243'},{alterOwner(p){p.parentDeadlineUTC='2026-10-16T10:02:00Z';}}]){
    const f=fixture(undefined,option);assert.throws(()=>f.runLauncher(),/NATIVE_LAUNCH_UNCERTAIN/);
    assert.equal(f.state.created,0);assert.ok(!f.state.files.has('started-native.json'));
  }
});

test('native launcher: thrown wrapper after stale ready never synthesizes causal return',()=>{
  const f=fixture();vm.runInContext("DSGNativeLinearMeasurement=function(root){syntheticActualWrapper(root);throw Error('SYNTHETIC_AFTER_READY');};",f.context);
  assert.throws(()=>f.runLauncher(),/NATIVE_LAUNCH_UNCERTAIN/);assert.ok(f.state.files.has('terminal-ready.json'));
  assert.ok(!f.state.files.has('native-return.json'));assert.ok(f.state.files.has('native-publication-uncertain.json'));
});

test('native launcher: stored terminal must equal full actual returned object',()=>{
  const f=fixture(undefined,{afterWrapper(state){const t=JSON.parse(state.files.get('terminal.json'));t.state='FAILED_RETAINED';state.files.set('terminal.json',bytes(t));}});
  assert.throws(()=>f.runLauncher(),/NATIVE_LAUNCH_UNCERTAIN/);assert.equal(f.json('native-publication-uncertain.json').errorCode,'NATIVE_LAUNCH_ACTUAL_RETURN');
  assert.ok(!f.state.files.has('native-return.json'));
});

test('native launcher: actual returned cleanup evidence survives elapsed deadline without scientific acceptance',()=>{
  const f=fixture(undefined,{afterWrapper(state){state.wall+=181000;state.mono+=181;}});
  const r=f.runLauncher();assert.equal(r.state,'COMPLETED_CONDITIONAL_COMPUTATION');assert.equal(r.qualifiedControls,0);
  assert.equal(r.fullPhysicalVariance,null);assert.ok(!Object.hasOwn(r,'technicalComputationAccepted'));
});

test('native launcher: existing return is preserved and never grants another wrapper call',()=>{
  const f=fixture();f.state.files.set('native-return.json',Buffer.from('KEEP'));
  assert.throws(()=>f.runLauncher(),/NATIVE_LAUNCH_UNCERTAIN/);assert.equal(f.state.files.get('native-return.json').toString(),'KEEP');
  assert.equal(f.state.created,0);assert.equal(f.state.writes.filter(n=>n==='native-return.json').length,0);
});

test('native launcher: failed or partial return IO retains uncertainty without retry',()=>{
  for(const option of [{failWrite:'native-return.json'},{onWrite(name,state){if(name==='native-return.json')state.files.set(name,Buffer.from('{'));}}]){
    const f=fixture(undefined,option);assert.throws(()=>f.runLauncher(),/NATIVE_LAUNCH_UNCERTAIN/);
    assert.equal(f.state.writes.filter(n=>n==='native-return.json').length,1);assert.ok(f.state.files.has('native-publication-uncertain.json'));
  }
});

test('native launcher: valid return file does not outrank fence created during publication',()=>{
  const f=fixture(undefined,{onWrite(name,state){if(name==='native-return.json')state.files.set('native-publication-uncertain.json',Buffer.from('SYNTHETIC_FENCE'));}});
  assert.throws(()=>f.runLauncher(),/NATIVE_LAUNCH_UNCERTAIN/);assert.equal(f.json('native-return.json').protocol,'DSG_NATIVE_LINEAR_RETURNED_V1');
  assert.equal(f.state.files.get('native-publication-uncertain.json').toString(),'SYNTHETIC_FENCE');
});

test('native launcher: stalled UTC cannot renew one second of original residual budget',()=>{
  let ready;
  const f=fixture(undefined,{alterOwner(p){p.parentDeadlineUTC='2026-10-16T10:00:02Z';},onSleep(state){state.wall-=10;state.mono+=2;state.files.set('native-owner-ready.json',ready);}});
  ready=f.state.files.get('native-owner-ready.json');f.state.files.delete('native-owner-ready.json');
  assert.throws(()=>f.runLauncher(p=>{p.parentDeadlineUTC='2026-10-16T10:00:02Z';}),/NATIVE_LAUNCH_UNCERTAIN/);
  assert.equal(f.state.created,0);assert.ok(!f.state.files.has('started-native.json'));
  assert.equal(f.json('native-publication-uncertain.json').errorCode,'NATIVE_LAUNCH_DEADLINE');
});

test('native launcher: wrapper carries live original residual after a partial wait with stalled UTC',()=>{
  let ready;
  const f=fixture(undefined,{alterOwner(p){p.parentDeadlineUTC='2026-10-16T10:00:02Z';},advanceMono:.6,
    onSleep(state){state.wall-=10;state.mono+=.5;state.files.set('native-owner-ready.json',ready);}});
  ready=f.state.files.get('native-owner-ready.json');f.state.files.delete('native-owner-ready.json');
  const r=f.runLauncher(p=>{p.parentDeadlineUTC='2026-10-16T10:00:02Z';});
  assert.equal(r.state,'FAILED_RETAINED');assert.equal(f.json('terminal.json').cooperativeDeadlineExceeded,true);
  assert.equal(f.json('terminal.json').errorCode,'NATIVE_LAUNCH_DEADLINE');
});
