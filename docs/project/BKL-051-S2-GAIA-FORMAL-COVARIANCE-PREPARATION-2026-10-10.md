# BKL-051 S2 — preparazione delle covarianze formali Gaia

Stato: **preparazione matematica del solo riferimento di catalogo; NOT_VALIDATED**. Nessuna associazione, incertezza delle immagini o astrometria assoluta accettata. Incremento successivo al [controllo del catalogo completo](BKL-051-S2-GAIA-CATALOG-COMPLETENESS-2026-10-10.md).

Il catalogo già acquisito conserva cinque errori formali e dieci correlazioni. Ignorare questi termini o trattare come indipendenti epoche riferite alla stessa sorgente può produrre covarianze errate. Il componente separato ricostruisce la matrice formale e prepara un modello lineare esplicitamente condizionale; non viene collegato alle decisioni della coda o a una policy di associazione.

## Dati e modello

Si leggono soltanto il CSV DR3 completo verificato nella fase precedente e i due vicini diagnostici di ciascuna delle72posizioni native conservate. **32identità di catalogo distinte**, non associazioni accettate. SHA256 CSV `d4af2e600024e3e16379019a625399fdcd9b288d57d869a307e2fda5e22455ed`; identità e riferimento precedente fissati nelle ricevute private. Nessuna nuova query TAP, dipendenza, misura nativa o modifica di dati.

Assi della matrice: `α*`, `δ`, `ϖ`, `μα*`, `μδ`; unità `mas, mas, mas, mas/yr, mas/yr`. Ogni elemento ha il prodotto delle unità dei suoi due assi. `ra_error` Gaia è **già** moltiplicato per cosδ: nessuna seconda moltiplicazione. `ref_epoch` è anno giuliano TCB. Verificato nel [modello dati ufficiale DR3](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html).

Ricostruzione `Cᵢⱼ = σᵢ σⱼ ρᵢⱼ`, con diagonale `σᵢ²`. Errori positivi e finiti, correlazioni entro[-1,+1], Cholesky della matrice di correlazione per consistenza matematica, valori derivati rappresentabili e diagonali non nulle. Un insieme di correlazioni singolarmente ammesse ma incompatibile con una matrice positiva viene respinto. Questi controlli non sono tagli di qualità astronomica o soglie di significatività.

Campi mancanti: matrice5D **UNAVAILABLE**, elenco dei campi assenti e nessuno zero inventato. È una matrice marginale dei cinque assi astrometrici; non si deduce il tipo di soluzione Gaia dai soli errori disponibili.

Proiezione solo sul piano tangente fissato:

`J(t) = [[1,0,0,Δt,0], [0,1,0,0,Δt]]`, `Cpos(t) = J(t) C J(t)ᵀ`.

Per la stessa sorgente a due epoche si conserva `Cpos(tₐ,tᵦ) = J(tₐ) C J(tᵦ)ᵀ`. Il singolo blocco tra epoche non deve essere simmetrico; invertendo le epoche si ottiene il suo trasposto. Non si assumono epoche indipendenti. Le ripetizioni dei modelli PSF della stessa epoca condividono anche il medesimo riferimento.

Il modello è **lineare a piano tangente fissato**, non propagazione rigorosa6D, posizione apparente o correzione dell'osservatore. La colonna di parallasse nel Jacobiano è nulla soltanto perché questo modello non include la parallasse dell'osservatore: non è una misura di parallasse nulla. Epoca effettiva OBSJD→UTC→TCB e ICRS del FITS restano condizionali come nella fase precedente.

## Esiti privati e verifiche

| Controllo | Esito |
| --- | ---: |
| Vicini di catalogo distinti | 32 |
| Matrici formali5D ricostruibili | 27 |
| Matrici5D incomplete, mantenute indisponibili | 5 |
| Coppie posizione/vicino tra le epoche | 144 |
| Proiezioni condizionali disponibili | 124 |
| Proiezioni indisponibili | 20 |
| Blocchi del riferimento condiviso tra epoche | 51 |

Otto test significativi PASS: unità e correlazioni, dati mancanti, valori invalidi, correlazioni incoerenti, termini incrociati posizione/moto, epoche e forme invalide, blocchi tra epoche e overflow/underflow. CI Windows/Linux include la suite. Il primo prototipo senza blocchi condivisi e le successive ricevute sono conservati; nessuna versione precedente è presentata come quella finale.

Sul catalogo reale già acquisito, confronto indipendente NumPy: `diag(σ) ρ diag(σ)`, `J C Jᵀ` e `Jₐ C Jᵦᵀ`. Tutte27matrici di correlazione hanno autovalori positivi; minimo0,1419671171, dato di consistenza senza soglia astronomica. Differenza numerica massima di ricostruzione5,56e-17 nelle unità proprie dei singoli elementi; per proiezioni e blocchi4,45e-16mas². Tolleranze del confronto numerico soltanto, nessuna policy scientifica. Componente pubblico e prototipo privato byte-identici, hash fissato nella ricevuta finale. Nessuna nuova installazione: NumPy2.5.3 già autorizzato, con il Python3.12 esistente.

## Gate residui

Non vengono sommate covarianze delle immagini né calcolate likelihood, significatività, raggio di match, upper limit o classificazioni. Restano centroidi e covarianze native verificate, qualità Gaia/RUWE/excess-noise e tipo di soluzione, sistematiche e correlazioni spaziali, velocità radiale/covarianze mancanti, frame/timing/observer e propagazione rigorosa. La precisione formale Gaia non è l'errore calibrato di una posizione ZTF o della sottrazione fotometrica.

Sorgenti scelte come vicini statici nella fase precedente, non controparti accettate. Incompletezze e dipendenze fra epoche non sono eliminate per far risultare validata la prova. IRSA semantica UNC e rumore/provenienza della sottrazione restano irrisolti; nessuna nuova risposta o invio deriva dal presente lavoro.

PR546 candidata S4 resta preparatoria e fissata al suo merge `c3942103366b0bccb20eb7a534877d96f2e2b4cf`: sorgente/piano della prossima proposta di sola lettura non aggiornati implicitamente alla main. Budget futuro totale10EUR e Owner scelto nel solo piano privato. Prima del live: nuovo accesso isolato autorizzato, letture/costi EUR verificati, poi distinta build/retention e dopo digest effettivo distinta attivazione/OAT/verifica GCS/arresto. Nessuna nuova credenziale, build o deploy.

BKL-051 OPEN / NOT_VALIDATED; S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. P6 Accepted nei limiti; F4 lifecycle pending, F5 dopoF4/BKL-050 finale. Nessuna nuova fotografia, invio astronomico, soglia quantitativa Owner, misura PixInsight, dispositivo, Scheduler, Safety Authority o modifica C→F.

PR547 verificata dopo il merge `8fba0c9833dff2d3f13d5e39db8a2bd15aa3317c`: 14 workflow postmerge e 10 risorse pubblicate PASS; archivio privato55elementi CRC e ogni SHA256 verificati. Il primo verificatore postmerge ereditava un marker S4 non pertinente al nuovo handover; corretto in v2 con il marker effettivo del dossier Gaia, originale conservato. Nessun dato prodotto o gate di CI/review modificato.
