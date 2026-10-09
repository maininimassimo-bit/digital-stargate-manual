# BKL-051 S1 — Calibrazione fotometrica proposta e precisione numerica

| Campo | Valore |
|---|---|
| Identificativo | BKL-051-S1-PHOTOMETRIC-CALIBRATION |
| Versione | 1.0 |
| Data | 2026-10-09 |
| Stato | Proposed — aritmetica offline; scienza NOT_VALIDATED |
| Dipendenze | ADR-020, contratto S1 d'incertezza e dati pubblici conservati |

## Problema e comportamento

La conversione in magnitudine richiede una distinzione tra precisione dei valori memorizzati, errore strumentale e incertezza della calibrazione. Un errore strumentale numericamente coerente non prova un budget completo. Un catalogo PSF strumentale, una curva di luce già calibrata e una misura d'apertura non corretta non possono ricevere indistintamente lo stesso zero point.

`tools/scientific_transients/photometry.mjs` introduce un inspector proposto, senza I/O o integrazione runtime. Per dichiarazioni eleggibili calcola m = m_inst + Z + C × color. Ordine delle quattro variabili: [m_inst, Z, C, color]; gradiente [1, 1, color, C]. Le sei covarianze seguono [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]. Le varianze hanno le unità al quadrato delle corrispondenti variabili; le covarianze il prodotto delle rispettive unità. Il colore è una differenza di magnitudini nel sistema esplicitamente dichiarato. I coefficienti devono appartenere alla stessa definizione e banda; le etichette non ne attestano la compatibilità.

La sigma condizionale è sqrt(gᵀΣg), approssimazione del primo ordine. Le varianze devono essere già dichiarate come tali, non numeri grezzi di header di significato ignoto. Semantica irrisolta blocca la sigma. Colore mancante non diventa zero, neppure con coefficiente nullo. Dati già calibrati, aperture non corrette, banda incompatibile o definizione del colore assente bloccano la calibrazione di questo inspector. Non vengono applicate conversioni automatiche tra σ e varianza, correzioni d'apertura o assunzioni di spettro piatto.

`covariance.mjs` centralizza la fattorizzazione normalizzata già usata dal contratto di coppia `uncertainty.mjs`, conservandone API e stati. Matrici impossibili sono rifiutate anche con stime mancanti; budget parziali verificano i vincoli noti tra coppie. La tolleranza 64 × Number.EPSILON riguarda solo la fattorizzazione numerica. Zero, covarianza ignota e matrice singolare restano distinti. Nessuna soglia astronomica deriva dalla tolleranza.

## Input e limiti

Schema chiuso di oggetti passivi già materializzati: non è un parser di JSON grezzo o un confine sicuro per accessori/proxy. Un futuro adapter deve rifiutare chiavi duplicate, materializzare dati passivi e verificare byte/provenienza. Hash e metadati ricevuti sono dichiarazioni. Il helper di covarianza riceve soltanto vettori già validati dagli inspector; non è un intake autonomo.

Il budget richiede almeno una componente omessa. Unknown rimane null e non viene sostituito con zero. Un valore `VARIANCES_DECLARED` non attesta il significato statistico dei prodotti di un provider. Il componente non legge pixel, non misura flussi, non associa sorgenti, non valida likelihood a basso SNR o dispersioni sistematiche, non accetta una policy e non modifica il rapporto del worker o l'interfaccia Owner.

Output sempre `scientificValidation: NOT_VALIDATED`, classificazione `NOT_EVALUATED`, significatività e limite di mancata rilevazione null. Una magnitudine o sigma condizionale è aritmetica sulle dichiarazioni, non misura scientifica accettata.

## Evidenze private riconciliate

Tre cataloghi PSF ZTF a singola epoca conservati, 76.932 righe: impronte originali verificate e controlli indipendenti dei dati. Header catalogo più precisi degli header immagine, numeri compatibili entro metà dell'ultima cifra scritta nell'immagine; definizione del colore differente solo per spazi. I valori originali restano distinti.

Gli errori strumentali di magnitudine sono compatibili con una griglia di 0,001 mag. Il solo arrotondamento dell'errore non spiega rigorosamente 1.417 righe; aggiungendo gli intervalli di mezzo ULP della memorizzazione float32 di flusso ed errore del flusso, tutte le righe risultano compatibili con la propagazione logaritmica del primo ordine. È compatibilità numerica sui tre prodotti, non verifica dell'implementazione del provider né nuova soglia di accettazione.

Nei tre header, interpretare i due campi UNC di calibrazione come deviazioni standard viola la semidefinitezza positiva con la covarianza dichiarata. L'ipotesi varianze è numericamente compatibile ma **non adottata**. Una richiesta tecnica contenente soltanto riferimenti pubblici è stata inviata a IRSA con autorizzazione Owner. Risposta non ancora disponibile in questo dossier; incertezza completa resta sconosciuta. Nessuna associazione, variazione o scoperta accettata.

Script, output, prove fallite e successive versioni sono nell'archivio privato di preparazione; nessun originale o History sostituito. Le prove usano dipendenze di analisi private già disponibili, esterne al package; nessuna dipendenza runtime introdotta. Nessun nuovo lancio PixInsight, query provider, estrazione di credenziale o sessione cloud per questi controlli.

## Validazione e rilascio

Sedici test fotometrici sintetici: quattro sensitività, sei cross term, segni, colore mancante, semantica irrisolta, prodotti non eleggibili, banda, budget parziale, matrici impossibili e singolari, vettori sparsi, overflow e dichiarazioni operative aggiunte. Tredici regressioni del contratto di coppia verificano la fattorizzazione condivisa. Verifica privata su 256 matrici 4×4 PSD sintetiche A Aᵀ confrontata con NumPy: massimo scarto normalizzato sigma 1,222 × 10⁻¹⁵ sul primo sorgente verificato; non precisione astrofisica. I digest collegano la ricevuta privata al sorgente effettivamente provato.

La CI include il nuovo test su Windows/Linux. Gate di consegna: controlli locali, exact-head CI, ARB poi RQ, merge protetto e post-merge/Pages. Il documento non anticipa gate ancora pendenti. Rollback mediante revert coerente dei file e rigenerazione delle projection; nessuna migrazione, servizio o archivio scientifico modificato.

## Residui necessari alla milestone

S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. Restano semantica provider e budget completo, fotometria nativa e indipendente, timing/moto proprio/covarianze di matching, confronti multi-epoca in bande compatibili, PSF/sottrazione giustificate, prove cieche con eventi reali e campi di controllo, completezza/falsi positivi e policy quantitativa Owner. La concorrenza GCS del nucleo coda/storage è provata in [PR #527](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/527), non completa i residui dell'intero servizio distribuito.

Restano obbligatori reporting CBAT/TNS/VSX/MPC, tracklet, formati, approvazione payload immutabile, revoca/duplicati/ricevute e collaudo autorizzato. Nessuna segnalazione astronomica inviata. P6 Accepted nei limiti del dossier; F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva. S10/Safety e collegamento C→F invariati. BKL-051 non viene chiusa per sottrazione di requisiti.

## Fonti metodologiche

- [ZTF Explanatory Supplement](https://irsa.ipac.caltech.edu/data/ZTF/docs/ztf_explanatory_supplement.pdf), §10.1.1 Eq.2, §10.2 per correzioni d'apertura: copia ufficiale conservata e pagina della formula verificata visivamente.
- [Contratto d'incertezza proposto](BKL-051-S1-UNCERTAINTY-CONTRACT-2026-10-08.md), inclusa legge di propagazione NIST già documentata.
- [ADR-020](../architecture/ADR-020-Private-Scientific-Transient-Analysis.md), [piano scientifico](BKL-051-SCIENTIFIC-TRANSIENT-CANDIDATES-2026-10-07.md), [piano reporting](BKL-051-SCIENTIFIC-REPORTING-PLAN-2026-10-08.md).

Revisione 1.0: inspector aritmetico proposto e riconciliazione diagnostica; nessuna accettazione scientifica o operativa.
