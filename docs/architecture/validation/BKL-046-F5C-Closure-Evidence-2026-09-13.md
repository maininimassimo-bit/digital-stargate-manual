# BKL-046 F5-C — Closure Evidence

| Campo | Valore |
|---|---|
| Identificativo | BKL-046-F5C-EVIDENCE-001 |
| Stato | Candidate evidence complete; exact-head CI and governance review pending |
| Data | 13/09/2026 |
| Baseline | `main` @ `8ed6085d15f6af9e466a90167f19e970e8c526a7` |
| F5-B merge | PR #179, `eb1827e2cc6e957080c6d1e928a7b13652261851` |
| Growth-safety hotfix | PR #180, `2edb44d1d26b36f9381a3796483efe9c105a679d` |
| Evidence session | `2026-09-12_2026-09-13` |
| Scope | Technical closure of the deterministic read-only capability only |

## 1. Outcome

La prima importazione reale successiva a F5-B e la relativa pubblicazione Pages chiudono l'observation `ARB-F5B-O01`. Catalogo, projection F4 e report F5 sono stati rigenerati nello stesso percorso governato e risultano allineati su 16 sessioni. Il consumer live ha verificato l'intera freshness chain e ha mostrato la nuova sessione senza fallback permissivi.

L'evidenza consente di proporre:

- `F5B_DYNAMIC_UPDATE = PASS`;
- `F5B_CONSUMER = PASS`;
- technical outcome `ACCEPTED_READ_ONLY_WITH_LIMITATIONS`;
- closure recommendation `CLOSE_DETERMINISTIC_CAPABILITY`.

Non consente di dichiarare efficacia scientifica, disponibilità di decisioni umane, execution evidence, production readiness o implementazione di un modello AI.

## 2. Runtime and workflow evidence

| Gate | Evidence | Risultato |
|---|---|---|
| EAGLE first publication | automation log `END outcome=PUBLISHED`, session branch pubblicato | PASS |
| Analysis workflow | [run 34766534178](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/34766534178), attempt 1 | SUCCESS |
| Generated commit | `8ed6085d15f6af9e466a90167f19e970e8c526a7` | PASS |
| Pages deployment | [run 34766571069](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/34766571069) | SUCCESS |
| Catalog growth | 15 -> 16 canonical sessions | PASS |
| F4 atomic alignment | 16 records; source catalog count 16 | PASS |
| F5 atomic alignment | 16 canonical sessions; F4 record count 16; matching snapshot digests | PASS |
| Candidate session | `2026-09-12_2026-09-13`, target M 27 | PASS |

## 3. Live consumer evidence

Verifica eseguita il 13/09/2026 su [AI Post-Processing Assistant](https://maininimassimo-bit.github.io/digital-stargate-manual/ai-post-processing-assistant/):

- pagina caricata con `FRESHNESS CHAIN VERIFIED`;
- 16 sessioni visualizzate;
- filtro exact session ID restituisce un solo record;
- nuova sessione M 27 presenta `GOVERNANCE_READINESS = PASS`;
- provenance assente resta `PROVENANCE_UNAVAILABLE`;
- processing history resta `FAIL_CLOSED` con `REQUIRED_SOURCE_AUTHORITY_MISSING`;
- nessuna decisione umana viene inferita;
- il collegamento apre il [dettaglio sessione](https://maininimassimo-bit.github.io/digital-stargate-manual/scientific-session-detail/?sessionId=2026-09-12_2026-09-13) con 28/29 light, 4,67 h e RMS totale 0,390 arcsec;
- nessun errore originato dalla pagina applicativa è stato osservato nella console durante il test.

## 4. Data outcome retained

| Asse | Stato candidato |
|---|---|
| Technical capability | `ACCEPTED_READ_ONLY_WITH_LIMITATIONS` |
| Scientific effectiveness | `NOT_EVALUABLE_CURRENT_EVIDENCE` |
| Human-decision evidence | `NOT_AVAILABLE` |
| Production readiness | `NOT_READY_FOR_PRODUCTION` |
| AI model implemented | `false` |
| Closure recommendation | `CLOSE_DETERMINISTIC_CAPABILITY` |

La distribuzione osservata è LDN 1320 = 3, M 27 = 12, UNKNOWN = 1. Provenance eligible, Human Decision Receipt ed execution evidence restano tutti a 0; le source processing non correlate restano 2.

## 5. Local candidate validation

Eseguiti sul candidato F5-C:

```text
node .github/scripts/generate-ai-post-processing-advisory-f5-evaluation.mjs --check
node .github/scripts/verify-ai-post-processing-advisory-f5-evaluation.mjs
node --test .github/scripts/test-ai-post-processing-advisory-f5-evaluation.mjs .github/scripts/test-ai-post-processing-assistant-consumer.mjs
```

Risultato: generator/check e verifier PASS; 85/85 test aggregati F2-F5 PASS, di cui 44/44 nella slice F5 evaluator + consumer. Sono inclusi tamper, stale snapshot, authority escalation, Web Crypto unavailable, first/retry ordering, atomic path e accessibility/non-mutation. La generazione in memoria contro il catalogo pubblicato a 16 sessioni ha inoltre superato la validazione di freshness.

## 6. Operational observation

Una seconda esecuzione manuale della stessa finestra EAGLE ha terminato con task result `0` e `END outcome=DEFERRED status=PARTIAL`, perché N.I.N.A. non era più presente tra le sorgenti candidate mentre PHD2 e meteo erano ancora rilevati. Il repository è rimasto pulito, su `main`, allineato `0/0` con `origin/main`.

Questa idempotency observation non invalida la prima pubblicazione né la catena F5-B, ma resta un miglioramento operativo separato: una riesecuzione della stessa finestra dovrebbe produrre `NOOP/ALREADY_PUBLISHED` invece di `PARTIAL`.

## 7. Pending gates

- exact-head GitHub Actions del candidato F5-C;
- ARB e Release Quality specifiche F5-C nella modalità effettivamente autorizzata;
- autorizzazione owner separata al merge e disposizione separata sulla branch protection;
- post-merge workflow e Pages verification;
- aggiornamento definitivo della closure da Proposed ad Accepted.

## 8. Rollback

Revert atomico del commit F5-C. F5-A/F5-B, catalogo, projection F4, session data e interlock fisici restano invariati. Dopo il revert devono essere rieseguiti F5 governance e Pages.
