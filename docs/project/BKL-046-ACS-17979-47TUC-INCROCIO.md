# ACS 17979 · Incrocio tra visite 02 e 06

Sono state riesaminate le coppie FLT/FLC archiviate delle visite 02 e 06, escludendo il puntamento centrale in sola guida giroscopica della visita 02. La selezione densa usa la visita 02 come riferimento, mantiene i controlli su DQ, isolamento, distanza astrometrica e differenza Y di almeno 550 trasferimenti e valuta soltanto coppie tra visite. I calcoli usano PAM e PHOTFLAM. Il riscontro conserva tutte le 340 candidate e il dettaglio dei rifiuti. [Calibrazione e correzioni CTE ACS](https://www.stsci.edu/hst/instrumentation/acs/performance/cte-information)

Delle quattro coppie ammesse, due sono sullo stesso chip WFC1. Si tratta delle stesse due sorgenti ottenute con la griglia preliminare. Le coppie distano 83,065 giorni, con differenza di orientamento di 52,43°. Le separazioni astrometriche sono 0,0564″ e 0,0576″. In entrambi i casi la posizione passa da una metà X di WFC1 all'altra.

| Differenza Y | Contrasto FLT | Contrasto FLC | Contrasto con modello parallelo |
| ---: | ---: | ---: | ---: |
| 1336 trasferimenti | +409,25 mmag | −14,57 mmag | +15,07 mmag |
| 700 trasferimenti | +10,44 mmag | −24,59 mmag | −39,69 mmag |

In un caso le correzioni riducono il contrasto assoluto. Nell'altro lo aumentano. Il cambio di metà del rivelatore, l'epoca, il rollio e possibili differenze di risposta o di sorgente restano nel confronto. [Geometria e amplificatori ACS/WFC](https://hst-docs.stsci.edu/acsihb/chapter-7-observing-techniques/7-7-acs-apertures)

Il controllo WCS su una griglia da 32 pixel distingue la copertura geometrica dalla copertura fotometrica. Tra jfln02010 e jfln06010 risultano 1.959 punti campionati con stessa metà del chip e almeno 550 trasferimenti di differenza. Una selezione esplorativa da quella regione ha prodotto 60 candidate in celle da 16 pixel. Nel secondo puntamento, 39 sono escluse per supporto DQ, 18 per sorgente debole o scostata, due per il dominio del modello e una per possibile sovrapposizione o artefatto. Non risulta alcuna coppia qualificata nella stessa metà. Non si estende questa conclusione alle altre combinazioni di puntamento. Zero avvii nativi e zero chiusure scientifiche.

I tre riscontri sono stati riprodotti byte per byte a partire dall'archivio su H: e dai due archivi dei FITS già riletti su H:. Riscontro fotometrico SHA-256 `d269f07b09669bef7e9a77a4a411c7a6f6605b09de52a33f5f6fcac9ed726882`. Geometria SHA-256 `13fc8751c5f12ce5e7f33d04a5a6242d3bd24e51e5ace60315aaabe5da4e49f8`. Stessa metà SHA-256 `c21abdc9f546cdd0d72dfef9e221bde49b4b1c72bbd330665925870cb96d4ae9`. Archivio SHA-256 `37313fcc11eaed1afee0b8b33a6b15f4f0a898bdf44dc8cbb1b46c87236ee25a`.

[Visita 02](BKL-046-ACS-17979-47TUC-CTE.md) · [Visita 06](BKL-046-ACS-17979-47TUC-VISITA06.md).
