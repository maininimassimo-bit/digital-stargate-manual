# BKL-046 · Diversità di fase in due pose di NGC 5986

L'asse `CFA_DITHER_DRIZZLE/2` rimane aperto. Il confronto usa 117 identificativi di sorgenti comuni alle pose `j9l915ooq_flc.fits` e `j9l915oqq_flc.fits`. Le predizioni di centro ePSF sono valutate sulle tessere dispari, separate dalle tessere pari usate per stimare la trasformazione affine. Ogni coppia ha lo stesso riferimento e lo stesso chip.

Per ogni sorgente abbiamo misurato la distanza di fase lungo ciascun asse modulo un pixel nativo. La soglia diagnostica è 0,25 px su entrambi gli assi. Per ciascun asse, il limite inferiore e superiore della distanza sono ottenuti sottraendo e sommando i raggi di errore delle due pose, con estremi limitati a [0, 0,5]. Come controlli analitici, lo sfasamento nullo e lo sfasamento di mezzo pixel su entrambi gli assi rimangono distinguibili anche con raggi di 0,10 px per posa.

| Chip | Coppie | Sopra soglia nominale su entrambi gli assi | Somma P90 (px) | Con P90: sopra / sotto / indeterminate | Con 0,10 px per posa: sopra / sotto / indeterminate |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 49 | 10 | 0,1072 | 1 / 28 / 20 | 0 / 11 / 38 |
| 2 | 68 | 16 | 0,0878 | 7 / 33 / 28 | 2 / 18 / 48 |

«Sotto» indica almeno un asse sotto soglia anche al limite superiore. Il totale nominale di 26 coppie si riduce a 8 sotto l'ipotesi dei raggi P90 e a 2 con i raggi fissi. I P90 dei residui radiali descrivono le distribuzioni osservate per posa e chip. Non forniscono una probabilità di copertura congiunta né un limite verificato per ogni sorgente.

Il risultato misura la sensibilità della diversità apparente di fase agli errori di registrazione. Restano da misurare gli effetti della ricostruzione a scala comune e la trasferibilità a sequenze CFA. Zero chiusure scientifiche e zero esecuzioni native.

SHA-256 della ricevuta `a1921e693456ae6e24895cf51e26d0c0bfddb8983fad9d2b6f7acd7da1d14771`.
