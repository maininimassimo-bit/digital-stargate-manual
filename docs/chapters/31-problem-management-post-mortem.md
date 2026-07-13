# Capitolo 31 – Problem Management e Post-Mortem

**Codice documento:** DSG-TM-001-31  
**Revisione:** 0.1 Draft

## 31.1 Scopo

Questo capitolo definisce il processo per trasformare gli incidenti ricorrenti in azioni strutturali di miglioramento. Un incidente ripristinato non è necessariamente un problema definitivamente risolto.

## 31.2 Distinzione tra incidente e problema

| Termine | Definizione |
|---|---|
| Incidente | Interruzione o degrado operativo |
| Problema | Causa reale o potenziale di uno o più incidenti |
| Workaround | Soluzione temporanea |
| Known Error | Problema noto con causa o workaround documentato |

## 31.3 Quando aprire un Problem Record

Aprire un problema quando:

- lo stesso incidente si ripete almeno due volte;
- l’impatto è CRITICAL o EMERGENCY;
- la causa non è stata identificata;
- il workaround richiede intervento manuale;
- il rischio residuo è considerato elevato.

## 31.4 Analisi della causa radice

Metodi consigliati:

- 5 Why;
- diagramma causa-effetto;
- timeline degli eventi;
- confronto dei log;
- test A/B controllati;
- analisi delle modifiche recenti.

## 31.5 Modello di post-mortem

Ogni post-mortem deve contenere:

1. sintesi dell’evento;
2. impatto operativo;
3. timeline;
4. causa radice;
5. fattori contribuenti;
6. azioni immediate;
7. azioni preventive;
8. owner e scadenze;
9. evidenze di chiusura.

## 31.6 Procedura DSG-PROC-031-01

1. Raccogliere i dati entro 24 ore dall’evento.
2. Ricostruire la timeline tecnica.
3. Identificare i punti di controllo mancanti.
4. Definire azioni correttive e preventive.
5. Aggiornare manuale, checklist o configurazioni.
6. Verificare l’efficacia dopo la prima sessione utile.

## 31.7 Registro Known Error

| ID | Sintomo | Causa | Workaround | Correzione definitiva | Stato |
|---|---|---|---|---|---|
| KE-001 | Pulse Guide Failed | DA VALIDARE | Riconnessione CPWI/PHD2 | DA VALIDARE | Aperto |

## 31.8 KPI

- problemi aperti;
- tempo medio di chiusura;
- azioni preventive completate;
- incidenti evitati dopo la correzione;
- percentuale di post-mortem completati.
