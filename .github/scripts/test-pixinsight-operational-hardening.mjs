import assert from 'node:assert/strict';
import test from 'node:test';
import {
  DEFAULT_PIXINSIGHT_OPERATIONAL_POLICY,
  PixInsightOperationalHardeningPolicy
} from './pixinsight-operational-hardening.mjs';

const manifest = () => ({
  processingRun: {
    inputs: ['asset:raw-001'],
    outputs: ['candidate:master-light-001'],
    processes: ['WeightedBatchPreprocessing']
  }
});

test('accepts an envelope within governed limits', () => {
  const policy = new PixInsightOperationalHardeningPolicy();
  const result = policy.evaluateEnvelope({ payloadBytes: 4096, manifest: manifest() });

  assert.equal(result.allowed, true);
  assert.deepEqual(result.violations, []);
  assert.equal(Object.isFrozen(result), true);
  assert.equal(Object.isFrozen(result.violations), true);
});

test('rejects payloads and collections above configured limits', () => {
  const policy = new PixInsightOperationalHardeningPolicy({
    maxPayloadBytes: 100,
    maxInputs: 1,
    maxOutputs: 1,
    maxProcesses: 1
  });
  const value = manifest();
  value.processingRun.inputs.push('asset:raw-002');
  value.processingRun.outputs.push('candidate:master-light-002');
  value.processingRun.processes.push('ImageIntegration');

  const result = policy.evaluateEnvelope({ payloadBytes: 101, manifest: value });

  assert.equal(result.allowed, false);
  assert.deepEqual(result.violations, [
    'payload-too-large',
    'input-limit-exceeded',
    'output-limit-exceeded',
    'process-limit-exceeded'
  ]);
});

test('retries transient failures using a bounded deterministic policy', () => {
  const policy = new PixInsightOperationalHardeningPolicy();

  assert.deepEqual(policy.classifyFailure({ errorCode: 'registry-read-timeout', attempt: 1 }), {
    disposition: 'retry',
    retry: true,
    nextAttempt: 2,
    reason: 'transient-error'
  });

  assert.deepEqual(policy.classifyFailure({ errorCode: 'registry-read-timeout', attempt: DEFAULT_PIXINSIGHT_OPERATIONAL_POLICY.maxRetryAttempts }), {
    disposition: 'dead-letter',
    retry: false,
    nextAttempt: null,
    reason: 'retry-exhausted'
  });
});

test('sends terminal and unknown failures to governed dead-letter handling', () => {
  const policy = new PixInsightOperationalHardeningPolicy();

  assert.equal(policy.classifyFailure({ errorCode: 'path-traversal' }).reason, 'terminal-error');
  assert.equal(policy.classifyFailure({ errorCode: 'unexpected-runtime-error' }).reason, 'non-retryable-error');
  assert.equal(policy.classifyFailure({ errorCode: 'path-traversal' }).retry, false);
});

test('summarizes operational outcomes without mutating records', () => {
  const policy = new PixInsightOperationalHardeningPolicy();
  const records = [
    { outcome: 'accepted' },
    { outcome: 'duplicate-noop' },
    { outcome: 'unresolved', disposition: 'retry' },
    { outcome: 'conflict', disposition: 'dead-letter' },
    { outcome: 'rejected', disposition: 'dead-letter' }
  ];
  const before = structuredClone(records);

  const metrics = policy.summarizeMetrics(records);

  assert.deepEqual(metrics, {
    received: 5,
    accepted: 1,
    duplicateNoop: 1,
    unresolved: 1,
    conflict: 1,
    rejected: 1,
    retry: 1,
    deadLetter: 2
  });
  assert.deepEqual(records, before);
  assert.equal(Object.isFrozen(metrics), true);
});
