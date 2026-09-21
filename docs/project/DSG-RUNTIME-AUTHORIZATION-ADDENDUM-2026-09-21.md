# DSG Runtime Authorization Addendum — Pre-Activation Governance

| Campo | Valore |
|---|---|
| Identificativo | DSG-RTA-ADD-001 |
| Stato | **OWNER-AUTHORIZED / ROLLED BACK / ACTIVATION BLOCKED** |
| Data | 2026-09-21 |
| Owner | Massimo Mainini |
| Repository | \`maininimassimo-bit/digital-stargate-manual\` |
| Baseline | \`main@6288bd1a3129ebf519cd1a66868cbe7b77514de9\` |
| Mandato modificato | DSG-AEM-001 v1.2 |
| Architettura correlata | AP-008; INT-REF-001; INT-CAT-001; AP-007; AP-003; AP-005; AP-006; AP-010 |
| Safety Authority | **Invariata: interlock fisici/locali** |

## 1. Decisione

Massimo Mainini autorizza formalmente la preparazione e, dopo il completamento dei gate indicati in questo addendum, l'attivazione controllata di un runtime read-only per:

- portale e schedule;
- macchina EAGLE30154;
- CloudWatcher;
- NINA;
- PHD2;
- dati live;
- scheduling senza limite giornaliero applicativo;
- conservazione delle evidenze su GitHub per sei mesi;
- uso di secrets già configurati nel relativo secret manager.

Questa decisione supera il precedente limite operativo di DSG-AEM-001 v1.2 **solo per lo scope sopra elencato**. Non attiva ancora il runtime e non costituisce autorizzazione a inviare comandi verso cupola, montatura, camere, relè, PLC, CPWI, ASCOM o altri apparati.

## 2. Boundary inderogabili

Restano invariati:

1. gli interlock fisici/locali come Safety Authority finale;
2. il fail-closed: dati mancanti, corrotti, incoerenti o obsoleti producono \`UNKNOWN\`, \`DEGRADED\` o \`NO_GO\`, mai \`SAFE\`;
3. l'agent locale deve essere read-only nella prima fase;
4. il traffico dell'agent deve essere esclusivamente outbound HTTPS;
5. nessun bypass di sensori, finecorsa, Safety Monitor, emergency stop o supervisore locale;
6. nessun automatic remediation e nessun command path nella fase iniziale;
7. nessun secret, token, password, chiave, seriale o dato protetto nella chat, nei log pubblici o nelle proiezioni;
8. nessuna cancellazione di dati o evidenze durante rollback senza ulteriore autorizzazione esplicita.

Il portale, GitHub Actions, il publisher, l'agent, l'AI e qualsiasi dashboard non sono Safety Authority.

## 3. Target runtime approvato

| Sorgente | Modalità | Cadenza target | Freshness target | Stato |
|---|---|---:|---:|---|
| CloudWatcher CSV | lettura locale read-only | 15 s | 60 s | da verificare su EAGLE |
| NINA | lettura locale read-only | 60 s | 5 min | da verificare su EAGLE |
| PHD2 | lettura locale read-only | 60 s | 5 min | da verificare su EAGLE |
| EAGLE health | lettura locale read-only | 30 s | 90 s | da verificare su EAGLE |
| GitHub projection/publisher | outbound HTTPS | secondo contratto | secondo contratto | non attivato |

Le proiezioni devono essere sanificate, versionate, correlate e accompagnate da audit log. Il publisher deve essere disabilitabile indipendentemente dall'agent.

## 4. Contratto applicativo dello scheduling

La rimozione del limite “due schedule al giorno” è autorizzata come modifica contrattuale applicativa, non come garanzia di capacità illimitata.

Il contratto dovrà:

- accettare almeno 3, 10, 100 e 1.000 schedule nello stesso giorno;
- gestire duplicati, sovrapposizioni, cancellazioni e restart in modo idempotente;
- separare stato desiderato, stato osservato e stato pubblicato;
- applicare retry con backoff e jitter solo agli errori transient;
- rispettare rate limit, quota e limiti tecnici GitHub/API;
- evitare doppia esecuzione tramite chiave di idempotenza;
- produrre \`UNKNOWN\` o \`DEGRADED\` quando la riconciliazione non è determinabile;
- non trasformare uno schedule in comando hardware.

Nessuna attivazione è autorizzata finché questo contratto non è implementato e validato con i test statici previsti.

## 5. Gap AP-008 da chiudere prima dell'attivazione

AP-008 è una baseline architetturale proposta e non è ancora un contratto runtime sufficiente. Prima dell'attivazione devono essere completati:

- owner del Contract Registry e degli adapter;
- contratti concreti per EAGLE health, CloudWatcher, NINA, PHD2, projection e publisher;
- protocolli, path locali, timeout, retry, rate limit e freshness approvati;
- matrice di compatibilità reale su EAGLE30154;
- test di schema, stale/unknown, duplicati, ordering, timeout, restart e recovery;
- audit e retention di sei mesi con policy di non cancellazione durante rollback;
- ORR coerente con AP-007;
- evidenza che il command path sia assente o tecnicamente bloccato;
- verifica che la Safety Authority locale resti indipendente.

## 6. Sequenza dei test autorizzati

L'ordine obbligatorio è:

1. test statici offline con 3, 10, 100 e 1.000 schedule;
2. duplicati, sovrapposizioni, cancellazioni e restart;
3. diagnostica read-only su EAGLE30154;
4. shadow test di 30 minuti senza comandi hardware;
5. CSV assente o corrotto;
6. rete assente;
7. dati NINA/PHD2 mancanti o obsoleti;
8. restart dell'agent;
9. test continuo di sei ore;
10. verifica di non-bypass di sensori, finecorsa e Safety Monitor;
11. verifica di pubblicazione GitHub e proiezione sul portale.

Ogni fase deve registrare separatamente test eseguiti, non eseguiti, output, failure e decisione di avanzamento. L'output della diagnostica locale deve essere restituito prima di qualunque modifica operativa.

## 7. Interlock applicativo `runtimeEnabled`

Il controllo `runtimeEnabled` è obbligatorio e fail-closed:

- il default è `false` nel launcher, producer, publisher e installer;
- `false` impedisce lettura dei secrets, scrittura runtime, pubblicazione e avvio del task;
- il task può essere creato/avviato solo con `-RuntimeEnabled $true`;
- il parametro `true` non costituisce da solo autorizzazione: richiede il completamento dei gate e l'autorizzazione owner;
- il controllo non sostituisce interlock locali, Safety Monitor o BKL-032.

## 7. Preconditions per l'attivazione

L'attivazione resta **bloccata** finché non risultano vere tutte le condizioni:

- questo addendum è pubblicato e referenziato dal package AP-008;
- la diagnostica read-only su EAGLE è stata eseguita e revisionata;
- i contratti runtime sono registrati e versionati;
- agent e publisher sono inizialmente disabilitati;
- \`runtimeEnabled=false\` è il default;
- non esiste command path verso hardware;
- i test statici e shadow sono passati;
- secrets e permessi sono verificati senza esporre valori;
- rollback e ripristino projection sono provati;
- ARB/Release Quality gate applicabile è aggiornato;
- l'owner autorizza esplicitamente il passaggio dal pre-activation allo shadow run.

## 8. Rollback obbligatorio

Il rollback deve poter essere eseguito in questo ordine:

1. impostare \`runtimeEnabled=false\`;
2. fermare l'agent locale;
3. bloccare il publisher GitHub;
4. ripristinare l'ultima proiezione valida;
5. fare revert del deployment o del commit;
6. conservare i log diagnostici e l'audit;
7. ruotare i secrets solo se esiste evidenza o sospetto di compromissione;
8. riattivare soltanto dopo un nuovo shadow test approvato.

Il rollback non deve cancellare dati, log o evidenze.

## 9. Criteri di stop

Il lavoro si arresta e richiede una nuova decisione owner se:

- è necessaria una credenziale nuova, la sua estrazione o la sua rotazione;
- occorre eseguire un comando hardware o interagire con interlock;
- emerge un protocollo o una semantica non documentata;
- un dato può essere interpretato come \`SAFE\` nonostante sia stale, missing o conflicting;
- la rete, GitHub o il secret manager impongono un bypass;
- il test richiede OAT fisico non eseguibile in modalità read-only;
- l'ownership del contratto o dell'authority è ambigua;
- si propone di ridurre retention, audit o rollback.

## 10. Evidenza e tracciabilità

Ogni attivazione futura deve citare:

- \`DSG-RTA-ADD-001\`;
- il commit esatto della configurazione;
- la versione dei contratti;
- la versione dell'agent e del publisher;
- l'evidenza dei test;
- l'assenza di command path;
- la verifica post-attivazione;
- il piano di rollback.

## 11. Evidenza di rollback — 2026-09-21

Il runtime telemetry risultava già attivo prima della diagnostica pre-activation:

- processo `Start-ObservatoryStatusTelemetryRuntime.ps1` rilevato con PID `2480`;
- task `DigitalStarGate-ObservatoryStatusTelemetry` in esecuzione;
- publisher outbound attivo con pubblicazione Cloud Run riuscita;
- NINA stale/non in esecuzione;
- projection meteo `UNSAFE`, Safety Authority `UNKNOWN`.

Su autorizzazione dell'owner è stato eseguito il rollback:

- task `DigitalStarGate-ObservatoryStatusTelemetry` impostato a `Disabled`;
- processo runtime arrestato; il PID risultava già terminato al controllo successivo;
- nessun processo `ObservatoryStatus`, `TelemetryProducer` o `Publish-ObservatoryStatus` residuo;
- proiezioni e log non cancellati;
- confronto dei timestamp dopo 10 secondi senza variazioni;
- nessun flag `runtimeEnabled` trovato sotto `C:\DigitalStarGate`.

Il rollback è verificato. L'assenza del flag `runtimeEnabled` è un gap bloccante da implementare prima di qualunque riattivazione.

## 12. Decisione corrente

**Decisione:** autorizzazione runtime formalizzata, con runtime preesistente ritirato.  
**Runtime:** fermato.  
**Schedule telemetry:** disabilitato.  
**Publisher:** non attivo.  
**Hardware command path:** non autorizzato.  
**Safety Authority:** invariata e locale.  
**Stato:** `NO_GO` fino all'implementazione del flag `runtimeEnabled=false`, alla correzione dei contratti e ai test autorizzati.  
**Prossimo gate:** correggere il diagnostico schema-aware e definire il contratto applicativo di enable/disable.