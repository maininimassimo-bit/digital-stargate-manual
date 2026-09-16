# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 7.1 |
| Baseline | 16/09/2026 |
| Stato | Current root bootstrap — F3-A3 exact four-resource platform applied and zero-drift verified; job unexecuted; no scientific execution authority |

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Memoria, conversazioni, roadmap visuali e dataset JSON non prevalgono sul repository corrente.

## 2. Sequenza obbligatoria di lettura

1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-15.md`
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-15.md`
4. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`
5. `docs/project/REPOSITORY_KNOWLEDGE_MAP.md`
6. `docs/project/BACKLOG.md`
7. `.github/roadmap/roadmap-source.json`
8. `docs/data/roadmap.json` — projection generata, non authority
9. `docs/project/TECHNICAL_DEBT.md`
10. `docs/project/DECISION_LOG.md`
11. `docs/project/DEVELOPMENT_WORKFLOW.md`
12. `docs/project/DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md`
13. `docs/project/CODING_STANDARDS.md`
14. `docs/project/RELEASE_PLAYBOOK.md`
15. `docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`
16. Package, ADR, review, evidence e componenti direttamente coinvolti.

Handover e baseline precedenti restano snapshot storici.

## 3. Verifica iniziale obbligatoria

Verificare branch, HEAD, PR, workflow, backlog, canonical roadmap, generated projection, closure/review/evidence e dependency readiness prima di modificare repository o runtime.

## 4. Principi non negoziabili

- repository as source of truth;
- projection mai authority implicita;
- Safety Authority fisica/locale indipendente;
- missing/unavailable evidence mai inventata;
- provenance `OBSERVED`, `DECLARED`, `SUGGESTED` sempre distinta;
- Citation, Provenance, semantic type, lifecycle e confidence preservati;
- nessuna claim di test, build, deployment o acceptance senza evidence reale.

## 5. Stato corrente

- BKL-037 — Session Comparison & Benchmarking: CLOSED / ACCEPTED;
- BKL-041 — Scientific Data Quality Score: CLOSED / ACCEPTED / POST-MERGE VERIFIED;
- BKL-046 — AI Post-Processing Assistant: CLOSED / ACCEPTED / POST-MERGE VERIFIED come capability deterministica advisory read-only con limitation;
- BKL-031 F1 — Source Discovery and Semantic Boundary: ACCEPTED / POST-MERGE VERIFIED;
- BKL-031 F2 — Machine-Readable Context/Source Contract and Bounded Fixtures: ACCEPTED / POST-MERGE VERIFIED via PR #188 and merge `7f861f7399079858c9744e69b6c773664b6b5b54`;
- BKL-031 F3 handoff and Solution Architecture: ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED; F3-A3 exact OCI publication and four-resource platform apply are evidence-complete and zero-drift verified, while artifact upload and scientific execution remain blocked;
- BKL-031 F3-A1 — Site Authority Contract: ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED via PR #193; acceptance reconciliation PR #194 merged as `1fd771632239cdca38d7527c55b974d805ffd1b9` with 9/9 workflows;
- BKL-031 F3-A2-D2 — first protected setup baseline is APPROVED; PR #202 merged as `bb11f25192200655427411a46a2e18560a5d9bec` and is post-merge verified;
- BKL-031 F3-A1-M1 — owner decisions and protected source authorization are complete;
- BKL-031 F3-A1-M2 — protected Site Authority DRAFT, schemas, validator and 51-case suite integrated/post-merge verified via PR #203;
- BKL-031 F3-A1-M3/M4 — exact-digest owner approval, protected receipt and unchanged APPROVED envelope integrated via PR #204, merge `e73b1aa631c41dff97b9e5ededb6d6be02a667d4`, with 10/10 post-merge workflows;
- BKL-031 F3-A1-M4 acceptance reconciliation — PR #205 merged as `d5f403bbe6a39731213c372cb22296324d10b03d` with 9/9 post-merge workflows;
- BKL-031 F3-A2-D3 — source, roles, separation and validity decisions are complete and integrated via PR #206;
- BKL-031 F3-A2-D4 — protected resolver-ineligible DRAFT, closed schemas, validator and 57-case suite are ACCEPTED / POST-MERGE VERIFIED via PR #207 and merge `e99e6b5ff5ea7247ee447a1c6c62dcaa479dee1b`;
- BKL-031 F3-A2-D5 — protected receipt and unchanged APPROVED envelope are ACCEPTED / POST-MERGE VERIFIED via PR #209 and merge `bc4307c2042a45985622044e11631421de5b2c3d`; exact-head CI passed 5/5, the suite passed 65/65 and post-merge workflows passed 7/7;
- Governance: `DSG-AEM-001` and `W-DSG-AEM-RULESET-001` are ACTIVE / POST-MERGE VERIFIED via PR #196 and merge `357a5edfbd39346b10a1a2d751018ff6d1dd208f`, with 9/9 workflows.

La closure BKL-046 non dichiara efficacia scientifica né produzione: `NOT_EVALUABLE_CURRENT_EVIDENCE`, `NOT_READY_FOR_PRODUCTION`, `aiModelImplemented=false`. Nessun modello/provider, automatic acceptance o PixInsight apply è autorizzato.

## 6. Sequenza governata

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 [F1/F2 ACCEPTED / F3 SA ACCEPTED / F3-A1+A2 REPOSITORY AUTHORITIES ACCEPTED / F3-A3 EXACT FOUR-RESOURCE PLATFORM APPLIED + ZERO DRIFT / JOB UNEXECUTED / ADR-010 PROPOSED / S10 UNAVAILABLE] -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 7. Authority e continuity

`BACKLOG.md` governa stato/priorità/dipendenze; `.github/roadmap/roadmap-source.json` governa la roadmap funzionale; `docs/data/roadmap.json` è generated projection. Closure, review, evidence e workflow sostengono le acceptance claim sui rispettivi exact SHA.

## 8. Safety boundary

Nessun portale, planner, comparison layer, quality score o AI è Safety Authority. Nessun device command, automatic remediation, go/no-go operativo o bypass degli interlock è autorizzato.

## 9. Punto di partenza operativo

PR #209 merged with expected-head control as `bc4307c2042a45985622044e11631421de5b2c3d` after 5/5 exact-head workflows, Documentation `ACCEPTED WITH OBSERVATION`, ARB `APPROVED WITH CONDITIONS — 99/100` and Release Quality `CONDITIONALLY READY FOR MERGE`. All 7 applicable post-merge workflows, including GitHub Pages, completed `SUCCESS`.

`BKL-031-F3-A2-D5` is ACCEPTED / POST-MERGE VERIFIED. The protected receipt is integrated, the historical DRAFT remains immutable and the separate `APPROVED` envelope preserves the assignment payload and digest. The repository authority resolves `AVAILABLE` only for authorized validated input with approved source authorities. S08 remains `UNAVAILABLE`; runtime S09 remains `UNAVAILABLE_CURRENT` because no adapter exists.

PR #212 integrated the F3-A3 decision-preparation package as `527b298094b07e5a00317e60cab3abefed7a5759`. PR #214 integrated the Google Cloud scaffolding, PR #215 integrated the ARB-213-MI02 state-lifecycle procedure, PR #217 integrated the immutable method profile and PR #218 added the reviewed Windows provider checksum. The authorized bootstrap plan for `main@af8b18f2f4e96642f453a30ead1e60e24ac8bd46` was applied with 27 additions, 0 changes and 0 destroys; bootstrap state is active in protected GCS. PR #219 promoted the permanent backend and the post-promotion remote-state, recovery and zero-drift checks satisfy ARB-213-MI02. PR #231 merged the exact OCI publication gate as `3abc8aa049262336fd5a814593cdfc521e4fc594`; run `35138527237` published the sole approved image and run `35138798214` verified the four-resource plan. PR #233 merged the exact apply gate as `af81b807c8f6d8861ede3ecf3ae9b34e66df7790`; run `35141947085` applied those four resources, verified zero drift and confirmed zero job executions with the kernel still absent. ADR-010 remains Proposed and S10 remains `UNAVAILABLE`.

## F3-A2-D4 acceptance checkpoint — 15/09/2026

The AI-assisted process-separated reviews recorded Documentation `ACCEPTED WITH OBSERVATION`, ARB `APPROVED WITH CONDITIONS — 99/100` and Release Quality `CONDITIONALLY READY`, with no Blocker or Major. The mandatory current step is explicit human approval or rejection of the exact protected assignment digest. No receipt, lifecycle promotion or runtime work may be inferred from CI, merge or the continuous mandate.


## F3-A2-D5 approval checkpoint — 15/09/2026

PR #209 is ACCEPTED / POST-MERGE VERIFIED at merge `bc4307c2042a45985622044e11631421de5b2c3d`. The protected receipt and separate unchanged `APPROVED` envelope are integrated; 65/65 executable cases and all 7 post-merge workflows passed. Repository-authority resolution is `AVAILABLE` only for authorized validated input. Runtime S09 remains `UNAVAILABLE_CURRENT`; no adapter, EAGLE operation, readiness/go-no-go, device command or Safety Authority change exists.


## F3-A3 program handoff — 15/09/2026

F3-A3 is the current documentation-only handoff. The specialist package must compare Astropy with pinned JPL data, Skyfield with pinned JPL BSP and JPL Horizons without presupposing a winner. It must prepare decision evidence for F3-OD04–F3-OD10 and stop before provider selection, dependency installation, scientific-data download, external calls, protected-site transmission, numeric threshold approval or runtime work. S10 remains `UNAVAILABLE`.


## F3-A3 decision-preparation checkpoint — 15/09/2026

Official candidate sources were refreshed. The conditional recommendation is local/offline primary evaluation, explicit local cross-check and Horizons only as a restricted validation reference unless privacy approval permits otherwise. ADR-010 remains `PROPOSED`; all spike cases are `NOT EXECUTED`; S10 remains `UNAVAILABLE`. The next mandatory gate after package integration is explicit owner disposition of F3-OD04–F3-OD10.

## F3-A3 partial owner decision and GCP scaffolding — 15/09/2026

Normative records are ADR-010, BKL-031-F3-A3-OD-2026-09-15 and BKL-031-F3-A3-INFRA-001. Continue only with repository review/CI. Stop before GCP bootstrap or apply, package/SPK/IERS acquisition, image push, Horizons traffic, protected-site processing or spike execution. The next owner action is F3-OD05 exact SPK selection. S10 remains `UNAVAILABLE`.

## F3-A3 F3-OD05 exact SPK decision — 16/09/2026

The owner approved `de442s.bsp` with SHA-256 `54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c`, verified NAIF MD5 `cc49327e06088124c0e39d8dde9f0b58`, exact kernel coverage, required SPICE chains, official provenance and the future private content-addressed URI. This closes F3-OD05 only at the identity/provenance decision level. No bucket creation, upload, Terraform operation, image build, Cloud Run execution, Horizons traffic, scientific calculation or protected-site use was authorized by that decision. At that checkpoint ARB-213-MI01 and ARB-213-MI02 remained open; both are now satisfied by their separately reviewed evidence.


## F3-A3 immutable method profile — 16/09/2026

`BKL-031-F3-A3-METHOD-PROFILE-001` records the approved F3-OD04–F3-OD10 method, scientific, time-data, privacy, hosting and request limits at SHA-256 `e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca`. Static preflight validates the exact bytes and rejects drift. The bootstrap-only plan/apply, protected remote state and MI02 post-promotion evidence exist. `BKL-031-F3-A3-CONTAINER-MANIFEST-001` now fixes the future base, dependency wheels and IERS identity as static evidence; no bytes were acquired and no image, platform plan/apply or scientific execution exists. Bounded artifact acquisition and container-build evidence are the next gate.

## F3-A3 ARB-213-MI02 bootstrap execution — 16/09/2026

The exact saved bootstrap plan SHA-256 `9bf2804ae697db1e5369e20f5594fbbaa0fa7fc202bc21e7290776b1e4c08d24` was applied under process-separated ARB and Release Quality authorization. State migrated to the private versioned GCS backend. Fail-closed incident `ARB-213-MI02-I01` stopped progression when Terraform advanced serial `23` to `24`; read-only inspection proved unchanged lineage and managed content. PR #219 merged the corrected rule and permanent backend as `6c6a9454f1f1f13f72b4ae5098c0f2475b537d60`; 7/7 post-merge workflows, remote lineage/content, generation `1789570006160390`, a read-only recovery candidate, absent residual lock and a zero-drift exit code `0` complete ARB-213-MI02. No platform or scientific operation is authorized.

## F3-A3 exact OCI publication and four-resource plan — 16/09/2026

PR #231 merged the main-only publication gate as `3abc8aa049262336fd5a814593cdfc521e4fc594` after exact-head review and CI. Run `35138527237` published and post-verified the sole registry image at manifest `sha256:de3331882e767c3a16fc479224da7c540385a6460e26df1ac73f8305676a0cce`. Separate run `35138798214` resolved that digest and verified exactly four create actions, zero changes and zero destroys while preserving empty platform state. The next gate is a separately reviewed exact saved-plan apply for those four resources. Artifact upload, scientific execution, external reference traffic, protected-site use and runtime activation remain blocked; ADR-010 is Proposed and S10 is `UNAVAILABLE`.

## F3-A3 exact platform apply — 16/09/2026

PR #233 merged the manual main-only apply gate as `af81b807c8f6d8861ede3ecf3ae9b34e66df7790` after 8/8 exact-head checks, ARB `APPROVED — 100/100`, Release Quality readiness and 5/5 post-merge workflows. WIF run `35141947085` applied only the verified saved plan with four additions, zero changes and zero destroys. The final state has the exact VPC, subnet, digest-pinned Cloud Run Job and deployer invoker binding, serial `3`, lineage `2be9b82b-88d3-888f-4fcd-dded2f74f7f3` and immediate zero drift. No job execution or kernel upload occurred. The next gate is separately reviewed acquisition and private content-addressed upload of the approved `de442s.bsp`; scientific execution, external reference traffic, protected-site use and runtime activation remain blocked. ADR-010 is Proposed and S10 is `UNAVAILABLE`.
