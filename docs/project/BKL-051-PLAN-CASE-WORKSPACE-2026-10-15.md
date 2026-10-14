# BKL-051 — piano, esecuzione vincolata e scheda del caso

## Stato e perimetro

Candidato integrato sulla baseline `31d02d916f19b5dc1b9de0b67e935d6227b39042`.
BKL-051 resta **OPEN / NOT_VALIDATED**, stima indicativa **37%**, zero controlli
scientificamente qualificati. Questo incremento collega componenti tecnici del
percorso selezione → piano → campione → esecuzione → evidenze → revisione → dossier;
non attesta il completamento operativo o scientifico del percorso.

Il portale importa in memoria documenti minimizzati. I nuovi importatori sono
passivi: nessun upload, persistenza, avvio o invio. Gli strumenti locali gestiscono
versioni congelate, eventi, collegamenti agli attempt e archivi privati. Le
identità e decisioni dichiarate nei documenti locali non costituiscono
autenticazione Owner. Il login pubblico osservato non attiva il servizio di analisi.

## Componenti e invarianti

| Componente | Comportamento e limite |
|---|---|
| `test_plan.py`, vista piano e revisioni | Versioni immutabili, hash, eventi conservati, esiti e revisioni dichiarati. Nessuna qualificazione automatica. |
| `plan_execution.py`, `plan_readiness.py` | Binding di piano, input, algoritmo e regole; autorizzazione esplicita, sessione consumata prima del dispatch. Incertezza da riconciliare senza replay. Readiness scientifica non dedotta. |
| `input_lineage.py`, preflight e binding dei derivati | Impronte e provenienza conservate; input alterati o incompleti bloccano il collegamento previsto. |
| `triplet_report.py` | Tutti i tentativi restano visibili. Tre job distinti verificati provano copertura tecnica, non validazione scientifica. |
| Contesti di calibrazione/astrometria, multi-epoca e ipotesi di moto | Contributi parziali e modelli descrittivi dichiarati. Incertezza completa e significatività mancanti restano sconosciute. |
| `controlled_recovery.py` | Parametri, verità sintetica, risultati e limiti conservati; separazione strutturale non equivale a prova indipendente di cecità. |
| `case_dossier.py`, `case_workspace.py` e viste | Piano, cronologia, journal ed evidenze verificati; pacchetto e caso devono coincidere. Contesto di recupero distinto dalle prove del caso. |
| `mpc_export.py` | Richiesta V2 con PERMID oppure TRKSUB locale; V1 numerata conservata. Stesso oggetto e stessi byte immagine non diventano osservazioni distinte cambiando data o percorso. Solo anteprima privata. |

Le guide operative in `tools/scientific_transients/*.txt` descrivono contratti e
comandi dei singoli moduli. Nessun file scientifico privato, credenziale, coordinata
protetta o fotografia è incluso nel package pubblico del codice.

## Evidenze locali e loro portata

Sul tree applicativo `b7cb1ff7f70983138e2fb900895ed0a419d22522`, prima del presente
aggiornamento documentale:

- Python: 445 test, esito OK; uno saltato perché il runner Windows non dispone del
  privilegio symlink. La copertura corrispondente resta da verificare su CI idonea.
- JavaScript: 274 PASS, nessun fallimento o skip.
- Build Pages rigorosa PASS; verifica di riferimenti interni e sitemap PASS su 992
  pagine HTML.
- Sottoinsieme finale MPC/ledger: 49 PASS; schema XSD fissato: tre casi positivi e
  sei negativi PASS. L'ultima modifica al solo generatore delle fixture XSD è
  verificata da questi controlli separati, dopo l'avvio della suite Python completa.
- ARB indipendente poi RQ indipendente, AI-assistite e separate per processo:
  APPROVED sul medesimo tree locale invariato, nessun finding bloccante rilevato.
  Non sono review umane o gate exact-head remoti.

I primi tentativi di discovery Python, conservati, fallivano per lo shadowing
di `queue` della libreria standard da parte di `queue.py` locale. La CI ora enumera
i moduli con nomi qualificati; include inoltre tutti i test JavaScript e i nuovi
script scientifici nei filtri. La correzione non cambia la coda applicativa.

La verifica manuale Owner riguarda la scheda preliminare importata: **zero tentativi,
copertura incompleta, zero controlli qualificati**. Non copre temi, tutte le
dimensioni, navigazione, tastiera, console, accessibilità o acceptance autenticata.

Le prove scientifiche private sono contestuali: il recupero esplorativo M27 ha
prodotto 1 recupero e 15 mancati recuperi su 16 inserzioni, nello stesso fondo.
Non sono 16 controlli indipendenti; il sigillo archivistico successivo allo scoring
non prova congelamento precedente alla conoscenza della verità. I tre job MOCK del
dossier dimostrativo e il contesto sintetico non attestano esecuzione sui tre input
reali preparati. La tripletta preliminare resta non eseguita.

## Gate residui

Prima di READY FOR MERGE occorrono commit esatto, CI applicabile positiva,
revisioni applicabili sul commit finale, controlli visivi più ampi e gate premerge
del mandato `DSG-AEM-001`. Pubblicazione e postmerge richiedono le proprie ricevute.
Gli esiti locali sopra non attestano questi passaggi.

Restano aperti tutti i requisiti scientifici e operativi della milestone: piano e
campione confermativi qualificati; calibrazione e incertezza complete; astrometria,
tempi, riferimenti e confronti accettati; recuperi e falsi collegamenti reali;
59 controlli indipendenti qualificati con zero false segnalazioni per il piano
5% / confidenza unilaterale 95%; percorso operativo autenticato completo e recovery;
evidenze/revisione Owner; requisiti provider e dossier/segnalazione produttivi;
privacy, accessibilità e acceptance finale. I 59 candidati in 15 gruppi notte non
soddisfano il requisito dei 59 controlli indipendenti. IRSA resta pendente senza
nuove interrogazioni o solleciti. Nessun invio astronomico è autorizzato da questo
incremento. BKL-050, Safety e gli altri package conservano i rispettivi gate.

## Ripristino

Revert del commit del package e ricostruzione Pages dalla baseline stabile
precedente, con verifica dei workflow e del sito. Conservare originali, versioni
del piano, journal, archivi, tentativi falliti e ricevute private: il ripristino
del codice non cancella evidenze né riconcilia implicitamente tentativi incerti.

[Handover](HANDOVER_2026-10-15-BKL051-PLAN-CASE-WORKSPACE.md).
