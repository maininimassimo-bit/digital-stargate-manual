# Repository Knowledge Map

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-KM-001 |
| Versione | 6.7 |
| Stato | Active |
| Data | 05/10/2026 |
| Root bootstrap | `AI_BOOTSTRAP.md` |
| Current governed package | BKL-043 F4 lifecycle pending; BKL-049 archive closed; local PixInsight AI pilot; S10 production runtime `UNAVAILABLE` |

## 1. Scopo

Mappa domini, authority, projection e percorsi di conoscenza. Non sostituisce le fonti canoniche.

## 2. Continuity hierarchy

1. `AI_BOOTSTRAP.md`;
2. `docs/project/HANDOVER_2026-10-05-BKL049-PIXINSIGHT-AI.md`;
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-10-05.md`;
4. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`;
5. questo Knowledge Map;
6. `DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md`;
7. `BACKLOG.md`;
8. canonical roadmap source;
9. generated roadmap projection;
10. Technical Debt, Decision Log, Development Workflow, Coding Standards e Release Playbook;
11. AMP-002 e package/review/evidence coinvolti.

Handover e baseline precedenti restano snapshot storici e non prevalgono sulla baseline corrente.

Riferimenti di continuità storici mantenuti per la verificabilità delle capability già accettate: `HANDOVER_2026-09-21-AP-007.md`, `CURRENT_TECHNICAL_BASELINE_2026-09-21.md`, F8 is Accepted / Post-Merge Verified, `BKL-032 Session Readiness / Go-No-Go Decision Support` e `2/2_EXHAUSTED`. Questi riferimenti non definiscono il package corrente né sostituiscono i documenti del 05/10/2026.

## 2.1 Current continuity reconciliation

AP-007 è Accepted with conditions come architecture baseline e AP-008 è chiuso nel suo perimetro bounded read-only. La catena corrente è `AI_BOOTSTRAP.md` → `HANDOVER_2026-10-05-BKL049-PIXINSIGHT-AI.md` → `CURRENT_TECHNICAL_BASELINE_2026-10-05.md` → roadmap source → BKL-043 F1/F2/F3/F4 evidence → Traceability Register. BKL-043 resta corrente: F4 attende lifecycle e accettazione finale secondo BKL-043-F4-STATUS-2026-10-01. BKL-049 archivio è chiusa; il pilota locale è una nuova estensione autorizzata.

## 3. Authority / projection map

Authority: repository, Architecture Package/ADR, backlog, canonical roadmap, registri, closure/review/workflow/evidence.

Projection: roadmap JSON, cataloghi/read model scientifici, Observatory Status, Timeline/Replay, Equipment Performance, Session Comparison e Analytics Center.

Ogni consumer preserva source locator, semantic type, lifecycle, Citation, Provenance, quality e completeness dove previsti.

## 4. Accepted foundation

BKL-015, BKL-044, BKL-035, BKL-040, BKL-038, BKL-039, BKL-045, BKL-037, BKL-041 e BKL-046 sono accepted. AP-013 resta authority degli asset; AP-014 resta catalog/synchronization boundary.

## 5. BKL-037 closed baseline

Session Comparison è read-only/descriptive-only. Confronta esclusivamente dimensioni/unità/provenance compatibili, conserva exclusions e non crea ranking, score, threshold, recommendation o authority.

## 6. Current accepted capability baseline

BKL-046 è CLOSED / ACCEPTED / POST-MERGE VERIFIED come capability deterministica advisory read-only tramite PR #181 e merge `3d680dd3a05c70b2a4654c4187c293e36b0af4a7`. Scientific effectiveness resta `NOT_EVALUABLE_CURRENT_EVIDENCE`, production `NOT_READY_FOR_PRODUCTION`, `aiModelImplemented=false`; nessun apply path o Safety Authority è autorizzato.

BKL-031 è **CLOSED / ACCEPTED / POST-MERGE VERIFIED** tramite PR #301 e merge `4a509d574a004fe7fb72bc6c678c9e7f71fe821f`. F1/F2, F3-A1/A2/A3/B/C, F4-A/B/C/D, F5/F6/F7/F8 e F9 sono accettati; F3-C are Accepted / Post-Merge Verified; F4-A and ADR-011 are Accepted / Post-Merge Verified; F8 is Accepted / Post-Merge Verified. F9 ha verificato il refresh repeatable MeteoHub, astronomia della notte corrente, suitability setup/target, ranking esplicabile e pagina pubblica di Manciano. Budget provider storico `2/2_EXHAUSTED`; budget sito protetto `1/1_EXHAUSTED`; Recurring provider traffic is not authorized. Il budget monetario resta €0, senza limite giornaliero imposto dal workflow, fail-closed e GRIB effimeri senza retention. BKL-032 conserva la readiness/go-no-go authority; local physical interlocks remain Safety Authority; S10 production runtime is `UNAVAILABLE`; il planner resta read-only/advisory senza scheduler, selezione automatica, device command o Safety Authority.

BKL-042 è CLOSED / ACCEPTED come retrieval advisory bounded read-only. BKL-043 è il package corrente: F1 source/population discovery e F2 two-plane design sono completati; F4 attende lifecycle e accettazione finale secondo lo stato del 1 ottobre; la presente revisione non ne estende il runtime.

## 7. BKL-032 closed baseline

BKL-032 is closed through PR #304 merge `7e38453b2e499fe577efa0231aeb7bb06329016e`. The accepted capability is a deterministic, read-only evaluator with versioned contracts, owner-approved thresholds and fail-closed missingness. Live source/transport acceptance and public runtime GO remain outside the closure. The governed handoff is **BKL-032 Session Readiness / Go-No-Go Decision Support** → **BKL-036 Observatory Health Score**.

## 8. BKL-036 closure state

BKL-036 is **CLOSED / ACCEPTED / POST-MERGE VERIFIED** for its bounded evidence and live read-only gates. It does not transfer command, remediation, scheduler or Safety Authority. BKL-031, BKL-032 and local physical interlocks remain separate authorities. Closure records are `docs/project/BKL-036-CLOSURE-2026-09-19.md` and `docs/project/BKL-036-F5-CLOSURE-2026-09-23.md`.

## 9. Roadmap sequence

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 CLOSED / ACCEPTED -> BKL-032 CLOSED / ACCEPTED -> BKL-036 CLOSED -> BKL-033 CLOSED -> BKL-034 CLOSED -> BKL-042 CLOSED / ACCEPTED -> BKL-043 CURRENT -> BKL-049 PLANNED -> BKL-050 PLANNED`.

## 10. CI/CD e publishing

Workflow e deployment sono evidence solo per l’exact SHA verificato. Generated projection non è authority.

## 11. Safety boundary

Nessun consumer analytics, comparison, scoring, planner o AI può comandare apparati, autorizzare remediation, produrre readiness/go-no-go come authority o sostituire gli interlock fisici. Le coordinate esatte del sito restano protette e non devono essere pubblicate nelle projection.

## 12. Registro revisioni

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 04/08/2026 | Prima repository knowledge map |
| 2.0 | 08/09/2026 | Continuity e knowledge foundation |
| 2.1 | 10/09/2026 | BKL-037 current |
| 2.2 | 10/09/2026 | BKL-037 closed/accepted e BKL-041 current |
| 2.3 | 11/09/2026 | BKL-041 closed/accepted e BKL-046 F1 current |
| 2.4 | 11/09/2026 | BKL-046 F1 accepted e F2 current |
| 2.5 | 11/09/2026 | BKL-046 F2 accepted e F3 current |
| 2.6 | 11/09/2026 | BKL-046 F3 accepted e F4 current |
| 2.7 | 12/09/2026 | BKL-046 F4 accepted/post-merge verified e F5 design current |
| 2.8 | 13/09/2026 | BKL-046 closed/accepted/post-merge verified e BKL-031 F1 current |
| 2.9 | 14/09/2026 | BKL-031 F1 accepted/post-merge verified; F2 current handoff only |
| 3.0 | 14/09/2026 | BKL-031 F2 accepted/post-merge verified; successor decision pending |
| 3.1 | 14/09/2026 | BKL-031 F3 promoted as current handoff only |
| 3.2 | 14/09/2026 | BKL-031 F3 Solution Architecture review candidate |
| 3.3 | 14/09/2026 | BKL-031 F3 Solution Architecture AI-assisted ARB/RQ complete; merge decision pending |
| 3.4 | 14/09/2026 | BKL-031 F3 Solution Architecture accepted with conditions; implementation decision pending |
| 3.5 | 15/09/2026 | PR #192 closure integrated; F3-A1 Site Authority Contract review candidate current |
| 3.6 | 15/09/2026 | PR #193 F3-A1 merged/post-merge verified; Acceptance Reconciliation current |
| 3.7 | 15/09/2026 | PR #194 F3-A1 reconciliation merged/post-merge verified; F3-A2 handoff current |
| 3.8 | 15/09/2026 | PR #195 F3-A2 handoff post-merge verified; DSG-AEM-001 active; detailed contract next |
| 3.9 | 15/09/2026 | PR #196 mandate post-merge verified; F3-A2 detailed contract and validation plan current |
| 4.0 | 15/09/2026 | PR #197 F3-A2 contract accepted/post-merge verified; concrete authority decision gate current |
| 4.1 | 15/09/2026 | ADR-009 authority model owner-authorized; first protected baseline payload remains DRAFT pending exact-digest approval |
| 4.2 | 15/09/2026 | PR #199 authority/DRAFT integrated and post-merge verified; exact-digest owner gate current |
| 4.3 | 15/09/2026 | Exact-digest owner approval recorded; PR #201 receipt and `APPROVED` lifecycle envelope under review |
| 4.4 | 15/09/2026 | PR #201 merged/post-merge verified; F3-A1-M1 Site Authority owner decision gate current |
| 4.5 | 15/09/2026 | PR #202 baseline verified; F3-A1-M1 decisions complete; F3-A1-M2 protected DRAFT review candidate and exact-digest approval next |
| 4.6 | 15/09/2026 | PR #204 Site Authority approval accepted/post-merge verified; F3-A2-D3 CurrentSetupAssignment owner decision gate current |
| 4.7 | 15/09/2026 | PR #205 reconciliation verified; F3-A2-D3 owner decisions complete and F3-A2-D4 DRAFT handoff next |
| 4.8 | 15/09/2026 | PR #207 D4 protected DRAFT accepted/post-merge verified; mandatory human exact-digest approval next |
| 4.9 | 15/09/2026 | Exact-digest assignment approval received; PR #209 receipt/promotion review candidate with 65/65 implementation tests |
| 5.0 | 15/09/2026 | PR #209 D5 accepted/post-merge verified; repository authority AVAILABLE; runtime adapter absent; successor selection current |
| 5.1 | 15/09/2026 | PR #210 D5 reconciliation accepted/post-merge verified; F3-A3 documentation-only handoff current; no provider selected |
| 5.2 | 15/09/2026 | PR #211 handoff integrated/post-merge verified; F3-A3 Solution/ADR/validation decision-preparation review candidate |
| 5.3 | 17/09/2026 | PR #258 F3-A3 scientific acceptance integrated/post-merge verified; ADR-010 accepted; F3-B authorized repository-only |
| 5.4 | 17/09/2026 | F3-B method/request/evidence schemas, bounded fixture and 34-case validator suite prepared for exact-head acceptance |
| 5.8 | 17/09/2026 | PR #263 F4-A source contract integrated and post-merge verified; ADR-011 accepted; F4-B machine-readable contracts promoted with zero provider traffic |
| 5.9 | 17/09/2026 | F4-B three-schema contract, synthetic TEST/NONE fixture and 24-case fail-closed validator prepared with zero provider traffic |
| 6.0 | 17/09/2026 | PR #265 F4-B integrated and post-merge verified; 26/26 tests and 14/14 workflows; F4-C acquisition-gate preparation promoted |
| 6.1 | 17/09/2026 | F8 Accepted/Post-Merge Verified via PR #279; continuity riallineata a handover/baseline 17/09 e F9 repeatable current-night planner closure promosso come unico successore |
| 6.3 | 25/09/2026 | Continuità riallineata a BKL-042 closed/accepted e BKL-043 F3/F4 preparation; nessun runtime BKL-043 autorizzato |

Le sezioni di checkpoint seguenti sono snapshot storici. Eventuali formulazioni come “current” o “next” valgono al momento del relativo checkpoint e non prevalgono sulla baseline corrente definita nelle sezioni 2, 6 e 7.

## F3-A2-D4 acceptance checkpoint — 15/09/2026

PR #207 merged as `e99e6b5ff5ea7247ee447a1c6c62dcaa479dee1b` after 5/5 exact-head workflows and completed 7/7 post-merge workflows. Closed schemas, exact-reference binding, canonical identity, fail-closed resolution, privacy enforcement and 57/57 cases are integrated. No assignment approval, runtime adapter or public protected projection exists. The current mandatory transition is human exact-digest approval or rejection.

## F3-A2-D5 approval checkpoint — 15/09/2026

PR #209 is ACCEPTED / POST-MERGE VERIFIED at merge `bc4307c2042a45985622044e11631421de5b2c3d`. It retains the historical DRAFT, preserves the assignment payload/digest, integrates the protected receipt and resolves `AVAILABLE` only in repository authority for authorized validated input with approved sources. The 65-case suite and all 7 post-merge workflows passed. Runtime S09 remains `UNAVAILABLE_CURRENT`; adapter, EAGLE and Safety Authority are outside scope.

## F3-A3 scientific acceptance gate

F3-A3 owner decisions F3-OD04–F3-OD10, immutable method profile, exact runner, platform and kernel evidence are complete. Main-only run `35189574972` executed the remediated runner once: 8 synthetic vectors, 17/17 metrics, repeatability and transit passed. One create-only private evidence object was verified at raw SHA-256 `483794c9a8a373e8aff2f0dd2ab0f6342826c9bd210beeebcf92e744fad72494`. ADR-010 is Accepted for repository method authority. Further scientific execution, external-reference traffic, protected-site use and runtime remain unauthorized; S10 remains `UNAVAILABLE`.

## F3-A3 decision-preparation package

Authority remains the repository and accepted ADR-010. Official-source observations remain evidence inputs. The accepted profile selects the exact local primary, shared-SPK implementation cross-check, kernel, thresholds and host used by the passed campaign. No external reference, protected-site calculation or runtime is selected. F3-B may now materialize the source-neutral request/evidence contracts and validator.

## F3-B contracts and validator acceptance

F3-B materializes separate method-profile, request and evidence schemas plus one bounded synthetic fixture. The canonical contract digest is `b06932edb860cc4062b45d75b62e7874c3a327a4b4dbfd0b8cb70bdf115cd1f1`; 34 fail-closed and privacy tests passed locally and in governed CI. The fixture is `TEST` / `authority=NONE`, and the public projection omits protected coordinates and internal digests. Exact-head review, expected-head merge and all 11 applicable post-merge workflows passed. F3-C adapter, runtime activation, protected-site calculation and external-reference traffic remain unimplemented and separately gated.


## 30/09/2026 — BKL-049 F0 in parallelo

BKL-043 resta corrente e aperta. L’Owner autorizza BKL-049 F0 limitatamente a ricerca SDK/licenze e fattibilità non invasiva, su branch dedicato. [Dossier e gate aperti](../architecture/assessments/BKL-049-F0-SDK-Licensing-Feasibility-Dossier.md). Nessuna closure F0, promozione F1 o estensione di autorità runtime.


## 30/09/2026 — BKL-049 scope aggiornato: archivio parziale e gallery

La successiva decisione esplicita dell’Owner sostituisce il requisito di cattura automatica integrale: archiviare le history disponibili, accettando lacune visibili, **con collegamento obbligatorio alla corretta immagine/versione nella gallery**. Nessuna associazione per supposizione. Il [piano aggiornato](../architecture/assessments/BKL-049-PixInsight-Native-Workflow-Capture-Module-Plan.md) prevale sulle descrizioni native precedenti. Baseline attuale dichiarata: PixInsight 1.9.5 build 1706; SYN-01/SYN-02 autorizzati separatamente hanno fornito evidenze circoscritte. F0 resta aperta per review del nuovo scope; F1 non promossa, BKL-043 corrente e autorità scientifiche invariate.


## 2026-09-30 — BKL-049 F0 accepted after review and delivery

La [riconciliazione F0](BKL-049-F0-ACCEPTANCE-2026-09-30.md) registra PR #445, merge `fc281eb80342c746303c58c2d2a8f61d134a5f5b`, review ARB/RQ e 17/17 workflow post-merge SUCCESS con Pages verificato. F0 è accettata nel perimetro archivio parziale con collegamento obbligatorio immagine/versione–workflow. Questa decisione successiva supera gli stati F0 OPEN precedenti; F1 è pronta per progettazione dettagliata, non ancora accettata. BKL-049 resta aperta e BKL-043 corrente. Nessuna funzionalità gallery reale, codice di produzione o autorità runtime viene dichiarata completata.

## Riconciliazione corrente — 2026-10-05

Le sezioni datate precedenti conservano l’evidenza storica. Il [nuovo handover](HANDOVER_2026-10-05-BKL049-PIXINSIGHT-AI.md) e la [baseline corrente](CURRENT_TECHNICAL_BASELINE_2026-10-05.md) prevalgono per lo stato: BKL-043 F4 lifecycle pendente; BKL-049 archivio chiuso, procedura foto/workflow e importer 1.2 consegnati; ultima M27 pubblicata con 80 processi e 16 associazioni dichiarate. Il [pilota locale BKL-049-EXT-PIAI](../architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md) aggiunge elaborazione file su copie del PC Owner. Worker remoto, modello API e pubblicazione automatica non sono implementati. Safety Authority e dispositivi restano invariati.

Versione 6.4 — 05/10/2026: nuova continuità M27 e pilota locale; snapshot storici conservati.

P2 locale implementato in `tools/pixinsight/local_pilot/worker.py` e `executor.jsh`; procedura in README, test sintetici Node/Python e [ricevuta nativa minimizzata](evidence/BKL-049-PIAI-P2-2026-10-05.json). Il journal e i checkpoint sono privati. P3 non lineare e remoto rimangono pianificati.

### 2026-10-05 — P3 implementation

P2 delivered #480. P3 adds `quality.py`, synthetic pixel/coordinator/native-boundary tests, the fixed `M27_LRGB_NONLINEAR_V1` executor and a private journal of masks/secondary outputs. See the current plan and handover for native/visual evidence and delivery status. P4–P6 remain planned; the available-history importer contract is unchanged.

P3 native technical/visual trial completed; [minimized evidence](evidence/BKL-049-PIAI-P3-2026-10-05.json): 29 actions, 15 checkpoints, finite normalized final pixels, unchanged originals, native cancel/selection/replay rejection and full-field/100% comparison. Prior published M27 retains stronger internal contrast; Owner acceptance remains required. Available History: 13 views, 47 steps, 82 instances, imported as data without promoting completeness/execution classifications. Exact-head CI/review and post-merge delivery are tracked on the PR; no remote/provider/portal activation.

Consegna P3 completata: PR #481, head `ce819ea192a30522f2c168631a0c1b05f77adfd9`, merge `342a169dbc87433da971f1660a239e6dc5a6b343`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Supera le indicazioni storiche di consegna P3 ancora pendente; acceptance scientifica Owner aperta.

## Snapshot precedente — P4 candidato prima dell’approvazione

L’Owner sceglie `SESSION_ASSISTED`: assistente di questa sessione, zero nuove chiamate API IA a pagamento. Implementati coda privata con CAS/backup, identità persistente senza scadenza o riassegnazione offline, autenticazione distinta Google Owner/credenziale worker e adapter PC HTTPS in uscita con allowlist locale. Preparazione una sola volta, retry di messaggi identici, cancellazione P2, raccolta solo dopo conferma di arresto nativo, recupero conservativo. Nessun avvio automatico PixInsight o modello cloud autonomo.

[Pacchetto operativo e proposta concreta](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/main/infrastructure/pixinsight-pilot): servizio Cloud Run separato, identità/registry e due bucket privati per soli stati, min=0/max=1, 1 CPU/512 MiB. Nuova infrastruttura potenzialmente a pagamento e credenziale dedicata richiedono approvazione prima di creazione/attivazione. Nessuna risorsa o credenziale creata, nessun OAT cloud/Google/TLS nativo dichiarato. Test persistenti sintetici e HTTP loopback reali restano distinti da runtime operativo. P4 resta aperta per attivazione; P5/P6 e acceptance Owner restano successivi. Archivio/M27 pubblicata e autorità dispositivi/Safety invariati.

## Aggiornamento corrente — P4 cloud autorizzato e attivato

L’Owner ha approvato le risorse e la credenziale dedicate il 5 ottobre. PR #482 consegnata: head `875cc375a130268b4be98b28ad11a7c8c11e4552`, merge `e000a3b96c980c22d47967e26fb5e79633c3d249`; 16 CI exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate.

Il nuovo servizio Cloud Run è attivo su immagine verificata per digest, con identità/registry e due bucket privati versionati separati. Credenziale PC generata e protetta con Windows User DPAPI, solo digest al server. Collegamento PC HTTPS reale e dieci controlli HTTP PASS; nessuna nuova API IA, porta PC in ingresso, esecuzione nativa automatica o pubblicazione. La [ricevuta di attivazione](evidence/BKL-049-PIAI-P4-ACTIVATION-2026-10-05.json) e il [runbook](PIAI-P4-CLOUD-ACTIVATION-2026-10-05.md) distinguono prove reali e gate ancora aperti.

Autenticazione Google Owner e prova nativa tramite trasporto non ancora eseguite. Pagina diagnostica P4 separata dalla navigazione principale: prova sintetica crea/legge/annulla, credenziale solo in memoria, destinazione approvata fissata per digest. Non abilita P5 né comandi scientifici dal portale. P4 OAT/P5/P6 e acceptance Owner restano aperti. M27 pubblicata e autorità dispositivi/Safety invariate.
