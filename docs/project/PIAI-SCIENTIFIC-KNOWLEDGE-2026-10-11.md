# PixInsight — conoscenza scientifica nelle API e percorso dal portale

| Campo | Valore |
|---|---|
| Identificativo | DSG-PIAI-SCIENTIFIC-KNOWLEDGE-001 |
| Versione | 1.5 — fusione non promossa e confini decisionali |
| Data | 11/10/2026 |
| Stato | Backend research-lineage-v1 attivo e portale pubblicato; M27 2ffd1ae8: 12 API note / 6 prove native, STOP dopo confronto della fusione CP006; controllo CP005 conservato, nessun finale consegnato o accettato |

## Obiettivo e confini

La correzione della provenienza SPCC è rilasciata con PR584 e la richiesta M27 è stata ripresa dal portale dopo verifica Owner. Il modello riceve il fit originale CP001 nella catena CP000→CP001→CP004→CP005. Ha provato la fusione LRGB CP006, quindi si è fermato per il rischio ai limiti dei canali RGB e beneficio non dimostrato. Consuntivo: 12 chiamate API note, sei prove native, 131.118 token input / 6.121 output / 137.239 totali. CP005 resta selezionato; CP006 è conservato come prova non promossa. Nessuna saturazione, consegna finale o accettazione scientifica. [Evidenze e limite del catalogo](PIAI-RESEARCH-COORDINATOR-2026-10-11.md#fusione-lrgb-prova-non-promossa-e-limite-operativo). Le verifiche preliminari e i consuntivi precedenti sono snapshot storici.

Owner richiede che il modulo funzioni dal portale web, senza dipendere da una chat, e che le API ricevano la conoscenza della skill `pixinsight-scientific`. La conoscenza è ora una risorsa del servizio, distinta dalle misure native e dalle capacità effettivamente implementate. Il modello rimane `gpt-6-luna`; chiave sul backend, master sul PC e ricevute immutabili conservati.

Il pacchetto `DSG_PIAI_SCIENTIFIC_KNOWLEDGE_V1` comprende quattro documenti: principi della skill, protocollo nativo portabile, calibrazione/presentazione e interpretazione delle misure. Il protocollo portabile esclude la sezione con percorsi e istruzioni locali del PC; non trasferisce la memoria della chat, credenziali o inventari privati. I riferimenti scientifici sono indicazioni da consultare: il loro testo non viene recuperato automaticamente dall'API né costituisce conoscenza verificata della versione installata.

La richiesta iniziale include il pacchetto nelle istruzioni del modello e conserva il suo SHA256 nella ricevuta provider. Il backend archivia il testo esatto; i checkpoint del nuovo job devono usare la stessa impronta. Una modifica del pacchetto interrompe il nuovo invio prima della chiamata provider: non cambia silenziosamente il metodo a metà elaborazione. I job precedenti senza questo binding mantengono il comportamento storico. Il contesto del worker include il pacchetto esatto per conservarlo nell'archivio finale. Nessuna lettura delle skill dal profilo personale è necessaria nel runtime cloud.

Conoscenza e capacità restano distinte: descrivere SPCC, MLDenoise o altri processi nella guida non li abilita nel catalogo V2. Il modello non esegue la skill, non acquisisce PixInsight a distanza e non scrive codice nativo arbitrario. Fonte autorevole dei fatti fisici restano file, misure e ricevute del worker; le istruzioni non concedono consensi, cambiano policy Owner o producono acceptance.

## Criteri tecnico-scientifici trasferiti

Le API devono distinguere segnale acquisito, rumore stimato e resa di presentazione. MRS conserva scala e supporto; non è automaticamente SNR. Varianza del campo contenente nebulosità non è varianza del cielo. Drizzle, resampling e denoise introducono correlazioni: non assumere indipendenza dei campioni.

FWHM, eccentricità e residui descrivono le PSF delle stelle selezionate. Confrontare le stesse stelle, campo, scala e condizioni; stelle rilevate separatamente non costituiscono un confronto appaiato. Riduzione della FWHM dopo deconvoluzione non prova da sola nuova risoluzione fisica. Le anteprime sono visualizzazioni derivate, non campioni scientifici o attestazioni di qualità.

SPCC richiede RGB lineare, astrometria coerente sulla griglia, Gaia con spettri, curve strumentali/QE e riferimento bianco documentati. Registrare punti, guadagni, scarti e dispersione; un processo terminato non certifica il fit. Per M27: camera QHY695A, RGB ZWO, Optolong L-Pro soltanto luminanza; le curve nominali non sono curve misurate dei singoli filtri. Conservare il RGB calibrato prima delle trasformazioni estetiche LRGB, contrasto e saturazione.

Le prove devono partire dal medesimo genitore, preservando controllo, rami scartati, History e parametri. Deconvoluzione prima di denoise/stretch/separazione quando adatta ai dati. Valutare filamenti deboli, stelle, aloni, ringing, grana, clipping e neri; minor rumore o maggiore vividezza non bastano a scegliere. Il modello può motivare il miglior candidato fra quelli verificati, senza dichiarare un optimum globale.

## Portale e nuova autonomia

Il portale indica quando una nuova proposta usa il protocollo versionato. Le misure, il grafo, le decisioni intermedie e i consumi continuano a essere consultabili nella richiesta privata. Non è richiesta una chat per usare il pacchetto scientifico.

Requisito di accettazione dell'estensione: l'intero percorso operativo deve essere accessibile dal portale. L'Owner seleziona dati, ricetta e obiettivo; il servizio acquisisce le misure dal worker, presenta il perimetro delle prove, registra la conferma e decide/esegue/verifica le alternative autorizzate. Arresto, problemi di provenienza o configurazione, consumi, motivazione della scelta e risultato finale devono comparire nella richiesta privata. Una conferma in chat, una skill del profilo Codex o un agente Codex presente durante l'esecuzione non devono essere dipendenze del modulo finale. Il worker locale e PixInsight restano necessari sul PC. Questo requisito descrive il nuovo ciclo richiesto, non capacità SPCC già disponibili nel V2.

Il servizio V2 conserva il proprio perimetro: grafo esatto e soli parametri del prossimo passo. La [ripartenza SPCC e selezione autonoma](PIAI-M27-PHOTOMETRIC-RESTART-2026-10-11.md) è l'estensione successiva in sviluppo: richiede funzioni native validate, nuovi contratti, conferma del perimetro dal portale, confronti appaiati e OAT. Trasferire la skill non completa queste capacità. L'Owner indica ricetta/obiettivo nel portale; il target è esecuzione autonoma delle alternative ammesse, con controllo iniziale del perimetro e revisione finale distinte.

## Verifica corrente e rilascio

Una nuova raccolta read-only M27 è stata eseguita nativamente su copie dei quattro master originali: geometria 4634×2808 mono, cinque regioni per canale, MRS e PSF native, originali/copie/History verificati invariati e istanza dedicata chiusa. I costruttori SPCC e Gaia sono stati ispezionati senza applicare calibrazione o inviare dati al provider. Un primo probe fallito prima delle misure per nome errato del costruttore Gaia è conservato separatamente; la successiva istanza usa `Gaia` correttamente. Nessuna qualità SPCC o validità WCS viene dedotta dai costruttori.

PR577: head `b89d873f8a1987f17cabc92492056b2955699765`, merge `a6408267da05d3be8f1adf4e5205de4f95f80103`; ARB poi RQ APPROVED, zero finding, nove check PR e otto workflow post-merge SUCCESS. MkDocs strict e test pertinenti PASS; Pages HTTP200 con pacchetto e requisito senza chat presenti. Waiver `W-DSG-AEM-RULESET-001` applicata e ricevuta nella PR.

Backend attivo al 100% sulla revisione `dsg-pixinsight-pilot-scientific-v1-20261011`, immagine `sha256:198beb5c994d4c41c257d96e033f2b8376e4a6d6d625f79dfcbc4391a8660fc5`, build `3301a0a7-3311-4268-a137-ae5a9e28d700` SUCCESS. Contesto pubblico allowlisted dall'head revisionato; modello, riferimento al secret, quota, identità, risorse, concorrenza e timeout confrontati invariati. Verifica della revisione a traffico zero prima della promozione: health200, opzioni/job privati403 senza credenziale; health200 anche sull'URL principale dopo la promozione. Nessuna nuova risorsa IAM, chiave trasferita al PC o modifica del worker nativo.

Test: trasferimento della guida nei payload iniziali/checkpoint, impronta costante, arresto prima dell'invio su guida cambiata, assenza dei percorsi personali e compatibilità dei job storici. I test con provider simulato non sono nuove chiamate API reali: l'OAT di una nuova proposta con guida archiviata e del ciclo SPCC rimane pendente. Rollback del backend sulla revisione `dsg-pixinsight-pilot-adaptive-diag-20261011`, senza riscrivere job o cancellare guide/risultati; mantenere il pacchetto corrispondente per ogni nuovo job iniziato.

## Revisioni

| Versione | Modifica |
|---|---|
| 1.0 | Pacchetto scientifico portabile e versionato nelle API; vincolo ai checkpoint e indicazione dal portale; preparazione della nuova autonomia |
| 1.1 | Rilascio PR577 e attivazione backend verificati; requisito operativo interamente dal portale e limiti OAT espliciti |


La [diagnostica rilasciata e i vincoli della decisione API](PIAI-RESEARCH-COORDINATOR-2026-10-11.md#diagnostica-rilasciata-e-vincoli-della-decisione-api) registrano anche il secondo tentativo distinto autorizzato: risposta completa, decisione rifiutata per vincolo del padre/ID TEST, 11.172 token noti e zero prove native. Schema più vincolante candidato; nessun riuso o reinvio automatico. OAT scientifico e accettazione restano aperti.


Successivo OAT distinto autorizzato `2ffd1ae8`: prima decisione SPCC validata e prova CP001 verificata localmente su copie, 11.098 token noti. Ricevuta di misure fermata prima dell’HTTP perché supera il limite 256KiB; nessun replay nativo. [Stato e correzione del limite di trasporto](PIAI-RESEARCH-COORDINATOR-2026-10-11.md#prima-prova-spcc-reale-e-dimensione-della-ricevuta). Selezione, workflow completo e accettazione restano pendenti.


Requisito di continuità della conoscenza: l'API deve ricevere il checkpoint di calibrazione della catena selezionata con ricevuta e trasformazioni successive. Assenza di un nuovo fit locale non cancella la calibrazione storica; presenza del fit storico non prova validità fotometrica del finale. La proiezione candidata trasmette questa distinzione e mantiene il pacchetto di guide approvato. La scelta dei rami BXT ha conservato il controllo per beneficio non conclusivo e rischio nelle alte luci; una FWHM minore da stelle non appaiate non è un criterio sufficiente. Per denoise, supporto MRS zero rende inutilizzabile quella stima, non prova rumore nullo. Rilascio/ripresa e OAT finale restano aperti.
