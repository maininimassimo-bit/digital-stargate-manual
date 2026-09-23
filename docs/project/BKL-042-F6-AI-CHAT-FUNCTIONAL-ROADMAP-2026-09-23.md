# BKL-042-F6 — AI Chat Functional Roadmap

**Stato:** Planned / separate governed gate  
**Owner / accountable:** Massimo Mainini  
**Prerequisito:** BKL-042-F5 real-evidence validation and closure

## Obiettivo funzionale

Integrare nel portale una chat AI consultiva che risponda usando esclusivamente fonti
governate, mostri citazioni e provenance, esponga incertezza e limiti e lasci ogni
decisione all'utente. La prima release è read-only e non esegue strumenti.

## Funzionalità possibili

### Release consultiva iniziale

- domande su stato osservatorio, sessioni, asset, target e workflow PixInsight;
- risposta con facts, evidence, inference e recommendation separati;
- citazioni cliccabili verso documenti e projection sorgente;
- indicazione di freshness, completeness, authority e limitation;
- risposte `INSUFFICIENT_EVIDENCE` o `CONFLICT_REQUIRES_REVIEW` quando necessario;
- ricerca per sessione, target, asset, workflow e intervallo temporale;
- riepilogo di provenance e passaggi dichiarati/observed senza ricostruzioni;
- confronto fra sessioni o workflow già presenti nelle projection governate;
- spiegazione del perché una risposta è stata prodotta, con method/producer version;
- export della risposta con correlation ID e citazioni, senza dati sensibili;
- feedback umano `useful`, `incorrect`, `defer` separato da qualsiasi execution.

### Funzionalità advisory successive

- RCA assistita su anomalie storiche con evidenza citata;
- supporto alla pianificazione osservativa senza GO/NO-GO automatico;
- checklist preparatorie per sessione e processing;
- suggerimenti PixInsight solo come opzioni bounded, mai apply;
- raccolta di human decision receipt separata dall'esecuzione.

### Funzionalità operative candidate, non autorizzate

- chiamata di tool o API esterne;
- esecuzione di workflow PixInsight;
- modifica o applicazione di parametri;
- apertura/chiusura osservatorio, mount, camera, power o network;
- remediation automatica, scheduling o target selection automatica.

Queste funzioni richiedono gate indipendenti per identity, consent, audit, dry-run,
rollback, least privilege, safety review e Safety Authority. Non sono incluse nella
milestone F6 read-only.

## Acceptance criteria proposta

- chat alimentata solo da projection con citation/provenance verificabili;
- prompt injection, fonte non citata, stale, conflict o unavailable producono risposta
  fail-closed;
- nessun segreto, path locale inutile o dato non minimizzato è esposto;
- ogni risposta conserva correlation ID, method/provider version e limitation;
- test di accessibilità, privacy, citazione, freshness e authority verdi;
- ARB/RQ e owner acceptance post-merge completati.
