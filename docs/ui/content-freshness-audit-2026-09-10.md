# Content Freshness and Legacy Audit — 10/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-UI-AUD-001 |
| Stato | Completed |
| Data | 10/09/2026 |
| Baseline verificata | b49a7f99ca89d93e8ca55043a810f14abfcba29a |
| Ambito | Pagine pubblicate, navigation, projection e pipeline GitHub Pages |

## 1. Metodo

Sono stati confrontati:

- HEAD main e albero repository;
- mkdocs.yml, homepage, hub e script UI;
- roadmap e Scientific Platform status generati;
- catalogo sessioni e latest observation;
- workflow di import, Analytics e deploy Pages;
- documenti Design System, release e publication governance.

## 2. Findings

| ID | Evidenza | Classificazione | Trattamento UI 7.0 |
|---|---|---|---|
| FR-01 | Homepage: AP-013 in corso, 3 sessioni, 31,83 h | Stale critico | Rimosso; placeholder fail-closed e hydration da projection |
| FR-02 | Storico corrente: 15 sessioni e 101,50 h | Fonte governata | Proiettato nella homepage |
| FR-03 | refresh_homepage.py mutava markup con valori statici durante il build Pages | Debito legacy | Riproposto come validator non mutante del contratto fail-closed |
| FR-04 | docs/index.md assente dai governed_paths | Vincolo di publish | Nessuna modifica privilegiata: il file resta strutturale e i dati arrivano via JSON no-store |
| FR-05 | 15 gruppi top-level MkDocs | Debito UX | Consolidati in 6 percorsi principali più Home |
| FR-06 | Custom navigation con link statici AP-013 | Stale | Sostituita con hub stabili e package dinamico |
| FR-07 | Scientific Intelligence con milestone AP-013/M3.3 statica | Stale | Convertita a consumer della projection governata |
| FR-08 | Repository Intelligence/Analytics con contatori statici | Legacy duplicato | Ritirate come viste metriche; rimando a Roadmap/Documentation |
| FR-09 | Roadmap URL con cache-buster BKL-040 datato | Legacy tecnico | Rimosso; fetch no-store mantenuto |
| FR-10 | Design System e Publication Guidelines Draft dal 26/07 | Governance stale | Revisionati per UI 7.0 |
| FR-11 | Handover e baseline datati 30/08–09/09 | Storico intenzionale | Conservati come snapshot, esclusi dai percorsi primari |
| FR-12 | analyze-session.yml.disabled e history-backup 22/07 | Artefatti legacy non pubblicati | Conservati fuori dalla UX; nessuna cancellazione autorizzata |

## 3. Pagine dinamiche e contratto di refresh

| Superficie | Fonte | Aggiornamento | Esito audit |
|---|---|---|---|
| Homepage | roadmap + sessions/targets/metadata | ogni import sessione | Corretto in UI 7.0 |
| Observatory Status | relay + fallback repository | polling 15 s, fail-closed | Conforme |
| Latest Observation | latest-observation.json | ogni import sessione | Conforme |
| Session Explorer/Detail | scientific-session-catalog.json | ogni import sessione | Conforme |
| Session Reports | package report + indice | ogni import sessione | Conforme |
| Analytics Center | storico consolidato | ogni import sessione | Conforme |
| Equipment Performance | projection BKL-039 | ogni import sessione | Conforme |
| Session Comparison | projection BKL-037 | ogni import sessione | Conforme |
| Roadmap | roadmap.json | ogni variazione governata | Conforme |
| Scientific Platform status | scientific-platform-status.json | ogni variazione roadmap | Conforme |

## 4. Regole conseguenti

1. Nessuna pagina primaria replica manualmente current package, conteggio sessioni o ore di integrazione.
2. I fallback mostrano loading/unknown, non vecchi valori plausibili.
3. Le pagine storiche rimangono datate e non vengono presentate come current.
4. Le viste duplicate prive di generatori vengono consolidate o marcate Superseded.
5. Le nuove sessioni devono produrre un unico commit coerente delle projection dipendenti; i consumer runtime non duplicano tali dati nel markup.
6. Il deploy Pages viene attivato soltanto dopo il publish delle projection.

## 5. Debito residuo

- Gli artefatti tecnici legacy non pubblicati restano nel repository perché la loro cancellazione è fuori ambito.
- Il nome legacy refresh_homepage.py è conservato perché referenziato dal workflow Pages; la sua semantica corrente è di validazione.
- La verifica visuale cross-browser automatizzata non è parte della pipeline corrente.
- Il contenuto storico può citare stati precedenti purché data e natura di snapshot siano esplicite.

## 6. Conclusione

Il rischio principale non era soltanto grafico: la homepage duplicava valori fuori dal ciclo automatico di aggiornamento scientifico. UI 7.0 elimina la duplicazione e consuma le projection già aggiornate dal workflow, senza ampliare permessi o automazioni di push/deploy.
