# BKL-046 · Controllo esterno della registrazione su Omega Centauri

Il programma GO16380 di monitoraggio ACS/WFC offre una coppia F606W da 40 s, due guide da 150 s e due pose da 400 s. Il primo gruppo nominale è stato escluso prima delle misure perché entrambe le pose brevi registrano la mancata acquisizione della stella guida. Nel gruppo esterno selezionato, gli header delle sei pose non riportano quell'anomalia e la separazione astrometrica dal campo GO14949 è di circa 59,8 gradi. I ruoli sono stati assegnati in ordine temporale nelle associazioni CALACS stabilite dai metadati. [Programma STScI GO16380](https://www.stsci.edu/hst/observing/program-information?program=16380)

Le pose brevi selezionate sono `jeg056a9q` e `jeg056abq`. Le guide sono `jeg057chq` e `jeg057cjq`. Le due pose profonde `jeg055llq` e `jeg055lnq` sono state valutate separatamente. Il protocollo conserva l'esclusione DQ prima dell'ordinamento dei picchi, il centroide congelato, la partizione spaziale, il minimo di 24 stelle e 8 tasselli in ciascuna partizione per sensore e il limite P90 di 0,1 pixel.

| Passaggio | Riferimenti validi sui due sensori |
| --- | ---: |
| Selezione nella prima posa da 40 s | 3.080 |
| Rimisura nella seconda posa da 40 s | 2.650 |
| Rimisura nelle due guide da 150 s, rispettivamente | 1 / 0 |
| Rimisura nelle due pose da 400 s, rispettivamente | 17 / 16 |
| Intersezione dei cinque fotogrammi, per ciascuna posa profonda | 0 / 0 |

Nelle due guide, i motivi prevalenti di rifiuto sono la qualità della zona di misura e il picco decentrato rispetto alla previsione WCS. Il P90 della traslazione non è misurabile con questo allineamento. La buona ripetibilità della coppia breve rende il set adatto a una diagnosi separata della proiezione verso le guide, da stimare sui soli tasselli di calibrazione e verificare sui tasselli riservati. L'asse `SATURATION_BLEND/4` resta aperto. Nessuna prova nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Selezione dai metadati | `64bb91b1e5f4bc2981423a2eab30f884a2d6c4aeb9aae397651b8ffe9f405b84` |
| Ricevuta prima posa profonda | `c6958e77af9f1c2a3898bd9c5f9300da68a0818da2778bce9f71f32fc6a124c5` |
| Ricevuta seconda posa profonda | `0eb5c6ad39d06ce85654cff00221785d359fc8cf6bef947ba362c1ecfd0c49d0` |
