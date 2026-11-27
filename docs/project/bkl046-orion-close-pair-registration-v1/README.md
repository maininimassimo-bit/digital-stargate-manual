# BKL-046 — Registrazione locale delle coppie di Orione

Il test usa le sei esposizioni ACS/WFC F555W verificate nel dossier precedente. Il riquadro di ricerca ha semiampiezza di 520 pixel ed è ritagliato sui bordi del chip. Il programma cerca massimi di campo con supporto DQ pulito, contrasto, SNR e separazione minima. Esclude 35 pixel attorno al sistema in esame. Riserva un terzo delle rilevazioni della prima posa alla verifica, ordinandole per ascensione retta prima di formare le associazioni. La traslazione è stimata sulle altre rilevazioni. Un modello affine è riportato a fini diagnostici con lo stesso insieme di verifica.

| Sistema | Stelle rilevate nelle due immagini | Associazioni per la stima | Associazioni nella verifica | P90 della traslazione |
|---|---:|---:|---:|---:|
| H97 232 | 140 / 140 | Nessuna traslazione coerente | — | — |
| H97 345 | 140 / 140 | Nessuna traslazione coerente | — | — |
| H97 488 | 140 / 140 | 21 | 4 | 148,7 mas |

Nessuno dei tre confronti soddisfa la tolleranza congelata di 20 mas. Per H97 488 il modello affine dà un P90 di 166,3 mas e lo scarto fra i due massimi resta 406 mas dopo la traslazione. Il limite di 140 rilevazioni per immagine è stato raggiunto. Le rilevazioni sono picchi d'immagine e non tutti sono stelle. Le corrispondenze di verifica sono quelle univoche entro la finestra stabilita e l'errore è condizionato alle corrispondenze disponibili. Restano da verificare l'identità dei riferimenti di campo con un catalogo astrometrico indipendente e la stabilità del modello sul campo comune. Zero esecuzioni native e chiusure scientifiche.

Lo script accetta directory del dossier, directory delle dipendenze, dossier del supporto sul rivelatore, percorso di output e modo replay.

[Verifica del supporto sul rivelatore](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/7ec7a542cd63deccbbe9e552e3e86b1981271744/docs/project/bkl046-orion-close-pair-detector-support-v1)
