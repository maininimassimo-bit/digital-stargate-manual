# BKL-051 S2 — Adapter locale TPV e controlli PSF reali

| Campo | Valore |
|---|---|
| Data | 2026-10-09 |
| Stato | Implementazione diagnostica; NOT_VALIDATED |
| Decisione | Astropy 8.0.1 e NumPy 2.5.3 locali autorizzati dall'Owner |
| Runtime | Adapter selezionato esplicitamente; nessuna integrazione o attivazione cloud |

## Problema e soluzione

PixInsight 1.9.5 build1706 non importa la proiezione TPV dei FITS pubblici verificati. I fit PSF nativi restano validi come diagnostica geometrica, senza astrometria celeste nativa attestata. TPV aggiunge una distorsione polinomiale a TAN: cambiarne soltanto la sigla eliminerebbe informazioni. L'adapter locale `tools/scientific_transients/tpv_coordinates.py` applica il WCS originale con Astropy, senza cambiare header o pixel.

La [decisione Owner](evidence/BKL-051-OWNER-LOCAL-TPV-2026-10-09.json) e l'[ADR-020 aggiornato](../architecture/ADR-020-Private-Scientific-Transient-Analysis.md) autorizzano le dipendenze del solo worker locale. Le verifiche private pregresse non costituivano autorizzazione runtime; la nuova decisione è esplicita. Nessuna build/attivazione cloud, credenziale, soglia scientifica, segnalazione o pubblicazione di fotografie.

## Contratto locale ristretto

Un chiamante fidato fornisce percorso locale, digest SHA256 atteso, geometria, convenzione e un massimo di 1.024 centri con riferimenti opachi unici. Sono limiti di risorse, non criteri astronomici. L'adapter rifiuta link/reparse tramite il controllo locale esistente, verifica dimensione massima 128 MiB e digest e analizza una sola snapshot di byte. È solo FITS non compresso con un PrimaryHDU bidimensionale: estensioni, header oltre 64 blocchi FITS e dati troncati sono rifiutati. Non è un intake di percorsi da portale né un parser generale di ogni FITS.

Richiede RA---TPV/DEC--TPV, unità esplicite deg, CRPIX/CRVAL/CD e coefficienti PV per entrambi gli assi, finiti e di ordine ammesso (0–39). Rifiuta card WCS duplicate, matrici miste, SIP/table distortion, WCS alternativi e frame ambigui. L'assenza di frame non viene inventata. La posizione viene espressa nel frame dell'header, senza trasformazione tra frame o attestazione della sua correttezza.

Le coordinate `PI_NATIVE_GEOMETRIC` di PSF.c0 vengono convertite sottraendo 0,5 prima di `all_pix2world(..., origin=0)`. La convenzione FITS_SAMPLE_INDEX_ZERO non viene traslata. I punti devono rimanere nei centri dell'immagine; output non finiti/fuori dall'intervallo celeste sono rifiutati. Astropy/NumPy devono avere le versioni autorizzate. L'adapter non risolve l'epoca osservativa, non propaga moto proprio o covarianze, non associa cataloghi e non calcola significatività.

Restituisce un oggetto privato con digest/byte/geometria/versioni/convenzione, frame/equinozio dichiarati e coordinate. Sempre NOT_VALIDATED/NOT_EVALUATED, frameAttested false, observationEpoch e positionalCovariance null, associationAccepted false. Non effettua I/O di rete, non scrive ricevute, non lancia PixInsight e non cambia il rapporto/coda/interfaccia. La conservazione esclusiva dell'output nel journal è responsabilità del chiamante e l'integrazione nel workflow completo resta aperta.

## Dipendenze e prove

`requirements-astrometry-local.txt` fissa Astropy 8.0.1, NumPy 2.5.3, pyerfa 2.0.1.5, astropy-iers-data 0.2026.10.5.1.0.7, PyYAML 6.0.3 e packaging 26.3. Sono opzionali rispetto al servizio cloud attuale. La CI S1 installa questo insieme in due job dedicati Windows/Linux, verifica `pip check` e lancia esplicitamente il modulo `tpv_coordinates_checks`; la discovery cloud senza queste dipendenze resta invariata. Nessuna installazione o modifica dell'ambiente cloud produttivo è dichiarata.

Versioni installate e requisiti obbligatori sono verificati con i metadati delle distribuzioni private già conservate; materiali di licenza e digest METADATA sono registrati nel dossier locale. Astropy/astropy-iers-data/pyerfa: BSD-3-Clause; PyYAML: MIT; packaging: Apache-2.0 OR BSD-2-Clause. NumPy dichiara BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0, includendo materiali vendorizzati. Conservare gli avvisi nella distribuzione locale; nessun codice terzo o wheel viene copiato nel repository. Il controllo non attesta una catena di distribuzione firmata o rende completo il deployment.

Dieci test sintetici: centro noto, mezzo pixel, polinomio di secondo ordine contro formula gnomonica indipendente, frame mancante, digest/geometria, coordinate invalide e duplicati, WCS incompatibili/duplicati/ordine, unità/proiezione/PV mancanti, estensione/troncamento, versioni/limite byte. Il confronto numerico è un known-answer sintetico, non precisione astrometrica assoluta.

Applicazione locale ai centri già conservati: sei FITS reali e 108 fit PSF, 72 nel campo pubblico Atami e 36 nel controllo noto AT 2018cow. Solo trasformazione, nessun nuovo lancio nativo o query per questa regressione. Ricevute private ancorate al digest del componente. Un secondo controllo privato valuta direttamente i 40 termini polinomiali TPV NASA e la proiezione gnomonica senza usare Astropy WCS per il calcolo indipendente: i 108 centri differiscono al massimo di 2,143 × 10⁻¹⁰ arcsec numerici sui sei header, con LONPOLE 180. La tolleranza è numerica e non una soglia astronomica; non prova precisione assoluta del WCS originale. Astrometria assoluta e associazioni rimangono non validate.

## Evidenze scientifiche nuove, distinte dal rilascio precedente

PR #529 è integrata sul merge 2b66c184964ced44ec4b168b6740f024f255929d: 15 workflow post-merge e sette endpoint Pages verificati. Il contratto fotometrico proposto resta distinto da questa nuova prova.

Sul campo Atami sono completati 72 fit Gaussian/Moffat, 2.583.992 campioni identici ai precedenti import verificati, originali invariati e processo dedicato fermo. Tre checkpoint XISF e History iniziale/corrente conservati. MAD del fit non è un errore formale di flusso; minore MAD non seleziona automaticamente il modello. Confronto TPV esterno col catalogo della stessa esposizione è diagnostico, non riferimento indipendente assoluto.

Per un controllo positivo reale sono stati consultati metadati pubblici di SN 2023ixf: 39 righe, ma primo originale/ritaglio richiesto HTTP404; nessun prodotto utilizzabile attestato. Tentativo conservato. Successivamente ottenuti sei FITS originali science/mask di AT 2018cow: tre epoche nella stessa banda ZTF_r, due precedenti e una successiva all'evento noto. 36 fit nativi completati, 169.932 pixel coincidenti bit per bit con l'import affine indipendente, originali invariati, processo fermo, tre checkpoint e History conservati. Il centro usa coordinate pubblicate e i cinque ulteriori semi per epoca sono pixel brillanti separati, non stelle classificate o assunte stabili.

Il primo controllo di maschera b==0 escludeva anche flag di sorgente: somme diagnostiche nulle non sono misure valide. Versione successiva conserva i flag, distingue i bit di difetto con la maschera diagnostica preesistente 6141 e mantiene null errore/significatività/limite. Un primo verifier ha fallito per shadowing Python; corretto senza rilancio PixInsight. Tutti i rami sono conservati. La galassia ospite, PSF, correzione d'apertura e modello completo del rumore impediscono di accettare la fotometria. Il controllo è selezionato, non cieco, non copre ogni nova o variabile.

Archivi privati verificati: fase PSF Atami 104 file, fase eventi 103 file, checkpoint/script/parametri, manifest e prove fallite inclusi. I genitori esterni restano richiesti; History a monte non attestata. Nessuna foto Owner approvata rielaborata e nessuna fotografia pubblicata. IRSA ha accusato ricezione della richiesta tecnica con ticket IRSASD-21929; nessuna risposta statistica attestata.

## Gate e residui

Gate del presente package ancora da completare: CI exact-head, ARB poi RQ, merge protetto e post-merge/Pages. Rollback: revert coerente del componente/dipendenze/documenti e rigenerazione delle projection; conservare le evidenze e tornare al risultato di astrometria incompleta per TPV.

BKL-051 OPEN / NOT_VALIDATED. Restano verifica astrometrica indipendente, epoca/moto proprio/covarianze, budget del rumore e calibrazione, sottrazione/PSF giustificate, recupero e falsi positivi su prove cieche reali, policy quantitativa Owner, integrazione scientifica e rapporto completo, residui del servizio distribuito, reporting CBAT/TNS/VSX/MPC e accettazione S5. Questo adapter non completa S2 o la milestone. P6 Accepted nei limiti, F4 lifecycle pending, F5 dopo F4 e BKL-050 conclusiva; S10/Safety e C→F invariati.

## Fonti primarie

- [NASA FITS registry: TPV](https://fits.gsfc.nasa.gov/registry/tpvwcs/tpv.html), polinomio/distorsione e convenzioni.
- [Astropy: proiezioni supportate](https://docs.astropy.org/en/stable/wcs/supported_projections.html).
- [IRSA: API](https://irsa.ipac.caltech.edu/docs/program_interface/ztf_api.html) e [percorsi dei prodotti](https://irsa.ipac.caltech.edu/docs/program_interface/ztf_metadata.html).
- [TNS: AT 2018cow](https://www.wis-tns.org/object/2018cow); [studio di SN 2023ixf](https://arxiv.org/html/2306.04721v2). Eventi noti selezionati, nessuna nuova scoperta.
