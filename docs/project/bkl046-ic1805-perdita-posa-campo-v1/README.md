# IC 1805 e perdita della stessa posa nel campo CFA

I 38 file candidati alla rimozione sono associati alle 72 stelle tramite gli ordinali di validazione del riscontro sulla registrazione nel verde. Il produttore della geometria ha controllato che l’elenco ordinato delle stelle per posa coincidesse prima di accodare gli spostamenti per metà intercalata. Il riferimento è escluso dalle rimozioni. Una stella senza contributo dalla posa rimossa conserva il valore nominale.

| Larghezza deposito (px) | Pose che causano almeno una discesa sotto 2 contributi effettivi | Massimo numero di stelle che scendono sotto 2 nella stessa rimozione | Pose che lasciano almeno una cella vuota |
| --- | ---: | ---: | ---: |
| 1,00 | 2/38 | 1/72 | 0/38 |
| 0,70 | 13/38 | 3/72 | 1/38 |

A 0,70 px la rimozione della posa 17 fa scendere tre stelle sotto soglia, mentre una la supera. Il totale passa da 66 a 64. La posa 13 lascia una cella vuota per una stella, mentre due superano la soglia e il totale sale a 67. Il numero effettivo può aumentare se viene tolto un contributo di peso dominante. Il riscontro conserva le transizioni in entrambe le direzioni insieme al conteggio delle celle vuote.

L’ordinale della posa parte da 1 dopo il riferimento. L’impronta per posa è calcolata sulla stringa del nome del membro ZIP, usando UTF-8. Lo script usa soltanto la libreria standard Python e i tre JSON con impronta fissata, nell’ordine geometria, associazioni, rimozioni locali, seguiti da un nuovo percorso di uscita. La prova usa geometria nominale e pesi di area. Non propaga errori di registrazione, maschere, incertezze fotometriche o covarianze. Due contributi effettivi è una soglia diagnostica. Nessuna prova nativa o chiusura scientifica.
