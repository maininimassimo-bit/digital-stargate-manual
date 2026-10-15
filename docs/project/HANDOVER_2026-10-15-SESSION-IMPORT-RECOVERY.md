# Recupero importazione sessione 14–15 ottobre 2026

## Diagnosi

Il push EAGLE `398c5a0ef08ba35a000a18159afe3cd16e9a9af8`, ramo
`session/2026-10-14_2026-10-15`, è arrivato il 15 ottobre alle 06:01 UTC.
Validate session package 38689969862 SUCCESS. Promote 38689970022 fallisce:
la base `960cb4c` precede il refresh Planner `eaed15c` delle 05:57 UTC.
Analyze 38689969962 fallisce nel consolidamento con una configurazione
inesistente: C8 + ToupTek. Riproduzione locale: 24 sessioni, un errore.

Il log N.I.N.A. contiene preparazione Bias con C8/QHY, poi connessione
ToupTek e LIGHT NGC 281 salvati come Skywatcher quattro 200p. Il parser
accoppiava il primo telescopio incontrato con l'ultima camera connessa e
selezionava Bias come target. Nessuna nuova configurazione va inventata.

## Correzione

- Analizzatore: esclude target di calibrazione Bias/Dark/Flat/DarkFlat;
  telescopio e binning soltanto dai salvataggi LIGHT, camera dalla connessione
  attiva a quei salvataggi. Riconosce Skywatcher oltre a Sky-Watcher.
  Più strumenti LIGHT differenti rimangono indeterminati. Fallback QHY storico
  conservato per log privi di connessione esplicita.
- Promozione: workflow eseguito dal checkout main fidato, upload vincolato a
  SHA esatto e session ID; merge in worktree temporaneo contro main corrente.
  Scope del sorgente e del risultato limitato al pacchetto/report della sola
  sessione. Manifest COMPLETE, cartelle, dimensioni e SHA-256 riverificati.
  Push ordinario, mai force; massimo cinque tentativi solo se main avanza.
  Conflitti, scope esterno e hash errati bloccano. Il ramo upload è conservato.
- Analisi automatica soltanto su main dopo promozione; il dispatch esplicito
  resta necessario perché il push del GITHUB_TOKEN non scatena altri workflow.
- Recupero: workflow_dispatch di promote-session-package.yml su main, input
  session_id esatto; legge il ramo upload esistente senza ritrasferire i file.
  Il rilancio di un pacchetto già promosso è idempotente e ridispatcha l'analisi.
- Errori di validazione storico stampati anche nei log, con sessione/campo.

## Verifiche e limiti

Regressioni scientifiche sintetiche e storiche PASS; prove Git reali su remoto
bare sintetico: upload arretrato, idempotenza, race, conflitto, scope esterno,
hash errato. Contratto PowerShell preesistente PASS. Riproduzione della notte
con parser corretto: NGC 281, QUATTRO200_TOUPTEK294_BIN1, zero errori e tre
avvisi storici preesistenti. Rigenerazione target, equipment e cataloghi PASS.
Le metriche aggregate LIGHT già esistenti non sono una verifica dei binari RAW;
nessuna nuova immagine scientifica o configurazione manuale viene aggiunta.

CI exact-head, ARB poi RQ, merge e post-merge devono essere attestati nella PR;
il recupero è concluso solo dopo promozione, analisi, Pages e riscontro pubblico.
Nessuna modifica a EAGLE, schedulazione locale, Safety o comando dispositivi.

## Rollback

Revert del commit applicativo tramite PR governata; conservare il ramo upload
originale e i pacchetti ricevuti. Non riscrivere main o cancellare evidenze.
Le proiezioni derivate si ricostruiscono dall'analizzatore e dai generatori.
