# BKL-046 — Rilettura delle evidenze ACS, fondo diffuso e CFA v4

## Osservazioni ACS

L'archivio conservato su H: contiene 92 file verificati, inclusi 24 FITS. Da una copia isolata di 43 membri sono stati rigenerati cinque rapporti con impronte identiche. Il test identifica il runtime Python e le versioni delle librerie. L'analisi CTE per stelle brillanti resta una sensibilità a un modello fuori dal campione primario di calibrazione. [Visite ACS](BKL-046-ACS-VISITE-INDIPENDENTI-v1.md)

## Fondo diffuso

L'analisi appaiata di 729 iniezioni su pose M8 e M20 individua 133 casi con residuo di fondo migliore e grado stabile. Nessuno dei 133 conserva flusso e forma entro il 5% richiesto. Per una decisione di accettazione occorre misurare direttamente il recupero di flusso e forma per le morfologie dichiarate.

## CFA v4

Il preflight del pacchetto fissato ha confermato i percorsi e 3.824 file del runtime. Il supervisore offline non invia rilascio in assenza della ricevuta d'archivio o se il controllo finale fallisce. In caso di risposta persa o sconosciuta invia una sola richiesta e lascia la decisione alla rilettura del registro. La riconciliazione è stata collaudata separatamente su registri di prova. Restano la posa protetta, l'iscrizione dei revisori, le approvazioni ARB e RQ e l'ammissione R4.

## Riscontri verificati su H:

| Riscontro | SHA-256 |
| --- | --- |
| Archivio ACS | `7833f865b9bba285eb857e090db9c985e05f57190f7aca798e27cbdecf92d850` |
| Replay ACS | `9cd2b19f77d666a1349d7f3f43b10e14e1ae1a4dbb6661e6bd6b8bd652d7e5e7` |
| Controllo sul fondo diffuso | `42ddba38e0a405b4849a47445c6f61dedb279fedc3a8bec3f12e412c5b6a2957` |
| Rilascio CFA offline | `c6fddaa4744f913906871eab4ab788a8390db191c4dbc297fb7eaf138ca33edf` |
| Riconciliazione CFA | `a03c040ed490f0eca3f5c11b439550c035595f7967f86355b88a6b928b82f16d` |
| Preflight CFA | `e731518ec7c9a4dfb972eb8c1b364918b42098e1022cfc84c502af6bacfc6cdd` |

Nessuna ammissione reale richiesta. I criteri di accettazione restano aperti e le chiusure scientifiche a zero.
