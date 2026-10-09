# Current Technical Baseline — 2026-10-07

## Stato corrente — 9 ottobre 2026

P6 resta Accepted nei limiti del dossier. BKL-051 resta aperta. PR #520 dossier preliminare privato rilasciata su `bb68404e836c532986453c682846105e7fb5ce3a`: 15 workflow exact-head e 15 post-merge SUCCESS, ARB/RQ approvate senza finding e sette endpoint Pages verificati. Caller #519 e recovery #518 rilasciati. Due build circoscritte autorizzate separatamente: prima FAILURE per il percorso di una prova, seconda SUCCESS con 155/155 prove cloud offline e digest immutabile registrato. Runtime verificato ancora sulla revisione P6. Nuovo run tecnico sintetico 64×64 preparato, preflight offline PASS, non avviato o registrato sul cloud. Proposta concreta di attivazione/OAT temporanea in privato, decisione Owner pendente; nessuna credenziale nuova o modifica IAM. Dataset pubblico Atami preparato con tre FITS g e maschere, timing/bit-mask riconciliati nelle fonti; nessuna rilevazione o validazione scientifica. Invii disattivati. Restano PC/cloud OAT, workflow scientifico, calibrazione/uncertainty, validation, policy, oggetti mobili e adattatori produttivi. S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. Nessuna nuova elaborazione fotografica PixInsight. F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva; S10/Safety invariati. [Handover corrente](HANDOVER_2026-10-09-BKL051-BUILD-READINESS.md).

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-20261007 |
| Versione | 1.1 |
| Stato | P6 Accepted operativamente con limiti; PR #499 delivery gate; BKL-051 S1 preparazione |
| Handover | [7 ottobre](HANDOVER_2026-10-07-P6-CLOSURE.md) |

Questa baseline aggiorna sequencing ed evidenza locale, senza ricertificare deployment o runtime. La [baseline del 6 ottobre](CURRENT_TECHNICAL_BASELINE_2026-10-06.md) resta valida per le identità dei servizi e i limiti dei rilasci descritti.

| Area | Stato corrente |
|---|---|
| BKL-049 archivio | Closed nel perimetro accettato, non riaperta |
| BKL-049-EXT-PIAI/P6 | Accepted operativamente 07/10 con limiti del dossier, inclusi HOO tecnico e CFA singola esposizione; gate di consegna PR #499 |
| BKL-051 | In Progress — preparazione S1; sviluppo dopo delivery P6 verificata, nessun modulo/servizio/scansione implementati |
| BKL-043 F4/F5 | F4 lifecycle reale e accettazione finale pendenti; F5 solo dopo piena accettazione F4 |
| BKL-050 | Planned, ultima dopo BKL-051 e tutte le altre dipendenze approvate |
| S10 e Safety | S10 UNAVAILABLE; interlock locali e authority dei dispositivi invariati |

L'accettazione privata SHO riguarda il prodotto e non prova una nuova catena Owner HTTP → nativo → download né chiude i residui P6. History e classificazioni restano limitate alle evidenze effettive; nessuna pubblicazione gallery è implicita. Nessun dato scientifico privato è incluso nella presente baseline.

[Piano BKL-051](BKL-051-SCIENTIFIC-TRANSIENT-CANDIDATES-2026-10-07.md), [dossier P6](PIAI-P6-CANDIDATE-2026-10-06.md), [evidenza minimizzata](evidence/BKL-051-OWNER-PLAN-2026-10-07.json).


## Incremento P6 isolato

Owner approva servizio, due bucket privati, identità e credenziale di prova dedicate. Ambiente cloud isolato attivo sul digest già rilasciato; concorrenza Owner e recupero nativo cloud reali ancora da eseguire. CFA/SHO reali e download CFA riconciliati con limiti espliciti. P6 resta aperta; accettazione operativa finale pendente. Nessuna mutazione del pilota operativo, gallery, dispositivi o Safety. BKL-051 Planned dopo chiusura P6. Piano corrente: [PIAI-P6-ISOLATED-OAT-2026-10-07.md](PIAI-P6-ISOLATED-OAT-2026-10-07.md)

## P6 — collaudo completo, accettazione operativa pendente

Concorrenza Owner HTTPS reale, interruzione nativa isolata e nuovo worker, offline oltre 120 s, restart/rollback/forward del servizio di prova: PASS nei limiti documentati. Ambiente sospeso, archivi e prenotazioni conservati; stato della coda operativa byte-identico al baseline. HOO nativo sui master reali Drizzle2 ora PASS tecnico: 26 processi, 14 checkpoint, 26 coppie History, originali invariati; non accettazione estetica. P6 resta aperta per accettazione operativa; CFA è fixture tecnica da singola esposizione con decisione scientifica pendente. BKL-051 Planned dopo chiusura P6; F4/F5 e BKL-050 invariati. [Dossier finale e limiti](PIAI-P6-OPERATIONAL-ACCEPTANCE-2026-10-07.md). Questa nota supera soltanto i residui tecnici provati, conserva snapshot e gate di consegna.

## P6 — accettazione operativa Owner

L’Owner conferma «Accetto operativamente P6 con i limiti del dossier». Nessuna esclusione HOO: collaudo nativo completato. Accettazione distinta da valutazione estetica e pubblicazione; CFA resta prova tecnica su singola esposizione, History a monte non attestata e recupero soltanto conservativo. [Chiusura](BKL-049-EXT-PIAI-P6-CLOSURE-2026-10-07.md), [handover](HANDOVER_2026-10-07-P6-CLOSURE.md). Gate di consegna exact-head e post-merge nella PR #499; nessun PASS anticipato.


## BKL-051 S1 — preparazione autonoma del 7 ottobre

P6 delivery verificata sulla PR #499 e sul merge `0bd6e20df0b449cd163543ed30bd69d9264862b0`: 16/16 workflow post-merge SUCCESS incluse Pages e proiezioni pubbliche conformi. [Handover corrente](HANDOVER_2026-10-07-BKL051-S1.md), [fattibilità e contratto proposto](BKL-051-S1-FEASIBILITY-AND-CONTRACT-2026-10-07.md). Accessi pubblici limitati verificati, tentativi negativi conservati, nove test di intake offline. S1 non accettata: decisioni su architettura/trasporto, query minime su campi Owner e dataset pilota ancora pendenti. Nessuna soglia, analisi Owner, runtime o foto pubblicata. Le sezioni precedenti restano snapshot storici.
