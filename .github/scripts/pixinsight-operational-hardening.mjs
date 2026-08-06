const freeze = (value) => Object.freeze(value);

export const DEFAULT_PIXINSIGHT_OPERATIONAL_POLICY = freeze({
  schemaVersion: '1.0',
  maxPayloadBytes: 5 * 1024 * 1024,
  maxInputs: 5000,
  maxOutputs: 1000,
  maxProcesses: 500,
  maxRetryAttempts: 3,
  retryableErrors: freeze(['registry-read-timeout', 'catalog-read-timeout', 'transient-io']),
  terminalErrors: freeze(['unsupported-schema', 'payload-too-large', 'path-traversal', 'secret-detected'])
});

export class PixInsightOperationalHardeningPolicy {
  constructor(policy = DEFAULT_PIXINSIGHT_OPERATIONAL_POLICY) {
    this.policy = freeze({ ...DEFAULT_PIXINSIGHT_OPERATIONAL_POLICY, ...policy });
  }

  evaluateEnvelope({ payloadBytes, manifest } = {}) {
    const violations = [];
    if (!Number.isInteger(payloadBytes) || payloadBytes < 0) violations.push('invalid-payload-size');
    else if (payloadBytes > this.policy.maxPayloadBytes) violations.push('payload-too-large');

    const run = manifest?.processingRun;
    if (!run) violations.push('processing-run-missing');
    else {
      if (!Array.isArray(run.inputs) || run.inputs.length > this.policy.maxInputs) violations.push('input-limit-exceeded');
      if (!Array.isArray(run.outputs) || run.outputs.length > this.policy.maxOutputs) violations.push('output-limit-exceeded');
      if (!Array.isArray(run.processes) || run.processes.length > this.policy.maxProcesses) violations.push('process-limit-exceeded');
    }

    return freeze({ allowed: violations.length === 0, violations: freeze(violations) });
  }

  classifyFailure({ errorCode, attempt = 1 } = {}) {
    if (this.policy.terminalErrors.includes(errorCode)) {
      return freeze({ disposition: 'dead-letter', retry: false, nextAttempt: null, reason: 'terminal-error' });
    }

    if (this.policy.retryableErrors.includes(errorCode) && attempt < this.policy.maxRetryAttempts) {
      return freeze({ disposition: 'retry', retry: true, nextAttempt: attempt + 1, reason: 'transient-error' });
    }

    return freeze({
      disposition: 'dead-letter',
      retry: false,
      nextAttempt: null,
      reason: this.policy.retryableErrors.includes(errorCode) ? 'retry-exhausted' : 'non-retryable-error'
    });
  }

  summarizeMetrics(records = []) {
    const counters = {
      received: records.length,
      accepted: 0,
      duplicateNoop: 0,
      unresolved: 0,
      conflict: 0,
      rejected: 0,
      retry: 0,
      deadLetter: 0
    };

    for (const record of records) {
      const outcome = record?.outcome;
      if (outcome === 'accepted') counters.accepted += 1;
      else if (outcome === 'duplicate-noop') counters.duplicateNoop += 1;
      else if (outcome === 'unresolved') counters.unresolved += 1;
      else if (outcome === 'conflict') counters.conflict += 1;
      else if (outcome === 'rejected') counters.rejected += 1;

      if (record?.disposition === 'retry') counters.retry += 1;
      if (record?.disposition === 'dead-letter') counters.deadLetter += 1;
    }

    return freeze(counters);
  }
}
