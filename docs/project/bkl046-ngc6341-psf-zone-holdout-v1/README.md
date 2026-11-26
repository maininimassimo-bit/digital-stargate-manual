# BKL-046 · Orientazione PSF propria e di zona in NGC 6341

Ho usato le esposizioni ACS F606W da 5 e 90 s e i 736 centri appaiati già archiviati. I centri restano fissati alle misure disponibili per ciascuna posa. Il test confronta la scelta della forma a centro fissato. Ho scelto angolo, larghezza e ali su una posa e valutato la forma sull’altra, con ampiezza e piano locale stimati separatamente. Per la soluzione regionale, l’angolo proviene dalle altre stelle della stessa tessera da 512 pixel sullo stesso CCD. [Prova sulle parità verdi di M8/M20](../bkl046-m8-m20-psf-green-zone-holdout-v1/README.md)

| CCD e posa di stima | Confronti | Guadagno mediano dell’angolo proprio sul circolare | Guadagno mediano dell’angolo di zona sul circolare | Vantaggio mediano appaiato dell’angolo proprio sulla zona |
| --- | ---: | ---: | ---: | ---: |
| 1, 5 s | 339 | −4,1% | −10,8% | +2,5 punti percentuali |
| 1, 90 s | 339 | +1,3% | −6,3% | +3,5 punti percentuali |
| 2, 5 s | 394 | −12,9% | −19,8% | +2,4 punti percentuali |
| 2, 90 s | 394 | −6,9% | −15,8% | +3,4 punti percentuali |

L’angolo proprio ha un vantaggio mediano sulla soluzione di zona in tutti e quattro i confronti. Migliora il riferimento circolare in una delle quattro mediane. Ho misurato 1.466 dei 1.472 confronti. Sei restano esclusi per assenza di vicini. I risultati riguardano le due pose archiviate, con durate diverse, sullo stesso campo. Resta da verificare quanto incidano campionamento, segnale e modello, oltre alla validazione con PixInsight.

Per replicare, passare a `misura.py` il protocollo, `posizioni.json`, la directory dei due FITS, le dipendenze NumPy 2.3.5 e Astropy 7.2.0 e un nuovo rapporto. Il codice verifica gli SHA-256 degli ingressi prima della misura. Il kit H/K conserva il rapporto e gli ingressi.