# BKL-046 · Procedura di contesa fra host per ProcessInstance v601

Il collaudo usa un file di prova isolato su J:. Il ruolo Host è vincolato al PC principale e il ruolo VM a DSG-Shared. Entrambi usano lo stesso identificatore di prova in una directory nuova. Ogni segnale scambiato riporta identificatore, ruolo, macchina e fase. I segnali vengono pubblicati dopo scrittura e chiusura. Il test si arresta se manca un passaggio entro 40 secondi.

Il PC principale detiene il primo byte e attende che la VM registri il rifiuto. Dopo il rilascio la VM acquisisce il byte e il PC principale verifica il rifiuto in direzione inversa. Dopo il secondo rilascio, il PC principale riacquisisce il blocco. Entrambi rileggono i byte del file di prova e controllano che siano identici all’origine. La procedura usa solo il file di prova e i segnali.

Due prove generali su DSG-Shared, una con lo script archiviato su H:, hanno completato lo scambio in entrambe le direzioni e osservato `0x80070021` durante la contesa. Il programma distingue la prova generale dal collaudo fra due host. La sessione Codex del PC principale non era raggiungibile da questa VM. Il collaudo con un processo effettivo sul PC principale resta da eseguire prima di attestare la convivenza dei writer. Il registro autorevole è stato riletto e punta ancora a v600.

| Evidenza | SHA-256 |
| --- | --- |
| Programma di collaudo | 2eb9e29f0e2722657b1741c378bb452f5cc5fdfe6dee5c69d030a6bd25b378bc |
| Riscontro della prova generale | 6e99e707d92faf6024f9f4517075313add01e8e0f8bf3ca92dc5c2d78c0905fa |
