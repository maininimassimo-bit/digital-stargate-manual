# BKL-046 · Conservazione del segnale con scala e bordi favorevoli su M8/M20

Sulle 148 prove che superavano entrambi i controlli di residuo e sulle 27 coppie a scala unitaria si iniettano tre profili positivi dopo avere allineato e scalato la posa bersaglio. Il picco iniettato è 2 ADU. Si rifà la stima di offset o piano su tutto il supporto comune prima e dopo ogni iniezione. La verifica misura la perdita di flusso nell'apertura centrale e l'errore relativo L2 su tutto il supporto comune. Il fit usa le mediane delle celle e non riceve la forma del segnale.

| Profilo | Perdita mediana di flusso con offset | Perdita mediana di flusso con piano | Errore L2 mediano con piano | Prove entro 5% su flusso e forma |
| --- | ---: | ---: | ---: | ---: |
| Filamento corto | 35,8% | 35,8% | 22,9% | 0/148 con entrambi |
| Filamento lungo | 46,8% | 46,8% | 27,6% | 0/148 con entrambi |
| Diffuso largo | 50,5% | 50,5% | 76,8% | 0/148 con entrambi |

Anche i 27 controlli a scala unitaria falliscono per tutti i profili e per entrambi i modelli. Il superamento dei controlli di residuo lascia quindi non qualificata la conservazione del segnale iniettato. In questi controlli positivi e centrati gran parte della perdita si osserva già con l'offset. Si riusano pose e stime della stessa sequenza. Restano aperti i test con maschere indipendenti, altre posizioni e contrasti, altri campi, un riferimento astronomico e una prova nativa.

Il generatore riceve il protocollo, la directory dell'archivio di riferimento con capture e stellar, il rapporto completo del test congiunto, la directory delle dipendenze NumPy 2.3.5 e Astropy 7.2.0 e una directory di uscita nuova. Gli archivi H/K conservano le 525 iniezioni e i risultati per metodo. [Test congiunto](../bkl046-m8-m20-scale-and-held-out-edges-v1/README.md)