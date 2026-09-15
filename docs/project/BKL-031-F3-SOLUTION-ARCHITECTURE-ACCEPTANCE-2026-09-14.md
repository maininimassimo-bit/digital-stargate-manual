# BKL-031 F3 — Solution Architecture Acceptance Record

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-SA-ACCEPTANCE-001 |
| Stato | **ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED — NOT IMPLEMENTED** |
| Data | 14/09/2026 |
| Capability | BKL-031 — Observation Planner intelligente |
| Incremento accettato | F3 — Governed Site/Setup and Ephemeris/Lunar Solution Architecture |
| Pull request | [#191](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/191) |
| Technical head reviewed | `43a46ac28c30badc40e4cb180ed98924ebcf74a1` |
| Review-publication head | `d0f8098cfff9651b3ba1597fd77f09a11a7c634a` |
| Merge commit | `3a79bb93c9a0925280eba5214d517107804cb13c` |
| Successore | Decisione owner pending; nessuna implementation slice promossa |
| Runtime impact | None |
| PC Principale / EAGLE | Nessuna azione richiesta |

## 1. Decisione

Il Solution Architecture Package F3 è accettato con condizioni come baseline source-neutral per integrare in futuro:

- S08 — identità, posizione geodetica e timezone IANA governate;
- S09 — assegnazione del setup corrente con approvazione, validità e conflitto;
- S10 — richiesta, metodo, dati e projection ephemeris/lunare riproducibili.

L'accettazione riguarda esclusivamente architettura, contratti proposti, boundary, ordine di migrazione e validation plan. Non accetta né dichiara implementati record reali, provider, librerie, kernel, ADR, schema, fixture, validator, adapter, cache, projection o consumer runtime.

BKL-031 resta `In Progress`. Nessuna slice F3-A1, F3-A2, F3-A3, F3-B o F3-C è promossa.

## 2. Evidenza di integrazione

| Evidenza | Stato |
|---|---|
| F3 handoff PR #190 | integrated/post-merge verified |
| PR #191 technical head | `43a46ac28c30badc40e4cb180ed98924ebcf74a1` |
| ARB AI-assisted | APPROVED WITH CONDITIONS — 98/100 |
| Release Quality AI-assisted | CONDITIONALLY READY FOR MERGE |
| Review-publication head | `d0f8098cfff9651b3ba1597fd77f09a11a7c634a` — 7/7 SUCCESS |
| Merge | `3a79bb93c9a0925280eba5214d517107804cb13c` |
| Post-merge | 9/9 SUCCESS |
| Merge-control waiver | `W-BKL031-F3-SA-MERGE-001` — CONSUMED / EXPIRED |

Le review sono owner-authorized e AI-assisted, non equivalenti ad approvazioni umane indipendenti.

## 3. Ambito accettato

- source inventory e separazione fra conceptual/historical/derived authority;
- `GovernedSiteRecord`, `CurrentSetupAssignment`, `EphemerisLunarRequest` e `EphemerisLunarEvidence` come contratti architetturali;
- porte Application e adapter Infrastructure source-neutral;
- UTC, IANA timezone, time scale, frame, epoch, datum e refraction semantics;
- precision/error-budget gate prima di `AVAILABLE`;
- fail-closed missingness, conflict, coverage, provider e cache behavior;
- exact-site privacy e sanitized public projection;
- esecuzione futura fuori da EAGLE;
- osservabilità, NFR, migrazione e rollback;
- validation plan P01–P10/N21–N66.

Le alternative Astropy/JPL, Skyfield/JPL e JPL Horizons restano candidate non selezionate.

## 4. Condizioni trasferite

| ID | Stato | Gate |
|---|---|---|
| ARB-191-MI01 | Open / carried | separare il digest interno del record sito dal riferimento pubblico non correlabile; obbligatorio prima di F3-B/F3-C |
| ARB-191-MI02 | Open / carried | definire intervalli UTC half-open `[validFromUtc, validToUtc)`, end unbounded esplicito e test di adiacenza; obbligatorio prima di F3-A1/F3-A2/F3-B |
| ARB-191-O02 | Observation / carried | mantenere convenzione Moon phase univoca per nome, direzione e wrap |
| AI review independence | Disclosed | non rappresentare le review come approvazioni umane indipendenti |

Nessuna condizione è chiusa dalla sola acceptance documentale.

## 5. Quality gates

| Gate | Stato | Evidenza |
|---|---|---|
| Architecture | Passed with conditions | ARB 98/100; nessun Blocker/Major |
| Scope and dependency order | Passed | F3-A1/A2/A3/B/C non promosse |
| Documentation and links | Passed | PR #191 exact-head e post-merge workflow |
| Developer Foundation | Passed | #1401 / `34888655796` |
| Documentation validation | Passed | #1038 / `34888655824` |
| Word/manual | Passed | #1464 / `34888655795` |
| Governed projections | Passed | #40 / `34888655833` |
| Scientific Platform Governance | Passed | #101 / `34888655767` |
| Pages publication | Passed | #797 / `34888655790` |
| BKL-041/BKL-046 regressions | Passed | #103/#77/#62 |
| Security/privacy | Passed with condition | exact coordinates excluded; MI01 carried |
| Time/current validity | Passed with condition | MI02 carried |
| Safety | Passed | no readiness, command or Safety Authority |
| Runtime/OAT | Not Applicable | architecture-only increment |
| Scientific accuracy campaign | Not Executed | provider/error budget not selected |
| Implementation tests P01–P10/N21–N66 | Not Executed | no implementation exists |
| Independent human approval | Not Executed | AI-assisted disclosure retained |

## 6. Post-merge workflows

| Workflow | Run | Esito |
|---|---:|---|
| Developer Foundation #1401 | 34888655796 | SUCCESS |
| Validate documentation #1038 | 34888655824 | SUCCESS |
| Genera manuale Word #1464 | 34888655795 | SUCCESS |
| Deploy MkDocs artifact to GitHub Pages #797 | 34888655790 | SUCCESS |
| Governed Projection Sync #40 | 34888655833 | SUCCESS |
| Scientific Platform Governance #101 | 34888655767 | SUCCESS |
| BKL-041 F4 Governance #103 | 34888655773 | SUCCESS |
| BKL-046 F4 governance #77 | 34888655781 | SUCCESS |
| BKL-046 F5 governance #62 | 34888655782 | SUCCESS |

## 7. Rischi e waiver register

| ID | Stato | Disposizione |
|---|---|---|
| W-BKL031-F3-SA-MERGE-001 | **CONSUMED / EXPIRED** | limitata a PR #191 e head `d0f8098cfff9651b3ba1597fd77f09a11a7c634a`; non riutilizzabile e nessun precedente |
| ARB-191-MI01 | Open / carried | implementation gate, nessuna deroga |
| ARB-191-MI02 | Open / carried | implementation gate, nessuna deroga |
| provider/library/kernel/error budget | Open | decisione ADR separata |
| real site/setup authority | Not materialized | S08/S09 restano unavailable |
| implementation/runtime | **NOT AUTHORIZED** | richiede nuova decisione owner |

## 8. Preserved boundaries

- S08 resta `UNAVAILABLE` finché non esiste un record approvato;
- S09 resta `UNAVAILABLE_CURRENT` finché non esiste un assignment approvato interval-valid;
- S10 resta `UNAVAILABLE` finché ADR, metodo, dati e validazione non sono accettati;
- S07 resta current-unavailable e S11 appartiene a F4;
- F5 conserva pesi, scoring, ranking e consumer;
- BKL-032 conserva readiness/go-no-go;
- interlock fisici/locali restano l'unica Safety Authority;
- nessun workload o external call è autorizzato su EAGLE.

## 9. Rollback e impatto operativo

L'incremento accettato è documentale. Il rollback è il revert del merge #191; non richiede migrazione dati, rotazione credenziali, modifica di scheduled task, deployment runtime o azioni hardware.

## 10. Next governed action

Il primo candidato dependency-ordered è F3-A1 — Site Authority Contract. Una sua eventuale promozione richiede una nuova autorizzazione owner e deve includere la chiusura di ARB-191-MI02 prima della materializzazione.

Questa acceptance non autorizza F3-A1 né F3-A2/A3/B/C, provider/ADR, record reali, schema/fixture/validator/adapter, dipendenze, chiamate esterne, forecast, ranking, readiness, runtime, device command, PC/EAGLE o Safety Authority.

## 11. Current governance stop after ARB-192-M01 third remediation

La seconda re-review AI-assisted sull'exact head `cb519f8e7a36fea3919f7e6cc1f417d5fad09147` ha mantenuto `ARB-192-M01` aperto per la riga autorevole BKL-031 del backlog. La remediation del 15/09/2026 riallinea esclusivamente quella riga allo stato F3 accepted-with-conditions/post-merge-verified/not-implemented, preservando BKL-031 `In Progress` e tutti i boundary.

Dopo la CI sull'exact head della terza remediation, fermarsi prima di una nuova ARB/Release Quality re-review, del merge, di qualsiasi decisione ruleset/waiver e di ogni implementazione F3. `ARB-191-MI01` e `ARB-191-MI02` restano aperti; nessuna F3-A1/A2/A3/B/C è promossa.
