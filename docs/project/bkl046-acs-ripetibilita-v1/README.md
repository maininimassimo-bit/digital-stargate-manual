# BKL-046 – Ripetibilità ACS e scelta delle esposizioni

Le due visite di GRW+70D5824 hanno due esposizioni per filtro a 3 e 5 pixel. A 3 pixel la pesatura frazionaria riduce lo scarto medio assoluto tra pose da 0,303% a 0,193%, con miglioramento in quattro coppie su sei. A 5 pixel lo scarto medio passa da 0,190% a 0,182%, con miglioramento in tre coppie su sei.

Scegliendo una sola esposizione per filtro e visita, a 3 pixel lo scarto F658N/F606W con pesatura frazionaria varia da −0,59% a +0,40%. Per F658N/F660N resta positivo in tutte le 16 combinazioni a entrambi i raggi. Le combinazioni riusano le stesse esposizioni. I loro estremi sono un riepilogo descrittivo e il trasferimento tra visite resta da qualificare.

Per riprodurre i due riscontri dai tassi di flusso fissati negli allegati, salva localmente tutti i file di questa directory, apri PowerShell 7 nella stessa directory ed esegui i controlli.

~~~powershell
./ripetibilita-intra-visita-v1.ps1 -VerifyOnly
./sensibilita-scelta-posa-visite-v1.ps1 -VerifyOnly
~~~

Gli script verificano le impronte delle misure e confrontano l'output ricalcolato con i JSON pubblicati. La riproduzione parte dai tassi di flusso e lascia a monte il calcolo da FITS. Restano zero controlli qualificati e zero chiusure scientifiche.

[Confronto con pixel interi e pesi frazionari](../BKL-046-ACS-PIXEL-BORDO-v1.md)
