# BKL-051 S1 — fattibilità e contratto scientifico proposto

| Campo | Valore |
|---|---|
| Versione | 1.0 |
| Data | 2026-10-07 |
| Stato | PROPOSED — preparazione verificabile; decisioni Owner pendenti |
| Dipendenza | P6 Accepted, PR #499 merge `0bd6e20df0b449cd163543ed30bd69d9264862b0`, 16/16 workflow post-merge SUCCESS inclusa Pages |
| Scope della consegna | Fonti, contratto proposto, verifica offline, protocollo di validazione; nessuna analisi Owner o attivazione |

Il mandato di prosecuzione autonoma del 7 ottobre consente di preparare il massimo lavoro indipendente e raccogliere le domande per il ritorno Owner. Non sostituisce le decisioni strutturali e scientifiche previste da [DSG-AEM-001](DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md). S1 non è accettata e BKL-051 non è chiusa. [Piano approvato](BKL-051-SCIENTIFIC-TRANSIENT-CANDIDATES-2026-10-07.md).

## Risultato della ricerca

La fattibilità di accesso pubblico è dimostrata in modo limitato: metadata ZTF, metadata Pan-STARRS DR2, un piccolo esempio documentato su M101 e una riga arbitraria Gaia DR3 hanno restituito HTTP 200 con dati tabellari. Non è un test di copertura delle immagini Owner, completezza dei cataloghi, qualità scientifica, disponibilità futura o prestazioni. Nessuna fotografia, coordinata Owner, token o dato del sito è stato inviato. Le risposte originali e le impronte restano nel dossier locale; [evidenza pubblica minimizzata](evidence/BKL-051-S1-PUBLIC-SOURCE-PROBES-2026-10-07.json).

Due tentativi Gaia di schema con formato JSON hanno restituito HTTP 500. Il primo tentativo Pan-STARRS ha avuto un errore di connessione; una seconda prova esplicita ha restituito dati. I risultati negativi sono conservati, non trasformati in successi. Il piccolo esempio Pan-STARRS contiene anche `-999.0`: è un valore sentinella, non una magnitudine fisica. Identificatori interi a 64 bit vanno trattati come stringhe nei consumer JavaScript, senza perdita di precisione.

| Fonte | Uso proposto | Vincolo concreto |
|---|---|---|
| ESA Gaia DR3, release fissata nel manifest | Identificazione e astrometria stellare | Epoca astrometrica, moto proprio, errori/covarianze; identificatore associato alla release. Assenza di match non prova assenza di stella |
| NASA/IPAC IRSA ZTF | Riferimenti e serie temporali | Prodotti pubblici, filtro, epoca, footprint e flag per ogni esposizione; mancanza di prodotto distinta da campo vuoto |
| MAST Pan-STARRS DR2 | Catalogo, stack e osservazioni disponibili | Distingue aggregati da epoche individuali; sentinelle e qualità conservate; nessuna data singola inventata per uno stack |
| AAVSO VSX | Controllo di variabili note | Integrazione programmatica/condizioni d'uso ancora da verificare; mancato controllo resta UNKNOWN |
| Minor Planet Center | Controllo di oggetti mobili | Servono coordinate e tempo di osservazione; disponibilità/interfaccia/termini da confermare prima del runtime |

L'IRSA descrive attualmente DR24 nella pagina missione consultata; l'implementazione deve comunque registrare prodotto e release realmente interrogati, non assumere che “latest” sia stabile. Gaia DR3 è un riferimento fissato, senza affermazioni sulla futura disponibilità di DR4. Nessuna fonte da sola offre un workflow universale per camere e filtri Owner.

## Contratto di misura proposto

Le immagini estetiche sono consultabili come contesto visivo, ma le misure richiedono dati scientifici lineari per singola banda. SHO/HOO, denoise, deconvoluzione, stretch e separazione stelle non sono ingressi fotometrici equivalenti ai master originali. Un master narrowband può servire a localizzare sorgenti e confrontarsi con riprese della stessa risposta; non va sottratto direttamente da un riferimento broadband. SPCC non elimina questa incompatibilità.

Ogni ingresso privato deve riferire identità/revisione esatta, SHA256 dei byte, formato/immagine selezionata nel contenitore, geometria e unità; intervalli effettivi delle acquisizioni, provenienza temporale e filtri/risposte; soluzione WCS verificata con residui e sistema di riferimento; maschere, saturazione, varianza o modello d'incertezza e lineage prima delle alterazioni di misura. Il campo `DATE-OBS` di un master non basta a descrivere un'integrazione su più notti. Data di elaborazione e ora di upload non riempiono un'epoca mancante.

Il preparatore offline in `tools/scientific_transients/contract.mjs` implementa solo il sottoinsieme di intake **proposto**: schema chiuso, unknown espliciti, intervalli UTC, hash, linearità/filtri/WCS/lineage dichiarati e riferimenti a evidenze indipendenti. Non legge immagini, non verifica la verità delle dichiarazioni, non certifica l'indipendenza e non modifica i registry. Hash corretti non attestano autenticità o qualità. Restituisce sempre `NO_ANALYSIS_EXECUTED`, `NOT_EVALUATED` e `OWNER_CONTRACT_DECISIONS_PENDING`. Nessun valore “approvato” nel payload conferisce consenso.

Un'eventuale scheda scientifica dovrà aggiungere, in un contratto successivo revisionato, le misure reali e le unità mancanti a questo preparatore: pixel/WCS residui, PSF, flussi/errori, covarianze, flag, footprint e riferimenti provider. Questa consegna non dichiara completo il futuro schema operativo.

## Stati e limiti del confronto

Tre assi separati evitano falsi risultati: stato di esecuzione, comparabilità scientifica e revisione umana. `SOURCE_UNAVAILABLE`, `NO_COVERAGE`, `EPOCH_UNKNOWN`, `BAND_INCOMPATIBLE`, `ASTROMETRY_UNVERIFIED`, `PSF_UNVERIFIED`, `REFERENCE_TRUNCATED` e `QUALITY_UNKNOWN` non diventano `NO_TRANSIENT_FOUND`. Il riconoscimento di stelle note può essere possibile mentre fotometria o sottrazione restano non confrontabili.

Quando completo, l'output scientifico potrà indicare `KNOWN_SOURCE`, `UNMATCHED_SOURCE`, `BRIGHTNESS_CHANGE_REQUIRES_REVIEW`, `ARTIFACT_SUSPECT`, `MOVING_OBJECT_POSSIBLE` o `INCONCLUSIVE`, corredati da motivazione. Sono vocabolari proposti, non classi prodotte dal codice S1. Il reviewer userà stati privati `TO_REVIEW`, `DISMISSED` e `FOLLOW_UP_REQUIRED`, con ragione ed evidenza ancorate all'esatto risultato. Nessuna transizione automatica a nova/scoperta; un controllo non eseguito resta esplicito.

## Metodo da validare prima dell'uso

1. Verificare originali e leggere i contenitori senza alterare i master; esportare copie lineari per banda con manifest esatto quando necessario. Un'eventuale esportazione PixInsight conserva History e parent, non ricostruisce la provenienza mancante.
2. Risolvere e verificare WCS, distorsioni, footprint e residui. La propagazione Gaia richiede epoca, moto proprio e covarianze; `pmra` comprende cos(dec). Le epoche Gaia in anni giuliani TCB non sono timestamp UTC. Per parallasse/prospettiva e moto elevato usare un metodo documentato con distanza/velocità disponibili; non approssimare silenziosamente e non convertire unknown a zero.
3. Cross-match con incertezze e ambiguità esplicite. Il raggio non va fissato arbitrariamente: comprende residui WCS, errore del centroide, propagazione/covarianze e densità/confusione. Query abbastanza ampie da includere il moto proprio; paginazione, limiti e completezza verificati. Catalogo troncato blocca le conclusioni di assenza.
4. Verificare banda, epoche, profondità, saturazione, maschere e qualità. Misure differenziali con stelle di confronto adatte, errori e trasformazioni di colore validate; nessuna conversione generica Gaia G→Hα. Una non-rilevazione richiede limite superiore misurato, non zero flusso.
5. Sottrarre solo immagini compatibili: registrazione, background, scala di flusso e PSF con varianza/covarianza da ricampionamento, maschere e residui di controllo. L'immagine differenza deve restare invalida se le condizioni non sono soddisfatte.
6. Verificare ogni segnalazione in esposizioni calibrate o sottointegrazioni disgiunte documentate; master duplicati e split sovrapposti non sono conferme indipendenti. Controllare raggi cosmici, hot pixel, spike, aloni, bordi, saturazione, confusioni, variabili e movimento.
7. Salvare rapporti privati con input e riferimenti esatti, algoritmo/versione, parametri, misure/errori, limiti e decisione. Nessun invio a organizzazioni astronomiche senza richiesta esplicita.

## Compatibilità architetturale e proposta reviewable

Il Scientific Data Engine 2.1 attuale è un consumer/cache/index di cataloghi e workflow governati; non è un broker privato né un motore fotometrico. Aggiungere un semplice `fetch` NASA/ESA nel frontend aggirerebbe i confini esistenti. AP-013 resta authority per asset/lineage; AP-014 per contesto/catalogo e ammissione; ADR-019 conserva gli ingressi storici PARTIAL/UNKNOWN senza inventare sessioni. Un record ADMITTED non diventa scientificamente ACCEPTED.

**Proposta raccomandata, non attivata:** calcolo sul PC Owner; originali, misure e rapporti completi sul PC; consulta privata nel portale attraverso un adapter dedicato governato dal SDE. Interrogazioni provider dal componente locale esplicito, con allowlist, cache/versioni, timeout, limiti e ricevute. Nessun accesso al disco dal browser, endpoint arbitrario, nuovo cloud o credenziale implicita. Il trasporto SESSION_ASSISTED esistente è esperienza utile ma non autorizza automaticamente un nuovo tipo di job nel broker PIAI.

Occorre un assessment/ADR dedicato prima del runtime: il contratto nuovo gestisce dati scientifici privati e divulga ai provider la regione celeste interrogata. Questo documento valuta il bisogno, senza allocare un AP/ADR definitivo o dichiararlo approvato. Un portale interamente locale è alternativa reversibile, ma differisce dalla consultazione remota richiesta. La scelta sarà dell'Owner su questa proposta concreta, non inferita dal mandato autonomo.

La richiesta esterna proposta contiene solo regione ICRS/raggio o footprint, release/catalogo/prodotto, filtri e intervalli indispensabili. Mai pixel Owner, nominativi, percorsi, seriali, coordinate del sito, sessioni o report. I provider possono comunque registrare IP, query, orario e user-agent; una query di campo è informazione privata anche senza upload. Nessuna query su campi Owner è eseguita in S1.

## Validazione e gate successivi

| Gate | Prova richiesta | Situazione |
|---|---|---|
| Accesso fonte | Risposta/parsing/schema e negativa conservati | Prova pubblica limitata conclusa; nessuna SLA |
| Intake | Rifiuto duplicate/unknown/nonfinite, date false, false conferme, palette e consenso auto-dichiarato | Nove test offline sintetici; nessuna misura astronomica |
| Campioni provider | ID a 64 bit, sentinelle PS1, epoche TCB, errori CSV e limiti | Sei test sintetici; parsing offline delle risposte pubbliche Gaia (una riga) e PS1 (dieci righe) verificato separatamente |
| Astrometria | Known answers, wrap RA/poli, moto proprio elevato, mancanze/covarianze, WCS distortions | Pianificato S2 |
| Fotometria e differenze | Campi reali noti e di controllo, eventi storici pubblici, recovery/falsi positivi e precision-recall con intervalli | Pianificato S3, nessun risultato inventato |
| Soglie | Dataset sviluppo/validazione separati per campo, epoca e strumento; injection/recovery separata dai dati reali | Profilo quantitativo da proporre dopo baseline e approvare prima dell'uso |
| Privato/operativo | Non-Owner negato, idempotenza, cancellazione, crash conservativo e replay bloccato | S4/S5, nessun riuso di P6 come prova del nuovo modulo |

I test sintetici verificano invarianti, non un tasso di recupero reale. Non fissiamo qui S/N, raggio, differenza di magnitudine o soglie di classificazione. Il protocollo deve misurare rumore, correlazioni, completezza per campo, artefatti e falsi positivi prima della proposta numerica.

## Decisioni lasciate all'Owner

1. Confermare o modificare la proposta PC Owner + consultazione privata nel portale; l'ADR e il trasporto effettivo saranno revisionati prima dell'attivazione. Nessun costo o nuova risorsa è autorizzato implicitamente.
2. Consentire query programmatiche minime sulle regioni delle proprie riprese ai soli provider nominati, conservando tutto il resto localmente? La prova attuale usa soltanto esempi pubblici.
3. Indicare il campo pilota e i dati disponibili: raccomandati master lineari per singola banda, acquisizioni datate e singoli calibrati; se possibile due epoche nella stessa banda. Narrowband e fotografie finali rimangono casi limitati, non equivalenti ai riferimenti broadband.

Le scelte strutturali e il consenso alle query attendono risposta. La preparazione offline può proseguire. Le soglie scientifiche saranno una decisione successiva basata su risultati misurati, non una domanda astratta da risolvere oggi.

## Rollback e tracciabilità

Rimuovere il preparatore/contratto proposto e le pagine additive, conservando dossier locale e fonti consultate. Nessuna migrazione, immagine, registro, broker o risorsa è stata cambiata. BKL-051 rimane In Progress S1; F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva e S10/Safety invariati. P6 resta chiusa con limiti accettati.

Fonti ufficiali consultate il 7 ottobre 2026: [Gaia data model](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html), [ZTF missione](https://irsa.ipac.caltech.edu/Missions/ztf.html), [API ZTF](https://irsa.ipac.caltech.edu/docs/program_interface/ztf_api.html), [cataloghi Pan-STARRS](https://catalogs.mast.stsci.edu/docs/panstarrs.html), [immagini PS1](https://ps1images.stsci.edu/ps1image.html), [AAVSO verifica variabili](https://archive.aavso.org/index.php/how-report-new-variable-star-discoveries), [MPC servizi](https://docs.minorplanetcenter.net/services/), [MPC FAQ](https://docs.minorplanetcenter.net/mpc-ops-docs/faqs/). Documentazione e limiti di accesso programmatico AAVSO/MPC devono essere verificati prima dell'adapter.
