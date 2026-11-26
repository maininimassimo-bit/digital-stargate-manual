# BKL-046 · Scie F606W a gain 2 fra le visite 05 e 02 del programma 17979

L'associazione centrale JFLN05040 contiene due FLT da 400 s. Per entrambe le pose a gain 2 ho riusato le due esposizioni da 40 s della visita 02 e le soglie di preselezione già pubblicate. Le due visite hanno lo stesso puntamento di catalogo, circa 84 giorni di distanza e una differenza di 52,37° nel PA_V3. La proiezione WCS è un primo tentativo di abbinamento, senza un fit astrometrico indipendente fra le visite.

| Primo motivo di rifiuto | jfln05ykq | jfln05ymq |
| --- | ---: | ---: |
| Flag misti nella scia | 149 | 172 |
| Picco breve non abbinato | 130 | 116 |
| Due abbinamenti brevi discordanti | 103 | 95 |
| Nucleo breve o supporto con flag | 2 | 2 |
| Totale candidati | 384 | 385 |

I conteggi riguardano componenti per esposizione, con possibile ripetizione della stessa sorgente. Le quattro componenti che superano i passaggi di abbinamento falliscono il controllo sui flag del riferimento breve. Il risultato descrive la preselezione corrente. Gli scarti di abbinamento non provano l'assenza delle corrispondenti sorgenti. Le misure fotometriche di scie a gain 2 rimangono da qualificare. [Flag ACS/CALACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)

Per ripetere, estrarre questo archivio e rendere disponibili nella stessa directory i due FITS brevi e le due mappe PAM dello studio della visita 02. Eseguire `verifica.py` con runtime Astropy, runtime SciPy, directory dei file, protocollo della posa e un nuovo percorso di uscita. Le impronte dei dati sono fissate nei due protocolli. [Studio della visita 02](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/8da015387313cb9e9b0f31c5bbf4e0b6cf9ef40f/docs/project/bkl046-acs-17979-gain2-trail-screen-v1)
