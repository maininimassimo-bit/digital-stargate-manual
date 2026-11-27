# BKL-046 · Precisione richiesta per riferimenti indipendenti del fondo

Sulla griglia M8/M20 il test ipotizza sei misure del fondo senza contributo astronomico, a coordinate fissate. Il fondo vero è costante per il modello offset e affine per il piano. Si assume un limite assoluto comune per l'errore di ogni riferimento, anche quando gli errori hanno lo stesso segno. Si propaga l'errore a flusso in apertura e forma sul supporto comune. Per il massimo si valutano tutti i 64 vertici della scatola degli errori. Entrambe le misure d'errore sono funzioni convesse dei sei errori dei riferimenti.

| Disposizione dei riferimenti per il piano | Filamento corto | Filamento lungo | Diffuso largo |
| --- | ---: | ---: | ---: |
| Distribuiti | 0,00738 ADU | 0,01042 ADU | 0,04183 ADU |
| Concentrati in un angolo | 0,00105 ADU | 0,00149 ADU | 0,00505 ADU |
| Allineati | Fit non identificabile | Fit non identificabile | Fit non identificabile |

I valori sono il massimo errore ammesso **per riferimento** affinché entrambi gli indicatori restino entro il 5% per le iniezioni da 2 ADU. Con il profilo diffuso largo, 0,02 ADU rispetta il limite nella disposizione distribuita e lo supera in quella concentrata. Un errore comune ai sei riferimenti si trasferisce come offset e richiede controllo anche con una buona geometria.

Le misure dei riferimenti sono ipotetiche. Il bilancio riguarda solo il contributo del fondo affine e non include rumore della posa, errore di registrazione o difformità del modello. Nessun riferimento reale è stato qualificato. Il catalogo stellare disponibile riguarda la posizione delle sorgenti puntiformi. Per applicare il bilancio servono misure indipendenti effettive, un modello validato del fondo e una prova nativa.

Il generatore riceve protocollo, kit delle iniezioni, kit del riferimento M8/M20, rapporto congiunto completo, dipendenze e file di uscita nuovo. [Supporto dei profili iniettati](../bkl046-m8-m20-scale-edges-known-profile-mask-v1/README.md)