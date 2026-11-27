# BKL-046 · Copertura Gaia con pose spostate GO16380

Le due pose brevi aggiuntive `jeg056bnq` e `jeg056bpq` provengono dall'associazione CALACS 61809042. I file completi coincidono nei primi 65.536 byte con gli header già acquisiti per la selezione. La prova riproietta le stesse 548 sorgenti del [campione Gaia](BKL-046-GO16380-MISURE-DA-GAIA.md) nei due nuovi fotogrammi. Per contare una zona diversa del rivelatore, entrambe le proiezioni devono cadere su un altro sensore o spostarsi di almeno 32 pixel rispetto ad A40. Il centroide e i veti DQ restano quelli congelati, con limite di 0,7 pixel per confermare un centroide fra le due pose.

| Sensore di origine | Sorgenti nel campione | Presenti in entrambe le nuove pose, in altra zona del rivelatore | Nuove coppie valide | Prima o nuova coppia valida, stima / verifica |
| --- | ---: | ---: | ---: | ---: |
| 1 | 278 | 0 | 0 | 20 / 23 |
| 2 | 270 | 118 | 0 | 17 / 20 |

Per il sensore 2, la prima posa spostata ha respinto 100 sorgenti per qualità e 18 per picco decentrato. Il conteggio usa i semi della WCS nominale. Questi rifiuti non misurano separatamente un eventuale errore addizionale di registrazione. Il sensore 1 è fuori dal campo. Questa coppia non aumenta la copertura verificata ed esclude il suo uso diretto come complemento per entrambi i sensori.

L'asse `SATURATION_BLEND/4` resta aperto. Nessuna modifica alle maschere o ai pixel scientifici, prova nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo | `1eacded5413c9b6c4df175aad890936c28eac2e4a82ae83dbd8f1744d67af510` |
| Prima posa spostata | `3633af6e4cf24db831240decda00e0a7fb92a41a528a0cb83b8a23f929c03dd1` |
| Seconda posa spostata | `110d59a06ef51a1e2a2846f4d4055d4c835b5ef01066baf20f05a55917d70bda` |
| Ricevuta per sorgente | `b26519154eb3038cfb1f643ee86fee08f4591e57e34c6d20173f7f38ad7101e1` |
