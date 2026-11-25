# BKL-046 — Risposta dei flat TV4 RED a esposizioni escluse

Per DIFFUSE_BACKGROUND/2 ho ricalcolato la prova precedente sui 13 flat MRI FLBB24/RED del 4 marzo 2003 e ottenuto la stessa ricevuta byte per byte. Il nuovo confronto misura quanto bene i termini spaziali del modello predicano un tempo d'integrazione quando tutte le pose a quel tempo sono escluse dalla stima. Le medie degli altri quattro tempi hanno lo stesso peso. Per ciascuno dei 1.280 blocchi ho confrontato una retta e una quadratica. [Archivio TV4 NASA PDS](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)

| Integrazione esclusa | Pose escluse | Dispersione delle ripetizioni, DN | RMSE lineare, DN | RMSE quadratica, DN |
| ---: | ---: | ---: | ---: | ---: |
| 13,5 ms | 3 | 0,256 | 1,353 | 0,559 |
| 33,5 ms | 2 | 0,244 | 0,975 | 0,475 |
| 103,5 ms | 3 | 0,317 | 0,825 | 0,681 |
| 303,5 ms | 2 | 0,481 | 1,979 | 1,670 |
| 1.003,5 ms | 3 | 0,798 | 7,804 | 24,615 |

La quadratica riduce lo scarto sui tre tempi interni e a 13,5 ms. All'estremo alto, dove entrambi i modelli estrapolano da tempi fino a 303,5 ms, lo scarto della quadratica più che triplica. A tutti e cinque i tempi lo scarto predittivo supera la dispersione delle ripetizioni attorno alla loro media.

I tempi di integrazione crescono nello stesso ordine di acquisizione. Questo confronto non distingue la non linearità del sensore da una variazione del banco, dell'illuminazione o della temperatura nel tempo. I blocchi spaziali e le ripetizioni non sono acquisizioni indipendenti. Per qualificare il trasferimento serve una sequenza indipendente con livelli alternati e misure di bias e illuminazione. DIFFUSE_BACKGROUND/2 resta aperto. Zero prove native e zero chiusure scientifiche.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | `7de6fa00184daab137effe6e2d52d72cb5b49edde898a4d79824defd24787b5b` |
| Programma | `cdca2343b016053c5c1c6920405090256cb667bcab12529b8109f038d642e144` |
| Riscontro | `e7d1b648e3ec0db4b1efe8f63f5c4cdb89126ef79df4274bb80e000ed5e18a75` |
