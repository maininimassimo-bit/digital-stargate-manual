# BKL-046 · Margini numerici dei riferimenti CFA XDRZ

Sono stati riletti i FITS e i sei XDRZ di shear del piano congelato. Il calcolo riproduce l'area di sovrapposizione con le primitive poligonali del generatore archiviato. Il confronto usa il predicato esatto del verificatore CFA v4.

| Controllo | Risultato offline |
| --- | --- |
| Maschera verde in coordinate del rivelatore o del riferimento | Stesso supporto non nullo. Massima differenza assoluta 1 nei pesi e 0,31 nell'intensità sul supporto comune. Il comparatore distingue le due risposte. |
| Maschera sul canale sbagliato e nessuna maschera | Intensità e pesi coincidono. Il controllo sul canale sbagliato si interpreta insieme al caso verde e ai parametri riletti. |
| Conversione dei cinque riferimenti a Float32 e ritorno | Tutti passano. Sullo shear, differenza massima 1,15 × 10⁻⁷ nei pesi e 2,98 × 10⁻⁸ nelle intensità. |
| Matrici dello shear usate come coordinate a centro zero | La variante centro zero coincide col riferimento. La variante serializzata a 0,5 cambia 52 campioni del supporto RGB e raggiunge una differenza di 0,559 nei pesi. |
| Matrici convertite usando l'origine serializzata | Entrambe le varianti coincidono col riferimento entro la tolleranza. La differenza massima nei pesi della variante 0,5 è 2,66 × 10⁻¹⁵. |

Se una prova nativa producesse due corrispondenze, il comparatore v4 la fermerebbe per ambiguità. L'equivalenza riprodotta con la conversione esplicita è una spiegazione compatibile con tale esito, da verificare sui prodotti effettivi e sui parametri. Nessuna soglia è stata modificata. La conversione Float32 provata sugli oracoli riguarda la rappresentazione dei dati e lascia aperti gli arrotondamenti interni, l'origine interpretata e i risultati di PixInsight. [Piano e candidato](../bkl046-cfa-v4-review-intake/README.md)

Per replicare, passare al programma la directory del protocollo, la directory del piano a tre ingressi, il file verifica.py, la directory NumPy 2.3.5/Astropy 7.2.0 e il nuovo percorso per la ricevuta. Le copie esatte dei due kit sorgente sono incluse nella custodia H/K.