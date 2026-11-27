# BKL-046 · Risposta ACS per chip ed epoca nelle visite GD71 del 9020

La sintesi ripete l'integrazione F658N e F660N alla data di ciascuna delle otto pose. Per WFC2 sostituisce la componente di risposta dipendente dal tempo del chip, lasciando fisse le altre tabelle della catena. La risposta ricostruita concorda con PHOTFLAM degli header entro lo 0,00025% in tutte le pose. Il controllo usa quattro e otto nodi di quadratura. [Throughput ACS STScI](https://www.stsci.edu/hst/instrumentation/acs/instrument-design/system-throughputs)

| Quantità | Differenza j8c103 rispetto a j8c104 |
| --- | ---: |
| Rapporto F658N/F660N osservato, 3 px | +1,699% |
| Rapporto osservato, 5 px | +1,504% |
| Rapporto sintetico Gaia con chip ed epoca specifici | +0,0000311% |
| Rapporto sintetico CALSPEC con chip ed epoca specifici | +0,0000309% |

Per questi ingressi la sintesi produce gli stessi rapporti usando WFC1 a entrambe le epoche. La componente modellata di throughput per chip ed epoca da sola non risolve la differenza osservata. Le pose reali cambiano chip, amplificatore e visita. Le misure sono ad apertura finita e le previsioni ad apertura infinita. Restano aperti CTE, orientamento e profilo della PSF, sistematiche e attribuzione causale.

Per ripetere, passare protocollo, ricevuta della fotometria 9020, directory dei FITS, confronto precedente e relativo verificatore, spettro CALSPEC, spettri Gaia, protocollo ACS, directory con la componente WFC2 e nuovo file di uscita. L'archivio di progetto conserva il FITS WFC2 originale. Nessuna nuova esecuzione PixInsight o chiusura scientifica.
