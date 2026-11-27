# BKL-046 — Provenienza del rigetto AstroDrizzle nell'associazione ACS 11677

Ho recuperato da MAST il trailer completo e i primi 57.600 byte dei prodotti DRC e DRZ. Le carte D001DATA–D012DATA identificano sei esposizioni sui due chip. Il DRC elenca i prodotti FLC e il DRZ quelli FLT. Entrambi rimandano alla tabella CRDS `37g1550cj_mdz.fits`, verificata a parte. I due prefissi contengono le carte necessarie per questi riscontri. Gli header completi e i pixel dei prodotti combinati non sono stati scaricati.

Nelle ultime due esecuzioni registrate nel trailer, AstroDrizzle 3.11.0 usa la riga FITS 4 della tabella, adatta a sei immagini. Il passo di rigetto termina in entrambi i casi. I parametri coincidono: reset del bit 4096, rigetto attivo, soglie SNR 3,5 e 3,0, scale 1,2 e 0,7, espansione di un pixel. Il trailer contiene anche passaggi precedenti con rigetto disattivato. Il verificatore distingue queste fasi dalle due finali.

Questa ricostruzione individua i parametri registrati a monte delle differenze FLT/FLC già osservate. Per verificare quali flag siano attribuiti correttamente servono una rielaborazione controllata e un riferimento indipendente. Il replay coincide. Nessuna elaborazione AstroDrizzle o PixInsight è stata avviata.

[Guida DrizzlePac](https://hst-docs.stsci.edu/drizzpac/chapter-7-data-quality-checks-and-trouble-shooting-problems/7-1-inspecting-the-drizzled-products-from-mast) · [Archivio HST MAST](https://archive.stsci.edu/missions-and-data/hst)