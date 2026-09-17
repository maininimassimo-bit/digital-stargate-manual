import fs from 'node:fs';

const read=p=>fs.readFileSync(p,'utf8');
const write=(p,c)=>fs.writeFileSync(p,c.endsWith('\n')?c:`${c}\n`,'utf8');
const replaceOne=(text,pattern,replacement,label)=>{
  const matches=typeof pattern==='string' ? text.split(pattern).length-1 : [...text.matchAll(new RegExp(pattern.source,pattern.flags.includes('g')?pattern.flags:`${pattern.flags}g`))].length;
  if(matches!==1) throw new Error(`${label}: expected exactly one match, got ${matches}`);
  return text.replace(pattern,replacement);
};

// Canonical roadmap source.
const roadmapPath='.github/roadmap/roadmap-source.json';
const roadmap=JSON.parse(read(roadmapPath));
if(roadmap.currentPackage!=='BKL-031') throw new Error('roadmap currentPackage is not BKL-031');
if(roadmap.nextMilestone!=='BKL-031 F5 explainable ranking method and read-only consumer') throw new Error(`unexpected previous milestone: ${roadmap.nextMilestone}`);
roadmap.projectStatus='BKL-031 F3/F4 evidence chain and F5 explainable ranking method/read-only consumer accepted and post-merge verified; F5 PR #273 merged as 777924e2638430f15bf717fa33dd71057751625a with 7/7 post-merge workflows; factor values remain synthetic EVALUATION evidence only; provider request budget 2/2 exhausted, acquisition path removed, zero protected-site use; no readiness/go-no-go, scheduling, automatic target selection, commands or Safety Authority; S10 production runtime unavailable';
roadmap.nextMilestone='BKL-031 F6 capability closure';
roadmap.target='Reconcile the complete BKL-031 F1-F5 evidence chain and close the capability without adding runtime behavior. Preserve the exhausted 2/2 provider budget, synthetic F5 evidence classification, BKL-032 readiness boundary, local physical-interlock Safety Authority and S10 production-runtime unavailability.';
const bkl=roadmap.streams.flatMap(s=>s.items??[]).find(i=>i.id==='BKL-031');
if(!bkl) throw new Error('BKL-031 roadmap item missing');
bkl.note='F3/F4 evidence chain and F5 explainable ranking/read-only consumer are Accepted/Post-Merge Verified. F5 merged via PR #273 as 777924e2638430f15bf717fa33dd71057751625a after exact-head ARB/RQ and completed 7/7 post-merge workflows. F5 values are synthetic method-validation evidence only. Provider budget remains 2/2 exhausted; no protected-site acquisition, readiness/go-no-go, scheduler, automatic target selection, commands, Safety Authority or S10 production runtime is authorized. F6 capability closure is next.';
if(!roadmap.milestones.some(m=>m.id==='M-BKL031-F5-ACCEPTANCE')) roadmap.milestones.push({
  id:'M-BKL031-F5-ACCEPTANCE', itemRef:'BKL-031', title:'BKL-031 F5 Explainable Ranking Acceptance', date:'2026-09-17',
  description:'PR #273 passed exact-head governance on dfda963e7e9d088282516200a6bd8bb64dd0dd1d, merged with expected-head control as 777924e2638430f15bf717fa33dd71057751625a and passed all 7 applicable post-merge workflows. The deterministic EVALUATION/NONE/READ_ONLY ranking method, synthetic validation fixture and read-only consumer are Accepted/Post-Merge Verified. Provider budget remains 2/2 exhausted; F6 capability closure is next.'
});
write(roadmapPath,JSON.stringify(roadmap,null,2));

// Backlog remains In Progress until F6 closure.
const backlogPath='docs/project/BACKLOG.md';
let backlog=read(backlogPath);
backlog=replaceOne(backlog,'| Versione | 5.31 |','| Versione | 5.32 |','backlog version');
backlog=replaceOne(backlog,/^\| BKL-031 \|.*$/m,'| BKL-031 | P1 | Observation Planner intelligente | In Progress | F3-C, F4-A/ADR-011, F4-B, F4-C, F4-D and F5 Accepted/Post-Merge Verified; F5 PR #273 merge `777924e2638430f15bf717fa33dd71057751625a`; provider budget 2/2 exhausted; no protected-site use; S10 unavailable | Execute F6 capability closure as a governance-only reconciliation of F1-F5; no new provider traffic, readiness/go-no-go, scheduling, automatic target selection, command path or Safety Authority | ADR-010; ADR-011; `BKL-031-F5-RANKING-001`; F5 acceptance; PR #273; merge `777924e2…`; evidence `350a7b9a…` |','BKL-031 backlog row');
write(backlogPath,backlog);

// Decision Log.
const decisionPath='docs/project/DECISION_LOG.md';
let decisions=read(decisionPath);
if(!decisions.includes('| DLG-049 |')){
  const lines=decisions.split('\n');
  const idx=lines.findIndex(l=>l.startsWith('| DLG-048 |'));
  if(idx<0) throw new Error('DLG-048 anchor missing');
  lines.splice(idx+1,0,'| DLG-049 | 17/09/2026 | Accettare F5 come metodo di ranking spiegabile deterministico EVALUATION/NONE/READ_ONLY con fixture a valori sintetici, decomposition completa e nessuna autorità operativa; PR #273 merge `777924e2638430f15bf717fa33dd71057751625a` verificato 7/7 post-merge. Promuovere esclusivamente F6 capability closure. | BKL-031 F5 | Accepted / Post-Merge Verified | `BKL-031-F5-RANKING-001`; `BKL-031-F5-EXPLAINABLE-RANKING-ACCEPTANCE-2026-09-17`; PR #273; exact head `dfda963e7e9d088282516200a6bd8bb64dd0dd1d`; merge `777924e2638430f15bf717fa33dd71057751625a` |');
  decisions=lines.join('\n');
}
write(decisionPath,decisions);

// Governance Center.
const indexPath='docs/project/index.md';
let index=read(indexPath);
if(!index.includes('BKL-031-F5-EXPLAINABLE-RANKING-ACCEPTANCE-2026-09-17.md')){
  const anchor='| [F4-D Sanitized Forecast Projection and Portal](../architecture/scientific-assets/BKL-031-F4-D-Sanitized-Forecast-Projection-and-Portal.md) | Accepted/Post-Merge Verified via PR #271 and merge `8f948ba9`; metadata-only EVALUATION/NONE/READ_ONLY projection and separate portal consumer; zero provider traffic |';
  index=replaceOne(index,anchor,`${anchor}\n| [F5 Explainable Ranking Method and Read-Only Consumer](../architecture/scientific-assets/BKL-031-F5-Explainable-Ranking-Method-and-Read-Only-Consumer.md) | Accepted/Post-Merge Verified via PR #273 and merge \`777924e2\`; synthetic EVALUATION/NONE/READ_ONLY method-validation ranking and read-only consumer |\n| [F5 Explainable Ranking Acceptance](BKL-031-F5-EXPLAINABLE-RANKING-ACCEPTANCE-2026-09-17.md) | 6/6 exact-head and 7/7 post-merge workflows; provider budget remains 2/2 exhausted |`,'project index F4-D anchor');
}
index=index.replace(/^- BKL-031 F4-A\/ADR-011.*$/m,'- BKL-031 F3/F4 evidence chain and F5 explainable ranking/read-only consumer are Accepted/Post-Merge Verified. F5 merged via PR #273 as `777924e2638430f15bf717fa33dd71057751625a` with 7/7 post-merge workflows. Factor values remain synthetic EVALUATION evidence only; provider budget remains 2/2 exhausted; F6 capability closure is next; S10 production runtime remains `UNAVAILABLE`.');
index=index.replace(/^`\.\.\. -> BKL-037 CLOSED.*$/m,'`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 [F1-F5 ACCEPTED / F6 CLOSURE NEXT / S10 PRODUCTION UNAVAILABLE] -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.');
write(indexPath,index);

// MkDocs navigation: add missing F4-D/F5 records after F4-C evidence reconciliation.
const navPath='mkdocs.yml';
let nav=read(navPath);
if(!nav.includes('BKL-031 F5 - Explainable Ranking Method and Read-Only Consumer:')){
  const anchor='          - BKL-031 F4-C - Acquisition Evidence Reconciliation: architecture/validation/BKL-031-F4-C-Acquisition-Evidence-Reconciliation-2026-09-17.md';
  nav=replaceOne(nav,anchor,`${anchor}\n          - BKL-031 F4-D - Sanitized Forecast Projection and Portal: architecture/scientific-assets/BKL-031-F4-D-Sanitized-Forecast-Projection-and-Portal.md\n          - BKL-031 F5 - Explainable Ranking Method and Read-Only Consumer: architecture/scientific-assets/BKL-031-F5-Explainable-Ranking-Method-and-Read-Only-Consumer.md\n          - BKL-031 F5 - Explainable Ranking Acceptance: project/BKL-031-F5-EXPLAINABLE-RANKING-ACCEPTANCE-2026-09-17.md`,'MkDocs F4-C anchor');
}
write(navPath,nav);

console.log('BKL-031 F5 acceptance reconciliation applied; F6 capability closure promoted as next milestone.');
