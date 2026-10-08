# BKL-051 — evidenze di misura e residui scientifici

Stato: preparazione offline proposta, non contratto operativo accettato. P6 rimane Accepted nei limiti del dossier; S1/S2 restano aperte. Nessun runtime del modulo, soglia, classificazione o trasporto privato attivato. La decisione Owner [ADR-020](../architecture/ADR-020-Private-Scientific-Transient-Analysis.md) resta invariata.

## Riconciliazione successiva delle origini pixel

[Contratto e ramo corretto](BKL-051-S2-PIXEL-CONVENTION-2026-10-08.md). Export WCS fitted nativi richiedono indice+0,5 una sola volta; aperture sample-index usano distanze campione-campione. Le vecchie misure e diagnostiche restano storiche, non valide per inferenza. Coorte comune raccordata dopo correzione; budget dipendenti dalle aperture ancora da riconciliare. Nessuna soglia/precisione scientifica accettata.

## Evidenze riconciliate

Le prove private successive alla PR #501 comprendono selezione di qualità sulle esposizioni originali, tre epoche distinte con ripetizioni nella stessa notte, soluzioni astrometriche native e confronto esterno limitato. Pixel dei derivati astrometrici identici e originali invariati. Il confronto esterno non certifica epoca/moto proprio, indipendenza dei cataloghi o accuratezza fotometrica.

La calibrazione di camera selezionata dall’Owner consente un trasferimento condizionale di unità, verificato con raw, dark e flat effettivamente usati. Non completa il modello del rumore: calibrazioni condivise, fondo mediano, interpolazione/cosmetica e contaminazione introducono dipendenze o sistematiche. La risposta del filtro Owner rimane non attestata. Nessuna equivalenza con la banda pubblica viene inferita.

Le iniezioni numeriche, su copie di ritagli reali, comprendono 168 checkpoint con History. Profili gaussiani ideali e livelli rapportati al solo rumore del cielo non sono S/N totale; differenze con il medesimo genitore cancellano il rumore condiviso. Recuperi e controlli non certificano completezza o tasso di falsi positivi. Una prova isolata sulla dimensione minima del rilevatore spiega alcuni recuperi nei ritagli, senza promuovere il parametro a default di produzione.

Acquisiti da IRSA dieci immagini scientifiche pubbliche e le rispettive maschere, su due eventi storici noti, con provenienza, epoche, WCS TPV e ricevute conservate privatamente. Dieci checkpoint PixInsight e History verificati; due aperture difettose/sature escluse. La rappresentazione numerica usata per il caricamento nativo è documentata nel dossier, senza clipping, stretch o interpolazione. Il WCS pubblico letto da Astropy non è una soluzione nativa di questi checkpoint.

Un caso reale non recuperato con le impostazioni iniziali è recuperato abilitando separatamente `allowClusteredSources`. Il catalogo PSF pubblico della stessa esposizione contiene una sorgente alla posizione nota; è un confronto di metodi sulla stessa acquisizione, non una conferma indipendente. La modifica è verificata su dieci campi completi e aumenta il numero di sorgenti in alcuni campi. Ciò non prova che le rilevazioni aggiuntive siano affidabili né che il deblending sia fotometricamente valido. I bit ZTF informativi di sorgente sono distinti dai difetti; i tentativi che applicavano una maschera errata restano conservati ed etichettati.

## Incremento offline proposto

`tools/scientific_transients/measurement.mjs` ispeziona oggetti già materializzati dal chiamante locale. Schema chiuso, identità dell’immagine, unità ADU esplicite, metodo ad apertura in posizione nota, epoca UTC o unknown, riferimenti SHA256 a misura/maschera/ricevute, difetti/saturazione/confusione e due diagnostiche del rilevatore. Non legge pixel o file, non verifica le dichiarazioni, non risolve WCS, non misura, non esegue rete e non concede consenso.

Questo non è un parser di JSON grezzo o un boundary di trasporto: il chiamante deve conservare byte originali e usare un parser stretto per rifiutare chiavi duplicate prima di costruire oggetti. Il parser intake esistente non accetta questo schema diverso. L’identità dichiarata e i riferimenti non attestano autonomamente l’ancoraggio dei parametri, l’indice dell’immagine o la verità dei risultati. Queste verifiche restano nel preparatore/manifest privato.

Il risultato è sempre `NO_NEW_ANALYSIS_EXECUTED`, `NOT_EVALUATED`, revisione richiesta e policy non accettata dall’ispettore. Difetti e saturazione dichiarati producono un rifiuto locale; gli altri casi restano esplorativi non validati. Flussi nulli/negativi non diventano limiti di non rilevazione, distanze piccole non diventano match operativi, maggiori conteggi non diventano nuovi candidati. Non accetta un modello d’incertezza “completo” auto-dichiarato.

Nove nuovi test sintetici verificano questi invarianti; insieme ai test precedenti sono 24 test offline. Un’applicazione privata alle dieci osservazioni pubbliche ha prodotto due rifiuti per qualità locale e zero classificazioni. Non sono dieci nuovi eventi né una misura di precisione scientifica.

## Requisiti ancora aperti

| Fase | Residui |
|---|---|
| S1 | Contratto completo di incertezza/comparabilità, algoritmo e soglie prima dell’uso; trasporto privato concreto da revisionare |
| S2 | Cross-match ripetibile con epoca/moto proprio/covarianze; verifiche di incertezza, copertura, troncamento e indisponibilità nel runtime |
| S3 | Ricerca cieca; dataset e campi di controllo rappresentativi; recupero e falsi positivi; PSF/differenza compatibile; artefatti, sorgenti confuse, mobili e filtri incompatibili |
| S4 | Percorso Owner completo, adapter SDE dedicato, autorizzazioni negative, ripresa/annullamento/idempotenza, report privato |
| S5 | Soglie Owner approvate su evidence, regressioni/UI, gate di rilascio e accettazione operativa distinta dalla P6 |

Nessuna chiusura proposta. F4 attende lifecycle reale, F5 segue F4, BKL-050 rimane conclusiva. S10/Safety invariati. Nessuna fotografia, percorso Owner, coordinata protetta o calibrazione privata è inclusa in questa pagina.

## Verifica e rollback

Eseguire `node --test tools/scientific_transients/contract.test.mjs tools/scientific_transients/reference.test.mjs tools/scientific_transients/measurement.test.mjs`. Il workflow specialistico esegue gli stessi test su Linux e Windows. Le prove native/private restano nel dossier locale con manifest e archivi genitore; dipendenze e percorsi esterni impediscono di chiamarlo replay autonomo.

Consegna subordinata a exact-head CI, ARB, RQ, branch zero behind, merge protetto e post-merge/Pages. Rollback mediante revert dell’incremento offline e delle note additive, rigenerando le proiezioni dalle source e conservando immutati i dossier privati. Non cambia registry, broker o infrastruttura.

Fonti dei prodotti pubblici: [IRSA/ZTF API](https://irsa.ipac.caltech.edu/docs/program_interface/ztf_api.html), [metadata e prodotti PSF](https://irsa.ipac.caltech.edu/docs/program_interface/ztf_metadata.html), [definizione delle maschere ZTF](https://irsa.ipac.caltech.edu/data/ZTF/docs/ztf_pipelines_deliverables.pdf). Nessuna raccomandazione numerica operativa derivata automaticamente da queste fonti.
