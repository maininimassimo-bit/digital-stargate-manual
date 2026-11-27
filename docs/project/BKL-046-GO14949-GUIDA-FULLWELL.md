# BKL-046 · Prequalifica GO14949 delle guide per il full well

L'asse `SATURATION_BLEND/4` resta aperto. La prova offline su DSG-Shared ha riutilizzato le 677 associazioni del [test a profondità mista](BKL-046-GO14949-REGISTRAZIONE-PROFONDITA.md), incluse le esclusioni originali, e la separazione spaziale in tasselli da 512 pixel. La posa F606W di 400 s è il prodotto MAST `jdg301bwq_flc.fits`, SHA-256 `5c71129fcfc2d1d20f7d31592f66f0dc9f0b9609736595b08a6befbe70b554b9`. I due protocolli fissano per sensore almeno 24 stelle e 8 tasselli in ciascuna partizione, con P90 radiale affine ≤ 0,1 pixel sui tasselli esclusi dalla stima.

| WCS | Sensore | Stelle per stima / verifica | Tasselli per stima / verifica | P90 affine |
| --- | --- | ---: | ---: | ---: |
| Alternativo A | 1 | 0 / 1 | 0 / 1 | — |
| Alternativo A | 2 | 1 / 1 | 1 / 1 | — |
| Primario, relativo a Gaia DR3 | 1 | 29 / 18 | 13 / 9 | — |
| Primario, relativo a Gaia DR3 | 2 | 36 / 40 | 14 / 15 | 0,101571 px |

Con il WCS primario non si sono ripresentati i rifiuti per picco decentrato o spostamento eccessivo osservati col WCS alternativo. Sul sensore 2 la sola traslazione ha ottenuto un P90 di 0,095700 pixel come confronto diagnostico. Il criterio congelato usa il modello affine. Dei 63 casi del sensore 2 ammessi alla lettura delle maschere sul gruppo di verifica, tre avevano un nucleo con soli bit di full well o zeri e due avevano flag misti. I tre casi rimangono osservazioni preliminari. Su entrambi i sensori il numero di casi ammessi alla prequalifica geometrica è zero.

Non sono stati sostituiti pixel scientifici né eseguite prove native. I due casi storici della prova fotometrica V40 sono distinti e nessuno di questi risultati ne estende l'accettazione. La traslazione merita verifica su un nuovo gruppo indipendente con sufficiente copertura in entrambi i sensori e con controlli separati per il trasferimento ai nuclei saturi.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo e WCS alternativo | `f998ad38a5da30c9abc66c54933d60e6e28283794fe914fdd5ba3ef66afe4f0c` |
| Ricevuta WCS alternativo | `e04cfd6e5dad8c4be001a3e0a0ce79a2f522b02412da2bd4ab754652eb13572a` |
| Protocollo WCS primario | `9bb264918e07c013c1e7b1ce3df47b6c03812896496e548141da65a9cf5a003c` |
| Ricevuta WCS primario | `9bbec741ccec34d49733035ead3e719aa655abd826066a0d254425b15ead1ddb` |
