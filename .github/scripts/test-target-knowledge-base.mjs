import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { validateTargetKnowledgeBase } from './verify-target-knowledge-base.mjs';

const fixture = JSON.parse(fs.readFileSync('docs/data/target-knowledge-base.json', 'utf8'));
const catalog = JSON.parse(fs.readFileSync('docs/data/scientific-session-catalog.json', 'utf8'));
const clone = x => structuredClone(x);
const rejects = (mutate, pattern) => { const x = clone(fixture); mutate(x); assert.match(validateTargetKnowledgeBase(x, catalog).join('\n'), pattern); };

test('accepted bounded fixture validates', () => assert.deepEqual(validateTargetKnowledgeBase(fixture, catalog), []));
test('rejects authority escalation', () => rejects(x => x.authority = 'authoritative', /authority must remain projection/));
test('rejects identity bound expansion', () => rejects(x => x.identities = [...x.identities, ...x.identities, ...x.identities], /identity bound exceeded/));
test('rejects relation bound expansion', () => rejects(x => x.relations = [...x.relations, ...x.relations, ...x.relations], /relation bound exceeded/));
test('rejects validated identity without Citation', () => rejects(x => x.identities[0].citation_refs = [], /validated identity requires Citation/));
test('rejects unresolved source session', () => rejects(x => x.identities[0].source_refs[0] = 'session:2099-01-01_2099-01-02', /unresolved source session/));
test('rejects downstream canonical-name mutation', () => rejects(x => x.identities[0].canonical_name = 'Fuzzy LDN', /canonical_name must preserve primary governed target name/));
test('rejects relation target mismatch', () => rejects(x => x.relations[0].target_key = 'dsg-target:m-27', /relation target conflicts with governed session target/));
test('rejects non-canonical citation locator', () => rejects(x => x.citations[0].locator.record_key = 'session_id', /canonical Session Catalog locator/));
test('rejects ungoverned derivation method', () => rejects(x => x.provenance_records[0].method_id = 'AI-FUZZY-MATCH', /ungoverned derivation method/));
test('rejects unresolved Citation', () => rejects(x => x.relations[0].citation_refs[0] = 'CIT-MISSING@1.0', /unresolved Citation/));
test('rejects unresolved Provenance', () => rejects(x => x.identities[0].provenance_refs[0] = 'PRV-MISSING@1.0', /unresolved Provenance/));
test('rejects premature SQM materialization without governed F3 reconciliation', () => rejects(x => x.relations[0].relation_type = 'TARGET_HAS_SQM_EVIDENCE', /bounded F2 fixture may materialize TARGET_HAS_SESSION only/));
