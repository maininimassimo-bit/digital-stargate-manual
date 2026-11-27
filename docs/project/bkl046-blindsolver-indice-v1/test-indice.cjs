'use strict';

const assert = require('node:assert/strict');
const { createHash } = require('node:crypto');
const { readFileSync, writeFileSync } = require('node:fs');
const { Script, createContext } = require('node:vm');

const [enginePath, outputPath] = process.argv.slice(2);
const raw = readFileSync(enginePath);
const engineSha256 = createHash('sha256').update(raw).digest('hex');
assert.equal(engineSha256, 'ce315e997ff707d5af66b6b6eb2ff367f636d5c2719020d4663735fed40ec4ac');
const source = raw.toString('utf8').replace(/\r\n/g, '\n');
const selectors = [
  /^   static configuredIndexFilePath\(\)\n   \{\n[\s\S]*?^   \}/m,
  /^   astrometricIndexFilePath\(\)\n   \{\n[\s\S]*?^   \}/m,
];
const excerpts = selectors.map((pattern) => {
  const match = source.match(pattern);
  assert.ok(match, `Method missing: ${pattern}`);
  return {
    body: match[0],
    line: source.slice(0, match.index).split('\n').length,
    sha256: createHash('sha256').update(match[0], 'utf8').digest('hex'),
  };
});
const script = new Script(`class BlindSolverEngine {
  constructor() { this.indexFilePath = null; }
${excerpts.map(({ body }) => body).join('\n')}
}
globalThis.EngineUnderTest = BlindSolverEngine;`);

const path = 'X:/fixture/gdr3-index.xpsd';
const missing = /^No astrometric index file is available\./;
const cases = [];

function setup(options) {
  const calls = { gaia: [], fileExists: [] };
  const settings = { value: options.value ?? path, exists: options.exists ?? true };
  const context = {
    File: { exists(value) {
      calls.fileExists.push(value);
      if (options.fileError) throw options.fileError;
      return settings.exists;
    } },
  };
  if (!options.noGaia) {
    context.Gaia = class Gaia {
      static DataRelease_BestAvailable = 7;
      executeGlobal() {
        calls.gaia.push([this.command, this.dataRelease, this.verbosity]);
        if (options.gaiaError) throw new Error('simulated Gaia failure');
        this.astrometricIndexFilePath = settings.value;
      }
    };
  }
  script.runInContext(createContext(context));
  return { engine: new context.EngineUnderTest(), calls, settings };
}

for (const [name, options, expectedGaia] of [
  ['gaia-absent', { noGaia: true }, 0],
  ['get-info-error', { gaiaError: true }, 1],
  ['blank-configured-path', { value: '   ' }, 1],
]) {
  const { engine, calls } = setup(options);
  assert.throws(() => engine.astrometricIndexFilePath(), { message: missing });
  assert.deepEqual(calls, { gaia: expectedGaia ? [['get-info', 7, 0]] : [], fileExists: [] });
  cases.push({ name, calls, outcome: 'NO_CONFIGURED_INDEX' });
}

{
  const { engine, calls, settings } = setup({ exists: false });
  assert.throws(() => engine.astrometricIndexFilePath(), {
    message: `The astrometric index file does not exist: ${path}`,
  });
  assert.equal(engine.indexFilePath, null);
  settings.exists = true;
  assert.equal(engine.astrometricIndexFilePath(), path);
  assert.deepEqual(calls, { gaia: [['get-info', 7, 0], ['get-info', 7, 0]], fileExists: [path, path] });
  cases.push({ name: 'missing-then-present', calls, outcome: 'REJECT_THEN_RETRY_SUCCESS' });
}
{
  const sentinel = new Error('simulated filesystem failure');
  const { engine, calls } = setup({ fileError: sentinel });
  assert.throws(() => engine.astrometricIndexFilePath(), (error) => error === sentinel);
  assert.equal(engine.indexFilePath, null);
  assert.deepEqual(calls, { gaia: [['get-info', 7, 0]], fileExists: [path] });
  cases.push({ name: 'filesystem-error', calls, outcome: 'ERROR_PROPAGATED_NO_CACHE' });
}
{
  const { engine, calls, settings } = setup({ value: `  ${path}\t` });
  assert.equal(engine.astrometricIndexFilePath(), path);
  settings.value = 'X:/fixture/replacement.xpsd';
  settings.exists = false;
  assert.equal(engine.astrometricIndexFilePath(), path);
  assert.deepEqual(calls, { gaia: [['get-info', 7, 0]], fileExists: [path] });
  cases.push({ name: 'trim-and-cache', calls, outcome: 'CACHED_PATH_NOT_RECHECKED' });
}

const result = { protocol: 'BKL046_BLINDSOLVER_INDEX_METHOD_REPLAY_V1', engineSha256,
  node: process.versions.node, v8: process.versions.v8,
  excerpts: excerpts.map(({ line, sha256 }) => ({ line, sha256 })),
  cases, gaiaAndFileSimulated: true, indexBytesRead: false, nativeExecutions: 0, scientificClosures: 0 };
writeFileSync(outputPath, JSON.stringify(result, null, 2) + '\n', { encoding: 'utf8', flag: 'wx' });
