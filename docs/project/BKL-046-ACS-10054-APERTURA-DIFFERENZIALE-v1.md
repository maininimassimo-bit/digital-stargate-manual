# BKL-046 — Apertura fotometrica ACS nel programma HST 10054

Con due esposizioni per banda e per stella, il rapporto misurato di GD71 diviso per quello di GD153 è stato confrontato con il corrispondente rapporto sintetico da CALSPEC.

| Rapporto | Scarto differenziale a 3 px | Scarto differenziale a 5 px |
| --- | ---: | ---: |
| F658N/F606W | -3,794% | +0,143% |
| F658N/F660N | +0,533% | +0,130% |
| F660N/F606W | -4,304% | +0,013% |

I rapporti con F606W cambiano di circa quattro punti percentuali. Un fattore di correzione comune alle due stelle per lo stesso rapporto di bande si cancella. La sensibilità ai coefficienti ACS/WFC tabulati a 0,5 arcsec è stata calcolata usando 10 pixel come approssimazione esplorativa. A quel raggio, per GD71 resta una sola esposizione F660N utilizzabile. [Manuale ACS STScI, sezione 5.1.2](https://hst-docs.stsci.edu/acsdhb/chapter-5-acs-data-analysis/5-1-photometry)

Per qualificare questo controllo, fissare l'apertura prima del confronto, derivare la correzione locale per visita, verificare il dominio CTE e propagare l'incertezza comune fra bande. Verificare poi le scelte su osservazioni indipendenti. Controlli qualificati e chiusure scientifiche restano a zero.

Impronte SHA-256 dei riscontri archiviati su H: fisico.

- Confronto differenziale: `8c5a8c83c670c75085b254940f2ad5dbb03d95e0e802e779a9c1f01a444ce6af`
- Sensibilità ai coefficienti tabulati: `cfd4b75bea20793a2a0edfdf9c8528b05df9bc07302b10014a5159dbc8cc7422`
