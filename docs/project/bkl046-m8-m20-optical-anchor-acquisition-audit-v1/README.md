# BKL-046 · Inventario della copertura ottica coeva M8/M20

L'audit ha verificato le impronte di quattro archivi di Colmic e di tutti i 60 FITS. Ha confrontato tipo, data e durata con la ricevuta di calibrazione. Le coordinate RA/DEC sono campi del FITS e la verifica le usa come metadati dell'oggetto. [Tutorial e dati della serie](https://siril.org/tutorials/tuto-scripts/index.html)

| Gruppo | FITS | Data iniziale da DATE-OBS | Tipo |
| --- | ---: | --- | --- |
| Pose scientifiche | 15 | 2020-08-18 | Light da 180 s |
| Dark | 15 | 2020-07-09 | Dark da 180 s |
| Flat | 15 | 2020-08-15 | Flat da 3 s |
| Offset | 15 | 2020-07-10 | Bias da 3 s |

Nelle 15 pose `Light` compaiono sei coppie RA/DEC comprese entro 24,8 secondi d'arco dal centro nominale. Il filtro non è indicato nelle intestazioni esaminate. I quattro archivi non contengono un puntamento di cielo separato coevo. L'inventario riguarda i dati verificati e lascia aperta la disponibilità di ulteriori pose presso l'autore della serie o nell'archivio di acquisizione.

Per la prova sull'asse `DIFFUSE_BACKGROUND/2` servono eventuali pose di cielo accoppiate con il registro di puntamento e la configurazione ottica della serie. Se queste non esistono, il piano di raccolta proposto riguarda una nuova serie indipendente da fissare prima delle misure. Il requisito di trasferimento resta definire l'incertezza complessiva dell'interpolazione del fondo, della variazione fra puntamenti e della conversione in ADU. Zero avvii nativi e zero chiusure scientifiche.

La replica legge i quattro ZIP originali per impronta e conserva i valori strutturati delle schede FITS selezionate. Non riscrive i FITS. Usare Python 3.12 con `inventario.py`, passando in ordine il protocollo dell'audit, il protocollo della calibrazione, la ricevuta della calibrazione, gli ZIP Light, Dark, Flat e Bias, e il nuovo percorso per il rapporto.
