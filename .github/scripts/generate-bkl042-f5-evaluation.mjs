import fs from 'node:fs';
import crypto from 'node:crypto';

const reportPath = 'docs/data/bkl042-f5-real-evidence-evaluation.json';
const canonical = value => JSON.stringify(value, Object.keys(value).sort());
const digest = value => crypto.createHash('sha256').update(canonical(value)).digest('hex');

const f3 = JSON.parse(fs.readFileSync('docs/data/bkl042-f3-deterministic-advisory-output.json', 'utf8'));
const report = {
  schemaVersion: '1.0',
  evaluationType: 'BKL042_F5_REAL_EVIDENCE_EVALUATION',
  evaluationState: 'F5_TECHNICAL_GATE_EVALUATED',
  evaluationId: 'BKL042-F5-TECHNICAL',
  generatedAt: '2026-09-23T20:00:00Z',
  methodId: 'BKL042-F5-CLOSED-EVALUATION-1',
  sourceSnapshots: {
    f3Output: {
      path: 'docs/data/bkl042-f3-deterministic-advisory-output.json',
      contractType: f3.contractType,
      artifactDigest: f3.artifactDigest
    },
    f4Consumer: {
      page: 'docs/bkl042-advisory/index.md',
      mode: 'STATIC_READ_ONLY_CONSUMER',
      currentState: 'BOUNDED_SYNTHETIC_NOT_CURRENT'
    },
    realEvidence: {
      available: false,
      state: 'NOT_AVAILABLE_CURRENT_EVIDENCE',
      reasonCode: 'BKL042_REAL_ADVISORY_SOURCES_NOT_INTEGRATED'
    }
  },
  technicalGates: [
    { gateId: 'F5-T01-F3-CONTRACT', state: 'PASS', reasonCodes: [] },
    { gateId: 'F5-T02-F4-CONSUMER', state: 'PASS', reasonCodes: [] },
    { gateId: 'F5-T03-FAIL-CLOSED', state: 'PASS', reasonCodes: [] },
    { gateId: 'F5-T04-AUTHORITY-BOUNDARY', state: 'PASS', reasonCodes: [] },
    { gateId: 'F5-T05-REAL-EVIDENCE', state: 'NOT_EVALUABLE', reasonCodes: ['NO_CURRENT_GOVERNED_ADVISORY_SOURCE'] }
  ],
  outcomes: {
    technical: { state: 'ACCEPTED_READ_ONLY_WITH_LIMITATIONS', reasonCodes: ['F3_F4_BOUNDED_CAPABILITY_VERIFIED'] },
    scientific: { state: 'NOT_EVALUABLE_CURRENT_EVIDENCE', reasonCodes: ['NO_REAL_ADVISORY_COHORT', 'NO_GROUND_TRUTH'] },
    humanDecision: { state: 'NOT_AVAILABLE', reasonCodes: ['NO_OWNER_WITNESSED_DECISION_RECEIPT'] },
    production: { state: 'NOT_READY_FOR_PRODUCTION', reasonCodes: ['NO_MODEL_PROVIDER', 'NO_RUNTIME_AUTHORITY'] },
    capabilityOutcome: 'ACCEPTED_READ_ONLY_WITH_LIMITATIONS',
    closureRecommendation: 'CLOSE_DETERMINISTIC_CAPABILITY',
    aiModelImplemented: false
  },
  authority: {
    consumerMode: 'READ_ONLY',
    advisoryOnly: true,
    acceptanceAuthority: 'HUMAN_ONLY',
    actionAuthority: 'NONE',
    commandAuthority: 'NONE',
    executionAuthority: 'NONE',
    safetyAuthority: 'NONE',
    automaticAcceptanceAuthorized: false,
    pixInsightApplyAuthorized: false
  },
  limitations: [
    'F3/F4 prove only deterministic bounded behavior over synthetic fixture data.',
    'No current governed real-evidence advisory source is integrated for BKL-042.',
    'Scientific effectiveness, model quality and production readiness are not evaluated.',
    'Formal ARB, Release Quality and owner-witnessed acceptance remain a separate closure gate.'
  ]
};

report.evaluationDigest = digest(report);
const write = process.argv.includes('--write');
const expected = JSON.stringify(report, null, 2) + '\n';
if (write) fs.writeFileSync(reportPath, expected);
else if (fs.readFileSync(reportPath, 'utf8') !== expected) throw new Error('BKL-042-F5 evaluation drift detected. Run with --write.');
console.log(`BKL-042-F5 evaluation ${write ? 'written' : 'verified'}: technical=${report.outcomes.technical.state}; scientific=${report.outcomes.scientific.state}; authority=${report.authority.safetyAuthority}`);
