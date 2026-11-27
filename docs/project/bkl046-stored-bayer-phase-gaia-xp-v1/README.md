# Confronto delle quattro fasi Bayer con Gaia XP

Il controllo riusa i flussi separati per le quattro parità e gli spettri Gaia XP già associati alle stelle di IC 1805 e M8–M20. RGGB, BGGR, GRBG e GBRG assegnano blu e rosso a coppie distinte di parità oppure ne invertono l’ordine. Per ogni ipotesi si stima un solo zero cromatico sulle stelle di stima della calibrazione A. La pendenza resta +1. Il P90 dell’errore assoluto sulle stelle di verifica è valutato con due modelli spettrali, tre ricostruzioni e due calibrazioni per campo.

| Campo | Stelle di stima / verifica | Configurazioni con RGGB al primo posto | Minimo vantaggio sul secondo al P90 |
| --- | ---: | ---: | ---: |
| IC 1805 | 13 / 9 | 12/12 | 0,173 mag |
| M8–M20 | 20 / 19 | 12/12 | 0,711 mag |

Il calcolo ha riprodotto le misure e gli errori RGGB già registrati. Il confronto sostiene l’assegnazione cromatica RGGB nelle coordinate archiviate. Le configurazioni condividono le stesse stelle e ogni modello ottico approssima la risposta del sistema. Il controllo riusa dati già analizzati, non misura l’orientamento assoluto del sensore e non qualifica la risposta del lettore nativo.

Per replicare eseguire `misura.py <directory-ingressi> <pacchetti-Python> <nuovo-riscontro.json>`. La directory contiene il protocollo e quattro rapporti fissati per SHA‑256. La prima versione del protocollo riportava il nome del profilo Sony senza il suffisso QE. La correzione lo allinea alla chiave del rapporto ottico archiviato. Le ipotesi, gli ingressi e le regole di confronto sono gli stessi.
