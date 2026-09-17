import fs from 'node:fs';
const path='.github/roadmap/roadmap-source.json';
const roadmap=JSON.parse(fs.readFileSync(path,'utf8'));
roadmap.target='Establish F8 current astronomical windows/altitude/transit/lunar geometry and explicit OTA/camera/filter/target suitability, then combine them with governed current weather supply in an explainable read-only planner ranking. Historical F4-C generalized validation request budget remains 2/2_EXHAUSTED and no provider request is authorized by F6 acceptance. F7 separately authorized and consumed one protected-site evaluation request (1/1_EXHAUSTED); that one-shot evidence does not authorize recurring traffic. Recurring provider refresh still requires separately governed operating authorization before BKL-031 closure. Preserve privacy, fail-closed freshness/missingness, BKL-032 readiness separation and local physical-interlock Safety Authority.';
fs.writeFileSync(path,`${JSON.stringify(roadmap,null,2)}\n`);
console.log('Retained historical F6 provider-authority markers while keeping F8 as current target.');
