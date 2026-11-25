# BKL-046 — Riferimento dei byte per Stream34 v11

Su DSG-Shared un lettore Python indipendente ha riletto gli otto input congelati del launcher `0b029846da0412875e26595e2ead8361bc35fcef2c882ec2be95303b9582bdd1`. Ha verificato dimensione e SHA-256 di ogni file, per un totale di 139.469.422 byte. Il piano e il validatore della ricevuta erano entrambi legati all'impronta del launcher.

| Byte del file | Blocchi di dati attesi a 1 MiB | Byte dell'ultimo blocco |
| ---: | ---: | ---: |
| 0 | 0 | 0 |
| 1 | 1 | 1 |
| 1.048.576 | 1 | 1.048.576 |
| 1.048.577 | 2 | 1 |
| 3.145.745 | 4 | 17 |
| 603 | 1 | 603 |
| 33.558.528 | 33 | 4.096 |
| 100.667.392 | 97 | 4.096 |

Il lettore ha usato i risultati per costruire una ricevuta sintetica. Il validatore v11 l'ha accettata sul piano semantico e ha respinto dieci varianti, fra cui hash e conteggio errati, blocchi fuori limite, file aperto, identità o prenotazione diversa, dichiarazioni di memoria continua o di elaborazione scientifica e presenza simultanea di un esito di errore. La decisione ha lasciato disabilitate chiusura, rilascio e ripetizione.

Il conteggio dei blocchi è il riferimento calcolato dal lettore Python. La ricevuta v11 espone il massimo per file, senza contare le chiamate di lettura. Restano da osservare nel processo ammesso l'API nativa, la custodia dei file e la sua effettiva uscita. Il collaudo non ha richiesto ammissioni e ha prodotto zero chiusure scientifiche.

| Evidenza | SHA-256 |
| --- | --- |
| Piano congelato | `66dc8a2c794e004b63f60f51b21b837d41a13cacd0e025523c1a854600073c95` |
| Verificatore indipendente | `bdc615a121e1b8eb08646172925d2f86b1c9d9643cb6259b855f90ade219b959` |
| Riscontro offline | `73c5682ec23ed90629c4d022a799c38f26cae8d5557e6da07b7408e92ddc64b9` |

Lo ZIP BKL046-Stream34-riferimento-byte-v11-verificabile.zip è stato riletto da H:. Il verificatore estratto ha riprodotto la ricevuta byte per byte. SHA-256 dello ZIP: f901ed69f433d3ddd0bd9621b87aa25db878e0ce0a92d9a8a9853fd02dc8b902.
