# ARB — BKL-046 F3 AI-Assisted Architecture Review

| Campo | Valore |
|---|---|
| Package | BKL-046 F3 — Deterministic Advisory Demonstrator |
| Review date | 11/09/2026 |
| Reviewed head | `4c70fb73e6f57ab31a7deecd42b9473a55aa81fe` |
| Pull request | #169 |
| Review mode | **AI-assisted governance assessment — not a human-independent review** |
| Publication authority | Repository owner authorization recorded 11/09/2026 |
| Decision | **APPROVED — AI-assisted, owner-authorized** |
| Score | **99/100** |
| Findings | Blocker 0 · Major 0 · Minor 0 · Observation 2 |

## 1. Review scope

La review AI-assistita valuta il package F3 pubblicato sulla PR #169 rispetto a F1/F2 Accepted, alle observations ARB F2, alla roadmap corrente, ai confini di authority e all'evidence CI exact-head. La pubblicazione e l'uso come gate di repository sono stati autorizzati dal repository owner; il documento non dichiara una review umana indipendente.

F3 è valutato come demonstrator repository-side, deterministico, read-only e sintetico. La review non attribuisce implementazione di un assistente AI produttivo, recommendation quality, confidence calibrata, dati reali, consumer dinamico o PixInsight execution.

## 2. Reviewed evidence

- `docs/architecture/scientific-assets/BKL-046-F3-Deterministic-Advisory-Demonstrator.md`;
- `docs/contracts/ai-post-processing-assistant-f3.schema.json`;
- `docs/data/ai-post-processing-assistant-f3-output.json`;
- `.github/scripts/ai-post-processing-advisory-contract.mjs`;
- `.github/scripts/ai-post-processing-advisory-demonstrator.mjs`;
- `.github/scripts/verify-ai-post-processing-advisory-demonstrator.mjs`;
- `.github/scripts/test-ai-post-processing-advisory-demonstrator.mjs`;
- `.github/workflows/bkl-046-f3-governance.yml`;
- PR #169 reviewed head `4c70fb73e6f57ab31a7deecd42b9473a55aa81fe`;
- sei workflow GitHub Actions applicabili, tutti `SUCCESS`.

## 3. Repository and dependency consistency

- F2 è Accepted tramite PR #167, merge `b8a9025fdfc9b5254b9c79a5c37a775b4f8fd083`;
- la development baseline F3 coincide con `main` @ `2d2f876cfa9deead5cc8fee556edb10ac666ecc1`;
- roadmap, bootstrap, baseline e backlog indicano F3 come incremento corrente;
- l'envelope F3 è distinto dal root fixture F2 e rappresenta esplicitamente il tempo pre-decisione;
- Recommendation, subject, source binding, authority e digest riusano i tipi F2;
- Human Decision Receipt resta separato e l'execution evidence resta proprietà BKL-045;
- import AP-014, session catalog e proiezioni dinamiche non sono modificati.

Non risultano duplicazioni semantiche, nuove authority o inversioni di dipendenza.

## 4. Scorecard

| Dimensione | Score | Evidenza |
|---|---:|---|
| Coerenza con F1/F2 e programma | 100 | scope aderente al transition contract Accepted |
| Contract e temporal boundary | 100 | envelope autonomo `NOT_PRESENT_PRE_DECISION`, `$ref` F2 |
| Determinismo e fail-closed | 100 | regole chiuse, reason code, known answer, digest e immutabilità |
| Domain e authority boundaries | 100 | Recommendation, decisione ed execution evidence separate |
| Safety e security | 100 | apply, automatic acceptance, command e Safety Authority vietati |
| Privacy e data minimization | 100 | fixture sintetica; nessuna immagine, path assoluto, secret o provider |
| Operabilità e osservabilità | 97 | method/version/correlation/digest/reason code presenti; nessun runtime |
| Compatibility, migration e rollback | 100 | change additiva e revert documentato |
| Dynamic update architecture | 98 | F3 statico; gate F4 automatico e atomico esplicito |
| Traceability e documentazione | 99 | package, schema, fixture, CI e MkDocs allineati |
| Test e quality evidence | 100 | 16 regressioni F2, 21 test F3 e 6/6 workflow exact-head verdi |

**Score complessivo: 99/100.**

## 5. Findings

### Blocker

Nessuno.

### Major

Nessuno.

### Minor

Nessuno.

### Observations

**OBS-01 — Resolution of external JSON Schema references**  
Lo schema F3 riusa correttamente i `$defs` F2 tramite riferimenti relativi. Un futuro validator generico dovrà registrare e risolvere lo schema F2 con URI/versione esatti; il validator repository corrente verifica le stesse invarianti tramite codice e il verifier controlla i riferimenti dichiarati. L'observation non blocca il demonstrator.

**OBS-02 — Fixture time is deterministic, not execution time**  
`generatedAt` deriva intenzionalmente dalla fixture per garantire il known answer. Non deve essere interpretato come timestamp di una futura esecuzione runtime. F4 dovrà separare event time, projection generation time e source freshness.

## 6. Architecture integrity

Il package mantiene i confini accettati:

- valida l'intera fixture F2 prima di eseguire le regole;
- esporta dal validator F2 una funzione additiva per validare una singola Recommendation;
- genera sempre due rule evaluation chiuse e collega ogni evaluation a una sola Recommendation;
- verifica coerenza tra decisione, reason code, unknowns, lifecycle, category e source authority;
- rappresenta l'assenza dell'authority richiesta con `REQUIRED_SOURCE_AUTHORITY_MISSING`;
- non usa le Recommendation o i receipt presenti nella fixture come output runtime implicito;
- non modifica l'input e restituisce un output deep-frozen.

## 7. Safety, security and privacy

La review conferma:

- consumer mode read-only e advisory-only;
- acceptance authority human-only;
- action ed execution authority `NONE`;
- PixInsight apply e automatic acceptance `false`;
- Safety Authority invariata sugli interlock fisici locali;
- assenza di model/provider, immagini, credential, absolute path e canali eseguibili;
- nessun accesso o carico introdotto su EAGLE, PixInsight o apparati.

Non è richiesto un threat model o runbook operativo aggiuntivo perché F3 non introduce rete, servizio, secret o runtime osservativo.

## 8. Dynamic update assessment

F3 usa esclusivamente la fixture F2 bounded e non introduce una projection. Questo è coerente con lo scope approvato e non regredisce il requisito utente: F4 dovrà dimostrare rigenerazione automatica dopo ogni sessione importata, input canonici autorizzati, freshness/digest gate, pubblicazione atomica e consumer fail-closed.

L'acceptance F3 non autorizza dati reali o consumer.

## 9. Validation evidence

Sul reviewed head `4c70fb73e6f57ab31a7deecd42b9473a55aa81fe`:

| Workflow | Run | Esito |
|---|---:|---|
| BKL-046 F3 Governance | `34640820769` | SUCCESS |
| BKL-046 F2 Governance regression | `34640820796` | SUCCESS |
| Developer Foundation | `34640820793` | SUCCESS |
| Validate documentation (no deploy) | `34640820808` | SUCCESS |
| Genera manuale Word | `34640820762` | SUCCESS |
| BKL-041 F4 Governance regression | `34640820794` | SUCCESS |

Il gate F3 verifica il known answer e 21 test. Il Developer Foundation include build, formatting, suite repository, downstream idempotency e `mkdocs build --strict`.

## 10. Decision

**APPROVED — AI-assisted, owner-authorized**, senza condizioni bloccanti e senza waiver.

La decisione approva F3 per il successivo Release Quality gate. Non approva F4, sessioni reali, consumer dinamico, model/provider, recommendation quality, confidence numerica o PixInsight apply.

## 11. Re-review criteria

Una nuova review è obbligatoria se il package introduce o modifica:

- model/provider, inference, prompt, RAG o external transfer;
- dati di sessione reali o immagini;
- confidence/calibration o parameter recommendation method;
- consumer/projection dinamica e trigger post-import;
- decision, action o execution authority;
- PixInsight apply, device command o Safety Authority;
- schema incompatibile o nuova semantic authority.
