# Digital StarGate — Current Technical Baseline — 2026-09-06

| Campo | Valore |
|---|---|
| Stato | Active technical baseline after BKL-015 closure |
| Scope | Repository Knowledge Graph F1-F3 plus unchanged operational baseline |
| BKL-015 implementation merge | `c1a9f96b34a23407c5804e7fd6facfbad226f8fc` |
| BKL-015 | DONE / ACCEPTED |
| TD-008 | RESOLVED |
| Next governed capability | BKL-044 Knowledge Graph / AI Evidence Contract |
| Does not supersede | ADR, Architecture Package, OAT storiche o runtime evidence approvate |

## 1. Finalità

Questa baseline registra lo stato tecnico verificato al termine di BKL-015. Le baseline precedenti restano fotografie storiche valide.

## 2. Repository Knowledge Graph

La baseline repository-centric comprende:

- schema machine-readable versionato;
- entity IDs stabili;
- source locator verso repository authority/evidence authority;
- relazioni tipizzate/versionate;
- projection dichiaratamente non-authoritative;
- AP/ADR identity coverage al 100%;
- component/evidence identity coverage al 100% sull'Architecture Artifact Register governato;
- material-relation coverage al 100% sul medesimo registro;
- CI fail-closed per integrità, coverage e material relations.

Projection:

`docs/data/knowledge-graph.json`

Validation:

- `.github/scripts/verify-knowledge-graph.mjs`;
- `.github/scripts/verify-knowledge-graph-coverage.mjs`;
- `.github/scripts/verify-knowledge-graph-material-relations.mjs`.

## 3. Authority model

Il Knowledge Graph non sostituisce le fonti canoniche. Repository documents/registers restano authority; `docs/data/knowledge-graph.json` è una projection interrogabile e verificabile.

Nessuna inferenza automatica può trasformare una relazione non documentata in repository truth.

## 4. BKL-015 closure

BKL-015 è completato attraverso F1, F2 e F3.

Il merge F3 `c1a9f96b34a23407c5804e7fd6facfbad226f8fc` ha superato i workflow post-merge Developer Foundation #963, Validate documentation #572, Pages #685 e Word #997.

La closure review combinata conclude `DONE / ACCEPTED` per BKL-015.

## 5. TD-008 closure

TD-008 Knowledge Traceability è `RESOLVED` perché AP, ADR, componenti ed evidence — le quattro classi esplicitamente dichiarate dal debito — dispongono ora di rappresentazione machine-readable governata e gate di riconciliazione.

La closure non implica completezza semantica per scientific claims, AI confidence, recommendation provenance o runtime inference. Queste evoluzioni appartengono a BKL-044 e package successivi.

## 6. BKL-044 boundary

BKL-044 deve definire il Knowledge/AI Evidence Contract sopra la foundation chiusa da BKL-015.

Sono fuori dalla baseline corrente:

- graph database persistente;
- vector database;
- RAG runtime;
- AI inference engine;
- automatic knowledge mutation;
- AI/Safety Authority;
- command/remediation path.

Qualunque introduzione strutturale di queste capability richiede governance separata.

## 7. Runtime scientifico EAGLE

La closure BKL-015 non modifica il runtime EAGLE.

`DigitalStarGate.Reporting 1.0.8` resta la baseline runtime scientifica nota.

Runtime repository operativo:

`C:\DigitalStarGate\digital-stargate-manual-ap14-runtime`

Deve rimanere su `main`, con working tree pulito e `HEAD == origin/main` prima di session import o modifiche operative.

## 8. BKL-030 / Observatory Status

BKL-030 resta CLOSED / ACCEPTED. Restano invariati:

- collector EAGLE read-only;
- history append-only;
- Cloud Run EAGLE Health channel;
- portal consumer read-only;
- nessuna severity policy approvata;
- nessuna remediation automatica;
- Safety Authority fuori scope.

## 9. AP-013 transport

AP-013B resta rollback comportamentale `COPY_ONLY`. AP-013C resta chiuso per DRY_RUN/NO_DELETE e non autorizza cleanup produttivo C8/source.

`F:\Astrofotografia` resta destinazione autorevole e non cleanup target.

## 10. Safety / security

- Safety Authority fisica/locale indipendente;
- Knowledge Graph e AI non sono Safety Authority;
- nessun command endpoint introdotto;
- nessuna remediation automatica;
- stale/missing/conflicting evidence non produce stato o conoscenza simulata;
- nessun secret deve essere incorporato nella projection.

## 11. Continuity

Documenti correnti da leggere:

1. `AI_BOOTSTRAP.md`;
2. `docs/project/HANDOVER_2026-09-06.md`;
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-06.md`;
4. `docs/project/BACKLOG.md`;
5. `docs/project/TECHNICAL_DEBT.md`;
6. `docs/data/knowledge-graph.json`;
7. review/evidence del package direttamente interessato.

## 12. Next gate — BKL-044

Il prossimo package governato è **BKL-044 Knowledge Graph / AI Evidence Contract**.

Dovrà preservare repository authority e introdurre semantiche scientifiche/AI esplicite senza trasformare la foundation BKL-015 in un motore di inferenza o in un control plane.
