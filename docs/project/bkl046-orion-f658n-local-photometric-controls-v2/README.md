# BKL-046 — Controlli fotometrici locali per Orione F658N

La prova verifica se lo scarto delle due pose da 509 s rispetto alle due da 150 s compare anche nelle sorgenti vicine alla coppia di saturazione 5/5. Le sorgenti di controllo sono selezionate esclusivamente dalla prima posa da 150 s, ordinando i massimi locali per contrasto e imponendo separazione sul rivelatore. Le pose da 509 s non influenzano la selezione. Il confronto ripete il raggio diagnostico di 3 pixel, con correzione PAM, PHOTFLAM e fondo robusto, e richiede quattro aperture complete, SNR formale di almeno 20, astrometria coerente e accordo delle due pose brevi entro il 3%. Il confronto a luminosità simile richiede un flusso fra metà e il doppio di quello del candidato.

| Area di ricerca nella prima posa | Selezionati | Controlli utilizzabili | Luminosità simile |
|---|---:|---:|---:|
| Riquadro di semiampiezza 240 px | 8 | 0 | 0 |
| Riquadro esteso di semiampiezza 820 px | 64 | 1 | 0 |

Nel riquadro esteso il solo controllo misurabile mostra scarti di −0,20% e −2,03% nelle due pose da 509 s. Sul candidato 5/5 gli scarti sono +21,28% e +20,38%. Il protocollo richiedeva otto controlli complessivi e quattro a luminosità comparabile. La scarsità del supporto impedisce di stimare uno scarto comune di campo o attribuire quello del candidato a una causa fisica. Il precedente esito di esclusione del riferimento rimane valido. Zero esecuzioni native e chiusure scientifiche.

Il dossier H conserva il programma, le due coppie protocollo/rapporto, i due manifest degli intervalli e una copia per ogni blocco FITS distinto. Per ripetere una variante, usare il suo protocollo e manifest con la directory ranges. Gli argomenti sono directory della variante, directory runtime, dossier header, output, modo replay, dossier fotometrico e dossier delle pose da 509 s.

[Confronto delle pose da 509 s](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/4d2376484395aaf88f3426ded0a66d9035085e29/docs/project/bkl046-orion-f658n-alternative-holdout-509-v1)
