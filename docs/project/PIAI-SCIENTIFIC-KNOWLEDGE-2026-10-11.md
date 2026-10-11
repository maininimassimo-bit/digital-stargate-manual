# PixInsight — conoscenza scientifica nelle API e percorso dal portale

| Campo | Valore |
|---|---|
| Identificativo | DSG-PIAI-SCIENTIFIC-KNOWLEDGE-001 |
| Versione | 1.0 |
| Data | 11/10/2026 |
| Stato | Incremento candidato: conoscenza collegata ai provider; rilascio e attivazione da verificare |

## Obiettivo e confini

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

Nel candidato il portale indica quando una proposta usa il protocollo versionato. Le misure, il grafo, le decisioni intermedie e i consumi continuano a essere consultabili nella richiesta privata. Non è richiesta una chat per usare il pacchetto scientifico.

Il servizio V2 conserva il proprio perimetro: grafo esatto e soli parametri del prossimo passo. La [ripartenza SPCC e selezione autonoma](PIAI-M27-PHOTOMETRIC-RESTART-2026-10-11.md) è l'estensione successiva in sviluppo: richiede funzioni native validate, nuovi contratti, conferma del perimetro dal portale, confronti appaiati e OAT. Trasferire la skill non completa queste capacità. L'Owner indica ricetta/obiettivo nel portale; il target è esecuzione autonoma delle alternative ammesse, con controllo iniziale del perimetro e revisione finale distinte.

## Verifica corrente e rilascio

Una nuova raccolta read-only M27 è stata eseguita nativamente su copie dei quattro master originali: geometria 4634×2808 mono, cinque regioni per canale, MRS e PSF native, originali/copie/History verificati invariati e istanza dedicata chiusa. I costruttori SPCC e Gaia sono stati ispezionati senza applicare calibrazione o inviare dati al provider. Un primo probe fallito prima delle misure per nome errato del costruttore Gaia è conservato separatamente; la successiva istanza usa `Gaia` correttamente. Nessuna qualità SPCC o validità WCS viene dedotta dai costruttori.

Test: trasferimento della guida nei payload iniziali/checkpoint, impronta costante, arresto prima dell'invio su guida cambiata, assenza dei percorsi personali e compatibilità dei job storici. I test con provider simulato non sono nuove chiamate API reali. Gate: suite pertinente, MkDocs strict, CI exact-head, ARB poi RQ, merge e post-merge; attivazione richiede distribuire l'immagine backend revisionata e verificarne configurazione/digest. Rollback sulla precedente revisione backend, senza riscrivere job o cancellare guide/risultati.

## Revisioni

| Versione | Modifica |
|---|---|
| 1.0 | Pacchetto scientifico portabile e versionato nelle API; vincolo ai checkpoint e indicazione dal portale; preparazione della nuova autonomia |
