# BKL-046 F3 — Acceptance Record

| Campo | Valore |
|---|---|
| Incremento | BKL-046 F3 — Deterministic Advisory Demonstrator |
| Stato | CLOSED / ACCEPTED / POST-MERGE WORKFLOWS VERIFIED |
| Data | 11/09/2026 |
| Pull request | #169 |
| Accepted merge | `8339aecf0b6b7fa19396561b20253c0411fd7ee7` |
| Exact final head | `036b59ec39c2b43f4ee3cbe676189d1ce7b82c04` |
| Reviewed implementation head | `4c70fb73e6f57ab31a7deecd42b9473a55aa81fe` |
| Review mode | AI-assisted, repository-owner authorized; not an independent human approval |
| Known-answer digest | `a97f7ff5a394b6f714efc8a55b1b1ab6cd6c6865c9a58ea6b9ec5120e98a4070` |
| Successore | BKL-046 F4 — Session/Provenance-Driven Read-Only Consumer |

## 1. Acceptance decision

BKL-046 F3 è accettato come demonstrator deterministico, bounded, sintetico, read-only e pre-decisione. L'incremento prova che i contratti F2 possono essere consumati da regole chiuse e produrre Recommendation conformi, ripetibili e auditabili senza inferenza AI, selezione model/provider, sessioni reali, confidence numerica, accettazione automatica o applicazione PixInsight.

Le valutazioni ARB e Release Quality sono review AI-assistite autorizzate dal repository owner. Non costituiscono approvazioni umane indipendenti e non ampliano l'authority tecnica o scientifica dell'incremento.

## 2. Evidence verificata

| Evidenza | Esito |
|---|---|
| F2 regression suite | 16/16 test PASS |
| F3 demonstrator suite | 21/21 test PASS |
| Known-answer output | digest SHA-256 stabile e verificato |
| ARB F3 AI-assisted | APPROVED owner-authorized, 99/100, 0 Blocker/Major/Minor |
| Release Quality F3 AI-assisted | READY FOR MERGE owner-authorized, nessuna waiver |
| Exact-head CI | tutti i gate applicabili verdi sul final head |
| Post-merge workflows | 7/7 SUCCESS sul merge accettato |

Workflow post-merge verificati sul commit `8339aecf0b6b7fa19396561b20253c0411fd7ee7`:

| Workflow | Run | Esito |
|---|---:|---|
| Validate documentation | `34643716143` | SUCCESS |
| BKL-046 F3 Governance | `34643716177` | SUCCESS |
| Developer Foundation | `34643716150` | SUCCESS |
| BKL-041 F4 Governance regression | `34643716194` | SUCCESS |
| BKL-046 F2 Governance regression | `34643716340` | SUCCESS |
| Genera manuale Word | `34643716257` | SUCCESS |
| Deploy Pages | `34643716214` | SUCCESS |

## 3. Quality gate matrix

| Gate | Esito | Evidenza / decisione |
|---|---|---|
| Scope e authority | PASS | synthetic/read-only, HUMAN_ONLY, action/execution NONE |
| Contract integrity | PASS | schema F3 autonomo; tipi F2 riusati tramite `$ref` e validator |
| Determinismo e audit | PASS | identity, ordering, immutabilità e digest verificati |
| Fail-closed | PASS | missing, stale, invalid, suggested e unresolved correlation non sono promossi |
| Test e regressione | PASS | 16/16 F2 e 21/21 F3 |
| Security e privacy | PASS | nessuna immagine, secret, credential, path locale o rete |
| Safety | PASS | Safety Authority invariata; interlock fisici locali preservati |
| Documentazione e navigazione | PASS | architecture, review, contract, data e MkDocs integrati |
| Migration/runtime | N/A | nessun servizio, storage o migrazione dati |
| Waiver | NONE | nessuna deroga approvata o richiesta |
| Dynamic post-import consumer | NOT APPLICABLE TO F3 | requisito obbligatorio e gate di acceptance per F4 |

## 4. Contratti e comportamento accettati

- due regole chiuse e deterministiche: `GOVERNANCE_READINESS` e `PROCESSING_HISTORY_AVAILABILITY`;
- output F3 autonomo pre-decisione, senza Human Decision Receipt o execution claim;
- ogni Recommendation validata contro il contratto F2;
- `confidence.state=UNAVAILABLE_F2`, senza valore numerico inventato;
- missingness BKL-045 preservata mediante `FAIL_CLOSED` e `UNKNOWN_NOT_RECOMMENDED`;
- output deep-frozen e `artifactDigest` sull'intero payload escluso il campo digest;
- nessun comando, remediation, side effect o accesso a PixInsight/EAGLE/apparati.

## 5. Dynamic update boundary

F3 resta statico e usa esclusivamente fixture sintetiche bounded. Non modifica `analyze-session-automatic.yml`, catalogo AP-014 o proiezioni alimentate dalle sessioni.

F4 dovrà essere automaticamente collegato alla pipeline di import scientifico: dopo ogni nuova sessione importata dovrà rigenerare e pubblicare nello stesso incremento atomico una projection deterministica read-only. L'acceptance richiederà input canonici reali autorizzati, freshness e digest verificabili e comportamento fail-closed; dati stale o non verificabili non potranno essere presentati come correnti.

## 6. Limitation e rischi trattenuti

- la completezza automatica della processing history PixInsight reale resta `UNAVAILABLE` dove non osservata;
- F3 non fornisce quality/confidence scientifica, ground truth o validazione su sessioni reali;
- non è stato selezionato alcun modello, provider, RAG/vector store o image-transfer path;
- le osservazioni ARB su riferimento JSON Schema e uso temporale delle fixture restano input non bloccanti per F4;
- una Recommendation non equivale a decisione umana e una decisione non equivale a execution evidence.

## 7. Transition decision

È promosso esclusivamente BKL-046 F4 — Session/Provenance-Driven Read-Only Consumer. F4 dovrà progettare e dimostrare il consumer accessibile e la projection post-import automatica, atomica e freshness-verified senza introdurre model/provider, automatic acceptance, PixInsight apply, remediation, device command o Safety Authority.

F5 e ogni possibile evolution con AI runtime, confidence scientifica o assisted apply restano fuori scope e richiedono evidence e decisioni dedicate.
