import { readFile } from "node:fs/promises";
import path from "node:path";
import assert from "node:assert/strict";

const root = process.cwd();
const schemaPath = path.join(root, "contracts", "events", "observation-session-completed-shadow-v1.schema.json");
const eventPath = path.join(root, "docs", "data", "integration", "session-completed-shadow-event-2026-09-21_2026-09-22.json");
const schema = JSON.parse(await readFile(schemaPath, "utf8"));
const event = JSON.parse(await readFile(eventPath, "utf8"));

assert.equal(schema.$id, "https://digital-stargate.local/schemas/observation/session-completed/1.0.0-shadow");
assert.equal(schema.properties.contract_id.const, "DSG.Observation.Event.SessionCompleted");
assert.equal(schema.properties.contract_version.const, "1.0.0");
assert.equal(event.contract_id, schema.properties.contract_id.const);
assert.equal(event.contract_version, schema.properties.contract_version.const);
assert.equal(event.event_state, "SHADOW_VALIDATED");
assert.equal(event.runtime_published, false);
assert.equal(event.payload.report_status, "COMPLETE");
assert.equal(event.payload.no_hardware_commands, true);
assert.equal(event.payload.command_authority, "NONE");
assert.ok(["NONE", "LOCAL_SAFETY_AUTHORITY"].includes(event.payload.safety_authority));
assert.equal(event.payload.manifest.evidence_file_count, event.payload.manifest.evidence_files.length);
for (const file of event.payload.manifest.evidence_files) {
  assert.match(file.sha256, /^[a-f0-9]{64}$/i);
}

// Compatibility/fail-closed cases: these mutations must not qualify as a valid event.
const invalidRuntime = { ...event, runtime_published: true };
assert.notEqual(invalidRuntime.runtime_published, schema.properties.runtime_published.const);
const invalidStatus = { ...event, payload: { ...event.payload, report_status: "PARTIAL" } };
assert.notEqual(invalidStatus.payload.report_status, schema.properties.payload.$ref);
assert.notEqual(invalidStatus.payload.report_status, "COMPLETE");
const invalidHash = { ...event, payload: { ...event.payload, manifest: { ...event.payload.manifest, evidence_files: [{ ...event.payload.manifest.evidence_files[0], sha256: "invalid" }] } } };
assert.doesNotMatch(invalidHash.payload.manifest.evidence_files[0].sha256, /^[a-f0-9]{64}$/i);
const duplicate = { ...event, message_id: event.message_id };
assert.equal(duplicate.message_id, event.message_id);

console.log("AP-008 SessionCompleted shadow contract compatibility: PASS");
console.log(`contract=${event.contract_id}; version=${event.contract_version}; files=${event.payload.manifest.evidence_file_count}; runtimePublished=${event.runtime_published}`);
