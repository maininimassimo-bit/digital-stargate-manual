# ACS 17895 · Due nane bianche nel dominio di flusso CTE

Il campione comprende tutte le 12 associazioni pubbliche HST di WDFS0122-30 e WDFS0458-56 nei filtri F435W, F606W e F814W, con due visite per sorgente. Le richieste MAST mancanti sono state recuperate con una richiesta multipla. Il campo `parent_obsid` lega ogni membro all'associazione, mentre `obsID` individua il prodotto singolo. Sono stati verificati due RAW e due FLT e un ASN, un CRJ e un DRZ per associazione. Il mirror CADC conferma URI e dimensioni dei 36 prodotti di associazione. MAST non elenca FLC o CRC in queste associazioni. [Piani ACS](https://www.stsci.edu/hst/instrumentation/acs/calibration/calibration-plans) · [Servizio MAST CAOM Products](https://mast.stsci.edu/api/v0/_services.html) · [CADC TAP](https://www1.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/doc/tap/)

Sono stati acquisiti e verificati tutti i 12 DRZ. Il controllo legge i due nomi FLT dall'header di AstroDrizzle e li confronta con i membri CALACS. Si proietta la posizione Gaia DR3 propagata all'epoca dell'immagine, con soglia di quattro pixel per il massimo locale. La soglia esplorativa di contrasto, introdotta dopo aver osservato un picco debole, richiede un picco di almeno otto volte la dispersione robusta del fondo. L'apertura richiede peso positivo e contributo di entrambe le pose nel piano CTX. Il riscontro conserva tre esclusioni per posizione e due per contrasto. [Identità Gaia delle due sorgenti in CALSPEC](https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec)

| Risultato | Esito |
| --- | --- |
| DRZ con misura esplorativa | 7/12 |
| Visite con tutte e tre le bande | jfjv15 WDFS0458-56 e jfjv17 WDFS0122-30 |
| Conteggio a raggio 3 nelle due terne | 59.403–66.385 e⁻ |
| Conteggio a raggio 5 nelle due terne | 65.562–74.533 e⁻ |
| Fondo nelle due terne | 2,14–3,85 e⁻/px |
| Apertura strumentale nelle 12 associazioni | WFC1B-1K |

Le due terne rientrano nel dominio di **flusso** del calcolatore CTE. La prova non applica la correzione: occorrono il numero di trasferimenti dai FLT originali, il controllo di saturazione e maschere nei singoli input, e una valutazione dell'incertezza a fondo basso. Un confronto temporale indipendente per la stessa stella richiede una seconda visita con attribuzione verificata. Nessun contrasto tra amplificatori, nessun avvio nativo, zero chiusure scientifiche. [Calcolatore ACS CTE](https://acsphotometriccte.stsci.edu/)

Ripetizione byte per byte dall'archivio H:. SHA-256 riscontro `c1e86415ee16f47a7b7c1a84ce235ceeb2e1df04ac1f89cbc5fba726a1154d0a`. SHA-256 archivio `e5d560dd1a8b04ef41bf897376972807cea368c3c9264806aeda6d41e84b2ef1`.

[Verifica del dominio per GD153](BKL-046-GD153-ACS-CTE-DOMINIO.md).
