import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {buildChatCatalog} from './bkl042-chat-catalog.mjs';
test('Large telemetry never enters the bounded chat source; eligible facts preserved',()=>{
 const session={sessionId:'2026-10-16_2026-10-17',target:'NGC 281',integrationHours:3.67,raDeg:13,sourceMetricsPath:'private/path',guiding:{samples:'x'.repeat(1_100_000)}};
 const compact=JSON.parse(buildChatCatalog({sessions:[session]}));
 assert.deepEqual(compact.sessions,[{sessionId:session.sessionId,target:'NGC 281',integrationHours:3.67}]);
});
test('Growing eligible facts fail the generation budget rather than publishing an unreadable source',()=>{
 assert.throws(()=>buildChatCatalog({sessions:[{target:'x'.repeat(1_000_001)}]}),/byte budget/);
});
test('Committed compact projection matches all current catalog records',async()=>{
 const full=JSON.parse(await readFile('docs/data/scientific-session-catalog.json','utf8'));
 assert.equal(await readFile('docs/data/bkl042-session-catalog.json','utf8'),buildChatCatalog(full));
});
