# BKL‑046 · Perdita di segnale diffuso nella correzione a strisce

Il test inietta profili analitici nei due contrasti TV4 riservati alla verifica. Applica gli stessi operatori a strisce con e senza il segnale e misura la differenza. Il risultato coincide con la trasformazione diretta del profilo iniettato entro 1,16 × 10⁻¹⁴ DN. Il confronto comprende cinque regioni, più orientamenti dei filamenti e quattro modalità di correzione, per 440 esiti. [Controllo del rumore con strisce disgiunte](BKL-046-TV4-RUMORE-STRISCE.md)

| Profilo | Casi entro il 5% sia sul flusso centrale sia sulla forma, con entrambe le correzioni | Errore mediano firmato del flusso centrale | Errore relativo L2 massimo |
| --- | ---: | ---: | ---: |
| Compatto | 10/10 | <0,01% | <0,01% |
| Filamento corto | 40/40 | <0,01% | <0,01% |
| Filamento lungo | 20/40 | −19,18% | 72,62% |
| Componente diffusa larga | 10/10 | −1,83% | 2,30% |
| Costante | 10/10 | 0% | <0,01% |

I filamenti lunghi paralleli a righe o colonne perdono rispettivamente segnale con la correzione di riga o di colonna. Con entrambe le correzioni, ciascuno dei due orientamenti assiali perde in mediana il 38,36% del flusso nell’apertura circolare centrale, con perdite fino al 53,05%. Tutti i 20 casi diagonali restano entro le soglie per le strisce e le posizioni campionate.

Il flusso integrato nell’intera regione resta invariato alla precisione numerica perché ogni riferimento è centrato sulla propria media regionale. La conservazione del totale lascia quindi possibili perdite locali e alterazioni di forma. Non si tratta di una misura di SNR o di una prova nativa. Le iniezioni digitali quantificano la sensibilità a questi profili e non simulano l’acquisizione di fotoni. L’asse `DIFFUSE_BACKGROUND/1` resta aperto.

SHA‑256 della ricevuta `e0c14f59cee31b9e3442d05d720963164af7656c1230ad136fe950edd7ab53f5`.
