# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 8.6 |
| Baseline | 05/10/2026 |
| Stato | Current root bootstrap — BKL-043 F4 lifecycle pending; BKL-049 archive closed; PixInsight AI extension pilot; S10 unavailable |

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale
Il repository GitHub è l'unica fonte autorevole. Memoria, conversazioni e projection non prevalgono sul repository corrente.

## 2. Sequenza obbligatoria di lettura
1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-10-05-BKL049-PIXINSIGHT-AI.md`
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-10-05.md`
4. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`
5. `docs/project/REPOSITORY_KNOWLEDGE_MAP.md`
6. `docs/project/BACKLOG.md`
7. `.github/roadmap/roadmap-source.json`
8. `docs/data/roadmap.json` — generated projection, non authority
9. `docs/project/TECHNICAL_DEBT.md`
10. `docs/project/DECISION_LOG.md`
11. `docs/project/DEVELOPMENT_WORKFLOW.md`
12. `docs/project/DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md`
13. `docs/project/CODING_STANDARDS.md`
14. `docs/project/RELEASE_PLAYBOOK.md`
15. `docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`
16. package, ADR, review, evidence e componenti direttamente coinvolti.

Gli handover e le baseline precedenti restano snapshot storici.

## 3. Stato corrente
- BKL-031: **Closed / Accepted / Post-Merge Verified** via PR #301 merge `4a509d574a004fe7fb72bc6c678c9e7f71fe821f`.
- F3–F8: Accepted/Post-Merge Verified.
- F8 implementation: PR #279, reviewed head `3f05693482208df2b56b66dcb71162589880e72b`, merge `20669f7164460297d7318fc3b5874e4bc7f4bcde`, 9/9 exact-head e 10/10 post-merge SUCCESS.
- F8 acceptance reconciliation: PR #280, reviewed head `bca410dcde804483052beded16c29a9f58f43872`, merge `84d1b889a6c739c9e5d053e1f073fe1d87b8c5d4`, 17/17 exact-head e 19/19 post-merge SUCCESS; GitHub Pages build/integrity/deploy SUCCESS.
- F8 evidence: notte bounded 17–18/09/2026, forecast reale F7 site-specific, astronomia night-specific, suitability OTA/camera/filter esplicita, ranking/finestre advisory read-only.
- BKL-032 Session Readiness / Go-No-Go Decision Support è Closed / Accepted / Post-Merge Verified via PR #304; il suo evaluator resta read-only e il runtime source/transport è separatamente gated.
- BKL-036 è Closed come capability repository-only bounded; F3 Health Score resta `UNAVAILABLE`.
- AP-007 è **Accepted with conditions** come architecture baseline; non è un servizio operativo verificato.
- AP-008 è chiuso nel perimetro bounded read-only; non abilita command path, remediation o Safety Authority.
- BKL-042 è **Closed / Accepted** nel perimetro bounded read-only con limiti OAT espliciti.
- BKL-043 resta corrente: F4 attende lifecycle e accettazione finale secondo lo stato del 1 ottobre. BKL-049 archivio chiusa; M27 e importer aggiornati nel nuovo handover. Estensione BKL-049-EXT-PIAI autorizzata sul PC Owner, non produzione.
- S10 production runtime: `UNAVAILABLE`.

## 4. Boundary non negoziabili
- local physical interlocks = Safety Authority;
- BKL-032 = Session Readiness / Go-No-Go decision-support authority;
- BKL-031 = advisory/read-only, nessuna readiness/safety/action authority;
- nessun scheduler, automatic target selection o device command;
- coordinate sito protette mai in projection pubbliche;
- missing/stale/conflicted evidence fail-closed;
- provider/model/run lineage esplicita, nessun fallback/stitching silenzioso;
- il traffico MeteoHub F9 resta entro il modello ADR-012 governato: nessun limite giornaliero imposto dal workflow, budget EUR 0, fail-closed e GRIB effimeri.

## 5. Provider budget corrente
- F4-C generalized validation: `2/2_EXHAUSTED`;
- F7 protected-site one-shot: `1/1_EXHAUSTED`;
- F8: zero provider requests;
- F9 closure: refresh MeteoHub governato verificato; nessuna estensione di traffico oltre il limite ADR-012.

## 6. Disciplina di delivery
Exact-head CI → ARB → Release Quality sullo stesso SHA → expected-head merge → post-merge verification → acceptance reconciliation. Nessuna acceptance o runtime claim può precedere l'evidence reale.

## 7. Punto di ripresa
Riprendere dall’handover del 5 ottobre v2.0 e dal runbook PIAI-P4-CLOUD-ACTIVATION-2026-10-05.md v1.1. P1–P3 e candidato P4 consegnati #479–#482; attivazione #483 post-merge verificata. P4 Owner HTTP sintetico, non-Owner negato, IAM/restore, restart/lost-ack, CAS GCS concorrente amministrativo e trasporto nativo amministrativo M27 verificati. P4 acceptance operativa resta aperta e concorrenza HTTP Owner soltanto sintetica; P5 è tecnicamente completata: prova scientifica Owner UI/nativa/consegna privata verificata; P6 e accettazione scientifica Owner sono successive. SESSION_ASSISTED senza nuove API IA; M27 pubblicata invariata, BKL-043 conserva i propri gate, nessuna authority dispositivi/Safety. Consegna CI/review e Pages della riconciliazione attuale da tracciare sulla PR.


## Aggiornamento P5 — portale scientifico privato (2026-10-05)

Implementato il candidato P5: pagina Owner, selezione di master M27 registrati, sessioni/catalogo e versione di riferimento esatti; job con contesto immutabile e verifica sul PC prima delle copie; stato/cancel espliciti, preview privata, workflow delle 29 azioni, correlazioni runtime e revisione Owner vincolata alla ricevuta. Originale e journal completo restano sul PC. Le identità IMG/VER/WF del pilota sono private e distinte dall’archivio di pubblicazione; nessun caricamento o pubblicazione automatica. SESSION_ASSISTED senza nuove API IA; classificazioni WORKER_REPORTED_NOT_ATTESTED, OWNER_DECLARED e History a monte NOT_ESTABLISHED preservate. Release/deployment consegnati tramite #485; la prova scientifica reale HTTP/UI → PixInsight → consegna/revisione resta un gate P5 aperto, non sostituito dai test. P6 e acceptance scientifica Owner restano successivi. [Procedura P5](docs/project/PIAI-P5-PORTAL-2026-10-05.md).

## Rilascio P5 del 5 ottobre — prova scientifica Owner ancora aperta

PR #485 integrata nel commit `f1a4650dfb8da54c498b763752fd4d5d2b8877ad`: 20/20 check sullo head revisionato, ARB e RQ AI-assistite sequenziali PASS con zero finding residui; 22/22 check post-merge e deployment Pages effettivo SUCCESS. Cloud Build del codice revisionato PASS con 77 test; digest `sha256:b6d14fa1934076f16f0c44721fdc2852dd5e49f68bd21bf3cae0cf54b38e1ee0`, revisione `dsg-pixinsight-pilot-p5-science-01`, traffico 100%. Nessuna nuova risorsa, credenziale o estensione IAM. Registrazione reale di un gruppo M27 dopo verifica dei quattro master e ripetizione idempotente PASS.

La pagina scientifica è pubblicata e aperta; il completamento tecnico P5 richiede ancora accesso Owner sulla nuova pagina, creazione scientifica HTTP/UI, nuova esecuzione nativa e consegna/revisione privata con sessioni esatte. Non sostituire questa prova con fixture amministrative, prove P4 o accettazione scientifica simulata. Le dipendenze dei master nelle correlazioni cloud usano i ruoli, mentre il grafo originale e gli hash individuali restano sul PC. P6 e accettazione scientifica Owner rimangono aperti. La M27 pubblicata non è stata modificata. Questa riconciliazione documentale richiede i propri gate di consegna.

## Correzione compatibilità target durante il collaudo P5

Accesso Owner sulla nuova pagina verificato. Nessun job scientifico creato: confronto letterale `M27`/`M 27` rendeva invisibili le sessioni e il parent reali. Correzione con soli due alias espliciti, contesto originale conservato, tre regressioni e verifica locale dei profili pubblici reali (16 sessioni/un parent). Correzione candidata da rilasciare; il percorso Owner HTTP → nativo → consegna privata resta aperto. [Procedura P5](docs/project/PIAI-P5-PORTAL-2026-10-05.md).


## P5 — prova tecnica completa del 5 ottobre 2026

P5 è tecnicamente completata nel perimetro M27 del pilota: richiesta reale dalla pagina autenticata Owner, un gruppo di master registrato, tutte le 16 sessioni M27 e l'esatta versione pubblicata di riferimento; preparazione con verifica del contesto prima delle copie, nuova esecuzione supervisionata in PixInsight sul PC Owner, raccolta verificata e consegna privata. Sono state eseguite 29 operazioni, prodotti 15 checkpoint e verificati tutti i pixel finali del risultato RGB Float32 non lineare 4634×2808. I quattro master sono rimasti invariati. Anteprima privata e 29 passi del workflow sono stati consultati nell'interfaccia Owner. Workflow, correlazioni e ricevuta conservati dal servizio sono stati letti con la CLI amministrativa già autorizzata e confrontati con le impronte e i derivati locali: PASS. Questa lettura è distinta dal salvataggio sul PC tramite i pulsanti del browser. La M27 pubblicata conserva la stessa versione e lo stesso workflow.

La correzione dei soli alias `M27` e `M 27` è consegnata con PR #487: head revisionato `912d433345db0dc053f9e70466c1f2a340b23032`, 9/9 check exact-head, ARB e RQ AI-assistite separate e sequenziali senza finding; merge `85fea6c2955471427a50d93adf01aef2b4808350`, 10/10 check post-merge inclusa Pages effettiva SUCCESS. Cloud Build `60d5ab2b-a855-4da0-ac29-bb2e73d00835` SUCCESS con 80 test; revisione `dsg-pixinsight-pilot-p5-target-01`, digest `sha256:c6a4c7ead3035d896afda66b3f3580473418cb19f9ec92478f7cfb2ecbe9f993`, traffico 100%. Fonte e identità scientifiche originali conservate; nessuna nuova risorsa, credenziale o estensione IAM.

L'Owner ha accettato il risultato privato: `ACCEPT_PRIVATE` osservato nella pagina autenticata dopo la conferma umana del 5 ottobre. Nessun pulsante di accettazione/rifiuto è stato premuto dall'assistente e nessuna pubblicazione è avvenuta. Le sessioni restano `OWNER_DECLARED`, l'evidenza di esecuzione `WORKER_REPORTED_NOT_ATTESTED`, il workflow `RUNTIME_RECIPE_ONLY` e la History a monte `NOT_ESTABLISHED`. L'Owner conferma che entrambi i pulsanti workflow e collegamenti/ricevuta funzionano e salvano i file nella cartella Download (`PASS_OWNER_REPORTED_DOWNLOADS_FOLDER`). È una conferma umana del trasferimento browser → file locale, distinta dalla precedente verifica amministrativa degli asset e senza confronto indipendente degli hash dei file scaricati. La catena tecnica P5 richiesta → nativo → consegna privata → anteprima/workflow è provata. Dopo il ricaricamento della pagina, riaprire «Apri anteprima e workflow» nella sezione Stato delle elaborazioni per riabilitare i download. P6 deve completare acceptance operativa, casi errore/annullamento/offline/crash recovery e rollback secondo il piano, senza confondere i test sintetici con prove reali. SESSION_ASSISTED, zero nuove chiamate API IA; originali e journal completo sul PC. Le precedenti sezioni P5 pending sono snapshot storici superati da questo aggiornamento. La presente riconciliazione documentale conserva i propri gate CI → ARB → RQ → merge → Pages, registrati nella PR di consegna. [Procedura P5](docs/project/PIAI-P5-PORTAL-2026-10-05.md), [evidenza minimizzata](docs/project/evidence/BKL-049-PIAI-P5-2026-10-05.json).
