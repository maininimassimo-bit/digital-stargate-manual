# ARB-BKL-041-F2 — Independent Architecture Review

| Campo | Valore |
|---|---|
| Review | ARB-BKL-041-F2 |
| Data | 11/09/2026 |
| Proposal | `docs/architecture/scientific-assets/BKL-041-F2-Machine-Readable-Quality-Evidence-and-Profile-Contract.md` |
| Base | `6d48318c460bad040fd0754b0300fbcd76a2d312` |
| Reviewed head | `537df59385359ef95382928fa436dc67e8fd24a0` |
| PR | #160 |
| Decision | APPROVED |
| Score | 98/100 |

## 1. Executive decision

**APPROVED — 98/100.**

BKL-041 F2 traduce correttamente il semantic contract F1 in schema, fixture sintetica bounded, identity deterministica e validator fail-closed. L'incremento non materializza score, peso, normalizzazione, contribution o confidence numerica e mantiene l'authority read-only/non-Safety.

Non risultano Blocker, Major o Minor finding aperti. Le observation sono requisiti di ingresso per F3/F4 e non remediation F2.

## 2. Repository truth verificata

| Elemento | Evidenza | Esito |
|---|---|---|
| Baseline F1 | PR #159, merge `6d48318c460bad040fd0754b0300fbcd76a2d312`, ARB 98/100 | F1 correttamente riconciliata Accepted |
| Current package | bootstrap, backlog, handover, baseline e roadmap indicano BKL-041 F2 | coerente |
| Contract | schema 1.0 per profile, evidence, dimension assessment e authority | conforme |
| Fixture | `BOUNDED_SYNTHETIC_FIXTURE`, nessuna session evidence produttiva | confine verificabile |
| Identity | canonical JSON + SHA-256 con known-answer | deterministica |
| Missing evidence | guiding required rappresentato `UNAVAILABLE`, non zero | fail-closed |
| Scientific boundaries | unità SQM/guiding, FWHM calibration e PixInsight completeness validate | conforme |
| Authority | `READ_ONLY`, no acceptance/action authority, Safety locale | conforme |
| Dynamic refresh | non implementato F2; requisito esplicito F4 | boundary preservato |

## 3. Scorecard

| Dimensione | Score | Evidence-based assessment |
|---|---:|---|
| Scope e semantic integrity | 100 | F2 implementa solo profile/evidence/dimension contract e vieta esplicitamente lo scoring. |
| Domain e layer integrity | 99 | Modulo repository-side puro, senza dipendenze runtime, device o presentation. |
| Schema e versioning | 98 | JSON Schema Draft 2020-12, versione/contract type/identity method chiusi e additional properties vietate. |
| Deterministic identity | 100 | object-key ordering, array-order preservation, UTF-8, SHA-256 e preimage rule sono testati con known-answer. |
| Fail-closed behavior | 100 | proprietà sconosciute, tampering, missing required, unità e versioni incompatibili vengono rifiutati. |
| Scientific evidence integrity | 98 | calibration, evidence class, completeness e context-only semantics preservate; formula scientifica resta correttamente rinviata. |
| Safety, security e authority | 100 | no acceptance, action o Safety authority; source locator repository-relative; fixture sintetica. |
| Operability e observability | 96 | diagnostica tramite errori deterministici e gate dedicato; nessun runtime da osservare. |
| Migration e rollback | 99 | additivo e repository-only; nessun dato o consumer esistente migrato. |
| Traceability e continuity | 96 | F1, backlog, bootstrap, handover, baseline e projection governate risultano allineati; navigation rinviata a consumer stabile. |
| Validation evidence | 99 | 12 test locali e cinque workflow exact-head verdi. |

## 4. Findings

### Blocker

Nessuno.

### Major

Nessuno.

### Minor

Nessuno.

### Observations

#### O-01 — F3 weight-set e scale semantics

F3 deve definire e testare weight-set versionato, somma dei pesi, scale/range, rounding, out-of-range behavior e divieto di silent reweighting. Nessun valore numerico è approvato da F2.

#### O-02 — Schema/validator parity

Ogni evoluzione futura dello schema deve aggiungere test di parity fra proprietà JSON Schema e allow-list semantiche per evitare drift. F2 copre l'attuale versione 1.0 con reject delle proprietà sconosciute.

#### O-03 — F4 automatic session refresh

La prima projection/consumer production-ready deve essere integrata nel workflow session-driven e provare la rigenerazione automatica dopo ogni nuova sessione importata, con idempotency e stale/failure behavior.

#### O-04 — Discoverability

La navigation MkDocs può essere aggiornata quando F4 introdurrà una superficie consumer stabile. I file F1/F2 restano comunque indicizzati dalla search e validati dal build strict.

## 5. Architecture and authority review

Il modulo F2 è una funzione pura di validazione repository-side. Non introduce persistence, messaging, API, port adapter o dipendenza verso EAGLE/N.I.N.A./PHD2/PixInsight runtime. Schema e fixture non diventano authority su AP-013/AP-014.

L'envelope impone `consumerMode=READ_ONLY`, `acceptanceAuthority=false`, `actionAuthority=NONE` e `safetyAuthority=LOCAL_PHYSICAL_INTERLOCKS`. Weather rimane context-only. Nessun campo o comportamento consente decisione SAFE/UNSAFE, remediation o device command.

## 6. Validation matrix

| Gate | Stato | Evidenza |
|---|---|---|
| Local contract verifier | Passed | 7 evidence, 9 dimension assessments, digest `c59c5fdf0d1beff1b5a72c6085fe4982373fb0bf6066a0cbe655f6d7ec0e9727` |
| Local fail-closed tests | Passed | 12/12 |
| Node syntax | Passed | tre moduli `.mjs` |
| JSON/YAML syntax | Passed | schema, fixture e workflow |
| BKL-041 F2 Governance | Passed | #4, run `34566976225` |
| Developer Foundation | Passed | #1283, run `34566976219` |
| Scientific Platform Governance | Passed | #38, run `34566976245` |
| Validate documentation | Passed | #916, run `34566976250` |
| Genera manuale Word | Passed | #1341, run `34566976257` |
| Runtime/OAT | Not Applicable | nessun runtime o consumer F2 |
| Device/Safety validation | Not Applicable | nessun device o Safety change |

## 7. Migration, compatibility e rollback

- additive contract 1.0; nessun contratto esistente modificato;
- nessuna migrazione dati o persistenza;
- fixture sintetica non è production evidence;
- nessuna modifica alla pipeline automatica di import;
- rollback mediante revert dei file F2 e dei riferimenti di continuity/roadmap.

## 8. Decision and re-review criteria

Il PR #160 è **APPROVED FOR RELEASE QUALITY REVIEW** per il solo scope F2.

F3 richiede nuova ARB review su formula, normalizzazione, weight set, confidence, decomposition, sensitivity/bias e known-answer score. F4 richiede review su pipeline session-driven, consumer, automatic refresh, stale behavior e publication evidence.

L'approvazione F2 non autorizza F3/F4, score operativo, ranking, automatic acceptance, remediation, device command o Safety Authority.

