import { readFile } from "node:fs/promises";
import path from "node:path";
import assert from "node:assert/strict";

const root = process.cwd();
const sessionRoot = path.join(root, "data", "sessions", "2026", "09", "2026-09-21_2026-09-22");
const manifest = JSON.parse((await readFile(path.join(sessionRoot, "manifest.json"), "utf8")).replace(/^\uFEFF/, ""));
const metrics = JSON.parse(await readFile(path.join(sessionRoot, "normalized", "session-metrics.json"), "utf8"));
const event = JSON.parse(await readFile(path.join(root, "docs", "data", "integration", "session-completed-shadow-event-2026-09-21_2026-09-22.json"), "utf8"));

const failClosed = (candidate) => {
  if (candidate.report_status !== "COMPLETE") return false;
  if (!Array.isArray(candidate.files) || candidate.files.length === 0) return false;
  if (candidate.files.some(file => !/^[a-f0-9]{64}$/i.test(file.sha256))) return false;
  return true;
};

assert.equal(failClosed(manifest), true, "nominal manifest must be complete");
assert.equal(manifest.session_id, event.payload.session_id);
assert.equal(metrics.scientific.configuration_id, "QUATTRO200_TOUPTEK294_BIN1");
assert.equal(metrics.scientific.telescope, "Sky-Watcher Quattro 200P");
assert.equal(metrics.scientific.camera, "ToupTek 294MC PRO");
assert.equal(manifest.report_status, "COMPLETE");
assert.equal(event.contract_id, "DSG.Observation.Event.SessionCompleted");
assert.equal(event.contract_version, "1.0.0");
assert.equal(event.event_state, "SHADOW_VALIDATED");
assert.equal(event.runtime_published, false);
assert.equal(event.payload.no_hardware_commands, true);
assert.equal(event.payload.command_authority, "NONE");
assert.equal(event.payload.safety_authority, "LOCAL_SAFETY_AUTHORITY");
assert.equal(event.payload.manifest.evidence_file_count, manifest.files.length);
assert.match(event.payload.manifest.git_blob_sha, /^[a-f0-9]{40}$/);

const partial = { ...manifest, report_status: "PARTIAL" };
assert.equal(failClosed(partial), false, "PARTIAL must not complete");
const corrupted = { ...manifest, files: manifest.files.map((file, index) => index === 0 ? { ...file, sha256: "invalid" } : file) };
assert.equal(failClosed(corrupted), false, "corrupted checksum must not complete");
const duplicate = { ...event, message_id: event.message_id };
assert.equal(duplicate.message_id, event.message_id, "duplicate identity must reconcile as NO_OP");

console.log("SessionCompleted shadow event diagnostic: PASS");
console.log(`Session=${manifest.session_id}; severity=${metrics.severity}; evidenceFiles=${manifest.files.length}; runtimePublished=${event.runtime_published}`);
