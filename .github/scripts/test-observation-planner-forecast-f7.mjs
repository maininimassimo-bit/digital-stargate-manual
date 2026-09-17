import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
const authPath='governance/forecast-evidence/BKL031-F7-PROVIDER-REQUEST-AUTH-001.json';
if(!fs.existsSync(authPath)){ console.log('F7 authorization not materialized yet; negative authorization tests deferred.'); process.exit(0); }
const original=JSON.parse(fs.readFileSync(authPath,'utf8'));
function run(auth){ const dir=fs.mkdtempSync(path.join(os.tmpdir(),'bkl031-f7-')); const p=path.join(dir,'auth.json'); fs.writeFileSync(p,JSON.stringify(auth)); return spawnSync(process.execPath,['.github/scripts/observation-planner-forecast-f7-acquire.mjs','--preflight',`--auth=${p}`],{encoding:'utf8'}); }
assert.equal(run(original).status,0,'authorized F7 preflight must pass.');
for(const mutate of [a=>{a.maxProviderRequests=2;},a=>{a.protectedSiteUsed=true;},a=>{a.recurringTraffic=true;},a=>{a.productionUse=true;},a=>{a.runInitialisationUtc='2026-09-17T00:00Z';},a=>{a.location.latitudeDeg=42.5;}]){ const copy=structuredClone(original); mutate(copy); assert.notEqual(run(copy).status,0,'mutated authorization must fail closed.'); }
console.log('BKL-031 F7 authorization negative tests passed; no network request executed.');
