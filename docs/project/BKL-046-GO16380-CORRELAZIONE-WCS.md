# BKL-046 · Correzione della proiezione WCS nel campo GO16380

Il [primo controllo su Omega Centauri](BKL-046-GO16380-CONTROLLO-ESTERNO.md) aveva trovato una coppia breve valida ma zero riferimenti utilizzabili nelle cinque pose. Il seguito conserva le stesse pose e le stesse soglie. Stima una correzione di semina separatamente per ciascuna esposizione e ciascun sensore, tramite correlazione tra tasselli pari nel sistema della prima posa breve. La ricerca è limitata a ±48 pixel per asse. Occorrono almeno otto tasselli in accordo e una maggioranza stretta. I centroidi sono poi misurati sui dati originali con le regole DQ e di segnale congelate.

Le due guide hanno restituito uno spostamento di semina di −1 pixel in X e −3 in Y su entrambi i sensori. I 16 tasselli di stima hanno concordato. Applicando la correzione e la traslazione residua stimata sui soli tasselli pari, l'intersezione nelle cinque pose è diventata valutabile.

| Sensore | Stelle per stima / verifica | P90 radiale su tasselli di verifica | P90 con margine di 56 px | Riferimenti con margine |
| --- | ---: | ---: | ---: | ---: |
| 1 | 78 / 61 | 0,506314 px | 0,515569 px | 41 stelle, 14 tasselli |
| 2 | 68 / 70 | 0,447378 px | 0,443979 px | 41 stelle, 14 tasselli |

Il margine aggiunge al raggio della ricerca la finestra di misura e la tolleranza di consenso. La verifica con margine conserva la stima originale della traslazione. Su entrambi i sensori il P90 resta sopra **0,1 pixel**. La correlazione ha recuperato riferimenti, mentre lo scarto residuo impedisce di qualificare il trasferimento ai nuclei saturi. L'asse `SATURATION_BLEND/4` resta aperto. Il seguito usa la prima posa profonda `jeg055llq` e non estende questo risultato alla seconda posa. Nessuna prova nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo | `028e9e8107ceb5e36cd0e984644ebb5ac32b41f8c7821f7012b09b2f712fe7f7` |
| Ricevuta con le misure sui tasselli di verifica | `0ab6a06657e2fb6da6c6922a1565e3d786ee68bba50b1c892b13e0c88decd07c` |
| Analisi di sensibilità al margine | `3ffc63382e585af38e8deb6d35c42d3ca63e479be2e1f6a551910fde4bffc611` |
