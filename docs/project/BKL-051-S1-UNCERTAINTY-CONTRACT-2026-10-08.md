# BKL-051 S1 — Contratto proposto di confronto e incertezza

Preparazione offline del 8 ottobre 2026, successiva alla [consegna delle evidenze di misura](BKL-051-S1-MEASUREMENT-EVIDENCE-2026-10-08.md), integrata con PR [#502](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/502), merge `8f4a24db2d98c32802592b52d3c809976018effe`. **Proposed**, nessuna accettazione del modello scientifico completo o attivazione operativa. BKL-051 resta aperta.

## Calcolo e unità

Il modulo puro `tools/scientific_transients/uncertainty.mjs` riceve un oggetto già materializzato con due riferimenti di immagine, flussi firmati L e R, fattore positivo s di conversione da destra a sinistra, tre varianze e tre covarianze. Calcola soltanto D = L − sR, con gradiente g = [1, −s, −R] e deviazione condizionale sqrt(gᵀΣg). Σ segue l'ordine [L, R, s]; le covarianze seguono [(L,R), (L,s), (R,s)]. Ogni termine deve avere le unità coerenti con la grandezza corrispondente; s converte le unità dichiarate di R in quelle di L. Le etichette ADU/NORMALIZED_SAMPLE non verificano la conversione.

È un'approssimazione del primo ordine, non la distribuzione esatta del prodotto di variabili aleatorie. La [legge NIST di propagazione dell'incertezza](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty) include coefficienti di sensibilità e covarianze: non giustifica sostituire covarianze ignote con zero.

Varianze e covarianze sconosciute restano `null` e impediscono una sigma completa. Un flusso o fattore sconosciuto impedisce anche la differenza. Flussi negativi restano firmati; non diventano limiti di mancata rilevazione. Matrici complete incompatibili con la semidefinitezza positiva vengono rifiutate anche se manca un flusso; nei budget parziali vengono controllati i vincoli noti tra coppie. La tolleranza 64 × Number.EPSILON riguarda solo arrotondamento numerico. Non è una soglia scientifica. Overflow e valori non finiti vengono rifiutati.

Il budget richiede almeno una componente omessa dichiarata. Il codice non ammette una dichiarazione di modello completo. Il rumore di lettura non può essere dichiarato già incluso nel fondo e aggiunto separatamente. La documentazione [Photutils 2.3.0](https://photutils.readthedocs.io/en/2.3.0/api/photutils.utils.calc_total_error.html) distingue errore di fondo e componente Poisson della sorgente; è una fonte metodologica, senza nuova dipendenza runtime.

## Limiti del contratto

Schema chiuso, nessun I/O, credenziale, query, lettura dei pixel o transport adapter. Hash, banda, astrometria, PSF, qualità ed epoche sono dichiarazioni, non verifiche indipendenti. Due riferimenti allo stesso file/indice sono segnalati come non indipendenti. Anche una sigma zero non produce significatività infinita. Banda incompatibile, PSF confusa, saturazione o epoche ignote mantengono motivi espliciti di non validazione.

Gli output restano `scientificComparison: NOT_VALIDATED`, `scientificClassification: NOT_EVALUATED`, `significance: null`, `nondetectionLimit: null`, policy operativa non accettata e revisione necessaria. Una differenza algebrica eventualmente disponibile non costituisce confronto scientifico valido.

Questo inspector riceve oggetti passivi, non JSON grezzo o oggetti con accessori/proxy non fidati. Il futuro confine di intake deve materializzare dati passivi, rifiutare chiavi JSON duplicate e verificare evidenze e byte prima di qualsiasi uso operativo. Non sono introdotti soglie, ranking, consenso dedotto, AP-013/AP-014 o nuove semantiche ADR-019. ADR-020 conserva le query minime approvate e i gate separati di runtime/trasporto.

## Evidenze e residui

Tredici nuovi test coprono covarianze correlate/anticorrelate, segni del gradiente, dati mancanti, singolarità, matrici impossibili, doppio rumore di lettura, overflow e dichiarazioni operative aggiunte. La suite offline complessiva comprende 37 test. Una verifica privata precedente su 256 matrici sintetiche PSD generate come A Aᵀ concorda con un calcolo NumPy indipendente: massimo scarto normalizzato 4.143 × 10⁻¹⁶. È una prova aritmetica limitata, non precisione astrofisica, completezza o falsi positivi. I dataset numerici e la ricevuta restano nell'archivio privato; non sono fixture pubbliche della CI.

L'esempio reale su una coppia pubblica multi-epoca conserva scala/covarianze incomplete e PSF confusa: sigma e significatività restano nulle. Non sono pubblicati immagini, payload, flussi, coordinate, hash privati o calibrazioni Owner. Originali, History e rami scartati restano negli archivi privati già verificati.

Restano da validare modello completo del rumore e della calibrazione, correlazioni da master comuni/resampling, stima della scala, matching astrometrico con moto proprio/covarianze, sorgenti confuse, bande, completezza/falsi positivi e policy quantitativa. S1/S2 aperte, S3 parziale; S4/S5 non implementate/accettate. P6 Accepted con limiti invariati; F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva, S10/Safety invariati.

## Consegna e rollback

Incremento di strumenti offline e documentazione: nessun servizio distribuito o integrazione del portale. Gate: CI dell'esatto commit, ARB indipendente, RQ successiva, merge protetto sul commit atteso e controlli post-merge/Pages. Questo documento non attesta anticipatamente i gate. Rollback mediante revert del package; nessuna migrazione dati o modifica degli archivi scientifici.
