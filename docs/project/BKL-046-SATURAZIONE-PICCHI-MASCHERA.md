# BKL‑046 · Picchi e bordi nelle maschere di saturazione

Il controllo usa 37 scene di stelle Moffat, di cui 36 con una compagna e una isolata. Confronta posa lunga troncata, guida breve, sostituzione netta del nucleo e sostituzione con transizione di tre pixel. Le quattro modalità riusano gli stessi campioni di rumore per ogni scena e per ogni spostamento residuo della guida. Il rilevatore di picchi è congelato e viene applicato anche alle scene ideali.

| Errore residuo della guida | Errore RMS relativo mediano al bordo, sostituzione netta | Errore RMS relativo mediano al bordo, sostituzione sfumata | Casi entro il 5%, netta / sfumata |
| --- | ---: | ---: | ---: |
| 0 | 4,32% | 4,76% | 132/148 / 96/148 |
| 0,25 pixel | 13,16% | 14,31% | 0/148 / 0/148 |
| 0,50 pixel | 24,97% | 27,14% | 0/148 / 0/148 |

Otto delle 36 scene doppie risultano risolte nella verità secondo il rilevatore. Tutte le modalità conservano le 32 coppie risolte per spostamento, comprese le quattro repliche di rumore per scena. La sola guida divide da tre a quattro casi per spostamento che il rilevatore non separa nella verità. Entrambe le sostituzioni non mostrano tali divisioni né picchi non abbinati. La copertura delle coppie risolte resta circoscritta alle otto geometrie.

La sfumatura non migliora il criterio RMS nel dominio testato. Questo criterio registra gli scarti rispetto ai pixel ideali sui due lati del bordo, senza misurare direttamente oscillazioni o aloni sotto la soglia del rilevatore. Il taglio è ideale e l’offset della guida è noto. Righe di spillamento, saturazione del rivelatore, dati strumentali e maschere native restano da verificare. L’asse `SATURATION_BLEND/4` resta aperto.

SHA‑256 della ricevuta `25d13d631ba528873c2376602527f14caff807295e2114432ba6f5d3692300e0`.
