# BKL-046 · Confronto diagnostico su supporto comune nelle quattro pose ACS

Il rapporto precedente ha respinto la replica jfdp02vdq perché il supporto dell'apertura era 303/317, sotto il 97%. Per identificare l'effetto della maschera ho misurato tutte e quattro le pose sugli stessi 303 offset. Le centrature e le componenti DQ 256 provengono dall'analisi precedente. Un offset era già escluso nella posa primaria o nelle pose brevi. La maschera della replica ne rimuove altri 13. [Selezione e rifiuto della replica](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/10ecd56e074331d58c59b5965990870fb7470a60/docs/project/bkl046-acs-17656-saturated-core-sensitivity-v1)

Con il fondo a 35–48 px, i 13 offset valgono lo 0,175% della somma registrata nella posa primaria e lo 0,196% e lo 0,192% in quelle brevi. Rimuoverli aumenta lo scarto primario di circa 0,020 punti percentuali. Le due pose lunghe differiscono dello 0,11–0,12% sui tre fondi. Rispetto alla media delle pose brevi si misurano +3,08–3,09% nella primaria e +3,20–3,21% nella replica.

La maschera aggiuntiva non spiega lo scarto lungo-breve misurato sul supporto comune. La quota di flusso nei pixel esclusi è osservabile soltanto nelle tre immagini che conservano quei pixel. La replica resta respinta per l'apertura completa. Il risultato descrive una singola sorgente e non qualifica il recupero di scie estese o la causa dello scarto.

Per ripetere, eseguire `verifica.py` con runtime Astropy, runtime SciPy, directory estratta dello studio ACS17656 originale con i FITS brevi e la PAM, directory estratta dello studio di sensibilità, protocollo e nuovo file di uscita. I due studi precedenti e i FITS sono verificati attraverso le impronte vincolate.
