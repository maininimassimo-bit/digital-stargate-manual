# Digital StarGate – Technical Manual

Repository sorgente del manuale tecnico dell'Osservatorio Remoto di Manciano.

- Codice documento: `DSG-TM-001`
- Formato sorgente: Markdown
- Stato: Draft
- Autore: Massimo Mainini

## Struttura

- `chapters/` capitoli del manuale
- `appendices/` allegati tecnici
- `assets/` immagini, diagrammi e screenshot
- `templates/` modelli per procedure, checklist e registri

## Generazione documenti

Il repository è predisposto per una futura conversione in Word o PDF mediante Pandoc.

Esempio:

```bash
pandoc chapters/*.md -o DSG-TM-001_Digital_StarGate.docx --toc
```
