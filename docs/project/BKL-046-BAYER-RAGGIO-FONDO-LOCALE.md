# BKL-046 · Sensibilità del colore Bayer al raggio e al fondo locale

L'asse FILTER_COLOR/3 resta aperto. Ho rieseguito la fotometria lineare nei due campi, esportando i flussi blu e rossi a raggi di 6, 7 e 8 pixel. Entrambi i fondi, mediana locale e piano ai minimi quadrati, usano gli stessi pixel dell'anello 9–13 px. Le misure originali di crescita a 6–8 px si riproducono esattamente e il colore a 6 px con fondo mediano coincide con la precedente fotometria XP, entro la precisione numerica. [Stima del fondo nella fotometria di apertura](https://docs.astropy.org/projects/photutils/en/stable/user_guide/aperture.html)

Il confronto mantiene i riferimenti spettrali congelati: Canon di serie per IC 1805 e i due profili Sony con L-Pro per M8/M20. Per ciascun metodo di ricostruzione, le sei combinazioni di raggio e fondo sono confrontate sulla calibrazione A con esclusione a turno di una zona di stima. La combinazione così scelta è verificata sulle stelle riservate, sia in A sia in B. Si adegua solamente lo zero cromatico. Il criterio era abbassare il P90 di almeno 0,010 mag in entrambe le calibrazioni rispetto a mediana e raggio 6 px.

| Campo | Stelle di verifica | P90 del cambio di raggio 6→8 (mag) | P90 del cambio di fondo a raggio 8 (mag) | P90 differenza A/B nella variante selezionata (mag) |
| --- | ---: | ---: | ---: | ---: |
| IC 1805 | 9 | 0,015–0,027 | 0,010–0,017 | 0,011–0,018 |
| M8/M20 | 19 | 0,063–0,065 | 0,156–0,169 | 0,017–0,020 |

Nessuna combinazione scelta sulla stima ha ridotto il P90 di almeno 0,010 mag in entrambe le calibrazioni. Per M8/M20, quando la stima ha selezionato il fondo planare a raggio 6, il P90 sulle stelle di verifica è peggiorato di 0,008–0,018 mag. Il forte effetto della scelta del fondo a raggio 8 documenta la sensibilità del campo e non stabilisce il vero livello del fondo. La concordanza A/B è minore dello scarto tra stimatori di fondo, ma le due riduzioni condividono le pose scientifiche e non sono repliche indipendenti. Restano da controllare contaminazione da sorgenti vicine, struttura del fondo e adeguatezza della PSF in ogni banda.

## Riproducibilità

- SHA-256 della ricevuta `e76f51c22e86c71078deafed0a51ee46b90d75c3a3ebbc387d7d695d42ef98fe`.
- Archivio H: `Produzione/2026-10-13/Digital-StarGate-PixInsight/archives/BKL046-Bayer-raggio-fondo-e76f51c22e86.zip`.
- L'archivio contiene codice, flussi da entrambe le sequenze e risultati. Gli ingressi preesistenti sono fissati per impronta.
- Zero avvii nativi e zero chiusure scientifiche.
