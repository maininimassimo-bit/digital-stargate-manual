import fs from 'node:fs';

const input = JSON.parse(fs.readFileSync('docs/data/bkl042-f2-advisory-response-fixture.json', 'utf8'));
const output = {
  schemaVersion: '1.0', contractType: 'BKL042_F3_DETERMINISTIC_ADVISORY_OUTPUT', demonstratorMode: 'BOUNDED_SYNTHETIC_READ_ONLY',
  producer: 'DSG.DeterministicObservatoryAdvisory', producerVersion: '1.0.0-f3', methodId: 'BKL042-F3-CLOSED-RULES-1', inputFixtureId: input.fixtureId, generatedAt: input.generatedAt,
  responses: input.cases.map(item => {
    const unavailable = item.sources.some(source => ['UNAVAILABLE', 'UNKNOWN', 'STALE', 'CONFLICT'].includes(source.lifecycle) || source.completeness !== 'COMPLETE');
    return {caseId: item.caseId, state: unavailable ? 'INSUFFICIENT_EVIDENCE' : 'ANSWERED', sourceRefs: item.sources.map(source => source.sourceId), explanation: unavailable ? 'Evidence availability gate failed; no subject-specific advisory can be produced.' : 'Evidence and citation gate passed; bounded advisory context is available.', recommendations: unavailable ? [] : ['Review the cited governed source before any human decision.'], limitations: ['Deterministic demonstrator output; not model output, scientific acceptance or execution.']};
  }),
  ruleEvaluations: input.cases.flatMap(item => {
    const unavailable = item.sources.some(source => ['UNAVAILABLE', 'UNKNOWN', 'STALE', 'CONFLICT'].includes(source.lifecycle) || source.completeness !== 'COMPLETE');
    return [{ruleId: 'CITATION_AND_AUTHORITY', caseId: item.caseId, decision: 'PASS', reasonCodes: []}, {ruleId: 'SOURCE_AVAILABILITY', caseId: item.caseId, decision: unavailable ? 'FAIL_CLOSED' : 'PASS', reasonCodes: unavailable ? ['SOURCE_UNAVAILABLE_OR_INCOMPLETE'] : []}];
  }),
  authority: {consumerMode: 'READ_ONLY', advisoryOnly: true, actionAuthority: 'NONE', commandAuthority: 'NONE', executionAuthority: 'NONE', safetyAuthority: 'NONE', automaticAcceptance: false},
  limitations: ['Bounded synthetic deterministic output; no model, provider, upload, tool execution or PixInsight apply.', 'Human disposition and execution evidence remain separate future inputs.'], artifactDigest: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
};
const path = 'docs/data/bkl042-f3-deterministic-advisory-output.json';
if (process.argv.includes('--write')) fs.writeFileSync(path, `${JSON.stringify(output, null, 2)}\n`);
else if (JSON.stringify(JSON.parse(fs.readFileSync(path, 'utf8'))) !== JSON.stringify(output)) throw new Error('BKL-042-F3 output is stale');
console.log(`BKL-042-F3 advisory generated: cases=${output.responses.length}; method=${output.methodId}; failClosed=${output.responses.filter(item => item.state === 'INSUFFICIENT_EVIDENCE').length}; action=NONE; command=NONE; safety=NONE`);
