# BKL-046 · Associazione delle stelle Bayer di IC 1805 a Gaia DR3

L'asse FILTER_COLOR/3 resta aperto. Il collaudo offline associa le sorgenti delle pose grezze al catalogo pubblico Gaia DR3, poi misura se il colore Gaia BP−RP aiuta a prevedere la variazione del colore Bayer B−R fra aperture di raggio 3 e 6 pixel. Zero avvii nativi e zero chiusure scientifiche.

## Associazione astrometrica

La query ADQL dell'archivio ESA copre un cono di 0,9° al centro del campo e seleziona G < 15,5. Ha restituito 5.210 sorgenti. Il programma propaga i moti propri all'epoca DATE-OBS del FITS aggregato e usa il suo WCS TAN come geometria di riferimento. I flussi del FITS aggregato non entrano nella stima. Orientamento e affine sono stimati solo sul lato pari della scacchiera del catalogo RAW congelato. Le coppie sono reciprocamente più vicine entro 4 pixel nativi e gli ID non associati restano nei denominatori.

| Ripartizione | RAW | Coppie | Zone | Residuo P90, pixel nativi |
| --- | ---: | ---: | ---: | ---: |
| Stima | 101 | 70 | 17 | 0,476 |
| Controllo spaziale | 104 | 66 | 16 | 0,380 |
| Controllo spaziale con ascisse rimescolate | 104 | 2 | 2 | 3,792 |

L'esito supera i criteri fissati prima dell'esecuzione per questo abbinamento: almeno 16 coppie in 7 zone di controllo, P90 ≤ 3 pixel e al massimo 3 coppie nel controllo rimescolato. Il cono è più stretto del campo di circa 2,96° in larghezza. Il residuo misura l'associazione sul sottoinsieme coperto e non qualifica la registrazione nativa fra tutte le pose o l'accuratezza assoluta del WCS.

## Verifica esplorativa del colore

L'intersezione contiene 39 stelle con misure Bayer utilizzabili, BP e RP con rapporto flusso/errore ≥ 20 e seconda sorgente del sottoinsieme Gaia proiettata a più di 8 pixel dalla posizione prevista. Per il test del colore si usa la ripartizione per righe del protocollo Bayer esistente, distinta dalla scacchiera astrometrica. Il modello lineare in BP−RP e la mediana di confronto sono stimati su 18 stelle con la calibrazione A. Entrambi sono poi applicati sulle restanti 21 stelle usando le calibrazioni A e B. Due stelle di controllo cadono fuori dall'intervallo di colore della stima.

| Metodo | P90 con mediana, A / B (mag) | P90 con BP−RP, A / B (mag) |
| --- | ---: | ---: |
| drop 1,0 | 0,04786 / 0,05259 | 0,03658 / 0,04105 |
| drop 0,7 | 0,05255 / 0,05274 | 0,03664 / 0,03911 |
| Bilineare per parità CFA | 0,03103 / 0,03277 | 0,03226 / 0,03185 |

BP−RP riduce l'errore per entrambi i drop, con esito misto per la bilineare. Il bersaglio è una differenza di colore tra aperture della stessa camera. Restano da misurare il colore assoluto calibrato, la trasferibilità su un secondo campo e l'incertezza del modello su un campione indipendente. Il precedente collaudo della stabilità delle aperture resta valido.

## Riproducibilità

- Archivio fisico H: `Produzione/2026-10-13/Digital-StarGate-PixInsight/archives/BKL046-IC1805-Gaia-e205be51911b.zip`.
- `riscontro.json` SHA-256 `e205be51911ba9d4ea5a8132c0ec2dc2133f5049049e02da0f0531be75912071`.
- `riscontro-colore.json` SHA-256 `57498643d2aa8da59c854e11e613646373a76b53af8eb93a1cc45109a3fd8062`.
- La query `query-esa.adql`, il CSV `gaia-esa.csv` e i programmi sono conservati con le ricevute. Le ricevute fissano impronte dei dati di ingresso e programmi. Python usa NumPy 2.3.5 e Astropy 7.2.0.
- [Gaia DR3, descrizione del catalogo ESA](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html)
