# BKL‑046 · Minimi interni nei fit PSF con rumore

Il controllo completa il riesame numerico dei 547 adattamenti ellittici originariamente non stazionari. I 286 casi vicini al limite di ellitticità sono documentati nella prova al bordo. Qui si riproducono dal seme i 261 casi rimanenti e si verifica un minimo locale interno senza cambiare i vincoli del modello. [Controllo al limite di ellitticità](BKL-046-PSF-LIMITE-ELLITTICITA.md)

| Rapporto segnale-rumore | Casi riesaminati | Minimi interni verificati | Casi ancora senza minimo interno verificato |
| --- | ---: | ---: | ---: |
| 25 | 161 | 129 | 32 |
| 100 | 100 | 82 | 18 |
| Totale | 261 | 211 | 50 |

Il controllo richiede stazionarietà a due passi di differenziazione, curvatura locale positiva, distanza dai limiti e dal punto circolare, e residuo equivalente o inferiore a quello originario. Tutti i 50 casi residui falliscono la stazionarietà. Trenta terminano vicino al punto circolare, dove questo modello a scala maggiore fissata non è differenziabile nella parametrizzazione in ellitticità.

Sommando i due audit, 481 dei 547 arresti hanno un minimo locale numericamente verificato e 66 restano irrisolti. I fit prossimi alla circolarità richiedono un trattamento esplicito della non identificabilità dell’angolo. I 481 minimi verificati non cambiano le decisioni scientifiche della prova con rumore. L’asse `PSF_PIXEL/2` resta aperto.

SHA‑256 della ricevuta `6d166f73e65c9749f6e246121d118b22dbb745307bbc257cb075859c0d4adf55`.
