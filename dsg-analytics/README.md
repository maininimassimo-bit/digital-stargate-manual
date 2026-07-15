# Digital StarGate Observatory Analytics

Prima release operativa per trasformare i log archiviati nel repository in KPI, riepiloghi e report Markdown.

## Componenti
- collector: wrapper PowerShell per la raccolta gia esistente
- analyzer: analisi NINA, PHD2 e meteo
- reporter: generazione report Markdown/JSON
- knowledge-base: indice storico delle sessioni
- GitHub Actions: esecuzione automatica su nuovi pacchetti sessione

## Avvio rapido
1. Copiare la cartella nel repository `digital-stargate-manual`.
2. Installare Python 3.11+ sul PC di analisi o usare GitHub Actions.
3. Eseguire `python analyzer/analyze_session.py --session <percorso-sessione>`.
