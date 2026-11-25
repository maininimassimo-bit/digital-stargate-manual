# BKL-046 · Classificatore delle origini XDRZ

Il verificatore applica lo stesso predicato numerico del comparatore CFA v4 agli otto FITS dei quattro controlli fattoriali. Verifica l'insieme esatto dei nomi, forma RGB 3 × 28 × 32, campioni finiti, pesi non negativi e integrità dei file rilette alla fine. Registra gli SHA-256 e le corrispondenze per caso. Una sequenza è riconosciuta solo quando ciascun caso corrisponde a una sola mappa congelata e la sequenza completa coincide con una delle tre ipotesi.

| Caso offline | Esito |
| --- | --- |
| Origine dichiarata, zero fisso e 0,5 fisso | Riconosciute le tre sequenze distinte. |
| Quattro mappe di riferimento valide | Sequenza fuori modello. |
| Mappa RGB e mappa dei pesi incompatibili | Caso irrisolto. |
| FITS assente, in eccesso o con NaN | Ingresso respinto. |

Il piano è una proposta separata da sottoporre a revisione. Un risultato numerico riconosciuto richiede comunque la verifica dei casi effettivamente eseguiti, dell'origine dei file e dell'ammissione. Le fixture sono ricavate dagli oracoli sintetici. Nessuna esecuzione PixInsight e nessuna modifica del piano v4. [Previsioni fattoriali](../bkl046-cfa-origin-factorial-v1/README.md)

Il comando riceve la directory del piano, la directory dei FITS attesi e della ricevuta fattoriale, il comparatore v4 verifica.py, la directory delle dipendenze NumPy 2.3.5 e Astropy 7.2.0, la directory con gli otto FITS osservati e un percorso nuovo per la ricevuta. I nomi degli output sono gli ID del piano seguiti da -rgb.fits e -weight.fits. Il kit H/K include le fonti necessarie alla replica offline.