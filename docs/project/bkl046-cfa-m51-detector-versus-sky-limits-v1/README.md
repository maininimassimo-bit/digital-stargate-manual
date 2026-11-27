# BKL-046 · Ricorrenza dei codici RAW nel riferimento del cielo e del sensore

Sulle tre pose EOS 6D di M51 ho riletto le coordinate dei campioni a 12.507 DN o più, secondo il limite per canale del decoder, e dei campioni esattamente a 14.042 o 14.043 DN. Le coordinate sono pixel nativi del mosaico visibile. Ho proiettato i campioni della prima posa nelle altre due con le similarità già stimate sulle stelle, i cui P90 sui riferimenti esclusi dalla stima sono 0,594 e 0,781 px.

| Condizione | Posa centrale, sensore / cielo | Posa finale, sensore / cielo |
| --- | ---: | ---: |
| Limite decoder, qualsiasi fase entro 2 px | 23 / 369 su 405 | 23 / 366 su 397 |
| Codici 14.042–14.043, qualsiasi fase entro 2 px | 21 / 319 su 346 | 21 / 318 su 341 |

Sono conteggi di campioni della posa di partenza che trovano almeno un vicino nella posa di destinazione. Le associazioni non sono imposte uno a uno. Spostare la previsione celeste di 32 px nei quattro versi dà zero riscontri entro 4 px. I rapporti includono anche il requisito della stessa fase e i raggi di 1 e 4 px. Nelle finestre campionate, la maggior parte dei valori estremi segue la registrazione del campo. I campioni ricorrenti sul sensore richiedono dark EOS 6D abbinati per distinguere difetti, contributi fissi e coincidenze. Il confronto non misura full well o recupero del flusso e non chiude il criterio sulla saturazione per canale.

Per ripetere, eseguire `verifica.py` con la directory del protocollo, la directory estratta dello studio CFA precedente, il rapporto delle associazioni stellari, i pacchetti rawpy estratti dal wheel, la directory delle dipendenze SciPy, le DLL VCLibs e un nuovo file di uscita. [Studio sui limiti RAW](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/1aa418144f7df776547e9dfe0e6101b266078736/docs/project/bkl046-cfa-native-code-limits-v1)
