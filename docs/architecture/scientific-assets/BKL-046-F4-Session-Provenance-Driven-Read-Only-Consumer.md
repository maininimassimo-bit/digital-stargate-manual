# BKL-046 F4 — Session/Provenance-Driven Read-Only Consumer

| Campo | Valore |
|---|---|
| Identificativo | BKL-046-F4 |
| Stato | Proposed |
| Versione | 1.0 |
| Data | 11/09/2026 |
| Package | BKL-046 — AI Post-Processing Assistant for PixInsight |
| Baseline F3 | PR #169, merge `8339aecf0b6b7fa19396561b20253c0411fd7ee7` — Accepted |
| Baseline repository | `ec4eb991bd9e20bcd34b00e111400a5ac07fd750` |
| Authority | Session/provenance-driven, deterministic, read-only, human-only and non-Safety |

## 1. Purpose

Definire la soluzione implementabile che porta il demonstrator F3 dalle fixture sintetiche a una projection persistita e a un consumer portale alimentati da sessioni e provenance PixInsight reali già governate. F4 deve aggiornarsi automaticamente dopo ogni nuova sessione scientifica importata, pubblicare atomicamente i derivati e rifiutare come correnti dati stale, alterati, ambigui o non correlabili.

F4 non introduce inferenza AI, qualità scientifica calibrata o ottimizzazione automatica. Espone soltanto gli esiti deterministici delle regole F3 e le relative limitation, citation e source state.

## 2. Scope

F4 comprende:

- population session-driven dal catalogo canonico AP-014;
- discovery bounded della provenance BKL-045 repository-governed;
- correlazione esatta e fail-closed fra sessione, sidecar e processing projection;
- adapter real-input verso il contratto F3 pre-decisione;
- projection full-catalog deterministica, versionata e digest-protected;
- consumer portale accessibile, read-only e freshness-verified;
- integrazione nel workflow automatico post-import e nel suo retry path;
- test positivi, negativi, idempotenza, anti-tampering e gate CI dedicato.

Restano esclusi:

- LLM, machine learning, prompt runtime, RAG, vector store o selezione provider;
- upload, copia o lettura dei file immagine;
- suggestion di parametri numerici o claim di ottimizzazione scientifica;
- Human Decision Receipt generato automaticamente;
- PixInsight apply, script execution, image mutation o remediation;
- device command, modifica del runtime osservativo o Safety Authority;
- calibrazione, confidence numerica, production readiness e closure F5.

## 3. Architectural drivers

| Driver | Conseguenza architetturale |
|---|---|
| Aggiornamento dopo ogni import | un solo orchestratore canonico; generator inserito sia nel primo passaggio sia nel retry `regenerate()` |
| Atomicità | projection F4 nello stesso commit governato del catalogo e degli altri derivati |
| Missingness reale BKL-045 | `UNAVAILABLE`/`PARTIAL` restano espliciti e producono esiti F3 fail-closed |
| No stale data | catalog digest, source-set digest, session identity e projection digest verificati prima del rendering |
| Authority separata | AP-013 governa asset/provenance; AP-014 governa catalogo/reconciliation; BKL-046 è solo advisory projection |
| UX verificabile | stato, rationale, limitation e source citation visibili insieme; nessun controllo mutativo |
| Rollback sicuro | artefatti additivi; rimozione di consumer e generator senza migrare catalogo o provenance |

## 4. Current state

- F2 definisce Recommendation e Human Decision Receipt come contratti separati.
- F3 genera deterministicamente due Recommendation su una fixture bounded e sintetica.
- `docs/data/scientific-session-catalog.json` è il catalogo canonico pubblicato delle sessioni.
- `.github/workflows/analyze-session-automatic.yml` rigenera i derivati dopo un nuovo `data/sessions/**/manifest.json` e ripete l'intera generazione dopo ogni riallineamento a `main`.
- BKL-045 espone sidecar reali e `buildPixInsightProvenanceReadModel`, preservando evidence class e completeness senza inferenza.
- l'evidence reale BKL-045 accettata ha processing history `UNAVAILABLE` e zero step osservati o dichiarati.
- non esistono ancora schema, projection persistita o pagina consumer BKL-046 F4.

## 5. Target state and solution model

```mermaid
flowchart TD
  I["Session import COMPLETE"] --> C["AP-014 canonical catalog"]
  P["BKL-045 provenance evidence"] --> A["Bounded correlation adapter"]
  C --> A
  A --> G["F3 deterministic rules"]
  G --> J["F4 atomic projection"]
  J --> U["Freshness-verified portal"]
```

| Layer | Componente proposto | Responsabilità |
|---|---|---|
| External evidence | catalogo AP-014 e sidecar/read model BKL-045 | fatti e provenance già governati |
| Infrastructure adapter | F4 source discovery/correlation | discovery bounded, canonicalizzazione e exact-match |
| Application | projection generator | orchestration full-catalog, ordinamento, idempotenza e pubblicazione |
| Domain policy | regole F3 accettate | valutazioni chiuse senza side effect o nuova authority |
| Contract | schema/projection F4 | envelope persistito, identity snapshot, limitation e digest |
| Presentation | core validator e pagina portale | verifica client-side e rendering accessibile fail-closed |

Il Domain policy non dipende da browser, filesystem, workflow o GitHub. Gli adapter trasformano input governati nei tipi F2/F3 senza alterare source evidence o completare campi mancanti.

## 6. Source authority and eligibility

### 6.1 Session population

`docs/data/scientific-session-catalog.json` determina l'intera popolazione F4. Ogni record della projection deve corrispondere a un solo `sessionId` del catalogo; nessuna sessione può essere aggiunta da pathname, nome target o provenance non riconciliata.

### 6.2 PixInsight provenance

Sono eleggibili soltanto sidecar BKL-045 che:

1. hanno schema e authority supportati;
2. sono validabili dal contratto BKL-045;
3. mantengono `actionAuthority=NONE`;
4. hanno un `observationContext.sessionId` esatto;
5. se associati a una processing projection AP-014, superano la correlazione già governata e hanno `acceptanceAuthority=false`.

La discovery usa un pattern repository-relative chiuso e restituisce path ordinati. Non accede a directory locali PixInsight, EAGLE, OneDrive o file immagine.

### 6.3 Correlation rules

| Condizione | Stato F4 |
|---|---|
| una sola provenance eleggibile correlata esattamente | `PROVENANCE_MATCHED` |
| nessuna provenance correlata | `PROVENANCE_UNAVAILABLE` |
| più candidate per la stessa identità senza regola canonica | `CORRELATION_AMBIGUOUS` |
| sidecar/projection discordanti | `CORRELATION_INVALID` |
| evidence stale, alterata o con authority non ammessa | reject / `SOURCE_INVALID` |

Target name, data, directory e similarità testuale non autorizzano correlazioni implicite. Un record senza provenance resta pubblicabile soltanto come fail-closed, mai come recommendation validated.

## 7. F4 projection contract

Artefatti previsti per l'implementazione:

| Artefatto | Responsabilità |
|---|---|
| `docs/contracts/ai-post-processing-assistant-f4.schema.json` | schema chiuso della projection full-catalog |
| `.github/scripts/ai-post-processing-advisory-projection.mjs` | discovery, correlation, mapping e builder deterministico |
| `.github/scripts/generate-ai-post-processing-advisory-projection.mjs` | comandi `--write`, `--check`, `--print` |
| `docs/data/ai-post-processing-advisory-projection.json` | projection persistita e pubblicata |
| `docs/javascripts/ai-post-processing-assistant-core.mjs` | contract, authority, freshness e digest validation |
| `docs/javascripts/ai-post-processing-assistant.js` | consumer UI senza capability mutative |
| `docs/ai-post-processing-assistant/index.md` | pagina portale F4 |
| `.github/scripts/verify-ai-post-processing-advisory-projection.mjs` | drift, workflow e persisted-projection verification |
| `.github/scripts/test-ai-post-processing-advisory-projection.mjs` | determinismo, correlation, missingness e anti-tampering |
| `.github/scripts/test-ai-post-processing-assistant-consumer.mjs` | freshness, authority e browser failure paths |
| `.github/workflows/bkl-046-f4-governance.yml` | gate F4 e regressioni F2/F3 |

L'envelope deve contenere almeno:

- `schemaVersion`, `projectionType`, `projectionState`, `projectionId` e `generatedAt`;
- snapshot del catalogo con path, digest, session count e session ID ordinati;
- snapshot delle source di provenance con path e digest ordinati;
- method/producer/version F3 riusati senza ridefinizione;
- un record per ogni sessione, ordinato per `sessionId`;
- Recommendation F2-valid, source/correlation state, citation e limitation;
- summary esclusivamente descrittiva per stato, senza ranking o quality score;
- authority chiusa e `projectionDigest` SHA-256 canonico.

`generatedAt` è metadata di pubblicazione e non può influenzare regole, Recommendation ID o classificazione. In modalità `--check` viene riusato il timestamp persistito; una scrittura non avviene quando l'unica differenza sarebbe il clock.

## 8. Deterministic mapping to F3

Per ogni sessione, l'adapter costruisce un input pre-decisione con:

- subject derivato dall'identità canonica del catalogo;
- `repository_authority` derivata soltanto dal catalogo validato;
- `processing_evidence` derivata soltanto dal read model BKL-045 correlato;
- lifecycle, quality, completeness, citations e limitations preservati;
- confidence invariata a `UNAVAILABLE_F2`;
- authority F2/F3 invariata.

L'assenza di processing history non sopprime la sessione: `PROCESSING_HISTORY_AVAILABILITY` deve produrre `FAIL_CLOSED` con reason code deterministici. Nessuna regola può dedurre processi PixInsight dal target, dagli output immagine o da pattern statistici.

## 9. Automatic post-import publication

F4 estende l'orchestratore esistente senza crearne uno parallelo:

1. il trigger corrente rileva un nuovo manifest di sessione;
2. catalogo e source governate vengono rigenerati/validati;
3. il generator F4 esegue `--write` e poi `--check`;
4. test F4 e regressioni F2/F3 bloccano la pubblicazione in caso di errore;
5. `docs/data/ai-post-processing-advisory-projection.json` entra in `governed_paths`;
6. la stessa sequenza è presente nella funzione di retry `regenerate()` dopo il reset su `origin/main`;
7. catalogo, projection F4 e altri derivati vengono committati e pushati atomicamente;
8. Pages viene richiesto soltanto dopo il push riuscito.

Una modifica alla provenance BKL-045 deve includere la projection riallineata nella stessa PR oppure fallire il gate `--check`; non è ammesso un merge che lasci il consumer stale.

## 10. Freshness and fail-closed contract

Prima del rendering, il browser scarica catalogo e projection con `cache: no-store` e verifica:

- schema, lifecycle, producer/method e authority supportati;
- SHA-256 del catalogo corrente contro lo snapshot F4;
- session count e insieme ordinato degli ID;
- digest di ogni source di provenance referenziata;
- digest dell'intera projection;
- corrispondenza uno-a-uno dei record alle sessioni;
- assenza di proprietà o stati sconosciuti.

| Failure | UX obbligatoria |
|---|---|
| catalogo più recente della projection | banner `DATI NON ALLINEATI`, nessuna Recommendation mostrata come corrente |
| projection o source digest alterato | stato `VERIFICA FALLITA`, dettagli tecnici non sensibili |
| Web Crypto non disponibile | consumer non disponibile, nessun fallback permissivo |
| schema/versione non supportati | aggiornamento richiesto, dati non renderizzati |
| correlation missing/ambiguous | record visibile come incompleto con rationale; nessun claim validato |
| fetch parziale o errore rete | stato vuoto esplicito, nessun riuso di cache precedente come corrente |

## 11. Portal UX and accessibility

La pagina F4 deve distinguere chiaramente:

- **Projection verified**: digest e session set coerenti;
- **Recommendation validated**: sola validità contrattuale, non qualità scientifica;
- **Fail-closed / incomplete evidence**: source mancante, incompleta o non correlabile;
- **Human decision not present**: nessuna decisione implicita;
- **Execution not evidenced**: Recommendation e decisione non provano una lavorazione PixInsight.

Il consumer prevede summary descrittiva, ricerca per sessione/target, filtri per source/correlation state, elenco ordinabile senza ranking predefinito e dettaglio con rationale, reason code, citation, provenance e limitation. Stati e azioni non dipendono dal solo colore; focus, tastiera, live region e reduced motion rispettano il design system. Non sono presenti pulsanti Apply, Accept automatically, Execute o comandi verso PixInsight.

## 12. Security, privacy and safety

- solo JSON e riferimenti già destinati alla pubblicazione documentale;
- nessuna immagine, URI locale, hostname, credential, secret o prompt esterno;
- path source sempre repository-relative e allowlisted;
- proprietà inattese, path assoluti e traversal vengono rifiutati;
- nessun endpoint mutativo, token browser o upload;
- nessuna dipendenza di controllo da PixInsight, EAGLE, N.I.N.A., ASCOM, PLC o cupola;
- interlock fisici locali restano l'unica Safety Authority.

Authority invariata:

```text
consumerMode = READ_ONLY
advisoryOnly = true
acceptanceAuthority = HUMAN_ONLY
actionAuthority = NONE
executionAuthority = NONE
safetyAuthority = LOCAL_PHYSICAL_INTERLOCKS
pixInsightApplyAuthorized = false
automaticAcceptanceAuthorized = false
```

## 13. Observability and operations

Il workflow deve esporre conteggi per sessioni totali, provenance matched/unavailable/ambiguous/invalid e Recommendation PASS/FAIL_CLOSED, oltre a errori di validation e drift. I log non devono contenere dati immagine, payload completi non necessari o path locali.

Non sono introdotti servizi residenti, database, scheduler, secret o runbook hardware. La diagnosi avviene tramite gate CI, reason code persistiti e stato fail-closed del consumer.

## 14. Migration and rollback

La migrazione è additiva:

1. contratto e source adapter;
2. generator/projection e test;
3. integrazione post-import atomica;
4. consumer e navigazione;
5. ARB/RQ, exact-head CI, merge e verifica post-merge.

Il rollback rimuove artefatti F4 e le chiamate aggiunte al workflow. Catalogo AP-014, provenance BKL-045 e contratti F2/F3 restano invariati; non è richiesta migrazione dati o modifica runtime.

## 15. Delivery slices

| Slice | Output | Exit gate |
|---|---|---|
| F4-A — source and projection contract | schema, discovery/correlation adapter, builder e negative tests | source authority e missingness fail-closed verificate |
| F4-B — automatic atomic publication | generator persistito, workflow first/retry path e governed path | import simulation, idempotenza e drift gate verdi |
| F4-C — portal consumer and readiness | core browser validator, pagina, accessibility tests e governance workflow | freshness/tamper tests, MkDocs, ARB/RQ ed exact-head CI |

Le slice sono incrementi interni di delivery e non cambiano la dipendenza di programma: F5 può iniziare soltanto dopo acceptance completa di F4.

## 16. Quality and validation plan

| Gate | Evidenza richiesta |
|---|---|
| Architecture | boundary AP-013/AP-014/BKL-045/BKL-046 e dependency direction verificati |
| Contract | schema chiuso, validator, unknown-property e authority-escalation tests |
| Determinism | output byte-semantico, ID, ordering e digest stabili |
| Source correlation | exact match, missing, duplicate, mismatch e tamper tests |
| Dynamic update | workflow contiene `--write`, `--check`, test e output in entrambi i generation path |
| Atomicity | projection inclusa nei `governed_paths`; retry rigenera dopo reset |
| Consumer | no-store, SHA-256, stale/session-set/digest failure e empty-state tests |
| Accessibility | tastiera, focus, semantic labels, non-color status e reduced motion |
| Regression | suite F2 e F3 integralmente verdi |
| Documentation | MkDocs strict, link/navigation e Mermaid verificati |
| Security/safety | path/secret/image rejection; authority e interlock invariati |
| Release | ARB/RQ, exact-head CI, protected merge, post-merge workflows e Pages |

## 17. Risks and trade-offs

| ID | Rischio | Trattamento |
|---|---|---|
| F4-R01 | molte sessioni senza provenance PixInsight | record espliciti `PROVENANCE_UNAVAILABLE`; nessuna soppressione o inferenza |
| F4-R02 | OAT BKL-045 non correlabile al catalogo scientifico | mantiene evidence separata; nessun fuzzy match |
| F4-R03 | doppio generator path nel workflow diverge | verifier statico e test obbligatori su first/retry path |
| F4-R04 | Recommendation validata interpretata come scientificamente corretta | label e limitation obbligatorie; nessuna confidence numerica |
| F4-R05 | merge provenance senza projection aggiornata | gate `--check` fail-closed sulla stessa PR |
| F4-R06 | consumer mostra cache stale | `no-store`, digest chain e hard failure |
| F4-R07 | crescita lineare delle source | discovery e ordinamento O(n); nessun database introdotto prima di evidence di scala |

Non è richiesta una nuova ADR: F4 applica ADR-008, i contratti F2/F3 e il pattern di projection atomica già accettato in BKL-041 F4. Una ADR diventa necessaria solo se l'implementazione richiede un nuovo store, un servizio runtime, una correlation strategy non esatta o una modifica al capture mechanism PixInsight.

## 18. Traceability

| Requisito | Source |
|---|---|
| F3 accepted baseline | `docs/project/BKL-046-F3-ACCEPTANCE-2026-09-11.md` |
| Recommendation/Human Decision semantics | BKL-046 F1/F2 |
| deterministic rule behavior | `docs/architecture/scientific-assets/BKL-046-F3-Deterministic-Advisory-Demonstrator.md` |
| PixInsight provenance semantics | BKL-045 F1/F5 e `docs/project/BKL-045-CLOSURE-2026-09-10.md` |
| capture strategy | `docs/architecture/ADR-008-PixInsight-Provenance-Capture-Strategy.md` |
| session/catalog authority | AP-013, AP-014 e `docs/data/scientific-session-catalog.json` |
| automatic import boundary | `.github/workflows/analyze-session-automatic.yml` |
| atomic projection reference pattern | `docs/architecture/scientific-assets/BKL-041-F4-Session-Driven-Projection-and-Portal-Consumer.md` |
| roadmap authority | `.github/roadmap/roadmap-source.json` |

## 19. Acceptance criteria

F4 è accettabile soltanto quando:

1. ogni catalog session ha esattamente un record F4;
2. le source BKL-045 sono scoperte mediante pattern chiuso, validate e ordinate;
3. la correlazione è exact-match e missing/ambiguous/invalid falliscono chiuso;
4. Recommendation e reason code sono prodotti esclusivamente dalle regole F3 accettate;
5. F2/F3 authority, confidence e decision boundary restano invariati;
6. projection, source snapshot e digest sono deterministici e anti-tampering;
7. il consumer verifica catalogo, session set, source digest e projection digest prima del rendering;
8. dati stale non sono presentati come correnti;
9. il workflow post-import rigenera e verifica F4 sia nel first path sia nel retry path;
10. projection e catalogo sono pubblicati nello stesso commit governato;
11. ogni modifica di provenance non può essere integrata con projection drift;
12. UX, accessibility ed empty/failure states sono testati;
13. nessun image data, path locale, secret, model/provider, apply o automatic acceptance è introdotto;
14. Safety Authority e runtime osservativo restano invariati;
15. test F2/F3/F4, MkDocs e exact-head CI sono verdi;
16. ARB e Release Quality documentano review scope e modalità senza claim non verificati;
17. merge protetto, workflow post-merge e Pages risultano verificati.

## 20. Open issues

1. La baseline reale corrente potrebbe non contenere alcun sidecar BKL-045 correlabile esattamente alle 15 sessioni del catalogo; l'implementazione deve misurarlo, non presumerlo.
2. La completezza della processing history resta limitata da ADR-008 e dall'OAT BKL-045; F4 non può migliorarla semanticamente.
3. F5 dovrà definire cohort, evaluation criteria e retained limitations per la validazione su evidence reale; F4 non anticipa tale decisione.

## 21. Future evolution

F5 potrà valutare gli output F4 su evidence reale e decidere la closure come capability read-only con limitation. Qualsiasi model/provider, confidence scientifica, image transfer o modalità Assisted Apply resta separata, richiede nuovi driver, evidence, security/privacy assessment e decisione architetturale dedicata.
