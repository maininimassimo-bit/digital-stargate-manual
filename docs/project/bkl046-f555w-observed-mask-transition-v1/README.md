# BKL-046 — Transizione della maschera con profili stellari e flag DQ osservati

L'esperimento per SATURATION_BLEND/4 usa 19 associazioni CALSPEC F555W. Un fotogramma pulito fornisce il riferimento osservato, l'altro la guida. La forma della regione da sostituire deriva da 18 riquadri di Orione F555W con flag full well o ADC, proiettati sul centro e limitati a 10 pixel di raggio. Questa operazione simula quali pixel sarebbero sostituiti. Il fotogramma di riferimento resta disponibile per misurare l'errore, senza simulare il trasporto di carica o il segnale di una posa lunga reale.

Traslazione e piano di fondo sono stimati nell'anello da 13 a 17 pixel. Il primo confronto stima anche la scala della guida dall'anello. Il secondo fissa la scala a uno dopo aver verificato la stessa durata di esposizione nei due FLT. I raccordi sono netti o a coseno di larghezza 1, 2 o 3 pixel. La larghezza di 1 pixel coincide con il raccordo netto sulla griglia discreta. Si misurano lo scarto assoluto del flusso a raggio 8 pixel e l'errore RMS del gradiente attraverso i bordi fra pixel adiacenti.

Le 18 maschere in 19 associazioni producono 342 confronti per metodo. In entrambi i metodi 270 confronti hanno supporto incompleto. I 72 misurabili corrispondono a quattro associazioni di due sorgenti. I conteggi non sono prove indipendenti di accuratezza.

| Scala della guida | Raccordo | Errore mediano assoluto di flusso | Entro 5% | RMS mediano del gradiente al bordo |
|---|---|---:|---:|---:|
| Stimata dalle ali | Netto | 33,70% | 0/72 | 2.560 e⁻ |
| Stimata dalle ali | 2 px | 34,27% | 0/72 | 2.208 e⁻ |
| Stimata dalle ali | 3 px | 33,63% | 0/72 | 1.982 e⁻ |
| Unitaria per pari durata | Netto | 5,25% | 36/72 | 2.530 e⁻ |
| Unitaria per pari durata | 2 px | 3,11% | 40/72 | 2.105 e⁻ |
| Unitaria per pari durata | 3 px | 2,09% | 48/72 | 1.970 e⁻ |

Il miglioramento del gradiente non assicura il recupero del flusso. La scala unitaria è giustificata qui dalle durate uguali e dalle condizioni della prova. La sua efficacia non fissa la scala fra pose di durata diversa o con diversa risposta strumentale. Restano da valutare acquisizioni lunghe realmente sature con riferimento breve indipendente, strutture estese, transizioni adattive, aloni e separazione di picchi. Zero esecuzioni native e chiusure scientifiche.

[Dossier CALSPEC](https://github.com/maininimassimo-bit/digital-stargate-manual/commit/5be45b7d03a04eb99c65ebafb9b0f1e27dbb05c7) · [Provenienza delle maschere di Orione](https://github.com/maininimassimo-bit/digital-stargate-manual/commit/ad6f2c14cb54d84c8a0faa6ee147e628937abfec)
