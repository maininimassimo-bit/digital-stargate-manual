# BKL-046 — Riapertura: AI Post-Processing Assistant for PixInsight

| Campo | Valore |
|---|---|
| Data | 13/10/2026 |
| Stato | REOPENED / In Progress |
| Autorità | Richiesta esplicita dell’Owner nella chat di progetto |
| Baseline storica | F1–F5 advisory deterministica read-only, PR #181 |
| Ambito immediato | Documentazione e roadmap; studio ancora sospeso fino al completamento di questo aggiornamento |

## Motivazione e continuità

La chiusura del 13/09/2026 copriva una capacità deterministica advisory, non il completamento di un assistente IA scientificamente validato. L’Owner riapre BKL-046 prima di riprendere lo studio dettagliato di PixInsight. Le evidenze e le acceptance F1–F5 restano conservate; il loro esito non si estende automaticamente al nuovo perimetro.

## Lavoro ancora aperto

1. Completare lo studio verificabile di processi, script e PJSR della versione installata di PixInsight, distinguendo inventario, lettura documentale, sorgente esaminato e comportamento verificato nativamente.
2. Consolidare conoscenza immutabile e versionata, provenienza, anomalie, limiti e matrice delle lacune. La lettura del sorgente pubblico non prova equivalenza con il binario installato.
3. Definire ed eseguire, nel perimetro di volta in volta autorizzato, la validazione scientifica per famiglie di workflow, con metriche, criteri di accettazione, dataset tracciabili e possibilità di ripristino.
4. Definire l’ammissione delle conoscenze e la successiva integrazione IA sulla base delle evidenze. Studio, integrazione tecnica e validazione scientifica sono stati distinti.

## Punto di ripresa conservato

Il materiale di studio locale disponibile alla sospensione comprende matrice/manifest v197, registro criticità v11 e baseline di conoscenza v1.12. Questi identificativi sono riferimenti al materiale privato, non risultati pubblicati o una dichiarazione di copertura scientifica completa. La versione installata studiata è PixInsight 1.9.5 build 1706.

FFTRegistration: entry/config esaminati; lettura del motore limitata alle righe 1–390. Il consolidamento successivo era incompleto e richiede verifica prima della ripresa. La campagna scientifica delle sette famiglie di workflow non risulta eseguita e le soglie non sono calibrate.

## Vincoli mantenuti

- Nessuna attivazione della nuova conoscenza nel portale deriva da questa riapertura.
- M27 resta `STOPPED_FOR_REVIEW`: CP005 conservato, CP006 respinto; nessuna ripresa dell’elaborazione o modifica dei master.
- La baseline F1–F5 conserva `aiModelImplemented=false`, `NOT_EVALUABLE_CURRENT_EVIDENCE` e `NOT_READY_FOR_PRODUCTION`. Eventuali estensioni sperimentali locali non modificano retroattivamente tale baseline.
- Nessuna nuova autorizzazione a inviare immagini/dati a provider, applicare processi automaticamente o pubblicare materiale privato.
- Nessuna nuova acceptance, review indipendente o evidenza post-merge è dichiarata da questo documento.

## Criteri per una nuova chiusura

La milestone rimane aperta finché il perimetro concordato dello studio e le lacune residue non sono rendicontati, le prove richieste non hanno risultati riproducibili con limiti espliciti, i criteri di ammissione e validazione non sono soddisfatti e l’Owner non accetta la nuova baseline. La sola disponibilità di documentazione o di un modello IA non costituisce efficacia scientifica dimostrata.

## Roadmap e riferimenti

La voce BKL-046 diventa `active` nella fonte canonica e `In Progress` nel backlog. Il traguardo F1–F5 del 13/09 resta completato come evento storico; un nuovo traguardo attivo registra la riapertura. La priorità delle altre milestone non viene ridefinita da questa decisione.

- [Backlog](BACKLOG.md)
- [Chiusura storica F1–F5](BKL-046-CLOSURE-2026-09-13.md)
- [Roadmap del manuale](../chapters/33-roadmap-evolutiva.md)
- [Piano di valutazione F5](../architecture/validation/BKL-046-F5-Real-Evidence-Evaluation-Plan.md)
