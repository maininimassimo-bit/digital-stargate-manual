# GD153 · Copertura osservata nelle coppie ACS/WFC

Sono state riesaminate le nove coppie FLT sullo stesso amplificatore B, nei tre filtri e nelle tre visite GD153. Per ogni coppia, si proiettano i centri dei pixel dell'apertura di riferimento attraverso il WCS distorto dei due membri e si allinea la proiezione al centro misurato della sorgente. Un pixel è coperto se almeno un membro dispone di tutti i contributi bilineari a peso non nullo con DQ zero e valori SCI e ERR validi. Come confronto è stato calcolato anche il supporto del vicino più prossimo. Un controllo numerico con un pixel escluso verifica la distinzione fra i due metodi.

| Raggio | Coppie con copertura bilineare completa | Pixel mancanti per coppia |
| --- | ---: | ---: |
| 3 px | 9/9 | 0 |
| 5 px | 0/9 | 2 |
| 10 px | 0/9 | 17–19 |

Lo spostamento misurato tra i due centri di ogni coppia è al massimo 0,0412 pixel. A 5 pixel le lacune ricorrono alle stesse coordinate del rivelatore in tutti e tre i filtri di una visita, e due visite condividono anche la stessa coppia di coordinate. La guida ACS distingue la rimozione dei raggi cosmici con CR-SPLIT dalla copertura dei difetti fissi, per la quale servono spostamenti del telescopio. [ACS Instrument Handbook, operazioni CCD](https://hst-docs.stsci.edu/acsihb/chapter-4-detector-performance/4-3-ccd-operations-and-limitations)

Riunendo le maschere delle sei pose per filtro, **su tre visite**, il supporto geometrico è completo anche a 10 pixel in tutti e tre i filtri. Questo offre dati per validare una ricostruzione con maschere artificiali. Usare i pixel di un'altra visita come flusso misurato nella visita in esame eliminerebbe l'indipendenza del confronto temporale e richiederebbe un modello di trasferimento tra epoche. Il calcolo non interpola flussi, non misura CTE o risposta spettrale e non collauda la registrazione astrometrica assoluta. Zero nuove misure fotometriche, zero avvii nativi e zero chiusure scientifiche.

Il replay dagli archivi riletti su H: ha riprodotto il JSON byte per byte. SHA-256 del riscontro `20427f06bb82220747944b699bbd721725aea5679f32e4edb4c0215d1ebc5746`. SHA-256 dell'archivio `c927ce336527e9fda274e3b8bb4789888cb70e23820ea5c976b6dd53d7312674`.

[Misure e selezione delle pose](BKL-046-GD153-ACS-AMPLIFICATORE-B.md).
