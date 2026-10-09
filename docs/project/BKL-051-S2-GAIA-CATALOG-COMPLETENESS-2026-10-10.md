# BKL-051 S2 — controllo della selezione Gaia nel campo pubblico Atami

Stato: **diagnostica privata successiva alla PR546; BKL-051 OPEN / NOT_VALIDATED**. Nessuna associazione, astrometria assoluta, incertezza fotometrica o accettazione S1/S2/S4/S5 deriva da questo incremento.

Il controllo precedente usava `TOP 100` ordinato per magnitudine, con velocità radiale, parallasse positiva e moti propri disponibili. Il limite non consentiva di attestare il catalogo selezionato completo e poteva alterare i vicini più prossimi. Sono conservati i dati originali e tutte le misure native: il nuovo controllo legge soltanto cataloghi pubblici e posizioni già trattenute.

## Acquisizione delimitata e verificata

Quattro richieste pubbliche non autenticate al TAP ESA Gaia DR3: conteggio del cono, conteggio della selezione a sei dimensioni, acquisizione dell'intera selezione e acquisizione del cono senza TOP, limite di magnitudine o filtro a sei dimensioni. Nessun login, upload, retry automatico o nuova dipendenza. Il cono resta quello pubblico Atami già interrogato, raggio 0,2 gradi; non è il campo AT2018cow.

| Controllo | Righe | Evidenza |
| --- | ---: | --- |
| Conteggio di tutte le sorgenti DR3 nel cono | 80.328 | risposta HTTP200 |
| Selezione con RV, parallasse positiva e PM | 585 | conteggio e righe acquisiti coincidono |
| Catalogo senza filtri aggiuntivi | 80.328 | conteggio, righe e ID unici coincidono |
| Moti propri disponibili nel catalogo completo | 57.215 | conteggio locale dei campi presenti |
| Moti propri mancanti | 23.113 | conservati, non sostituiti con zeri |

Catalogo completo: 20.149.284 byte, SHA256 `d4af2e600024e3e16379019a625399fdcd9b288d57d869a307e2fda5e22455ed`. Selezione585: 191.941 byte, SHA256 `022e23fb6bd144fa770e67ab108cc5fc4ba0cdc1f8d7e130ba5e73a1ec742e6e`. Le 585 identità coincidono esattamente con il filtro applicato localmente alle 80.328 righe; gli ID Gaia restano stringhe intere. Quattro risposte HTTP200, trasferimenti entro limiti dichiarati; nessun esito provider dedotto da fixture.

Questa è completezza della **restituzione della query DR3 nel cono fissato**, verificata rispetto al conteggio del medesimo archivio. Non attesta completezza fisica del cielo, recupero degli eventi, copertura completa del sensore, qualità di ogni sorgente o correzione dell'epoca. Il precedente TOP100 e la selezione585 restano separati dal nuovo catalogo.

## Confronto sulle posizioni native conservate

Sono lette 72 posizioni PSF già misurate, su tre epoche del campo Atami. SHA256 degli originali FITS verificato prima e dopo; nessuna nuova estrazione o esecuzione PixInsight, nessun pixel, master, checkpoint, History o ramo fallito modificato.

Per isolare l'effetto del TOP, i cataloghi100 e585 usano lo **stesso modello condizionale** barycentrico rettilineo a sei dimensioni già esistente. L'OBSJD è interpretato condizionalmente come UTC e trasformato in TCB; l'ICRS del file è dichiarato, non attestato indipendentemente. Passando da100 a585, cambia l'identità del vicino più prossimo in **28 delle72 posizioni**.

| Catalogo e modello diagnostico | Minimo | Mediana | Massimo |
| --- | ---: | ---: | ---: |
| TOP100, stesso modello condizionale6D | 0,015729″ | 0,091681″ | 139,170609″ |
| Intera selezione585, stesso modello condizionale6D | 0,015729″ | 0,084853″ | 40,818890″ |
| Intero cono80.328, posizioni all'epoca del catalogo | 0,017616″ | 0,068506″ | 0,215452″ |

La terza riga ha un modello temporale diverso: non corregge moto proprio, osservatore o posizione apparente. Il risultato più piccolo non è una prova di accuratezza astrometrica e non può essere interpretato come associazione accettata. Nessun raggio di associazione, soglia scientifica, significatività o covarianza è stato scelto.

Una formula sferica indipendente da Astropy verifica entrambe le identità più prossime per tutte72posizioni, 144 confronti: differenza numerica massima `1,2444e-10` arcsec. Tolleranza di implementazione `1e-8` arcsec, esplicitamente non soglia scientifica. Tutti72centri conservati cadono nel cono richiesto; distanza massima dal centro0,145640gradi. Ciò non attesta l'intero footprint del sensore.

Il primo avvio della comparazione è stato fermato dall'incompatibilità del Python3.13 locale con le estensioni cp312 delle dipendenze già approvate. Ripetuta con il Python3.12 fornito e Astropy8.0.1/NumPy2.5.3 già autorizzati: PASS, nessuna nuova installazione. Fallimento conservato come storia del prototipo, senza retroattiva attestazione di successo.

## Residui e continuità

Risolto il solo limite di restituzione TOP100 del catalogo: le condizioni RV/parallasse/PM mantengono una selezione molto incompleta rispetto al campo. Restano epoca/esposizione effettive, frame e trasformazione osservatore, propagazione delle covarianze, qualità/ambiguità delle associazioni e incertezza scientificamente verificata. Nessun evento cieco o falso positivo è accettato; questo controllo non completa la pipeline.

Nuova ricerca metadata IRSA21929/21930 del 10ottobre locale: tre risultati e orari invariati, nessuna nuova risposta tecnica attestata; nessun corpo consultato, invio o reinvio. Semantica UNC e provenienza/noise della sottrazione restano irrisolte.

PR546: candidato S4 preparatorio rilasciato sul merge `c3942103366b0bccb20eb7a534877d96f2e2b4cf`; CI23/17, ARB poiRQ zero finding, gate premerge/late validi, 17workflow postmerge e10risorse pubblicate PASS. Pacchetto privato e sorgente pubblico locale verificati. Budget futuro totale10EUR e identità Owner nel solo piano privato; prossimo passo distinto è accesso fresco isolato di sola lettura. Nessuna nuova credenziale, build, deploy o prova GoogleOwner/GCS autorizzata dal presente controllo.

BKL-051 OPEN / NOT_VALIDATED; S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. P6 Accepted nei limiti; F4 lifecycle pending eF5 dopoF4/BKL-050 finale. Nessuna fotografia, invio astronomico, nuova policy quantitativa, comando/dispositivo, Scheduler, Safety Authority o modifica C→F.

Fonti: [accesso programmatico ESA Gaia](https://www.cosmos.esa.int/web/gaia-users/archive/programmatic-access), [estrazione dati ESA Gaia](https://www.cosmos.esa.int/web/gaia-users/archive/extract-data), [controllo TPV precedente](BKL-051-S2-LOCAL-TPV-ADAPTER-2026-10-09.md), [candidato S4](BKL-051-S4-LAB-CLOUD-CANDIDATE-2026-10-09.md), [mandato](DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md). Pagina programmatica non aperta dal browser di ricerca (HTTP451 conservato); descrizione indicizzata ufficiale e quattro query TAP effettive sono le fonti del presente controllo. I CSV e i parametri completi restano nel pacchetto privato.
