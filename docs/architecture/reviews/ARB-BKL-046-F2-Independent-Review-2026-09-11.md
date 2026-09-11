# ARB — BKL-046 F2 Independent Architecture Review

| Campo | Valore |
|---|---|
| Package | BKL-046 F2 — Machine-Readable Recommendation and Human Decision Contracts |
| Review date | 11/09/2026 |
| Reviewed head | `9ab6ac4c00d88b7bcd7bd0cf7da08f9c1a64cc43` |
| Pull request | #167 |
| Decision | **APPROVED** |
| Score | **98/100** |
| Findings | Blocker 0 · Major 0 · Minor 0 · Observation 2 |

## 1. Review scope

La review valuta in modo indipendente il package F2 pubblicato sulla PR #167 rispetto a F1 Accepted, BKL-044, BKL-045, roadmap corrente, authority boundary, sicurezza, operabilità, migrazione, tracciabilità ed evidence CI exact-head.

F2 è valutato come contratto repository-side e fixture sintetica. La review non attribuisce alcuna implementazione runtime, qualità scientifica, model/provider selection, image processing o PixInsight execution.

## 2. Reviewed evidence

- `docs/architecture/scientific-assets/BKL-046-F2-Machine-Readable-Recommendation-and-Human-Decision-Contracts.md`;
- `docs/contracts/ai-post-processing-assistant-f2.schema.json`;
- `docs/data/ai-post-processing-assistant-f2-fixture.json`;
- `.github/scripts/ai-post-processing-advisory-contract.mjs`;
- `.github/scripts/verify-ai-post-processing-advisory-contract.mjs`;
- `.github/scripts/test-ai-post-processing-advisory-contract.mjs`;
- `.github/workflows/bkl-046-f2-governance.yml`;
- `mkdocs.yml`;
- PR #167 exact head `9ab6ac4c00d88b7bcd7bd0cf7da08f9c1a64cc43`;
- five applicable GitHub Actions runs, all `SUCCESS`.

## 3. Repository and dependency consistency

- F1 risulta Accepted tramite PR #165, merge `3f2e3edae93b009f5800a58a4ac5afc4f04e9bb7`;
- la baseline di sviluppo F2 coincide con il merge di riconciliazione `fc4c82fdaa0cd1a3c438c9b6a0ad58ec1e54925d`;
- roadmap, backlog, bootstrap e scientific-platform status indicano F2 come incremento corrente;
- Recommendation riusa la semantic class BKL-044 senza creare una nuova evidence authority;
- execution evidence resta proprietà BKL-045;
- AP-013/AP-014 e la pipeline di import non vengono modificati.

Non risultano duplicazioni o inversioni di dipendenza.

## 4. Scorecard

| Dimensione | Score | Evidenza |
|---|---:|---|
| Coerenza con F1 e programma | 100 | scope F2 aderente al handoff accettato |
| Domain e authority boundaries | 100 | Recommendation, decisione ed execution evidence separati |
| Contract design e fail-closed | 98 | schema chiuso, identity, lifecycle, missingness e reference gates |
| Safety e security | 100 | apply/automatic acceptance/device/Safety Authority vietati |
| Privacy e data minimization | 98 | nessuna immagine, path assoluto, secret o provider nel contratto |
| Operabilità e osservabilità | 95 | correlation, producer/method/version e digest presenti; runtime non introdotto |
| Compatibility, migration e rollback | 100 | change additive, repository-only, revert documentato |
| Dynamic update architecture | 96 | F2 non crea projection; requisiti automatici F4 espliciti |
| Traceability e documentazione | 98 | package, schema, fixture, validation, CI e MkDocs allineati |
| Test e quality evidence | 99 | 16 test locali e 5/5 workflow exact-head verdi |

**Score complessivo: 98/100.**

## 5. Findings

### Blocker

Nessuno.

### Major

Nessuno.

### Minor

Nessuno.

### Observations

**OBS-01 — Fixture envelope versus future runtime envelope**  
Lo schema root è intenzionalmente `AI_POST_PROCESSING_ASSISTANT_F2_FIXTURE` e richiede almeno una Recommendation e un Human Decision Receipt. F3 non deve pubblicare questo envelope come contratto runtime implicito: dovrà riusare/versionare i `$defs` o introdurre un envelope di produzione separato, capace di rappresentare il tempo precedente alla decisione umana.

**OBS-02 — Confidence remains unavailable by design**  
`UNAVAILABLE_F2` è la scelta corretta sulla evidence corrente. Fasi successive non devono aggiungere una confidence numerica senza metodo, calibration population, versioning e validation separati.

Le observations non bloccano F2 e non richiedono remediation su questa PR.

## 6. Architecture integrity

Il package mantiene i layer e le authority coerenti:

- il contratto pubblico non espone domain entity o tipo di persistenza;
- il validator è repository tooling, non runtime observatory;
- source binding e subject ref non mutano le fonti upstream;
- il receipt non contiene execution evidence e impone `NOT_OBSERVED`;
- i digest rendono rilevabile il tampering senza attribuire veridicità scientifica;
- il fail-closed impedisce a stale, incomplete, invalid o `SUGGESTED` evidence di sostenere `validated`.

## 7. Safety, security and operations

La review conferma:

- `consumerMode = READ_ONLY`;
- `advisoryOnly = true`;
- `acceptanceAuthority = HUMAN_ONLY`;
- action ed execution authority `NONE`;
- PixInsight apply e automatic acceptance `false`;
- Safety Authority invariata sugli interlock fisici locali;
- nessun carico o dipendenza introdotta su EAGLE;
- nessuna trasmissione di immagini o credenziali.

Non è richiesto un runbook operativo perché F2 non introduce runtime o servizio.

## 8. Dynamic update assessment

F2 è statico per definizione e non aggiunge un consumer. Il requisito di aggiornamento automatico dopo ogni sessione importata resta preservato: il package lo rende un acceptance gate esplicito per il futuro consumer F4, includendo rigenerazione, pubblicazione atomica, digest/freshness e fail-closed.

L'assenza di una modifica alla pipeline di import in F2 è coerente e non costituisce una regressione.

## 9. Validation evidence

Sul reviewed head `9ab6ac4c00d88b7bcd7bd0cf7da08f9c1a64cc43`:

| Workflow | Run | Esito |
|---|---:|---|
| BKL-046 F2 Governance | `34633260514` | SUCCESS |
| Developer Foundation | `34633260375` | SUCCESS |
| Validate documentation (no deploy) | `34633260391` | SUCCESS |
| Genera manuale Word | `34633260345` | SUCCESS |
| BKL-041 F4 Governance regression | `34633260360` | SUCCESS |

Il gate F2 esegue verifier e 16 test positivi/negativi. Developer Foundation include build, test, regressioni scientifiche, idempotency e `mkdocs build --strict`.

## 10. Decision

**APPROVED**, senza condizioni bloccanti e senza waiver.

La decisione approva il package F2 per il successivo Release Quality gate. Non approva F3, model/provider, dati reali, recommendation quality, confidence numerica, consumer dinamico o PixInsight apply.

## 11. Re-review criteria

Una nuova review è obbligatoria se il package introduce o modifica:

- model/provider o external data transfer;
- runtime inference o generazione da sessioni reali;
- confidence/calibration method;
- action/execution authority o PixInsight apply;
- consumer dinamico e relativa pipeline post-import;
- schema incompatibile o nuova semantic authority.
