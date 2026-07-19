\# Digital StarGate Analytics



Benvenuto nel portale Analytics del progetto \*\*Digital StarGate\*\*.



Questa sezione raccoglie gli strumenti di analisi, i report e la dashboard generati automaticamente dalla pipeline di elaborazione delle sessioni osservative.



\---



\## Accesso rapido



\- \[Dashboard Analytics](dashboard.html)

\- \[Validazione dello storico](history-validation.md)

\- \[Riepilogo configurazioni](configuration-summary.md)



\---



\## Cosa puoi consultare



La dashboard consente di analizzare:



\- andamento delle sessioni osservative;

\- ore complessive di acquisizione;

\- numero di immagini raccolte;

\- target osservati;

\- distribuzione dei filtri utilizzati;

\- configurazioni strumentali;

\- statistiche operative.



\---



\## Dashboard



Per accedere direttamente alla dashboard interattiva:



\[Apri la Dashboard](dashboard.html){ .md-button .md-button--primary }



\---



\## Report disponibili



\### Validazione dello storico



Contiene l'esito dei controlli di coerenza sui dati acquisiti.



→ \[Apri il report](history-validation.md)



\### Configurazioni



Mostra il riepilogo delle configurazioni rilevate durante le sessioni.



→ \[Apri il riepilogo](configuration-summary.md)



\---



\## Pipeline Analytics



La pipeline viene eseguita con:



```powershell

python .\\dsg-analytics\\build\_all.py

```



Le principali elaborazioni comprendono:



1\. Consolidamento dello storico

2\. Analisi delle configurazioni

3\. Estrazione delle metriche dei target

4\. Aggregazione dei risultati

5\. Generazione della dashboard



\---



\## Roadmap



\### Versione 3.1

\- Portale Analytics integrato nel manuale MkDocs

\- Navigazione centralizzata

\- Accesso ai report



\### Versione 3.2

\- Validazione avanzata dei target

\- Report di qualità dei dati



\### Versione 3.3

\- Observatory Intelligence

\- KPI evoluti

\- Analisi stagionali

\- Statistiche per telescopio

